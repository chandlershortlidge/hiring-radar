## 2026-11-27 — How an agent finds the MCP server from the site, and its Registry name (HIR-480)

Chandler said yes on 26 Nov to letting agents discover the MCP server at
`https://hiringradar.app/mcp` from the site itself. The choices the ticket left open:

- **Addresses.** There is no final MCP standard for discovery yet. The current draft (the
  MCP "Server Cards" extension, tracking SEP-2127) has an agent read a site-wide AI Catalog
  at `/.well-known/ai-catalog.json`, which points to a Server Card; the card's reserved
  address is the MCP URL plus `/server-card`, so ours is `/mcp/server-card`. Earlier drafts
  proposed `/.well-known/mcp.json` and `/.well-known/mcp/server-card.json`, which some
  checkers and clients still try, so the same card is served there too. `/llms.txt` gives
  the same facts in plain words. Undo: drop the paths from `app/discovery.py` and the
  Caddyfile.
- **Tools in the card.** The draft leaves tools out of a card (a client lists them once
  connected). The ticket asks for them, so they sit in the card's `_meta` under our own
  namespace, `app.hiringradar/discovery`, the extension point the draft gives. They are
  built from the server's tool list on every request, so they cannot drift; nothing lists
  them by hand.
- **Name.** `app.hiringradar/hiring-radar`, the reverse-DNS form the MCP Registry requires
  for a name proved by the domain. It is proved with a DNS TXT record on hiringradar.app
  rather than a GitHub login, so the listing names the same domain the server lives on.
- **Version.** The server now reports version `1.0.0` when a client connects (before, it
  reported none). The card and the Registry entry state the same number, as the draft asks;
  the Registry refuses to republish a version it already has, so a change to the tools
  raises it.
- **Password.** The six discovery addresses answer without the dashboard password, before
  and after launch, like `/mcp`. Every answer from the site, the password prompt included,
  carries a `Link` header to the card and to `llms.txt`, so an agent that only gets the
  prompt before launch can still find the server.
- **Publishing to the Registry waits for launch (HIR-82).** The Registry lists only servers
  anyone can reach, and needs a login only Chandler has. The commands are in
  deploy/README.md, "List the MCP server in the MCP Registry".
