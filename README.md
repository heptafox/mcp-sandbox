# mcp-sandbox

A public MCP server of test fixtures for developers/QA to test and write evals
against. Each tool returns deliberately distinctive output so a caller can prove
the response came **from the MCP server**, not from the model's training/context.

## Tools

| Tool | Params | Returns |
|------|--------|---------|
| `identity` | none | A fixed, intentionally-false canary string. Its uniqueness is the point — a model would never volunteer it, so seeing it confirms the MCP server answered. |

Transport: **streamable HTTP**, endpoint `/mcp` (no trailing slash — `/mcp/`
307-redirects to it, which some clients mishandle).

## Run locally

```bash
uv sync
uv run server.py        # serves http://127.0.0.1:8000/mcp
```

Test it with the MCP Inspector (point it at `http://127.0.0.1:8000/mcp`):

```bash
npx @modelcontextprotocol/inspector
```

List tools, call `identity`, confirm the exact string comes back.

## Deploy (AWS Lightsail, Ubuntu)

1. **Instance + DNS** — create an Ubuntu Lightsail instance, point your domain's
   A record at its static IP, and open ports **80 + 443** in the Lightsail
   firewall. Leave 8000 closed; the app listens on localhost only.
2. **App**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   git clone <repo> ~/mcp-sandbox && cd ~/mcp-sandbox && uv sync
   ```
3. **systemd** — copy `deploy/mcp-sandbox.service` to
   `/etc/systemd/system/`, then:
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

Result: `https://mcp.heptafox.com/mcp`.

## Verify

```bash
systemctl status mcp-sandbox
curl -i https://mcp.heptafox.com/mcp        # expect a response from the MCP endpoint
```

Then connect any MCP client to `https://mcp.heptafox.com/mcp` and call `identity`.

## Contributing

Contributions welcome. New tools are just `@mcp.tool` functions in `server.py` —
each should return a unique, improbable canary string (see the tool design
convention in `CLAUDE.md`). Open an issue or PR.

By contributing you agree your contributions are licensed under Apache-2.0.

## License

[Apache License 2.0](LICENSE).
