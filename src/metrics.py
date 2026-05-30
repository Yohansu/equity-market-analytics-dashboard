import pandas as pd

# Function to calculate the daily returns
def calculate_daily_return(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["Daily Return"] = data["Close"].pct_change().fillna(0)
    return data

# Function to calculate the cumulative return between the given initial and final date
def calculate_cumulative_return(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["Cumulative Return"] = (data["Close"] / data["Close"].iloc[0]) - 1
    return data

# Function to calculate the total cumulative return
def calculate_total_return(data: pd.DataFrame) -> float:
    initial_price = data["Close"].iloc[0]
    final_price = data["Close"].iloc[-1]

    total_return = (final_price / initial_price) - 1

    return total_return