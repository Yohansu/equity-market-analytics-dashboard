# Manual test for calculating the Daily Returns

from src.data_loader import download_stock_data
from src.metrics import calculate_daily_return

data = download_stock_data(
    ticker='AAPL',
    start_date='2024-01-01',
    end_date='2024-12-31'
)

data_with_returns = calculate_daily_return(data)
print(data_with_returns[["Close", "Daily Return"]].tail())