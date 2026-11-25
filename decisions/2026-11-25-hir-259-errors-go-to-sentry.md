## 2026-11-25 — errors from visitors' browsers and from the server go to Sentry, with no visitor details (HIR-259)

Chandler, 23–24 Nov: use **Sentry on its free plan** for browser and server errors. He opened
the account himself (EU region, `ingest.de.sentry.io`): error monitoring only, with tracing,
logs, metrics, profiling and session replay switched off in the projects. A new error group
reaches him as Sentry's own email alert; nothing else notifies.

This is the first time the public site sends anything about a visit to an outside company.
The limits that came with the yes, and how each is kept:

- **Off until a key is present.** Server: `SENTRY_DSN` in the VM's environment file
  (`/etc/hiring-radar.env`), never in the repo. Browser: `VITE_SENTRY_DSN`, read from the
  GitHub Actions repository variable of the same name when the deploy builds the frontend.
  The browser key is public by nature (it ships in the page), so it is a variable, not a
  secret. No key → the SDK is never started and nothing is sent.
- **No personal data.** Both SDKs run with every automatic collection category that can
  hold a visitor detail turned off: user info (so no IP address is attached or inferred),
  cookies, request headers (Caddy's `X-Forwarded-For` holds the visitor's address), request
  bodies (a flag note is visitor-typed text), URL query strings (search text), stack-frame
  local variables (they can hold the same), and the MCP tool inputs and outputs (a
  visitor's Claude can send their skills). A last filter before sending drops any `user`
  block and any query string that got through. The page path stays: it is what makes an
  error findable, and no path on the site carries a visitor detail.
- **No cookies.** The browser SDK sets none; cookie collection is off on both sides.
- **No session replay, no tracing, no visitor counts.** Replay and tracing are not loaded;
  the browser SDK's session tracking (one ping per page load, which is a visitor count) is
  removed, so out-of-scope visitor statistics never start by accident. Breadcrumbs from the
  console and from clicks and typing are dropped; page changes and our own API calls stay.
- **One bug is one entry.** Grouping is Sentry's own (by stack trace). Errors a page's
  safety box catches (the "couldn't load" notes) are reported too, or a broken panel would
  never reach Sentry.
- **No test route on the live site.** Sentry's guide suggests a `/sentry-debug` route; it is
  not shipped. The check is a one-off thrown error from a local build.

Undo: remove the two keys (the server and the next deploy then send nothing), or revert the
pull request.
