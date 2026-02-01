# **DỰ ÁN: HỆ THỐNG PHÂN TÍCH DỮ LIỆU TÀI CHÍNH VÀ THỰC THI CHIẾN THUẬT GIAO DỊCH**

## **1. Xác định bài toán**
* **Lĩnh vực:** Tài chính / Đầu tư chứng khoán.
* **Loại bài toán:** Phân tích dữ liệu chuỗi thời gian (Time-series) và Xây dựng hệ thống giao dịch dựa trên quy tắc (Rule-based Trading).
* **Input:** Dữ liệu gồm các cột OHLC, Adj Close, Volumn download từ Yahoo Finance.
* **Output:** Tín hiệu giao dịch (Buy/Sell), các chỉ số kỹ thuật và báo cáo cơ cấu danh mục đầu tư (Portfolio Distribution).

## **2. Giới thiệu Dataset**
Dữ liệu được quản lý dưới dạng Multi-Index DataFrame để xử lý đồng thời nhiều mã chứng khoán.
| Cột | Mô tả |
|:----|:------|
| **Open** | Giá mở cửa của phiên giao dịch. |
| **High** | Giá cao nhất đạt được trong phiên. |
| **Low** | Giá thấp nhất trong phiên. |
| **Close** | Giá đóng cửa khi kết thúc phiên. |                  
| **Adj Close** | Giá đóng cửa điều chỉnh (đã tính cổ tức/chia tách). |          
| **Volume** | Tổng khối lượng giao dịch trong phiên. |

## 3. Cấu trúc 
```
project/
├── src/
│   ├── data/
│   │   ├── data_loader.py          # Tải và lưu trữ dữ liệu từ Yahoo Finance.
│   │   └── data_processor.py       # Tiền xử lý và làm sạch dữ liệu.
│   ├── features/
│   │   └── calculate_indicators.py # Tính toán các chỉ số kỹ thuật.
│   ├── strategies/
│   │   ├── momentum.py             # Momentum Strategy.
│   │   └── mean_reversion.py       # Mean-Reversion Strategy.
│   ├── backtest/
│   │   ├── backtester.py           # Chạy kiểm thử và đánh giá.
│   │   └── visualizer.py           # Trực quan hóa kết quả.
│   └── portfolio/
│       └── portfolio_creater.py    # Danh mục đầu tư.
├── plot.py                         # Các hàm hỗ trợ vẽ biểu đồ.
├── config.py
└── README.md                    
```                  
## 4. Hướng dẫn cài đặt
```
python
python --version
python -m venv venv
```
## 5. Hướng dẫn chạy
_Chạy trên file main.ipynb để theo dõi luồng xử lý._