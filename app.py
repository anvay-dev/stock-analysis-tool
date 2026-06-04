import streamlit as st
from fetch_data import get_stock_data
from visualize import get_figure
from model import run_model

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