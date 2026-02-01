import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizer:
    
    @staticmethod
    def plot_strategy_vs_benchmark(strategy_curve, benchmark_curve, title="Cumulative Return Performance"):
        """
        Vẽ biểu đồ so sánh Lợi suất tích lũy (Cumulative Return) giữa Strategy và Benchmark.
        """
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 1. CHUẨN HÓA DỮ LIỆU
        strat_pct = (strategy_curve / strategy_curve.iloc[0]) - 1
        bench_pct = (benchmark_curve / benchmark_curve.iloc[0]) - 1
        
        # 2. VẼ BENCHMARK
        ax.plot(bench_pct.index, bench_pct, label="Benchmark (Buy & Hold)", 
                linewidth=1, color='gray', alpha=0.7, linestyle='--')
        
        # 3 VẼ STRATEGY
        ax.plot(strat_pct.index, strat_pct, label="Momentum Strategy", 
                linewidth=1.5, color='#0056b3')
        
        # 4. TRỰC QUAN HÓA SỰ CHÊNH LỆCH
        # Vùng Xanh (Outperformance)
        ax.fill_between(strat_pct.index, strat_pct, bench_pct, where=(strat_pct >= bench_pct), 
                        color='green', alpha=0.1, interpolate=True, label='Outperformance')
        
        # Vùng Đỏ (Underperformance)
        ax.fill_between(strat_pct.index, strat_pct, bench_pct, where=(strat_pct < bench_pct), 
                        color='red', alpha=0.1, interpolate=True, label='Underperformance')

        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        ax.set_ylabel("Cumulative Return (%)", fontsize=12)
        ax.set_xlabel("Date", fontsize=12)
        ax.legend(loc="upper left", framealpha=0.9, fancybox=True)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_tuning_heatmap(results_df, metric='Sharpe Ratio'):
        """
        Vẽ biểu đồ Heatmap để phân tích độ nhạy của tham số.
        """
        plt.figure(figsize=(10, 7))
        
        pivot_table = results_df.pivot(index='Window', columns='Threshold', values=metric)

        ax = sns.heatmap(pivot_table, annot=True, fmt=".2f", 
                         cmap='RdYlGn', center=0, linewidths=.5, 
                         cbar_kws={'label': metric})
        
        plt.title(f"Parameter Sensitivity Analysis ({metric})", fontsize=14, fontweight='bold', pad=20)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_underwater(strategy_curve, benchmark_curve=None):
        """
        Vẽ biểu đồ Underwater (Drawdown Profile) để phân tích rủi ro của chiến lược.
        """
        fig, ax = plt.subplots(figsize=(12, 5))

        strat_peak = strategy_curve.cummax()
        strat_dd = (strategy_curve - strat_peak) / strat_peak
        
        # Vẽ vùng đỏ thể hiện rủi ro của Strategy
        ax.fill_between(strat_dd.index, strat_dd, 0, color='#d63031', alpha=0.3, label="Strategy Drawdown")
        ax.plot(strat_dd.index, strat_dd, color='#d63031', linewidth=1)

        # XỬ LÝ BENCHMARK
        if benchmark_curve is not None:
            bench_peak = benchmark_curve.cummax()
            bench_dd = (benchmark_curve - bench_peak) / bench_peak
            
            # Vẽ đường nét đứt màu xám cho Benchmark
            ax.plot(bench_dd.index, bench_dd, color='gray', linewidth=1, linestyle='--', alpha=0.8, label="Benchmark Drawdown")
        
        ax.axhline(0, color='black', linewidth=0.8)

        ax.set_title("Drawdown Profile & Risk Analysis", fontsize=14, fontweight='bold', color='#c0392b', pad=15)
        ax.set_ylabel("Drawdown (%)", fontsize=12)
        ax.set_xlabel("Date", fontsize=12)
        ax.legend(loc="lower left", framealpha=0.9)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.show()
        
    @staticmethod
    def plot_rolling_sharpe(strategy_data, window=126, risk_free_rate=0):
        """
        Vẽ Rolling Sharpe Ratio.
        """
        # 1. KIỂM TRA VÀ CHUẨN HÓA DỮ LIỆU ĐẦU VÀO
        if strategy_data.mean() > 1:
            print("CẢNH BÁO: Phát hiện dữ liệu đầu vào là Portfolio Value ($). Đang chuyển đổi sang Returns (%)...")
            returns = strategy_data.pct_change().fillna(0)
        else:
            returns = strategy_data
            
        # 2. TÍNH TOÁN SHARPE
        # Trừ đi lãi suất phi rủi ro (Risk Free Rate - thường lấy theo ngày, ví dụ 0)
        excess_returns = returns - (risk_free_rate / 252)
        
        # Tính Mean và Std
        rolling_mean = excess_returns.rolling(window=window).mean()
        rolling_std = excess_returns.rolling(window=window).std()
        
        # Annualized Sharpe Ratio
        rolling_sharpe = (rolling_mean / (rolling_std + 1e-9)) * np.sqrt(252)
        
        # 3. VẼ BIỂU ĐỒ
        plt.figure(figsize=(12, 5))
        plt.plot(rolling_sharpe.index, rolling_sharpe, label=f"Rolling Sharpe ({window} days)", color='#e67e22', linewidth=1.5)
        
        # CÁC ĐƯỜNG THAM CHIẾU
        plt.axhline(risk_free_rate, color='firebrick', linewidth=2, linestyle='--', 
                    label=f"Risk-Free Performance (Rf={risk_free_rate:.1%})")
        
        # plt.axhline(0, color='black', linewidth=1.5)                        
        # plt.axhline(0.5, color='gray', linestyle=':', alpha=0.8, label="Market Avg (~0.5)")                
        # plt.axhline(1.0, color='green', linestyle='--', alpha=0.8, label="Institutional (>1.0)")   
        # plt.axhline(2.0, color='gold', linestyle='--', alpha=0.8, label="Top Tier (>2.0)")                   
        # plt.axhline(3.0, color='red', linestyle='-.', alpha=0.6, label="Anomaly (>3.0)")    
        
        plt.ylim(bottom=max(-5, rolling_sharpe.min()), top=min(6, rolling_sharpe.max()))
        plt.title("Rolling Sharpe Ratio (Annualized)", fontsize=14, fontweight='bold')
        plt.ylabel("Sharpe Ratio")
        plt.legend(loc="upper left")
        plt.grid(True, linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.show()