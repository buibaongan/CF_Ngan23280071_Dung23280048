import pandas as pd
import numpy as np

class Calculate:
    def __init__ (self, file):
        self.df = pd.read_csv(file, header=[0, 1], index_col=0, parse_dates=True)
        self.tickers = self.df['Adj Close'].columns

    def add_indicators(self, short_window = 50, long_window = 200):
        # Tính SMA
        SMA_50 = self.df['Adj Close'].rolling(window=short_window).mean()
        SMA_200 = self.df['Adj Close'].rolling(window=long_window).mean()
        
        SMA_50.columns = pd.MultiIndex.from_product([['SMA_50'], self.tickers])
        SMA_200.columns = pd.MultiIndex.from_product([['SMA_200'], self.tickers])
        
        # Tính Volatility 1 tháng (21 ngày), chuẩn hóa theo năm (căn 252)
        log_returns = self.df['Log Return']
        volatility = log_returns.rolling(window=21).std() * np.sqrt(252)
        volatility.columns = pd.MultiIndex.from_product([['Volatility'], self.tickers])
        
        self.df = pd.concat([self.df, SMA_50, SMA_200, volatility], axis=1)
