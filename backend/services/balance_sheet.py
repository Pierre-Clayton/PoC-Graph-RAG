import pandas as pd

def get_balance_sheet_data() -> pd.DataFrame:
    data = {
        "Company": ["BNP Paribas", "BNP Paribas"],
        "Statement": ["Balance Sheet", "Balance Sheet"],
        "Period": ["Q1 2024", "Q4 2023"],
        "CurrentAssets": [2500, 2450],
        "NonCurrentAssets": [5000, 4900],
        "TotalAssets": [7500, 7350],
        "CurrentLiabilities": [2000, 1950],
        "NonCurrentLiabilities": [2500, 2450],
        "TotalLiabilities": [4500, 4400],
        "Equity": [3000, 2950]
    }
    return pd.DataFrame(data)
