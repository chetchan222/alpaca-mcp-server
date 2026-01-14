FROM python:3.10-slim

WORKDIR /app

# 安裝編譯工具，避免部分套件安裝失敗
RUN apt-get update && apt-get install -y gcc

# 複製所有檔案
COPY . .

# 安裝依賴庫，包含 starlette 和 uvicorn (網頁伺服器核心)
RUN pip install --no-cache-dir . uvicorn starlette

# 暴露端口
EXPOSE 8000

# 【關鍵修改】使用 uvicorn 啟動我們剛剛建立的 main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
