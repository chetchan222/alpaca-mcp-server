import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from mcp.server.sse import SseServerTransport
from alpaca_mcp_server.server import mcp  # Use the 'mcp' object defined in server.py

# 定義 SSE 連線處理函數
async def handle_sse(request):
    # 建立一個與 /messages 溝通的傳輸通道
    transport = SseServerTransport("/messages")
    
    # 啟動 SSE 串流 using the mcp instance
    async with mcp.run(transport.read_stream, transport.write_stream, request.scope.get("mcp_init_options", {})):
        await transport.handle_sse(request)

# 定義訊息接收處理函數 (HiAgent 發送指令的地方)
async def handle_messages(request):
    # 這裡只是一個佔位符，實際的 SSE Transport 會自動處理 POST 到 /messages 的請求
    # 但我們需要這個路由存在，Starlette 才能導向
    async with SseServerTransport("/messages") as transport:
        await transport.handle_post_message(request.scope, request.receive, request._send)

# 建立 Starlette 網頁應用
routes = [
    Route("/sse", endpoint=handle_sse),
    Route("/messages", endpoint=handle_messages, methods=["POST"])
]

app = Starlette(debug=True, routes=routes)

# 如果直接執行此檔案則啟動伺服器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
