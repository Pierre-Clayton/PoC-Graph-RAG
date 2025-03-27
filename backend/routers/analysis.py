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
    prompt = f"""
Based on the following balance sheet data for BNP Paribas, please answer the following question:

Question: {question}

Data (in Markdown Table):
{md_table}

Provide a clear, professional summary in Markdown format. Use tables if necessary.
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

@router.post("/graph-analysis", response_class=JSONResponse)
def graph_analysis(payload: dict = Body(...)):
    question = payload.get("question", "")
    all_relationships = get_graph_relationships()
    metrics = compute_graph_metrics()
    relevant_relationships = get_relevant_subgraph(question)
    summary = summarize_graph_insights(relevant_relationships, metrics)
    prompt = f"""
Graph Summary:
{summary}

Question: {question}

Please provide a detailed analysis in Markdown format, using tables if necessary.
"""
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
