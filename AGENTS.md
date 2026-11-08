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

## Starting a session

**This is the first action of every session that will commit, before reading any code,
docs or diff.** A session that only reads or answers a question skips it and stays where
it is. If such a session turns into a change — and they do — stop and run this *before the
first edit*, not before the first commit: the switch is free while there is nothing to
carry.

1. **Which ticket is this session for?** If the prompt does not name one, ask — before
   anything else. Do not infer it from the branch the terminal is on, from uncommitted
   changes, or from what looks half-finished.

2. **Claim it in Linear before anything else** (HIR-124). Set the issue to In Progress
   as the session's first write — before the brief, before the worktree, before any edit.
   Several orchestrators now run at once and each sees only its own workers, so the issue
   status is the one claim both can read: an issue read but not claimed is an issue a
   second session will start a second worker on. An issue already In Progress with no
   status note saying where a run stopped belongs to a session you cannot see — say so and
   stop.

3. **Get onto that ticket's branch — in its own worktree.** A folder has one current
   branch and one `TICKET`, so two sessions in one folder will commit onto each other's
   branches however careful each one is (HIR-94: an HIR-72 commit landed on the HIR-92
   branch this way). `git worktree add ../<repo>-hir-NN -b <branch> origin/main`, then
   work there. Never inherit whatever branch the terminal happens
   to be on. A terminal left on another ticket's branch, or on `main`, is the ordinary
   case between sessions, not a hint about what to work on.

   ```bash
   # work not started yet
   git switch main && git pull
   git switch -c chandlershortlidge/<ticket>-<slug>      # e.g. .../hir-88-git-hygiene

   # work already has a branch
   git switch chandlershortlidge/<ticket>-<slug>
   ```

   If the tree has uncommitted changes, `git switch main` either refuses or carries them
   onto the new branch. Stop and ask whose they are; do not stash, commit or discard them
   to get moving.

4. **Write the id to `TICKET`.**

   ```bash
   echo HIR-NN > TICKET
   ```

   `TICKET` is gitignored and does not travel with a switch or a merge, so a stale id left
   by the previous session is normal — rewrite it every time rather than trusting it.

Once per clone, so `.githooks/pre-commit` actually runs:

```bash
git config core.hooksPath .githooks
```

Then, for the rest of the session:

- **One ticket per branch, per folder, per commit.** `TICKET` holds one id; the branch
  name must contain it (`pre-commit`) and a commit subject that names a ticket must name
  the same one (`commit-msg`).
- **If the branch and the ticket disagree, stop and ask.** Do not rewrite `TICKET` to
  match the branch, and do not switch branches to make it fit — which of the two is wrong
  is the person's call. This applies once step 4 has been done this session. If you
  skipped step 4 and the ticket was named in the prompt, do step 4 now; that isn't
  rewriting `TICKET` to match the branch.
- **Never commit to main.** The hook refuses it; do not reach for `--no-verify`.
- **A branch open more than two days gets split or merged**, not carried. If the work has
  grown past its ticket, say so and propose the split.

---

## What this project is

**hiring-radar** — answers one question: *what skills is the AI-engineering job market
asking for, and how does that differ by city?* Job descriptions come in from job-board
feeds, pasted links or text, or screenshots; a model maps each one to skill ids in a
versioned taxonomy; the dashboard aggregates by document frequency. Extraction quality
is measured against a labeled Golden set with a held-out split.

Rebuild of `job-skills-dashboard` (the June 2026 hackathon version). Why the rebuild and
what changed: DECISIONS.md, first entry.

Out of scope (deliberately): résumé matching or tailoring, email parsing, applicant
counts, anything that requires LinkedIn. One narrow exception, since 2026-11-01 (HIR-14):
a CV may be read **in the browser** to pre-select the profile's skill chips, which the
person then edits. The CV never reaches the server or a provider. Tailoring, stored
résumés and scoring a person against a posting stay out.

---

## How this project is built and laid out

### Running and testing

```bash
uv sync                      # Python deps
uv run pytest                # tests — model calls are always mocked

# Live eval (~20 model calls per repeat). Key comes from the environment or .env:
cp .env.example .env         # then put the key in .env — it is gitignored; never commit it
uv run python scripts/run_eval.py --repeats 1     # a routine change → evals/results/<run_id>/
uv run python scripts/run_eval.py                 # 3 repeats: a release, or 1 repeat tripped the gate

# Required before a PR that touches app/extract.py or taxonomy/skills.json can merge
# (AGENTS.md "The eval gate"): run the dev eval above, then
uv run python scripts/eval_table.py <run_id>      # score table for the PR body, vs. the last committed run
uv run python scripts/eval_table.py --version-check   # ...unless the baseline already measured this extractor

# Intake (writes ./data/hiring-radar.db; migrations apply automatically)
uv run python -m app poll                 # fetch feeds → ingest → extract new jobs
uv run python -m app poll --no-extract    # fetch + ingest only (no model calls)
uv run python -m app extract              # extract anything still pending
pbpaste | uv run python -m app add-text --company "Acme" --title "AI Engineer" --location Berlin --found-via linkedin
uv run python -m app add-screenshot shot.png --company "Acme" --title "AI Engineer" --location Berlin
uv run python -m app check https://boards.greenhouse.io/acme/jobs/4012345   # in the DB? if not, why no feed stored it
uv run python -m app check https://acme.com/careers/ai-engineer --company "Acme" --add   # ...and store it
uv run python -m app check --file urls.txt          # a batch, one URL per line (- = stdin)
uv run python -m app poll --only ashby:jupus        # poll just the named feed(s), e.g. after adding a board
uv run python -m app discover-boards                # find boards we don't poll (Brave search, ~10 searches)
uv run python -m app discover-boards --add lever:acme   # or --reject lever:acme --reason "no Berlin AI roles"
uv run python -m app stats

# Dashboard
cd web && npm install && npm run build && cd ..   # once, and after frontend changes → web/dist
cd web && npm test && cd ..                       # the frontend's own tests (vitest), e.g. the CV matcher
uv run python -m app serve                        # http://127.0.0.1:8000 (API + built frontend)
cd web && npm run dev                             # frontend with hot reload on :5173, proxies /api to :8000
HIRING_RADAR_DB=/tmp/demo.db uv run python scripts/seed_demo.py   # fake data to look at the UI without model calls
cd web && DEMO_URL=http://127.0.0.1:8000 npm run demo   # screenshots + recording → web/demo-out/ (server must be running)
# On a PR, .github/workflows/pr-demo.yml runs that walkthrough on main and on the branch and posts the before/after as a comment

# One-off: import the legacy corpus (needs the screenshot folder from the old Supabase bucket)
uv run python scripts/import_legacy.py --screenshots ~/Downloads/screenshots --city Berlin --dry-run
```

### Stack

- Python 3.13, `uv`. FastAPI; Anthropic SDK called in-process from the add endpoints.
- SQLite, one file, schema managed by numbered migrations in `app/migrations/`.
- React 18 + Vite frontend in `web/`, no chart library (CSS bars), served from `web/dist`
  by the same process.
- Hosting: one GCP Compute Engine e2-micro in europe-west3 (HIR-29): systemd service +
  07:00 poll timer, Caddy for HTTPS + basic auth, nightly SQLite backup to a GCS bucket
  with a 30-day lifecycle, deploy on merge to `main` via GitHub Actions. The deploy job
  authenticates by workload identity federation (no stored key; only `main` of this repo)
  and reaches the VM through IAP + OS Login. How to SSH in, operate it, rebuild it and
  restore a backup: [deploy/README.md](deploy/README.md); the shape and the reasons are in
  DECISIONS.md (2026-10-21 and 2026-11-01, HIR-74).

### Where things live

- `app/db.py` — connection + migrations. `app/migrations/NNN_name.sql` — never edit a
  committed migration; add a new one.
- `app/taxonomy.py` — load/validate `taxonomy/skills.json`, resolve labels to skill ids.
- `app/transcribe.py` — stage 1: screenshot bytes → verbatim transcript (vision call).
  Only screenshots go through it; feeds and pastes are already text.
- `app/extract.py` — stage 2: JD text → skill mentions (taxonomy ids), proposed new
  skills, rejected items, and four per-job attributes, each with a quoted signal or none:
  seniority (junior/mid/senior), German (required/nice_to_have), degree (level,
  requirement, or-equivalent-experience), production experience
  (required/nice_to_have — prior shipping, never a responsibility). One tool call. Model client is injected.
- `app/evaluation.py` — scoring (micro P/R/F1, requirement accuracy, rank agreement)
  and the suite runner. `scripts/run_eval.py` — live CLI around it.
- `app/sources/` — one adapter per feed (`greenhouse`, `lever`, `ashby`, `join`, `arbeitnow`,
  `arbeitsagentur`, `jsearch`, `startup_jobs`): `parse(payload)` is pure and tested on `tests/fixtures/feeds/`;
  `fetch()` is the thin HTTP wrapper. `app/html_text.py` strips HTML.
- `app/dedup.py` — company/title keys and 3-word-shingle text measures; `find_match` needs
  the same company AND `is_same_posting`: an exact `title_key` match (HIR-108, no text test
  at all — a feed can store a paraphrase of the same posting with near-zero text overlap),
  **or** Jaccard ≥ 0.7, **or** the containment path added by HIR-113 (the shorter text ≥ 0.9
  contained in the longer, ≥ 60 shingles long, and the shorter title's words all in the
  longer title). A title *without* the same company never carries a match alone, and a
  title that is merely similar (not identical) still needs one of the text tests. The
  real postings the thresholds rest on are `tests/fixtures/dedup/real_cases.json`.
  `app/geo.py` — location → tracked city or EU-remote.
- `app/ingest.py` — the still-listed / merge / repost / new decision and the title+city
  filters. `app/pipeline.py` — extract skills for jobs not yet at the current
  `extractor_version`. `app/poll.py` — run all feeds in `config/feeds.json`.
- `app/discover.py` + `app/sources/brave.py` — `discover-boards`: Brave `site:` searches
  (config/discover.json: domains × queries) → boards we don't poll → each fetched live and
  judged by ingest's filters → report. `--add`/`--reject` are the only writes (feeds.json,
  `config/boards_rejected.json`). Needs `BRAVE_API_KEY`.
  `--launch <city>` is the one path that writes without being asked (HIR-132): it counts
  roles in that city alone, adds every employer board with 5+ of them, skips agencies and
  aggregators, leaves 1–4 unrecorded, and stops the whole launch — adding nothing — above
  €10 of one-time model reading or 5,000 postings added to the daily download.
- `app/check.py` — `check`: a careers-page URL → found / not found, and on a miss why no
  feed could have stored it (board not polled, filter would drop it, not an ATS page).
  Writes only its own log (`url_check`, the first check per URL drives the coverage line
  in `stats`); `--add` in the CLI hands the resolved posting to `ingest_one`.
- `app/skill_tree.py` — the radial skill tree (`/api/skills/tree`): mentioned and required
  counts per skill over the filtered job set, a parent for each (the least prevalent skill
  its own jobs still nearly always ask for), which branch each reads as part of, and every
  coordinate of the layout down to where each label goes. Pure `build_tree` plus a thin
  `fetch_jobs`; display names are passed *in*, because a label's width decides the layout.
  Ignores the `requirement` and skill filters on purpose — see the two DECISIONS entries
  of 2026-10-30, "reads the conditional asymmetry" and "made readable".
- `app/queries.py` — read queries behind the dashboard: filters (city, seniority, German,
  degree, production, requirement, window), skill document frequency with per-city counts,
  related-skills co-occurrence with lift (`related_skills`, feeds `/api/skills/related`),
  job list/detail, proposed-skill grouping and resolution. The open-job rule lives here.
  Two job-list searches that never blur: `query` over company and title, `text` over the
  posting itself (`fts_query` sanitizes it; the FTS5 index is migration 014's `job_fts`,
  kept in step with `job.description_text` by triggers, so writers need not know of it).
- `app/api.py` — FastAPI routes over `queries` plus the add-a-job paths (url / text /
  screenshot), which run intake + extraction for the one job added. Validates every filter
  value (422), one SQLite connection per request, model client created lazily.
- `web/src/` — `App.jsx` (filters, header, stats, controls, and the one route: `/jobs/{id}`
  read from the address bar), `JobPage.jsx` (a job's own page: detail + the stored posting
  text), `SkillChart.jsx`,
  `CompareChart.jsx`, `SkillTree.jsx` (draws `/api/skills/tree`; does no layout arithmetic
  of its own, and the card is collapsed by default so it is not fetched until opened),
  `RelatedSkills.jsx` (what the jobs requiring the selected skill also
  require; renders only with a skill selected and computes nothing itself),
  `JobList.jsx` (rows + expanded detail with quotes), the three drawers
  (`AddJobDrawer`, `ReviewDrawer`, `ProfileDrawer`), `profile.js` (localStorage profile +
  set-overlap coverage; the server never sees it), `api.js`, `format.js`.
- `web/src/cvSkills.js` + `cvText.js` — "Fill from your CV" in `ProfileDrawer` (HIR-14).
  `cvSkills.js` is the pure matcher (CV text → taxonomy ids: literal, word-boundary,
  case-insensitive except ReAct/React, phrases under 3 characters never match) and is what
  the tests cover; `cvText.js` is the thin reader (PDF via pdf.js, .docx via mammoth, plain
  text). **The CV is read in the browser and never leaves it** — no endpoint, no model call,
  nothing stored (DECISIONS 2026-11-01). Keep it that way: the drawer promises it.
- `app/__main__.py` — the CLI (`python -m app ...`, including `serve`).
- `.claude/skills/check-url/` — `/check-url <url>`: runs `check` and acts on the verdict
  (adds the board to `config/feeds.json` and polls; stops on filter judgment calls).
- `config/feeds.json` — which feeds to poll. Add a company's Greenhouse/Lever/Ashby/JOIN board here.
- `taxonomy/skills.json` — the skill taxonomy. The source of truth for what a skill is.
  See `taxonomy/README.md` for how to edit it.
- `evals/goldens/` — labeled JDs: text + expected `{skill_id, requirement, raw_text}`.
  Each has a `split` (`dev` or `heldout`).
- `legacy/` + `scripts/import_legacy.py` — the old Supabase export (48 jobs, their skills)
  and the one-off importer. See its docstring for the three import paths.
- `scripts/fix_jsearch_ids.py` — one-off: collapse jsearch rows stored under unstable ids
  (before 2026-10-18) and undo the repost counts they caused. `--dry-run` first.
- `scripts/remove_headline_jobs.py` — one-off: delete jobs stored under an aggregator's
  search-result headline before HIR-96 stopped the feed writing them. Selects with
  `jsearch.is_headline`, deletes only jobs with a jsearch source row, cascades their skill
  mentions. `--dry-run` first. See DECISIONS 2026-11-02 (HIR-104).
- `scripts/eval_table.py` — the eval gate's table: finds the newest *committed* dev run,
  compares every aggregate metric with it, and exits non-zero on either stop line — a
  per-Golden attribute score that lost more than 2 Goldens, or a skill score down more than
  0.02 (HIR-164). Flips come from rescoring both runs' `predictions.jsonl` through
  `app.evaluation.attribute_hits`, the function the runs scored with; when rescoring no
  longer reproduces what a run recorded, the Goldens were relabelled since and it says so
  instead of reporting a count. `--version-check` answers whether the baseline already
  measured this extractor (the gate's one exemption). Calls no model and writes nothing.
- `scripts/new_goldens.py` — draft unlabeled held-out Goldens from DB jobs
  (`--german N` or `--ids ...`); run_eval skips files with `"draft": true`.
- `scripts/agent_label.py` — held-out Goldens via two blind labeler agents: pick → label A
  and B → auto-check → merge → review queue (`label`), then your decisions → final Goldens
  with provenance (`apply`). Refuses to label with the extractor's model. Never runs the
  held-out eval. See DECISIONS 2026-10-27 and `evals/LABELER_PROMPT.md`. `--city <city>`
  narrows the pool to one city, which is what a city launch samples.
- `scripts/launch_check.py` — the quality check a city launch reports (HIR-132): scores the
  labeller panel's *agreed* labels against what the extractor actually stored for the same
  postings, with `app.evaluation`'s scorer, and against a second run on Berlin
  (`--baseline-run`) as the bar. Read-only; calls no model. The labels it reads are
  model-written and unreviewed, so they are **not** Goldens — they wait in the run's
  `review_queue.md` for the ordinary spot-check. A skill both labellers found but one
  flagged unsure is **set aside** while it waits there: out of the yardstick *and* out of
  the extractor's side, so it is neither credited nor penalised, and the report prints how
  many were set aside and how long the queue is next to the score (DECISIONS 2026-11-04,
  HIR-159). A verdict a model wrote does not lift that: only a person's does.
- `scripts/seed_from_legacy.py` — one-off that built the taxonomy and Goldens from the
  legacy repo. Kept for provenance.
- `deploy/` — everything about the VM: the runbook (`README.md`), `provision.sh` (rebuilds
  the VM's software side, re-runnable), the five systemd units and the `Caddyfile` as
  verbatim copies of what is in the VM's `/etc` (the Caddyfile's password hash is a
  placeholder), `backup.sh`, `remote-deploy.sh` (what the GitHub deploy job runs on the
  VM) and the bucket's lifecycle rule. Editing a unit or the Caddyfile here changes
  nothing by itself — a deploy does not apply them; `provision.sh` does.
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

### The eval gate: extractor and skill-list changes are measured before they merge

**Any change that touches the extractor or the skill list runs the dev eval before its PR
merges** (HIR-133, Chandler's decision 2026-11-03). This holds for autopilot and
orchestrator runs exactly as for attended ones — nobody is there overnight to ask for the
eval, which is how skill-list v6 and v7 merged unmeasured and left v8's small drop
untraceable to any one change.

The trigger is mechanical, so nobody has to judge it: **the diff touches
`app/extract.py` or `taxonomy/skills.json`** — the two inputs to `extractor_version`.
Then, before the PR is reviewable:

1. `uv run python scripts/run_eval.py --repeats 1` on the branch. Dev split, about 20 model
   calls per repeat — cents, not the ~€3 that re-reading every job costs on merge.
   **One repeat for a routine change, 3 before a release or when 1 repeat trips the gate**
   (DECISIONS 2026-11-04): a single repeat is the cheap read, and when it stops the merge
   you re-run at `--repeats 3` before believing the number, because one repeat is exactly
   the noise the gate exists to tame. 100 Goldens × 3 repeats is 300 traces, about 16 runs
   a month inside the free LangSmith plan — enough for releases, not for every PR.
   The held-out release gate always runs 3.
2. `uv run python scripts/eval_table.py <run_id>` and paste its output into the PR body
   under a `## Eval (dev)` heading. It compares every metric with the last committed dev
   run and shows the deltas.
3. **Commit the whole `evals/results/<run_id>/` directory in the same PR.** That run
   becomes the baseline the next such change is measured against, so there is no separate
   re-baseline step — and a PR that runs the eval without committing it leaves the next
   change nothing to compare against.

**Two stop lines, because the metrics carry very different amounts of evidence**
(DECISIONS 2026-11-04, HIR-164). `eval_table.py` applies both and exits non-zero on either,
so this is not a judgment call:

- **The four per-Golden attribute scores** — seniority, German, degree, production — are
  gated on **Goldens that flipped from right to wrong: more than 2 stops the merge.** Each
  is one yes/no answer per Golden, so on a 20-Golden set one posting is 0.05 of the score
  and a fractional threshold cannot tell one unlucky posting from a regression. The table's
  "Goldens worse / better" column is the number that decides; the Δ beside it is context,
  not a stop line. Don't read a 0.05 drop here as a regression — it is one posting.
- **The skill scores** — precision, recall, f1, requirement accuracy, grounding, rank — pool
  hundreds of mentions a run, so they keep the **0.02** drop rule. A smaller move is noise;
  note it in the PR and carry on.

Either kind of stop is on the stop list below: say so in the PR, don't merge, and ask.

Flips are counted by rescoring both runs' stored predictions, so if the table says they
**could not be counted**, read it: either a run has no `predictions.jsonl`, or the Goldens
were relabelled since a run and the two are no longer comparable Golden by Golden. The gate
then falls back to 0.02 for everything, which on a small dev set is strict — a flagged
attribute there may well be one posting. Say which case it is in the PR.

**One exemption, and it must be evidenced.** Run
`uv run python scripts/eval_table.py --version-check`. If it answers MATCH, the committed
baseline already scored this exact extractor — prompt, tool schema, model id and skill list
all identical, the branch only touched a comment, a docstring or a test helper — so a fresh
run cannot produce new information. Skip it, and paste those two version lines into the PR
body instead of the table. If it answers DIFFERENT, the gate applies, and that includes the
case where the branch changed nothing but main itself was never measured: then the run also
re-baselines main, which is the gap this rule exists to close.

The held-out split stays release-only (the rule just above). This gate is the dev split.

### A change to an agent's instructions takes effect in the next session, not this one

Agents and skills load from the project folder on Chandler's Mac, not from the branch and
not from GitHub, and the copy in that folder is only refreshed when a session starts with
`claude-hr`, which pulls `main` first (HIR-153). So a merged edit to `AGENTS.md`, a skill or
an agent definition is inert until the next such session: the agents running now, including
any subagent this session starts, still follow the version the folder held when it opened.

**Don't test a change to an agent's instructions in the session that made it** — test it in
the next one. On 4 Nov an agent spent a long investigation diagnosing the reviewer from the
branch while the reviewer it was watching ran a version two tickets older (HIR-145).

### The rules gate: a PR that changes the agents' own rules asks Chandler first

**No PR that touches the agents' own rules merges on its own** (Chandler's decision
2026-11-04, HIR-142). Since HIR-136 a reviewed PR merges itself, and that would include a PR
that rewrites how review and merging work: an agent could change its own rules and the change
would land without Chandler ever seeing it.

The trigger is a file list, not a judgment. The diff touches any of:

- anything under `.claude/` — agents, skills, settings
- `AGENTS.md`
- `.github/pull_request_template.md`
- anything under `.github/workflows/` — the automated checks are part of the gate
- `scripts/rules_gate.py` — the gate's own code, so a PR cannot rewrite the check into
  one that always passes

Then the PR gets `needs-chandler`, does not merge, and its description carries this block,
with nothing more in it:

> Changes were made to .claude/agents/skills:
>
> * bullet a
> * bullet b
>
> Did you authorize these?

One bullet per change, in plain words. No paragraph, no diff walkthrough. **The reviewer
writes the bullets; the agent that made the change does not** — the point of the gate is a
second reader saying what changed. Chandler does not read these files. He discusses what goes
in them beforehand, so the only question is whether he authorized this one. He answers by
merging, or by sending it back.

**Two enforcers, because one of them is itself a rule file.** The reviewer applies the rule
(`.claude/agents/reviewer.md`). And `scripts/rules_gate.py` runs in CI on every PR
(`.github/workflows/rules-gate.yml`, check name "Rules gate"): it reads the PR's own changed
files and fails when one of them is a rule file and the block is absent. That half is the
backstop — it still fires on a PR that edits the reviewer's instructions out of existence. It
re-runs when the PR description is edited, which is how it goes green once the reviewer has
added the block.

A failing check only blocks a merge once it is on the repository's required-checks list, and
**that list is Chandler's to change, never an agent's** (DECISIONS 2026-11-04). It is a
repository setting, so no diff can show a change to it — which is exactly why it is the one
gate an agent cannot edit through a PR.

### Pitfalls specific to this project

- `ReAct` (agent pattern) and `React` (framework) differ only by case. The taxonomy
  resolves them case-sensitively; keep it that way.
- `scripts/seed_from_legacy.py` output no longer matches the committed taxonomy/Goldens
  (they were hand-edited after seeding). Never run it against the real files.
- Feeds return everything; `app/ingest.py` filters by title regex and *active* city. A job
  in an untracked or inactive city is dropped, not stored. `app/geo.py` has two lists:
  `CITIES` (recognized) and `ACTIVE_CITIES` (collected: Berlin, `REMOTE_EU`, San Francisco
  and New York). The scope is Germany, EU-remote, and the cities Chandler has turned on —
  SF since 2026-11-03 (HIR-12), New York since 2026-11-03 (HIR-132). Launching a city is
  automated: `discover-boards --launch <city>` applies the written board policy itself and
  reports afterwards, so neither the city nor its boards waits on approval (DECISIONS
  2026-11-03, HIR-132, which supersedes both the "SF is the single exception" line and the
  manual `--add` approval rule). Adding a city Chandler has *not* named is still his call.
  EU-remote rules live in `geo.is_remote_eu` (DECISIONS 2026-10-26).
- `skill_mention` holds one extraction per job (the latest). Re-extraction replaces.
  `extraction_reject` (items that failed validation) follows the same rule.

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


### Deciding alone vs. stopping

Agents decide the small things and stop for the big ones. The test for a decision is
whether Chandler could judge it right or wrong from one plain sentence; if he couldn't,
it is either mechanical (don't report it) or badly explained (rewrite it).

**Decide, don't report** — mechanical, already settled by this file or DECISIONS.md:
next free migration number; DECISIONS.md merge conflicts (keep both entries, newest
first); a proposed skill needs 3 jobs before it becomes an entry; alias before new entry
when a phrase is another spelling of an existing skill; test names, fixture choice,
commit wording.

**Decide, then report in the PR's "Decisions taken"** — judgment, cheap to undo: which
postings to sample; how a UI label or a DECISIONS entry is worded; alias vs. new entry
when the phrase is genuinely ambiguous; the shape of a taxonomy change (parent/children,
which entries); anything the issue left open that costs one commit to reverse. One
sentence each: what, why, how to undo.

Anything that bumps `extractor_version` (prompt, taxonomy, model) is decided here too.
Say in the PR body that merging re-reads every job (about €3). **The merge is the
approval**; nothing waits before the PR.

**An existing rule is never a question.** When an issue and DECISIONS.md (or this file)
disagree, the rule wins: apply it, note the conflict in one line under "Decisions taken",
carry on. Before asking anything, check whether a standing rule already answers it. Ask
only when no rule covers the case — then the answer becomes a rule, and the question
is never asked again.

**Stop and ask, even unattended** — irreversible, expensive, or policy:
- any edit to `evals/LABELING.md` or to an attribute's definition (invalidates every eval)
- `ACTIVE_CITIES`; what the public site stores, shows, or sends to a provider; spend
- deleting or rewriting stored jobs, Goldens, or eval results
- an eval score over either stop line against the last committed run: a per-Golden
  attribute score that lost **more than 2 Goldens**, or a skill score **down more than
  0.02** (the eval gate above; the run itself is not a question, only a result this size is)
- the branch and `TICKET` disagree; a hot-spot file is already changed on another branch
- a PR that changes the agents' own rules — `.claude/`, `AGENTS.md`, the PR template,
  `.github/workflows/` (the rules gate above). The reviewer is what asks, by adding the
  block to the PR; no run of any label merges such a PR.

**Questions go to the decider agent before they go to Chandler.** `.claude/agents/decider.md`
(Fable) reads only AGENTS.md, DECISIONS.md, taxonomy/README.md and evals/LABELING.md, and
answers the question from them. It returns either an answer with the rule it rests on (the worker
applies it and notes it under "Decisions taken"), or "no rule covers this" plus the
question rewritten per "How to write anything Chandler reads". Only the second kind
reaches Chandler: a comment on the Linear issue that @mentions him, two sentences of
situation, one line per option with its consequence, a recommendation. His answer is
written into DECISIONS.md so it is never asked again. Meanwhile the worker does any step
that doesn't depend on the answer, and stops.

**Autopilot is the default** (HIR-120). `/work-issue HIR-n` runs unattended: no "go" on
the brief, every question to the decider, the first thing Chandler sees is the PR. The
worker adds the `autopilot` label to the issue itself; that label is what the reviewer
reads before merging, not a thing anyone applies by hand. A NO RULE from the decider
still stops the run — guessing is not autopilot.

An issue runs **attended** only when Chandler wants to be in it: `/work-issue HIR-n
attended`, or the Linear label `attended` on the issue (he applies that one, or an agent
filing an issue that plainly needs him — a direction call, a public-facing change, work
he asked to be involved in). Attended means the brief waits for his "go" and the PR waits
for his merge.

What keeps the default safe is the stop list above and the reviewer's file stop-list,
which apply to every run regardless of label.

**Who merges.** A worker never merges its own PR. For an `autopilot` issue the
`reviewer` agent (`.claude/agents/reviewer.md`, fresh context, Fable) merges when CI is
green, the diff stays in scope and off the stop-list files, "Needs Chandler" is empty,
every decision has an undo and every follow-up a ticket; otherwise it labels the PR
`needs-chandler` and @mentions Chandler on the issue. A PR that changes the agents' own
rules is never merged by any run — the rules gate above. At most one PR that re-reads every
job (taxonomy, prompt, model) merges per day. PRs for `attended` issues always wait for
a person.

**No person presses anything: the reviewer merges, or arms auto-merge and GitHub does it**
(HIR-136, HIR-157). The reviewer reads `mergeable_state` and that picks the command. A
`clean` PR — required checks already green, branch up to date — is **merged directly**,
`gh pr merge <n> --merge`, because GitHub refuses to arm auto-merge on a PR that can
already merge, and the reviewer usually arrives after CI has finished. Any other state gets
`gh pr merge <n> --merge --auto`, which tells GitHub to merge the PR the moment its
required checks are green. Neither is a human merge, and neither can get round the checks:
the ruleset requires all three, so a merge command on a PR whose checks are not green is
refused by GitHub. Any other error from either command is `needs-chandler` with no retry.
There is **no merge queue** on this repository and there cannot be — GitHub offers queues
only on organization-owned repositories, and this one belongs to a personal account.
HIR-124 wrote a queue into these rules anyway, which is why every autopilot PR stalled
until HIR-136.

Because nothing is testing each PR against the latest main for us, **being behind main is
the reviewer's job**: `main` requires branches to be up to date before they merge
(`strict_required_status_checks_policy`, still on as of 4 Nov), so after arming auto-merge
the reviewer brings the branch up to date and the checks re-run. That is also why the two
merge paths above never overlap — with that policy on, a branch behind main reports
`behind`, never `clean`. A
**worker still never merges main into its branch** — doing that during review is what
produced the duplicate edits of 3 Nov; the point is that it happens once, at the end, and
not by the author. A real conflict drops the PR back to its author, which is the one case
that is still the worker's.

**Every merge happens from the run that reviewed it.** There is no timer and no scheduled
cloud reviewer: an autopilot `/work-issue` waits for CI at the end of its own run and
starts the `reviewer` agent on the PR it just opened; inside an orchestrator the
orchestrator does that instead. A run that stops before merging leaves its PR labelled
`needs-chandler` and says so, rather than leaving it for something to pick up later.

**A Linear description is appended to, never replaced** (HIR-124). Two agents overwrote
HIR-112's description on 3 Nov. Any agent — worker, decider, reviewer, orchestrator —
changing a description it did not write in this session uses `save_issue` with `patch`
(`append`, `insert_after`, or a single-match `replace`), or just adds a comment. A full
`description` field replace is only for a description this session wrote.

`/work-issue-orchestrator HIR-a HIR-b …` runs a batch: pick, one worker per issue in
parallel worktrees, reviewer merges the autopilot PRs, `attended` ones pause for
Chandler's go and wait for his merge, one report. More than one orchestrator may be
running, each blind to the other's workers: the shared state is the Linear issue status
(the claim) and the open PRs (what files are taken), never a session's own table.

### Skills

`.claude/skills/` holds the repeatable procedures. `/work-issue HIR-n` takes a Linear
issue to a PR; `/work-issue-orchestrator` runs a batch of issues through work, review and
merge; `/check-url` audits feed coverage for careers-page URLs. `.claude/agents/` holds
the `decider` (answers questions from the rules) and the `reviewer` (merges autopilot PRs). When a procedure
has been typed into a session twice, it belongs here; when one fails, fix the skill, not
the conversation.

<!-- END PROJECT -->
