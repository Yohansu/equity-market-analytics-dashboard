import pandas as pd


def validate_close_prices(data: pd.DataFrame) -> None:
    """
    Validate that the input DataFrame contains usable closing prices.

    This function prevents incorrect financial calculations caused by:
    - Empty DataFrames
    - Missing 'Close' column
    - Missing values in closing prices
    - Zero or negative closing prices
    """

    # Case 1: The DataFrame has no rows or columns
    if data.empty:
        raise ValueError("DataFrame is empty.")

    # Case 2: The required 'Close' column does not exist
    if "Close" not in data.columns:
        raise KeyError("DataFrame must contain a 'Close' column.")

    # Case 3: The 'Close' column contains missing values
    if data["Close"].isna().any():
        raise ValueError("Close prices contain missing values.")

    # Case 4: The 'Close' column contains zero or negative prices
    # This avoids division by zero and invalid financial results.
    if (data["Close"] <= 0).any():
        raise ValueError("Close prices must be greater than zero.")


def calculate_daily_return(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily returns using closing prices.

    Formula:
    Daily Return = (Current Close / Previous Close) - 1
    """

    validate_close_prices(data)

    data = data.copy()

    data["Daily Return"] = data["Close"].pct_change().fillna(0)

    return data


def calculate_cumulative_return(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative return over time.

    Formula:
    Cumulative Return = (Current Close / Initial Close) - 1
    """

    validate_close_prices(data)

    data = data.copy()

    initial_price = data["Close"].iloc[0]

    data["Cumulative Return"] = (data["Close"] / initial_price) - 1

    return data


def calculate_total_return(data: pd.DataFrame) -> float:
    """
    Calculate the total return for the selected period.

    Formula:
    Total Return = (Final Close / Initial Close) - 1
    """

    validate_close_prices(data)

    initial_price = data["Close"].iloc[0]
    final_price = data["Close"].iloc[-1]

    total_return = (final_price / initial_price) - 1

    return total_return