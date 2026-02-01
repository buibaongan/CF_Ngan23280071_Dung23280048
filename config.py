import os

# --- 1. QUẢN LÝ ĐƯỜNG DẪN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# --- 2. THAM SỐ DỮ LIỆU ---
tickers = [
    # Technology (Công nghệ)
    "AAPL","MSFT","GOOGL","AMZN","META",
    "NVDA","AMD","INTC","AVGO",
    "ADBE","CRM","ORCL","IBM",
    "SAP","ASML","QCOM","TXN",
    "UBER","SHOP","XYZ","NFLX","SONY",
    "INTU","ADSK","SNOW",

    # Financials (Tài chính – ngân hàng – đầu tư)
    "JPM","BAC","WFC","C",
    "GS","MS","BRK-A","BRK-B",
    "V","MA","PYPL","AXP",
    "SCHW","BLK","HSBC","RY",
    "CME","BK",

    # Consumer (Tiêu dùng – bán lẻ – giải trí)
    "WMT","COST","HD","TGT",
    "MCD","SBUX","KO","PEP",
    "PG","UL","DEO","PM",
    "NKE","DIS","CMG","TSM",
    "EA","TTWO","RBLX",
    "MGM","YUM",

    # Industrials (Công nghiệp – vận tải – quốc phòng)
    "CAT","DE","BA","LMT",
    "UPS","FDX","GE","HON",
    "MMM","RTX","NOC","GD",
    "EMR",

    # Energy & Materials (Năng lượng – nguyên vật liệu)
    "XOM","CVX","BP","SHEL",
    "COP","SLB","HAL","EOG",
    "LIN","APD","SHW","FCX","NUE",

    # Healthcare (Y tế – dược phẩm – bảo hiểm y tế)
    "JNJ","PFE","MRK","ABT","ABBV",
    "UNH","CVS","TMO","BMY","AMGN"
]

start_date = '2010-01-01'
end_date = '2025-10-11'

# --- 3. THAM SỐ CHIẾN THUẬT & KIỂM THỬ ---
short_window = 50
long_window = 200
momentum_threshold = 0.01
mr_window = 20
mr_std = 2

initial_capital = 100000
transaction_cost = 0.001
train_end = '2020-12-31'
val_end = '2023-12-31'

risk_free_rate = 0.045

# --- 4. KHÔNG GIAN THAM SỐ ---
momentum_params = {
    'threshold': [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1],
    'window': [20, 50, 100, 200]  
}
mean_reversion_params = {
    'window': [20, 50, 100, 200],
    'std_dev': [1, 1.5, 2, 2.5, 3]
}
