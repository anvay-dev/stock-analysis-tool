#my baby is the best . i love him so much. may god bless him with long healthy happy life <-- my mom wrote this so i am going to keep it
from screener import UNIVERSE
from fetch_data import get_stock_data
from mean_reversion import run_reversion
import numpy as np
import pandas as pd

def get_universe_data(local_universe):
    universe_data = {}
    train_data = {}
    test_data = {}
    deploy_data = {}
    for ticker in local_universe:
        universe_data[ticker] = get_stock_data(ticker)

        train_data[ticker] = universe_data[ticker].iloc[0:(int(len(universe_data[ticker])* 0.5))]
        test_data[ticker] = universe_data[ticker].iloc[(int(len(universe_data[ticker])* 0.5)):(int(len(universe_data[ticker])* 0.75))]
        deploy_data[ticker] = universe_data[ticker].iloc[(int(len(universe_data[ticker])* 0.75)):]
    return universe_data, train_data, test_data, deploy_data

global_universe, training_data, testing_data, deploying_data = get_universe_data(UNIVERSE)

def score_stocks(train, test):
    reversion_result = {}
    ticker_result = {}
    for ticker, data in train.items():
        reversion_result = run_reversion(train[ticker], test[ticker])
        alpha = reversion_result["Final Strategy Return"] - reversion_result["Buy and Hold Return"]
        nav = np.array(reversion_result["Net Asset Values"])
        peak = np.maximum.accumulate(nav)
        drawdown = np.min((nav - peak) / peak) * 100

        ticker_result[ticker] = [alpha, drawdown]

    return ticker_result

ticker_reversion = score_stocks(training_data, testing_data)

def select_stock(ticker_result):
    filtered = {}
    sortedtuple = {}
    sorteddict = {}
    best_stocks = []
    for ticker, data in ticker_result.items():
        if data[1] >= -15:
            filtered[ticker] = data

    sortedtuple = sorted(filtered.items(), key=lambda x: x[1][0], reverse=True)
    sorteddict = dict(sortedtuple)

    best_stocks = list(sorteddict.keys())[:5]
    return best_stocks

selected_stocks = select_stock(ticker_reversion)

def deploy_stocks(best_stocks, test, deploy, ticker_result):
    weight = 0
    best_results = []
    allocation = []
    total_alpha = sum(ticker_result[ticker][0] for ticker in best_stocks)
    
    for ticker in best_stocks:
        weight = ticker_result[ticker][0] / total_alpha
        allocation.append(weight * 100000)
    
    deploy_result = {}
    count = 0
    for ticker in best_stocks:
        reversion_result = run_reversion(test[ticker], deploy[ticker])
        deploy_result[ticker] = allocation[count] * (reversion_result["Final Balance"] / 10000)
        count += 1
    total = 0
    for key, value in deploy_result.items():
        total += value

    spy_deploy = deploy["SPY"]
    spy_deploy = spy_deploy.copy()
    spy_deploy.columns = spy_deploy.columns.get_level_values(0)
    first = float(spy_deploy["Close"].iloc[0])
    last = float(spy_deploy["Close"].dropna().iloc[-1])
    print(spy_deploy["Close"].head())
    print(type(spy_deploy["Close"].iloc[0]))
    print(f"first: {first}, last: {last}")
    spy_return = (last - first) / first * 100

    return total, spy_return
    

final, spy_compare = deploy_stocks(selected_stocks, testing_data, deploying_data, ticker_reversion)

print(selected_stocks)
print(final)
print(spy_compare)