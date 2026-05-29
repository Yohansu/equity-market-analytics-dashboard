import pandas as pd

def calculate_daily_return(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["Daily Return"] = data["Close"].pct_change()
    return data
