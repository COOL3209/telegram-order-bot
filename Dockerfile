# 使用官方 Python 映像檔
FROM python:3.10-slim

# 安裝 unixODBC 系統函式庫（包含 libodbc.so.2）
RUN apt-get update && \
    apt-get install -y unixodbc unixodbc-dev gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製程式碼進容器
COPY . .

# 安裝 Python 套件
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 啟動 Bot
CMD ["python", "order_query_bot_v2.py"]