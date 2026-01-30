import pandas as pd
import numpy as np

class MeanReversionStrategy:
    def __init__(self, df, window=20, std_dev=2):
        self.df = df
        self.tickers = df.columns.get_level_values(1).unique()
        self.window = window
        self.std_dev = std_dev

    def generate_signals(self):
        """
        MEAN REVERSION (BOLLINGER BANDS):
        - Long (1): khi giá cắt lên từ phía dưới dải Lower Band
        - Short (-1): khi giá cắt xuống từ phía trên dải Upper Band
        - Giữ vị thế (0) trong các trường hợp còn lại
        """
        adj_close = self.df['Adj Close']
        
        rolling_mean = adj_close.rolling(window=self.window).mean()
        rolling_std = adj_close.rolling(window=self.window).std()
        
        upper_band = rolling_mean + (rolling_std * self.std_dev)
        lower_band = rolling_mean - (rolling_std * self.std_dev)

        prev_adj_close = adj_close.shift(1)
        
        # Create buy/sell signals based on crossovers
        buy_signal = (prev_adj_close < lower_band) & (adj_close > lower_band)
        sell_signal = (prev_adj_close > upper_band) & (adj_close < upper_band)
        
        signals = pd.DataFrame(np.nan, index=adj_close.index, columns=adj_close.columns)
        signals[buy_signal] = 1
        signals[sell_signal] = -1
        signals = signals.ffill().fillna(0)
        
        signals_df = pd.DataFrame(signals, index=self.df.index, columns=self.tickers)
        signals_df.columns = pd.MultiIndex.from_product([['Signal'], self.tickers])
        
        return signals_df