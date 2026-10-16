# Decisions Log

What we decided, why, and what we tried that didn't work — so nobody (person or agent)
re-treads a dead end or undoes a decision without knowing the reason. Newest first.

---

## 2026-10-16 — Stage 1 (vision) and the legacy import

- **Stage 1 is transcription only.** The vision model returns the posting's text verbatim
  (headings and bullets kept, UI chrome dropped). It never names skills; stage 2 reads
  the transcript like any other text. Truncated, empty, or refused responses raise rather
  than yielding partial text.
- **Screenshot bytes are stored** on the job (`screenshot` table, SHA-256 unique), so stage
  1 can be re-run and a re-upload of the same image is caught before any model call.
- **Manually added jobs skip the title filter** (`trust_title`): a person chose them.
  Feeds still go through it.
- **A backdated sighting may move `first_seen` earlier.** Needed for the legacy import,
  where real capture dates are June–Sept 2026.
- **Legacy corpus: 48 jobs in three groups.** 20 have text in the Goldens (19 corpus +
  Artefact, which was deleted as job-1 and re-added live); 21 have a screenshot and get
  transcribed; 7 have neither (files never stored) and are imported with the old summary
  as text and their old skills mapped through the taxonomy, stamped
  `extractor_version='legacy'` so they count on the chart but are never re-extracted.
  Old labels the taxonomy can't resolve are dropped and reported. All legacy rows are
  `source=screenshot, found_via=linkedin`.

---

## 2026-10-16 — Title filter needs a role term; startup.jobs ordering is nondeterministic

- **An in-scope title names an AI/ML domain AND a technical role.** The domain-only regex
  put three postings in the database that nobody would call AI engineering: an
  `Account Executive / Sales Manager … Industrial AI & SaaS`, a `Call Center Agent` and a
  `Brand Agent … Minijob`. "AI" turns up in sales titles and "Agent" is a job-title agent
  far more often than the agent pattern. `in_scope_title` is now
  `DOMAIN_PATTERN and ROLE_PATTERN` (role = engineer/developer/scientist/researcher/
  architect/mlops). `applied scientist` and `research engineer` stay in the domain pattern
  too, so those role names still pass on their own as they did before.
  Also fixed in passing: `\bdata scien\b` could never match "Data Scientist" — the trailing
  word boundary made the prefix useless. It is `data scien\w*` now.
- **Those three jobs are deleted from the local DB** (ids 1, 7, and 8; no skill_mention rows
  between them, so no chart data moved). They cannot be re-ingested under the new filter.
  Three more stored jobs are out of scope under it and were **not** deleted — two
  `Senior Performance Marketing Manager … & AI` and one `AI Consultant – Customer
  Experience`. They are where the Meta/Bing/Pinterest/Reddit Ads proposals come from, so
  the next person looking at `proposed_skill` should decide whether to drop them as well.
- **startup.jobs page ordering is unstable between calls; accepted.** The same query minutes
  apart returns a different page 1, so pages collected across a poll can repeat jobs or miss
  them: per-poll coverage is nondeterministic. Dedup absorbs the repeats and the next poll
  catches what a run missed, which is enough for a document-frequency chart. Not worked
  around — no cursor snapshot, no retry-until-stable.
- **Taxonomy v3 adds `typescript`** (reviewed, no parents) and the four pending `TypeScript`
  proposals are `accepted` with `resolved_skill_id='typescript'`. Bumping the taxonomy
  changes `extractor_version`, which re-queues every job for extraction.

---

## 2026-10-16 — Intake: feeds, dedup, daily poll

- **Five adapters, one Posting shape.** Greenhouse/Lever/Ashby company boards, arbeitnow,
  startup.jobs (needs a free key; skipped without one). Each adapter's `parse` is pure and
  pinned to a recorded fixture. Adapters return everything; ingest filters.
- **Filters at ingest, not fetch.** Title regex (AI/ML/LLM/agent/…) and tracked-city match
  (`app/geo.py`). Remote-only and untracked-city postings are dropped. Manual adds skip
  the city filter.
- **Dedup is three checks in order.** (1) same source + same source id → still listed,
  bump `last_seen`, no model call. (2) same normalized company AND description similarity
  ≥ 0.7 (Jaccard over 3-word shingles) → merge: add a sighting; if that source already
  had a different id for the job, it's a repost (`repost_count` +1). (3) else new job.
  Company suffixes (GmbH, Inc…) and gender tags ((m/w/d)…) are stripped from keys.
  Below 0.7 is a new job; no review queue for near-misses yet — add one if the stats show
  it's needed.
- **Repost = same source, new id, same text.** Another source finding the same job is a
  sighting, not a repost.
- **Extraction is decoupled from fetch** and keyed on `job.extracted_version`: a job is
  processed once per extractor version, zero-skill jobs included; a taxonomy or prompt
  change re-queues everything on the next `extract`. One extraction per job is kept.
- **Coverage query lives in `stats`:** manually added jobs that a feed later matched ÷
  all manually added jobs.
- **Polling cadence: daily**, via Railway cron or crontab running `python -m app poll`.
  Re-running is idempotent.
- Not built yet: URL paste (ATS detection + HTML/JSON-LD fallback), screenshot path
  (stage 1), near-miss review, web UI.

## 2026-10-16 — Two labeling rulings; the labeling guide is frozen

`requirement_accuracy` sat at 0.944 (3 repeats, min 0.942 max 0.945 — stable, not noise)
while every other metric improved. The 19 disagreements behind it were not scattered
phrasing: 17 of 19 ran `nice_to_have` -> `required`, in two clusters that pointed opposite
ways. Both are resolved by deciding what the label means, not by tuning the model.

- **A section heading scopes the items under it.** 10 of the 19 were golden_019, whose
  `Strongly Preferred` heading the Goldens treat as covering every bullet beneath it. Rule
  6 listed only inline markers, so the model read each unmarked bullet as `required`. The
  Goldens were right; the rule was silent. Rule 6 now says a heading that marks its section
  optional sets the default for every item under it until the next heading, and a marker on
  the item itself overrides that default either way.
- **An unmarked entry in a tech-stack list is `required`.** The other cluster was
  golden_003's `Tech stack you will work with` line, where the Goldens had `langgraph`,
  `docling`, `litellm`, `phoenix` and `aws` as `nice_to_have`. Here the model was right by
  the prompt's own rules — a tech stack describes the job, and nothing marked those entries
  optional. Those five are relabeled `required`. Nothing else in any Golden was touched.
- **`raw_text` quotes the mention that determined the label.** `langgraph` and `aws` are
  each named twice in golden_003, once with an inline marker and once in the stack list;
  the stack mention is what makes them `required`, so that is the phrase they quote. Bare
  "LangGraph" appears 3x in that JD and bare "AWS" 6x, so these two quote enough of the
  stack line to identify it, which the shortest-phrase rule alone would not.

**`evals/LABELING.md` is the frozen guide** holding these rules plus the skill definition
and the one-criterion-per-skill rule. Editing it changes what the Goldens mean and
invalidates stored results, so an edit is a release decision: record it here and relabel in
the same change.

Before and after, dev split, 3 repeats, taxonomy v2, `claude-sonnet-5-5`:

| | P | R | F1 | req | rho |
|---|---|---|---|---|---|
| before (`x2-14856c159b`) | 0.901 | 0.973 | 0.936 | 0.944 | 0.914 |
| rule 6 only (`x2-d5dedb6520`) | 0.903 | 0.970 | 0.935 | 0.988 | 0.910 |
| + golden_003 relabeled (`x2-d5dedb6520`) | 0.908 | 0.953 | 0.930 | 0.991 | 0.903 |

`requirement_accuracy` 0.944 -> 0.991, nearly all of it from the heading-scope sentence;
the relabeling added the last 0.003 and lifted precision. Both post-change runs share
`extractor_version` `x2-d5dedb6520` because the version hashes the prompt, tool schema,
taxonomy and model — not the Goldens — so a relabeling is invisible in it. Compare run
directories by timestamp, not version, when only labels moved.

The F1 and recall dip in the last row is one `stop_reason='refusal'` on golden_019 in run
3 of 3 (a red-team / adversary-emulation JD), which cost that run every skill in the
Golden: recall 0.913 against 0.970-0.976 in the other two. It is the model's safety
classifier declining, not an extraction bug, and it is intermittent — the same Golden
scored clean in the two preceding runs and in every earlier run today. Not addressed here;
if it recurs, the harness has no retry by design, so a refusal will keep showing up as an
error on whichever run draws it.

## 2026-10-16 — Stage 2 extractor and eval harness

- **Prompt = 8 general principles + the taxonomy as an id list.** No JD-specific rules; a
  test fails if known legacy Golden phrases appear in the principles.
- **Every mention must be grounded.** `raw_text` has to appear in the JD (case- and
  whitespace-insensitive) or the item is rejected and reported. Checked against the
  Goldens' own answers: 342/344 pass; the 2 failures are synthesized `raw_text` in
  golden_011 and golden_016 labels, which the scorer doesn't use.
- **Unknown labels are proposals.** `new:<Label>` (or an id the taxonomy can't resolve
  as a display/alias) goes to `proposed`, never to mentions. The eval summary lists the
  most frequent proposals as taxonomy candidates.
- **No retries.** Anything other than exactly one forced tool call raises; in the eval,
  that Golden counts as an error with all expected skills missed.
- **`extractor_version`** hashes the prompt, tool schema, taxonomy, and model, so any
  change to one of them produces a new version on stored rows and eval runs.
- **Micro-averaged metrics**, plus Spearman rank correlation and top-10 overlap of skill
  frequencies across the suite. Three repeats by default; summary reports mean/min/max.
- Default model `claude-sonnet-5-5` (override with `HIRING_RADAR_MODEL` or `--model`).
  Not yet run live.

## 2026-10-16 — Rebuild from scratch; scope, architecture, and evaluation reset

Built after a full review of the legacy `job-skills-dashboard` repo (164 commits, June–Sept 2026).

**Why rebuild.** The legacy core reached precision ~0.94 / recall ~0.83 on 20 Goldens and
stopped improving: three further prompt changes recovered nothing (legacy DECISIONS
2026-09-27). The review found the cause was structural, not wording:

- One vision call did reading, sectioning, skill judgment, labeling, and grouping at once.
  41 of 67 missed skills were in passages the model had already read.
- Skill policy lived as 44 prose prompt rules, several of them copying specific Golden
  JDs' wording and several reversing earlier rules. Two extractors (Python, Node) had drifted.
- The Goldens were both the development set and the benchmark, and expected answers were
  rewritten alongside prompt changes. The reported numbers were in-sample.
- About half the labeling and scoring (non-skill audit, alternative groups) fed features
  that are now out of scope, not the skills chart.
- ~46% of commits went to résumé tailoring, the email parser, and the storage/hosting
  work they required.

**Scope.** Intake → text → skill extraction → aggregate chart, by city. Out: résumé
matching/tailoring, email parsing, applicant counts, LinkedIn scraping.

**Architecture.** One Python process (FastAPI), Anthropic SDK in-process, SQLite on disk,
React frontend served by the same process, hosted on Railway. Dropped from legacy:
Daytona sandbox, Vercel functions, Supabase + RLS, Storage bucket, static jobs.json.

**Pipeline.** Two stages. Stage 1 (screenshots only): image → transcript. Stage 2 (all
jobs): text → skill ids from `taxonomy/skills.json`, plus `requirement` and supporting
`raw_text`. Labels the taxonomy doesn't know go to `proposed_skill`, never to the chart.
Rows store taxonomy and extractor versions so they can be re-normalized later.

**Taxonomy.** Seeded from the legacy alias map, every Golden label, and the legacy
implication edges (which become `parents`): 175 skills. All seed entries are
`reviewed: false`; the legacy corpus included non-skills (languages, domain knowledge)
that a human pass should remove.

**Intake.** Aggregator feeds (startup.jobs API, arbeitnow), company ATS boards
(Greenhouse, Lever, Ashby), pasted URL (ATS adapter or generic HTML fallback), pasted
text, screenshot. Daily polling.

**Dedup.** A source's own job id identifies "still listed" (update `last_seen`, no model
call). A new id from the same company with near-identical text is a repost: merge, bump
`repost_count`. Legacy experience: same-company "possible duplicate" warnings were almost
always the same job reposted 30–60 days later, so reposts merge rather than count as new.
SHA-256 screenshot dedup is kept only for screenshots.

**Coverage tracking.** Manual adds record `found_via`. Share of jobs with at least one
feed source, and the lag before a feed finds a manually added job, measure how much the
feeds can replace manual searching. Backend query only.

**Evaluation.** Goldens carry only `{skill_id, requirement, raw_text}`. Labeling guide is
written and frozen before new labeling. Split into dev and held-out; held-out results are
looked at only at release points. Metrics: micro precision/recall/F1 on skill ids,
requirement accuracy, and rank agreement (Spearman, top-10 overlap) between predicted and
gold skill frequencies — because the ranking is the product. Three repeats per prompt
version. One script, results committed.

**Second city.** `city` is in the schema from day one; SF ingestion starts after Berlin
extraction clears the held-out eval.
