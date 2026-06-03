from fetch_data import aapl_data
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

aapl_data["Target"] = np.where(aapl_data["Close"].shift(-12) > aapl_data["Close"], 1, 0)
aapl_data.dropna(axis = 0, inplace=True)

X = aapl_data[["MA_10", "MA_30", "Daily_Return", "Volatility", "RSI"]]
y = aapl_data["Target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)
y_pred = rfc.predict(X_test)
scores = cross_val_score(rfc, X_train, y_train, cv = 3)
print("Test Accuracy:", accuracy_score(y_test, y_pred))
print("Cross Val Scores:", scores)
print("Mean Cross Val:", scores.mean())