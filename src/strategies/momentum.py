import pandas as pd
import numpy as np

class MomentumStrategy:
    def __init__(self, df, threshold=0.01, window=50):
        self.df = df
        self.tickers = df.columns.get_level_values(1).unique()
        self.threshold = threshold
        self.window = window

    def generate_signals(self):
        """
        Logic: 
            Long (1):    Giá > SMA * (1 + threshold)
            Short (-1):  Giá < SMA * (1 - threshold)
            Đóng vị thế (0): Khi gãy xu hướng (giá quay đầu cắt nang SMA)
        """
        adj_close = self.df['Adj Close']
        sma = adj_close.rolling(window=self.window).mean()
        
        upper_bound = sma * (1 + self.threshold)
        lower_bound = sma * (1 - self.threshold)

        # Create signals
        signals = pd.DataFrame(np.nan, index=adj_close.index, columns=adj_close.columns)
        
        signals[(adj_close > upper_bound)] = 1      # Long
        signals[(adj_close < lower_bound)] = -1     # Short
        
        cross_sma = ((adj_close.shift(1) > sma.shift(1)) & (adj_close < sma)) | \
                    ((adj_close.shift(1) < sma.shift(1)) & (adj_close > sma))
        signals[cross_sma] = 0                       # Đóng vị thế
        
        signals = signals.ffill().fillna(0)           
        signals[sma.isna()] = 0                      # Khi chưa đủ dữ liệu cho SMA
        
        signals_df = pd.DataFrame(signals, index=self.df.index, columns=self.tickers)
        signals_df.columns = pd.MultiIndex.from_product([['Signal'], self.tickers])
        
        return signals_df