import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, df, initial_capital=100000, transaction_cost=0.001):
        """
        df: DataFrame tổng (chứa Log Return)
        initial_capital: Vốn ban đầu (Week 9)
        transaction_cost: Phí giao dịch (Week 9)
        """
        self.df = df
        self.initial_capital = initial_capital
        self.cost = transaction_cost

    def split_data(self, train_end, val_end):
        """
        Chia dữ liệu theo Slide:
        - Training set: Dữ liệu sớm nhất đến cutoff.
        - Validation set: Dùng để tuning tham số.
        - Test set: Dữ liệu unseen cuối cùng để đánh giá.
        """
        train_data = self.df.loc[:train_end]
        val_data = self.df.loc[train_end:val_end]
        test_data = self.df.loc[val_end:]
        return train_data, val_data, test_data

    def run_backtest(self, data_segment, signals):
        """
        Thực hiện mô phỏng giao dịch (Đã sửa lỗi lệch cột và phí giao dịch)
        """
        # 1. Xử lý lệch tầng Index (MultiIndex) từ Strategy
        # Nếu signals có tầng 'Signal' ở trên, lấy tầng cuối (tên Ticker) để khớp với Log Return
        if isinstance(signals.columns, pd.MultiIndex):
            signals.columns = signals.columns.get_level_values(-1)

        # 2. Đồng bộ hóa Index (Ngày) giữa dữ liệu và tín hiệu
        common_index = data_segment.index.intersection(signals.index)
        data = data_segment.loc[common_index]
        log_returns = data['Log Return']

        # 3. Đồng bộ hóa Cột (Ticker) và xử lý dữ liệu thiếu
        # reindex giúp đảm bảo thứ tự các mã cổ phiếu trong pos khớp hoàn toàn với log_returns
        pos = signals.loc[common_index].reindex(columns=log_returns.columns).ffill().fillna(0)
        
        n_tickers = len(pos.columns)
        
        # 4. Tính lợi nhuận chiến thuật (Vị thế ngày t-1 * Return ngày t)
        # Sử dụng shift(1) để tránh look-ahead bias (nhìn trước tương lai)
        daily_ret = (pos.shift(1) * log_returns).sum(axis=1) / n_tickers
        
        # 5. Tính phí giao dịch (Đã sửa logic trọng số)
        # Phải chia n_tickers vì phí tính trên phần vốn phân bổ cho từng lệnh, không phải tổng vốn
        trades = pos.diff().abs().sum(axis=1)
        net_ret = daily_ret - ((trades / n_tickers) * self.cost)
        
        # 6. Tính Equity Curve (Lũy kế vốn theo Log Return)
        return np.exp(net_ret.cumsum()) * self.initial_capital
    
    def evaluate(self, equity_curve):
        """Tính chỉ số Sharpe và Drawdown (Week 5)"""
        returns_pct = equity_curve.pct_change().dropna()
        # Sharpe Ratio (Lợi nhuận/Rủi ro) chuẩn hóa 252 ngày
        sharpe = (returns_pct.mean() / returns_pct.std()) * np.sqrt(252) if returns_pct.std() != 0 else 0
        
        # Max Drawdown (Mức sụt giảm lớn nhất)
        peak = equity_curve.cummax()
        max_dd = ((equity_curve - peak) / peak).min()
    
        return {
            "Total Return": f"{(equity_curve.iloc[-1]/self.initial_capital)-1:.2%}",
            "Sharpe Ratio": round(sharpe, 2),
            "Max Drawdown": f"{max_dd:.2%}",
            "Final Capital": f"${equity_curve.iloc[-1]:,.2f}"
        }
        
    def run_and_evaluate(self, data, strategy_class, label, **params):
            """Phương thức chạy backtest và trả về metrics"""
            strategy = strategy_class(data, **params)
            signals = strategy.generate_signals()
            equity = self.run_backtest(data, signals)
            
            metrics_dict = self.evaluate(equity)
            metrics_df = pd.DataFrame([metrics_dict], index=[label])
            return equity, metrics_df

    def find_best_threshold(self, val_df, strategy_class, thresholds):
        """Phương thức tìm threshold tối ưu trên tập Validation"""
        best_sharpe = -float('inf')
        best_t = None
        for t in thresholds:
            _, metrics = self.run_and_evaluate(val_df, strategy_class, f"Val_{t}", threshold=t)
            # Ép kiểu để so sánh
            current_sharpe = float(metrics.loc[f"Val_{t}", "Sharpe Ratio"])
            if current_sharpe > best_sharpe:
                best_sharpe = current_sharpe
                best_t = t
        return best_t, best_sharpe