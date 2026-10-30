# Decisions Log

What we decided, why, and what we tried that didn't work — so nobody (person or agent)
re-treads a dead end or undoes a decision without knowing the reason. Newest first.

---

## 2026-10-29 — Production experience joins the HIR-70 labeling: a production-only pass, no restart (HIR-85)

HIR-69 made production experience a fourth per-job attribute while HIR-70's held-out
labeling was mid-flight, so `scripts/agent_label.py` still labels three. The merge of main
into HIR-70 surfaced it as a red test, not a conflict: the Goldens had gained `production_*`
keys and the shape test read `golden_021.json` as its oracle. PR #24 fixed the oracle only
(it now builds the expected key set from `ATTR_FIELDS`); this entry records the plan for the
attribute itself. Nothing in the script has changed yet.

**(a) Four constants, one function, and an attribute scope.** `ATTRS` gains `"production"`,
which alone drives the agreement loop, the summary counters and `final_golden`'s field loop,
since all three iterate it. `ATTR_FIELDS["production"]` is
`("production", "production_basis", "production_signal")` — no `_or_equivalent`, so
`degree`'s special cases in `apply_decision` stay untouched. `ATTR_KEYS["production"]` is
`("production", "production_basis")`, following `german`: the value and its basis are
compared, the signal is checked verbatim but never compared, because two correct quotes of
the same requirement differ in length. `final_golden` gains `production_reviewed` as its own
flag beside `seniority_reviewed` rather than joining the `{german, degree}` set behind
`attrs_reviewed` — the dev Goldens already carry it as a separate flag. The labeler prompt
takes the production rules from this log's 2026-10-28 rule bullets as revised by the
2026-10-29 entry, which is what HIR-69's `rules_sha` hashes, not fresh wording: policy lives
in the recorded rules, not in a prompt rewritten from memory.

A fifth change makes (c) possible at all: **an attribute scope**, so a run can label
production alone. `label_heldout_production.py` says outright that `agent_label.py` "cannot
scope to one attribute", and without it the only way to add production to an existing Golden
is to re-label everything.

**(b) HIR-70's provenance shape is canonical, and the four old Goldens are not back-filled.**
The two shapes differ in scope, not format. `labeled_by` / `adjudicated` / `spot_checked`
are whole-Golden facts; main's `production_labeled_by` is a per-attribute string that also
carries a run id, an "A flagged uncertain" note and production's own `rules_sha` /
`prompt_sha` — none of which the trio has a slot for. So provenance becomes
per-attribute-capable where an attribute was labeled in a different run from the rest of its
Golden, rather than flattened into one list.

- **What we rejected:** migrating `golden_021`–`024`'s `production_labeled_by` into the trio.
  Those four predate HIR-70's process and have no `labeled_by`, `adjudicated` or
  `spot_checked` today. A whole-Golden `labeled_by` written from a string that only ever
  described production would assert provenance for skills, seniority, German and degree that
  nobody recorded — a quiet edit to the answer key, which is the thing this log exists to
  prevent. They keep their per-attribute record as it stands.
- The 20 dev Goldens carry `production_reviewed` but no `production_labeled_by`; they need
  nothing here.

**(c) A production-only pass over the same 24 postings. No restart.** HIR-70's labeling
calls are already spent — `20261027T110516Z_label/summary.json` reports `n_labeled` 24/24,
`failed: []` — and what is in flight is human adjudication of a 201-item queue. Restarting
costs the same 48 labeler calls and additionally throws that adjudication away.

- **Cost is identical either way: 24 postings × 2 labelers = 48 calls.** The `extractor`
  model is recorded but never called; `check_models` uses it only to refuse a labeler that
  shares the extractor's blind spots. A restart buys nothing in calls.
- **The other three attributes are not re-labeled.** Agreement was seniority 1.000, German
  1.000, degree 0.958 (23/24), and each attribute is judged on its own `ATTR_KEYS`, so a
  fourth one changes nothing either labeler saw for the first three.
- **Precedent, not a new shape:** HIR-69 already ran exactly this pass over the four
  existing held-out Goldens (`20261029T153540Z_heldout_production`, 4 × 2 = 8 calls, same
  `claude-opus-5-5` / `gpt-6.1-sol` pair): 3 agreed, 1 disagreed, 3 uncertain.
- **The pass runs through the extended `agent_label.py`, not by widening the one-off.**
  `scripts/label_heldout_production.py` hardcodes `GOLDEN_IDS` to `golden_021`-`024` and
  borrows only the independence rules; its docstring already assigns the general tool to
  HIR-70. Widening it would fork the labeling pipeline in two.
- **Expect ~15–25 new queue items,** scaling that run's 1 disagreement and 3 uncertain to 24
  postings, minus the overlap between the two buckets. A spot-check over production at the
  main run's 80/305 rate costs no model calls - it samples items both labelers already
  agreed on for a person to re-check - and would add roughly 6 more items to adjudicate.
- The four existing held-out Goldens already have production labels and are not re-run.

A guard is already in place for the work: adding `production` to `ATTR_FIELDS` without
wiring it into `final_golden` fails the shape test in `tests/test_agent_label.py`.

---

## 2026-10-29 — Production experience: the verb, not the tense; a level-scoped demand is not job-wide (HIR-69)

Two rules settled at the Goldens checkpoint. They revise the rule bullets in the 2026-10-28
entry, which stands otherwise.

**The verb carries the demand, not the tense.** The 2026-10-28 wording asked for "a record
of having shipped", which read "able to ship production-quality agentic systems, not just
prototypes" (golden_019) as a quality bar and labeled it not mentioned. Wrong: the posting
is demanding that the candidate ship to production, and a modal demand is the same demand
as a past-tense one. `required` now covers ship / operate / deploy / run in production in
any tense or modality; only a bar on the code itself — "write production-grade code",
"writing production-quality code and tests" — stays not mentioned. golden_019 is `required`.

**A demand scoped to one seniority level is not job-wide.** golden_006 is open to "all
levels" and asks for "several years of practical experience in the design and operation of
productive AI systems" only under a "Senior Level:" heading. Labeling the posting `required`
hides it from a junior filtering on production-not-required, which is the opposite of what
that filter is for — the junior track of that posting carries no such demand. golden_006 is
not mentioned.

**Building is a demand verb.** The first eval run after the two rules above missed
golden_004 and golden_012 — both gold `required` on "experience building production-grade
applications" / "practical experience building production-oriented LLM workflows" —
because the prompt's verb test listed only ship / operate / deploy / run. State the rule
as the verb against its object: **build / ship / operate / deploy / run** production
systems, services, applications, pipelines or workflows is `required`; *write*
production-quality code is not mentioned. A hyphenated modifier on the object does not
weaken the demand — production-grade, production-ready and production-oriented software is
production software. golden_012 stays `required`: "practical experience building" is a
track record, and the gold does not move to match the model.

**Knowing about production is a knowledge bar.** golden_006 carries a *second* production
clause with no level heading — knowledge of MLOps and of how AI models are operated in
production — and the model read it as a demand in 2 of 3 runs. It is not one: asking what a
candidate knows of production is not asking what they have built or run, so it is not
mentioned. Consistent with golden_005, whose "deep knowledge of … deployment and
monitoring" is also not mentioned. golden_006 therefore rests on two rules, this one and
the level-scoping one above; either alone would leave the other clause unaccounted for.

**Optional markers are a category, not a word list.** golden_011's "production ML would be
highly relevant" is `nice_to_have` and was missed 3/3 because the prompt listed only
plus / preferred / ideally / advantage / bonus. The fix is the category — soft phrasing
that frames the demand as welcome rather than expected — not golden_011's wording. Putting
the dev set's own phrases in the prompt buys eval points and no accuracy, so
`test_prompt_contains_no_golden_specific_text` now also asserts the dev-Golden phrases
these three rules were tempted to copy are absent from `PRINCIPLES`.

**Candidate for the next iteration, not applied: the production object is necessary, the
verb is not.** After the rules above, dev production accuracy is 0.933 with both decoy
rows at zero, and the two remaining misses pull in opposite directions. golden_011
("…data platforms or production ML would be highly relevant", gold `nice_to_have`) is
missed 3/3 because the clause is a bare noun phrase in a list of optional extras — no
verb, so the verb-against-object test never nominates it. golden_010 is a false positive
in 1 of 3 runs on "you would rather ship a working automation in two weeks than a perfect
one in six months" — the verb *ship* with no production object. One rule answers both:
require the production object, and let it carry the demand whether or not a verb is
attached. **Deliberately not applied.** `nice_to_have` has support 1 on dev and golden_010
is a 1-of-3 flip, so changing the prompt for either is fitting the 20-Golden dev set, and
the prompt is frozen for this release regardless of what the held-out run says. Both are
written up as known misses in the dev run's `summary.md`.

**The held-out relabel uses these rule bullets directly, and `evals/LABELING.md`'s
`## Production experience` section is deferred.** The guide is the usual source for a
labeler, but HIR-70's adjudication run (`evals/labeling/20261027T110516Z_label/`, on
`chandlershortlidge/hir-70-held-out-goldens-via-independent-agent-labeling-2-blind`) inlines
LABELING.md into its labeler prompt and keys its cached labels on that prompt's hash, so
editing the guide mid-run invalidates every label it has cached — a restart that run has
already paid for once. The section goes in once that queue closes, with the relabel, as the
release decision the 2026-10-16 freeze requires. Until then `scripts/label_heldout_production.py`
sends golden_021-024's labelers the 2026-10-28 definition and rule bullets verbatim and
nothing from `app/extract.py`. Labeling golden_021-024 for production is HIR-69's gap:
they were labeled at the freeze, before this attribute existed, so the held-out split
scores seniority, German and degree but not production.

All of these rules are in the `PRINCIPLES` prompt rule in `app/extract.py`, so the prompt hash
changes and stored eval results from before this entry are not comparable. `evals/LABELING.md`
still owes its `## Production experience` section (frozen; 2026-10-16) — it must carry both
rules when it is written, with the relabeling, as a release decision.

---

## 2026-10-29 — The skill filter is a set, read as AND (HIR-75); the chart gets a find box (HIR-67A)

HIR-66 left the related-skills rows unclickable because drilling in ("jobs requiring both")
needed the skill filter to hold more than one id. It does now.

- **Several skills mean AND, never OR.** The question the panel asks is what jobs wanting
  *both* X and Y also want; an OR would answer a question nobody asked and would make
  `selected_count` grow as skills were added, which reads as the opposite of narrowing.
  `Filters.skill_id` became `skill_ids`, and the API takes repeated `skill=` params, the
  convention `city` and `seniority` already use.
- **One `EXISTS` per selected skill, each under its own alias** (`_skills_clause`), so
  "required only" vs "required + nice-to-have" still applies per skill rather than being
  smuggled in once. The clause is shared by `list_jobs` and `related_skills`, so the panel
  and the list can never disagree about which jobs are in the conditional set.
- **The baseline stays the whole filter set.** Only the conditional set narrows as skills
  are added. Holding the share against a baseline that narrowed with it would drive every
  lift towards 1 and empty the panel of meaning.
- **MIN_CO_JOBS prunes harder with every skill added, and that is correct.** Five jobs is
  the point below which one odd stack of skills reads as a signal (2026-10-28); that does
  not get weaker because the selection got more specific. So the panel has two empty
  answers and words them differently: no job requires them together, or some do but
  nothing else recurs in at least five of them.
- **No new field on the response to say which.** `selected_count` already tells them
  apart, and adding a key would have changed the single-skill response. That response is
  pinned: `tests/fixtures/single_skill_api_snapshot.json` holds nine responses captured
  from the pre-change code, replayed as a test, so a single `skill=` answers field for
  field as it did before.
- **A chart click replaces the selection; shift- or meta-click adds; a related row always
  adds.** Swapping the skill you are looking at is the common move and keeps its plain
  click. Adding is deliberate, and the related panel is the place you go *to* add, so its
  rows need no modifier. The hint under the chart says so — and it now stays visible when
  a profile is set, where the legend used to take the whole line and hide it.
- **The main chart still ignores the selection**, as in HIR-66. Selecting skills moves the
  job list and the panel, never the bars.
- **No URL sync.** A shareable link to a filter set is a separate piece of work.
- **The find box above the chart (HIR-67A part A) is display only.** It narrows rows by
  display name or any alias — which is why `/api/taxonomy` now carries aliases — and it
  filters *before* the show-15 cut, so typing a name surfaces a skill that would otherwise
  sit past it. It never touches the selection and issues no request. Ranks and the axis
  keep the values they have in the whole chart: a filtered row still says where it sits
  overall, and bar widths do not jump while typing. Full-text search over postings
  (HIR-67 part B, FTS5) is not part of this.

---

## 2026-10-28 — Production experience is a fourth per-job attribute, not a skill (HIR-69)

Does the posting **demand production work of the candidate — shipping or operating
software that real users depend on?** `required | nice_to_have | not mentioned`, with a
quoted signal — the German shape, in migration 013.

Not a skill: the taxonomy excludes work practices, and "production" or "produktiv" appears
in 168 of 243 stored descriptions, so as a skill it would sit atop every chart and measure
nothing. This is the first entry of HIR-59's role-demands vocabulary and answers HIR-35 for
this one practice.

Rule bullets revised 2026-10-29 — see that entry for what changed and why.

- **The line is the verb, not the tense.** A demand to build, ship, operate, deploy or run
  software in production is `required` in any tense or modality — "you have shipped
  production systems", "experience building production AI systems", "able to ship
  production-quality agentic systems", "track record of building and running production
  services", "commercial software engineering experience in production environments". A
  past record, a present ability and a stated expectation are the same demand; *build*
  alone carries it; and a hyphenated modifier on the object (production-grade,
  production-ready, production-oriented) does not weaken it.
- `nice_to_have`: that same demand marked optional. The marker may be explicit —
  "experience with production ML is a plus", "ideally…" — or soft phrasing that frames the
  demand as welcome rather than expected ("production ML would be highly relevant",
  golden_011).
- **Not mentioned** when the posting never asks the candidate for it. Most mentions of the
  word are responsibilities ("you'll deploy models to production", "turn prototypes into
  production-ready systems", "from idea to production"), and PRINCIPLES rule 1 already
  excludes responsibilities for technologies — the same rule applies here.
- **A quality bar on the code itself is not the demand**: "write production-grade code",
  "strong Python skills, including writing production-quality code and tests" → not
  mentioned. The attribute measures a demand to ship or run the software, not a standard
  for the code to be written. The verb is the test: *build*, *ship*, *operate*, *deploy*,
  *run* → `required`; *write*, *code to* a production standard → not mentioned. The corpus carries
  both one clause apart — golden_018 has each — so the verb decides, not the tense.
- **Knowledge of production is not a demand to have done production work.** "Knowledge of
  MLOps and the structured operation of AI models in production environments" (golden_006),
  "deep knowledge of … deployment and monitoring" (golden_005) → not mentioned. What the
  candidate is asked to *know about* is not what they are asked to have built or run.
- **A demand scoped to one seniority level is not a job-wide demand.** A posting open to
  several levels that asks for production experience only under a level heading
  ("Senior Level: several years … in the design and operation of productive AI systems")
  is not mentioned: the track the posting opens to a junior carries no such demand, and
  `production=not_required` has to keep showing that posting to a junior. golden_006 is the
  reference case.
- German postings: `required` on "Du hast bereits Produkte … in den produktiven Betrieb
  gebracht", "Erfahrung mit produktiven AI-Anwendungen, nicht nur Prototypen". Not mentioned
  on the common "von der Idee bis zum produktiven Einsatz" responsibility phrasing.
- **No `inferred` basis.** `production_basis` only ever holds `stated`: unlike German,
  nothing about the posting's own form implies the demand. The validation rule is otherwise
  German's — a value whose quoted signal is not found in the text collapses to not
  mentioned.

Amends the 2026-10-18 rule "three is the limit": column groups on `job` stay the pattern
through four demands. The fifth demand migrates all four groups into `job_requirement` in
one migration before it is added.

Filters mirror German's four keys exactly (`any | none | not_required | required`), because
`not_required` — not mentioned *or* nice_to_have — is the key the dashboard's headline set
needs and the ticket's proposed `nice_to_have`-only key is not asked for anywhere.

Why it matters: junior + German not required + production not required ≈ "jobs you can get
today", the set HIR-51's ranking should start from, and the number the Advisor (HIR-63)
needs to say how many doors a first production project opens.

Goldens, eval scoring and re-extraction are a separate change; `evals/LABELING.md` is frozen
and gains its `## Production experience` section there, with the relabeling, as a release
decision (2026-10-16).

---

## 2026-10-28 — Related skills rank by lift, against a baseline from the same filter set (HIR-66)

"43% of jobs want Machine Learning" says nothing about what else those jobs want. Selecting
a skill now opens a panel between the chart and the job list: of the jobs requiring that
skill, what else they require.

- **The baseline comes from the same filter set as the share.** `related_skills` takes its
  `total`, its baseline counts and its conditional job set from one `job_set_clause` (city,
  seniority, German, degree, window) — the baseline is literally `skill_frequency`'s output
  under the same filters, so the two can't drift. A share over Berlin jobs held against a
  baseline over all jobs would make every Berlin-heavy skill look like a signal.
- **Selected by lift, `(cond_count/selected_count) / (base_count/total)`, computed from the
  counts and never from the rounded percentages.** Raw share would fill the panel with the
  skills every job asks for; lift keeps the ones specific to these jobs — PyTorch (55% among
  ML jobs vs 21% overall) earns a slot that Python's 80% would otherwise take. Lift is
  rounded to three decimals before sorting, so ties break deterministically on count desc.
- **Those ten rows are then returned by share desc (pct, then count).** Lift decides who is
  in the panel; it does not decide the reading order, because a list whose displayed numbers
  jump around looks broken. The multiplier that justifies a row's presence is not shown
  (below), so ordering by it would leave the visible numbers unexplained.
- **Lift is not displayed.** The panel shows "55% · vs 21% of all jobs". For a common
  selected skill every row sits near the ceiling of 1/share, so the multiplier reads as
  noise next to two numbers people already understand.
- **Hidden under 5 co-occurring jobs (`MIN_CO_JOBS`), top 10 kept (`RELATED_LIMIT`).** One
  odd posting stacking six skills otherwise shows up as a 4x lift. Both thresholds, the
  sort and the cap live in `queries.py`, not the UI, so pytest covers them.
- **A separate endpoint, `GET /api/skills/related`.** `/api/skills` and `skill_frequency`
  are untouched — selecting a skill must not move the main chart or the compare view — and
  a regression test pins `skill_frequency`'s output against a snapshot taken before the
  shared group/sort/pct block was factored out into `_skill_rows`. The endpoint requires
  `skill` (422 without it); its requirement filter follows the request like everywhere
  else, so the conditional set and the baseline always use the same mention semantics.
- **Row click is a no-op for now.** Drilling in (jobs requiring both skills) needs `skill`
  to become a list on the filters with AND semantics; that is a second step.

---

## 2026-10-27 — Inferred seniority narrowed to years / "proven experience" / lead duty

`evals/LABELING.md` is frozen, so this records the edit. **The guide now matches the
extractor, not the other way round**, and three dev Goldens were relabeled to fit.

The gap: `app/extract.py` has told the model since `ac20971` (2026-10-20) that "experienced,
expert, advanced, autonomous, production experience" are not level signals on their own.
LABELING.md still allowed an inferred level from "ownership or mentoring language, or the
depth of the qualifications" — wider than the prompt, and the source of the entire dev
seniority gap: 0.850, identical across all three repeats of
`20261027T080458Z_dev_x2-ee524a6720`, every miss a deterministic `null` against a non-null
gold label.

**Decision: keep the strict prompt line; narrow the guide to it.** `null` is the safe error
here — seniority is a secondary filter in the profile, so a missing level costs a job a
place in a filtered view, while a wrong level puts it in the wrong one. A rule the extractor
can apply from the text beats a rule that needs a judgment about "depth".

Changed:

- **LABELING.md**, inferred basis: years of experience, "proven experience", or lead or
  mentoring duty — nothing else. "Ownership or mentoring language" is now just lead or
  mentoring *duty*, and "the depth of the qualifications" is gone. Spelled out that
  experienced / expert / advanced / autonomous / production experience / ownership language
  are not level signals alone, and that a posting whose only level-ish phrase is one of
  those is none, not a guess.
- **Relabeled → `seniority: null`, basis null, signal null**: golden_004 ("Strong hands-on
  software engineering background with experience building production-grade applications"),
  golden_005 ("Expert knowledge on state-of-the-art AI use cases"), golden_015 ("High
  ownership mentality"). All three keep `seniority_reviewed: true`. golden_017 keeps `mid`
  on "Proven expertise in machine learning algorithms" — "proven experience" is still a
  basis. golden_003, 009, 014, 016 unaffected.
- **No prompt change, no `extractor_version` bump, no re-extraction.** The extractor already
  behaved this way; only the labels and the guide moved.

Re-scoring the stored `20261027T080458Z` predictions against the relabeled Goldens (no new
model calls): **seniority accuracy 0.850 → 1.000, 20/20 on all three repeats**, zero
remaining misses. That run's own `summary.json` still reports 0.850, since it records what
was scored at the time.

Supersedes HIR-71, which was filed the other way round (fix the prompt, keep the guide) and
is closed pointing here. The nine Goldens already labeled `None` are unaffected — they were
never the problem; `ac20971` is what made them stable (13/20 → 20/20), and it stays.

HIR-70's held-out labelers read LABELING.md, so the run must use the narrowed guide: the
labeling run started before this edit was stopped at posting 3 of 24 and restarted after it.

## 2026-10-27 — Held-out Goldens come from two blind labelers plus human adjudication (HIR-70)

> **Finished 2026-10-30: adjudication by model, a person on what the models could not
> settle.** Run `evals/labeling/20261027T110516Z_label/`, tracked in git. **Do not re-merge
> it** (`label --run …` rewrites `review_queue.md` from `items.json` and would erase every
> decision; the queue file is the only copy). Applied; 22 Goldens written.
>
> Hand-adjudicating 201 items was abandoned after 49 of them: too slow to finish. The rest
> is decided by model, with a person reading only what the models cannot settle between
> them, plus a seeded sample. Three new subcommands, each refusing any model that is the
> extractor or a labeler in this run:
>
> - **`judge`** — for every undecided item carrying a `PROPOSED:` line, a third model rules
>   on it given the posting excerpt (with the section heading above the quote), both
>   labelers, the proposal and its reason, and the five rules below. Agreement with the
>   proposal is recorded with `by: "model"`; disagreement leaves the item `?` for a person.
>   `gemini-4-argon`, a third family — not `gpt-6.1-sol`, which is labeler B and would have
>   been ruling on its own label on every A-vs-B item.
> - **`third`** — a blind third labeler over the postings behind the agreed spot-check
>   labels: same prompt, same posting bytes, no sight of A and B. Compared on merge's own
>   rule (a skill by id and requirement, an attribute by value and basis). Where all three
>   agree the item is recorded `ok`, again `by: "model"`; where it differs, `?`. It refuses
>   to run if the labeler prompt has changed since the run, since a disagreement under an
>   edited guide cannot be told apart from a rule change.
> - **`sample`** — the human spot-check, drawn seeded from the three-way-agreed labels and
>   put back to `?` so `apply` cannot pass without it. n=15 of 79, seed 0 — 19% of the
>   agreed pool, the 15–20% HIR-70 asked for.
>
> **What a model decided is recorded as such.** A Golden carries `adjudicated` (fields a
> person decided) and `adjudicated_by_model` (fields the judge or the third labeler
> settled) separately, plus `third_labeler` where one read the posting.
> `seniority_reviewed` / `attrs_reviewed` keep their meaning — a person looked at this —
> so they stay false for anything only a model touched. `apply` counts the spot-check error
> rate over the human sample, not over every agreed label.
>
> **Measured.** judge: ruled 70, agreed with the proposal on **50**, **20** left for a
> person, 0 unusable verdicts. Agreement is judged on the outcome, not the verdict word: on
> an item both labelers agreed on, `ok` resolves to A's value, so `A` and `ok` are one
> decision — comparing words made five of those look like disagreements. third labeler:
> **0 of 79** agreed labels differed (Wilson 95% [0.000, 0.046]) — 63 skills, 8 German, 4
> seniority, 4 degree, 19 postings, 0 failures. Read that 0 for what it is: the accepted
> pool is the labels two models already agreed on, so it says the easy cases are solid, not
> that the answer key is right. The hard cases went to the queue.
>
> **Settled by a person:** all 15 spot-check labels came back `ok`. Of the 21
> judge-vs-proposal splits, the judge was taken on 8, the proposal on 7, and on the six that
> differed only in the quote the shorter quote won three times — `Architektur` alone does not
> name *software* architecture, `deployment` alone does not name *AI* deployment, and
> `ML workflows` is a character shorter than `ML frameworks` but sits in the responsibilities
> list, where rule 4 says it does not count. The three items still `?` sit on the two
> out-of-scope postings, which `apply` skips.
>
> **One label split off from the stack five.** golden_037 `llms` was grouped with the six
> tech-stack labels but is not one: its quote, "GenAI", comes from the candidate profile
> ("You are passionate about the potential of GenAI"), so requirement rule 3 does not reach
> it, and by rule 5 GenAI does not name LLMs while "passionate about" is not a skill demand.
> Dropped. The other five keep the agreed label.
>
> **The five rules sit under LABELING.md, not beside it.** Where a rule the adjudication
> produced and the frozen guide disagree, the guide wins. The judge dropped six of
> golden_037's labels (`aws`, `backend-development`, `evaluation`, `llms`, `observability`,
> `postgresql`) on its rules 1 and 4, for sitting in a "Current Tech Stack" list rather than
> a qualification bullet — but the guide's requirement rule 3 makes an unmarked tech-stack
> entry `required`, and the five rules do not override a frozen guide. Items 90-95 keep the
> agreed label. The judge is not told that precedence, so a verdict leaning on rules 1 or 4
> against a plain stack entry is one to check rather than take.
>
> **Rules the adjudication produced, and that the judge was given verbatim.** Not in
> LABELING.md yet — the guide is not edited mid-run. They go in as one clarification with
> its own entry:
>
> 1. A qualification bullet or sentence that names a skill counts, even if the phrase is
>    broad.
> 2. A title or years-of-experience line does not — "experience *as* a software engineer" is
>    a seniority signal, not a skill; "experience *with* ML systems" is a skill.
> 3. An API being consumed is not `apis`; that is the `llms` criterion. `apis` means
>    building or designing APIs.
> 4. Any required mention wins; `raw_text` quotes the determining mention.
> 5. Responsibilities do not count unless the candidate is also asked for it, and a broad or
>    parent skill the text does not name is not added.
>
> **Still unresolved, carried from the hand pass:** a posting that requires a degree and
> prefers a higher one (golden_036) loses the required level, because `degree` takes the
> highest level named and that mention carries the optional marker. Decided `ok` on the
> guide's letter.

**Supersedes "no model pre-fill for held-out labels" (2026-10-18, above).** That rule was
aimed at one specific failure: a draft pre-filled by the *extractor* anchors whoever labels
it on the answer being measured, so the eval grades the extractor against itself. Hand-
labeling avoided that but capped the held-out split at 4 Goldens, which is too few to gate
a release on (HIR-55). Independent models avoid the same failure without the cap.

The process, `scripts/agent_label.py`:

1. **Pick** ~24 postings, spread across seniority, German/English, source, role family and
   place, including a few "Remote (EU)" ones — remote-EU extraction is unmeasured
   (2026-10-26). Seeded, so the same database and seed pick the same postings. Shares its
   candidate query, dedup (`source_sha256`) and `job_description` construction with
   `scripts/new_goldens.py`, so a labeler sees byte-for-byte what the extractor receives.
2. **Two blind labelers**, each given only `evals/LABELER_PROMPT.md` with `evals/LABELING.md`
   and the taxonomy inlined, plus the posting. Not the extractor's `PRINCIPLES`, not its
   output, not the other labeler's answer, not another Golden. Labeler A is a Claude model
   other than the extractor's; labeler B is another family (OpenAI by default). **The script
   refuses to run a labeler on the extractor's model**, rather than warning: a labeler that
   shares the extractor's blind spots scores its mistakes as correct, which is the one
   failure this whole process exists to prevent.
3. **Auto-check**, deterministic: every `raw_text` and every `*_signal` found verbatim
   (whitespace-normalised, the same rule as `parse_skills`), every `skill_id` in the
   taxonomy, one criterion per `skill_id`, and the field-consistency rules the extractor
   validates (a value needs its basis, `stated` needs a quote, inferred German carries none,
   a null degree nulls its requirement and or-equivalent).
4. **Merge.** A skill is accepted when both labelers gave the same id with the same
   requirement; an attribute when both gave the same value and basis. Everything else goes
   to a review queue, per field and per skill: disagreements, the same quoted phrase mapped
   to two different ids, anything either labeler flagged `uncertain`, and every auto-check
   failure. Nothing is dropped silently. One documented exception: when the value agrees and
   only the quoted signal differs, A's quote is kept and the difference is recorded in
   `summary.json` rather than queued — two correct quotes of one requirement often differ in
   length, and the spot-check covers the rest.
5. **Spot-check** a seeded random sample of the *accepted* labels, at the label level (one
   skill, one attribute — not whole postings), 80 by default. This is the number that
   matters: two labelers can agree and both be wrong, so agreement alone measures nothing
   about correctness. `apply` reports its error rate with a 95% Wilson interval (Wilson, not
   the normal approximation, because at 0 errors in 80 the normal interval is [0, 0]).
6. **Scope.** The queue opens with one `in_scope` item per posting, pre-answered `yes`, so
   leaving it alone keeps the posting. Answered `no <why>`, the posting goes to
   `evals/goldens/excluded.json` with the reason instead of becoming a Golden, and neither
   this script nor `new_goldens.py` picks it again (`existing()` unions both lists, and the
   spent `golden_NNN` number is never reused). This is for a posting that cleared the title
   and city filters but isn't the market we measure — the first run turned up benuta's
   "Senior Performance Marketing Manager – Paid Social & AI". A recorded exclusion beats
   deleting the file afterwards: a silent drop gets re-picked next run and leaves no trace
   of why it is not a Golden.
7. **Apply** the decisions and write the Goldens, with provenance: `labeled_by` (both model
   ids), `adjudicated` (the fields a person decided), `spot_checked`. `apply` refuses while
   any item still says `?`. `seniority_reviewed` / `attrs_reviewed` keep their existing
   meaning — a person looked at this label — so they are true only for a field a person
   decided or spot-checked, never for one accepted on agreement.

**Added 2026-10-30, after the hand pass stalled at 49 of 201 items:** `judge`, `third` and
`sample`, described in the handover above. The two-labeler core is unchanged. What changed is
who settles the queue: a third model rules on each proposal, a third labeler re-reads the
postings behind the agreed labels, and a person reads only the items the models split on
plus a seeded 15 of the agreed ones. The guard that made this safe to automate is the same
one `check_models` already enforced for A and B — `check_extra_model` refuses a judge or
third labeler that is the extractor or either labeler in the run.

Raw labeler responses are cached per posting per labeler, so re-merging after a change to
the merge or check rules costs nothing. Re-merging refuses to overwrite a queue that already
holds decisions.

**Never from this script:** the held-out eval. That stays `run_eval.py --split heldout
--i-am-releasing`, at a release point (2026-10-17).

Measured on the first full run (`20261027T110516Z_label`, 24 postings, A `claude-opus-5-5`
vs B `gpt-6.1-sol`, 0 failures): **skills P 0.932 / R 0.974 / F1 0.953** (tp 301, B-only 22,
A-only 8), requirement 0.993 on shared ids, seniority 24/24, German 24/24, degree 23/24.
243 skills and 62 attributes accepted on agreement; 201 queue items (24 in-scope, 31
disagreement, 65 uncertain, 1 mapping, 80 spot-check). **Spot-check error rate 0 of 15 labels, 95%
Wilson [0.000, 0.204]** — the human sample drawn seeded from the three-way-agreed pool.

### The numbers this process produced (2026-10-30)

Run `20261027T110516Z_label`, 24 postings, A `claude-opus-5-5` vs B `gpt-6.1-sol`, judge and
third labeler `gemini-4-argon`, extractor `claude-sonnet-5-5` (never a labeler).

| what it measures | result |
|---|---|
| labeler agreement, A vs B, skills | P 0.932 / R 0.974 / F1 0.953 (tp 301, B-only 22, A-only 8) |
| labeler agreement, requirement on shared ids | 0.993 |
| labeler agreement, attributes | seniority 24/24, German 24/24, degree 23/24 |
| third labeler vs the agreed labels | **0 of 79 differed**, Wilson 95% [0.000, 0.046] |
| human spot-check of the three-way-agreed labels | **0 errors of 15**, Wilson 95% [0.000, 0.204] |
| adjudication split, fields | **45 decided by a person, 50 by a model** |

Each number answers a different question, and the weakest one is the one that counts.
Agreement measures whether two readers coincide, not whether they are right. The third
labeler's 0/79 is drawn from the pool two models already agreed on — the easy cases by
construction, since every hard one was queued — so it bounds how often three independent
readers of an easy label all err, not how good the answer key is. The spot-check's 0/15 is
the only number where a person read the posting, and its interval is wide: 15 labels cannot
rule out a 20% error rate. Treat the key as good enough to gate a release and not as
settled; the interval narrows only by a person reading more labels.

### Held-out eval at the release point

`run_eval.py --split heldout --i-am-releasing --repeats 3`, run `20261030T123219Z_heldout`,
26 Goldens (the 22 new plus the 4 hand-labeled), extractor `x2-2e0cac6944`, taxonomy v4,
0 errors. Next to the dev run on the same extractor and taxonomy (`20261029T122622Z_dev`,
20 Goldens, 3 repeats), means over three repeats:

| metric | held-out (26) | dev (20) |
|---|---|---|
| precision | **0.952** | 0.881 |
| recall | **0.888** | 0.967 |
| F1 | 0.919 | 0.922 |
| requirement accuracy | 0.968 | 0.989 |
| seniority accuracy | 0.962 | 0.817 |
| German accuracy | 0.962 | 1.000 |
| degree accuracy | 0.949 | 0.950 |
| rank Spearman | 0.933 | 0.914 |
| top-10 overlap | 0.667 | 0.800 |

**F1 holds across the split (0.919 vs 0.922), but the two halves swap.** Held-out precision
is 7 points higher and recall 8 points lower. That is what the two answer keys are: the
agent-labeled held-out key is more generous than the hand-labeled dev key — 315 skills over
22 postings, about 14 each — so the extractor's own output is a subset of it more often, and
what it misses is what the key adds.

**The misses name the adjudication's own decisions.** The three most-missed skills over the
three repeats are `ai-deployment` (19), `ai-ml` (18) and `software-engineering` (16) — the
broad, inferred-from-a-phrase labels the queue argued about most, including golden_037's
tech-stack labels kept on requirement rule 3 against the judge's `drop`. Recall on the
held-out split is therefore partly a measure of a labeling policy the extractor was never
given: the labelers were asked to label what the text names, the extractor is told not to
add parents, and the gap shows up as recall. **No prompt or taxonomy change on the strength
of this run** — a held-out result is not a tuning signal (2026-10-17), and whether that
policy gap is the key's fault or the prompt's is its own decision, with HIR-72's unmapped
triage next to it.

**`production_accuracy` 1.000 is not a result.** Only 4 of the 26 held-out Goldens carry a
production label at all (support: 1 `nice_to_have`, 3 `none`, 0 `required`), all four from
the hand-labeled originals. The agent labelers were not asked for that attribute, so it is
effectively unmeasured on this split.

That spread is the argument for insisting labeler B is a different family. A smoke run with
two Claude models (`claude-opus-5-5` vs `claude-fable-5-1`) agreed on 43/43 skills and all 6
attributes — F1 1.000, zero disagreements — and flagged the same 8 items uncertain. Two
correlated labelers produce a clean number and measure nothing; the cross-family pair
produces 31 real disagreements to adjudicate.

With those adjudicated and the spot-check recorded, **the held-out split is a release gate**
(HIR-55): 26 Goldens, provenance per label, and an error rate with an interval on it.

**Scope calls on that run: two postings out, two kept on purpose.**

- **Out**: golden_048 (benuta, "Senior Performance Marketing Manager – Paid Social & AI") — a
  marketing role, outside the AI/data engineering scope. golden_039 (Arbeitsagentur, "AI
  Engineer Team Lead") — 382 characters, a search-result teaser rather than a posting, below
  the same 400-character floor `queries.MIN_TEXT_CHARS` uses to keep fragments off the chart
  (2026-10-21). Both are recorded in `evals/goldens/excluded.json` with those reasons.
- **Kept on purpose**: golden_030 (SAP AI Lead Architect, 5.7k characters, 2 accepted skills)
  and golden_038 (Intercom Staff Product Engineer, 7.7k, 2 accepted skills). Both are full,
  in-scope postings whose content is mostly outside the taxonomy — SAP BTP / Joule / Business
  AI, inference-stack vocabulary. A held-out set holding only postings the taxonomy already
  covers would hide the gap it exists to measure, so a low skill count is a taxonomy signal,
  not a bad Golden. **In-scope is about the job, not about how much of it we can currently
  label.**

The 216 unmapped labels the run collected are triaged in **HIR-72**, after labeling, not
during it: `taxonomy/skills.json` is inlined into the labeler prompt, so editing it mid-run
changes what the labelers were asked and invalidates the cache.

**Found during adjudication, both worth keeping:**

- **An agreed-and-wrong, caught by the `uncertain` flag rather than the spot-check.**
  golden_044 says "hands-on TypeScript skills; Python experience is useful." Both labelers
  made `python` **required**; "is useful" is an inline optional marker with the force of the
  guide's listed "is an advantage", so requirement rule 2 overrides the heading and the
  label is `nice_to_have`. Adjudicated as an override. Agreement would have shipped this
  silently — which is the argument for queueing every `uncertain` flag even when both
  labelers agree, not only the disagreements.
- **A guide gap, left as written for now.** golden_036 requires a degree and prefers a
  higher one: "Du hast einen Abschluss in Informatik…; ein Master oder Ph.D. ist von
  Vorteil." LABELING.md says `degree` is *the highest level named* and `nice_to_have` only
  when that mention is marked optional, so the correct label by the guide is
  `phd` / `nice_to_have` — a posting that does require a degree ends up labeled as not
  requiring one. Both labelers applied the rule correctly; the rule loses the required
  floor. Decided `ok` on the guide's letter and recorded as **clarification candidate #4**,
  to be settled after HIR-70 with the three rules the disagreements produced (a
  qualification bullet that names a skill counts; a title or years-of-experience line does
  not; an API being consumed is not `apis`). LABELING.md is not edited mid-run.

**Queue order.** Items are grouped by what they ask of the reviewer, in working order:
in-scope, disagreements, uncertain, mapping, then the spot-check sample last. A spot-check
prints the posting excerpt and the agreed label with no `A:` / `B:` lines — both labelers
said the same thing there by construction, so showing them twice only invites agreeing with
them. The question a spot-check asks is whether the posting supports the label.

---

## 2026-10-27 — LABELING.md: broad vs specific skills written down, no relabel (HIR-70)

`evals/LABELING.md` is frozen, so this records the edit. Before the HIR-70 labelers run, the
guide had no rule for broad-vs-specific skills (`cloud` over `aws`, `llms` over `rag`,
`containerization` over `docker`), while the extractor did (`PRINCIPLES` rule 3). A labeler
reading only the guide could reasonably have added parents the posting never names, which
would have scored the extractor against a rule it is not given.

Added a "Broad and specific skills" subsection: label each when the text names both, never
add a parent the text does not ask for, and the broad skill's own `raw_text` must name it.

**No Golden relabel, because this documents existing practice.** Checked all 20 dev Goldens:
every labeled broad skill is itself named in its `raw_text` (`cloud` from "cloud platforms
(GCP, AWS, or Azure)" in golden_001), and no Golden carries a parent the posting does not
name (golden_001 has `docker` without `containerization`). Stored eval results stay valid.

Two dev Goldens are *missing* a broad label the posting does name, which the new wording
makes visible. Left as they are, not fixed in this change:

- golden_003: tech stack reads "LangGraph & related LLM orchestration tools"; `langgraph` is
  labeled, `llm-orchestration` is not.
- golden_013: "Serious experience using AI development tools such as Claude Code, Codex,
  Cursor, Copilot"; the four tools are labeled, `ai-developer-tooling` is not — golden_009
  labels `ai-developer-tooling` from the same shape of phrase, so the two disagree.

Both are false negatives in the answer key, so they cost the extractor precision on a
correct answer. Fixing them is a relabel and therefore its own release decision.

(Also noted, not a labeling question: `apache-spark` has no "Spark" alias, so golden_011's
"Spark/PySpark" resolves only by display name.)

---

## 2026-10-26 — EU-remote postings are collected as the place "Remote (EU)"

Chandler applies to any remote job he can take from Berlin, and /check-url rejected one
(Kake, "Senior AI/LLM Engineer (Python) - Remote": no JSON-LD, so no location, so "no
tracked city"). Until now geo dropped every remote posting on purpose (2026-10-16 below).

- **One extra active place, `geo.REMOTE_EU = "Remote (EU)"`,** stored in `job.city` like a
  city, so the dashboard filters it and the skills of remote roles stay separable from
  Berlin's. A city match wins ("Berlin or remote" is Berlin).
- **What counts:** a remote location naming an EU-wide region or Germany (Europe, EU, EEA,
  EMEA, DACH, CET/CEST, Germany, Deutschland, bundesweit), or naming no region at all
  ("Remote", "Anywhere") unless the description restricts residence to a non-EU country
  ("must be located in the US", "authorized to work in the US", "US only").
- **What doesn't:** remote tied to one other country ("Remote – Spain", "Remote, US",
  "Remote (UK)"): those usually need residence or an employer entity there. Revisit if the
  url_check log shows many of them worth having.
- **Empty location** (careers pages without JSON-LD): the title's remote part, then strong
  description phrases ("fully remote", "remote-first", "work from anywhere"). Plain
  "remote" in a description is not enough: hybrid postings mention remote days.
- **Sources now carry their remote flag into `location_raw`:** JSON-LD `TELECOMMUTE` +
  `applicantLocationRequirements`, arbeitnow `remote` (German board → "(remote, Germany)"),
  startup.jobs `workplace_type`, JSearch `job_is_remote` + `job_country` (field name from
  JSearch docs, not yet in a recorded fixture). JOIN already did.
- **Accepted risk:** a bare "Remote" on a US company's board with no residence sentence in
  the JD gets in. Time-zone overlap ("5h with PST") is not treated as a residence rule.
- **Extraction caveat:** the Goldens are all Berlin postings; extraction quality on
  remote-EU descriptions is unmeasured, the same caveat as SF.

Compare mode stays Berlin vs San Francisco; "Remote (EU)" is a filter button.

---

## 2026-10-21 — Host on a GCP Compute Engine VM, not Railway (HIR-29)

Decision: one e2 VM in europe-west3 (Frankfurt) runs FastAPI plus the built `web/dist`
behind Caddy, which terminates HTTPS and holds the basic-auth gate. The daily poll becomes
a systemd timer on the same box; SQLite is backed up nightly to a GCS bucket; deploys go
through GitHub Actions. No domain yet, so the host is an sslip.io name (the VM's IP spelled
into a hostname), which is enough for Caddy to get a certificate. The full plan is in HIR-29.

Why: this is a portfolio project, and the hands-on DevOps — running the box, the ops around
it, and CI/CD on a major cloud — is the point. A managed PaaS hides exactly the parts worth
learning.

Rejected: **Railway** (the 2026-10-16 plan) — it works and costs about the same, but it does
the ops for you. **Cloud Run** — the container filesystem doesn't persist between revisions,
so SQLite would have to be replaced with a managed database. **GCP's free-tier e2-micro** —
US regions only, and EU hosting was chosen, so this is a paid VM.

This supersedes the "hosted on Railway" and "Railway cron" lines in the earlier entries
below. Those entries stay as written; the log is a record, not a current-state document.

## 2026-10-21 — The extractor sees the job title (HIR-57)

`extract_pending` sent the model `description_text` only. Every feed adapter keeps the title
in `job.title`, so for feed jobs the model never saw "Senior …", "Junior …" or "Werkstudent …",
which LABELING.md treats as the strongest seniority signal. The dev Goldens all open with
their title (screenshot and legacy origin), so the dev seniority score (0.82–0.85) measured
an input production never sent.

Decision: `extract.extraction_input(title, text)` puts the title on top, unless the text
already opens with it. `INPUT_FORMAT` is part of `extractor_version`, so this re-extracts
every job. `new_goldens.py` drafts with the same input; `source_sha256` still hashes the
stored description, because that is the dedup key against the DB.

Held-out Goldens built from feed text had no title line. golden_021 (Almedia) now opens
with "Junior Data Scientist", and that title is its seniority signal (it was the indirect
"Most Junior Data Scientists…" sentence). 022–024 need the same treatment from their job
rows. This is an input-format fix, not tuning, so the held-out edits are allowed.

## 2026-10-21 — Jobs with under 400 characters of text are left out of the chart

After the taxonomy v4 re-extract, four jobs had zero skills: 37 Enpal, 38 eduBITES, 39 POS
TUNING (old screenshot imports) and 43 Mercanis, each with 249–343 characters of stored
text. That's a fragment, not a posting: the screenshot transcript was cut off (HIR-9) or a
teaser was stored. They still counted in the chart's denominator, so every share was
slightly low.

`queries.MIN_TEXT_CHARS = 400`: below that a job is out of skill frequencies and city
totals, like legacy imports, and the job list shows it greyed as "short". Re-adding the full
posting by link or text replaces it through dedup. 400 sits well below any real posting
(the dev Goldens are 1,500+) and above every fragment seen so far.

## 2026-10-20 — Taxonomy v4: proposed-skill batch; a label earns an entry at 3 jobs

First review of the proposed-skill queue: 247 labels, 387 rows, 88 jobs; 182 labels in a
single job. Added 56 entries (taxonomy v4, 200 skills): everything in 2+ jobs once spelling
variants merge (MLflow 12, Infrastructure as Code 11, Kubeflow 10, Feature Engineering 9,
NLP 8, Terraform 8, Rust 7, Statistics 7 …), plus `etl` as an alias of data-pipelines.
Bare "Triton" left out: ambiguous between NVIDIA's server and OpenAI's language.

Rule from here: a proposed label becomes a taxonomy entry once it appears in **3 jobs**.
Below that it stays pending; the queue is the frequency counter. Reject only what isn't a
skill under taxonomy/README.md (domain knowledge, marketing analytics terms, vague words).
Rejection is now sticky: `store_extraction` skips any label already rejected, so
re-extraction doesn't re-queue it.

Goldens updated for the new entries (a label the taxonomy couldn't express before is a
missing gold label now): 001 devops (nice); 022 statistics (req), causal-inference, r-lang,
rust (nice); 023 kafka (req); 024 nlp (nice). Taxonomy-driven, not tuning, so the
held-out edits are allowed.

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

## 2026-10-19 — Reposts: only when the earlier listing is gone from a complete board

A repost is a job taken down and posted again under a new id. Ingest used to count one
whenever the matched job already had a different id from the same source. That also fired
when one board listed the same job twice at the same time: Nebius had "Senior Applied
Scientist, Efficient LLM Inference & Model Optimization" up under two Greenhouse ids. Ingest
merged them into job 169, correctly, but also set repost_count=1.

- **Rule.** A merge counts as a repost only when (a) the source is a board feed (Greenhouse,
  Lever, Ashby, JOIN; `ingest.REPOST_SOURCES`), (b) the job already has other ids from that
  source, and (c) none of them is in the current fetch. `ingest()` passes the fetch's id set
  down, so the order within a batch does not matter. If any earlier id is still listed, the
  new id is a concurrent duplicate. It merges and does not count.
- **Why only boards, and narrower than the open rule's FEED_SOURCES.** A repost needs proof
  that the earlier listing went away, so it needs a fetch that lists everything. A board
  fetch returns the company's whole board. JSearch and the Arbeitsagentur are samples
  (2026-10-18 open-rule entry). startup.jobs is a search query over the last 14 days, with
  unstable paging. Arbeitnow is capped at `max_pages`. For none of these does a missing id
  mean a takedown. The open rule still counts startup.jobs and arbeitnow as complete feeds.
  This entry leaves that unchanged.
- **Manual adds** (url / paste / screenshot, and `check --add`, which hands `ingest_one` a
  single board posting) have no fetch around them, so they never count as reposts.
- Data: job 169's repost_count was set back to 0. It was the only job with reposts, so no
  other job needed fixing.

## 2026-10-19 — Active cities: Berlin only until the held-out eval passes

The plan said SF collection starts only after Berlin extraction passes the held-out eval
("Second city", below). The code never held to that. `app/geo.py` has tracked San Francisco
since the intake build (32c43c5, 2026-10-16), so every poll kept SF postings. Nobody chose
that on purpose. It surfaced when discover-boards listed SF-heavy boards (OpenAI, Anthropic):
208 SF roles against 33 Berlin.

- **Tracked vs active.** `geo.CITIES` still recognizes San Francisco, and manual adds keep
  their real city. Only `geo.ACTIVE_CITIES` (`("Berlin",)`) passes the ingest filter and
  discover-boards' relevance check, through `geo.active_city`. `check` names a tracked but
  inactive city in its diagnosis.
- **Turning SF on** is a one-line change to `ACTIVE_CITIES`. Make it deliberately, once
  the held-out eval passes. Also check extraction on SF descriptions then: every Golden is a
  Berlin posting.
- Job 140 (Intercom, SF, polled 2026-10-19) predates this change and stays in the DB. Polls
  now skip its posting, so it is no longer marked as still listed.

## 2026-10-19 — San Francisco collection starts now (replaces the "Second city" gate)

The plan said SF collection would start only after Berlin extraction passed the held-out eval
("Second city", below). The code never held to that: `app/geo.py` has tracked San Francisco
since the intake build (32c43c5, 2026-10-16), so every poll already kept SF postings. Nobody
made that call on purpose, and it went unnoticed until discover-boards listed SF-heavy boards
(OpenAI, Anthropic). The person decided to keep it: collect SF from now on.

- No code change. The city filter stays as it is.
- Before SF counts are compared with Berlin, check extraction quality on SF job descriptions
  too. The Goldens are all Berlin postings.

## 2026-10-19 — discover-boards: find new company boards by `site:` web search, add by hand

Board feeds (Greenhouse, Lever, Ashby, JOIN) each cover one company, and none of those
services lists the companies using it. So a company we have never heard of stays invisible:
Pipedrive, Intercom and Rematiq were all misses until someone pasted a link. The search
feeds can't fill the gap. Measured: 0 of the feed rows in `job_source` point to a
greenhouse/lever/ashby page (they link to arbeitsagentur.de, arbeitnow, StepStone, LinkedIn).

- **`site:` search over the hosted ATS domains** (`site:jobs.lever.co "AI engineer" Berlin`)
  finds pages that name a board. A manual test on 2026-10-19 found 3 boards: 2 had current
  Berlin AI roles (bluefishai on Greenhouse, vestiairecollective on Lever) and 1 was stale
  (cortea on Ashby: the indexed posting was gone and no live Berlin role passed the title
  filter). Search hits are leads, so every board is fetched live and judged by ingest's
  own title and city filters before it is reported.
- **Approval is manual** (`--add` / `--reject`). A board joins the daily poll, and its
  jobs reach the chart, only after a person looks at it. A rejection is written to
  `config/boards_rejected.json` with its reason so it is not suggested again.
- **Brave Search, not Google.** Google's Custom Search JSON API is closed to new sign-ups
  and retires on 1 Jan 2027. Brave's web search API supports `site:`, costs $5 per 1,000
  searches with $5 of monthly credit, and a run is domains × queries searches (10 by
  default).
- JOIN's own site-wide job sitemap is behind bot protection (403 for scripts). We don't work
  around that; `site:join.com/companies` is in the search domains instead.

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
Goldens. `scripts/new_goldens.py --german N` drafts unlabeled held-out Goldens from them;
run_eval skips files marked `draft`. The no-model-pre-fill rule stated here was superseded
on 2026-10-27 (two blind labelers, below) — the rule it came from, that a held-out label
must not be anchored on the extractor's own answer, still holds.

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
  (`app/geo.py`). Remote-only and untracked-city postings are dropped (remote: superseded 2026-10-26). Manual adds skip
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
