import yfinance as yf

aapl_data = yf.download("AAPL", start = "2023-01-01", end = "2025-01-01")

print(aapl_data.head(10))
print(aapl_data.shape)
aapl_data["MA_10"] = aapl_data["Close"].rolling(window=10).mean()
aapl_data["MA_30"] = aapl_data["Close"].rolling(window=30).mean()
print(aapl_data.tail(20))
