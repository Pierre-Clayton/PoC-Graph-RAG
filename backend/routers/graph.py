# backend/routers/graph.py
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.config import driver
from backend.services.graph_service import generate_graph_json_data
import os

router = APIRouter()

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
                # Delete all existing nodes and relationships
                tx.run("MATCH (n) DETACH DELETE n")
                # Insert nodes
                for node in graph_data.get("nodes", []):
                    cypher_node = f"MERGE (n:{node['label']} {{id: $id}}) SET n.name = $name"
                    params_node = {"id": node["id"], "name": node["name"]}
                    tx.run(cypher_node, params_node)
                # Insert relationships
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
        return {"status": "Graph successfully inserted into Neo4j."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting graph: {e}")

# --- New visualization endpoint ---
@router.get("/visualize-graph", response_class=JSONResponse)
def visualize_graph():
    """
    Instead of returning a static image, this endpoint returns the graph in a JSON format 
    suitable for interactive front-end visualization (e.g., using Cytoscape.js).
    """
    try:
        # Generate the graph JSON using the same function that builds your knowledge graph
        graph_data = generate_graph_json_data()
        
        # Convert the generated JSON to a format with nodes and edges arrays.
        nodes = graph_data.get("nodes", [])
        # Map relationships to edges. You can include additional properties if needed.
        edges = []
        for rel in graph_data.get("relationships", []):
            # Ensure the relationship has source and target fields.
            if "source" in rel and "target" in rel:
                edges.append({
                    "data": {
                        "source": rel["source"],
                        "target": rel["target"],
                        "label": rel["type"],
                        **({ "period": rel["period"], "value": rel["value"] } if rel.get("type") == "HAS_VALUE" else {}),
                        **({ "role": rel["role"] } if rel.get("type") == "EQUATION" and rel.get("role") is not None else {})
                    }
                })
        # Return the nodes and edges in a structure friendly for interactive libraries.
        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error visualizing graph: {e}")
