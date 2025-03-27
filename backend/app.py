import os
import io
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase
from openai import OpenAI

app = FastAPI()

# --- CORS configuration ---
origins = [
    "http://localhost:3000",  # Frontend React
    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration de Neo4j et OpenAI ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "azertyuiop"  # Remplacez par votre mot de passe Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD), database="trash")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Helper : simulation des données de bilan ---
def get_balance_sheet_data() -> pd.DataFrame:
    data = {
        "Company": ["BNP Paribas", "BNP Paribas"],
        "Statement": ["Balance Sheet", "Balance Sheet"],
        "Period": ["Q1 2024", "Q4 2023"],
        "CurrentAssets": [2500, 2450],
        "NonCurrentAssets": [5000, 4900],
        "TotalAssets": [7500, 7350],
        "CurrentLiabilities": [2000, 1950],
        "NonCurrentLiabilities": [2500, 2450],
        "TotalLiabilities": [4500, 4400],
        "Equity": [3000, 2950]
    }
    return pd.DataFrame(data)

# --- Endpoint 1 : Retourner les données de bilan (CSV) ---
@app.get("/balance-sheet-data", response_class=JSONResponse)
def balance_sheet_data():
    df = get_balance_sheet_data()
    csv_text = df.to_csv(index=False)
    return {"csv": csv_text}

# --- Endpoint 2 : Générer le JSON du Knowledge Graph via OpenAI ---
@app.post("/generate-graph-json", response_class=JSONResponse)
def generate_graph_json():
    df = get_balance_sheet_data()
    csv_text = df.to_csv(index=False)
    prompt = f"""
You are an expert in financial data and knowledge graph extraction.
Using the following simulated CSV data, generate a detailed JSON representing a comprehensive Financial Knowledge Graph.
Focus solely on the 'Balance Sheet' document type for BNP Paribas.
The graph must follow this schema:

Entities (Nodes):
  - Company (e.g., BNP Paribas)
  - FinancialStatement (e.g., Balance Sheet)
  - FinancialItem (e.g., Current Assets, Non-current Assets, Total Assets, Current Liabilities, Non-current Liabilities, Total Liabilities, Equity)
  - Period (e.g., "Q1 2024", "Q4 2023")
  
Relationships (Edges):
  - (Company)-[:HAS_STATEMENT]->(FinancialStatement)
  - (FinancialStatement)-[:HAS_ITEM]->(FinancialItem)
  - (FinancialItem)-[:HAS_VALUE {{period: "Q1 2024", value: 2500}}]->(Period)
  - Use BREAKDOWN relationships (without an explicit contribution property) to indicate which FinancialItems contribute to totals.
  - Use EQUATION relationships (with a 'role' property) to indicate how FinancialItems are calculated.

The JSON must have two keys: "nodes" and "relationships".
For each node, include:
  - "id": a unique identifier (e.g., "n1", "n2", …)
  - "label": the node type (e.g., "Company", "FinancialStatement", "FinancialItem", "Period")
  - "name": the value extracted from the CSV for that entity.
For each relationship, include:
  - "source": the id of the source node,
  - "target": the id of the target node,
  - "type": the relationship type (e.g., "HAS_STATEMENT", "HAS_ITEM", "HAS_VALUE", "BREAKDOWN", "EQUATION"),
  - And include additional properties such as "period", "value", or "role" where applicable.

Here is the simulated CSV data:
{csv_text}

Respond only with the JSON.
"""
    import re
    import json

    def extract_json(text):
        # Recherche le premier bloc commençant par { et se terminant par }
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print("Erreur de décodage JSON:", e)
                raise e
        else:
            raise ValueError("Aucun bloc JSON trouvé dans la réponse.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in financial knowledge graph extraction."},
                {"role": "user", "content": prompt}
            ]
        )
        json_output = response.choices[0].message.content
        graph_data = extract_json(json_output)
    except Exception as e:
        print("Erreur dans generate_graph_json:", e)
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI: {e}")

    return graph_data

# --- Endpoint 3 : Insérer le graph dans Neo4j (avec transaction) ---
@app.post("/insert-graph", response_class=JSONResponse)
def insert_graph():
    try:
        # Générer le nouveau graphe depuis OpenAI
        graph_data = generate_graph_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating graph JSON: {e}")

    try:
        with driver.session() as session:
            # Démarrer une transaction
            with session.begin_transaction() as tx:
                # 1. Supprimer tous les nœuds et relations existants
                tx.run("MATCH (n) DETACH DELETE n")
                print("Previous graph deleted.")

                # 2. Insertion des nœuds
                for node in graph_data.get("nodes", []):
                    cypher_node = f"MERGE (n:{node['label']} {{id: $id}}) SET n.name = $name"
                    params_node = {"id": node["id"], "name": node["name"]}
                    tx.run(cypher_node, params_node)
                    print(f"Node inserted: {node['label']} - {node['id']}")

                # 3. Insertion des relations
                for rel in graph_data.get("relationships", []):
                    # Vérification minimale que les clés 'source' et 'target' existent
                    if "source" not in rel or "target" not in rel:
                        print("Relation ignorée (source/target manquant):", rel)
                        continue

                    if rel["type"] == "HAS_VALUE":
                        params_rel = {
                            "source": rel["source"],
                            "target": rel["target"],
                            "period": rel.get("period"),
                            "value": rel.get("value")
                        }
                        cypher_rel = """
                            MATCH (a {id: $source}), (b {id: $target})
                            MERGE (a)-[r:HAS_VALUE {period: $period, value: $value}]->(b)
                        """
                    elif rel["type"] == "EQUATION":
                        if "role" in rel and rel["role"] is not None:
                            params_rel = {
                                "source": rel["source"],
                                "target": rel["target"],
                                "role": rel.get("role")
                            }
                            cypher_rel = """
                                MATCH (a {id: $source}), (b {id: $target})
                                MERGE (a)-[r:EQUATION {role: $role}]->(b)
                            """
                        else:
                            params_rel = {
                                "source": rel["source"],
                                "target": rel["target"]
                            }
                            cypher_rel = """
                                MATCH (a {id: $source}), (b {id: $target})
                                MERGE (a)-[r:EQUATION]->(b)
                            """
                    else:
                        params_rel = {
                            "source": rel["source"],
                            "target": rel["target"]
                        }
                        cypher_rel = f"""
                            MATCH (a {{id: $source}}), (b {{id: $target}})
                            MERGE (a)-[r:{rel['type']}]->(b)
                        """
                    tx.run(cypher_rel, params_rel)
                    print(f"Relationship inserted: {rel['type']} from {rel['source']} to {rel['target']}")

                # Valider la transaction
                tx.commit()
                print("Transaction commitée avec succès.")
        return {"status": "Graph inserted into Neo4j successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting graph: {e}")


# --- Endpoint 4 : Calculer la contribution des actifs pour un period donné ---
@app.get("/asset-contributions/{period_name}", response_class=JSONResponse)
def asset_contributions(period_name: str):
    query = """
    MATCH (fs:FinancialStatement {name:"Balance Sheet - BNP Paribas"})-[:HAS_ITEM]->(sub:FinancialItem),
          (sub)-[v:HAS_VALUE]->(p:Period {name: $period}),
          (fs)-[:HAS_ITEM]->(total:FinancialItem {name:"Total Assets - BNP Paribas"}),
          (total)-[v_total:HAS_VALUE]->(p)
    WHERE (sub)-[:BREAKDOWN]->(total)
    RETURN sub.name AS SubItem, v.value AS SubValue, v_total.value AS TotalValue, v.value / v_total.value AS ContributionRatio
    """
    contributions = []
    try:
        with driver.session() as session:
            results = session.run(query, {"period": period_name})
            for record in results:
                contributions.append({
                    "SubItem": record["SubItem"],
                    "SubValue": record["SubValue"],
                    "TotalValue": record["TotalValue"],
                    "ContributionRatio": float(record["ContributionRatio"])
                })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying asset contributions: {e}")
    return {"contributions": contributions}

# --- Endpoint 5 : Analyse classique via OpenAI ---
@app.post("/classic-analysis", response_class=JSONResponse)
def classic_analysis():
    df = get_balance_sheet_data()
    csv_text = df.to_csv(index=False)
    prompt = f"""
Based on the following balance sheet data for BNP Paribas, analyze the key drivers of its financial position.
Data:
{csv_text}
Provide a clear, professional summary.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        analysis = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI for classic analysis: {e}")
    return {"classic_analysis": analysis}

# --- Endpoint 6 : Analyse basée sur le graph via OpenAI ---
@app.post("/graph-analysis", response_class=JSONResponse)
def graph_analysis():
    contributions_q1 = asset_contributions("Q1 2024")["contributions"]
    contributions_q4 = asset_contributions("Q4 2023")["contributions"]
    graph_insights = contributions_q1 + contributions_q4
    prompt = f"""
Based on the following graph-derived insights regarding BNP Paribas's balance sheet:
{graph_insights}
Provide a clear, professional analysis explaining how the breakdown of current and non-current assets contributes to total assets and how this relates to the overall financial position.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        analysis = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI for graph analysis: {e}")
    return {"graph_analysis": analysis}

# --- Endpoint 7 : Visualiser le graph (image PNG) ---
from fastapi.responses import StreamingResponse

@app.get("/visualize-graph", response_class=StreamingResponse)
def visualize_graph():
    query = "MATCH (n)-[r]->(m) RETURN n, r, m"
    G = nx.DiGraph()
    try:
        with driver.session() as session:
            results = session.run(query)
            for record in results:
                n1 = record["n"]
                n2 = record["m"]
                id1 = n1.get("id") or f"node_{id(n1)}"
                id2 = n2.get("id") or f"node_{id(n2)}"
                label1 = list(n1.labels)[0] if n1.labels else "Unknown"
                label2 = list(n2.labels)[0] if n2.labels else "Unknown"
                name1 = n1.get("name", "")
                name2 = n2.get("name", "")
                G.add_node(id1, label=label1, name=name1)
                G.add_node(id2, label=label2, name=name2)
                rel = record["r"]
                rel_type = rel.type
                G.add_edge(id1, id2, label=rel_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying graph: {e}")
    
    pos = nx.spring_layout(G, seed=42)
    # Assurez-vous d'utiliser le backend "Agg" de matplotlib dans votre fichier, avant l'import de pyplot:
    # import matplotlib
    # matplotlib.use("Agg")
    fig, ax = plt.subplots(figsize=(12, 8))
    node_labels = {node: f"{data['label']}:\n{data['name']}" for node, data in G.nodes(data=True)}
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color="lightblue", node_size=1500, font_size=8, ax=ax)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=8, ax=ax)
    ax.set_title("Knowledge Graph Visualization")
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


# --- (Optionnel) Endpoint racine pour test ---
@app.get("/", response_class=HTMLResponse)
def read_index():
    return HTMLResponse("<h1>Welcome to the Financial Knowledge Graph API</h1>")
