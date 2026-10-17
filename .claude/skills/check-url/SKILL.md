---
name: check-url
description: Audit feed coverage for one careers-page URL — run `python -m app check`, then act on its verdict (add the board to feeds.json and poll, add the posting, or stop on a judgment call). Use when the person pastes a job URL and asks whether we have it, or invokes /check-url.
---

# /check-url <url> [--company "Name"]

`app/check.py` decides; this skill only chooses the next command. Never re-implement the
lookup, edit `app/ingest.py` filters, or touch the database by hand.

## 1. Run the check

```bash
uv run python -m app check "<url>"            # quote the URL: ? and & break the shell
```

Add `--company "<Name>"` only if the person gave one or the output asks for it. Add
`--found-via linkedin` (or `indeed`, `referral`) when the person says where they found the
posting; the default is `company_site`.

Every `check` is logged to `url_check` and feeds the "coverage of checked URLs" line in
`stats`. Only the first check of a URL counts, so the re-checks below are safe to run.

## 2. Act on the verdict — exactly one branch

**`found: job N …`** → report it (step 3). Nothing to do.

**`not found: board <type>:<token> is not in config/feeds.json — add {…}`**
1. Open `config/feeds.json`. If an entry with the same `type` and `token` exists, do not
   add another; set it `"enabled": true` if it was false.
2. Otherwise append the printed JSON object to the `feeds` array. Keep the file valid JSON.
3. Run `uv run python -m app poll`.
4. Re-run the check from step 1. It must now say `found … via <type>`. If it does not,
   this is a feed or adapter bug: report the full `check` and `poll` output, unsummarized,
   with the board token and job id, and stop.

**`not found: board … is polled; ingest would drop it: <reason>`** → STOP. This is the
person's call: either the filter is leaking (fix `app/ingest.py` or `app/geo.py`, with a
test) or the rejection is correct and the job is out of scope. Report the exact reason
and ask which. Do not change the filter on your own.

**`not found: board … is polled and the posting passes both filters …`**
1. Run `uv run python -m app poll`.
2. Re-run the check. `found` → report it, noting it was posted since the last poll.
   Still `not found` → feed bug. Report both outputs unsummarized with the job id and stop.

**`not found: board … no longer lists job …`** → report as closed/re-posted. If the
person wants it anyway, `check --add` stores the page version as `source=url`.

**`not found: not a hosted ATS page …`**
- If the notes say `pass --company`, ask for the company (or take it from the page title
  if unambiguous) and re-run with `--company`.
- Then `uv run python -m app check "<url>" --company "<Name>" --add --found-via company_site`.
  Extraction runs automatically. Report the `add:` line and the extraction line.

**`board token unknown`** (a `?gh_jid=` embed URL) → ask for the `boards.greenhouse.io`
link for that job and re-run.

## 3. Report

One headline, per AGENTS.md "Reporting a run":

> found: job 42 "AI Engineer" via arbeitnow, ashby — board almedia added to feeds.json, poll clean (3 new, 0 failed).

Then offer detail. Any `FAILED` line, `extracted=n/m` with n<m, or a judgment call you
did not take is reported in full, not summarized.

## 4. Commit

If `config/feeds.json` changed: one commit, message `feeds: add <type>:<token> (<Company>)`.
Do not commit the database.
