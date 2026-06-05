Model Experiment Log — Stock Analysis Tool
Version 1.0 — Baseline Random Forest

Train/test split: random 80/20
Prediction window: 12 days
Trading logic: buy if prediction == 1, sit out if 0
Results: AAPL -14%, META +0.95%, NVDA negative, TSLA negative, INTC negative
Notes: Works better in bear markets. Look-ahead bias likely inflating model.py accuracy.

Version 1.1 — Confidence Threshold

Change: predict_proba > 0.65, then 0.55
Results: Worse across all tickers
Notes: Too restrictive, filters out too many valid trading days.

Version 1.2 — Chronological Split

Change: Train on first 80% of dates, predict on all
Results: AAPL -11%, META -16%, NVDA -102%, TSLA -79%, INTC -182%
Notes: Volatile stocks got worse — confirms model was overfitting. INTC improved (downtrend stock). More honest evaluation than V1.0.

Version 1.3 — Shorting on DOWN days

Change: When prediction == 0, apply inverse of daily return
Results: AAPL -38%, META -42%, NVDA -149%, TSLA -129%, INTC -287%
Notes: Significantly worse. Model's DOWN predictions not reliable enough to short profitably. Shorting amplifies losses when wrong.
