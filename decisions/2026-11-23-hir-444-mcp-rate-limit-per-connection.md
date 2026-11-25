## 2026-11-23 — The MCP rate limit counts per connection, with a higher ceiling per address (HIR-444)

**What was decided.** Chandler, 23 Nov, in the ticket (as a settled recommendation): the
MCP server's rate limit counts **each connection on its own**, not each IP address. This
replaces the "it counts per IP address" and "the numbers" points of
`2026-11-17-hir-338-mcp-open-read-only-rate-limit.md`; the rest of that record (open,
read-only, the limit lives in the app, 50 jobs per call, no DNS-rebinding check) stands.

**Why.** A web assistant (claude.ai, ChatGPT, Gemini) connects from its maker's servers,
not from the person's device. So everyone using the radar through one assistant arrived
from the same few addresses and shared one allowance of about 60 requests a minute: one
busy person, or a few morning digests at 7:00, throttled all the others.

**What that means in practice.**

- **A connection** is what the MCP protocol calls a session: the server hands the client
  an id (the `Mcp-Session-Id` header) in its first answer, and the client sends it back
  with every later request. The MCP library runs this server without sessions, so the
  rate limit hands out the id itself. It is only a counter's name: nothing about the
  conversation is stored with it.
- **Per connection: the old numbers.** Bursts of up to **30 requests**, refilled at **1 a
  second** (`BURST`, `RATE` in `app/mcp_server.py`).
- **Per address: a ceiling, as abuse protection.** Bursts of up to **300 requests**,
  refilled at **5 a second**, so about 300 a minute sustained: five times the old limit,
  room for about fifteen people's digests in the same minute from one of an assistant
  maker's addresses (`IP_BURST`, `IP_RATE`). This, not the per-connection number, is now
  what bounds one script.
- **New connections per address:** bursts of up to **60**, refilled at **1 a second**, so
  about 60 a minute (`NEW_BURST`, `NEW_RATE`). Without it, opening a fresh connection for
  every request would step around the per-connection limit. A request with no id, or
  with an id the server does not know, counts as a new connection.
- **An id the server does not know is taken on, not refused.** The table of connections
  is in memory, so a deploy forgets it. Refusing an unknown id would break every open
  connection at each deploy and rely on each assistant reconnecting correctly; taking it
  on costs one "new connection" from that address and nothing else.
- **The newest MCP protocol version (2026-07-28) has no connections at all**: no
  handshake, no id, every request stands alone. Nothing in such a request tells two
  people on one assistant apart, so those requests are held to the per-address ceiling
  only. Telling them apart needs sign-in (HIR-218). This is not a corner case: the MCP
  library's own client (2.3) speaks this version by default, so an assistant that has
  moved to it gains the higher ceiling from this change and nothing more.
- **Order of the checks:** the connection's own allowance first, then the address's. A
  connection that hammers is refused on its own allowance and so cannot use up the
  ceiling of the address it shares with other people.
- **The server never opens a listening stream.** A client that holds an id may ask for
  one (a `GET`); the server answers "405: not offered", which the protocol allows, and
  does not count it against any allowance. It has nothing to push: every answer goes out
  with the request that asked. Before this change such a request was held open for
  nothing.

**Not checked on the live site.** Which protocol version claude.ai, ChatGPT and Gemini
speak, and whether those on an older one send the id back on every call (the protocol
says a client must), was not observed: the server never issued one before this change.
Checked here: the library's client on the older protocol does send it back, and works
with the listening stream refused. A client that ignores the id is held to the
new-connections number, 60 a minute per address, which is what it had before.

**Undo or retune:** the six constants above in `app/mcp_server.py`. Setting `NEW_BURST`
and `IP_BURST` to 30 and both rates to 1 gives back a limit of 60 a minute per address.
