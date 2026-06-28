from pathlib import Path

from fastmcp import FastMCP
from starlette.responses import FileResponse

mcp = FastMCP("mcp-sandbox")


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


if __name__ == "__main__":
    # ponytail: bind localhost only — nginx terminates TLS and proxies to /mcp/.
    mcp.run(transport="http", host="127.0.0.1", port=8000)
