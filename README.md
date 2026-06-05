# Stock Analysis Tool

An end-to-end stock analysis and prediction tool built with Python, pandas, and scikit-learn.

## What It Does
- Pulls real-time historical stock data for any ticker
- Computes technical indicators: Moving Averages, RSI, Volatility, Daily Return
- Trains a Random Forest classifier to predict 12-day price direction
- Backtests the strategy against buy-and-hold and compares returns
- Displays everything in an interactive web app built with Streamlit

## Tech Stack
- Python, pandas, numpy, scikit-learn, yfinance, matplotlib, Streamlit

## Key Findings
- Model performs best as a capital preservation tool on downtrending stocks
- Chronological train/test split used to eliminate look-ahead bias
- Tested across AAPL, META, NVDA, TSLA, INTC

## How To Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure
- `fetch_data.py` — data pipeline and feature engineering
- `visualize.py` — matplotlib charting
- `model.py` — Random Forest training and prediction
- `backtest.py` — backtesting engine
- `app.py` — Streamlit web app
- `MODEL_LOG.md` — experiment tracking log
