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

<!-- END PROJECT -->
