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
uv run python scripts/run_eval.py --repeats 1     # quick look
uv run python scripts/run_eval.py                 # dev split, 3 repeats → evals/results/<run_id>/

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
- `scripts/new_goldens.py` — draft unlabeled held-out Goldens from DB jobs
  (`--german N` or `--ids ...`); run_eval skips files with `"draft": true`.
- `scripts/agent_label.py` — held-out Goldens via two blind labeler agents: pick → label A
  and B → auto-check → merge → review queue (`label`), then your decisions → final Goldens
  with provenance (`apply`). Refuses to label with the extractor's model. Never runs the
  held-out eval. See DECISIONS 2026-10-27 and `evals/LABELER_PROMPT.md`.
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
- an eval metric down more than 0.02 against the last committed run
- the branch and `TICKET` disagree; a hot-spot file is already changed on another branch

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
`needs-chandler` and @mentions Chandler on the issue. At most one PR that re-reads every
job (taxonomy, prompt, model) merges per day. PRs for `attended` issues always wait for
a person.

**Nothing merges directly to main: it goes through the merge queue** (HIR-124). The
reviewer enqueues (`gh pr merge <n> --merge --auto`) and GitHub does the rest — it builds
each PR on top of the ones ahead of it, runs the required checks on that combination, and
merges in order. So no branch is ever updated or rebased to get a merge through, and a
worker does not merge main into its branch before review: being behind main is the queue's
job. A conflict the queue can't resolve drops the PR back out to its author.

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
parallel worktrees, reviewer enqueues the autopilot PRs, `attended` ones pause for
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
