import numpy as np
from fetch_data import get_stock_data

df = get_stock_data("AAPL")
df.columns = df.columns.get_level_values(0)

df["middle_band"] = df["Close"].rolling(window=20).mean()
stddev = df["Close"].rolling(window=20).std() * 2
df["upper_band"] = df["middle_band"] + (stddev)
df["lower_band"] = df["middle_band"] - (stddev)
df["signal"] = np.where(df["Close"] > df["upper_band"], -1, np.where(df["Close"] < df["lower_band"], 1, 0))

print(df["signal"].value_counts())