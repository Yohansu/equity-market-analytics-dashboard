import pandas as pd

close = pd.DataFrame({
    "Close": [100] * 251 + [110]
})
print(close)