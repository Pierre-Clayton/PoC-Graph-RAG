# backend/services/balance_sheet.py
import pandas as pd
from fastapi import UploadFile
import io

def get_balance_sheet_data() -> pd.DataFrame:
    # Simulated balance sheet data for eight quarter periods
    data = {
        "Company": ["BNP Paribas"] * 8,
        "Statement": ["Balance Sheet"] * 8,
        "Period": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
        "CurrentAssets": [2400, 2450, 2500, 2550, 2600, 2650, 2700, 2750],
        "NonCurrentAssets": [4800, 4850, 4900, 4950, 5000, 5050, 5100, 5150],
        "TotalAssets": [7200, 7300, 7400, 7500, 7600, 7700, 7800, 7900],
        "CurrentLiabilities": [1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250],
        "NonCurrentLiabilities": [2400, 2450, 2500, 2550, 2600, 2650, 2700, 2750],
        "TotalLiabilities": [4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000],
        "Equity": [2900, 2900, 2900, 2900, 2900, 2900, 2900, 2900]
    }
    df = pd.DataFrame(data)
    
    # Compute additional metrics for a more detailed balance sheet
    df["WorkingCapital"] = df["CurrentAssets"] - df["CurrentLiabilities"]
    df["CurrentRatio"] = df["CurrentAssets"] / df["CurrentLiabilities"]
    df["DebtToEquityRatio"] = df["TotalLiabilities"] / df["Equity"]
    df["CurrentAssetsPercentage"] = (df["CurrentAssets"] / df["TotalAssets"]) * 100
    df["NonCurrentAssetsPercentage"] = (df["NonCurrentAssets"] / df["TotalAssets"]) * 100
    
    return df

def process_balance_sheet_csv(file: UploadFile) -> pd.DataFrame:
    """
    Processes an uploaded CSV file to generate a detailed balance sheet.
    It reads the CSV into a DataFrame and computes extra financial metrics.
    """
    try:
        content = file.file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        
        # Compute additional fields if required columns exist
        required_cols = {"CurrentAssets", "CurrentLiabilities", "NonCurrentAssets", "TotalAssets", "NonCurrentLiabilities", "TotalLiabilities", "Equity"}
        if required_cols.issubset(df.columns):
            df["WorkingCapital"] = df["CurrentAssets"] - df["CurrentLiabilities"]
            df["CurrentRatio"] = df["CurrentAssets"] / df["CurrentLiabilities"]
            df["DebtToEquityRatio"] = df["TotalLiabilities"] / df["Equity"]
            df["CurrentAssetsPercentage"] = (df["CurrentAssets"] / df["TotalAssets"]) * 100
            df["NonCurrentAssetsPercentage"] = (df["NonCurrentAssets"] / df["TotalAssets"]) * 100
        return df
    except Exception as e:
        raise Exception(f"Error processing CSV file: {e}")
