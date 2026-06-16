from fetch_data import get_stock_data
from mean_reversion import run_reversion

UNIVERSE = [
    # Tech
    "AAPL", "MSFT", "GOOGL", "NVDA", "META", "AMZN",
    # Finance
    "JPM", "GS", "BAC", "V", "MA",
    # Consumer
    "TSLA", "KO", "PEP", "MCD", "NKE",
    # Healthcare
    "JNJ", "PFE", "UNH",
    # Energy
    "XOM", "CVX",
    # ETFs
    "SPY", "QQQ", "DIA",
    # Volatile/Interesting
    "INTC", "AMD"
]

def run_screener():
    result_on_uni = []

    for ticker in UNIVERSE:
        try:
            find_data = get_stock_data(ticker)
            reversion = run_reversion(find_data)
            last_signal = reversion["Data"]["signal"].iloc[-1]
            result_on_uni.append({
                "Ticker": ticker,
                "Strategy Return %": reversion["Final Strategy Return"],
                "Buy and Hold Return %": reversion["Buy and Hold Return"],
                "Signal": "BUY" if last_signal == 1 else "SELL" if last_signal == -1 else "NEUTRAL"
            })
        except Exception as e:
            print(f"Skipping {ticker}: {e}")
            result_on_uni.append({
                "Ticker": ticker,
                "Strategy Return %": None,
                "Buy and Hold Return %": None,
                "Signal": "ERROR"
            })

    return result_on_uni