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

    # def calculate_position_size(self, total_capital=100000, risk_per_trade=0.01):
    #     # target_risk = 0.01          # 1% of portfolio value
    #     # h_l = self.df['High'] - self.df['Low']
    #     # prev_close = self.df['Adj Close'].shift(1)
    #     # h_pl = (self.df['High'] - prev_close).abs()
    #     # l_pl = (self.df['Low'] - prev_close).abs()
    #     # tr = np.maximum.reduce([h_l, h_pl, l_pl])
    #     # tr = pd.DataFrame(tr, index=self.df.index, columns=self.df['High'].columns)
    #     # atr = tr.rolling(window=20).mean()
    #     # position_size = (target_risk / (atr / self.df['Close']))
    #     # position_size.columns = pd.MultiIndex.from_product([['Position Size'], position_size.columns])
    #     # self.df = pd.concat([self.df, position_size], axis=1)
        
    #     risk_amount = total_capital * risk_per_trade
    #     price = self.df['Adj Close']        # Giá hiện tại
    #     sigma = self.df['Volatility']       # Độ biến động năm
        
    #     # Công thức: Size = R / (P * σ)
    #     position_size = risk_amount / (price * sigma)  
        
    #     # Xử lý chia cho 0 hoặc NaN
    #     position_size = position_size.replace([np.inf, -np.inf], 0).fillna(0)
        
    #     # Làm tròn xuống (Số lượng cổ phiếu phải là số nguyên)
    #     position_size = position_size.astype(int)
        
    #     position_size.columns = pd.MultiIndex.from_product([['Position Size'], self.tickers])
    #     self.df = pd.concat([self.df, position_size], axis=1)
        