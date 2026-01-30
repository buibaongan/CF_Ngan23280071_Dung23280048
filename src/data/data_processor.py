import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize

class DataProcessor:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(self.file, header=[0, 1], index_col=0, parse_dates=True)
        # Lấy danh sách tickers từ level 1 của columns
        self.tickers = set(self.df.columns.get_level_values(1))

    def add_log_returns(self):        
        log_returns = np.log(self.df['Adj Close'] / self.df['Adj Close'].shift(1))
        log_returns.columns = pd.MultiIndex.from_product([['Log Return'], log_returns.columns])
        self.df = pd.concat([self.df, log_returns], axis=1)

    def check_na(self, ticker):
        for col in self.df.columns.levels[0]:
            na_count = self.df[(col, ticker)].isna().sum()
            print(f"{col} : {na_count}")
    
    def drop_na(self):
        self.df = self.df.dropna()
        
    def detect_outliers(self, ticker, col):
        series = self.df[(col, ticker)]
        
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        return outliers
    
    def draw_boxplot(self, ticker, col):
        series = self.df[(col, ticker)]
        plt.figure()
        plt.boxplot(series.dropna())
        plt.title(f"Boxplot of {col} for {ticker}")
        plt.show()
    
    def draw_histogram(self, ticker, col):
        series = self.df[(col, ticker)]
        plt.figure()
        plt.hist(series, bins=50)
        plt.title(f"Return of {ticker}")
        plt.show()

    def winsorize_data(self):
        for ticker in self.tickers:
            # Xử lý Log Return
            if ('Log Return', ticker) in self.df.columns:
                log_returns = self.df[('Log Return', ticker)]
                mask_valid = ~log_returns.isna()        # Lọc bỏ NaN
                data_valid = log_returns[mask_valid]
                if len(data_valid) > 0:
                    self.df.loc[mask_valid, ('Log Return', ticker)] = winsorize(data_valid, limits=[0.01, 0.01])
            
            # Xử lý Volume
            if ('Volume', ticker) in self.df.columns:
                volume = self.df[('Volume', ticker)]
                mask_valid = ~volume.isna()        # Lọc bỏ NaN
                data_valid = volume[mask_valid]
                if len(data_valid) > 0:
                    self.df.loc[mask_valid, ('Volume', ticker)] = winsorize(data_valid, limits=[0.01, 0.01])
    
    def save_cleaned_data(self, output_file):
        self.df.to_csv(output_file)
