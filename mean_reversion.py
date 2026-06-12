import numpy as np
import pandas as pd
def run_reversion(df):
    df = df.copy()
    df.columns = df.columns.get_level_values(0)
    print(df["Daily_Return"].describe())
    
    df["middle_band"] = df["Close"].rolling(window=20).mean()
    stddev = df["Close"].rolling(window=20).std() * 2
    df["upper_band"] = df["middle_band"] + (stddev)
    df["lower_band"] = df["middle_band"] - (stddev)
    df["signal"] = np.where((df["Close"] > df["lower_band"]) & (df["Close"].shift(1) < df["lower_band"].shift(1)), 1, np.where((df["Close"] < df["upper_band"]) & (df["Close"].shift(1) > df["upper_band"].shift(1)), -1, 0))
    buy_days = df[df["signal"] == 1]["Daily_Return"]
    print(buy_days.describe())
    print(buy_days.sum())

    balance = 10000
    portfolio_values = []

    for index, row in df.iterrows():
        if pd.isna(row["Daily_Return"]):
            portfolio_values.append(balance)
            continue
        if row["signal"] == 1:
            balance = balance * (1 + row["Daily_Return"])
        elif row["signal"] == -1:
            balance = balance * (1 - row["Daily_Return"])
        portfolio_values.append(balance)
    print(type(df["Close"].iloc[-1]))
    print(df["Close"].iloc[-1])
    last_close = df["Close"].iloc[-1]
    first_close = df["Close"].iloc[0]
    buyhold = (last_close - first_close) / first_close * 100
    strategy_return = (balance - 10000) / 10000 * 100

    return {
        'Net Asset Values': portfolio_values, 
        'Final Strategy Return': strategy_return, 
        'Buy and Hold Return': buyhold,
        'Data': df
    }