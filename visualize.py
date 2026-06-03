import matplotlib.pyplot as plt
from fetch_data import aapl_data

plt.plot(aapl_data["Close"], label="Close")
plt.plot(aapl_data["MA_10"], label="MA_10")
plt.plot(aapl_data["MA_30"], label="MA_30")

plt.title("AAPL Price + Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.show()