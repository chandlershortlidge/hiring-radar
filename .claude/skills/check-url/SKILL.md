---
name: check-url
description: Audit feed coverage for one or many careers-page URLs — run `python -m app check` on the batch, add every missing board in one pass, poll only those boards, re-check, and report once with judgment calls grouped. Use when the person pastes job URLs and asks whether we have them, or invokes /check-url.
---

# /check-url <url> [<url> …]

`app/check.py` decides; this skill only chooses the next command. Never re-implement the
lookup or edit `app/ingest.py` / `app/geo.py` filters.

**Batch rule: never stop mid-batch to ask.** Run every URL through, do all the mechanical
work, and put every question in the one report at the end.

## 1. Check the whole batch

Write the URLs to a scratchpad file (one per line), then:

```bash
uv run python -m app check --file <urls.txt>                # add --found-via linkedin if the person said so
```

A JOIN company page (`join.com/companies/<slug>`, no job number) is not a posting: add
`{"type": "join", "enabled": true, "token": "<slug>", "company": "<Name>"}` and poll it.

The output has one `== <url>` block per URL. A single URL can be passed directly (quote it).
Every check is logged to `url_check`; only the first check of a URL counts toward coverage,
so the re-check in step 3 is safe.

## 2. Do the mechanical work, all at once

Sort the blocks by verdict:

| verdict | action |
|---|---|
| `found: job N …` | nothing |
| `board <type>:<token> is not in config/feeds.json — add {…}` | append that JSON to `feeds` in `config/feeds.json` (if the type+token is already there, set `"enabled": true` instead). Use the real company name if the page makes it obvious, else the token. Do this for every such board before polling. |
| `is polled and the posting passes both filters` | queue the board for the poll |
| `is polled; ingest would drop it: <reason>` | **judgment call** — collect it, don't act |
| `no longer lists job` | closed — collect it |
| `not a hosted ATS page` | if `--company` is not needed, collect it as "add?"; if it is, take the company from the page title when unambiguous, otherwise collect it as "needs company" |
| `board token unknown` (`?gh_jid=`) | collect it as "needs the boards.greenhouse.io link" |
| `error: …` | collect it with the message |

Then **one** poll limited to the boards just added or queued:

```bash
uv run python -m app poll --only ashby:jupus --only greenhouse:acme …
```

Never run a full `poll` for a check; that fetches every search feed (JSearch has a quota) and
is the slow part. Then re-run `check` only on the URLs whose boards were polled. A URL that
should now be found but still says `passes both filters` is a feed bug: include both outputs
unsummarized in the report.

## 3. Report once

**Keep it extremely short.** The person is working through many URLs. A clean result is one
line, e.g. `Already have it (job 31).` or `Added 2: AI Engineer (Berlin), ML Engineer (Berlin).`
No background or mechanics. Questions are one line each. For a big batch:

> 23 checked: 14 already in (feeds covered 12), 4 added via 3 new boards (poll: 4 new, 0 failed), 5 need you.

Then the items that need the person, **grouped by reason** so one answer covers many:

- `location 'Germany' maps to no tracked city` × 3: urls… → keep out, or widen `app/geo.py`?
- `title '…' fails the title filter` × 1: url → out of scope, or a leaking filter?
- not an ATS page × 2: urls… → add them (`check <url> --company X --add`)?
- closed × 1, errors × n, feed bugs (in full).

Any `FAILED` poll line or `extracted=n/m` with n<m is reported in full. When the person
answers, act on the whole group at once (e.g. `check --file <group.txt> --add`).

## 4. Commit

If `config/feeds.json` changed: one commit for the batch,
`feeds: add <type>:<token>, <type>:<token> (<Companies>)`. Do not commit the database.
