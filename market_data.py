import yfinance as yf
import pandas as pd
import numpy as np

class MarketData:
    def __init__(self, tickers):
        self.tickers = tickers
        self.df = None

    def download_data(self, start_date, end_date, auto_adjust=False):
        """
        Download price-volume data:
        open, high, low, close (OHLC), adjusted prices, volume
        """
        self.df = yf.download(self.tickers, start=start_date, end=end_date, auto_adjust=auto_adjust)
        return self.df

    def save_df(self, filename='price_volume_data.csv'):
        """
        Save data to CSV file
        """
        self.df.to_csv(filename)

    def load_df(self, filename='price_volume_data.csv'):
        """
        Load data from CSV file
        """
        # header=[0,1]: 2 dòng đầu tạo MultiIndex cột
        # index_col=0: cột Date làm index
        self.df = pd.read_csv(filename, header=[0, 1], index_col=0, parse_dates=True)