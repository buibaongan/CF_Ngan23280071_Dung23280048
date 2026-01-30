import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizer:
    @staticmethod
    def plot_strategy_vs_benchmark(strategy_curve, benchmark_curve, title="Strategy vs Market Benchmark"):
        """
        So sánh chiến lược với thị trường (Benchmark)
        """
        plt.figure(figsize=(15, 7))
        sns.set_style("whitegrid")
        
        # Vẽ đường chiến lược và benchmark
        plt.plot(strategy_curve, label="Momentum Strategy", linewidth=2.5, color='#1f77b4')
        plt.plot(benchmark_curve, label="Market Benchmark (Equal Weight)", linewidth=2, color='#ff7f0e', linestyle='--')
        
        # Tô màu vùng Drawdown của chiến lược (Week 5)
        peak = strategy_curve.cummax()
        plt.fill_between(strategy_curve.index, strategy_curve, peak, color='gray', alpha=0.15, label="Strategy Drawdown")

        plt.title(title, fontsize=16, fontweight='bold')
        plt.ylabel("Portfolio Value ($)", fontsize=12)
        plt.legend(loc="upper left")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_tuning_heatmap(results_df, metric='Sharpe Ratio'):
        """
        Vẽ Heatmap để tìm 'vùng xanh' tham số ổn định thay vì chọn điểm ăn may
        """
        plt.figure(figsize=(10, 6))
        # Nếu chỉ có 1 tham số, ta vẽ dạng thanh màu (Color Bar)
        plot_data = results_df.set_index('Threshold')[[metric]]
        sns.heatmap(plot_data.T, annot=True, cmap='RdYlGn', center=0, cbar_kws={'label': metric})
        
        plt.title(f"Parameter Sensitivity Analysis ({metric})", fontsize=14)
        plt.show()

    @staticmethod
    def plot_underwater(equity_curve):
        """Biểu đồ soi kỹ các giai đoạn 'nằm dưới nước' (Week 5)"""
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        plt.figure(figsize=(15, 3))
        plt.fill_between(drawdown.index, drawdown, 0, color='#e74c3c', alpha=0.4)
        plt.axhline(0, color='black', linewidth=1)
        plt.title("Underwater Plot (Risk Analysis)", color='#c0392b', fontweight='bold')
        plt.ylabel("Drawdown %")
        plt.show()