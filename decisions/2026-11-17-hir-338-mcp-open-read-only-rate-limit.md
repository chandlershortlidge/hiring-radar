## 2026-11-17 — The MCP server is open, read-only and rate limited per visitor (HIR-338)

> **Partly replaced, 23 Nov (HIR-444):** the limit now counts per connection, with new
> numbers: `2026-11-23-hir-444-mcp-rate-limit-per-connection.md`. The rest stands.

**What was decided.** Chandler, 17 Nov, in the ticket: the MCP server (anyone's Claude
connects to it at `/mcp` on the live site) is **open and read-only** in its first version.
No sign-in; a rate limit per visitor. The data is public job-market data with nothing
personal in it. Sign-in and per-user caps come later (HIR-218).

**What that means in practice.**

- **Open.** `/mcp` is outside the dashboard's password: the web server (Caddy) sends it
  straight to the app and asks every other address for the password, as before.
  `deploy/Caddyfile` holds that split. No deploy changes the web server's config (the VM's
  copy holds the real password), so it is applied by hand once, after the merge: the steps
  are in `deploy/README.md`, "Caddy: open `/mcp`".
- **Read-only.** Every tool reads the dashboard's own queries and nothing else: no tool
  writes, calls a model or runs a query of its own (AGENTS.md "The MCP server").
- **The rate limit lives in the app**, not the web server: the stock Caddy on the VM has no
  rate-limit module, and building a custom Caddy is more moving parts than a small counter.
  It counts per IP address, which uvicorn reads from the header Caddy adds.
- **The numbers:** bursts of up to **30 requests**, refilled at **1 a second**, so about
  **60 a minute** sustained per visitor. One tool call is one or two requests, so a person
  asking their Claude questions never meets it; a script hammering the server gets "429:
  too many requests" with how long to wait. Undo or retune: `BURST` and `RATE` in
  `app/mcp_server.py`.
- **At most 50 jobs per call**, paged with an offset, so one answer stays small enough for
  a model to read.
- **No DNS-rebinding check.** The MCP library turns one on for servers on a person's own
  machine; this one is public, holds no credentials and only reads public data, and the
  check would refuse the live site's own address.
