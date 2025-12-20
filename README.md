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
├── market_data.py           # Tải và lưu trữ dữ liệu từ Yahoo Finance
├── data_processor.py        # Tiền xử lý, làm sạch dữ liệu và xử lý nhiễu
├── calculate_indicators.py  # Tính toán các chỉ số kỹ thuật
├── trading_strategy.py      # Chiến thuật giao dịch: Momentum, Mean Reversion
├── plot.py                  # Trực quan hóa 
├── scripts-Final.ipynb      # File thực thi tổng hợp (Main Workflow)
└── README.md  
```                  
## 4. Hướng dẫn cài đặt
```
python
python --version
python -m venv venv
```
## 5. Hướng dẫn chạy
_Chạy trên file scripts-Final.ipynb để theo dõi luồng xử lý._