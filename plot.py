import matplotlib.pyplot as plt

class Plot:
    def __init__(self, df):
        self.df = df

    def plot_short_time(self, strategy_name, ticker, time, plot_signals=False):
        #time: how many days to plot 
        if strategy_name == 'mean_reversion':
            plt.figure(figsize=(14, 7))
            plt.plot(self.df.index[-time:], self.df['Adj Close'][ticker][-time:], label='Price', color='black', alpha=0.6)
            plt.plot(self.df.index[-time:], self.df['BB_Mean'][ticker][-time:], label='Mean', color='orange', linestyle='--')
            plt.plot(self.df.index[-time:], self.df['BB_Upper'][ticker][-time:], label='Upper Band', color='green', alpha=0.3)
            plt.plot(self.df.index[-time:], self.df['BB_Lower'][ticker][-time:], label='Lower Band', color='red', alpha=0.3)
            plt.fill_between(self.df.index[-time:], self.df['BB_Upper'][ticker][-time:], self.df['BB_Lower'][ticker][-time:], color='gray', alpha=0.1)

            if plot_signals:
                buy_signals = self.df.index[(self.df['Signal'][ticker] == 1) & (self.df.index.isin(self.df.index[-time:]))]
                sell_signals = self.df.index[(self.df['Signal'][ticker] == -1) & (self.df.index.isin(self.df.index[-time:]))]
                plt.scatter(buy_signals, self.df['Adj Close'][ticker][buy_signals], marker='^', color='green', label='Buy Signal', s=100)
                plt.scatter(sell_signals, self.df['Adj Close'][ticker][sell_signals], marker='v', color='red', label='Sell Signal', s=100)
            plt.title(f'Bollinger Bands for {ticker}')

        elif strategy_name == 'momentum':
            plt.figure(figsize=(14, 7))
            plt.plot(self.df.index[-time:], self.df['Adj Close'][ticker][-time:], label='Price', color='black', alpha=0.6)
            plt.plot(self.df.index[-time:], self.df['SMA_50'][ticker][-time:], label='50-day SMA', color='blue', linestyle='--')
            #plt.plot(self.df.index[-time:], self.df['SMA_200'][ticker][-time:], label='200-day SMA', color='red', linestyle='--')
            if plot_signals:
                buy_signals = self.df.index[(self.df['Signal'][ticker] == 1) & (self.df.index.isin(self.df.index[-time:]))]
                sell_signals = self.df.index[(self.df['Signal'][ticker] == -1) & (self.df.index.isin(self.df.index[-time:]))]
                plt.scatter(buy_signals, self.df['Adj Close'][ticker][buy_signals], marker='^', color='green', label='Buy Signal', s=100)
                plt.scatter(sell_signals, self.df['Adj Close'][ticker][sell_signals], marker='v', color='red', label='Sell Signal', s=100)
            plt.title(f'SMA Crossover for {ticker}')
        else:
            print("Invalid strategy name. Choose 'mean_reversion' or 'momentum'.")
            return
        

    def plot_full_time(self, strategy_name, ticker, plot_signals=False):
        # Plot the entire time series
        if strategy_name == 'mean_reversion':
            plt.figure(figsize=(14, 7))
            plt.plot(self.df.index, self.df['Adj Close'][ticker], label='Price', color='black', alpha=0.6)
            plt.plot(self.df.index, self.df['BB_Mean'][ticker], label='Mean', color='orange', linestyle='--')
            plt.plot(self.df.index, self.df['BB_Upper'][ticker], label='Upper Band', color='green', alpha=0.3)
            plt.plot(self.df.index, self.df['BB_Lower'][ticker], label='Lower Band', color='red', alpha=0.3)
            plt.fill_between(self.df.index, self.df['BB_Upper'][ticker], self.df['BB_Lower'][ticker], color='gray', alpha=0.1)

            if plot_signals:
                buy_signals = self.df.index[self.df['Signal'][ticker] == 1]
                sell_signals = self.df.index[self.df['Signal'][ticker] == -1]
                plt.scatter(buy_signals, self.df['Adj Close'][ticker][buy_signals], marker='^', color='green', label='Buy Signal', s=100)
                plt.scatter(sell_signals, self.df['Adj Close'][ticker][sell_signals], marker='v', color='red', label='Sell Signal', s=100)
            plt.title(f'Bollinger Bands for {ticker}')

        elif strategy_name == 'momentum':
            plt.figure(figsize=(14, 7))
            plt.plot(self.df.index, self.df['Adj Close'][ticker], label='Price', color='black', alpha=0.6)
            plt.plot(self.df.index, self.df['SMA_50'][ticker], label='50-day SMA', color='blue', linestyle='--')
            plt.plot(self.df.index, self.df['SMA_200'][ticker], label='200-day SMA', color='red', linestyle='--')
            if plot_signals:
                buy_signals = self.df.index[self.df['Signal'][ticker] == 1]
                sell_signals = self.df.index[self.df['Signal'][ticker] == -1]
                plt.scatter(buy_signals, self.df['Adj Close'][ticker][buy_signals], marker='^', color='green')

    def plot_porfolio(self, long_df, short_df, name):
        top10_long = long_df[["Ticker", "Value"]].head(10)
        top10_short = short_df[["Ticker", "Value"]].head(10)
        
        others_long = long_df["Value"].iloc[10:].sum()
        others_short = short_df["Value"].iloc[10:].sum()

        top10_long.loc[len(top10_long)] = ["Others", others_long]

        top10_short.loc[len(top10_short)] = ["Others", others_short]


        fig, axes = plt.subplots(1, 2, figsize=(16, 7))

        axes[0].pie(top10_long["Value"], labels=top10_long["Ticker"], autopct='%1.1f%%')
        axes[0].set_title("Long Portfolio")

        # Short
        axes[1].pie(top10_short["Value"], labels=top10_short["Ticker"], autopct='%1.1f%%')
        axes[1].set_title("Short Portfolio")

        plt.suptitle(f"Portfolio Allocation - {name}")
        plt.show()