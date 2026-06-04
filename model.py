import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

def run_model(df):
    df["Target"] = np.where(df["Close"].shift(-12) > df["Close"], 1, 0)
    df.dropna(axis = 0, inplace=True)

    X = df[["MA_10", "MA_30", "Daily_Return", "Volatility", "RSI"]]
    y = df["Target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    rfc = RandomForestClassifier()
    rfc.fit(X_train, y_train)
    
    y_pred = rfc.predict(X_test)
    crossval = cross_val_score(rfc, X_train, y_train, cv = 3)

    latest = X.dropna().iloc[[-1]]
    prediction = rfc.predict(latest)[0]

    scores = {'Test Accuracy': [accuracy_score(y_test, y_pred)],
              'Cross Validation Scores': [crossval],
              'Mean Cross Validation Score': [crossval.mean()],
              'Prediction': [prediction]}
    return scores
