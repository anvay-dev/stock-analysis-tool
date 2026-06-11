import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def run_backtest(df):
    df["Target"] = np.where(df["Close"].shift(-12) > df["Close"], 1, 0)
    df.dropna(axis = 0, inplace=True)

    X = df[["MA_10", "MA_30", "Daily_Return", "Volatility", "RSI"]]
    y = df["Target"]

    split = int(len(X) * 0.8)
    X_train = X.iloc[:split]
    y_train = y.iloc[:split]

    rfc = RandomForestClassifier()
    rfc.fit(X_train, y_train)

    all_predictions = rfc.predict(X)
    balance = 10000
    portfolio_values = []

    for count, (index, row) in enumerate(df.iterrows()):
        if all_predictions[count] == 1:
            balance = balance * (1 + row["Daily_Return"])
        else:
            balance = balance * (1 - row["Daily_Return"])
        portfolio_values.append(balance)

        
    last_close = df["Close"].iloc[-1]
    first_close = df["Close"].iloc[0]
    buyhold = (last_close - first_close) / first_close * 100
    strategy_return = (balance - 10000) / 10000 * 100

    returned_dict = {'Net Asset Values': portfolio_values, 'Final Strategy Return': strategy_return, 'Buy and Hold Return': buyhold}
    return returned_dict