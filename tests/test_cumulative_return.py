import pandas as pd

from src.metrics import calculate_cumulative_return, calculate_total_return


prices = pd.DataFrame({
    "Close": [100, 110, 121, 108.9]
})

data_with_cumulative_return = calculate_cumulative_return(prices)
total_return = calculate_total_return(prices)

print(data_with_cumulative_return)
print()
print(f"Total Return: {total_return:.2%}")