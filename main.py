import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from alpaca_mcp_server.server import mcp

# FastMCP provides a method to create a Starlette application for SSE transport.
# This handles both the /sse and /messages endpoints automatically.
mcp_sse_app = mcp.sse_app()

# Create the main Starlette application and mount the MCP SSE app
# We mount it at the root so that /sse and /messages are available directly.
app = Starlette(debug=True)
app.mount("/", mcp_sse_app)

if __name__ == "__main__":
    # Start the server using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)