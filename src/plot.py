import matplotlib.pyplot as plt
import numpy as np

class EDAPlots:

    def plot_price_with_rolling_mean(self, df, ticker, window=50, days=None):
        price = df[('Adj Close', ticker)]
        if days is not None:
            price = price.tail(days)  
        rm = price.rolling(window).mean()
        plt.figure()
        plt.plot(price, label="Price")
        plt.plot(rm, label=f"MA({window})")
        plt.title(f"Price + Rolling Mean - {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    def plot_returns(self, df, ticker, days=None):
        returns = df[('Log Return', ticker)]
        if days is not None:
            returns = returns.tail(days)
        plt.figure()
        plt.plot(returns)
        title = f"Log Returns - {ticker}"
        if days:
            title += f" (Last {days} days)"
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Log Return")
        plt.show()

    def plot_rolling_returns(self, df, ticker, window = 20, days = None):
        returns = df[('Log Return', ticker)]
        if days is not None:
            returns = returns.tail(days)
        rr = returns.rolling(window).mean()
        plt.figure()
        plt.plot(returns, label = "Returns")
        plt.plot(rr, label = "Rolling Returns")
        plt.legend()
        plt.title(f"Rolling Returns - {ticker}")
        plt.show()

    def draw_histogram(self, df, ticker, col, days=None):
        series =df[(col, ticker)]
        if days is not None:
            series = series.tail(days)
        plt.figure()
        plt.hist(series, bins=50)
        plt.title(f"Histogram of {col} for {ticker}")
        plt.show()

    def draw_boxplot(self, df, ticker, col, days=None):
        series = df[(col, ticker)]
        if days is not None:
            series = series.tail(days)
        plt.figure()
        plt.boxplot(series.dropna())
        plt.title(f"Boxplot of {col} for {ticker}")
        plt.show()

    def plot_zscore(self, df, ticker, window=20, days=None):
        price = df[('Adj Close', ticker)]
        if days is not None:
            price = price.tail(days)
        mean = price.rolling(window).mean()
        std = price.rolling(window).std()
        z = (price - mean) / std
        plt.figure()
        plt.plot(z)
        plt.axhline(0)
        plt.axhline(2, linestyle="--")
        plt.axhline(-2, linestyle="--")
        plt.title(f"Z-score - {ticker}")
        plt.show()

    def plot_rolling_volatility(self, df, ticker, window=20, days=None):
        returns = df[('Log Return', ticker)]
        if days is not None:
            returns = returns.tail(days)
        vol = returns.rolling(window).std()
        plt.figure()
        plt.plot(vol)
        plt.title(f"Rolling Volatility - {ticker}")
        plt.show()

    def plot_cumulative_returns(self, df, ticker, days=None):
        log_return = df[('Log Return', ticker)]

        if days is not None:
            log_return = log_return.tail(days)

        cum_log = log_return.cumsum()

        cum_returns = np.exp(cum_log) - 1

        plt.figure()
        plt.plot(cum_returns)
        plt.title(f"Cumulative Returns - {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.show()

    def plot_volume(self, df, ticker, days=None):
        volume = df[('Volume', ticker)]
        if days is not None:
            volume = volume.tail(days)

        plt.figure()
        plt.plot(volume)
        plt.title(f"Volume over time - {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.show()




