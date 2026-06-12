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

**Version 2.0 — Mean Reversion with Bollinger Band Crossover**
- Strategy: Buy when price crosses back above lower band, short when 
  price crosses back below upper band
- Bands: 20-day moving average ± 2 standard deviations
- Key fix: Crossover signals instead of threshold signals — buy on 
  recovery not on continued decline
- Results: AAPL +1.97%, KO +0.57%, TSLA +36.57% vs buy and hold
  NVDA -1.24%, SPY -3.53%, INTC -55.92%
- Notes: First version to beat buy and hold on multiple tickers. 
  Works best on volatile stocks with clear mean reversion behavior 
  (TSLA). Struggles on extreme downtrends (INTC).

**Version 2.1 — Stock Universe Screener**
- Feature: Runs mean reversion strategy across a predefined 25-stock universe
- Universe: Tech, Finance, Consumer, Healthcare, Energy, ETFs
- Key metric: Alpha % (Strategy Return - Buy and Hold Return)
- Results: 
  - Positive strategy returns across all 25 stocks (0 negative)
  - Beats buy and hold on 11/25 stocks (44% win rate)
  - Best alpha: META, NVDA, AMZN, MA
  - Weakest: GOOGL, GS, INTC (strong bull runs, momentum beats mean reversion)
- Notes: Strategy works best on volatile stocks with mean-reverting behavior. 
  Pure momentum stocks are hard to beat with this approach.
