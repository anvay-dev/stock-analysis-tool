import yfinance as yf

aapl_data = yf.download("AAPL", start = "2023-01-01", end = "2025-01-01")

print(aapl_data.shape)
aapl_data["MA_10"] = aapl_data["Close"].rolling(window=10).mean()
aapl_data["MA_30"] = aapl_data["Close"].rolling(window=30).mean()
aapl_data["Daily_Return"] = aapl_data["Close"].pct_change()
aapl_data["Volatility"] = aapl_data["Daily_Return"].rolling(window=10).std()
delta = aapl_data["Daily_Return"]
gain = delta.where(delta > 0, 0).rolling(window=14).mean()
loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
rs = gain / loss
aapl_data["RSI"] = 100 - (100 / (1 + rs))
print(aapl_data.tail(20))
