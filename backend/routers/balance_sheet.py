from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.services.balance_sheet import get_balance_sheet_data

router = APIRouter()

@router.get("/balance-sheet-data", response_class=JSONResponse)
def balance_sheet_data():
    df = get_balance_sheet_data()
    return {"columns": list(df.columns), "data": df.to_dict(orient="records")}
