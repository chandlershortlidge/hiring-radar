# Decisions Log

What we decided, why, and what we tried that didn't work — so nobody (person or agent)
re-treads a dead end or undoes a decision without knowing the reason. Newest first.

---

## 2026-10-20 — Seniority labels reviewed; "none" is a scored label

The 2026-10-18 dev eval had seniority accuracy 0.45. Most of the gap was the labels, not
the extractor: eight dev Goldens carried "mid" from the legacy project with no years, no
"proven", no level word — the default LABELING.md forbids. Reviewed all 20 with Chandler
against the guide: 9 → none (006 "all levels"; 007, 008, 010, 012, 013, 018, 019 no
signal), 003 senior → mid ("proven experience"), 016 senior → mid ("3+ years"), 002 and
011 inferred → stated (level in the title). Every label now quotes a verbatim
`seniority_signal` (or is none); `seniority_signal_legacy` removed.

The evaluator used to treat a None seniority as unlabeled and skip it, so guessing a level
on a "none" posting never counted as a miss. Now a Golden is scored whenever it carries a
`seniority` key, None included — the same as German and degree.

Re-scoring the 2026-10-18 predictions against the new labels: 0.80. The remaining misses
(003, 006, 009, 017) are the extractor reading "proven" and "all levels" differently from
the guide.

## 2026-10-20 — German rule unchanged after review: a stated working language wins

Considered and reverted the same day: "a posting written in German requires German, even
if it also asks for English" (e79af37). golden_024 (Parship) is written in German but asks
only for "Gute Englischkenntnisse für die tägliche Kommunikation" — good English for daily
communication, i.e. the working language — and never mentions German. Parship presents
itself as international and lists some jobs in English. The original rule already
gets this right and stays: a German-language posting counts as German required (inferred)
only when it says nothing about language; when it names a language, the text decides.
golden_024 is "German not mentioned". LABELING.md, the prompt and extractor_version are
back to their pre-e79af37 state, so no re-extraction.

Kept from the same review (golden_022–024, now final held-out Goldens): a tech list headed
"in our projects we often use" counts as a tech-stack list (all entries required), as in
dev golden_003, even at a consultancy; and "you are an expert in X" counts as a
requirement wherever it appears, including the responsibilities.

## 2026-10-19 — Consulting roles are out of scope for the MVP

Titles like "Consultant GenAI & Agentic AI" fail the title filter ("Consultant" is not a
role word), and they stay out, both from feeds and from manual `check --add`. The chart
measures what AI *engineering* jobs ask for. Consulting JDs mix in advisory skills (client
management, pre-sales, workshops) that would dilute it. Adding them by hand, one at a time,
would also make the data depend on which links someone happened to click.

To revisit: `url_check.diagnosis` records every rejected check, so count the "Consultant"
title rejections first. Widening is one word in `ROLE_PATTERN` (`app/ingest.py`).

**Exception: roles that build the AI themselves are kept, whatever the title.** For example,
"AI Associate - Voice-Agents" (Lane One, job 145) runs client workshops and then builds and
integrates the agent (MCP tools, testing). The test is whether the job builds something.
Client-facing work alone does not rule a role out. These come in only through
`check --add` (which trusts the title), because feeds still drop titles like "Associate".
The trade-off is accepted: part of the point is to count roles like this, especially ones
that require German.

## 2026-10-18 — Open rule: complete feeds vs search sources

A job counts as open while a *complete* feed (Greenhouse, Lever, Ashby, arbeitnow,
startup.jobs) saw it in the last 3 days — those list every live posting each poll, so
absence means closed. JSearch and the Arbeitsagentur are *search sources*: JSearch returns
~10 ranked results per query, the Arbeitsagentur query only covers postings published in
the last 30 days, so absence there proves nothing. A job known only from search sources
(or added by hand) is assumed open for 60 days. When a complete feed has the job, only
that feed's own last sighting counts — a search source re-finding a job must not keep a
delisted board posting open. `queries.FEED_SOURCES` / `SEARCH_SOURCES`.

German-language postings arrive via the Arbeitsagentur and are not represented in the
Goldens. `scripts/new_goldens.py --german N` drafts unlabeled held-out Goldens from them
(no model pre-fill — held-out labels must not be anchored on the extractor's answer);
run_eval skips files marked `draft`.

## 2026-10-18 — German and degree are per-job attributes, extracted like seniority; three is the limit

Two more things a posting asks for that decide whether it is open to a given person:
German, and a degree. Neither is a skill (PRINCIPLES rule 2 still excludes them from the
skills list); each is a per-job attribute with the seniority shape — value, basis, verbatim
signal — in migration 006, with the same validation rule: a value without a quote found in
the text collapses to "not mentioned". The one exception is `german_basis='inferred'`: a
posting written in German, which carries no quote.

Degree carries `degree_or_equivalent` because "or equivalent experience" is the line that
decides whether a posting is open to someone without a degree. A bare "Master's in CS or a
related field" in a requirements list is `required`, `or_equivalent=false` — "related
field" widens the field, not the requirement. Expect most labeled degrees to be `required`.

Both are scored in the eval (`german_accuracy`, `degree_accuracy`) over every Golden that
carries the key, so "not mentioned" is a scored label — unlike seniority, where an unlabeled
and a labeled-none Golden are indistinguishable today. The 21 Goldens were pre-filled and
marked `attrs_reviewed: false`.

Rule going forward: `job` now has three attribute column groups (seniority, german, degree).
A fourth per-job requirement (years of experience, visa sponsorship, remote) goes into a
`job_requirement` table, not more columns on `job`.

Done in one migration and one prompt change so the ~78 jobs re-extract once, not twice.

## 2026-10-17 — Legacy-only jobs are listed but never charted or re-extracted

Of the 48 jobs imported from the old project, 7 had no posting text and no screenshot.
They were inserted with the old summary as text and the hackathon extractor's skills,
stamped `extracted_version='legacy'`. Those skills were never produced by the evaluated
extractor, and re-extracting from a summary would be worse than the labels they carry.

Decision: `queries.job_set_clause` excludes them from skill frequencies and city totals;
`list_jobs`/`job_detail` include them with `legacy: true` so the UI can show them greyed;
`pipeline.jobs_needing_extraction` skips them permanently. The way to fix one is to add
the real posting (link or screenshot), which supersedes it through the normal dedup path.

The 21 screenshot-transcribed imports are a separate, open question: the extractor is
evaluated, the transcription step is not. Labeling a sample of them as held-out Goldens
(checking transcript against image first) covers both.

## 2026-10-17 — Held-out Goldens: only postings labeled after the freeze

A held-out Golden is one labeled **after the prompt and taxonomy froze (2026-10-16)** and
never used while tuning — not looked at, not scored against while a rule was being changed.
The original 20 Goldens are `dev` permanently: all of them were labeled, relabeled or
scored against while the prompt and taxonomy were being written, so none can serve as an
out-of-sample check. **golden_021 (Almedia) is the first held-out item.** New Goldens go to
`heldout` unless they are added to fix a dev-side problem.

---

## 2026-10-17 — Every `check` is logged; coverage is measured over checked URLs

The coverage line in `stats` (manually added jobs a feed later matched) read 0/48 and
could not move: all 48 manual jobs are legacy screenshots with no URL, and a `check` that
found the posting already in a feed left no trace, which was the most informative outcome
of all. So `check` now appends one row to `url_check` (migration 005): url, time,
`found_via`, verdict, matched job, and `feed_had_it`.

- **`feed_had_it` is fixed at check time:** found, and at least one of the job's sources
  is a feed (not `url`/`paste`/`screenshot`). A job a person added by hand earlier does
  not count as feed coverage.
- **Only the first check of a URL counts.** The /check-url skill re-checks after adding a
  board and polling; that re-check finds the job via the feed and would otherwise score as
  the feed having had it all along. A different URL for the same posting counts again;
  accepted, it should be rare.
- **`check_url` itself still never writes.** `log_check` is called from the CLI; the
  existing coverage line stays alongside the new one.
- **`found_via` default unchanged** (`company_site`, from the `check` entry below). For
  the LinkedIn flow pass `--found-via linkedin`; the skill now says so.

---

## 2026-10-17 — Skills count only where the candidate is asked for them (PRINCIPLES rule 1)

The chart measures **what employers ask candidates to have**, not what the job involves.
Those are different sets, and conflating them makes the ranking useless: almost every
posting *describes* technologies in its responsibilities, so a chart built from
responsibilities measures what teams happen to run, which is already public and tells a
candidate nothing about what to learn.

So rule 1 of `PRINCIPLES` in `app/extract.py` stands: extract only from requirements,
qualifications, "nice to have" lists, or a dedicated tech-stack section. A technology that
appears **only** in responsibilities or the company description is excluded unless the
candidate is also asked for it.

This looks like under-extraction when you read a posting by eye, and it is not.
`golden_021` (Almedia, Junior Data Scientist, job 66) is the reference case: the posting
says "Run A/B tests on offers, rewards and ranking" and "Build and fix the data pipelines
your models depend on" under *What You'll Do*, and `a-b-testing` and `data-pipelines` both
exist in the taxonomy — yet the Golden expects only `python` and `sql`, the two skills
*What You'll Bring* actually asks for. A low skill count on a long posting is not by
itself evidence of a bug; check which section the skills sat in first.

Consequence to live with: a posting that lists its stack only in responsibilities
contributes few or no mentions. That is the intended trade — a precise answer to a
narrower question beats a muddled answer to a broader one.

---

## 2026-10-17 — `check`: audit feed coverage one careers-page URL at a time

The question behind the LinkedIn pass is not "add this job" but "did the feeds already
have it, and if not, why not". `python -m app check <url>` answers that without writing.

- **Three lookups, in order.** (1) A hosted Greenhouse/Lever/Ashby URL carries the board
  token and the board's job id → exact hit on `job_source`, no network. (2) Otherwise the
  posting text is fetched — from the board API when the board is known, else the page
  (JSON-LD `JobPosting` if present, whole page text if not) — and matched against stored
  jobs of the same company. (3) Nothing → `not found` plus a diagnosis.
- **Text matching is containment, not Jaccard.** A careers page carries nav, footer and
  sibling listings, so ingest's symmetric similarity would score the same posting below
  0.7. `check` scores the share of the *stored* JD's shingles present on the page (≥ 0.7).
  Ingest's dedup is unchanged; `--add` still goes through `ingest_one` and its rules.
- **The diagnosis is the product.** It says what to do: `board lever:newco is not in
  config/feeds.json — add {...}` (the common case, paste it into feeds.json); the board is
  polled but the title or city filter would drop it (a filter bug or a correct rejection —
  the person decides); polled and it passes (posted since the last poll, or a feed bug);
  or not an ATS page at all (no feed can reach it; `--add` stores it as `source=url`).
- **`--add` keeps the feed identity.** A board posting is ingested as its feed source with
  its board id, so the next poll sees it as still-listed rather than a repost; a page
  posting is `source=url`. `found_via` defaults to `company_site`.
- **LinkedIn URLs are not fetched.** Out of scope by the first entry; the page needs a
  login anyway. `check` reports them as not-an-ATS-page.
- Not done: a `gh_jid` embed URL gives the job id but not the board token, so it gets the
  exact lookup but no board fetch; the coverage number in `stats` still counts only manual
  adds, so a `found` with no `--add` leaves no trace.

---

## 2026-10-17 — Seniority comes from stage 2, with a basis, or not at all

Same three fields as the legacy project (level, basis, quoted signal), produced by the
same stage-2 call that returns skills — no extra model call.

- **Levels: junior / mid / senior, or none.** The legacy extractor forced a guess and
  defaulted to mid (most legacy rows read "Mid / inferred"). Now a level without a basis
  is dropped, a "stated" level must carry its quoted signal, and "all levels" or no signal
  means none. Lead/principal/staff/architect fold into senior; intern/working
  student/graduate into junior.
- **Scored.** `seniority_accuracy` is reported next to skill P/R, over Goldens that carry a
  label. All 20 Goldens got their legacy labels, flagged `seniority_reviewed: false`:
  they were model output, not human review. Three look wrong under the new rules and
  should be checked first: golden_002 (working student → junior/stated, not inferred),
  golden_011 ("Lead AI Engineer" in the title → stated), golden_006 ("all levels" → none).
- **Stored on `job`** (migration 004). Re-extraction overwrites it like skills.
- **Why it matters:** seniority is the first filter in the user profile (role family →
  seniority → skills). It was the legacy dashboard's best demo and is the main lever
  for "jobs I could plausibly get" without a résumé.

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
