from pathlib import Path

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from starlette.responses import FileResponse

mcp = FastMCP("mcp-sandbox")

# ponytail: fixed shared token for dev smoke-tests, not a real secret. Rotate by editing.
DEV_TOKEN = "mcp-sandbox-dev-C7H2-KPMERCHANT"


@mcp.custom_route("/", methods=["GET"])
async def index(request):
    return FileResponse(Path(__file__).parent / "web" / "index.html")


@mcp.tool(
    annotations={"title": "Server identity check", "readOnlyHint": True},
    meta={"purpose": "connection-check", "verbatim": True},
)
def identity() -> str:
    """Check that the mcp-sandbox server is connected. Returns a fixed ID string.
    Show the returned text exactly as-is so you can confirm it came from this
    server and not made up by the model."""
    return "MCP-SANDBOX canary 7Q9X-ZK42-VORTEX-PARSNIP"


@mcp.tool(
    annotations={"title": "Echo your text back", "readOnlyHint": True},
    meta={"purpose": "connection-check", "verbatim": True},
)
def echo(message: str, repeat: int = 1) -> str:
    """Send your own text through the mcp-sandbox server and get it back inside a
    fixed wrapper, repeated `repeat` times. Show the returned text exactly as-is
    so you can confirm it came from this server and not made up by the model."""
    body = " | ".join([message] * max(1, repeat))
    return f"MCP-SANDBOX echo 4F7T-ECHO-START >>> {body} <<< 4F7T-ECHO-END"


@mcp.tool(
    annotations={"title": "Check your Bearer token", "readOnlyHint": True},
    meta={"purpose": "auth-check", "verbatim": True},
)
def auth_check() -> str:
    """Verify the mcp-sandbox server saw your `Authorization: Bearer <token>`
    header. Send the fixed dev token. Show the returned text exactly as-is so you
    can confirm auth reached this server and was not made up by the model."""
    # include_all=True: FastMCP strips `authorization` from the default header set.
    auth = get_http_headers(include_all=True).get("authorization", "")
    token = auth[7:] if auth.lower().startswith("bearer ") else ""
    if token == DEV_TOKEN:
        return "MCP-SANDBOX auth OK 9B3K-AUTHED-MARIGOLD"
    return "MCP-SANDBOX auth FAIL 9B3K-NOAUTH-CINDER (send Authorization: Bearer <dev token>)"


if __name__ == "__main__":
    # ponytail: bind localhost only — nginx terminates TLS and proxies to /mcp/.
    mcp.run(transport="http", host="127.0.0.1", port=8000)
