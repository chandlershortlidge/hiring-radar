# hiring-radar

**What skills is the AI-engineering job market actually asking for — and how does that
differ by city?**

Job ads are written to be read one at a time, so nobody can tell whether "RAG experience"
is in 5% of postings or 50%. hiring-radar reads them in bulk and answers that with a
number.

It pulls postings from company job boards, maps each one to a fixed list of skills with an
LLM, and charts how many *distinct jobs* mention each skill. One posting shouting
"Python, Python, Python" counts once.

Today, across 222 collected postings (all Berlin but one):

| skill | jobs asking for it |
|---|---|
| Python | 149 |
| LLMs | 117 |
| Agents | 80 |
| Evaluation | 77 |
| Cloud | 73 |
| Machine learning | 70 |

## Why trust the numbers

A chart built by an LLM is only as good as the extraction behind it, so extraction is
measured, not assumed:

- **24 job descriptions are hand-labeled** with the skills they truly ask for. Scoring
  against them gives **F1 0.925** (precision 0.881, recall 0.972) on the development set.
- **Four of those labeled ads are held out** and never looked at while tuning, so the
  score can't quietly become a score of how well the test was memorized.
- **Skills live in a versioned list**, not in the prompt. A skill the list doesn't know
  never reaches the chart — it goes to a review queue instead. 208 labels are queued now,
  and one earns a permanent entry once three separate jobs ask for it.
- **Every extracted skill carries the sentence it came from.** Click a job in the
  dashboard and you see the quote, so any number can be traced back to the words.

Each job also gets seniority, German-language requirement, and degree expectations — the
three things that decide whether a posting is worth reading at all.

## What this means for you

The market view is half the point. The other half is which of those skills you already
have. You describe yourself once — role, seniority, German, degree, the skills you'd
claim — and the dashboard reads the whole corpus back through that: how much of each
posting's ask you cover, and which in-demand skills you're missing.

Your profile stays in your browser's local storage. The server never sees it, so there's
no account and nothing to upload.

**Next up:** matching postings to a profile end to end — ranking jobs by how well you
cover them and naming the specific gap per job — turning "222 jobs in Berlin" into the
shortlist you could plausibly get, and the few skills standing between you and the rest.

## What it is not

No résumé *tailoring* — the tool tells you what the market wants and where you stand, it
does not rewrite your CV per posting. No email parsing, no applicant counts, nothing that
needs LinkedIn. Those were in the predecessor and were cut deliberately
([DECISIONS.md](DECISIONS.md), 2026-10-16).

**Status:** working locally — intake, extraction, evaluation, and dashboard all run. 44
job-board feeds are polled. Collection is Berlin-only until the held-out evaluation
passes; the city-comparison view is built and waiting on a second city. Runs 24/7 on a
GCP VM with a daily 07:00 poll; ops runbook in [deploy/README.md](deploy/README.md).

This is a rebuild of
[job-skills-dashboard](https://github.com/chandlershortlidge/job-skills-dashboard), a
one-day hackathon project whose extraction plateaued for structural reasons.
[DECISIONS.md](DECISIONS.md) records what went wrong and every choice made since.

---

# Technical details

## Quick start

```bash
uv sync
uv run pytest                 # model calls are always mocked

cp .env.example .env          # add your Anthropic API key (gitignored)

uv run python -m app poll     # fetch feeds → ingest → extract
uv run python -m app serve    # dashboard at http://127.0.0.1:8000
```

The dashboard needs a frontend build first (`cd web && npm install && npm run build`).
To see the UI without any model calls:

```bash
HIRING_RADAR_DB=/tmp/demo.db uv run python scripts/seed_demo.py
```

## How a job becomes a row in the chart

```
feeds / pasted link / pasted text / screenshot
        │
        ├─ screenshot only → vision call → verbatim transcript   (app/transcribe.py)
        │
        ▼
  ingest: new, still-listed, merge, or repost?                   (app/ingest.py)
        │   filtered by title regex and active city
        ▼
  extract: one tool call → skill ids + requirement + quote,      (app/extract.py)
        │   plus seniority / German / degree, each with a quote or none
        │   unknown labels → proposed_skill, never the chart
        ▼
  aggregate: document frequency per skill, per city              (app/queries.py)
```

Postings under 400 characters are treated as fragments and excluded from the chart
(DECISIONS, 2026-10-21).

## Stack

- Python 3.13, `uv`, FastAPI. Anthropic SDK called in-process.
- SQLite, single file, numbered migrations in `app/migrations/`.
- React 18 + Vite in `web/`, no chart library (CSS bars), served by the same process.

## Intake commands

```bash
uv run python -m app poll --no-extract          # fetch + ingest only, no model calls
uv run python -m app poll --only ashby:jupus    # one named feed
uv run python -m app extract                    # extract anything still pending
uv run python -m app check <url>                # in the DB? if not, why no feed had it
uv run python -m app discover-boards            # find boards we don't poll yet
uv run python -m app stats

pbpaste | uv run python -m app add-text --company "Acme" --title "AI Engineer" \
  --location Berlin --found-via linkedin
uv run python -m app add-screenshot shot.png --company "Acme" --title "AI Engineer" \
  --location Berlin
```

## Evaluation

```bash
uv run python scripts/run_eval.py --repeats 1   # quick look, ~20 model calls
uv run python scripts/run_eval.py               # dev split, 3 repeats
```

Results land in `evals/results/<run_id>/` with a `summary.md`. Metrics are
micro-averaged precision/recall/F1 plus requirement accuracy, Spearman rank correlation,
and top-10 overlap of skill frequencies. Held-out Goldens are read only at release
points.

## Layout

| path | what lives there |
|---|---|
| `app/sources/` | one adapter per feed (Greenhouse, Lever, Ashby, JOIN, Arbeitnow, …) |
| `app/ingest.py` | the new / still-listed / merge / repost decision, title + city filters |
| `app/extract.py` | JD text → skill mentions and per-job attributes |
| `app/evaluation.py` | scoring and the eval suite runner |
| `app/queries.py` | the read queries behind the dashboard |
| `app/api.py` | FastAPI routes plus the add-a-job paths |
| `taxonomy/skills.json` | the skill list — source of truth (v4, 200 entries) |
| `evals/goldens/` | labeled JDs with a `dev` / `heldout` split |
| `config/feeds.json` | which boards get polled |
| `web/src/profile.js` | the local profile and skill-overlap coverage (never sent to the server) |
| `web/src/` | the rest of the frontend |

Three layout rules: imports flow one direction, I/O is split from pure logic so the logic
can be tested, and every module opens with a docstring saying what it does *not* do.

Working in this repo (human or agent)? Read [AGENTS.md](AGENTS.md) first.

MIT licensed.
