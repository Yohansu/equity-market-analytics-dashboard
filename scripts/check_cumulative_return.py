# Manual test for cumulative return and total cumulative return

from src.data_loader import download_stock_data
from src.metrics import calculate_cumulative_return, calculate_total_return

data = download_stock_data(
    ticker="AAPL",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

data_with_cumulative_return = calculate_cumulative_return(data)
total_return = calculate_total_return(data)

print(data_with_cumulative_return[["Close", "Cumulative Return"]].tail())
print()
print(f"Total Return: {total_return:.2%}")