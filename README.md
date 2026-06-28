# mcp-sandbox

**A free, open MCP server for developers and GenAI evaluations.**

Every tool returns a stable, improbable **canary token** — something a model
would never volunteer on its own. If the token shows up in a response, the call
really reached this Model Context Protocol (MCP) server. If it doesn't, the tool
was never invoked. That makes it a clean fixture for learning MCP, wiring up
clients, and asserting on tool calls in CI and evals.

🌐 **Live server:** `https://mcp.heptafox.com/mcp` &nbsp;·&nbsp; 📖 **Guide:** [mcp.heptafox.com](https://mcp.heptafox.com/)

---

## What is mcp-sandbox?

A public [MCP](https://modelcontextprotocol.io) server of **deterministic test
fixtures**. Each tool returns a fixed canary string instead of real data, so you
can prove a response originated from the server rather than the model's training
or context.

## Why use it?

When you're building or testing an agent, you usually *don't* want to point it at
a production MCP server. You want a deterministic endpoint that always returns a
known value. mcp-sandbox is that endpoint:

- 🎓 **Learn MCP** — connect a real server in minutes, no API keys or data setup.
- 🔌 **Test clients** — confirm your client actually calls tools and relays output.
- ✅ **Verify integrations** — prove the MCP layer works end to end.
- 🚦 **Smoke tests** — a one-call health check for CI/CD pipelines.
- 🧪 **Automated evals** — assert on a stable token, not on fuzzy model prose.

## Who is it for?

Developers learning MCP · AI application & agent-framework developers · QA
engineers · GenAI evaluation frameworks · CI/CD integration testing.

## Supported MCP clients

Works with any MCP-compatible client over streamable HTTP, including:

Claude Desktop · Claude Code · Cursor · Google ADK · LangChain · CrewAI ·
OpenAI Agents SDK · MCP Inspector

## Features

- ✨ **Stable canary tokens** — deterministic output you can assert on exactly.
- 🌐 **Streamable HTTP transport** — the modern MCP transport, endpoint `/mcp`.
- 🔑 **Bearer-token auth check** — a tool to verify auth reached the server.
- 🪶 **Zero setup** — no API keys, no accounts, no data.
- 🆓 **Free & open source** — Apache-2.0.

## Learning progression

The tools are ordered so you can climb from "is it connected?" to "did auth
arrive?" one concept at a time:

| Level | Tool         | Auth   | Params | Teaches            |
|:-----:|--------------|:------:|:------:|--------------------|
| 1     | `identity`   | No     | No     | Connectivity       |
| 2     | `echo`       | No     | Yes    | Passing parameters |
| 3     | `auth_check` | Bearer | No     | Authentication     |

## Tools

### `identity` — connectivity check
No params. Returns a fixed ID string. Show it verbatim to confirm the server answered.

```
MCP-SANDBOX canary 7Q9X-ZK42-VORTEX-PARSNIP
```

### `echo` — parameter passing
Params: `message: str`, `repeat: int = 1`. Sends your text through the server and
returns it inside a fixed wrapper, repeated `repeat` times.

```
MCP-SANDBOX echo 4F7T-ECHO-START >>> your text <<< 4F7T-ECHO-END
```

### `auth_check` — authentication
No params (reads the `Authorization` header). Verifies the server saw your
`Bearer` token.

```
MCP-SANDBOX auth OK 9B3K-AUTHED-MARIGOLD      # valid token
MCP-SANDBOX auth FAIL 9B3K-NOAUTH-CINDER      # missing/invalid token
```

## Authentication

`auth_check` is gated by a **public development Bearer token**:

```
Authorization: Bearer mcp-sandbox-dev-C7H2-KPMERCHANT
```

This is a shared smoke-test token for integration testing — **it is public and
is NOT a production credential.** It only gates `auth_check`.

## Quick Start

### Use the hosted server

**Claude Code** — one command:

```bash
claude mcp add --transport http mcp-sandbox https://mcp.heptafox.com/mcp \
  --header "Authorization: Bearer mcp-sandbox-dev-C7H2-KPMERCHANT"
```

**Claude Desktop** — config is stdio-only, so bridge through `mcp-remote` in
`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-sandbox": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "https://mcp.heptafox.com/mcp",
        "--header", "Authorization: Bearer mcp-sandbox-dev-C7H2-KPMERCHANT"
      ]
    }
  }
}
```

**Raw HTTP** — call the endpoint directly:

```bash
curl -X POST https://mcp.heptafox.com/mcp \
  -H "Authorization: Bearer mcp-sandbox-dev-C7H2-KPMERCHANT" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"identity","arguments":{}}}'
```

> **Endpoint is `/mcp` — no trailing slash.** `/mcp/` 307-redirects to `/mcp`,
> and some clients drop the POST body across the redirect. Always use `/mcp`.

### Run it locally

```bash
uv sync
uv run server.py        # guide at http://127.0.0.1:8000/ , MCP at /mcp
```

Inspect it with the MCP Inspector — point it at `http://127.0.0.1:8000/mcp`:

```bash
npx @modelcontextprotocol/inspector
```

## Examples

Ask any connected model to call a tool, then assert on the token it relays:

> **Prompt:** Call the mcp-sandbox `identity` tool and show me what it returned.
>
> **Expected:** `MCP-SANDBOX canary 7Q9X-ZK42-VORTEX-PARSNIP`

If the token appears, the call reached this server. If the model answers without
it, the tool was never invoked.

## QA & GenAI Evaluations

In evals, **assert on the raw tool result** (`result.content[0].text`), not on the
model's natural-language summary — the token is stable, the wording isn't.

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("https://mcp.heptafox.com/mcp") as c:
        result = await c.call_tool("identity", {})
        assert "7Q9X-ZK42-VORTEX-PARSNIP" in result.content[0].text

asyncio.run(main())
```

## Roadmap

- More beginner-friendly tools (error simulation, streaming, structured output)
- OAuth and additional authentication examples
- Client integration examples (Cursor, Google ADK, LangChain, CrewAI, OpenAI Agents SDK)
- Ready-made evaluation scenarios and tutorials

Have an idea? [Open an issue or discussion.](https://github.com/heptafox/mcp-sandbox/issues)

## Contributing

Contributions are welcome — especially beginner-friendly tools, client examples,
and docs. New tools are just `@mcp.tool` functions in `server.py`, each returning
a unique canary string. See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## Deploy your own

The hosted instance runs on AWS Lightsail (Ubuntu) behind nginx + Let's Encrypt.
To self-host: `uv sync`, run via `deploy/mcp-sandbox.service` (systemd), front
with `deploy/nginx.conf` + `certbot --nginx -d <domain>`, and open ports 80/443
only — the app binds to localhost and nginx proxies `/mcp` in. Step-by-step below.

<details>
<summary>Full deploy steps (AWS Lightsail, Ubuntu)</summary>

1. **Instance + DNS** — create an Ubuntu Lightsail instance, point your domain's
   A record at its static IP, and open ports **80 + 443** in the Lightsail
   firewall. Leave 8000 closed; the app listens on localhost only.
2. **App**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   git clone <repo> ~/mcp-sandbox && cd ~/mcp-sandbox && uv sync
   ```
3. **systemd** — copy `deploy/mcp-sandbox.service` to `/etc/systemd/system/`, then:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now mcp-sandbox
   ```
4. **nginx + TLS**
   ```bash
   sudo apt install -y nginx certbot python3-certbot-nginx
   # deploy/nginx.conf is set for mcp.heptafox.com; copy to /etc/nginx/sites-available/,
   # symlink into sites-enabled/, then:
   sudo certbot --nginx -d mcp.heptafox.com
   sudo systemctl reload nginx
   ```

Verify: `systemctl status mcp-sandbox` and `curl -i https://<domain>/mcp`.

</details>

## License

[Apache License 2.0](LICENSE). By contributing you agree your contributions are
licensed under Apache-2.0.
