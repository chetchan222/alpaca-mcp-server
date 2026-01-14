# 使用 Python 3.10 作為基礎環境
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝 gcc 等基礎工具 (避免安裝依賴時出錯)
RUN apt-get update && apt-get install -y gcc

# 複製所有程式碼到容器內
COPY . .

# 安裝 Alpaca MCP Server (包含依賴) 以及 uvicorn (網頁伺服器)
# 注意：這裡我們直接安裝當前目錄的程式碼
RUN pip install --no-cache-dir . uvicorn

# 告訴 Render 我們會用 8000 端口
EXPOSE 8000

# 啟動指令：強制開啟 HTTP 模式
# 注意：這裡假設官方代碼支援 --transport 參數。
# 如果官方代碼不支援，我們需要確保安裝了最新版的 mcp SDK
CMD ["python", "-m", "alpaca_mcp_server.server", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]