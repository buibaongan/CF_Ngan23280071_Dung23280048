import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize


class DataLoader:
    def __init__(self, file):
        self.file = file

    def load(self):
        return pd.read_csv(self.file, header=[0,1], index_col=0, parse_dates=True)

    def save(self, df, output_file):
        df.to_csv(output_file)


class FeatureEngineer:
    def add_log_returns(self, df):
        log_returns = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
        log_returns.columns = pd.MultiIndex.from_product(
            [['Log Return'], log_returns.columns]
        )
        return pd.concat([df, log_returns], axis=1)


class DataCleaner:
    def drop_na(self, df):
        return df.dropna()

    def winsorize_column(self, df, col, ticker, limits=[0.01,0.01]):
        series = df[(col, ticker)]
        mask = ~series.isna()
        if (len(series[mask]) > 0):
            df.loc[mask, (col, ticker)] = winsorize(series[mask], limits=limits)
        return df


class OutlierDetector:
    def detect_iqr(self, series):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lb = Q1 - 1.5*IQR
        ub = Q3 + 1.5*IQR
        return series[(series < lb) | (series > ub)]


class DataProcessor:
    def __init__(self, file):
        self.loader = DataLoader(file)
        self.feature_engineer = FeatureEngineer()
        self.cleaner = DataCleaner()
        self.outlier_detector = OutlierDetector()

    def process(self):
        # Load data
        df = self.loader.load()

        # Feature engineering
        df = self.feature_engineer.add_log_returns(df)

        # Winsorize 
        tickers = set(df.columns.get_level_values(1))
        for ticker in tickers:
            if ('Log Return', ticker) in df.columns:
                df = self.cleaner.winsorize_column(
                    df, 'Log Return', ticker
                )

            if ('Volume', ticker) in df.columns:
                df = self.cleaner.winsorize_column(
                    df, 'Volume', ticker
                )

        return df

    def save(self, df, output_file):
        self.loader.save(df, output_file)