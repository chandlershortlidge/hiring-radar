# Decisions Log

What we decided, why, and what we tried that didn't work — so nobody (person or agent)
re-treads a dead end or undoes a decision without knowing the reason. Newest first.

---

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
