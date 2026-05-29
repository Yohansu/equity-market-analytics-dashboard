import pandas as pd

# Closing prices from a ticker
close_prices = [100, 101, 102, 103]
df_close = pd.DataFrame(close_prices, columns=['close'])

# Calculate the daily returns
# Daily returns = (today's price/ yesterday's price) - 1
# The Daily returns for the first closing price doesn't exist; NaN

daily = df_close.pct_change()

print(daily)

