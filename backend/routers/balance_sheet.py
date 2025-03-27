# backend/routers/balance_sheet.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from backend.services.balance_sheet import get_balance_sheet_data, process_balance_sheet_csv

router = APIRouter()

@router.get("/balance-sheet-data", response_class=JSONResponse)
def balance_sheet_data():
    df = get_balance_sheet_data()
    return {"columns": list(df.columns), "data": df.to_dict(orient="records")}

@router.post("/upload-balance-sheet", response_class=JSONResponse)
async def upload_balance_sheet(file: UploadFile = File(...)):
    """
    Endpoint to accept a CSV file upload.
    Reads the CSV, computes additional metrics, and returns the enhanced data.
    """
    try:
        df = process_balance_sheet_csv(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"columns": list(df.columns), "data": df.to_dict(orient="records")}
