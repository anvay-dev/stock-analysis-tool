import matplotlib.pyplot as plt

def get_figure(df, ticker):
    fig, ax = plt.subplots()
    ax.plot(df["Close"], label="Close")
    ax.plot(df["MA_10"], label="MA_10")
    ax.plot(df["MA_30"], label="MA_30")
    ax.set_title(ticker + " Price + Moving Averages")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    return fig
