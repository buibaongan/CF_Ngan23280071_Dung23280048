import pandas as pd
import numpy as np

class TradingStrategy:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, header=[0,1], index_col=0, parse_dates=True)
        self.df = self.df.sort_index(axis=1)
        self.tickers = self.df['Adj Close'].columns

    def momentum_signal(self):
        """
        MOMENTUM:
            Giá > SMA_50 => Xu hướng tăng => Mua (Long)
            Giá < SMA_50 => Xu hướng giảm => Bán (Short)
        """
        adj_close = self.df['Adj Close']
        sma_50 = self.df['SMA_50']

        signals = np.where(adj_close > sma_50, 1, -1)
        
        signals_df = pd.DataFrame(signals, index=self.df.index, columns=self.tickers)
        signals_df.columns = pd.MultiIndex.from_product([['Signal'], self.tickers])
        
        if 'Signal' in self.df.columns:
            self.df = self.df.drop(columns=['Signal'])
        self.df = pd.concat([self.df, signals_df], axis=1)
    
    
    def mean_reversion_signal(self, window=20, num_std=2):
        """
        MEAN REVERSION (BOLLINGER BANDS)
            Mua khi giá < Lower Band    (1)
            Bán khi giá > Upper Band    (-1)
            Giữ nguyên khi giá ở giữa   (0)
        """
        adj_close = self.df['Adj Close']
        
        # Tính Bollinger Bands
        rolling_mean = adj_close.rolling(window=window).mean()
        rolling_std = adj_close.rolling(window=window).std()
        
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)

        signals = np.where(adj_close < lower_band, 1, 
                           np.where(adj_close > upper_band, -1, 0))
        
        def create_df(data, name):
            df = pd.DataFrame(data, index=self.df.index, columns=self.tickers)
            df.columns = pd.MultiIndex.from_product([[name], self.tickers])
            return df

        signals_df = create_df(signals, 'Signal')
        mean_df    = create_df(rolling_mean, 'BB_Mean')
        upper_df   = create_df(upper_band, 'BB_Upper')
        lower_df   = create_df(lower_band, 'BB_Lower')

        cols_to_drop = ['Signal', 'BB_Mean', 'BB_Upper', 'BB_Lower']
        existing_cols = [c for c in cols_to_drop if c in self.df.columns.get_level_values(0)]
        if existing_cols:
            self.df = self.df.drop(columns=existing_cols, level=0)

        self.df = pd.concat([self.df, mean_df, upper_df, lower_df, signals_df], axis=1)


    def apply_position_sizing(self, total_capital=100000, risk_per_trade=0.01):
        """
        Tính Position Size
        Công thức: Size = Risk / (Volatility * Price) * Signal
        """ 
        risk_amount = total_capital * risk_per_trade
        pre_price = self.df['Adj Close'].shift(1)
        pre_sigma = self.df['Volatility'].shift(1)
        pre_signal = self.df['Signal'].shift(1)

        # Tính số lượng cổ phiếu lý thuyết
        raw_size = risk_amount / (pre_price * pre_sigma).replace(0, np.nan)
        # Xử lý chia cho 0 hoặc NaN
        raw_size = raw_size.replace([np.inf, -np.inf], 0).fillna(0)
        
        # Áp dụng Signal
        # Làm tròn xuống (Số lượng cổ phiếu phải là số nguyên)
        final_position = (raw_size * pre_signal).astype(int)

        final_position.columns = pd.MultiIndex.from_product([['Position Size'], self.tickers])
        
        if 'Position Size' in self.df.columns:
            self.df = self.df.drop(columns=['Position Size'])
        self.df = pd.concat([self.df, final_position], axis=1)


    def get_actions(self, date_str=None):
        """
        Danh sách các lệnh cần thực hiện.
        """
        target_date = self.get_target_date(date_str)
        actions = []
        
        current_idx = self.df.index.get_loc(target_date)
        if current_idx == 0:        # Ngày đầu tiên, không có dữ liệu trước đó
            return pd.DataFrame()
        
        pre_date = self.df.index[current_idx - 1]
        
        for ticker in self.tickers:
            target_shares = self.df.loc[target_date, ('Position Size', ticker)]
            current_shares = self.df.loc[pre_date, ('Position Size', ticker)]
            delta = target_shares - current_shares
            
            if delta != 0:
                price_est = self.df.loc[pre_date, ('Adj Close', ticker)]
                actions.append({
                    'Ticker': ticker,
                    'Action': 'BUY' if delta > 0 else 'SELL',
                    'Shares': int(abs(delta)),
                    'Price_Est': price_est,
                    'Value_Est': abs(delta) * price_est
                })
        
        if not actions:
            return pd.DataFrame()
        
        return pd.DataFrame(actions)   
    
    
    def get_target_date(self, date_str=None):
        # Xác định ngày cần tìm kiếm
        if date_str is None:
            search_date = self.df.index[-1]        # Mặc định lấy ngày cuối cùng
        else:
            search_date = pd.to_datetime(date_str)
        
        # Nếu không phải Business Day, lấy ngày gần nhất trước đó
        # Nếu không có trong phạm vi tìm kiếm, báo lỗi
        valid_dates = self.df.index[self.df.index <= search_date]
        
        if len(valid_dates) == 0:
            raise ValueError("Không có ngày cần tìm trong dữ liệu.")
            return
        
        target_date = valid_dates[-1]   # Lấy ngày hợp lệ gần nhất
        if target_date.date() != search_date.date():
            print(f"{search_date.date()} là ngày nghỉ/lễ.\nDùng dữ liệu ngày gần nhất: {target_date.date()}")
        
        return target_date
    
    
    def get_portfolio_at_date(self, date_str=None):
        """
        Danh mục đầu tư tại một ngày cụ thể.
        """
        target_date = self.get_target_date(date_str)
        portfolio_data = []
        
        for ticker in self.tickers:
            shares = self.df.loc[target_date, ('Position Size', ticker)]
            
            if shares != 0:     # Có Long hoặc Short
                price = self.df.loc[target_date, ('Adj Close', ticker)]
                vol = self.df.loc[target_date, ('Volatility', ticker)]
                
                portfolio_data.append({
                    'Ticker': ticker,
                    'Price': price,
                    'Volatility': vol,
                    'Action': "LONG" if shares > 0 else "SHORT",
                    'Shares': int(shares),
                    'Value': abs(shares) * price
                })
        
        if portfolio_data:
            df_result = pd.DataFrame(portfolio_data)
            # Sắp xếp theo Value giảm dần để thấy mã quan trọng nhất trước
            df_result = df_result.sort_values(by='Value', ascending=False).reset_index(drop=True)
            return df_result
        else:
            return pd.DataFrame()       # Nếu không giao dịch
        
        
    def get_top_portfolio(self, date_str=None, top_n=5):
        """
        Top N mã Long và Short có quy mô vốn lớn nhất trong danh mục.
        """
        df_full = self.get_portfolio_at_date(date_str)
        if df_full.empty:
            print("Không có giao dịch.")
            return pd.DataFrame()
        
        print(f"Ngày giao dịch: {self.get_target_date(date_str).date()}")
        # Lấy top N Long và Short
        top_long = df_full[df_full['Action'] == 'LONG'].head(top_n)
        top_short = df_full[df_full['Action'] == 'SHORT'].head(top_n)
        top_portfolio = pd.concat([top_long, top_short]).reset_index(drop=True)
        return top_portfolio