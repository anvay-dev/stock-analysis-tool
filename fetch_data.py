import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(ticker):
    end = datetime.today()
    start = end - timedelta(days=730)
    df = yf.download(ticker, start, end)

    df["MA_10"] = df["Close"].rolling(window=10).mean()
    df["MA_30"] = df["Close"].rolling(window=30).mean()
    df["Daily_Return"] = df["Close"].pct_change()
    df["Volatility"] = df["Daily_Return"].rolling(window=10).std()
    delta = df["Daily_Return"]
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    return df

