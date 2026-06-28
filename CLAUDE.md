# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A public MCP (Model Context Protocol) server of **test fixtures** for QA and
evals. Each tool returns deliberately distinctive output so a caller can prove a
response originated from this server, not from the model's own training/context.
Planned to host on AWS Lightsail (Ubuntu) behind nginx + Let's Encrypt.

## Commands

```bash
uv sync                 # install deps into .venv
uv run server.py        # run server: guide at :8000/ , MCP at :8000/mcp
uv add <pkg>            # add a dependency
```

There is no test framework — the tools are constant returns. To smoke-test a
tool in-memory (no network), use the FastMCP `Client` against the `mcp` object:

```bash
uv run python -c "
import asyncio; from fastmcp import Client; from server import mcp
async def m():
    async with Client(mcp) as c:
        print((await c.call_tool('identity', {})).content[0].text)
asyncio.run(m())"
```

## Architecture

Single-process design: **one uvicorn serves both** the static guide and the MCP
endpoint, from `server.py`:

- `@mcp.tool` functions are the MCP tools (currently just `identity`).
- `@mcp.custom_route("/")` serves `web/index.html` (the visitor guide).
- `mcp.run(transport="http", ...)` = FastMCP **streamable HTTP** transport.

Routes (same port):
- `GET /` → guide page
- `POST /mcp` → MCP endpoint

Two more tools are planned and go in the same `server.py` as additional
`@mcp.tool` functions — no new files needed.

## Gotchas

- **Endpoint is `/mcp`, no trailing slash.** FastMCP 3.x 307-redirects `/mcp/`
  → `/mcp`, and `mcp-remote` (the Claude Desktop bridge) drops the POST body
  across that redirect → 404. Always configure clients with `/mcp`.
- **Bind `127.0.0.1` only.** nginx terminates TLS and proxies in; the app port
  is never exposed publicly. `deploy/nginx.conf` uses `location /mcp` (matches
  both `/mcp` and the redirect). It does not yet proxy `/` — add a `location /`
  block to serve the guide publicly.
- **`web/index.html` fills in the live URL via JS** (`location.origin`), so the
  Claude config snippets show the real deployed URL with no hardcoding.

## Tool design convention

Tool output should be a **unique, improbable canary** that a model would never
volunteer (e.g. `MCP-SANDBOX canary 7Q9X-...`) — that's how callers verify the
response came from the MCP. Avoid false/sensitive *factual claims* as canaries:
models refuse to relay them, which defeats interactive testing. For evals,
assert on the **raw tool result** (`result.content[0].text`), not the model's
prose — the token is stable, the wording isn't.

## Deploy

Lightsail Ubuntu: `uv sync`, run via `deploy/mcp-sandbox.service` (systemd),
front with `deploy/nginx.conf` + `certbot --nginx -d <domain>`. Open ports
80/443 only. See `README.md` for the step-by-step.
