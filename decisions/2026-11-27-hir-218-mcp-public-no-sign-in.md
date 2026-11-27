## 2026-11-27 — The public Claude connection has no sign-in; going over the limit is refused with a message a client can show (HIR-218)

**What was decided.** Chandler, 24 Nov, in the ticket: **open to anyone, no sign-in.**
"What I want is for people to use it." The limit per connection with a ceiling per
address (`2026-11-23-hir-444-mcp-rate-limit-per-connection.md`) is the protection. This
replaces "Sign-in and per-user caps come later (HIR-218)" in
`2026-11-17-hir-338-mcp-open-read-only-rate-limit.md`: there is no sign-in planned, and
the per-connection limit is the per-user cap. A tool that writes or calls a model still
needs sign-in first (AGENTS.md "The MCP server"); none exists.

**The refusal (decided in this PR).** A request over an allowance gets:

- HTTP **429** with `Retry-After` in whole seconds, as before, for clients that back off
  on their own;
- a **JSON-RPC error** body (`application/json`, code `-32000`, the request's id when the
  body has one, else `null`) whose message says which allowance ran out, its numbers, and
  how long to wait. The MCP library's client hands a JSON-RPC error body at a non-2xx
  status to the caller as that error, so the model reads the message and can tell the
  person; a plain-text body reaches it as "Server returned an error response".
- `data` carries `retry_after` (seconds) and `limit` (`connection`, `new_connections` or
  `address`), for a client that wants to act on it without reading the sentence.

**Why one message per allowance.** "Slow down" alone leaves a person whose assistant
shares an address with others thinking they did something wrong. The address ceiling's
message says the limit is shared by everyone arriving from that network address.

**Undo:** `_refusal` in `app/mcp_server.py`; returning the old plain-text body there gives
back the previous behaviour. The numbers are unchanged.
