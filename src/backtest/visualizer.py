import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizer:
    @staticmethod
    def plot_strategy_vs_benchmark(strategy_curve, benchmark_curve, title="Strategy vs Market Benchmark"):
        """
        So sánh chiến lược với thị trường (Benchmark)
        """
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 1. Vẽ Benchmark
        ax.plot(benchmark_curve.index, benchmark_curve, label="Benchmark (Market)", 
                linewidth=1.5, color='gray', alpha=0.8)
        
        # 2. Vẽ Strategy
        ax.plot(strategy_curve.index, strategy_curve, label="Momentum Strategy", 
                linewidth=2, color='#0056b3')
        
        # 3. Vùng Drawdown 
        peak = strategy_curve.cummax()
        ax.fill_between(strategy_curve.index, strategy_curve, peak, color='red', alpha=0.1, label="Drawdown Area")

        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        ax.set_ylabel("Portfolio Value ($)", fontsize=11)
        ax.legend(loc="upper left", frameon=True)
        
        fmt = '${x:,.0f}'
        tick = mtick.StrMethodFormatter(fmt)
        ax.yaxis.set_major_formatter(tick)
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_tuning_heatmap(results_df, metric='Sharpe Ratio'):
        """
        Vẽ Heatmap kết quả tối ưu hóa đa tham số (Grid Search).
        """
        plt.figure(figsize=(8, 6))
        pivot_table = results_df.pivot(index='Window', columns='Threshold', values=metric)


        sns.heatmap(pivot_table, annot=True, fmt=".2f", 
                    cmap='RdYlGn', center=0, linewidths=.5, cbar_kws={'label': metric})
        
        plt.title(f"Heatmap({metric})", fontsize=14, fontweight='bold', pad=15)
        plt.ylabel("Window", fontsize=11)
        plt.xlabel("Threshold", fontsize=11)
        
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_underwater(equity_curve):
        """
        Biểu đồ Underwater: Chỉ hiển thị phần trăm sụt giảm từ đỉnh
        """
        # Tính Drawdown
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        
        fig, ax = plt.subplots(figsize=(12, 3))
        
        ax.fill_between(drawdown.index, drawdown, 0, color='#d63031', alpha=0.6)
        ax.plot(drawdown.index, drawdown, color='#c0392b', linewidth=1)

        ax.axhline(0, color='black', linewidth=0.8, linestyle='-')
        
        ax.set_title("Underwater Plot (Drawdown Risk)", fontsize=12, fontweight='bold', color='#c0392b')
        ax.set_ylabel("Drawdown (%)")
        
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()