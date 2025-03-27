import io
import json
import re
import networkx as nx
import matplotlib.pyplot as plt
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from backend.config import driver
from backend.services.graph_service import (
    get_graph_relationships,
    generate_graph_json_data
)
from openai import OpenAI
import os

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/generate-graph-json", response_class=JSONResponse)
def generate_graph_json():
    try:
        graph_data = generate_graph_json_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI: {e}")
    return graph_data

@router.post("/insert-graph", response_class=JSONResponse)
def insert_graph():
    try:
        graph_data = generate_graph_json_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating graph JSON: {e}")

    try:
        with driver.session() as session:
            with session.begin_transaction() as tx:
                # Supprimer tous les nœuds et relations existants
                tx.run("MATCH (n) DETACH DELETE n")
                # Insertion des nœuds
                for node in graph_data.get("nodes", []):
                    cypher_node = f"MERGE (n:{node['label']} {{id: $id}}) SET n.name = $name"
                    params_node = {"id": node["id"], "name": node["name"]}
                    tx.run(cypher_node, params_node)
                # Insertion des relations
                for rel in graph_data.get("relationships", []):
                    if "source" not in rel or "target" not in rel:
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
                            params_rel = {"source": rel["source"], "target": rel["target"]}
                            cypher_rel = """
                                MATCH (a {id: $source}), (b {id: $target})
                                MERGE (a)-[r:EQUATION]->(b)
                            """
                    else:
                        params_rel = {"source": rel["source"], "target": rel["target"]}
                        cypher_rel = f"""
                            MATCH (a {{id: $source}}), (b {{id: $target}})
                            MERGE (a)-[r:{rel['type']}]->(b)
                        """
                    tx.run(cypher_rel, params_rel)
                tx.commit()
        return {"status": "Graph inséré dans Neo4j avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting graph: {e}")

@router.get("/visualize-graph", response_class=StreamingResponse)
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
