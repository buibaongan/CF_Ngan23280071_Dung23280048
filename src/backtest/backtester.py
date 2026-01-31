import pandas as pd
import numpy as np
import itertools 
class Backtester:
    def __init__(self, df, initial_capital=100000, transaction_cost=0.001):
        self.df = df
        self.initial_capital = initial_capital
        self.cost = transaction_cost

    def split_data(self, train_end, val_end):
        """Chia dữ liệu train/val/test theo thời gian."""
        train_data = self.df.loc[:train_end]
        val_data = self.df.loc[train_end:val_end]
        test_data = self.df.loc[val_end:]
        return train_data, val_data, test_data

    def run_backtest_with_weights(self, weights):
        """
        Chạy Backtest dựa trên trọng số (weights).
        """
        # 1. Đồng bộ Index
        common_idx = self.df.index.intersection(weights.index)
        log_returns = self.df.loc[common_idx, "Log Return"]
        simple_return = np.exp(log_returns) - 1
        
        # 2. Xử lý Trọng số (Reindex & Fillna)
        w = weights.loc[common_idx].reindex(columns=log_returns.columns).fillna(0)
        shifted_w = w.shift(1).fillna(0)
        
        # 3. Tính toán
        gross_return = (shifted_w * simple_return).sum(axis=1)
        turnover = shifted_w.diff().abs().sum(axis=1)
        cost = turnover * self.cost
        
        # 5. Equity Curve
        equity = (1 + gross_return - cost).cumprod() * self.initial_capital
        
        return equity
    
    
    def run_backtest_with_signals(self, data, signals):
        """
        Chạy Backtest dựa trên signals.
        """
        # 1. Đồng bộ dữ liệu
        if isinstance(signals.columns, pd.MultiIndex):
            signals.columns = signals.columns.get_level_values(-1)
        common_idx = data.index.intersection(signals.index)
        signals = signals.loc[common_idx].reindex(columns=data['Adj Close'].columns).ffill().fillna(0)

        # 2. CHUYỂN ĐỔI SIGNALS -> WEIGHTS (Equal Weighting)
        active_pos = signals.abs().sum(axis=1).replace(0, np.nan)
        weights = signals.div(active_pos, axis=0).fillna(0)
        
        return self.run_backtest_with_weights(weights)

    def evaluate(self, equity):
        """Tính các chỉ số đánh giá (Sharpe Ratio, Drawdown)."""
        ret = equity.pct_change().dropna()
        sharpe = (ret.mean() / ret.std() * np.sqrt(252)) if ret.std() > 0 else 0
        
        peak = equity.cummax()
        drawdown = ((equity - peak) / peak).min()

        return {
            "Total Return": f"{equity.iloc[-1]/self.initial_capital - 1:.2%}",
            "Sharpe Ratio": round(sharpe, 2),
            "Max Drawdown": f"{drawdown:.2%}",
        }

    def run_and_evaluate(self, data, strategy_cls, label, **params):
        """Chạy 1 lần backtest."""
        # Khởi tạo chiến lược với bất kỳ tham số nào được truyền vào (**params)
        strategy = strategy_cls(data, **params)
        signals = strategy.generate_signals()
        
        equity = self.run_backtest(data, signals)
        metrics = pd.DataFrame([self.evaluate(equity)], index=[label])
        return equity, metrics

    def optimize_grid_search(self, data, strategy_cls, param_grid):
        """
        Tối ưu tham số.
        """
        results = []
        
        # Tạo tất cả các tổ hợp tham số
        keys, values = zip(*param_grid.items())
        combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

        for params in combinations:
            label_parts = [f"{k}={v}" for k, v in params.items()]
            label = "_".join(label_parts)
            
            # Chạy Backtest với bộ tham số hiện tại
            _, metrics = self.run_and_evaluate(data, strategy_cls, label, **params)
            
            # Kết quả
            res = metrics.iloc[0].to_dict()
            res.update(params) 
            results.append(res)
        
        # Trả về bảng kết quả sắp xếp theo Sharpe
        return pd.DataFrame(results).sort_values(by='Sharpe Ratio', ascending=False)