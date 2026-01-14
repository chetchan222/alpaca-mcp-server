import uvicorn
from starlette.applications import Starlette
from alpaca_mcp_server.server import mcp

# FastMCP handles the SSE and message endpoints automatically via sse_app().
# This avoids manually managing the SseServerTransport which caused the crash.
mcp_sse_app = mcp.sse_app()

# Create the main Starlette application and mount the MCP SSE app.
# By mounting at "/", the endpoints will be available at:
# - /sse (for SSE stream)
# - /messages (for posting messages)
app = Starlette(debug=True)
app.mount("/", mcp_sse_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)