# backend/services/balance_sheet.py
import pandas as pd
from fastapi import UploadFile
import io

def get_balance_sheet_data() -> pd.DataFrame:
    # Simulated balance sheet data for eight quarter periods
    data = {
        "Company": [
            "BNP Paribas",
            "BNP Paribas",
            "BNP Paribas",
            "BNP Paribas",
            "BNP Paribas",
            "BNP Paribas",
            "BNP Paribas",
            "BNP Paribas"
        ],
        "Statement": [
            "Balance Sheet",
            "Balance Sheet",
            "Balance Sheet",
            "Balance Sheet",
            "Balance Sheet",
            "Balance Sheet",
            "Balance Sheet",
            "Balance Sheet"
        ],
        "Period": [
            "Q1 2023",
            "Q2 2023",
            "Q3 2023",
            "Q4 2023",
            "Q1 2024",
            "Q2 2024",
            "Q3 2024",
            "Q4 2024"
        ],
        "CashEquivalents": [800, 815, 812, 825, 840, 850, 860, 870],
        "ShortTermInvestments": [400, 415, 418, 420, 425, 430, 435, 440],
        "AccountsReceivable": [500, 505, 495, 500, 505, 500, 505, 510],
        "Inventory": [300, 312, 315, 320, 325, 320, 325, 330],
        "OtherCurrentAssets": [400, 412, 415, 420, 425, 430, 435, 440],
        "TotalCurrentAssets": [2400, 2459, 2455, 2485, 2520, 2530, 2560, 2590],
        "PropertyPlantEquipment": [2800, 2815, 2822, 2830, 2840, 2850, 2860, 2870],
        "IntangibleAssets": [1000, 1012, 1015, 1022, 1055, 1050, 1055, 1060],
        "OtherNonCurrentAssets": [1000, 1012, 1010, 1018, 1040, 1045, 1050, 1075],
        "TotalNonCurrentAssets": [4800, 4839, 4847, 4870, 4935, 4945, 4965, 5005],
        "TotalAssets": [7200, 7298, 7302, 7355, 7455, 7475, 7525, 7595],
        "ShortTermDebt": [800, 805, 815, 820, 840, 850, 860, 870],
        "AccountsPayable": [700, 710, 705, 710, 720, 725, 730, 770],
        "OtherCurrentLiabilities": [400, 408, 410, 415, 420, 425, 430, 470],
        "TotalCurrentLiabilities": [1900, 1923, 1930, 1945, 1980, 2000, 2020, 2110],
        "LongTermDebt": [1400, 1415, 1410, 1415, 1440, 1445, 1450, 1470],
        "DeferredTaxLiabilities": [500, 510, 508, 510, 540, 545, 550, 570],
        "OtherNonCurrentLiabilities": [500, 511, 510, 511, 540, 545, 550, 570],
        "TotalNonCurrentLiabilities": [2400, 2436, 2428, 2436, 2520, 2535, 2550, 2610],
        "TotalLiabilities": [4300, 4359, 4358, 4381, 4500, 4535, 4570, 4720],
        "CommonStock": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        "RetainedEarnings": [1500, 1530, 1529, 1553, 1527, 1505, 1513, 1425],
        "AdditionalPaidInCapital": [300, 307, 311, 315, 320, 325, 330, 335],
        "OtherEquity": [100, 102, 104, 106, 108, 110, 112, 115],
        "TotalEquity": [2900, 2939, 2944, 2974, 2955, 2940, 2955, 2875],
        "TotalLiabilitiesAndEquity": [7200, 7298, 7302, 7355, 7455, 7475, 7525, 7595]
    }


    df = pd.DataFrame(data)
    
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
