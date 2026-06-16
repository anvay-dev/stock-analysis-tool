import numpy as np
import pandas as pd

def run_reversion(training_data, testing_data = None):
    training_data = training_data.copy()
    training_data.columns = training_data.columns.get_level_values(0)

    if testing_data is None:
        simulate_on = training_data
    else:
        testing_data = testing_data.copy()
        testing_data.columns = testing_data.columns.get_level_values(0)
        simulate_on = testing_data

    training_data["middle_band"] = training_data["Close"].rolling(window=20).mean()
    stddev = training_data["Close"].rolling(window=20).std() * 2
    training_data["upper_band"] = training_data["middle_band"] + (stddev)
    training_data["lower_band"] = training_data["middle_band"] - (stddev)
    upper = training_data["upper_band"].iloc[-1]
    lower = training_data["lower_band"].iloc[-1]
    simulate_on["signal"] = np.where((simulate_on["Close"] > lower) & (simulate_on["Close"].shift(1) < lower), 1, np.where((simulate_on["Close"] < upper) & (simulate_on["Close"].shift(1) > upper), -1, 0))
    
    balance = 10000
    portfolio_values = []

    for index, row in simulate_on.iterrows():
        if pd.isna(row["Daily_Return"]):
            portfolio_values.append(balance)
            continue
        if row["signal"] == 1:
            balance = balance * (1 + row["Daily_Return"])
        elif row["signal"] == -1:
            balance = balance * (1 - row["Daily_Return"])
        portfolio_values.append(balance)
    
    last_close = simulate_on["Close"].iloc[-1]
    first_close = simulate_on["Close"].iloc[0]
    buyhold = (last_close - first_close) / first_close * 100
    strategy_return = (balance - 10000) / 10000 * 100

    return {
        'Net Asset Values': portfolio_values, 
        'Final Strategy Return': strategy_return, 
        'Buy and Hold Return': buyhold,
        'Final Balance': balance
    }