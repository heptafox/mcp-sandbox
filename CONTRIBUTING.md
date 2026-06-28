# Contributing to mcp-sandbox

Thanks for your interest! mcp-sandbox aims to be the **go-to sandbox MCP server**
for people learning the Model Context Protocol, building agents, and writing
GenAI evaluations. Contributions of all sizes are welcome — **beginners
especially.** A new tool, a fixed typo, a client example, or a clearer sentence
all help.

## Ways to contribute

- 🧰 New beginner-friendly tools (error simulation, streaming, structured output…)
- 🔑 OAuth / additional authentication examples
- 🔌 MCP client integration examples (Cursor, Google ADK, LangChain, CrewAI, OpenAI Agents SDK)
- 🧪 Evaluation scenarios and tutorials
- 📖 Documentation improvements and sample projects
- 🐛 Bug fixes

Not sure where to start? **Open an issue or a discussion** — we're happy to help
you find a first contribution.

## Run locally

```bash
uv sync                 # install deps into .venv
uv run server.py        # guide at http://127.0.0.1:8000/ , MCP at /mcp
```

Smoke-test a tool in-memory (no network) with the FastMCP `Client`:

```bash
uv run python -c "
import asyncio; from fastmcp import Client; from server import mcp
async def m():
    async with Client(mcp) as c:
        print((await c.call_tool('identity', {})).content[0].text)
asyncio.run(m())"
```

Or inspect interactively: `npx @modelcontextprotocol/inspector` pointed at
`http://127.0.0.1:8000/mcp`.

## Proposing a new tool

Tools are plain `@mcp.tool` functions in `server.py` — no new files needed. The
one rule that makes this project work:

> **Every tool returns a unique, improbable canary token** — something a model
> would never volunteer on its own (e.g. `MCP-SANDBOX canary 7Q9X-…`). That token
> is how callers prove the response came from the server, not the model.

Guidelines:

- **Keep output deterministic.** The same call returns the same token, every time.
- **Make the canary unique.** Use a fresh, distinctive marker per tool so results
  are unambiguous.
- **Avoid false or sensitive factual claims as canaries.** Models refuse to relay
  them, which defeats interactive testing. Use nonsense markers, not fake facts.
- **Write a clear docstring** — it becomes the tool description the model sees.
  Tell the caller to show the returned text verbatim.

Open an issue first for anything non-trivial so we can align on the design.

## Coding style

- Match the existing style in `server.py` — small, readable functions.
- No new dependencies unless genuinely needed (`uv add <pkg>`).
- Comment only what isn't obvious from the code.

## Documentation guidelines

If your change is user-facing, update the docs in the same PR:

- **`README.md`** — the canonical reference (tools table, examples, quick start).
- **`web/index.html`** — the landing page served at `/`; add a tool card and any
  examples. The page fills in the live URL via JavaScript (`location.origin`), so
  **don't hardcode URLs** — use the existing `.url` placeholder pattern.

Keep docs concise and scannable. Prefer cards and short examples over long prose.

## Pull request process

1. **Fork** the repo and create a branch (`feat/my-tool`, `docs/fix-typo`).
2. **Make your change** and test it locally (see above).
3. **Update docs** if the change is user-facing.
4. **Open a PR** with a clear description of what and why. Link any related issue.
5. A maintainer will review. Small, focused PRs get merged fastest.

## License

By contributing, you agree your contributions are licensed under the
[Apache License 2.0](LICENSE).
