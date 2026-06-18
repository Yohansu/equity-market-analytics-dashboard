import pandas as pd

# Glogabl variable that stores the number of trading days per year
TRADING_DAYS_PER_YEAR = 252

# Function to validate 'Close' prices
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

# Function to calculate daily return
def calculate_daily_return(data: pd.DataFrame) -> pd.DataFrame:
    validate_close_prices(data)

    data = data.copy()
    data["Daily Return"] = data["Close"].pct_change().fillna(0)
    return data

# Function to calculate the cumulative return between the given initial and final date
def calculate_cumulative_return(data: pd.DataFrame) -> pd.DataFrame:
    validate_close_prices(data)

    data = data.copy()
    data["Cumulative Return"] = (data["Close"] / data["Close"].iloc[0]) - 1
    return data

# Function to calculate the total cumulative return
def calculate_total_return(data: pd.DataFrame) -> float:
    validate_close_prices(data)

    initial_price = data["Close"].iloc[0]
    final_price = data["Close"].iloc[-1]

    total_return = (final_price / initial_price) - 1

    return total_return

# Function to calculate annualized return
def calculate_annualized_return(data: pd.DataFrame) -> float:
    """
    Calculate the annualized return for the selected period.

    Formula:
    Annualized Return = (1 + Total Return) ** (252 / Number of Trading Periods) - 1

    Where:
    - 252 represents the approximate number of trading days in one year.
    - Number of trading periods is calculated as len(data) - 1.
    """

    validate_close_prices(data)

    number_of_trading_periods = len(data) - 1

    if number_of_trading_periods <= 0:
        raise ValueError(
            "At least two closing prices are required to calculate annualized return."
        )

    total_return = calculate_total_return(data)

    annualized_return = (
        (1 + total_return) ** (TRADING_DAYS_PER_YEAR / number_of_trading_periods)
    ) - 1

    return annualized_return

# Function to calculate annualized volatility
def calculate_annualized_volatility(data:pd.DataFrame) -> float:

    validate_close_prices(data)

    if len(data) < 2:
        raise ValueError(
            "At least two closing prices are required to calculate annualized volatility."
        )

    data = calculate_daily_return(data)

    daily_return_std = data["Daily Return"].std()

    annualized_volatility = daily_return_std * (TRADING_DAYS_PER_YEAR ** 0.5)

    return annualized_volatility