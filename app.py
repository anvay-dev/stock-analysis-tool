import streamlit as st
from fetch_data import get_stock_data
from visualize import get_figure
from model import run_model
from backtest import run_backtest
from mean_reversion import run_reversion

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
        try:
            reversion_results = run_reversion(df)
            mr_strategy = float(reversion_results["Final Strategy Return"])
            mr_buyhold = float(reversion_results["Buy and Hold Return"])
            mr_comparison = mr_strategy - mr_buyhold
            st.write(f"Strategy Return: {mr_strategy:.2f}%")
            st.write(f"Buy and Hold Return: {mr_buyhold:.2f}%")
            st.write(f"Model did better/worse by: {mr_comparison:.2f}%")
        except Exception as e:
            st.error(f"Mean reversion error: {e}")