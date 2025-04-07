import json
import re
import networkx as nx
from backend.config import driver, OPENAI_API_KEY
from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_graph_relationships():
    """
    Queries Neo4j to retrieve all relationships in the graph.
    """
    query = "MATCH (n)-[r]->(m) RETURN n, r, m"
    relationships = []
    try:
        with driver.session() as session:
            results = session.run(query)
            for record in results:
                n1 = record["n"]
                n2 = record["m"]
                relationship = {
                    "source": n1.get("name"),
                    "sourceLabel": list(n1.labels)[0] if n1.labels else "Unknown",
                    "target": n2.get("name"),
                    "targetLabel": list(n2.labels)[0] if n2.labels else "Unknown",
                    "type": record["r"].type,
                    "properties": dict(record["r"])
                }
                relationships.append(relationship)
    except Exception as e:
        print("Error querying graph relationships:", e)
    return relationships

def compute_graph_metrics():
    """
    Computes graph metrics, for example density and the most central nodes.
    """
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
        print("Error querying graph for metrics:", e)
    metrics = {}
    try:
        metrics["density"] = nx.density(G)
        centrality = nx.degree_centrality(G)
        # Select the top 3 most central nodes
        top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:3]
        metrics["top_central_nodes"] = top_nodes
    except Exception as e:
        print("Error computing graph metrics:", e)
    return metrics

def get_relevant_subgraph(question: str):
    """
    Returns only those relationships where the type, source, or target
    contains words matching the question.
    """
    relationships = get_graph_relationships()
    relevant = []
    lower_q = question.lower()
    for rel in relationships:
        if lower_q in rel["type"].lower() or lower_q in rel["source"].lower() or lower_q in rel["target"].lower():
            relevant.append(rel)
    if not relevant:
        return relationships
    return relevant

def summarize_graph_insights(insights, metrics):
    """
    Constructs a concise summary of graph insights and metrics via OpenAI.
    """
    summary_prompt = f"""
You are a financial data summarization expert. Summarize the following graph insights and metrics into a concise summary in English, formatted in Markdown.

Graph Insights:
{json.dumps(insights, indent=2, ensure_ascii=False)}

Graph Metrics:
{json.dumps(metrics, indent=2, ensure_ascii=False)}

Provide a detailed summary highlighting key findings such as important relationships, central nodes, and overall graph characteristics.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a summarization expert."},
                {"role": "user", "content": summary_prompt}
            ]
        )
        summary = response.choices[0].message.content
    except Exception as e:
        summary = "Unable to summarize the graph insights."
    return summary

def generate_graph_json_data():
    """
    Generates the graph JSON via OpenAI based on balance sheet data.
    """
    from backend.services.balance_sheet import get_balance_sheet_data
    df = get_balance_sheet_data()
    csv_text = df.to_csv(index=False)
    prompt = f"""
You are an expert in financial data and knowledge graph extraction. Using the following simulated CSV data representing a modified Balance Sheet for BNP Paribas—with subtle, non-linear fluctuations and complex inter-item relationships—generate a detailed JSON representing a comprehensive Financial Knowledge Graph. Focus solely on the 'Balance Sheet' document type for BNP Paribas.

The graph must follow this schema:

**Entities (Nodes):**
  - **Company** (e.g., BNP Paribas)
  - **FinancialStatement** (e.g., Balance Sheet)
  - **FinancialItem** (e.g., CashEquivalents, ShortTermInvestments, AccountsReceivable, Inventory, OtherCurrentAssets, TotalCurrentAssets, PropertyPlantEquipment, IntangibleAssets, OtherNonCurrentAssets, TotalNonCurrentAssets, TotalAssets, ShortTermDebt, AccountsPayable, OtherCurrentLiabilities, TotalCurrentLiabilities, LongTermDebt, DeferredTaxLiabilities, OtherNonCurrentLiabilities, TotalNonCurrentLiabilities, TotalLiabilities, CommonStock, RetainedEarnings, AdditionalPaidInCapital, OtherEquity, TotalEquity, TotalLiabilitiesAndEquity)
  - **Period** (e.g., "Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024")

**Relationships (Edges):**
  - **(Company)-[:HAS_STATEMENT]->(FinancialStatement)**
  - **(FinancialStatement)-[:HAS_ITEM]->(FinancialItem)**
  - **(FinancialItem)-[:HAS_VALUE {{ period: "<Period>", value: <value> }}]->(Period)**

For each FinancialItem, generate a separate HAS_VALUE relationship for each period available in the CSV data, linking the item to the corresponding Period node with the correct value from the CSV.

  - Use **BREAKDOWN** relationships (without an explicit contribution property) to indicate which FinancialItems contribute to a total. For instance, *TotalCurrentAssets* is a sum of *CashEquivalents*, *ShortTermInvestments*, *AccountsReceivable*, *Inventory*, and *OtherCurrentAssets*.
  - Use **EQUATION** relationships (with a `role` property) to indicate how FinancialItems are calculated. For example, *TotalAssets* is the sum of *TotalCurrentAssets* and *TotalNonCurrentAssets*, and *TotalLiabilitiesAndEquity* is the sum of *TotalLiabilities* and *TotalEquity*.

The JSON must have two keys: "nodes" and "relationships".

For each node, include:
  - "id": a unique identifier (e.g., "n1", "n2", …)
  - "label": the node type (e.g., "Company", "FinancialStatement", "FinancialItem", "Period")
  - "name": the value extracted from the CSV for that entity.

For each relationship, include:
  - "source": the id of the source node
  - "target": the id of the target node
  - "type": the relationship type (e.g., "HAS_STATEMENT", "HAS_ITEM", "HAS_VALUE", "BREAKDOWN", "EQUATION")
  - And include additional properties such as "period", "value", or "role" where applicable.

Here is the simulated CSV data representing the modified Balance Sheet with subtle fluctuations:
{csv_text}

Respond only with the JSON.
"""
    def extract_json(text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print("JSON decode error:", e)
                raise e
        else:
            raise ValueError("No JSON block found in the response.")
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
        return graph_data
    except Exception as e:
        raise Exception(f"Error calling OpenAI: {e}")
