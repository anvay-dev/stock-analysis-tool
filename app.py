import streamlit as st
from fetch_data import get_stock_data
from visualize import get_figure
from model import run_model
from backtest import run_backtest
from mean_reversion import run_reversion
import pandas as pd
from screener import run_screener
from portfolio import create_portfolio

st.title("Stock Analysis Tool")
ticker = st.text_input("Enter a stock ticker: ")

if ticker != "":
    df = get_stock_data(ticker)
    if df is not None:
        st.success("Ticker Data Successfully Loaded")
        st.pyplot(get_figure(df, ticker))

        model_results = run_model(df)
        st.write("Test Accuracy:", model_results["Test Accuracy"])
        st.write("Cross Val Scores:", model_results["Cross Validation Scores"])
        st.write("Mean Cross Val:", model_results["Mean Cross Validation Score"])
        prediction = model_results["Prediction"]
        if prediction == 1:
            st.success("Model predicts: UP in 12 days")
        else:
            st.error("Model predicts: DOWN in 12 days")

        st.title("Backtest Engine (V1)")
        backtest_results = run_backtest(df)
        strategy = float(backtest_results["Final Strategy Return"].iloc[0])
        buyhold = float(backtest_results["Buy and Hold Return"].iloc[0])
        comparison = strategy - buyhold
        st.write(f"Strategy Return: {strategy:.2f}%")
        st.write(f"Buy and Hold Return: {buyhold:.2f}%")
        st.write(f"Model did better/worse by: {comparison:.2f}%")

        st.title("Mean Reversion Strategy (V2)")
        reversion_results = run_reversion(df)
        mr_strategy = float(reversion_results["Final Strategy Return"])
        mr_buyhold = float(reversion_results["Buy and Hold Return"])
        mr_comparison = mr_strategy - mr_buyhold
        st.write(f"Strategy Return: {mr_strategy:.2f}%")
        st.write(f"Buy and Hold Return: {mr_buyhold:.2f}%")
        st.write(f"Model did better/worse by: {mr_comparison:.2f}%")

        st.title("Stock Universe Screener")
        st.write("Running mean reversion signals across 25 stocks...")
        screener_results = run_screener()
        screener_df = pd.DataFrame(screener_results)
        screener_df = screener_df.sort_values("Strategy Return %", ascending=False).reset_index(drop=True)
        screener_df["Strategy Return %"] = pd.to_numeric(screener_df["Strategy Return %"], errors='coerce').round(2)
        screener_df["Buy and Hold Return %"] = pd.to_numeric(screener_df["Buy and Hold Return %"], errors='coerce').round(2)
        screener_df["Alpha %"] = (screener_df["Strategy Return %"] - screener_df["Buy and Hold Return %"]).round(2)
        screener_df = screener_df.sort_values("Alpha %", ascending=False).reset_index(drop=True)
        st.dataframe(screener_df)

        st.title("V3: Quantitative Portfolio System")
        st.write("Constructing optimal portfolio from 25-stock universe...")
        with st.spinner("This may take 1-2 minutes..."):
            final, spy_compare, selected_stocks = create_portfolio()

        st.write(f"Selected stocks: {selected_stocks}")
        st.write(f"Portfolio final value: ${final:,.2f}")
        st.write(f"Portfolio return: {((final - 100000) / 100000 * 100):.2f}%")
        st.write(f"SPY return (benchmark): {spy_compare:.2f}%")
        portfolio_return = (final - 100000) / 100000 * 100
        if portfolio_return > spy_compare:
            st.success(f"Portfolio beats SPY by {(portfolio_return - spy_compare):.2f}%")
        else:
            st.error(f"Portfolio underperforms SPY by {(spy_compare - portfolio_return):.2f}%")