from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from backend.services.balance_sheet import get_balance_sheet_data
from backend.services.graph_service import (
    get_graph_relationships,
    compute_graph_metrics,
    get_relevant_subgraph,
    summarize_graph_insights
)
from openai import OpenAI
import os

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/classic-analysis", response_class=JSONResponse)
def classic_analysis(payload: dict = Body(...)):
    question = payload.get("question", "")
    df = get_balance_sheet_data()
    md_table = df.to_markdown(index=False)
    prompt = (
        f"Question:\n{question}\n\n"
        f"Data: {md_table}\n\n"
        "Please provide a detailed analysis in Markdown format, using tables if necessary."
    )
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

def build_values_table_from_graph():
    """
    Construit une table Markdown en se basant sur les relations HAS_VALUE récupérées depuis le graphe.
    Pour chaque relation, le FinancialItem (source) et la période (propriété period) sont associés à la valeur (propriété value).
    """
    relationships = get_graph_relationships()
    # Filtrer uniquement les relations de type HAS_VALUE
    has_value_rels = [rel for rel in relationships if rel["type"] == "HAS_VALUE"]
    
    # Organiser les valeurs par période et par FinancialItem
    data = {}
    for rel in has_value_rels:
        # On considère que "source" est le FinancialItem
        item = rel["source"]
        period = rel["properties"].get("period", "Inconnue")
        value = rel["properties"].get("value", "N/A")
        if period not in data:
            data[period] = {}
        data[period][item] = value
    
    # Déterminer tous les FinancialItems présents dans les données
    all_items = set()
    for period in data:
        all_items.update(data[period].keys())
    all_items = sorted(all_items)
    
    # Construction de la table Markdown
    header = "| Période | " + " | ".join(all_items) + " |"
    separator = "| --- " * (len(all_items) + 1) + "|"
    rows = [header, separator]
    for period in sorted(data.keys()):
        row = f"| {period} "
        for item in all_items:
            val = data[period].get(item, "")
            row += f"| {val} "
        row += "|"
        rows.append(row)
    
    return "\n".join(rows)

@router.post("/graph-analysis", response_class=JSONResponse)
def graph_analysis(payload: dict = Body(...)):
    question = payload.get("question", "")
    all_relationships = get_graph_relationships()
    metrics = compute_graph_metrics()
    relevant_relationships = get_relevant_subgraph(question)
    summary = summarize_graph_insights(relevant_relationships, metrics)
    
    # Récupérer directement les valeurs depuis le graphe et construire une table Markdown
    graph_values_table = build_values_table_from_graph()
    
    # Construit le prompt en incluant le résumé du graphe, les valeurs extraites depuis le graphe et la question
    prompt = (
        f"Graph Summary:\n{summary}\n\n"
        f"Graph Values Table:\n{graph_values_table}\n\n"
        f"Question: {question}\n\n"
        "Please provide a detailed analysis in Markdown format, using tables if necessary."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst with deep knowledge in graph-based financial analysis."},
                {"role": "user", "content": prompt}
            ]
        )
        analysis = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI for graph analysis: {e}")
    return {"graph_analysis": analysis}