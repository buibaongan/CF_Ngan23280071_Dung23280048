import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
            Đóng vị thế (0): Khi gãy xu hướng (giá quay đầu cắt ngang SMA)
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
    
    def plot_strategy(self, signals_df, ticker, start_date=None, end_date=None):
        """
        Vẽ biểu đồ giá và tín hiệu trong một khoảng thời gian cụ thể.
        start_date, end_date: định dạng 'YYYY-MM-DD'
        """
        # 1. Trích xuất dữ liệu gốc
        price = self.df['Adj Close'][ticker]
        signal = signals_df['Signal'][ticker]
        sma = price.rolling(window=self.window).mean()
        upper = sma * (1 + self.threshold)
        lower = sma * (1 - self.threshold)

        # 2. Cắt dữ liệu theo thời gian (Slicing)
        # Nếu không truyền ngày, hàm sẽ lấy toàn bộ dữ liệu
        price = price.loc[start_date:end_date]
        signal = signal.loc[start_date:end_date]
        sma = sma.loc[start_date:end_date]
        upper = upper.loc[start_date:end_date]
        lower = lower.loc[start_date:end_date]

        # 3. Vẽ biểu đồ
        plt.figure(figsize=(15, 7))
        plt.plot(price.index, price, label='Price', color='royalblue', alpha=0.8, lw=1.5)
        plt.plot(sma.index, sma, label=f'SMA {self.window}', color='orange', ls='--')
        plt.fill_between(sma.index, lower, upper, color='gray', alpha=0.2, label='Threshold Band')

        # Điểm vào/ra lệnh (trên tập dữ liệu đã cắt)
        buys = price[(signal == 1) & (signal.shift(1) != 1)]
        shorts = price[(signal == -1) & (signal.shift(1) != -1)]
        exits = price[(signal == 0) & (signal.shift(1) != 0)]

        plt.scatter(buys.index, buys, marker='^', color='green', s=120, label='Long', zorder=5)
        plt.scatter(shorts.index, shorts, marker='v', color='red', s=120, label='Short', zorder=5)
        plt.scatter(exits.index, exits, marker='x', color='black', s=100, label='Exit', zorder=5)

        # Định dạng tiêu đề và hiển thị
        plt.title(f"Strategy: {ticker} | Period: {start_date} to {end_date}")
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()