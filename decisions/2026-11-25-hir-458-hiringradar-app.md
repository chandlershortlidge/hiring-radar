## 2026-11-25 — the site lives at hiringradar.app; the old sslip.io address forwards until 31 Jan 2027 (HIR-458)

Chandler bought `hiringradar.app` (Cloudflare Registrar, 24 Nov). DNS: `A @` → the VM's
static IP and `CNAME www` → `hiringradar.app`, both DNS only (no Cloudflare proxy), so Caddy
gets its own Let's Encrypt certificate. `.app` is HSTS-preloaded: HTTPS only.

- **`https://hiringradar.app`** serves the dashboard (password) and the open MCP at `/mcp`.
- **`www.hiringradar.app`** forwards (301) to it, path kept.
- **`34-159-223-190.sslip.io`** forwards (301) to it, path kept, **except `/mcp`, which it
  still serves**. A client following a 301 resends a POST as a GET, which `/mcp` refuses
  (HIR-444), so a redirect would cut off any Claude already connected at the old address.
  The ticket asked for 301 "so the MCP connection doesn't break"; the reason wins over the
  letter.
- **The old address is removed on 31 Jan 2027** (its own ticket). Until then it is the one
  place `sslip.io` appears in the repo: its block in `deploy/Caddyfile`.
- **A deploy still does not apply the Caddyfile** (2026-11-01, HIR-74). The switch is two
  hand steps around the merge (deploy/README.md, "The move to hiringradar.app"), so the
  uptime check and the robot visitor, which read one address, are green before, across and
  after the merge. Making the deploy apply the Caddyfile is a separate question.
