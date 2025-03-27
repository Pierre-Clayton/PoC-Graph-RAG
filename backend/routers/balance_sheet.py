from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.services.balance_sheet import get_balance_sheet_data

router = APIRouter()

@router.get("/balance-sheet-data", response_class=JSONResponse)
def balance_sheet_data():
    df = get_balance_sheet_data()
    csv_text = df.to_csv(index=False)
    return {"csv": csv_text}
