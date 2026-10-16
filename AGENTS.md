# AGENTS.md

<!-- TEMPLATE-VERSION: 2026-09-19-v4 -->

This is the operating manual for any AI agent working in this repo. Read it before
starting.

The file has two parts:

- a **shared operating manual**, copied from the user's canonical AGENTS template;
- **project specifics**, filled separately for each repository.

Do not make repo-local edits to the shared operating manual unless the person
explicitly asks. Improvements to shared workflow should be made in the canonical
template first, then synced into projects while preserving the project-specific block.

<!-- BEGIN SHARED -->

## Shared guidance (v4)

1. Read the repository's project instructions and relevant README, DECISIONS, and specifications before changing code.

2. Verify files, symbols, interfaces, and repository facts before relying on them. Do not invent missing facts.

3. Follow recorded decisions and existing repository patterns unless the task explicitly changes them.

4. Make the smallest change that satisfies the task. Avoid unrelated refactors and unnecessary dependencies, abstractions, compatibility layers, or features.

5. Preserve existing behavior outside the requested scope.

6. Add deterministic regression tests for meaningful behavior changes and bug fixes. Test observable behavior, including relevant boundaries and failure paths.

7. Use existing real or sample fixtures where available. Do not alter authoritative fixtures merely to make tests pass.

8. Mock provider calls in tests. Never make live provider calls from tests.

9. Run the relevant test suite and other checks proportionate to the change's risk before claiming completion. Report anything not verified.

10. For load-bearing pure logic where ordinary tests may miss semantically wrong behavior—such as scoring, evaluators, parsers, validation, or privacy/data-release boundaries—use mutation testing only when an established mutation workflow already exists and the expected signal justifies the added cost. Do not introduce new mutation-testing infrastructure as part of an unrelated task.

11. Explain changes and results plainly. Report test, build, runtime, API, error, and stack-trace evidence as observed only when actually run or seen in the current session. Surface failures, contradictions, and uncertainty.

12. Verify the final patch against the task, including scope, unintended changes, and consistency with the reported evidence, before claiming completion.

<!-- END SHARED -->

<!-- BEGIN PROJECT -->

## What this project is

**hiring-radar** — answers one question: *what skills is the AI-engineering job market
asking for, and how does that differ by city?* Job descriptions come in from job-board
feeds, pasted links or text, or screenshots; a model maps each one to skill ids in a
versioned taxonomy; the dashboard aggregates by document frequency. Extraction quality
is measured against a labeled Golden set with a held-out split.

Rebuild of `job-skills-dashboard` (the June 2026 hackathon version). Why the rebuild and
what changed: DECISIONS.md, first entry.

Out of scope (deliberately): résumé matching or tailoring, email parsing, applicant
counts, anything that requires LinkedIn.

---

## How this project is built and laid out

### Running and testing

```bash
uv sync                      # Python deps
uv run pytest                # tests — model calls are always mocked

# Live eval (~20 model calls per repeat). Key comes from the environment or .env:
cp .env.example .env         # then put the key in .env — it is gitignored; never commit it
uv run python scripts/run_eval.py --repeats 1     # quick look
uv run python scripts/run_eval.py                 # dev split, 3 repeats → evals/results/<run_id>/

# Intake (writes ./data/hiring-radar.db; migrations apply automatically)
uv run python -m app poll                 # fetch feeds → ingest → extract new jobs
uv run python -m app poll --no-extract    # fetch + ingest only (no model calls)
uv run python -m app extract              # extract anything still pending
pbpaste | uv run python -m app add-text --company "Acme" --title "AI Engineer" --location Berlin --found-via linkedin
uv run python -m app stats
```

### Stack

- Python 3.13, `uv`. FastAPI (to come), Anthropic SDK called in-process (to come).
- SQLite, one file, schema managed by numbered migrations in `app/migrations/`.
- React frontend (to come), served by the same process.
- Hosting: Railway (to come). Runs locally until then.

### Where things live

- `app/db.py` — connection + migrations. `app/migrations/NNN_name.sql` — never edit a
  committed migration; add a new one.
- `app/taxonomy.py` — load/validate `taxonomy/skills.json`, resolve labels to skill ids.
- `app/extract.py` — stage 2: JD text → skill mentions (taxonomy ids), proposed new
  skills, and rejected items. Model client is injected.
- `app/evaluation.py` — scoring (micro P/R/F1, requirement accuracy, rank agreement)
  and the suite runner. `scripts/run_eval.py` — live CLI around it.
- `app/sources/` — one adapter per feed (`greenhouse`, `lever`, `ashby`, `arbeitnow`,
  `startup_jobs`): `parse(payload)` is pure and tested on `tests/fixtures/feeds/`;
  `fetch()` is the thin HTTP wrapper. `app/html_text.py` strips HTML.
- `app/dedup.py` — company/title keys and 3-word-shingle Jaccard similarity; `find_match`
  needs same company AND similarity ≥ 0.7. `app/geo.py` — location → tracked city.
- `app/ingest.py` — the still-listed / merge / repost / new decision and the title+city
  filters. `app/pipeline.py` — extract skills for jobs not yet at the current
  `extractor_version`. `app/poll.py` — run all feeds in `config/feeds.json`.
- `app/__main__.py` — the CLI (`python -m app ...`).
- `config/feeds.json` — which feeds to poll. Add a company's Greenhouse/Lever/Ashby board here.
- `taxonomy/skills.json` — the skill taxonomy. The source of truth for what a skill is.
  See `taxonomy/README.md` for how to edit it.
- `evals/goldens/` — labeled JDs: text + expected `{skill_id, requirement, raw_text}`.
  Each has a `split` (`dev` or `heldout`).
- `scripts/seed_from_legacy.py` — one-off that built the taxonomy and Goldens from the
  legacy repo. Kept for provenance.
- `tests/` — pytest.

Three layout rules:

- Imports flow one direction — lower-level files don't import from higher-level ones.
- Functions that mix input/output with logic get split into pure logic plus a thin I/O
  wrapper. The pure part is what gets tested.
- Every module gets a top docstring: what it does, what it explicitly does *not* do, and
  the invariants it holds.

### Project rules

- **Policy lives in the taxonomy, not the prompt.** If extraction gets a skill wrong,
  first ask whether the taxonomy is missing an entry or alias. Prompt rules stay general;
  never copy a specific JD's wording into the prompt.
- **Never tune on held-out Goldens.** Look at held-out results only at release points.
- **Unknown skills never reach the chart.** They go to `proposed_skill` for review.

### Pitfalls specific to this project

- `ReAct` (agent pattern) and `React` (framework) differ only by case. The taxonomy
  resolves them case-sensitively; keep it that way.
- `scripts/seed_from_legacy.py` output no longer matches the committed taxonomy/Goldens
  (they were hand-edited after seeding). Never run it against the real files.
- Feeds return everything; `app/ingest.py` filters by title regex and tracked city. A job
  in an untracked city is dropped, not stored — widen `app/geo.py` to add a city.
- `skill_mention` holds one extraction per job (the latest). Re-extraction replaces.

## Reporting a run

When you run `poll`, `extract` or `stats`, lead with one headline and stop there. Do not
paste per-feed lines, the stats block or raw stdout unless asked.

The headline is one or two sentences carrying, in this order:

- jobs and cities (`17 jobs, all Berlin`)
- mentions extracted, then proposed skills pending
- failures — always named, `0 failed` as explicitly as a non-zero count
- a count of judgment calls that need a human, if any

> Poll clean: 17 jobs (all Berlin), 106 mentions, 58 proposed, 0 failed. 2 judgment calls.

Then offer the rest: per-feed counts, document-frequency table, the judgment calls. The
numbers come from the command output and `data/hiring-radar.db`; query the DB directly for
anything `stats` does not print (mention counts, top skills, zero-skill jobs).

Three things break the headline rule, because a wrong summary of them costs a model call
or a bad chart:

- **Any FAILED line, or `extracted=n/m` where n < m** — report it in full, unsummarized,
  with the job ids.
- **A silently truncated or empty feed.** A feed that returns far fewer postings than its
  `max_pages` allows has usually stopped paginating; say so rather than reporting the
  smaller number as the result. See the startup.jobs docstring for how that looks.
- **A judgment call you did not take** — a leaking title filter, an unstable feed, a
  near-miss dedup. State it plainly as the person's call, separate from the numbers.

A clean run is one headline. Silence on failures is not cleanliness.

<!-- END PROJECT -->
