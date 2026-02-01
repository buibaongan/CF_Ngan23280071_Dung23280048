import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        - Đóng vị thế (0): khi giá quay về cắt đường SMA
        """
        adj_close = self.df['Adj Close']
        
        rolling_mean = adj_close.rolling(window=self.window).mean()
        rolling_std = adj_close.rolling(window=self.window).std()
        
        upper_band = rolling_mean + (rolling_std * self.std_dev)
        lower_band = rolling_mean - (rolling_std * self.std_dev)

        prev_adj_close = adj_close.shift(1)
        
        # Create signals
        signals = pd.DataFrame(np.nan, index=adj_close.index, columns=adj_close.columns)
        
        signals[(prev_adj_close < lower_band.shift(1)) & (adj_close > lower_band)] = 1
        signals[(prev_adj_close > upper_band.shift(1)) & (adj_close < upper_band)] = -1
        
        cross_mean_up = (prev_adj_close < rolling_mean.shift(1)) & (adj_close >= rolling_mean)
        cross_mean_down = (prev_adj_close > rolling_mean.shift(1)) & (adj_close <= rolling_mean)
        signals[cross_mean_up | cross_mean_down] = 0
        
        signals = signals.ffill().fillna(0)
        
        signals_df = pd.DataFrame(signals, index=self.df.index, columns=self.tickers)
        signals_df.columns = pd.MultiIndex.from_product([['Signal'], self.tickers])
        
        return signals_df
    
    def plot_strategy(self, signals_df, ticker, start_date=None, end_date=None):
        """
        Trực quan hóa chiến lược Mean Reversion (Bollinger Bands).
        start_date, end_date: định dạng 'YYYY-MM-DD'
        """
        # 1. Trích xuất và tính toán lại các thành phần Bollinger Bands
        price = self.df['Adj Close'][ticker]
        signal = signals_df['Signal'][ticker]
        
        sma = price.rolling(window=self.window).mean()
        std = price.rolling(window=self.window).std()
        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)

        # 2. Cắt dữ liệu theo thời gian (Slicing)
        price = price.loc[start_date:end_date]
        signal = signal.loc[start_date:end_date]
        sma = sma.loc[start_date:end_date]
        upper_band = upper_band.loc[start_date:end_date]
        lower_band = lower_band.loc[start_date:end_date]

        # 3. Vẽ biểu đồ
        plt.figure(figsize=(15, 8))
        
        # Vẽ đường giá và đường trung bình
        plt.plot(price.index, price, label='Price', color='royalblue', alpha=0.8, lw=1.5)
        plt.plot(sma.index, sma, label='Middle Band (SMA)', color='darkorange', ls='--', lw=1)
        
        # Vẽ dải Bollinger (Vùng biến động rủi ro)
        plt.plot(upper_band.index, upper_band, color='gray', alpha=0.3, lw=0.8)
        plt.plot(lower_band.index, lower_band, color='gray', alpha=0.3, lw=0.8)
        plt.fill_between(sma.index, lower_band, upper_band, color='gray', alpha=0.1, label='Bollinger Bands')

        # 4. Xác định các điểm Entry/Exit dựa trên Signal
        buys = price[(signal == 1) & (signal.shift(1) != 1)]
        shorts = price[(signal == -1) & (signal.shift(1) != -1)]
        exits = price[(signal == 0) & (signal.shift(1) != 0)]

        # Vẽ Marker
        plt.scatter(buys.index, buys, marker='^', color='green', s=130, label='Long', zorder=5)
        plt.scatter(shorts.index, shorts, marker='v', color='red', s=130, label='Short', zorder=5)
        plt.scatter(exits.index, exits, marker='x', color='black', s=100, label='Exit', zorder=5)

        # Định dạng biểu đồ
        plt.title(f"Mean Reversion (Bollinger Bands): {ticker} | Window: {self.window}, Std Dev: {self.std_dev}", fontsize=14)
        plt.ylabel("Price ($)")
        plt.legend(loc='best', frameon=True, shadow=True)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()