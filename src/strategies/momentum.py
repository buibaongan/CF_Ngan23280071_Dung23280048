import pandas as pd
import numpy as np

class MomentumStrategy:
    def __init__(self, df, threshold=0.01):
        self.df = df
        self.tickers = df.columns.get_level_values(1).unique()
        self.threshold = threshold

    def generate_signals(self):
        """
        Logic: Giá > SMA_50 * (1 + threshold) => Buy (1)
               Giá < SMA_50 * (1 - threshold) => Sell (-1)
        """
        adj_close = self.df['Adj Close']
        sma_50 = self.df['SMA_50']
        
        upper_bound = sma_50 * (1 + self.threshold)
        lower_bound = sma_50 * (1 - self.threshold)

        # Signal (Dùng np.nan cho các ô không đủ dữ liệu SMA)
        signals = np.where(sma_50.isna(), np.nan,
                           np.where(adj_close > upper_bound, 1, 
                                    np.where(adj_close < lower_bound, -1, 0)))
        
        signals_df = pd.DataFrame(signals, index=self.df.index, columns=self.tickers)
        signals_df.columns = pd.MultiIndex.from_product([['Signal'], self.tickers])
        
        return signals_df