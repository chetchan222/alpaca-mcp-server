import uvicorn
from starlette.applications import Starlette
from mcp.server.transport_security import TransportSecuritySettings
from alpaca_mcp_server.server import mcp

# Disable DNS rebinding protection to allow any Host header.
# This fixes the "Invalid Host header" error when running behind proxies or in unknown environments.
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
    allowed_hosts=["*"],
    allowed_origins=["*"]
)

# FastMCP handles the SSE and message endpoints automatically via sse_app().
mcp_sse_app = mcp.sse_app()

# Create the main Starlette application and mount the MCP SSE app.
app = Starlette(debug=True)
app.mount("/", mcp_sse_app)

if __name__ == "__main__":
    # Start the server using uvicorn
    # We bind to 0.0.0.0 to allow external access (e.g., from Docker host)
    uvicorn.run(app, host="0.0.0.0", port=8000)
