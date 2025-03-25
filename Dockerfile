FROM python:3.12-slim

# 安裝必要套件與 ODBC Driver
RUN apt-get update &&     apt-get install -y gnupg2 curl unixodbc-dev gcc g++ &&     curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - &&     curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list &&     apt-get update &&     ACCEPT_EULA=Y apt-get install -y msodbcsql17 &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*

# 複製程式碼
WORKDIR /app
COPY . /app

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 啟動程式
CMD ["python", "order_query_bot_v2.py"]