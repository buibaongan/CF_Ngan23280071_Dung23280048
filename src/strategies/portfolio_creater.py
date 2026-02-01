import numpy as np
import pandas as pd

class AlphaCombiner:
    def combine(self, signal_list):
        sig1, sig2 = signal_list
        combined = np.where(np.sign(sig1) == np.sign(sig2), (sig1 + sig2)/2, 0)
        return pd.DataFrame(combined, index=sig1.index, columns=sig1.columns)
    

class Portfolio:
    def __init__(self, signals, returns, max_weight=0.1):
        self.max_weight = max_weight
        self.signals = signals
        self.returns = returns
        self.weights = None
        self.portfolio_returns = None

    def build_weights(self):
        """
        signals: DataFrame (-1,0,1)
        return: portfolio weights
        """

        # Raw weight
        x = self.signals.copy()

        # De-mean
        x = x.sub(x.mean(axis=1), axis=0)

        # Re-scale
        abs_sum = x.abs().sum(axis=1)
        w = x.div(abs_sum, axis=0).replace([np.inf, -np.inf], 0).fillna(0)

        # Cap weight
        w = w.clip(lower=-self.max_weight, upper=self.max_weight)

        # Re-scale after cap
        abs_sum = w.abs().sum(axis=1)
        w = w.div(abs_sum, axis=0).fillna(0)
        self.weights = w
        return w

    def compute_returns(self, transaction_cost=0.0005):
        """
        weights: DataFrame w(t)
        returns: DataFrame R(t)
        """
        if self.weights is None:
            raise ValueError("Run build_weights first")
        shifted_w = self.weights.shift(1).fillna(0)
        raw_returns = (shifted_w * self.returns).sum(axis=1)

        turnover = (self.weights - self.weights.shift(1).fillna(0)).abs().sum(axis=1)
        costs = turnover * transaction_cost
        
        self.portfolio_returns = raw_returns - costs
        return self.portfolio_returns
    

    def compute_benchmark(self):
        simple_returns = np.exp(self.returns) - 1
        benchmark_returns = simple_returns.mean(axis=1)
        benchmark_curve = (1 + benchmark_returns).cumprod()
        return benchmark_returns, benchmark_curve

    

    