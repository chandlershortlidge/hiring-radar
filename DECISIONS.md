# Decisions Log

What we decided, why, and what we tried that didn't work — so nobody (person or agent)
re-treads a dead end or undoes a decision without knowing the reason. Newest first.

---

## 2026-11-12 — The caretaker runs on the VM as plain code, report-only first (HIR-257)

Chandler, 12 Nov: "we need more agents to notice this stuff and just deal with it." The
caretaker checks every job source each morning after the 07:00 poll, fixes the routine
breakages (a company board that moved, a board gone empty) and reports once a week.

**Where it runs: a systemd timer on the VM, not a GitHub Action or a cloud task.** The
issue offered those two. Both run somewhere without the database, and every check reads
what the poll actually got — which lives only in the SQLite file on the VM. The VM already
runs the poll and the backup this way and already holds the Brave key the board search
needs. Undo: delete the timer; nothing else depends on it.

**Plain Python, not an AI agent.** Every check is a rule over numbers the poll already has
(errors, posting counts, field lists, city totals), and the board search reuses the
discovery code. Plain code makes no model calls, cannot edit its own rules or anyone
else's, and every "never does" line is a test rather than an instruction a model might
skip. Undo: put an agent around `app/caretaker.py` later; the rules stay the same.

**The rules it applies** (constants at the top of `app/caretaker.py`):

- A company board is *dead* when it errors or returns nothing, it gave us postings before,
  and the newest of them was last seen 3 or more days ago. A board that answers 404/410 is
  *gone* at once. Either way the caretaker first searches for the company's new board.
- A new board counts as *the same company* when the company name and the board token
  match after dropping case, spaces and punctuation, and it has at least one posting the
  poll would keep. Found → switch the board's token; the stored jobs are untouched.
- Dead and no new board found → pause: `enabled: false` plus a `paused` note in
  `config/feeds.json`. The entry stays. Paused boards are re-checked every Monday and
  switched back on when they have a posting we would keep. A board a person disabled (no
  `paused` note) is never switched on.
- A country-wide feed or search is *low* when it returns under half its median over its
  last 5+ good runs. Reported only.
- A city is *dropping* when its open-job count falls by more than 30% overnight from at
  least 20. Reported only.
- Model-call spend is zero; Brave searches are counted at €0.005 each against a €0.50
  daily cap. The cap is checked before every search; hitting it stops the search and is
  reported at once.

**Report-only for the first week**, as the issue asks: it writes what it would have done.
Acting mode — applying the feeds.json change through a pull request — is a separate step.

**Built in two halves.** The append-only log the weekly summary reads needs a new
migration, and an open PR (#146) already adds one; migrations are one branch at a time,
so the log, the timer and the poll's per-feed record waited for #146 to merge (it did,
12 Nov).

**The record and the log.** The poll now keeps one row per feed per run (`feed_run`:
worked or not, postings seen, fields carried); until now it printed this and forgot it,
so "silent for three days" could not be asked. The caretaker writes every finding to
`caretaker_log`. Both are append-only, enforced by the database as for the extraction log.
A city's "yesterday" count is the dashboard's open rule evaluated 24 hours earlier on
today's data, so no daily snapshot table is needed.

**When it runs and how it reports.** A timer at 10:00 Berlin: three hours after the poll
starts, so the poll's readings are normally done (a reading still running then shows up
as "jobs still waiting to be read", which is the half-finished case the issue asks to
notice anyway). On Mondays it posts last week's summary as one Linear issue in the
Hiring-radar team; the collection down two days running or the spending cap hit is posted
at once, at most once a day. With no `LINEAR_API_KEY` on the server it writes the text to
its journal instead. Undo: disable the timer.

## 2026-11-11 — Taxonomy v11: 27 entries from the queue after the German launch; the bar counts distinct postings (HIR-219)

The queue was re-read from the live site's backup of 11 Nov 02:30Z (916 jobs, all but
four at the current extractor stamp, so the HIR-128 caveat about stale stamps does not
apply): 504 pending suggestions, 366 labels once case, punctuation and parentheses are
normalised. Thirty reach the 2026-10-20 bar of 3 jobs counting rows.

**The bar counts distinct postings, not stored rows.** Three pairs of rows are one
posting each, stored twice because the company was spelled two ways or the title
changed slightly: Zeta Global / zetaglobal ("Senior Data Scientist, Data Cloud
Acceleration", jobs 167 and 357), Control Risks / Control Risks Group Holdings ("AI
Engineer", near-identical text, 813 and 908), and Botgenossen's "KI Entwickler / AI
Engineer" (378 and 799). Counted once, **AWS Glue, Power Platform and Neo4j are at 2 and
stay pending.** Caspar Health's backend role (228, 293, and an aggregator's copy, 289)
is also one posting; Ruby on Rails is counted with it once and stays over the bar.
Hamburger Energienetze's 360 and 832 are two different roles and both count. The rule is
the bar's own purpose — frequency, independent evidence — as applied in HIR-128 ("4
distinct postings") and HIR-108 (same company and title is the same posting, judged by
reading, not by the matcher's threshold). The stored rows are left alone; deleting jobs
is a stop-list item, so the missed duplicates are a follow-up ticket.

**27 entries land, v11, 244 skills.** With their distinct-posting counts and parents:

- Microsoft and Azure: `azure-ai-foundry` 5 [azure], `microsoft-entra-id` 5 [azure,
  active-directory], `azure-key-vault` 4 [azure], `azure-devops` 3 [azure, ci-cd],
  `azure-ai-search` 3 [azure, vector-search], `microsoft-fabric` 3 [azure], `power-bi` 3
  [business-intelligence], `dotnet` 3, `semantic-kernel` 3 [llm-orchestration].
- Web and backend: `angular` 6 [frontend-development], `ruby-on-rails` 5 [ruby], `ruby` 4,
  `nestjs` 4 [node-js], `mongodb` 3 [nosql], `oauth` 6 (with the "OAuth 2.0" and
  "OAuth/OIDC" spellings merged).
- Platform and delivery: `jenkins` 4 [ci-cd], `argocd` 3 [gitops] ("ArgoCD" and "Argo CD"
  merged; bare "Argo" stays pending, it can mean Argo Workflows), `openshift` 3
  [kubernetes], `playwright` 3 [testing], `bazel` 3, `hadoop` 3, `secrets-management` 3
  [devsecops].
- Training and models: `megatron-lm` 4 ("Megatron" merged) [distributed-training], `fsdp`
  3 [distributed-training], `slurm` 4 [ai-infrastructure], `transformers` 3
  [deep-learning], `pydanticai` 3 [agents].

Whether platform and web tooling belongs on an AI-engineering chart is not a separate
test: taxonomy/README says a skill is a language, framework, tool, platform, technique or
practice a job can ask for, and 2026-10-20 says the queue's count decides. Every one of
these was asked for by AI-titled postings.

**Judgment calls.** `microsoft-entra-id` is its own entry with `active-directory` as a
parent, not an alias of it: Entra ID is the cloud identity service once called Azure AD,
and "Active Directory" on its own usually means the on-premises directory; aliases are
for the same thing spelled differently. "Azure AD" and "Azure Active Directory" are its
aliases. `transformers` is the model architecture ("transformer-based architectures",
"transformer"); the Hugging Face library is covered by `hugging-face`, and
"sentence-transformers" is left pending. `fsdp` lands here rather than under HIR-131,
because this ticket's brief is everything at the bar (the HIR-72 `opentelemetry`
precedent); Datadog is at 2 and HIR-131 stays open for it. `ruby-on-rails` takes `ruby`
as its parent, as `spring-boot` sits under `java`.

**Scrum is rejected**, though at 3: it was ruled a working method, not a skill, on HIR-72
(2026-11-01). That is about what it is, not how often it appears. This change does not
touch the database: its three pending rows are rejected from the review queue on the live
site, which also keeps the label from being re-queued.

**Seven held-out Golden labels added to five Goldens**, on the 2026-10-20 precedent that
a label the taxonomy could not express before is a missing gold label, not tuning:
golden_029 `jenkins`, `azure-devops`, `playwright` (required, "Ihr Profil"); golden_035
`transformers` (required, "Must-haves"); golden_038 `ruby` (required, an example language
beside the already-labelled Python and JavaScript); golden_046 `oauth` (nice to have,
"wünschenswert"); golden_047 `dotnet` (required, beside the labelled C#). Not labelled:
golden_028's PydanticAI and golden_038's Rails app and "transformer neural networks", which
sit in the responsibilities or the company description (LABELING.md).

Merging re-reads 163 of 722 open postings once, about €1.17, measured by
`reread-cost` against the same backup (HIR-224 keeps the other 559 readings).

## 2026-11-11 — Adding skills re-reads only the postings that name them; "current" can mean "carried over" (HIR-224)

Any edit to the skill list changes the extractor's version stamp, and since HIR-195 a new
stamp re-reads every open job — 722 of them, about €5.19, on the live database today. Most
skill-list edits are a batch of accepted suggestions (HIR-128, HIR-219), and a skill that
was just added can only change the reading of a posting whose text names it. Chandler's
yes on the ticket (9 Nov).

**What triggers a targeted re-read.** The old stamp and the new one must differ *only* in
skills or spellings added to the skill list. Everything else the stamp covers — the
prompt's rules, the tool schema, the model, the input format, the layout of the skill list
in the prompt — must be identical, and every skill the old list had must still be there
with the same display name and at least the same spellings. Anything else (a skill
removed, renamed, a spelling taken away, any prompt change) re-reads every open job, as
before. Changing a skill's *parents* never touched the stamp — parents are not in the
prompt — so that is unchanged too.

**What gets re-read.** An open job whose title plus posting text (what the model is sent)
contains one of the new names, case-insensitive and word-bounded: every new skill's id,
display name and aliases, and every alias added to an existing skill. Matching is generous
on purpose: an extra re-read costs under a cent; a missed one leaves a skill off a
posting.

**The alias gap, closed from the suggestion queue (Chandler, 11 Nov).** The model can
resolve a skill from wording that contains none of its names ("transformer-based
architectures" for Transformers). So a job is *also* re-read when the queue of skills the
model has suggested holds a pending suggestion of an added skill for it — the new skill
list resolves the suggested label, or the label contains one of the skill's names —
whatever words the posting used. And `reread-cost` lists, per added skill, the model's own
labels and quotes from those suggestions (across the whole queue) that the entry does not
yet catch: short ones only, none that already contain one of the skill's names. They are
offered as aliases in the PR, never added by themselves. What remains uncaught is a
posting that names the skill only in other words *and* was never given it as a
suggestion; it gets the skill at its next full re-read.

**What "current" means for a carried-over job.** `job.extracted_version` keeps its meaning
— "this job needs no reading at this version" — and the job is moved to the new stamp
without a model call. A new column, `job.read_version`, says which version actually
produced its skills, so no row claims a reading that never happened: a carried-over job
shows the old stamp there, its skill rows keep the stamp they were written under, and the
reading log is untouched. A job read in full gets the same value in both columns.
"Stored extractions with no logged reading" now checks `read_version`, since that is the
reading the log should hold.

**How the old skill list is known.** A version stamp is a hash, so the skill list behind
it cannot be recovered from it. The app now records, for every version it runs under, the
skill list the prompt carried and a hash of everything else (a new table,
`extractor_snapshot`). It records on every extraction run and when the dashboard process
starts, so the version live before a skill-list merge is recorded by the deploy of this
change or any later poll. A stamp with no recorded snapshot — e.g. a database restored from
before this change — re-reads in full: the safe direction. "Everything else" is the stamp
of the same code with a fixed one-skill list, so any new ingredient a later change adds to
the stamp is covered without anyone remembering to add it here.

**The re-read cost follows.** `reread-cost`, run on a branch with a skill-list change,
counts only the jobs that branch would really re-read. It knows the old list from the
database's snapshots, or, if the database has none for that stamp, from `origin/main`'s
skill list in git. On a branch with no extractor change it prints the full figure, as
before, labelled as what a change other than added skills would cost.

**The eval gate is unchanged**: any edit to the skill list still needs the dev eval, which
reads its own Goldens and has nothing to do with which stored jobs are re-read.

To undo: revert the HIR-224 commits; migration 019's column and table can stay, nothing
else reads them, and every open job behaves as before on the next version change.

---

## 2026-11-10 — The key alone turns tracing on; `LANGSMITH_TRACING` is no longer needed too (HIR-238)

With the HIR-236 flush fix deployed and `LANGSMITH_API_KEY` set, the next poll still sent
nothing to `hiring-radar-live`. `langsmith.trace` only posts a span when it reads
`LANGSMITH_TRACING=true` (or `*_TRACING_V2`) from the environment — a second switch,
separate from the key, that `langsmith_live.enabled()` never checked and the README never
mentioned. Adding `LANGSMITH_TRACING=true` to `/etc/hiring-radar.env` by hand made the
17:17 poll's trace arrive, confirming that was the whole gap.

**`langsmith_live.run()` forces the SDK's switch on for its own duration, via
`langsmith.tracing_context(enabled=True)`, whenever the key is set.** That context is
ambient (the same mechanism nesting already relies on), so it covers the run span, every
job span opened inside it, and the model-call span `wrap_anthropic` opens under each job —
all without touching `LANGSMITH_TRACING`. Undo: delete `_force_enabled` and the `with
_force_enabled():` around `run()`'s body in `app/langsmith_live.py`.

**Not `enabled=True` on `langsmith.trace()` itself**, as a first reading of the fix
suggested: the installed SDK's `trace()` has no such parameter — passing one lands in
`**kwargs`, which only warns and is silently dropped, so tracing would have stayed exactly
as broken. `tracing_context` is the SDK's real override point.

The VM's `/etc/hiring-radar.env` keeps `LANGSMITH_TRACING=true` from the manual workaround;
it is harmless now, just redundant. `deploy/README.md`'s "Tracing the poll" section says so.

---

## 2026-11-10 — Every run flushes its own client before the trace can be lost (HIR-236)

The 07:00 poll on 10 Nov ran with tracing on and the package installed (HIR-233), read 5
jobs, and printed no warning — yet nothing reached `hiring-radar-live`. LangSmith's SDK
sends a run from a background thread; the poll is a systemd oneshot, so the process exited
and killed that thread before it had sent anything. A manual trace on the VM, made the same
way but followed by an explicit `client.flush()`, did arrive — the queue was never the
problem, only the missing wait for it to drain.

**`langsmith_live.run()` flushes the run's own client when the trace closes, capped at 30
seconds.** One place, because every live caller — the poll, a re-read, add-by-link, a
backfill — already opens its run through this one function; fixing it there means no
caller has to remember to flush, including the ones not written yet. The 30-second cap is
so an unreachable LangSmith delays a run, never hangs the 07:00 timer. Undo: delete
`_flush` and the call to it at the end of `run()` in `app/langsmith_live.py`.

**The flush goes through the same `_safe` net as everything else here.** HIR-160's
invariant is that no LangSmith problem fails a run; a flush that times out or raises prints
`[langsmith] flush failed, continuing without it` and the run's result is unaffected. Undo:
call `run_tree.client.flush(...)` directly, outside `_safe`.

A test gives the run a fake client and checks flush is called exactly once, with the capped
timeout; another makes that fake client's flush raise and checks the run still succeeds.

---

## 2026-11-10 — A labelling run never overwrites another run's Goldens (HIR-167)

Every labelling run numbers its picks from the highest Golden that existed when the run
started (`new_goldens.existing()`). Two runs begun before either applied therefore claim
the **same ids for different postings**. The two batches of 3 Nov were started five
minutes apart and both numbered `golden_049`–`golden_063`; the three runs of 8 Nov all
start at `golden_049` as well. `apply` wrote each Golden by id with no check, so the
second run to apply would have overwritten the first's fifteen Goldens with fifteen
unrelated postings. Nothing would have said so: the only symptom is a Golden set smaller
than expected, which is exactly the number HIR-167 was growing.

**`apply` refuses when a Golden on disk holds a different posting.** Compared by
`source_sha256`, not by id, so the ordinary loop — fix a decision, run `apply` again —
still overwrites the same posting as before. The refusal names each clash, both companies
and the next free id. It runs *before* the "every item is decided" refusal, because the
clash is a property of the run's numbering and not of its decisions: discovering it after
someone has worked through 157 items is the cost the refusal exists to save. Undo: drop
the `taken` block in `cmd_apply`.

**The Berlin batch of 3 Nov was renumbered to `golden_064`–`golden_078`**, leaving the New
York batch on `golden_049`–`golden_063` where it sits as the earlier of the two. Ids were
shifted in `picks.json`, `items.json`, `merged.json`, `summary.json`, `summary.md` and the
`## N. golden_NNN` headings of `review_queue.md`, and the 30 files in `raw/` were renamed;
their contents carry no ids. **The decisions already written into the queue were not
touched** — they are keyed by item number, which no part of this changes, and the
renumbering asserted the parsed item-number-to-decision map was identical before and
after. This is why renumbering happens *before* a queue is finished rather than after.

**The clash had already reached the label store.** `test_the_real_run_folders_all_import`
asserted that the 3 Nov runs held 15 postings with five labeller answers each. They hold
30 postings; the "five answers" were three from New York plus two from Berlin, on two
unrelated postings that shared an id. The test now asserts 30 distinct ids and that no id
carries answers from both runs. Rows in `label_answer` were never lost — the run is part
of the key — but any count or join by `golden_id` alone was merging the two batches.

**Not renumbered: the three runs of 8 Nov**, which still share `golden_049`–`golden_063`
with the New York batch. They belong to the next batch of this work (HIR-168) and `apply`
now refuses rather than destroying anything.

**Chandler's decision, 2026-11-09**, asked because the ticket's own step 2 would have
destroyed half its input: renumber the clashing batch, and make the command refuse to
overwrite an existing Golden so this cannot happen again.

---

## 2026-11-09 — One pinned Python everywhere, and the VM installs wheels only (HIR-235)

The deploy of HIR-233 failed on the VM: `uv` tried to compile `zstandard` from source and
there is no `cc` on the instance. The project only ever said "Python 3.12 or newer", so
`uv` on the VM picked the newest it could find — 3.15, released days earlier — and the
first dependency without a 3.15 wheel broke the install, after the pre-deploy backup and
before the restart. Local machines were on 3.12 and CI on 3.13, so neither saw it.

**`.python-version` pins 3.13 for every environment, and `requires-python` is capped at
`<3.15`.** One version across local, CI and the VM, and the cap means an unattended
installer can never again choose a Python nobody has run this on. 3.13 because CI already
used it. Undo: delete `.python-version` and drop the upper bound — and accept that the VM
chooses its own Python again. The floor stays 3.12 so nobody's existing environment is
invalidated by this change alone.

**The VM gets no compiler.** The alternative fix was `apt-get install build-essential` on
an instance with 969 MB of RAM, which would have it compiling C on every lockfile change.
A pinned Python with wheels is cheaper and quieter. Undo: install the toolchain in
`deploy/provision.sh`.

**The regression test reads the lockfile rather than installing anything.**
`tests/test_deploy_install_set.py` walks the dependencies the deploy's `--no-dev` install
would fetch and fails if any has no wheel for the pinned Python on linux. It is a second
and needs no network, where actually running the server's install set in CI is a minute
and a separate ticket (HIR-234). Undo: delete the file.

---

## 2026-11-09 — The tracing package ships with the app, and a missing one is tracing off (HIR-233)

`langsmith` was a dev-only dependency. The deploy installs the app with `uv sync --frozen
--no-dev`, so the server never had the package; the first traced poll on the VM died with
`ModuleNotFoundError` before reading a single job, while CI stayed green because tests and
local runs do have it.

**The package is a real project dependency now, not a dev one.** Tracing is part of how
the live system is operated (deploy/README.md), so the thing it needs is installed
wherever the app is. It adds no model cost and no behaviour. Undo: move the line back to
`[dependency-groups] dev` in `pyproject.toml` and re-lock.

**A failed `import langsmith` counts as a LangSmith failure, not a failed run.** HIR-160's
invariant was that no LangSmith problem can fail a run, but both imports in the live path
sat outside the safety net that promise is made of. They now go through one helper that
returns nothing and warns once per process — `[langsmith] import failed, continuing
without it` — and the run proceeds exactly as it does with tracing off. Warning once, not
once per job, is deliberate: a poll reads a few hundred jobs. Undo: import the module
directly again in `app/langsmith_live.py`.

A test now sets the key, makes the package unimportable, and asserts that the poll still
stores its mentions; the same is asserted for the dashboard's add-a-job path.

---

## 2026-11-09 — The live poll is traced: one trace per run, and the grounding check is measured, never enforced (HIR-160)

Every extraction run — the daily poll, a full re-read after a version bump, an add, the
legacy backfill — is now one LangSmith trace in the project `hiring-radar-live`, with a
child span per job and the model call nested under its job. Four choices inside that are
worth keeping.

**One trace per run, not per job.** The free plan allows 5,000 traces a month and the eval
(HIR-78) shares it. A trace per job would have been about 200 a day in Berlin alone and
would have run out within a week of adding cities; a trace per run is a few dozen a month
whatever we add. Jobs are children, so nothing is lost. Undo: open the trace in
`_extract_pending` instead of `extract_pending`.

**The run's name is the entry point, not a guess about its contents.** `poll`, `re-read`,
`add`, `backfill`. A poll after a version bump reads new postings *and* re-reads old ones,
so "is this a re-read" is not a yes/no: the run carries `first_reads` and `reread_queued`
as numbers and a `reread` tag when the queue held any, and HIR-224's targeted re-read is
compared against a full one on exactly those numbers.

**Grounding is measured on every live reading and never acted on.** The check (does every
snippet the model quoted as evidence actually appear in the posting?) moved out of
`app/evaluation.py` into `app/grounding.py`, below both the eval and the pipeline, so the
two can never measure it differently. The live pipeline counts it per job and per run, tags
the failures, and stores the extraction unchanged. Enforcing it in the poll — dropping a
skill whose quote the check cannot find — was rejected: the extractor already drops those
itself, and a second, differently-placed rule would let the poll and the eval disagree
about the same posting. Undo: delete the two `report.grounded/quotes` lines in
`_extract_pending`.

**Tracing is off unless `LANGSMITH_API_KEY` is set, and a LangSmith failure is never
fatal.** Same rule HIR-78 settled for the eval, for the same reason: the daily poll cannot
depend on a third party being reachable, and no test may send anything to a real account.
Every LangSmith call goes through a `_safe` wrapper that warns on stderr and carries on;
`tests/conftest.py` already unsets the key for the whole suite.

**What is not scripted.** The monitoring dashboard is set up by hand in the LangSmith UI —
the SDK (0.14) has no dashboard API, so there is nothing to automate. The four panels are
written down in `deploy/README.md` under "Tracing the poll".

---

## 2026-11-09 — The cost of a full re-read is computed, never quoted from memory (HIR-221)

Every agent instruction that mentioned the cost of re-reading the stored jobs said "about
€3". That was true at a few hundred jobs. By the time Hamburg, Frankfurt and Munich had
launched, the database held 730 jobs and HIR-165's full re-read cost about €10.50 — so a
pull request saying €3 understated what merging it would spend by more than three times,
and the reviewer's "at most one re-reading PR per day" rule was reasoning from the wrong
number. The cost grows with every city, so any constant goes stale by design.

Chandler's answer on the ticket: compute it instead of quoting a constant.

`uv run python -m app reread-cost` now prints the figure: the jobs the queue would hold
times the average cost of one reading, averaged over the token counts stored for the most
recent readings we have actually paid for (HIR-170) and priced at the model that would do
the next one. It makes no model call, so asking is free. On the live database the day this
merged: 619 open jobs, about €9.01. Validation that the method is right rather than merely
plausible — priced over all 730 stored jobs it returns €10.63, against the ~€10.50 the
HIR-165 launch really spent.

Three choices worth knowing:

- **Tokens are measured, prices are looked up.** The average is of token counts, not of
  euros, so switching models reprices the same reading honestly instead of carrying an old
  model's prices forward. `app/reread_cost.py` is now the one place model prices are
  written down; `app/discover.py` takes the city-launch cap's prices from it.
- **Only open jobs are counted**, because since HIR-195 only open jobs are re-read.
  The count comes from the extraction queue's own WHERE clause, and a test pins the two
  together so the figure cannot quietly measure a rule that has changed.
- **Too few readings is said out loud.** Under 20 stored readings with token counts, the
  command falls back to a hand-made estimate and labels itself an estimate rather than
  presenting a guess as a measurement.

To undo: revert the HIR-221 commits. Nothing in the pipeline or the dashboard depends on
the command — reverting restores the flat €3 wording and loses only the figure.

---

## 2026-11-09 — The agency screen also runs at ingest, on every country-wide feed (HIR-220)

The 2026-11-03 entry below (HIR-123, "Rejection is for boards whose problem will not
change") settled that a recruitment agency or a job portal is never one of our boards: the
postings it carries are not written by the hiring company, so they distort skill counts the
way the aggregator headline rows did (HIR-104). But that screen only ever ran when a board
was *added*. Postings arriving through the country-wide sources — the Bundesagentur für
Arbeit, arbeitnow, JSearch, Startup Jobs — were never checked against it, so Randstad
Digital, Robert Half, Michael Page and European Tech Recruit were stored like employers: 7
of 730 postings when HIR-165 found it, too few to move any skill's share, but a growing
share as more German cities are added — 13 of Hamburg's first 14 postings and 12 of
Frankfurt's 13 came from the Bundesagentur feed.

**Chandler's decision, 9 Nov:** the same screen applies at ingest. An agency's posting is
not stored, temporary staffing (`ARBEITNEHMERÜBERLASSUNG`) included.

**One rule, in one place.** `AGENCY_WORDS` and the match now live in `app/ingest.py`, next
to `in_scope_title` — the other screen that decides what gets stored — and
`discover.agency_word` calls it. That direction is forced: `app/discover.py` already
imports from `app/ingest.py`, so the reverse would be an import cycle. The board screen's
own behaviour is unchanged; it still matches the board token and the company name together,
and `discover.AGENCY_WORDS` still resolves for anything reading it there.

**Which sources it covers, and which it does not.** Every source of kind `feed` or `search`
in `app/sources/registry.py`, which is exactly the four country-wide ones. Chandler named
three; Startup Jobs is the same kind of source and is screened for the same reason, so it
is in, and a country-wide source added later is screened by being registered, not by
anybody remembering this entry. Board sources are **not** screened at ingest: a board is
screened before it is ever added, so screening its postings again would let a board we
chose store nothing at all, silently. The manual sources are not screened either — a person
who adds a posting by hand has chosen it, which is the same reason `trust_title` exists.

**The screen runs last,** after the title, city and company checks, so those three counts
keep meaning what they did and `skipped_agency` only ever holds postings that would
otherwise have been stored. The poll report prints it with the others.

**The accepted cost is unchanged from 2026-11-03, and now it bites in more places.** The
word list is substring-matched on a squashed company name, so a real employer whose name
contains one of the words is dropped silently. That trade was accepted for boards because a
missed agency is one noisy feed you can disable while a false positive quietly loses an
employer. At ingest the same trade now applies to roughly 700 postings a day rather than to
a few dozen board decisions, so the count in the poll report is the thing that makes it
auditable: a jump there is the signal that the list caught something it should not have.

**What this does not do:** remove the agency postings already stored, which HIR-220 put out
of scope deliberately — numbers Chandler has already seen do not silently change underneath
him. They age out instead, because a refused posting no longer moves its job's `last_seen`:
the dashboard's open rule drops an arbeitnow-only job 3 days after its last sighting
(`FEED_OPEN_DAYS`) and a Bundesagentur- or JSearch-only job 60 days after it
(`MANUAL_OPEN_DAYS`, since absence from a sample proves nothing). So the 7 postings this
started with disappear from the open view within two months without anything being deleted.

**How to undo:** revert the PR. There is no migration and nothing is deleted, so the only
effect is that agency postings start being stored again on the next poll.

## 2026-11-08 — Hamburg, Frankfurt and Munich are collected; two of them have no boards to add (HIR-165)

Chandler named these three cities on the HIR-165 ticket, so the 2026-11-03 rule below
(HIR-132) applies as written: a city he has named is launched by the automated path and
neither it nor its boards waits on approval. `geo.ACTIVE_CITIES` is now
`("Berlin", "Remote (EU)", "San Francisco", "New York", "Hamburg", "Frankfurt", "Munich")`.
The stop list's `ACTIVE_CITIES` and spend lines were read against that rule; the specific
rule governs, and the launch path's own caps (EUR 10 of one-time reading, 5,000 postings a
day, per city) were the spend limit. No cap was reached.

**What the three launches found, which is the thing worth keeping.** The board policy adds
an employer board with 5 or more AI roles in the city being launched. Applied to these
three, it added boards for Munich only:

- **Hamburg:** 284 boards judged, **0 added** — the best had 2 roles in the city.
- **Frankfurt:** 337 boards judged, **0 added** — same reason.
- **Munich:** 381 boards judged, **3 added** (Agile Robots, Celonis, Alexander Thamm),
  about EUR 0.28 of one-time reading and 318 postings on the daily download.

So outside Berlin and Munich, German AI hiring does not sit on company-run Greenhouse,
Lever, Ashby or JOIN boards in the quantity the policy looks for. These cities' postings
arrive through the country-wide German feeds instead, which is what the ticket predicted:
of Hamburg's first 14 postings, 13 came from the Bundesagentur für Arbeit and 1 from
arbeitnow. Each city therefore also got the two Bundesagentur searches Berlin has ("AI
Engineer" and "Machine Learning Engineer", 25 km, Munich's spelled "München") and its own
two board-discovery queries. Nothing here says the policy is wrong — a board with 2 roles
is left unrecorded rather than rejected, so it can be picked up when it grows.

**The launch quality check: all three read as well as Berlin, or better.** Each city's
sample was labelled by the same two-model panel as the Berlin run it is measured against
(`20261103T224145Z_label`), so the panel check added in HIR-149 prints no warning: the
labeller sets match. Scores are the panel's agreed labels against what the extractor
actually stored.

| city | postings scored | F1 | vs Berlin 0.938 |
| -- | -- | -- | -- |
| Hamburg | 12 of 14 | 0.935 | -0.004 |
| Frankfurt | 10 of 13 | 0.945 | +0.007 |
| Munich | 15 of 15 | 0.969 | +0.031 |

None is clearly worse (the check's line is 0.05), so no follow-up is owed on quality. Two
Hamburg and three Frankfurt postings scored nothing because the two labellers agreed on no
skill at all for them; with pools of 14 and 13 postings there was nothing to swap in, which
is the real limit of a check on a city this small, not a quality signal. Munich reads
*better* than Berlin on the same panel, which is the first city launch where that has
happened.

**What the new cities actually ask for, which nobody has decided yet.** The labellers
proposed roughly 100 skills per city that have no entry in the skill list, and they are
strikingly unlike San Francisco's GPU and inference stack (HIR-128): Hamburg and Frankfurt
are Microsoft Azure and enterprise integration (Azure AI Foundry, Entra ID, Power Automate,
Copilot Studio, SAP), and Munich adds robotics and reinforcement learning (MuJoCo, IsaacSim,
sim-to-real, PPO, vision-language models) from the boards its launch added. None of this is
on the chart, so the three cities currently look emptier than they are. HIR-219 is the
batch review; this paragraph is the reason it matters more than its job counts suggest.

**Tracking a city moves its remote postings into it.** "Hamburg, Germany (remote)" read as
Remote (EU) until today and reads as Hamburg now, because a named city has always won over
a remote phrase (the 2026-10-26 EU-remote entry). This is the same thing that has always
happened for Berlin, and no posting is dropped by it — only relabelled. Several test
fixtures used Hamburg and Munich as their stand-ins for "a German city we do not track";
they now use Leipzig and Stuttgart.

---

## 2026-11-07 — The no-company rule is enforced where every job is stored (HIR-207)

The rule of 6 Nov below ("A job is never stored without a company", HIR-198) was only
checked on the add-by-link path. The poller stores feed postings as they arrive, so a feed
that returned a blank company stored it blank — and because dedup matches on company
first, such a row can never be recognised as a duplicate, so every repost of it from
another source becomes a second row. One job was already stored this way, from the
Arbeitsagentur feed.

Decision: the check moves to `ingest_one`, which every stored job passes through. A posting
whose company is empty *to dedup* — `dedup.company_key` comes out blank, which also covers
punctuation used as a placeholder and a bare legal suffix — is refused and counted as
`skipped_company`, the same way an out-of-scope title or an untracked city is, and the poll
totals it per run. The check sits after the title and city filters so those counts keep
their meaning, and `trust_title` (the waiver for a posting a person chose by hand) does not
waive it: how a blank-company row got in does not change that it can never dedup.

The add-by-link check in `app/add.py` stays: it is what lets the dashboard's drawer ask for
the company and keep the form filled, which a bare refusal at ingest cannot do. Ingest is
now the backstop for every other path, which is why `add-text` and `add-screenshot` with an
empty company string are refused rather than stored blank — they were only ever safe because
the field is required in the form, not because anything checked it.

Rows stored blank before this are a separate, still-open question: the `repair-companies`
command fills them, and where that reveals a duplicate it merges two rows into one, which
deletes a stored job. That is on the AGENTS.md stop list and nothing here authorises it, so
this entry changes no stored row. The one row concerned (job 95, Arbeitsagentur feed) would
also be filled wrongly today — its page is gone (HTTP 410) and the hostname fallback proposes
"Arbeitsagentur", the board rather than the employer, because the polled feed sources are
missing from the not-an-employer list of the 6 Nov entry. HIR-211 fixes that first.

To undo, drop the `company_key` check from `ingest_one`; the add-by-link path keeps the rule
and nothing needs backfilling, since the check only ever refuses a write.

---

## 2026-11-06 — The two blank readings that drop a posting must be consecutive (HIR-199)

Clarifies the "try twice, then drop" rule of 5 Nov below (HIR-172). That entry says a posting
is "deleted on the second one" blank reading; it meant two blank readings in a row of a
posting we could not read. The count (`job.blank_extractions`) was a lifetime tally, so this
sequence deleted a job whose skills were already on the dashboard: a blank reading (count 1),
a retry that worked (job stamped, skills stored, count still 1), then a version bump that put
the still-open job back in the queue and a second blank reading (count 2) — dropped, skills
and all.

Decision: `store_extraction` sets `blank_extractions` to 0 in the same transaction that stamps
the job. A reading that worked proves the posting is readable, so the blank before it stops
counting. A posting that only ever reads blank is still read at most twice, which is what the
5 Nov rule was protecting. The alternative — counting blanks per extractor version — was
rejected as heavier and unnecessary once the reset is in place.

Migration 015's comment says the count "is never reset" and is now wrong on that point. It
stays as written, because a committed migration is never edited (AGENTS.md "Where things
live"); `app/pipeline.py`'s module docstring and this entry are the current rule.

To undo, drop `blank_extractions=0` from that UPDATE: the count becomes a lifetime tally
again and a posting is dropped on its second blank reading whenever it happens. Nothing needs
backfilling — the column only ever drops jobs, never gates anything else.

---

## 2026-11-06 — A job is never stored without a company (HIR-198)

Duplicate detection matches on company first, so a row with a blank company can never be
recognised as a duplicate — the same posting added twice by link became two rows. The add
paths now guarantee a company: paste-text and screenshot always required one, and the
add-by-link path now reads it off the page when the page carries no structured job data,
in this order:

1. the site name the page declares (`og:site_name`, then `application-name`) — unless it
   is a job board's or ATS vendor's own name (LinkedIn, Indeed, StepStone, Glassdoor,
   XING, Personio, Workday, Greenhouse, Lever, Ashby, JOIN), which names the host, not
   the employer;
2. the page title's tail after its last "|", "–", "—", spaced "-", or " at " — with the
   same exclusion, and not a careers-section word (Jobs, Careers, Karriere, Join us).
   When this rule supplies the company, the tail is also stripped from the stored title;
3. the registrable part of the hostname (`careers.acme.de` → "Acme"), skipping the same
   ATS and job-board hosts.

If none of the three finds a company, the job is refused (API outcome `needs_company`;
the drawer asks for the company and keeps the form filled), never stored blank. The
one-off `repair-companies` command applies the same rules to rows stored blank before
this decision and merges the duplicates it uncovers. To undo, revert the HIR-198 commits;
existing rows repaired by the command keep their filled companies.

---

## 2026-11-06 — The README's headline numbers are the whole corpus, open postings only (HIR-192)

The front page had drifted a long way from the repository: 222 postings "all Berlin but
one", 44 feeds, 24 hand-labelled ads, F1 0.925, and a scope line saying collection was
Berlin-only until the held-out eval passed — a gate that was met on 2026-11-03. Every one
of those is now re-derived.

Two choices worth keeping consistent the next time it is refreshed:

- **The headline skill table counts all four markets together, not one city**, and counts
  the *open* postings with a full description — the same slice the dashboard opens on
  (`/api/skills` with no filters). A per-city line follows it for Berlin and San Francisco.
  Quoting one city in the headline is what made the old table wrong the moment a second
  city switched on.
- **Each number says where it came from** — the command (`app stats`), the endpoint
  (`/api/skills`), or the eval results directory. The numbers go stale by design, about
  once a month; naming the source makes the next refresh a re-run rather than a hunt.

To undo, revert the HIR-192 commit; nothing outside README.md changed.

---

## 2026-11-06 — Entry is a query bar, not city tabs (HIR-188)

The page used to open on a row of city tabs — All / Berlin / Remote (EU) / San Francisco /
New York / Compare — and a second row of job-family buttons. That row is a list of every
option, so it only works while the options are few. At 20 cities and 5 families it is a
wall of buttons and the first thing a visitor sees is an inventory, not a question.

Entry is now one sentence with two pickers: **[AI Engineer ▾] in [Berlin ▾]**. Three rules
hold it together.

**The query bar is the entry point, and the address bar holds it.** City and job family
live in the URL — `/berlin`, `/berlin/ai-engineer`, `/compare/berlin+san-francisco`. Every
market therefore has a link that can be shared, and the back button works. There is no
router: `web/src/routes.js` is two pure functions, `parsePath` and `pathFor`, extending the
hand-parsed `/jobs/:id` that was already there. An address we cannot read falls back to the
home view rather than erroring — a stale link should land somewhere usable.

**The home grid is only for people who have not chosen.** `/` shows a headline and one card
per market, each with its open-job count and top three skills. The moment a city is chosen
it is remembered in localStorage, and `/` redirects there on the next visit. So the grid is
a first-run screen, not a page anyone sees twice. ("All markets" in the header still shows
it on demand.) The redirect uses `replaceState`, so back leaves the site rather than
bouncing between `/` and the city.

**Compare is a mode, not a destination.** It was a tab, which made it a seventh city and
fixed it at exactly two sides. It is now a mode you turn on from the city you are already
looking at: the picker becomes two or three removable tokens, the chart grows one column
per city, and rows sort by any column, by the widest spread, or by name. Three is the
limit — a fourth column does not fit the row, and reading three markets at once is already
the edge of useful. The diverging "gap" bar is gone; the row with the widest spread is
marked instead, which generalises past two cities where a signed gap does not.

**What a new city costs.** One entry in `PLACES` (`web/src/format.js`) carrying its name,
URL slug, country group and any search aliases. Picker, market grid, compare and the URLs
all read that one list, so nothing else on the frontend changes. (Collecting the city is
separate and unchanged: `geo.ACTIVE_CITIES` plus `discover-boards --launch`.)

**Numbers, and why two of them differ.** Nothing new is computed and no endpoint was added.
Per-city counts in the picker and on the cards come from `/api/stats` `open_by_city`; the
cards' skill bars are a share of `city_totals` from the single `/api/skills` call the page
already makes with no city filter. Those two differ slightly — a handful of postings are
stored as a fragment too short to chart — so the card count and the picker count match each
other, and the bars match the chart. One request serves every card; there is no call per
city.

**The job family moved into the query bar and became single-choice.** It was a multi-select
button row; it is now one `<select>`, because a market is one role in one city and the URL
has to name it. A short flat list of five needs no search box, so it is the browser's own
control. Nothing defaults to a family: a first visit shows every AI and data role, as
before, rather than silently hiding four fifths of the market.

**The landing view is centred, and it is one grid (HIR-191).** Chandler's first look at the
shipped screen: splitting the grid into one row per country left every row half empty, so
the page read as small and pushed left. Below four cities there is not enough in a country
group to be worth its own row, so every market now sits in **one** grid sorted by open
jobs, with its country as a small label on the card. Grouping comes back on its own once a
group can fill a row; the "request a city" prompt left the grid and is a centred link under
it, because a dashed card in a row of real markets reads as a market. On the landing view
only -- no city chosen -- the headline, the line under it, the pickers and the Recent chips
are centred and one size larger; the dashboard keeps its left alignment, because there the
query bar is a control above a chart rather than the subject of the page.

**Compare starts from a dropdown.** "+ Compare with another city" was a dashed button that
only switched modes: you then had to click "+ add" and pick, so seeing two cities took two
decisions. It is now the same searchable city list as the city picker, minus the city you
are already on, and picking lands straight on `/compare/<a>+<b>`. Compare mode's "+ add" is
that same control, so it opens on the first click.

---

## 2026-11-05 — MVP page: no skill tree card, no posting-text search box (HIR-187)

Both are hidden from the page and kept in the code and the API. Nothing was deleted on the
server: `/api/jobs` still accepts the `text` filter, `/api/skills/tree` still answers, and
`app/skill_tree.py`, `web/src/SkillTree.jsx`, `api.skillTree` and their tests are untouched.
This is a decision about what the MVP page shows, not about what the product can do.

**Why the posting-text box went.** The Jobs toolbar is one flex row: a left group (title,
Saved pill, skill chips, "+ Add skill", the jobs count) and a right group (the search boxes
and Sort). The left group's width follows the city label, so "56 open jobs · Remote (EU)" is
much wider than "… · Berlin". With two ~260 px inputs in the right group the row could not
hold on All, Remote (EU) or New York and wrapped to two rows — the toolbar changed height as
you clicked between cities. Two search boxes were also the wrong answer to begin with: "Search
company or title" and "Search the posting text" sat side by side with no explanation of which
to use, and the same word means different things in each. One box stays; the posting-text
search belongs in an advanced-filters drawer, which the home-screen rework will place.

**Why the row now holds for every label.** Removing one input was most of it. The rest is in
`.jobs-head`: the left group may shrink (`min-width: 0; flex: 1 1 auto`), the right group may
not (`flex: 0 0 auto`), the remaining input shrinks down to 160 px instead of a fixed 260 px,
and the count label never breaks mid-phrase. Below 1024 px the wrap is now deliberate — the
search and Sort take their own line — rather than an accident of the label's length.

**Why the skill tree card went.** It is the page's biggest drawing and it sat shut by default
under the job list, so most visits paid for a card they never opened, and the ones that did
opened a map the MVP has nothing to say about yet. HIR-81 and HIR-89 own the tree; they bring
it back deliberately, per career track, when there is a reason to look at it. A comment is
left where the card was so the next reader knows this was a choice.

**To undo.** Both are small, self-contained reverts: the card is one `<section>` plus the
state that fed it, the box is one `<label>`/`<div className="search">` pair plus its `text`
state. `filters.text` is still in the filter shape and still sent to the server; it is simply
always `""` from the UI.

---

## 2026-11-05 — Job family is a title rule (v1) (HIR-186)

Decision: every job carries one of five job families — `ai-engineer`, `ml-engineer`,
`data-scientist`, `ml-platform`, `research` — decided from `job.title` alone, matched
case-insensitively, first match wins:

| family | title matches |
| -- | -- |
| `data-scientist` | `data scien`, `datenwissenschaft` |
| `ml-platform` | `mlops`, `ml platform`, `ml-platform`, `ml infra`, `platform engineer` |
| `ml-engineer` | `machine learning engineer`, `machine-learning engineer`, `ml engineer`, `ml-engineer`, `mle` (whole word) |
| `research` | `research`, `applied scientist` |
| `ai-engineer` | everything else |

Why a rule and not the model: every stored job already passed the ingest title filter (an
AI/ML domain term plus a technical role term), so the title carries enough signal to split
the pool into five buckets at no model cost and with no re-extraction. Data-scientist
postings were already in the pool, just unlabelled. The families exist so the planned
"my job in my city" entry screen (HIR-105) has a family field to offer a picker over.

Known limits, accepted for v1:

- A title naming two families takes the earlier row, so "Senior Data Scientist / Machine
  Learning Engineer" is `data-scientist`, not both.
- `ml-platform` is tested before `ml-engineer` so "ML Platform Engineer" is platform. The
  cost is that `platform engineer` catches any platform role in the pool, AI-platform
  titles included.
- `research` catches "Research" anywhere in the title, so "Research Engineer, LLM
  Infrastructure" is research rather than platform.
- `ai-engineer` is the remainder, not a positive match: an unusual title with no family
  word lands there. On 5 Nov that is the largest bucket by construction.
- `mlops` is matched as one word, so "ML Ops" spelled with a space does not reach
  `ml-platform`: "ML Engineer (Computer Vision & ML Ops)" is `ml-engineer`.
- The family describes the title, not the work. A posting whose body is pure data science
  under an "AI Engineer" title is misfiled, and nothing here notices.

The rule lives twice: `family_of` in `app/ingest.py` labels new jobs at insert, and the
same CASE in `app/migrations/017_job_family.sql` backfilled the existing rows. A test
asserts the two agree over a fixture list of titles, so changing one without the other
fails the suite.

Measured on the 562 jobs stored on 5 Nov 2026, the backfill gives: `ai-engineer` 329,
`research` 90, `ml-engineer` 64, `data-scientist` 60, `ml-platform` 19, none unlabelled.
`research` is larger than one might expect because any "Research" in the title counts,
including "Senior Machine Learning Research Engineer".

To undo: revert the HIR-186 commits and drop the column; the filter is additive, so no
earlier number changes. A model-assigned family can replace the rule later without the
column, the API parameter or the dashboard control changing — only `family_of` and the
extractor would.

---

## 2026-11-05 — `ai-deployment` is not narrowed: the two spot-check rejections were item-level calls (HIR-183)

Chandler was asked whether to narrow `ai-deployment`, and chose not to. **The skill list and
`evals/LABELING.md` are unchanged by this decision, and no boundary between `ai-deployment`
and `mlops` is written down.** Recording the measurement here so this is not re-asked.

**What prompted it.** Of the 11 `unsure` skills he hand-checked under HIR-159, he rejected 2,
and both were `ai-deployment`: New York/ramp on the `raw_text` "deployment trade-offs" (a
fragment of "Strong fundamentals in ML/GenAI, including problem decomposition, evaluation, and
deployment trade-offs"), and Berlin/Bluefish on "Extensive experience with training and
deploying machine learning models". Two of two looked like it might imply a narrower skill than
the stored mentions reflect.

**It does not, and the rules already said so.** Two standing rules settle most of it. The
2026-11-01 entry below (HIR-101) draws `ai-deployment` against generic deployment: bare
"deployment" is "ordinary software delivery, not deploying a model", a false positive in
practice, while `model deployment` / `ml model deployment` "cover the narrow sense". That
disposes of the New York quote with no rule change at all. And DECISIONS 2026-11-04 (HIR-159)
plus `evals/LABELING.md` protocol rule 8 say a verdict that calls a label wrong scores that one
posting and goes to `corrections_to_decide` — it never rewrites the taxonomy. So "no rule
change" was already the default; narrowing would have been a separate, deliberate act.

**The measurement, on 5 Nov 2026 (36 stored `skill_mention` rows for `ai-deployment`).** Split
by whether the quote names a model at all, and then by wording:

| Group | Mentions |
| --- | --- |
| Bare "deployment" — no model/ML/AI/KI word in the quote | 8 |
| Names a model, explicit first-hand experience wording ("Experience deploying…", "hands-on", "Erfahrung", "You've deployed…") | 14 |
| Names a model, deployment as a task or topic ("Training, Fine-Tuning und Deployment von…", "designing, training, tuning, and deploying models") | 14 |

So the three candidate lines were **36 → 28** (drop only the bare ones), **36 → 14** (require
first-hand experience wording), and **36 → 5** (require deployment-machinery wording:
serving, monitoring, scaling, maintaining, produktiver Betrieb — only 5 of the 28 qualify,
which would take the skill off the chart). Chandler was given all three numbers and chose
**36 → 28**: the Berlin posting keeps its label, and that stays a one-posting call.

**Why a first-hand-experience rule was rejected on its own merits, not just on cost.** It would
not have excluded the quote that prompted the question. "Extensive experience with training and
deploying machine learning models" *is* first-hand experience wording, so a rule requiring
first-hand experience keeps it. Its stated mechanism — that "knowledge of X" wording would then
map nowhere — only reaches the New York quote, which the 2026-11-01 rule already handles. It
would also have contradicted `evals/LABELING.md` requirement rule 3, which says knowledge
wording ("You have basic knowledge of ML libraries" → `scikit-learn` stays `required`,
golden_020) counts as asking for the skill; editing that is a stop-list change that invalidates
every stored eval result. All cost, no effect on the motivating case.

**Merging `ai-deployment` into `mlops` was also rejected, on the data.** Only 9 of
`ai-deployment`'s 36 jobs also carry `mlops` (2 carry `model-serving`), so postings are using
them as different things. Counts that day: `mlops` 49 jobs, `ai-deployment` 36, `model-serving`
23, `devops` 16, `llmops` 8.

**The 8 bare mentions are handled separately, as HIR-183 did not cover them.** They are wrong
under the 2026-11-01 rule whichever way this went — they arrived as extractor output, which
that entry's alias reasoning never reached. Filed as HIR-185 (`attended`, because dropping
stored rows moves counts the dashboard has already shown): jobs 18, 114, 125, 126, 211, 213,
329, 420, every one of which carries `ai-deployment` *only* through a bare quote, so the skill
goes from 36 jobs to 28 when they are corrected.

**To undo.** Nothing to revert — no code, skill list, guide or stored data changed in this
ticket. Re-opening the question means re-opening HIR-183, and the numbers above are the
starting point rather than something to re-measure.

---

## 2026-11-05 — Wanting a skill is not having it: appetite wording is `nice_to_have` (HIR-178)

Decision: wording that asks only for *appetite* toward a skill — eager to, eagerness to,
interest in, interested in, keen to, curious about, excited by, hungry to, willing to learn,
and the German Interesse an, Lust auf — makes that skill `nice_to_have`, whatever the section
heading says. This also covers a posting that accepts appetite *instead of* experience
("initial experience or a very strong interest in X"): a candidate can qualify without X, so
X is not a requirement. Chandler decided this in session on 5 Nov 2026, choosing option 1 of
the three the ticket put up.

Why: the rules did not cover this wording, so the extractor guessed, and guessed both ways —
of 6,189 stored skill mentions, 10 rested on appetite wording and split 6 `required` to 4
`nice_to_have`. The guide marked something optional only on a closed list of six words
(preferred, plus, bonus, nice to have, ideally, is an advantage) and otherwise let the heading
decide; "Your Profile" is a requirements heading, so the rule as written returned `required`
for "are eager to dive deep into LangChain". Both readings were defensible, which is the
defect. Option 1 won because it is how the words read to someone applying for the job, and
because it is the only option that does not quietly turn "interest in X" postings into hard
requirements on the chart.

What this does **not** cover, deliberately:

- The appetite has to govern the skill itself. "Basic knowledge of ML libraries (e.g.
  scikit-learn) and are eager to dive deep into LangChain" asks for scikit-learn and only
  wants LangChain: scikit-learn stays `required` (golden_020).
- An extra clause about deepening a skill the posting already asks for does not soften it:
  "Hands-on exposure to LLM and agentic ecosystems … and eagerness to deepen this expertise"
  is `required` (golden_014).
- The company's own enthusiasm is not the candidate's appetite: "we'd love to hear from you"
  changes nothing (golden_038).

Also decided, as a consequence: where a label rests on appetite wording, `raw_text` has to
include the appetite phrase. Four criteria in golden_020 and golden_024 quoted the bare skill
list ("LangChain, LLM orchestration, and vector databases") and so hid the very words that
decide the label — which is how the first count of affected criteria came out at 10 instead of
the true 17.

Scope of the relabel: **17 criteria in the answer key flip `required` → `nice_to_have`** — 13
in the dev split (golden_001, golden_002, golden_020) and 4 in held-out (golden_024, and
golden_046's `rag`, which contradicted the `mcp` label in the very same sentence). The guide's
own header requires relabeling affected Goldens in the same change. The dev split holds 337
criteria, so this moves `requirement_accuracy` by roughly 4% on its own: the eval score
measured after this change is **not comparable** with any measured before it, and the drop is
the answer key catching up, not the model getting worse.

To undo: revert this commit range. The stored mentions correct themselves on the next
re-extract either way; nothing was edited by hand in the database.

## 2026-11-05 — The AI-assisted-coding skill is shown as "AI Coding Tools", with the spellings the postings use (HIR-181)

Decision: the `ai-developer-tooling` entry's display name becomes **AI Coding Tools**. Its
id stays `ai-developer-tooling` — 70 stored postings and six Goldens point at it, and the id
rule in `taxonomy/README.md` is that an id is never renamed once rows reference it. The two
children, `cursor` and `github-copilot`, keep it as their parent, untouched.

**Why "AI Coding Tools" and not "AI Coding Assistants"** (the ticket's runner-up): it is the
postings' own phrase. Of the 61 distinct quotes behind the 70 jobs, one is literally "AI
Coding Tools" and four more are "AI coding tools" ("Proficiency in using AI coding tools",
"power user of AI coding tools", "similar AI coding tools", "uses AI coding tools and agent
workflows as a force multiplier"). "Tools" also covers both children, which are different
kinds of thing — Cursor is an agent, GitHub Copilot an autocomplete assistant — where
"Assistants" would read oddly over an agent. The old name "AI developer tooling" appears in
only 2 of the 70, and one of those two is a posting for *building* such tooling.

**Every alias added here was read off a real stored quote**, not guessed. The entry had two
aliases ("coding agents", "ai development tools"); it now also answers to: "ai coding tools",
"ai coding assistants", "ai coding agents", "coding agent", "agentic coding", "agentic coding
tools", "ai-assisted coding", "coding copilots", "ai-assisted development tools",
"ai-assisted developer tooling", "ai-powered development tools", "ai-powered developer
tools", "ai dev tools", "genai coding tools", and the German "ki-coding-agenten",
"ai-coding-copiloten", "ki-gestützte tools", "ki-entwicklungstools", "coding-agenten".

**"ai developer tooling" is kept as an alias of the renamed entry.** It used to resolve as
the display name; renaming without the alias would silently stop `resolve("ai developer
tooling")` working — the same trap HIR-177 recorded a day's work earlier. Two stored postings
and Golden `golden_009` quote that phrase, and `app/extract.py`'s `new:` path would have
turned it into a *proposed* skill instead of a mention, while `web/src/cvSkills.js` matches a
CV against display names and aliases.

**What was deliberately left out.** "agentic development" and "agent-driven development":
both appear in quotes, but they sit one word away from `agents` (170 jobs, *building* agents)
and `tool-calling` (60 jobs, a model calling tools), and the ticket names that confusion as
the thing to avoid. "AI tools" and "KI-Tools" bare: too broad — a posting saying "Du nutzt
KI-Tools souverän im Arbeitsalltag" need not mean coding. Both stay out until a posting
forces the question. No new skills were created: this entry plus Cursor and Copilot already
cover the ground.

`version` goes 9 to 10: the rename changes what an existing label resolves to, so every job
is re-read once on merge (about €3).

## 2026-11-05 — The Testing skill is shown as "Software Testing", and the word-sharing boundaries live in taxonomy/README.md (HIR-177)

Decision: the `testing` entry's display name becomes **Software Testing**. Its id stays
`testing` — 72 stored postings and the labelled Golden set point at it, and the id rule in
`taxonomy/README.md` is that an id is never renamed once rows reference it. Renaming the id
would mean rewriting stored data, which is Chandler's call and a separate ticket.

The bare word **`testing` is added as an alias** of that entry. It used to resolve as the
display name; renaming the display without the alias would have silently stopped
`resolve("testing")` working, which matters in two places — the `new:` proposal path in
`app/extract.py`, where an unresolvable label becomes a *proposed* skill instead of a
mention, and `web/src/cvSkills.js`, which matches a CV against display names and aliases.

The three neighbours that share the word "test" keep the phrase families that belong to
them: `a-b-testing` gains "a/b test", "split test", "split testing" (it had no aliases at
all); `statistics` gains "statistical testing", "hypothesis testing", "significance
testing". `evaluation` gains nothing — it already answers to "model evaluation", "llm
evaluation", "ai output evaluation", "evaluation frameworks" and "Evaluierung".

**Why, and what the evidence was.** The entry was called "Testing" with no statement
anywhere of what it covers; the only thing pinning the meaning was its alias list, which is
all software testing. It had not actually drifted: of the 72 stored postings carrying it, all
72 quote a software-testing phrase. Nor had the neighbours leaked into it — across every
stored mention, "a/b test" lands on `a-b-testing` (15), "hypothesis testing" on `statistics`
(3), and neither "split test", "statistical testing" nor "significance testing" appears in
the corpus at all. So the aliases added here are prevention, not repair; "split test" and
"significance testing" are absent from today's postings and are added because they are the
same thing spelled differently, which is the alias rule.

**Where the boundary is written down: a new "Skill boundaries" section in
`taxonomy/README.md`**, not in `evals/LABELING.md`. The skill list itself has no per-entry
description field, and adding one would change the schema and every reader of it. LABELING.md
would otherwise be the natural home — it is what a labeller reads — but editing it is on
AGENTS.md's stop list ("any edit to `evals/LABELING.md` … invalidates every eval"), and
LABELING.md already names `taxonomy/README.md` as "the source of truth" for what counts as a
skill and quotes it, so a labeller following that pointer reaches the boundary. The rule wins
over the ticket's wording; nothing in LABELING.md changed, so no stored eval is invalidated.
The section is deliberately for word-sharing pairs only, so it does not grow into a
definition for all 217 entries.

No Golden label changes: every `testing` criterion in the 46 Goldens quotes a plainly
software-testing phrase, and the answer key already treats a compound quote as two skills
(golden_013 carries both `testing` and `evaluation` off "evaluation, testing, validation…").

**Undo:** revert the three entries and the README section, and set `version` back to 8. It
costs one re-read of every job (about €3) in each direction.

## 2026-11-05 — A blank reading of a posting is a failure, not a result (HIR-172)

Decision: when the model answers with a well-formed tool call that carries nothing at all
— no skills, nothing proposed, nothing rejected, and none of the four attributes
(seniority, German, degree, production) — `extract()` raises `EmptyExtractionError`. The
pipeline then leaves the job unstamped and counts it in the `failed=` tally, so it is read
again on the next run and shows in the poll line. Zero skills *with* any attribute found
stays a success, because a posting that lists no technical skills but does state a
seniority has genuinely been read.

**Why.** Job 569 (Accenture, "AI LLM Architect (All Genders)") was stored on 5 Nov with
every extracted field null off 5,975 characters dense with taxonomy skills, and reported as
`extracted=1/1 ... failed=0`. The old checks only caught a `max_tokens`/`refusal` stop, a
missing tool block, or a missing `skills` list; an empty list passed all three. Because the
job was stamped with the extractor version, nothing downstream would ever look at it again
— the one failure mode that is invisible both on the chart and in the poll line.

The cost of being wrong in this direction is a retry worth one model call; the cost of the
old behaviour is a posting silently missing from every count until the next version bump.

**Try twice, then drop — Chandler's decision, 5 Nov** (HIR-172 comment). A blank reading is
counted on the job (`job.blank_extractions`, migration 015) and the posting is deleted on
the second one. The handling is the same whether the job is new or already stored: the
blank reading already on disk counts as the first attempt, so
`scripts/reextract_blank_jobs.py` sets the count to 1 when it clears the stamp, and one
further blank reading drops the posting. Every *other* failure — a connection error, a
`max_tokens` stop — is still retried for ever, because it says nothing about the posting;
only a completed-but-empty reading counts towards the two.

A dropped posting is deleted outright, which is the one place this overrides the stop list's
"deleting stored jobs" line — Chandler decided it himself, which is the authority that line
defers to. The poll line reports it: `failed=` plus a new `dropped=`, both always printed.

Short postings are the exception to re-reading at all: `scripts/reextract_blank_jobs.py`
leaves a blank job under 1,000 characters stamped, because a posting that short legitimately
has nothing to find.

**What this still accepts.** Nothing remembers a dropped posting, so the feed that carried it
re-ingests it on the next poll and it earns two fresh attempts — about two model calls a day
for a posting the model cannot read, and a job id that keeps changing. Filed as HIR-176.

Still open: why the model returned an empty call on that posting at all (365 output tokens
were spent producing it). The `failed=`/`dropped=` lines are what will show whether a second
reading repeats it.

To undo, revert the HIR-172 commits: an empty call is stored as a blank success again. The
`blank_extractions` column stays behind harmlessly (never edit a committed migration) and
nothing re-reads; postings already dropped are gone, and come back only when their feed
next lists them.

---

## 2026-11-04 — The eval gate counts flipped Goldens, not fractions of a point (HIR-164)

On 20 dev Goldens one Golden is 5% of a yes/no attribute score, so the gate's 0.02 stop
line was smaller than the smallest move the measurement can make. Every single flip fired
it and nothing distinguished noise from a regression: the first LangSmith comparison the
same day showed production 0.98 → 0.85 — two or three Goldens on one repeat — and read as
a stop-the-merge event.

**For the four per-Golden attributes — seniority, German, degree, production — the gate now
counts Goldens that flipped from right to wrong, and stops the PR at more than 2.** The
skill scores (precision, recall, f1, requirement accuracy, grounding, rank) pool hundreds
of mentions per run, so they keep the 0.02 rule.

Why counts rather than a bigger threshold: a threshold scaled to the set size has to be
re-chosen every time the set grows, and it still reports a 5% move on 20 Goldens and a 5%
move on 100 as the same number when they are not the same evidence. A count says what
actually happened — "two postings the model used to get right, it now gets wrong" — and
stays meaningful at any size. The rule is written to hold as dev grows toward ~100; it is
not a temporary scaffold to be removed at that point.

How a flip is decided, and why:

- A Golden counts as right in a run when it is right in **most of that run's repeats**, so
  a single unlucky repeat is not a flip. With one repeat that is just the one answer.
- Only Goldens **both** runs scored are counted, so growing the set never registers as
  flips.
- Correctness comes from `app/evaluation.attribute_hits`, which the live run and the table
  both call, on the stored prediction. One code path on purpose: a gate that compared
  attributes by its own slightly different rules could stop a PR the run called clean.
- Improvements are counted and shown the same way, so the table says "2 worse, 1 better"
  rather than implying every flip is a loss.

**Repeats: routine changes run 1 repeat, releases and anything that trips the gate run 3.**
100 Goldens × 3 repeats is 300 traces a run, about 16 runs a month inside the free
LangSmith plan — enough to measure a release, not enough for every PR. One repeat is the
cheap read; when it trips the gate, re-run at 3 before taking the number seriously, because
a single repeat is exactly the noise this entry exists to tame. Three repeats stay
mandatory for the held-out release gate.

What this does not change: the trigger (a diff touching `app/extract.py` or
`taxonomy/skills.json`), the requirement to commit `evals/results/<run_id>/` as the next
baseline, the one version-check exemption, and held-out staying release-only.

To undo: restore the single 0.02 rule for every metric in `scripts/eval_table.py` and in
AGENTS.md "The eval gate". The stored runs need no change — flips are computed from
`predictions.jsonl`, which every dev run already carries, so the rule can be changed in
either direction without re-running anything.

---

## 2026-11-04 — Compare mode is two pickable sides, not a fixed pair (HIR-138)

Decision: compare mode keeps its two-sided layout, and each side is a picker over every
collected place (`PLACES` in `web/src/format.js` — Berlin, Remote (EU), San Francisco, New
York). It opens on Berlin vs San Francisco, so nothing moves until the reader chooses. A
newly launched city joins `PLACES` and is compareable with no compare-view change. This
replaces "Compare mode stays Berlin vs San Francisco" (2026-10-26, the EU-remote entry),
which was decided when two cities existed; EU-remote stays a filter button and is now also
pickable as a side.

**Why two sides and not one column per city.** Comparing two markets for the same skill is
what the second city was collected for, so pairwise is the purpose. One column per place
would widen with every launch, narrow the bars, miss a phone screen at four columns, and
give no way to focus on a pair. An all-cities view can still be added later.

The two sides are always different: picking the place already on the other side swaps the
pair rather than showing a place against itself. The pair is kept outside the filter object
because compare asks the server for every city at once and slices the answer in the
browser, so changing a side refetches nothing.

**Provenance, and what is still open.** This design was the recommendation the decider put
to Chandler on HIR-138; the "go" reached the worker relayed through its coordinating agent,
not observed from Chandler directly. The PR says so and does not merge on it.

Alternatives rejected: leaving compare as Berlin vs San Francisco (New York could then
never be set against another market, which is the point of collecting it). To undo, revert
the HIR-138 commits — the view returns to the fixed pair; nothing stored changes, and no
job is re-read.

---

## 2026-11-04 — LangSmith watches the eval, and only the eval (HIR-78)

Observability on this project starts at the regression eval, not in production. Whenever
the extractor or the skill list changes, `scripts/run_eval.py` now also reports the run to
LangSmith: the dev-split Goldens as a dataset called `goldens-dev`, the run itself as an
experiment named `<extractor_version>-<run timestamp>`, one trace per Golden per repeat
with the model call and the taxonomy-mapping step as children, and the scores attached. Two
taxonomy versions can then be read side by side, and a single posting can be opened to see
what the model was told, what it answered, what the mapping kept or threw away, and what it
cost.

**Why the eval and not the daily poll.** The eval is where a number is compared against a
previous number, so it is where a trace earns its keep; the poll's failures are already
visible in its own logs. Tracing production is HIR-160, after launch.

**What is sent, and where.** Chandler's existing LangSmith account, US region (the default
endpoint), so the 2026 experiments on `jd-skill-extraction-golden-v1` and this work sit in
one place. Only public job-ad text goes out — the dev Goldens' postings, their labels, and
the model's answers. No CV, no profile, no user data. Held-out Goldens are never uploaded:
`app/langsmith_eval.py` raises on a Golden from any split but `dev` before anything is
sent, because held-out text is what the release measurement rests on.

**LangSmith is the view; `evals/results/` is the gate.** The committed result directory
stays the only thing that decides whether a change may merge (AGENTS.md "The eval gate").
Every LangSmith call goes through a wrapper that warns and carries on, so a LangSmith
outage, a missing key or a bad key leaves the eval and the gate working exactly as before.
Tracing is off unless `LANGSMITH_API_KEY` is set, and `--no-langsmith` turns it off with the
key present.

**The old dataset stays as history.** `jd-skill-extraction-golden-v1` and its 7 experiments
predate the current labels and the dev/held-out split, so their numbers are not comparable
with anything measured now (Chandler, 4 Nov). They are left untouched rather than migrated.

**Two things the eval now measures that it did not.** A grounding score: of every skill
quote the model returned, how many really appear in the posting. Invented evidence is a
different failure from a wrong skill, so it gets its own metric instead of hiding among the
false positives. And an extras judge, off unless `--extras-judge` is passed: for each skill
the model added that the Golden lacks, a model says whether the label missed it or the
extractor is wrong, for the HIR-92 spot-check to work from. A verdict is a pointer for a
person, never an edit to a label.

**No test reaches LangSmith.** `tests/conftest.py` unsets the key for every test. This is
not belt-and-braces: `run_eval.py` calls `load_dotenv()` at import, so while HIR-78 was
being built the mocked eval tests picked up the real key, uploaded a fixture Golden
("Python and LangChain") into `goldens-dev` and opened four experiments in the live
account. Those five objects were deleted. The guard makes it an environment guarantee
rather than something every new test has to remember.

To undo: revert the HIR-78 commits. Nothing outside the eval path changes, the dashboard
and the daily poll are untouched, and the dataset and experiments can be deleted in the
LangSmith UI.

---

## 2026-11-04 — "Few skills listed" is 3 or fewer, and the Best fit floor moves with it (HIR-161)

**Supersedes the K = 7 of HIR-154 below, and its "side effect, accepted" paragraph.** K is
now 4: a job listing 3 or fewer required skills is thin, and one listing 4 or more is a
normal posting that shows its percentage and ranks on its own ratio.

HIR-154 set the floor at 7 — the measured median required-skill count — and used that one
number for two things: the ranking denominator `max(total, K)` and the badge's "thin"
threshold. It recorded the consequence as a side effect it accepted: a job listing 6
required skills, all of which you have, read "6/6 · few skills listed" instead of 100%.

In use that side effect was the bug. Chandler saw "2/6 · few skills listed" on a Lieferando
ML Engineer row and 3/4 and 3/6 on Anthropic rows (4 Nov) and ruled: six is a normal list,
the tag is for postings so thinly extracted that a percentage would mislead, like 2/2 or
2/3. "Few skills" means 3 or fewer; 4 or more shows the normal percentage and ranks like
any other job.

**The two numbers stay one number.** HIR-154 explicitly refused to lower the badge
threshold alone, because that decouples the ratio a row shows from the ratio it is ordered
by — a row could read 100% and still be held back, with nothing on screen saying why.
HIR-161 changes where the single threshold sits, not the fact that it is single. So the
floor drops to 4 along with the tag, and a 6/6 job now both reads 100% and ranks on 6/6.

**What this costs, on the record.** HIR-154 measured inversions at K from 5 to 8 and found
the ordering barely moved across that band; K = 4 is below it, and was not measured. The
scripts that produced those numbers were in git-ignored `scratch/hir-154/` and are gone, so
this change ships unmeasured on Chandler's explicit instruction ("Don't re-ask"). The known
exposure: a posting listing 4 or 5 required skills that you cover in full is now floored at
its own count rather than at 7, so it can sit near the top of Best fit again — a weaker
version of the complaint HIR-154 was filed about, which concerned 2/2 and 3/3 rows. Those
stay floored. If Best fit starts looking top-heavy with 4/4 and 5/5 rows, this is the cause
and the undo is restoring `SKILL_FLOOR` to 7.

The floor still only ever lowers a score, never raises one, and nice-to-have skills still
do not count toward it (HIR-51).

---

## 2026-11-04 — A PR whose checks have already passed is merged directly, not armed (HIR-157)

HIR-136 gave the reviewer one command for every PR: `gh pr merge <n> --merge --auto`. On
PR #88 that command failed with GitHub's generic "Something went wrong while executing your
query". The PR was `mergeable_state: clean` — every required check green, branch up to
date. **GitHub refuses to arm auto-merge on a PR that can already merge**; `--auto` is only
for a PR still waiting on something. The reviewer, correctly refusing to merge by hand when
the rules said arm, labelled it and Chandler merged #88 himself. Every PR the reviewer
reaches after CI has finished would have done the same — and the reviewer usually *does*
arrive after CI, because `/work-issue` waits for the checks before starting it.

**The reviewer now reads `mergeable_state` first and branches on it:**

- `clean` → **merge directly**, `gh pr merge <n> --merge`. This is not merging by hand in
  the sense HIR-136 forbade. What that rule protects is the requirement that the checks
  decide; the ruleset still enforces it, and a merge of a `clean` PR cannot happen unless
  the three required checks ("Python tests", "Frontend build", "Rules gate") are green.
  The command is refused by GitHub otherwise.
- anything else → arm `--auto` and bring the branch up to date, exactly as HIR-136 wrote
  it. Unchanged.
- any other error → `needs-chandler`, **no retry**. A merge command that failed for a
  reason we did not predict is the case where a second attempt is how a wrong merge
  happens.

**What this entry does not do: it does not drop the update-branch step.** HIR-157 asked
for that, on the grounds that "the ruleset no longer requires it, as of 4 Nov". That
premise does not hold — the `main` ruleset (id 26303302, last updated 2026-11-04 10:41)
still carries `strict_required_status_checks_policy: true`, which is GitHub's "require
branches to be up to date before merging". So being behind main is still the reviewer's
job and the step stays, per AGENTS.md "Nothing merges directly to main" and the HIR-136
entry below. The two halves fit without a conflict: with strict on, a branch behind main
reports `behind`, never `clean`, so it takes the auto-merge-and-update path that still
needs the step. If Chandler does turn strict off later, the step becomes dead rather than
wrong, and the `clean` branch already covers every PR.

**How to undo:** restore step 4 of `.claude/agents/reviewer.md` to the single
`--merge --auto` command. The cost of undoing it is the one above: every PR reviewed after
its checks finish stalls on `needs-chandler`.
---

## 2026-11-04 — Best fit scores a job against a floor of 7 required skills (HIR-154)

HIR-113 made the *order* the Wilson lower bound of `covered/total`, so a 2/2 job (bound
0.342) stopped beating a 10/14 one (0.454). It did not stop 2/2 beating the far commoner
*partially* covered job: 4/10 bounds at 0.168, so in San Francisco the top of Best fit
filled up with Anthropic and OpenAI rows reading "100% · 2/2". Two required skills is
usually what the extractor found, not what the posting asks.

**The floor.** A job is now scored against `max(total, K)` with **K = 7**, so a job that
lists fewer than K required skills is judged as though it had listed K and simply failed
the rest. 2/2 is scored as 2 out of 7.

K = 7 is measured, not guessed: the median required-skill count over the 410 open jobs in
the chart set on 2026-11-04 (San Francisco 6, Berlin 11, New York 6). It is a constant,
**not** recomputed per request — a median over whatever jobs a filter returns would score
the same job differently on page 1 and page 2, and the ranking has to be reproducible.
The issue guessed "about 5 or 6"; the distribution says 7, and between K = 5 and K = 8 the
measurement below barely moves, so the exact value is not load-bearing.

**The floor tightens the bound rather than replacing it** (the issue left this open and
asked for one of the two to be kept). The ranking score is now the Wilson lower bound of
`covered / max(total, K)`.

Measured by running the real 273-job San Francisco open list through the shipped
`rankJobs` against 201 stand-in profiles — each one the required skills of two randomly
chosen SF jobs, plus one built from the 12 most-demanded skills — and counting
*inversions*: a job listing fewer than K required skills ranked above a job covering
strictly more skills than it does. Gated-out jobs are excluded from the count on both
sides, since a job whose posting rules you out sorts last whatever it scores (HIR-51).

| ranking | mean inversions per profile |
| --- | --- |
| Wilson alone (HIR-113, before this) | 346 |
| floor alone | 82 |
| **floor inside the Wilson bound (kept)** | **36** |

The floor alone loses what HIR-113 bought — among jobs at the same floored ratio it has
nothing to separate 5/7 from 6/10 — so the two together beat either alone, at every K from
5 to 8. The top of the list for the most-demanded-skills profile goes from seven thin rows
(4/4 Databricks, 3/3 OpenAI, then five 4/5s) to 5/7, 5/8, 5/8, 6/11, 5/9, 5/9, with the
first thin row seventh.

The scripts behind these numbers are in `scratch/hir-154/` (git-ignored): `measure_k.py`
for the distribution, `dump_sf.py` plus `sf_rank_check.test.js` for the list comparison.

**What the row shows.** The badge still shows the plain ratio, because that is the honest
count of what the posting asks. But a job below the floor shows the count *without* the
percentage — "2/2 · few skills listed" — and never gets the "full match" wording in the
tooltip or the expanded row, which is what made a thin extraction read as a perfect one.
Side effect, accepted: at K = 7 a job listing 6 required skills all of which you have
reads "6/6 · few skills listed" rather than 100%. It sorts correctly either way; lowering
the badge's threshold alone would decouple two numbers the issue deliberately tied
together.

Nice-to-have skills still do not count toward the score, only toward breaking ties
(HIR-51), and the floor does not touch that.

Not looked at here: *why* so many postings come back with two or three required skills —
83 of 273 open San Francisco jobs list fewer than 5, and 60 of those 83 are OpenAI (32)
and Anthropic (28), which is a pattern in their Greenhouse postings rather than in the
market. Filed as its own ticket.

---

## 2026-11-04 — A PR that changes the agents' own rules never merges on its own (HIR-142)

Since HIR-136 a reviewed PR merges itself. That included PRs that rewrite how review and
merging work, so an agent could have changed its own rules and the change would have landed
without Chandler seeing it. **Chandler's decision, 2026-11-04:** any PR touching the agents'
own rules stops, gets `needs-chandler`, and carries a short block listing each change in
plain words followed by "Did you authorize these?" — nothing more. He answers by merging or
by sending it back. He does not read those files; he discusses what goes in them beforehand,
so the only question is whether he authorized the change. The rule is in AGENTS.md "The
rules gate"; the watched paths are `.claude/**`, `AGENTS.md`,
`.github/pull_request_template.md` and `.github/workflows/**` (he confirmed the workflows
belong in the list the same day — CI is part of the gate).

`scripts/rules_gate.py`, the check's own code, was added to that list as a judgment
call while building this (HIR-142): the paths Chandler named cover the workflow that
runs the check but not the script it runs, and a PR that rewrote the script to always
pass would have walked through. To undo, drop it from `RULE_FILES` in that script.

**The bullets are written by the reviewer, never by the agent that made the change.** The
value is a second reader saying what changed; an author summarising its own diff is the
thing this gate exists to distrust.

**Two enforcers, because one of them is a rule file.** The reviewer agent applies the rule,
and `scripts/rules_gate.py` runs in CI (`.github/workflows/rules-gate.yml`, check name
"Rules gate") on the PR's own file list. The CI half is the backstop: it still fires on a PR
that edits the reviewer's instructions out of existence. It re-runs when the PR description
is edited, which is how the check goes green once the reviewer has added the block.

**Who adds "Rules gate" to the repository's required-checks list: Chandler, after the
HIR-142 PR merges** (his answer in session, 2026-11-04). A failing check only blocks a merge
when it is on that list, and that list is a repository setting — no diff can show a change
to it, which is precisely why it is the one gate an agent cannot edit through a PR. Agents do
not add themselves to it. Until he flips it, the Rules gate check goes red but does not stop
a merge. Rejected: an agent adding it with one command (an invisible change to the merge rule
by an agent, and a check required before it exists on main stalls every other open PR), and a
standing permission for agents to add checks (same two hazards, permanently).

---

## 2026-11-04 — A labeller's "unsure" sends the skill to the hand-check, not out of the answer key (HIR-159)

**Chandler's written decision on the HIR-159 ticket, 2026-11-04: "A skill both labellers
found, where one or both said they were unsure, no longer drops out of the answer key. It
goes to Chandler's hand-check queue instead. Until he has checked it, the score leaves it
out of both sides: it counts neither as a correct find nor as a mistake. Don't re-ask
this."**

Why it had to change. The labeller panel's yardstick is what both labellers agree on;
anything either flagged uncertain went to the review queue and so out of the yardstick,
which made the extractor's own copy of that skill a mistake. HIR-139 found that 29 of New
York's 35 "extractor mistakes" were exactly this: skills *both* labellers had found. The
score was punishing the extractor for being right.

The rule, as implemented in `scripts/launch_check.py`: an unsure skill both labellers found
is **set aside** — removed from the yardstick and from the extractor's side alike — for as
long as it sits unanswered in the run's `review_queue.md`. Once a person writes a verdict it
counts normally: `ok` / `A` / `B` / a JSON override puts the label into the yardstick, and
`drop` leaves it out and charges the extractor for it as before. A verdict written by the
judge model or the third labeller is **not** a hand-check and leaves the skill set aside,
which is the same rule as everywhere else here: a model's reading of a label is not a
person's (2026-11-03, HIR-132). The report now prints three numbers — the score, how many
skills were set aside unchecked, and how many items are still waiting in the hand-check
queue — because a score computed over a yardstick with holes in it should never be read
without knowing how many holes.

Recomputed under the rule, which settles HIR-139's question:

| | before | after |
| -- | -- | -- |
| New York (14 postings) | 0.739 precision, **0.846 F1**, 35 extras | 0.943 precision, **0.966 F1**, 6 extras |
| Berlin (15 postings) | 0.845 precision, **0.910 F1**, 37 extras | 0.922 precision, **0.953 F1**, 17 extras |
| gap | **−0.064 F1** ("clearly worse") | **+0.013 F1** (New York slightly ahead) |

Recall and requirement accuracy do not move: a set-aside skill was never in the yardstick,
so it was never a miss. 42 New York skills and 36 Berlin skills are set aside pending
hand-check; 62 and 142 items respectively are waiting in those queues. The unagreed extras
the HIR-139 entry reports per posting shrink with the same arithmetic — 2.5 and 2.5 before,
0.4 (New York) and 1.1 (Berlin) after — because most of those extras *were* the unsure
skills.

Scope. Skills only one labeller found, and skills neither found, are scored exactly as
before. Nothing about the extractor, the prompt or the taxonomy changes, and the held-out
eval's release-only rule is untouched. To undo: revert the HIR-159 commits — the rule is
reporting only, and no stored data depends on it.

This supersedes the measure described in the HIR-139 entry below, which was written against
the old rule: the numbers in that entry are the "before" column of the table above.

---

## 2026-11-04 — New York's 0.064 F1 gap is the measure, not the extractor (HIR-139)

New York's launch check scored 0.846 F1 against Berlin's 0.910. The gap is past the 0.05
the check calls "clearly worse", so HIR-132 filed a follow-up instead of undoing the
launch. **The verdict is that the extractor reads New York postings about as well as
Berlin's, and the gap is an artefact of how precision is calculated.** The launch itself
stands; nothing about extraction changes.

How that was settled. All 35 New York "unagreed extras" — skills the extractor stored that
the labeller panel did not *both* agree on — were classified by hand against the posting
text and against each labeller's own raw output:

| | New York | Berlin |
| -- | -- | -- |
| both panel labellers proposed it | 30 (86%) | 27 (73%) |
| exactly one proposed it | 2 (6%) | 1 (3%) |
| neither proposed it | 3 (9%) | 9 (24%) |
| corroborated by at least one labeller | **32/35 (91%)** | **28/37 (76%)** |

So 30 of New York's 35 extras are skills *both* labellers found; 29 of those were kept out
of the agreed yardstick only because at least one labeller flagged uncertainty, which sends
a label to the review queue. They are counted as extractor errors by the score and are not
errors. Of the three no labeller proposed, one is a defensible inference (`a-b-testing` from
"design and evaluate experiments" in a personalization role) and two are real mistakes:
`llm-orchestration` read from "orchestration" where the posting's own list is about
distributed systems and model serving, not LLMs; and `statistics` taken from the degree
clause "Master's or PhD in machine learning, computer science, statistics", which names a
field of study rather than a skill the job asks for. **Two real errors in 35 extras.**

By the same test Berlin is the worse of the two, not the better: 9 of its 37 extras had no
labeller behind them, and spot-checking those found the extractor right and the panel
simply short — the postings literally say "MCP" and "embeddings, vector search".

Why precision still fell. The extractor adds the same ~2.5 unagreed extras per posting in
both cities; New York postings carry roughly half as many agreed labels (7.1 against 13.7)
for those extras to be divided by, so the same behaviour scores worse. This is the "US
postings name fewer skills" effect already recorded for San Francisco on 2026-11-03
(HIR-12).

A second limit, equal in both cities: the yardstick is agreement only, so a skill one
labeller found counts as an extractor error. Precision here is a lower bound, not an error
rate — and the two runs are not even measured by the same panel, since the third checker
(`gemini-4-argon`) ran on New York only. Comparisons across cities therefore use the two
labellers both runs share.

What changed because of this: the launch check now prints agreed labels and unagreed extras
per posting next to F1, and says so when F1 falls while the extras count holds — the extras
count was flat across the two cities and F1 was not, so the pair separates an arithmetic gap
from a real one. To undo, revert the HIR-139 commits; the measure is reporting only and no
stored data depends on it.

Not done here: the two real errors are a Follow-up, not a fix. Changing the prompt or the
taxonomy was out of this ticket's scope, runs the dev eval first (HIR-133) and re-reads
every job on merge.

---

## 2026-11-03 — Adding a city is automated, and New York is the first one (HIR-132)

Two standing rules end here, both by Chandler's written decision on the HIR-132 ticket
("Adding a city is fully automated … Don't re-ask any of this"):

**Provenance of that decision, so nobody has to ask again (2026-11-04).** The HIR-132 PR
was held at `needs-chandler` because switching a city on is on the stop list and the only
authority for doing it unattended was a decision section on the ticket itself — and an
agent cannot clear the stop list by citing a rule change it made in the same PR. Nothing
available to an agent settles who wrote that section: Linear's edit history is not exposed
through the MCP, and the integration posts as Chandler's account, so an author name proves
nothing (every agent comment on HIR-132 reads as his). **Chandler confirmed in session on
2026-11-04 that the decision section is his and that he asked for it on 2026-11-03.** That
is the go; this paragraph is the record of it, per the 2026-11-03 HIR-110 rule that a go
has to be on the record. A future agent reads this entry, not the ticket, and does not
re-ask.

- **A city is no longer an exception by name.** The 2026-11-03 HIR-12 entry below says
  San Francisco is "the single exception" to a Germany-and-EU-remote scope and that an
  agent asked about any further non-German city "applies this rule as a *no*". That line
  is superseded: **New York is active too**, and the scope rule is now "Germany, EU-remote,
  and the cities Chandler has turned on" — SF and NYC so far. `geo.ACTIVE_CITIES` is
  `("Berlin", "Remote (EU)", "San Francisco", "New York")`.
- **A board no longer waits for a person to approve it.** The 2026-10-19 rule
  ("Approval is manual (`--add` / `--reject`). A board joins the daily poll … only after a
  person looks at it") is superseded for city launches: `discover-boards --launch <city>`
  applies the written policy below itself and reports afterwards.

**The board policy, which is Chandler's SF choices (HIR-123) turned into code.**

- **Add** every board with **5 or more** roles that pass the title filter and map to the
  city being launched.
- **Skip** recruitment agencies and job aggregators — only employers' own boards.
- **Leave the rest unrecorded.** A board with 1–4 roles is neither added nor rejected:
  rejecting hides it from every future search for good, and a small board may grow
  (the "skipping is not rejecting" entry of 2026-11-03, HIR-123).
- **Two caps, and hitting either one stops the launch and reports instead of adding:**
  more than **€10** of one-time model reading, or more than **5,000** postings added to
  the daily download.

**Why automated at all.** The approval step was the whole cost of a city. Chandler made the
same call 67 times for SF (HIR-123) and the policy above is just what he did; a rule he can
write down is a rule an agent can apply, and the report afterwards is what he actually reads.

**What this does not change.** No extractor, prompt or taxonomy change, so no
`extractor_version` bump — a NYC posting is read by the same prompt as a Berlin one, exactly
as the HIR-12 entry recorded for SF. The site still shows every city it collects (HIR-12,
"Hiding SF from other people using the site is not required"), so NYC appears on the
dashboard as its own place because it is collected.

**The launch quality check is not a Golden.** A sample of NYC postings is labelled by the
three-family labeller panel and compared with what the extractor read, to catch "the
extractor reads US wording worse" early. Those labels are model-written and unreviewed, so
they are **not** Goldens: they land in the ordinary review queue for Chandler's 10–15%
spot-check and become Goldens only after it. The check never blocks or undoes a launch —
a bad result files a follow-up.

**What the first run of that check said (2026-11-04).** New York F1 **0.846** against a
Berlin run of the same panel at **0.910** — 0.064 apart, past the 0.05 the check calls
clearly worse, so HIR-139 is filed and the launch stands, exactly as the rule says.
Read it carefully, though: the gap is entirely precision (recall 0.990 vs 0.985,
requirement accuracy 1.000 vs 0.990), and the extractor adds **the same 2.5 unagreed
skills per posting in both cities** — 2.5 of 9.6 stored in New York, 2.5 of 15.9 in
Berlin. Precision divides by a New York posting's 7.1 agreed labels against Berlin's
13.7, which is the "US postings name fewer skills" effect already recorded for SF above,
not new noise. The non-Claude third labeller (`gemini-4-argon`), the one this ticket says
to weigh most, differed on 0 of 80 agreed New York labels.

**So precision against an agreement-only yardstick is a lower bound, not an error rate.**
Only what *both* labellers agreed counts as truth, so a skill one of them found scores as
an extractor error. That holds equally in both cities, which is why the comparison is worth
more than either number alone — and why HIR-139's first step is a person reading 35 of
those "extras" rather than any change to the extractor.

---

## 2026-11-03 — There is no merge queue on this repository; auto-merge replaces it (HIR-136)

HIR-124, earlier today, wrote a merge queue into AGENTS.md, both work-issue skills and the
reviewer agent: nothing merges directly to main, the reviewer enqueues, and the queue
builds each PR on top of the ones ahead of it, tests that combination and merges in order.
That queue was never switched on, and the entry said so — it ends "this needs *Require
merge queue* on in the `main` ruleset to do anything".

**It cannot be switched on. GitHub offers merge queues only on repositories owned by an
organization, and this one is owned by a personal account** — "Require merge queue" is not
in the ruleset's rule list at all, and `mergeQueue(branch:"main")` is null. So the rules
described a mechanism that does not exist here, and the reviewer, correctly refusing to
merge by hand when told to enqueue, labelled the first PR to reach it (#74) `needs-chandler`
for a reason that had nothing to do with the PR. Every autopilot PR after it would have
done the same.

**Chandler's call: reviewed work still merges without him** — the intent of HIR-124 stands,
only the mechanism changes. **GitHub auto-merge replaces the queue.** It works on personal
repositories, and "Allow auto-merge" is now on.

The reviewer's command is unchanged (`gh pr merge <n> --merge --auto`); what changes is
what it does and who owns being behind main.

- **With no queue, `--auto` is a plain auto-merge:** GitHub merges the PR as it stands the
  moment its conditions hold. Nothing is tested against the latest main first, and nothing
  is ordered. That protection is gone, and this entry is the record that we traded it away
  because the alternative was a queue we cannot have.
- **Being behind main is the reviewer's problem, not the worker's.** The `main` ruleset
  requires branches to be up to date before they merge (`strict_required_status_checks_policy`),
  so auto-merge will not fire on a branch behind main. The reviewer arms auto-merge, then
  brings the branch up to date (`gh api -X PUT repos/:owner/:repo/pulls/<n>/update-branch`),
  which re-runs the checks; auto-merge fires when they go green. **A worker still never
  merges main into its branch** — that is what produced the duplicate edits of 3 Nov, and
  moving it to the moment before the merge is the point. The worker's one case is still a
  real conflict: `update-branch` returns 422 and the PR goes back to its author.
- **Two reviewers can race:** each updates its branch, one merges first, the other is
  behind again. The reviewer updates at most **twice** and then labels the PR
  `needs-chandler` rather than looping — a PR losing an update race forever is the failure
  this bounds.

The `merge_group:` trigger stays in `ci.yml`. It is inert without a queue and costs
nothing, and leaving it means a future move to an organization-owned repository needs no CI
change.

Unchanged from HIR-124: an issue is claimed by setting it In Progress, ticket descriptions
are appended to and never replaced, every merge happens from the run that reviewed it, and
there is no timer backstop. Nothing about extraction, the taxonomy or the dashboard
changes, and no model call is involved.

---

## 2026-11-03 — Extractor and skill-list changes run the dev eval before they merge (HIR-133)

Skill-list versions v6 and v7 merged with no eval run at all. When v8 was finally measured
(HIR-128, earlier today) the only committed dev run to compare it with was v5's, three
changes back, so the small drop it showed could not be attributed to any one of them. It
turned out to be noise. A real regression would have been exactly as untraceable, and
overnight autopilot batches make the silent case the normal one — there is nobody there to
ask for the eval.

**So the eval is a gate, not a request.** Any diff touching `app/extract.py` or
`taxonomy/skills.json` runs `scripts/run_eval.py` on the dev split, pastes the score table
into the PR, and commits `evals/results/<run_id>/` in that same PR. Committing it is the
load-bearing half: the run a PR commits is the baseline the next one is measured against,
which is what removes the separate re-baseline step and the three-changes-back gap that
caused this. The full rule, with the one evidenced exemption for diffs that leave
`extractor_version` unchanged, is in AGENTS.md under "The eval gate".

**The trigger is a file list, deliberately, not a judgment.** "Does this change how the
model reads a posting?" is a question an agent can talk itself out of at 3am; "does the
diff touch these two paths?" is not. It over-triggers on docstring edits, and the
exemption handles those by printing both `extractor_version` strings rather than by
letting the agent assert that nothing changed.

`scripts/eval_table.py` exists so the table is the same table every time: it finds the
last committed dev run itself, compares every aggregate metric, and marks drops over the
0.02 stop line. Hand-rolled comparisons were the alternative and they would differ per
run, which defeats the point of a baseline. It shows every metric rather than a chosen
few, because the 0.02 stop line applies to any metric and a metric left out of the table
is a metric nobody gates on.

Held-out Goldens stay release-only (unchanged, HIR-55). This gate is the dev split.

---

## 2026-11-03 — The dev baseline moves to v8, and the top-10 dip that moved it is not a regression (HIR-128)

Taxonomy v8 shipped without an eval, on the reasoning that no dev-split Golden mentions any
of its seven entries. Run afterwards on request: `evals/results/20261103T174722Z_dev_x2-5b6ff30617/`
— 20 Goldens, 3 repeats, 60 live calls, `claude-sonnet-5-5`, **0 errors**. **It is now the
baseline the 0.02 rule compares against**, replacing the v5 run of 2026-11-01.

Against that v5 run: precision 0.881 → 0.875, recall 0.970 → 0.966, **f1 0.924 → 0.919**,
requirement accuracy 0.993 → 0.991, seniority 0.967 → 0.983, German 1.000 flat, degree
0.950 flat, production 0.950 flat, rank spearman 0.907 → 0.892, **top-10 overlap 0.800 →
0.767**.

**`top10_overlap` is down 0.033, past the 0.02 that AGENTS.md says to stop on, and it is
not this change.** Three reasons, recorded so it is not re-argued:

- **The old baseline was three taxonomy versions behind.** It ran at v5; v6 (HIR-97) and v7
  (HIR-101) both shipped without an eval, so the gap spans three changes rather than one.
  This is the cost of skipping the run on an alias-only change, and it is why the baseline
  is being moved rather than the dip investigated.
- **None of v8's seven entries appear in the regression at all.** The frequent extras are
  `testing` (12), `software-engineering` (6), `observability` (6), `tool-calling` (6),
  `data-pipelines` (6); the most-missed are `apis` (9) and `software-engineering` (9). Not
  one of `ansible`, `nccl`, `ray`, `bash`, `redis`, `sagemaker`, `temporal` is named on
  either list — as expected, since no dev Golden mentions them.
- **`top10_overlap` is the coarsest metric in the suite.** Ten slots, so one slot in one of
  three repeats moves the mean 0.033. Its min/max was 0.700/0.800 against a flat 0.800, so
  the whole delta is one skill in one run. `f1`, which actually tracks extraction quality,
  moved 0.005.

**The rule worth carrying:** skipping the eval on a taxonomy change is cheap once and
expensive twice. Two skipped runs turned a 0.005 F1 drift into a 0.033 reading on a coarse
metric that no longer attributed to anything, and the only way back was a fresh baseline.
A taxonomy-only change can still skip the run, but the next change then inherits the debt.

**The Ray/Ray Serve split was checked separately, outside the eval**, because `ray` appears
in no dev Golden — only in held-out `golden_035`, which is not run outside a release point.
Four stored postings were re-extracted under v8 against a copy of the database: the Nebius
posting that names both got `ray-serve` *required* (from "Ray Serve" in its must-haves) **and**
`ray` *nice_to_have* (from the bare "Ray" in its open-source list), and three postings naming
only the framework got `ray` alone. **No posting had `ray` displace `ray-serve`.** One
observation rather than a fault: a fourth posting says "Ray Train", and the model mapped it
to `ray` rather than proposing a new label, so an unnamed Ray component folds into the
parent instead of reaching the review queue. `Ray Train`, `Ray Tune` and `Ray Data` all
resolve to nothing in the taxonomy, so nothing is folded silently by the resolver itself.

## 2026-11-03 — Taxonomy v8: seven entries from the San Francisco queue, and the queue's count was inflated (HIR-128)

HIR-128 reported 18 proposed labels at or over the 2026-10-20 bar of 3 jobs after HIR-123
read the 264 San Francisco postings. **Nine of the 18 already had entries.** `cuda`,
`kserve`, `ray-serve`, `speculative-decoding`, `spring-boot`, `triton-inference-server`,
`nvidia-dynamo`, `opentelemetry` and `quantization` all landed in taxonomy v5 (HIR-72,
2026-11-01); their pending rows came from 165 jobs still stamped at the v4-era
`extractor_version`. Counting only jobs at the current stamp, all nine sat at **zero**
pending rows — and an extraction run during this ticket proved it: with all 528 stored
jobs now at the current stamp, those nine labels have left the queue entirely without
anyone reviewing them.

**So the queue is only a frequency counter for jobs read under the current taxonomy.** A
label whose rows all predate the entry that covers it is not evidence of a gap; it is a
job awaiting re-extraction. Read the queue with `job.extracted_version` joined in, or the
same batch gets reviewed twice. That is the finding worth carrying forward from this
ticket.

**Seven entries land, taxonomy v8, 217 skills:** `ansible`, `nccl`, `ray`, `bash`,
`redis`, `sagemaker` and `temporal`. They were selected at 5/4/3/3/3/3/3 jobs counting
only the then-current stamp, which was the conservative reading; after the re-extraction
described above they stand at 6/4/4/4/6/3/5. Bare `triton` stays out at 1 job.

**`fsdp` and `datadog` crossed the bar mid-ticket and are not in v8** (HIR-131). Both read
2 jobs when this change was scoped and 3 after the re-extraction. They are left out
deliberately rather than quietly added: the seven above are what the brief named, and two
extra rows on the chart is a visible change that should arrive as its own reviewable
ticket. Neither is a fresh judgment call — HIR-72's triage already recorded `datadog`
[`observability`], and `fsdp` is a distributed-training technique like `deepspeed`.

**`nccl` lands although 2026-11-02 listed it under "What stays out, and why, so it is not
re-litigated".** That list's stated reason for the 45 golden_035 names was frequency —
"so one posting's vocabulary does not become 45 chart rows with document frequency 1" —
and NCCL now has 4 distinct postings in the live queue, which is where 2026-10-20 says
frequency is counted. "Not re-litigated" protects the reasoning, and the reasoning was
frequency; applying the standing rule to a count that has since changed is what the rule
is for, not a reversal of the decision. The same entry's "promotion stays available" is
the precedent. Its parent is `distributed-training`: the exclusion paragraph said "the
level above each of them is a decided id", but the id it meant for NCCL (`gpu-computing`,
proposed on HIR-72) never landed, so the nearest entry that does exist carries it.

**Bare `triton` still resolves to nothing, and a higher count would not change that.**
Its exclusion rests on ambiguity between NVIDIA's Triton Inference Server and OpenAI's
Triton kernel language, not on frequency (2026-10-20, reaffirmed 2026-11-01). It is at 1
job anyway. The one posting behind it quotes "CUDA or Triton", which is the kernel
language — the ambiguity is real and live, so the rows stay pending on purpose.

**`ray-serve` is reparented from `["model-serving", "distributed-systems"]` to
`["model-serving", "ray"]`,** which is the shape HIR-72's triage comment recorded
(`ray` [distributed-systems] · `ray-serve` [ray]). It landed with `distributed-systems`
only because `ray` was at 2 jobs and did not land with it. `distributed-systems` is still
an ancestor through `ray`, so nothing a parent walk sees has changed. The issue called the
Ray/Ray Serve shape a judgment call; a recorded decision already covered it, so the rule
won (AGENTS.md, "An existing rule is never a question").

**`redis` takes no parent and `ray` takes `distributed-systems`,** both as recorded on
HIR-72. The four names that pre-date no decision are `ansible` [`infrastructure-as-code`,
following `terraform`], `sagemaker` [`aws`, following `vertex-ai` under `gcp`], `temporal`
[`distributed-systems`] and `bash` [no parent, as every other language entry].
`temporal` is the durable-execution engine, capitalised in all three postings, not
"temporal" as a property of data.

**Three Golden labels added to two held-out Goldens**, on the 2026-10-20 precedent that a
label the taxonomy could not express before is a missing gold label rather than tuning,
applied to the same file on 2026-11-02. golden_031 gains `redis`, golden_035 gains `ray`
and `nccl`. Each sits in an ask, per evals/LABELING.md; `requirement` follows the section
rule. Nothing was deleted or rewritten.

**Every job re-extracts on the next poll** — `extractor_version` hashes the system prompt,
which contains the taxonomy, so seven entries invalidate every stamp. About €6 at 510
stored jobs. Per AGENTS.md the merge is the approval. **No eval was run:** no dev-split
Golden mentions any of the seven, so a dev run could not show a change attributable to
this edit, and the stamp change makes it incomparable to the last committed run either
way. The last two taxonomy changes (v6, v7) shipped the same way.

## 2026-11-03 — Dedup gains an exact-title path: company + identical title is enough (HIR-108)

HIR-108 reported 11 pairs stored twice under the same company and title, found on
2026-11-02. Re-measuring on the live DB a day later (polls and HIR-104's cleanup had run
in between) found 9 current pairs, not 11 — three of the original ids now point at
unrelated postings or no longer exist, and one new pair (eGroup, 77+240) had arrived since.
The table below is what is true now, not what the issue originally listed:

| company | title | ids | Jaccard | containment | sources |
| --- | --- | --- | --- | --- | --- |
| BWI GmbH | Senior AI Engineer (w/m/d) | 184, 185 | 0.302 | 0.507 | arbeitsagentur / arbeitsagentur |
| BWI GmbH | Senior AI Engineer - Agentic Software Development (w/m/d) | 106, 109 | 0.007 | 0.143 | arbeitsagentur / arbeitsagentur |
| BWI GmbH | Senior AI Platform Engineer (w/m/d) | 101, 105 | 0.008 | 0.135 | arbeitsagentur / arbeitsagentur |
| Doctolib | Principal Machine Learning Engineer - Applied AI & LLMs (x/f/m) | 4, 154 | 0.640 | 0.854 | arbeitnow / greenhouse |
| Nebius | Senior Machine Learning Engineer, LLM Inference Optimization | 196, 219 | 0.550 | 0.782 | arbeitnow / greenhouse |
| Nebius | Staff Machine Learning Engineer, LLM Inference Optimization | 195, 220 | 0.481 | 0.810 | arbeitnow / greenhouse |
| commercetools | AI Engineer (m/f/x) | 2, 16 | 0.603 | 0.882 | arbeitnow / startup_jobs |
| eGroup | (Senior) AI Web & GTM Engineer (f/m/d) | 78, 188 | 0.362 | 0.892 | url+recruitee / jsearch |
| eGroup | AI Product Engineer (f/m/d) | 77, 240 | 0.619 | **0.997** | url / recruitee |

**What the BWI pairs actually are.** The issue flagged these three as the ones most likely
to be real separate listings, so they were the ones to check by hand, not by threshold.
Reading job 106 and 109 side by side: 106 is Arbeitsagentur's own short auto-generated
summary of the posting (285 characters, machine-paraphrased, not an excerpt), 109 is the
full scraped page for the identical job. Same for 101/105 and 184/185. They are the same
posting, not separate listings — the near-zero Jaccard and containment are an artifact of
Arbeitsagentur sometimes storing a paraphrase instead of the page, not evidence of two
different roles. No text measure can bridge a paraphrase to the text it paraphrases; HIR-113's
containment path, built for a literal-prefix snippet, does not and cannot catch this either
(containment tops out at 0.507 here, nowhere near its 0.9 guard).

**The other five pairs (Doctolib, Nebius ×2, commercetools, eGroup's first pair) are
ordinary same-posting-via-different-feeds cases** — containment 0.78–0.89, just under
HIR-113's 0.9 guard, almost certainly boilerplate differences between how `arbeitnow`,
`greenhouse`, `startup_jobs`, `url`/`recruitee` and `jsearch` each strip or wrap the same
HTML. Lowering the containment or Jaccard threshold far enough to reach 0.78 would still
miss the BWI pairs (0.135–0.507) and starts to risk the kind of false merge HIR-113's title
guard exists to prevent. Stripping each feed's specific boilerplate is a real option but a
much bigger, source-by-source change for a 3% chart effect.

**The rule: same `company_key` and byte-identical `title_key` is sufficient on its own, no
text test required.** `dedup.is_same_posting` now checks this first, before Jaccard and
before the containment path. It is the only candidate the measurements support — nothing
short of ignoring the text can bridge a 0.007 Jaccard pair that is, by inspection, the same
job. The existing invariant, "a title never carries a match alone", still holds in the
sense that matters: the title only carries a match when the *company also matches*, and
only when the title is *exactly* identical after normalization, not merely similar — a
same-company, similar-but-not-identical title (the pplwise case, HIR-113) still requires
text corroboration exactly as before. Checked against the full live set: this rule adds
exactly these 9 pairs as merges (8 new, plus the eGroup pair HIR-113's containment path
already caught) and changes no other existing match, because it only ever fires when both
the company and the full normalized title string already agree — a much narrower
precondition than the containment path's.

**The real BWI pair (106 + 109) is the regression fixture** — `bwi_auto_summary` and
`bwi_full` in `tests/fixtures/dedup/real_cases.json` — because it is the case no threshold
tuning could have caught, and the case the issue most worried the fix might get wrong in
the other direction.

**Not done here: merging the 9 pairs already stored.** Deleting or rewriting stored jobs is
on the AGENTS.md stop list. Like HIR-113's two pairs before it, these stay split until
Chandler says to merge them; the shape of that merge (repoint `job_source`, keep the
longer `description_text`, drop the loser's `skill_mention`/`extraction_reject`, re-extract
if the kept text changed) is recorded in the 2026-11-03 HIR-113 entry above and applies
unchanged here. The fix in this entry stops the pattern from recurring; it does not clean
up what already recurred.

---

## 2026-11-03 — Several orchestrators at once: claims, a merge queue, append-only tickets (HIR-124)

Running more than one `/work-issue-orchestrator` at a time is what we want, and the batch
of 3 Nov showed what breaks without it being designed for. Each orchestrator sees only its
own workers, so two of them went wrong in two different ways: two agents each sent a whole
new description for HIR-112 and erased the other's edit, and eleven PRs merged into main
inside eighty minutes while workers were merging main into their branches to get reviewed,
which produced duplicate edits and cost a whole extra PR (#64) to sort out.

**The fix is to stop inventing shared state and use the state that is already shared.**
Two things are visible to every session: the Linear issue status, and the open pull
requests. So those are the claim and the lock.

- **An issue is claimed by setting it In Progress**, as a session's first write — before
  the brief, before the worktree. Orchestrators skip In Progress issues when picking. An
  issue that has been read but not claimed is an issue a second orchestrator will start a
  second worker on.
- **The open PRs say which files are taken.** Before starting each worker (not once per
  batch) the orchestrator lists every open PR's changed files and holds back any issue
  that would touch one, or a hot spot an open PR touches — whoever opened it. A session's
  own batch table is not shared state and never decides a collision.
- **Nothing merges directly to main; it goes through GitHub's merge queue.** The reviewer
  enqueues (`gh pr merge --merge --auto`) and the queue builds each PR on top of the ones
  ahead of it, runs the required checks on that combination, and merges in order. This is
  what lets the rebasing stop: *workers no longer merge main into their branch before
  review, and no agent updates a branch to force a merge through.* Being behind main is the
  queue's problem. A conflict the queue can't resolve drops the PR back out to its author,
  which is the one case that is still the worker's.
- **Ticket descriptions are appended to, never replaced.** Any agent changing a
  description it did not write this session uses `save_issue`'s `patch` (`prepend` for a
  status line, `append`/`insert_after` elsewhere) or adds a comment. The HIR-112 overwrite
  is impossible that way.

**Rejected: a lane per orchestrator** (a reserved slice of the repo or the issue list each
one owns). It needs coordination to hand out the lanes, which is the problem it was meant
to solve, and claims plus the queue already cover the two failures we actually saw. If
those turn out not to be enough, lanes are the next thing to try.

**The scheduled cloud reviewer is retired** — disabled, not deleted. Merges now happen
from the run that did the review: an autopilot `/work-issue` waits for CI at the end of
its own run and starts a fresh `reviewer` agent on the PR it just opened, and inside an
orchestrator the orchestrator does that. There is deliberately **no timer backstop**: a
run that stops before merging labels its PR `needs-chandler` and says so, because a PR
quietly waiting for a nightly job is how work goes missing. Enqueueing needs GraphQL,
which works from a Mac session and not from a scheduled cloud run, so this is also the
only place it can happen.

This needs **"Require merge queue" on in the `main` ruleset** to do anything; until that
is on, `--auto` behaves as a plain auto-merge and the old behaviour continues. Nothing
about extraction, the taxonomy or the dashboard changes, and no model call is involved.

---

## 2026-11-03 — Skipping a board is not rejecting it (HIR-123)

A `discover-boards` run after San Francisco went active surfaced 69 boards we don't poll,
carrying 400 roles that pass the title and city filters (379 SF, 14 EU-remote, 7 Berlin).
Chandler's pick: **the 16 boards carrying five or more relevant roles** — openai,
anthropic, brainco, databricks, doordashusa, scaleai, mercor, distyl, faire, figma,
togetherai, chime, cognition, plaid, egen, gleanwork — 303 of the 400 roles. The long tail
of 53 boards carried 1–4 roles each: about a quarter of the roles for roughly half the
daily fetching, and too few postings each to move any skill's share.

**The rule this settles: a board we decline is left out of both files, not rejected.**
`config/boards_rejected.json` means *never suggest this again* (2026-10-19), which is the
wrong verdict on a company that is small today and may hire properly next quarter. So the
51 declined boards are in neither `config/feeds.json` nor the rejected list. The price is
accepted deliberately: every future `discover-boards` run re-reports them, and that noise
is cheaper than permanently blinding the search to 51 companies. Do not "tidy up" by
rejecting them.

**Rejection is for boards whose problem will not change.** Two JOIN boards were rejected
with a reason — `worldwideplacementlimitedcouk` and `verwaltungssprungcom` — because they
are recruitment agencies and job portals rather than single employers: the postings they
carry are not written by the hiring company, so they distort skill counts the way the
aggregator headline rows did (HIR-104). Being an agency is a permanent property, so a
permanent rejection is the right record.

**This replaced the issue's own "done when",** which had asked for every board not added
to be rejected. Where an issue's completion condition and this reasoning disagree, this
entry wins.

## 2026-11-03 — learn4good's headline shape is also dropped, not repaired (HIR-107)

HIR-104 found two more stored "Primetime" phantom-employer rows while removing the
JobLeads ones: job 248 ("AI/ML Engineer arbeitnow Melotech", duplicate of job 12) and job
327 ("AI Application Engineer – AI Products (LLM & RAG) arbeitnow Machine Learning
Reply" with a trailing fragment, duplicate of jobs 59/238). Same aggregator employer name,
different publisher (learn4good) and a different shape: no trailing date — `jsearch.
is_headline` only caught JobLeads's "ends in a date" signature — the board's own name is
wedged between the real title and the real company instead, and learn4good's listing date
is in the description body, not the title.

**Detection widens to a second signature, not a replacement.** `is_headline` keeps the
trailing-date test unchanged (still sufficient alone — a real title never ends in a date)
and adds: the title has `arbeitnow` wedged with text on both sides, **and**
`employer_name` is a known aggregator identity (so far only ever "Primetime", seen on both
shapes). The wedge alone is rejected as a signature — a real posting can legitimately
mention the arbeitnow board by name — which is why `is_headline` now also takes
`employer_name`; `scripts/remove_headline_jobs.py` passes the stored `job.company` the
same way.

**Recovering the real title and company from the wedge is rejected here too.** The
build asked whether HIR-96's "drop, don't repair" answer for JobLeads still holds for
learn4good's simpler-looking `<title> arbeitnow <company>` shape. It does: job 327's own
text already shows the split is not always clean (a trailing fragment sits after the
company name that the clean stored duplicate doesn't have), so a parsed-out title risks
being subtly wrong rather than simply dropped — stored as a second, messier near-duplicate
that dedup's text-similarity check might not even catch, which is worse than one dropped
posting. Undo: if a cleaner pattern turns up later, recovery can be added as its own
change; nothing here forecloses it.

**No fixture existed for this shape; recording a live one was not worth the budget.**
`tests/fixtures/feeds/jsearch_learn4good.json` is hand-built from the two titles HIR-107
quotes from the live database (job 327's reconstructed from the clean real title in jobs
59/238, since the issue's own quote of the headline carries what reads as a
markdown-escaping artifact — stray semicolons and a missing paren — not real data), the
same way `jsearch.json` is already hand-built for shapes `jsearch_recorded.json` doesn't
cover. JSearch's plan is a hard 200-requests-a-month budget; spending one to record a
fixture for a bug fix wasn't asked for.

**Jobs 248 and 327 are not deleted by this change.** Same as HIR-104: deleting stored jobs
needs Chandler's go. Once given, `scripts/remove_headline_jobs.py --dry-run` will now
select both (its `is_headline` call was widened the same way), to confirm before a real
run.

---

## 2026-11-03 — One pre-HIR-98 row is deleted; the German ones wait for HIR-102 (HIR-110)

**This entry settles one row, not a class.** No standing permission is recorded here: an
agent that finds another stored row it thinks should go still asks, because "deleting or
rewriting stored jobs" is on the AGENTS.md stop list with no count threshold. The decider
was asked twice whether a one-row scope escapes that list and said it does not — a deleted
row is not reversed by a commit.

**The contamination window.** Until 2026-11-01 ~18:06 UTC `app/sources/arbeitnow.py`
appended "(remote, Germany)" to the location of every posting the feed marked remote,
whatever its real place, so `geo._EU_WIDE` matched the injected word and all of them were
stored as `Remote (EU)` — ingest's city filter could never drop them (HIR-98 fixed intake
only).

**Measured on the 2026-11-03T14:05:51Z backup:** 390 stored jobs, 60 filed as
`Remote (EU)`, 23 rows still carrying the stamp. Re-running today's adapter and
`geo.active_place` over each row's real location leaves **three** candidates, and
**exactly one** of them is placed wrongly by today's rules:

- **job 278** — Lightly AG, "AI Research Scientist – Scientific Evaluation (ML/AI)",
  3 skill mentions, stored `location_raw` **`'Zürich (remote, Germany)'`**. That string is
  the clearest surviving artifact of the bug: Zürich is in Switzerland, and nothing but the
  adapter put "Germany" next to it. Remote tied to one non-EU country, which the EU-remote
  rule of 2026-10-26 does not collect. **Deleted, with its 3 skill mentions, 0 extraction
  rejects and its feed-source row** (2026-11-03). The dry run immediately before it listed
  the same three candidates and removed nothing, so the selector had not drifted between
  measuring and running:

  ```
  removed job 278: 'Lightly AG' — 'AI Research Scientist – Scientific Evaluation (ML/AI)'
    ['Zürich (remote, Germany)' -> today None] (3 mentions, 0 rejects)
  CANDIDATE job 275 (not confirmed): 'hurra.com' — 'Freelance Full-Stack Developer | …'
    ['Stuttgart' -> today None]
  CANDIDATE job 339 (not confirmed): 'Pentadoc Gruppe' — 'Working Student (m/f/d) - AI Engineering'
    ['Würzburg' -> today None]
  removed: 1 job(s), 3 skill mention(s); candidates left: 2
  ```

  Pre-deletion state, if it ever has to come back:
  `gs://hiring-radar-512318-backups/db/hiring-radar-2026-11-03T140551Z.db.gz`
  (11,134,109 bytes, 2026-11-03T14:05:53Z).
- **jobs 275 (Stuttgart) and 339 (Würzburg) were deliberately kept**, and the run above
  shows them reported as candidates rather than removed. They are remote work at untracked
  *German* cities, which the 2026-10-26 rule counts as postings a Berlin resident can take,
  so they are not damage — they only *look* like the Zürich row to the code, because `geo`
  has no notion of "this place is in Germany". Whether to collect that shape is **HIR-102**,
  and it stays open; until it is decided these two rows stay. **A later reader should not
  read "2 candidates left" as unfinished work**: leaving them is the decision, not a
  shortfall, and this is the precedent for the next one.
- Rows stamped by `app/sources/startup_jobs.py` are not candidates at all: it builds the
  same string out of the feed's own `location.country`, which was never fabricated. One
  such row (381, Berlin) was stored *after* the fix and is correct.

**A place is never blanked to hide a row.** Nulling `city` was the third option and is the
worst of the three: it rewrites stored data and changes nothing anyone sees, because
`queries.job_set_clause` constrains `j.city` only when a city filter is chosen and the
default view chooses none. So the row would keep counting on the chart while the stored
data became less true.

**The selector is the rule, not a row id.** `scripts/remove_pre_hir98_remote_jobs.py`
strips the stamp, runs the bare location back through the current adapter and
`geo.active_place`, and only then offers a row for deletion — so it cannot remove a row the
current code would have kept, and it stays correct if ids move between reading the database
and running it. It still requires `--confirm <id>` and refuses an id that is not a
candidate, because of the German-city judgment above. Same pattern as
`scripts/remove_headline_jobs.py` (2026-11-02).

**What the earlier record got wrong.** The 2026-10-26 entry describes the arbeitnow
"(remote, Germany)" mapping as a deliberate part of EU-remote collection; HIR-98 removed it
as a bug five days later without amending that entry. The removal is right — the feed
carries Swiss, Dutch and UK postings, so the country was being invented — and that clause
of the 2026-10-26 entry no longer holds. The EU-remote rules themselves are unchanged.

**Provenance of the go, so nobody has to guess.** Chandler chose this option in a Claude
Code session's question prompt; it reached this ticket as a comment written by the
orchestrator agent rather than typed by him (HIR-110, 2026-11-03 13:36Z). The working agent
refused to act on the relay until it was on the record, and **Chandler ran the deletion
himself on the VM** — no agent executed it.

**What that cost, and why it was right.** Three agent sessions could not carry out this
one-row delete: the permission layer refused the production read (`[Production Reads]`),
the backup (`[Remote Shell Writes]`) and even the no-op dry run on the VM, and an attempt to
write a blanket "no further ask" rule into this log was refused as `[Instruction
Poisoning]`. Every one of those refusals was correct — a stop-list item was being
approached on a relayed go. The lesson is not to loosen the controls but to **say in the
brief, up front, when a ticket ends in a production write**, so the hand-off to a person is
planned rather than discovered at the last step. HIR-110's brief promised a count and a
stop; it should also have said that whatever followed would need someone at a terminal.

---

## 2026-11-03 — San Francisco is active: the one exception to a Germany-only scope (HIR-12)

Collection is switched on for San Francisco, so `geo.ACTIVE_CITIES` is now
`("Berlin", "Remote (EU)", "San Francisco")`. The gate this waited on — "SF only after
Berlin extraction passes the held-out eval" (2026-10-19, below) — is met: HIR-70 built the
26 held-out Goldens, a person read a 30-label sample of them with 0 errors (HIR-92), and
the 2026-10-30 held-out run reads F1 0.919 / requirement accuracy 0.968
(`evals/results/20261030T123219Z_heldout_x2-2e0cac6944`). Chandler called it unblocked on
2026-11-03.

- **The scope rule, stated once so it is never re-argued.** hiring-radar collects Germany
  and EU-remote. **San Francisco is the single exception**, decided by Chandler on
  2026-11-03, for one reason: comparing two markets for the same skill is the product's
  point, and SF is where the volume is. An agent asked whether some other non-German city
  may be added applies this rule as a *no* — the exception is SF by name, not "non-German
  cities are fine now". Turning a further city on stays on the AGENTS.md stop list.
- **Hiding SF from other people using the site is not required.** Also Chandler's call:
  the site shows every city it collects, and nobody will spend time on a per-viewer scope.
- **Board discovery searches for SF too.** `config/discover.json` gains two SF queries
  next to the two Berlin ones, so a `discover-boards` run surfaces SF boards instead of
  judging every SF posting irrelevant. That doubles a run's Brave searches (domains ×
  queries), from 10 to 20 — about 10 cents at $5/1,000.
- **What does not change.** The dashboard already had the San Francisco button, the
  per-city counts and compare mode (`PLACES` in `web/src/format.js` has listed SF since
  the compare build); until now they simply had no SF job to show. No extractor change, no
  taxonomy change, no `extractor_version` bump — SF postings are read by the same prompt
  as Berlin ones.
- **Job 140** (Intercom, SF, polled 2026-10-19) was kept in the DB when SF was switched
  off and is in reach again. It is one row; polls will mark it still-listed or not on
  their own.

**The spot-check (2026-11-03, HIR-12).** 12 SF postings from four boards — a frontier lab
(ashby:openai), a lab with a commercial org (greenhouse:anthropic), a non-AI company hiring
AI roles (greenhouse:asana) and a startup (ashby:distyl) — ingested into a scratch database
and extracted with the current prompt and taxonomy (`x2-5068a71f9d`). 73 mentions,
**0 proposed skills, 0 validation rejects, 0 failures**: on this sample US wording opens no
taxonomy gap, which was the thing worth checking.

- **Skill density is lower than Berlin's, and the postings explain most of it.**
  6.1 mentions per SF posting against 23.7 on six stored Berlin postings re-extracted with
  the same version, at the same description length (mean ~6.7k characters both). The SF
  postings name far fewer skills verbatim to begin with: a literal label-and-alias scan
  finds ~8 taxonomy skills named per SF posting against ~26 per Berlin posting. SF research,
  architect and platform roles describe the work; Berlin data-science roles list a stack.
- **The one zero-skill posting is a correct zero.** Asana's "Software Engineer - AI
  Teammates Platform" asks for "2+ years working within large, well-maintained codebases",
  communication and "curiosity about AI tools" — no concrete skill to extract. Berlin's
  corpus runs 8 zero-skill jobs in 244.
- **What this does not establish.** 12 postings cannot separate "SF postings ask for fewer
  named skills" from "the extractor reads US wording less well". Only labeled SF Goldens
  measure that, and there are none — every Golden is a Berlin posting. Until then, read a
  Berlin-vs-SF skill-share comparison as a comparison of how the two markets *write*
  postings as much as of what they ask for.

---

## 2026-11-03 — Dedup gains a containment path, guarded by the title (HIR-113)

Cloover appeared three times in the job list. Pulling the rows settled what happened — and
it was two different things, not one:

| pair | Jaccard | containment | what it is |
| --- | --- | --- | --- |
| 76 + 231 | 0.683 | **1.000** | the same posting; one source stored a shorter extract |
| 206 + 76 | 0.013 | 0.033 | the same posting **in German** |
| 206 + 231 | 0.011 | 0.022 | likewise |

**The near miss.** Job 76's text is a literal prefix of job 231's: every one of its 675
shingles is in 231. Jaccard still read 0.683, under the 0.7 threshold, because it divides
by the *union*, which grows with the longer text. So the measure was working as designed and
the design was wrong for this case. `dedup.containment` — `|A∩B| / min(|A|,|B|)` — reads
1.000, and `is_same_posting` now accepts either path.

**Why the containment path needs three guards, not one.** Containment ≥ 0.9 on its own
breaks the invariant that two different roles at one company never merge. Checked over all
246 stored jobs it would have merged pplwise's "AI engineer in manufacturing" with their
"Senior AI / Machine Learning Engineer" at containment 0.931 — a recruiter whose postings
share most of their boilerplate. Two genuinely different jobs. So the path requires all of:

- containment ≥ 0.9; **and**
- the shorter text at least 60 shingles (~60 words), because less than that cannot
  establish identity; **and**
- every word of the shorter title present in the longer title.

The title is a *supporting* signal only — `test_a_matching_title_alone_never_merges` pins
that identical titles with unrelated text still do not merge. With all three, the rule adds
exactly two merges across the stored set (Cloover 76+231, eGroup 77+240), both genuine
duplicates, and changes no existing merge. Those numbers, and the four real postings behind
them, are in `tests/fixtures/dedup/real_cases.json`.

**The German translation is a known limit, not a fix.** No shingle measure over words can
see that job 206 is job 231 in German; both read under 0.04. Catching it needs a different
signal (same company + same source + same posted date, or a translation step), which is its
own ticket — HIR-117 — not a threshold change.

**The rows already split stay split.** Changing stored jobs is Chandler's call, so nothing
was rewritten here; the fix stops *new* duplicates only. When it is wanted, merging the two
pairs above means, for each: repoint the loser's `job_source` rows at the winner, take
`min(first_seen)` and `max(last_seen)`, drop the loser's `skill_mention` and
`extraction_reject` rows (the winner's extraction stands; the FTS triggers follow the
delete), and delete the loser. Keep the longer description — it is the one the extractor
should read. That is a `scripts/` one-off with `--dry-run`, in the shape of
`scripts/remove_headline_jobs.py`, and the three Cloover rows are only two merges, so doing
it by hand is also reasonable.

## 2026-11-03 — Best fit sorts on a lower bound, not the ratio (HIR-113)

The first live list had Pentadoc first at `100% · 2/2`, above PharmaHera at 6/8 and
Deloitte at 10/14. Two matched skills is not evidence of a perfect fit; it is evidence of
almost nothing. Ranking on the raw ratio rewards exactly the postings we know least about,
and short required-skill lists are usually thin extractions rather than genuinely simple
jobs.

So `rankJobs` orders on the **Wilson score interval's lower bound** of covered/total
instead, and `fit()` returns it as `rank_score` beside the plain `score`. The three rows
above become 0.45, 0.41 and 0.34 — the order a person would pick by eye.

- **Why a lower bound rather than a smoothed ratio.** It answers the question the list is
  actually asking: given this much evidence, how good can we be confident the fit is? A
  prior-based smoothing (add-k) would do something similar, but needs a k chosen out of
  thin air; the bound needs only a confidence level, and the same method is already used on
  PatternAI's eval rates, so the two read alike.
- **Why z = 1.96.** The conventional 95% level, and the number already in use for those
  eval rates. Nothing here is sensitive to the exact value — it sets how hard small
  denominators are penalised, and 1.96 reproduces the ordering a person reads off the
  screenshot. One constant, `Z`, so there is one place to change it.
- **The badge did not change.** A row still reads `100% · 2/2`, because that *is* what the
  posting asked and what the profile covers; inventing a "34%" badge would be telling the
  person their two-for-two match is a third of a fit. `score` is for showing, `rank_score`
  is for ordering, and the return shape says so. Alerts (HIR-19) and the Advisor sort on
  `rank_score` so every surface agrees.
- **Nothing else about the order moved.** Gated-out jobs still sort below everything in
  reach; a job with no required skills to judge still sorts last among the ungated; the
  quarter-weighted nice-to-have share is still a separate, lower tie-break.

## 2026-11-03 — A title can name a level (HIR-113)

HIR-51 said a posting that names no level never gates, because `null` is the extractor's
safe error. On the live list that turned out to be the wrong default for one shape of
posting: "(Senior) AI Web & GTM Engineer", "Senior Consultant AI Engineer", "Staff
Engineer…", "Principal Software Engineer…" all reached the browser with no stored level,
so none of them gated, and they sat at the top of a list filtered to Mid — the exact jobs
the filter was meant to push down.

So when a job stores no level, `jobSeniority` in `web/src/profile.js` reads the title:
Senior, Staff, Principal, Lead or Head as a whole word means `senior`, and Junior,
Werkstudent, Working Student or Intern means `junior`. Four things about that:

- **A stored level still wins.** The extractor read the whole posting; the title is one
  line of it. When they disagree the body is the better evidence, so "(Senior) AI Web & GTM
  Engineer" stored as `mid` stays `mid` and does not gate a Mid profile. This is why the
  change fixes fewer rows than the screenshot suggests, and why the extractor's own
  behaviour on bracketed "(Senior)" is a separate ticket rather than something papered over
  here.
- **Whole words only, and a short list.** `\b(senior|staff|principal|lead|head)\b` —
  so "Internal Tools Engineer" is not an internship and "Leading Edge AI" is not a Lead. The
  list is only the words HIR-113 names. A wrong guess here *hides a job*, which is worse
  than letting one sort too high, so the list stays short rather than clever.
- **A title that names two levels names none.** "Junior to Lead AI Engineer" returns
  `null` and never gates. Ambiguous is treated exactly like silent.
- **The badge still names a level.** A row gated on its title alone would otherwise show a
  blank word, because the row's own `seniority` is null; `JobList.jsx` asks `profile.js`
  for the effective level instead of reading the field.

Browser-only and deterministic: no model call, no stored data, nothing re-extracted.

## 2026-11-03 — arbeitnow's "Remote job" is a placeholder, and its URL carries the place (HIR-111)

A large block of arbeitnow's remote postings sends the literal string `"Remote job"` as the
location. Every word of it is filler to `geo` ("remote", "job"), so it read as a remote
posting naming no region at all and became `Remote (EU)` wherever the job really was — a
Zürich role, an Amsterdam role, the UK-local Bromcom role from HIR-110. HIR-98 fixed the
bare-place-name case ("Bromley" passes through and gets dropped) and never saw this one.
Measured over one live 5-page poll (1410 postings): 20 carry the placeholder, 3 of those also
pass the title filter and were stored, all 3 as `Remote (EU)` and none of them EU-wide.

The adapter now reads the place out of the posting's own URL, which is the only other thing
that carries it: the host is country-localized (`.com` Germany, `.ch`, `.nl`, `.co.uk`,
`.fr` — 20/20 agreed with the city in the slug) and the slug ends in the place and the
posting id. A tracked city in the last two slug words wins, which is geo's own rule that a
city beats a remote marker; otherwise the host's country goes in and geo judges
`"Remote (Switzerland)"` exactly as it judges a feed that writes "Remote, UK" itself — not
EU-remote, because such a posting usually needs residence or an entity there (2026-10-26).
No policy changed: the placeholder was hiding a place the 2026-10-26 rules already decide.

Three things were weighed and rejected:

- **Treating the placeholder as an empty location.** The adapter already turns an empty
  location into `"Remote (Germany)"`, so this would have kept every one of these postings
  EU-remote. Handing `None` to geo instead (title and description stand in) was measured:
  it drops the two Zürich postings but still stores the Amsterdam one as `Remote (EU)`,
  because its description says "fully remote". The feed knows where the job is; guessing
  from prose when the URL says "amsterdam" is the weaker reading.
- **Widening `geo._NON_EU_ONLY`** (HIR-109's axis). It only ever catches a posting that
  writes a residence sentence, and the Bromcom one does not.
- **Reading the slug for anything but a tracked city.** Only the last two words before the
  posting id are read, and only `city_of` reads them, so title words that end up in that
  window ("...-software-engineer-302654") are never mistaken for a place — they fall back
  to the host's country rather than dropping the posting on a word like "engineer".

Known cost: a posting that is genuinely open worldwide but sits on a non-German host is now
dropped — the seven Tether "100% Remote Worldwide" rows in HIR-110's sample would be. That is
the same loss the 2026-10-26 rule already takes on any feed that says "Remote, UK", and
undoing it means letting a title or description override a country the feed named, which is
its own decision.

## 2026-11-03 — The backups were never missing: a truncated listing read as a complete one (HIR-112)

HIR-112 reported that no database backup had reached the bucket since 2026-11-01 10:09Z —
two nightly runs and two pre-deploy backups all apparently absent. None of that was true.
Every backup had landed. What had gone wrong was the *looking*.

The bucket holds 56 objects (one per nightly plus one per deploy, under the 30-day
lifecycle rule). `gcloud storage ls` on it returns all 56, sorted lexicographically, which
for this naming scheme is also oldest-first. Chandler's `rtk` CLI proxy — the
output-shrinking wrapper the Claude Code hook prepends to shell commands — cuts its output
at 30 lines and appends `... (26 lines truncated)`. Thirty lines in, the newest name
visible is `hiring-radar-2026-11-01T100917Z.db.gz`. That is exactly the object the issue
named as the newest, and exactly the count ("31 objects") the issue reported: 30 names plus
the truncation line. The two "missing" nightlies (`2026-11-02T023000Z`,
`2026-11-03T023030Z`) and the two "missing" deploy backups (`2026-11-01T180622Z` for the
HIR-98 merge, `2026-11-02T155131Z` for the HIR-106 merge) were all sitting past the cut.
The VM agreed throughout: the timer's last run was 2026-11-03 02:30:30 UTC, and every run
since 11-01 logged `backup ok`.

Two things make this trap worse than an ordinary truncation, and both are why it is written
down rather than just closed:

- **Piping does not escape it.** `... | sort | tail -3` still answers
  `2026-11-01T100917Z`, because the wrapper truncates its own stdout *before* the pipe
  sees it. The reflex that normally rescues a long listing makes this one look confirmed.
- **The truncated answer is plausible.** A listing that ends two days ago reads as a
  service that stopped two days ago. Nothing about the output says "this is a prefix".

So the rule is: **never establish "the newest backup" from an unbounded listing.** Ask the
bucket a question whose true answer is short. `deploy/README.md` now carries the date-glob
form — `gcloud storage ls "gs://…/db/hiring-radar-$(date -u +%Y-%m-%d)*"` — which returns a
handful of lines no wrapper will cut, and answers "did a backup land today?" directly.
`rtk proxy <cmd>` (unfiltered) is the other way out, but it is personal tooling and not
something the runbook should depend on.

Nothing was restored and nothing was lost; the 30-day retention and the lifecycle rule were
never in question. A fresh on-demand backup (`2026-11-03T133146Z`, 10.6 MiB) was taken to
close the issue's "a backup newer than the investigation" condition, and the nightly timer
is scheduled for 2026-11-04 02:30 UTC.

One real gap survives, separately from this: `backup.sh` is loud only in the journal. If it
ever genuinely failed, the timer would go on firing and nobody would hear. That is filed as
its own ticket rather than built here.

## 2026-11-03 — Best fit: a gate, then a ratio, then the nice-to-haves (HIR-51)

The job list can now be ordered by how well each job fits the profile. Three things about
how that order is computed were open, and this is how they were settled.

- **A nice-to-have breaks ties and does nothing else.** The issue asks for a fit score of
  covered required skills over required skills, with covered nice-to-haves "weighted at a
  quarter of a required one" as the tie-break. Folded into one number — `(covered + 0.25 ×
  covered_nice) / total` — a quarter weight does more than break ties, and the demo data
  showed it immediately: a job asking two required skills you half cover, with two
  nice-to-haves you have, reads 0.75 and outranks a job you cover 3 of 5 of. The worse fit
  came first. So the ratio sorts, and the quarter-weighted nice-to-have share is a
  *separate, lower* sort term that only separates jobs the ratio leaves equal. The badge
  shows the plain ratio either way.
- **A gate outranks every score.** A job that insists on German, production experience or a
  degree the profile says no to — or names a level the profile isn't targeting — sorts
  below every job still in reach, however well its skills line up, and says which ask in one
  word. A posting that names no level never gates: most don't, and `null` is the extractor's
  safe error there (DECISIONS 2026-10-27). Seniority is a gate at all because the profile
  targets exactly one level; that is the filter's own meaning.
  **Narrowed the same week — see the 2026-11-03 HIR-113 entry above:** a posting that stores
  no level but names one *in its title* now gates on the title. "Names no level" means
  neither the body nor the title did.
- **"Best fit" ranks in the browser, over at most 200 jobs.** The server is never told the
  profile, so it cannot sort by fit; `web/src/profile.js` does, over one page of the
  filtered set, and pages through the result locally. 200 is the largest page `/api/jobs`
  serves, now pinned by a test, because setting the constant above it silently empties the
  list — which is exactly what happened on the first run. Past 200 matching jobs the foot
  says the ranking covers the newest 200, rather than ranking a slice quietly. Today's
  corpus is 248 jobs across all windows and far fewer open, so this bites rarely; a real
  fix is a server-side sort over ids the browser sends, which is more machinery than the
  cap is worth until the corpus demands it.

`coverage()` is gone; `fit()` replaces it, returning `{score, covered, total, missing,
gated_by}` with `score: null` for a job that lists no required skills at all — 0/0 is
"nothing to judge", not "no fit", and those jobs sort below every judged one rather than
at the bottom with the gated-out. Alerts (HIR-19) and the Advisor call the same function.

---

## 2026-11-02 — Aggregator-headline rows already stored are deleted, not kept and hidden (HIR-104)

HIR-96 stopped the JSearch adapter storing aggregator search-result headlines, but two rows
written before that fix were already in the database: jobs 208 ("Primetime", "AI Engineer
(m/f/x) arbeitnow commercetools Berlin · 10/16/2026") and 230 ("Primetime", "Voice AI
Engineer arbeitnow NAIRON Berlin · 10/18/2026"), duplicates of jobs 2/16 (commercetools)
and 183 (NAIRON) under a company that never posted them.

The live database held five, not two: also jobs 254 (Nebius), 255 (Perplexity) and 363
(SumUp). The dev copy was simply older.

**A headline row that duplicates a posting we already hold is deleted.** Chandler's go,
2026-11-02 — deleting stored jobs is on the AGENTS.md stop list, so this is the standing
answer for rows of that shape: a title that `jsearch.is_headline` matches, on a job with a
jsearch source row, **whose posting is stored under its real company too**, is removable
without asking again. Four of the five qualified (208→2/16, 230→183, 254→196/219,
255→175, all title-for-title). Rejected: keeping them and filtering them out of the
queries (the chart would be right and the stored data wrong, and every later query would
have to remember them), and rewriting their company and title by hand from the headline
(it guesses, and dedup would then merge two rows whose text came from different places).

**A headline row that is the only copy of a posting is a different question, and waits.**
Job 363 is SumUp's "AI / Machine Learning Engineer II", stored nowhere else, and it cannot
come back: HIR-96 now drops the record at parse time, and SumUp's polled Greenhouse board
does not carry that posting (its other three rows came in on 2026-11-02 without it). So
deleting it loses a real Berlin posting rather than a duplicate, which is not what the go
covered. It stays, via `--keep 363`, until Chandler says which he wants: lose the posting,
or repair the row by hand (its description text is genuine; only the company and title are
the aggregator's, and both read unambiguously out of the headline). The chart therefore
still shows one phantom "Primetime" employer.

**The removal is a script, not typed SQL.** `scripts/remove_headline_jobs.py` selects with
`app.sources.jsearch.is_headline` — the same test the adapter applies — so it can never
remove a row the adapter would have kept, and so the two copies of the database are
cleaned by the same rule rather than by two sets of hand-typed ids, which differ between
them (as they did: the live copy had three rows the dev copy never saw). `--keep <id>`
is how a person's "not that one" is expressed, so sparing a row is a recorded argument
rather than an edited script. It refuses to run with foreign keys off (that would orphan
the skill mentions instead of cascading them), and it leaves a headline-titled job from
any other source alone and reports it: that would be a different bug from the one
approved here.

---

## 2026-11-02 — A person read 30 held-out labels: 0 errors of 30 (HIR-92)

The held-out answer key now has one number a human produced. Until today the whole HIR-70
batch — 22 Goldens, ~300 skill labels and ~60 attribute labels — was graded only by models
agreeing with each other, and the 15-label "spot-check" recorded on 2026-10-30 was answered
by `claude-fable-5-1`, not a person. That gap is what this entry closes.

**The result: 0 errors of 30, Wilson 95% [0.000, 0.114]** — skills 0 of 24, attributes 0 of 6.
The ticket's rule accepts the batch at 0–1 errors in 30, so no second sample was drawn. The
interval is the honest part: 30 labels cannot rule out an 11% error rate. It is still the
first bound on this answer key that does not rest on model agreement.

**The protocol, which is the reusable half.** `scripts/spot_check.py`, two subcommands:

- `sample` draws at the **label** level, not the posting level — one skill or one attribute
  per item — seeded and stratified, and renders each item with its quote located in the
  posting, the section heading named and classified, the neighbouring bullets, the other
  sections the skill appears under, and (behind a null attribute) every mention of that
  attribute's trigger words. 30 items in 3 batches of 10.
- `apply` scores the answers, writes `summary.json`, and stamps `spot_checked_by_human` on
  the labels that passed. It never changes a label's value: a wrong one lands in
  `corrections_to_decide` to be ruled on separately. The Wilson interval is imported from
  `agent_label.py` rather than re-implemented, so the two cannot fork.

**The pool excludes every label a person had already read** — `adjudicated`,
`spot_checked_by_human`, and attributes under a true `seniority_reviewed` / `attrs_reviewed`.
Re-asking a question already answered by hand measures nothing. It deliberately ignores the
whole-Golden `spot_checked` / `spot_checked_by` fields, because a model wrote those. 343
labels eligible (281 skills, 62 attributes).

**Each item arrives pre-answered, and the human confirms or flips.** Both checks — is this
asked of the candidate, and is it required or nice-to-have — are stated with their one-line
reason, plus a "watch for" line naming the single thing most likely to be misread. Quote-
verbatim is not asked as a human question; the auto-check already enforces it, and the bold
span in the context *is* the located quote. This is what keeps an item under 30 seconds.
Rejected: showing the A/B/third-labeler outputs or the earlier adjudication notes — a
reviewer who sees three models agree is no longer an independent read.

**German postings are presented in English, translated, with the original quote kept.** The
quoted phrase stays bold in the translation; the LABEL line carries the German verbatim in
parentheses; the section heading is translated and classified; and an optional marker is
named by its English meaning *and* by which bullet it attaches to, since that is the single
most common way these labels go wrong ("sind von Vorteil" governing a three-item list, an
"idealerweise" in the adjacent bullet). 16 of the 30 items were German.

**Two readings confirmed as guide rules rather than changed.** Both were put up as candidate
guide edits and came back accepted as-is: "These are meant to be indicative, not hard
requirements" above a list does **not** flip the section to `nice_to_have` — it is prose, not
a heading, and "indicative" is not one of rule 2's inline markers (golden_038); and "MS or
PhD" takes the **highest** level named, per the degree rule as written (golden_040).

**Amends the 2026-10-30 entry.** "A human spot-check is still open" and "the error rate on
this answer key is four models agreeing with each other" were true when written and are now
superseded by the 0-of-30 above. The 0-of-15 fourth-model row stands as a record of what was
actually run; it is not a human number and the table already says so.

Two taxonomy gaps the sample surfaced, both filed rather than fixed here: "recommendation
engines" → `recommender-systems` and "prompting" → `prompt-engineering` are mapped by
meaning with no registered alias. Three others the sample flagged the same way
("orchestration frameworks", "Orchestrierungs-Frameworks", "Container-Orchestrierung") were
already closed by taxonomy v7 on main.

---

## 2026-11-01 — The deployed setup, written down: OS Login + federated deployer, units in the repo (HIR-74)

HIR-29 built the VM by hand and left the result undocumented. This records the shape it
settled into, and the two choices made while writing it down.

**The server's own configuration lives in the repo, and `/etc` is a copy of it.** The five
systemd units and the Caddyfile are committed to `deploy/` byte-for-byte as they are on the
VM, so `diff` against `/etc` answers "has the box drifted?". The one exception is the
Caddyfile's bcrypt password hash, replaced by `REPLACE_WITH_BCRYPT_HASH`; `provision.sh`
substitutes the real hash at install time, so the password never enters git. A deploy does
**not** apply these files — only `provision.sh` or a hand copy does. Rejected: keeping them
only on the VM (one disk failure and the setup is gone), and templating the whole thing
(one VM, one hostname; the indirection buys nothing).

**`provision.sh` provisions the VM, not the cloud.** It does the inside-the-VM half
(packages, 1 GB swap, app user, checkout, `uv sync`, a secrets *template*, the units,
Caddy) and is re-runnable: every step checks for its own result, it never overwrites
`/etc/hiring-radar.env`, and it never touches the database. The static IP, firewall,
instance, backups bucket and CI/CD identity stay hand-run from the Mac — they need admin
credentials the VM deliberately does not have, and they are created once in the life of the
project. Rejected: one script for all of it, which would need owner-level credentials to
exist somewhere.

**No deploy key exists anywhere.** CD authenticates by workload identity federation:
GitHub mints an OIDC token per run, GCP's provider accepts it only when the claims say
repository `chandlershortlidge/hiring-radar` *and* ref `refs/heads/main`, and swaps it for a
token for the `github-deployer` service account. A fork, a branch or a PR gets nothing.
That account holds three roles and no more: `compute.viewer` and
`iap.tunnelResourceAccessor` on the project, `compute.osAdminLogin` on the one instance.
**OS Login** (`enable-oslogin=TRUE`) is what turns the IAM role into a Linux account, so no
SSH key sits in instance metadata and each run gets a throwaway key that expires in 30
minutes. `osAdminLogin` rather than `osLogin` because the deploy script needs `sudo`.
Rejected: a service-account JSON key in a GitHub secret — a long-lived credential to rotate
and to leak.

**Backups are the VM's own job, restores are a documented procedure.** `backup.sh` runs at
03:30 Europe/Berlin: SQLite `.backup`, integrity check, gzip, into
`gs://hiring-radar-512318-backups/db/`, where a lifecycle rule deletes copies after 30 days.
The VM writes as its default Compute Engine service account, which already has project
`roles/editor` — no extra grant. A deploy takes one first, so the pre-deploy state is always
one object away. Restoring is in the runbook and its load-bearing step is deleting the
`-wal` and `-shm` files: leave them and SQLite replays the old write-ahead log over the
restored file, giving a silent mix of two databases.

## 2026-11-01 — JSearch postings whose title is an aggregator headline are dropped, not repaired (HIR-96)

The job list showed a row titled "AI / Machine Learning Engineer II arbeitnow SumUp Berlin,
Berlin, Germany · 10/28/2026" under the company "Primetime", sitting next to the real SumUp
posting. A recorded JSearch response (now `tests/fixtures/feeds/jsearch_recorded.json`)
shows what happens: for some postings the publisher JobLeads hands Google its own
search-result headline as `job_title`, and `employer_name` is an unrelated firm — Primetime,
website primetime.company, not the employer at all. Two such rows are already stored
(jobs 208 commercetools and 230 NAIRON, both duplicates of rows we hold from the real board
feed).

Decided: `jsearch.parse` skips these records. Neither field can be repaired — the real
company name exists only inside the headline text, and there is no way to tell where the
title ends and the aggregator's branding begins. Nothing is lost: the same SumUp posting
came back in the same response from another publisher with the right title and company.

Rejected: a company-normalisation step before dedup (the issue's second question). It cannot
help, because "Primetime" is not a variant spelling of "SumUp" — it is a different company.
Normalising would still leave dedup comparing two different companies and storing a second
copy. Also rejected: parsing the real title and company out of the headline — the boundary
between them is not recoverable, and a wrong guess is worse than a dropped posting.

The signature is a title that ends in a date; a job title never does. The two rows already
stored are left alone — deleting stored jobs needs Chandler's go.

## 2026-11-01 — Taxonomy v7: the German and short-form spellings the Golden pass found (HIR-101)

The HIR-97 pass over the 46 Golden postings listed every label a Golden spells one way and
the taxonomy another. Twenty-four aliases close them, mostly German words for skills already
tracked in English: `vektordatenbanken`, `vector db` → `vector-databases`;
`container`, `containerisierung` → `containerization`; `softwareentwicklung` →
`software-engineering`; `architekturdesign` → `software-architecture`;
`machine-learning-konzepte` → `machine-learning`; `verteilte systeme` →
`distributed-systems`; `datenpipelines` → `data-pipelines`; `datenmodelle` →
`data-modeling`; `evaluierung` → `evaluation`; `versionierung` → `model-versioning`;
`versionskontrolle` → `git`; `feinabstimmung` → `fine-tuning`; `automatisierte tests`,
`testautomatisierung` → `testing`; `netzwerke` → `networking`; `statistische methoden` →
`statistics`; `orchestrierungs-frameworks` → `llm-orchestration`; plus the short forms
`spark` → `apache-spark`, `huggingface` → `hugging-face`, `nodejs` → `node-js`,
`bedrock` → `aws-bedrock`, `s3` → `aws-s3`. Taxonomy v7, still 210 skills — aliases add no
row to the chart, so the rule that a proposed skill needs three postings does not apply.

**`deployment` stays out, and this is the general shape of the rule.** It is the one
candidate whose English and German spelling are the same word, and it reads as a whole word
in 23 of the 46 Goldens — five of them (003, 005, 006, 011, 045) in postings that do *not*
ask for `ai-deployment`: "deployment and monitoring of data pipelines", "cloud-native
deployment", "concept & design, development, QA, deployment and production monitoring".
Those are ordinary software delivery, not deploying a model. An alias has to be the same
*thing* spelled differently; bare "deployment" is a broader thing than `ai-deployment`, so
it would be a parent at best and is a false positive in practice. `model deployment` and
`ml model deployment` already cover the narrow sense.

**`container` goes in, on the same test.** Four whole-word occurrences across the Goldens,
every one in a posting that does ask for `containerization` ("DevOps-Stacks (CI/CD, IaC,
Container, Kubernetes)", "Container-Technologien wie Docker"). German compounds the word
rather than pluralising it, so the existing `containers` alias misses all four.

**`netzwerke` goes in despite one miss.** Its single occurrence in the Goldens is company
boilerplate — golden_025 runs "Kommunikations-Netzwerke für den Digitalfunk BOS" — not a
requirement, and that posting does not ask for `networking`. It is kept anyway because it is
simply the German for Networking, the same thing spelled differently, which is what an alias
is; the miss is a posting describing its own infrastructure, which the extractor is told not
to read as a requirement. If `networking` starts appearing on the chart for postings that
never asked for it, this alias is the first thing to pull.

**`s3` is the documented exception to the three-character floor.** `cvSkills.js` refuses any
phrase under `MIN_PHRASE` = 3 characters, so `s3` resolves when a job posting names it and
is silently ignored when a CV does — which is the right split: "S3" in a stack list is
unambiguous, "S3" in a CV is as likely a model number. Every other alias added here is 3
characters or more. `postgress` (a typo), and bare `c#`, `r` and `go` stay out for the same
floor, as in HIR-97.

---

## 2026-11-01 — Taxonomy v6: the nine spellings the first real CV run missed (HIR-97)

Chandler's own CV through the HIR-14 matcher ticked 20 skills and missed six, every one a
missing alias rather than a matcher bug: "LLM products" (the taxonomy had `llm apis` and
`large language models` but not the bare singular), "ChromaDB", "SQLite/Postgres",
"tool-call design", "NER (Presidio + spaCy)", "OpenCV". Nine aliases close all six:
`llm` → `llms`; `chromadb`, `chroma` → `vector-databases`; `postgres` → `postgresql`;
`tool-call`, `tool calls` → `tool-calling`; `spacy`, `named entity recognition` → `nlp`;
`opencv` → `computer-vision`. Taxonomy v6, still 210 skills.

**`ner` stays out.** Three characters, which `cvSkills.js`'s `MIN_PHRASE` admits, so it
would match — and that is the problem: in a CV "NER" is as likely a product name or a
German word fragment as the technique. `named entity recognition` carries the same meaning
with no ambiguity, and someone who writes only "NER" loses one click.

**ChromaDB, spaCy and OpenCV become aliases of the category, not entries of their own,
and the 3-jobs rule is why.** Weaviate, pgvector and FAISS *are* entries under
`vector-databases`, so the precedent for a named tool is an entry — but each of those
cleared the 2026-10-20 bar of 3 jobs in the `proposed_skill` queue first. These three have
no queue support at all; they surfaced from one person's CV, which is not frequency
evidence. Counts do not roll up from child to parent anywhere in `app/queries.py`, so an
entry now would move a posting that says "ChromaDB" *off* the Vector Databases bar and onto
a bar of its own with one job behind it — the exact fragmentation the 3-jobs rule exists to
prevent. Promotion stays available: if any of the three reaches 3 jobs in the queue it
becomes an entry with the category as parent, and the alias moves with it.

**The matcher is unchanged.** `MIN_PHRASE` is 3 and "LLM" is exactly 3, so the singular
passes as the issue predicted; nothing in `cvSkills.js` needed touching.

Merging re-reads every job once (`extractor_version` hashes the taxonomy block), about €3
on the next poll.

---

## 2026-11-01 — A CV may pre-fill the profile, but only inside the browser (HIR-14)

**The scope line changes, narrowly.** AGENTS.md and the rebuild entry below both put
"résumé matching/tailoring" out of scope. That stays true for tailoring, stored résumés and
scoring a person against a posting. What is now **in** scope is one thing: reading a CV to
pre-select skills the person then edits, as a faster way to fill the same
`profile.skills` set they could fill by clicking chips. Nothing downstream changes — the
profile shape, `coverage()` and the chart are untouched.

**It happens in the browser, and the CV never leaves it.** HIR-14 was written for the
Dossier method: extract text server-side, send it to Anthropic with a CV variant of the
extractor prompt. Chandler chose the browser-only version instead (asked and answered on
HIR-14, 1 Nov). The reason is the promise the profile panel already makes — "Stays in this
browser… nothing is scored or uploaded" — and the fact that HIR-14 blocks the public
launch. A CV is the most sensitive document a visitor has; sending one to our server and on
to a provider is a new privacy surface, and it would have made that promise false. So:

- CV text is read in the page, matched in the page, and dropped when the drawer closes.
- No endpoint, no model call, no bytes stored — server-side and client-side alike.
- The panel's promise stands unchanged and stays true.

**What we give up, knowingly.** Matching is substring, not semantic: a CV that spells a
skill out ("we served models with Triton") matches; a paraphrase the taxonomy has no alias
for ("stood up our own inference endpoints") does not. That is acceptable because a
pre-fill is a starting point the person reviews — the drawer already lets them add and
remove anything — and because the alternative was a model call per upload on a public site.
If the local match proves too weak once people use it, the model-call version can be added
later as its own decision, with its own disclosure.

**Why the issue's "supersedes" line could not be honoured as written.** HIR-14 asked the
entry to supersede "no résumé upload (too error-prone)". That phrase is recorded nowhere in
this repo; it is from the legacy project. This entry is written against the scope line in
the rebuild decision instead.

---

## 2026-11-01 — Taxonomy v5: the HIR-70 gaps triaged, but the 3-jobs rule still gates (HIR-72)

The two HIR-70 labelers reported 216 label strings they could not map to taxonomy v4. All
216 are now triaged, each with exactly one verdict (the full table is on HIR-72). The shape:
**61 would-be entries, 17 strings that are other spellings of 13 entries we already have,
107 out.** The 216 overstates the gap — it counts "Spring", "Spring Boot" and
"Spring/SpringBoot" as three, and every German/English pair twice.

**The 3-jobs rule from 2026-10-20 holds, and it counts jobs in the live `proposed_skill`
queue, not postings in the Goldens.** This was the decision that shaped the change. 24
Goldens cannot establish frequency: in that run all but one label appears in a single
posting, so "both labelers agreed" is corroboration that the *phrase* is unmapped, not
evidence that the market asks for it. The queue is the frequency counter; the Goldens only
tell us which names to look up in it.

Gating the 61 on the queue, **9 land**: `cuda` (4 jobs), `kserve` (4), `nvidia-dynamo` (3),
`quantization` (4, folding "model quantization"), `ray-serve` (4),
`speculative-decoding` (4), `spring-boot` (4, folding "spring" and "springboot"),
`triton-inference-server` (5, folding "NVIDIA Triton"), `knowledge-distillation` (4,
folding "distillation" and "model distillation"). **`opentelemetry`** (3) joins them: it
never appeared in the 216, but the bar is the bar and it was sitting over it, so leaving it
pending would have meant running the same review twice. Taxonomy v5, 210 skills.

The other 52 stay pending in the queue and cost nothing to revisit — ten are already at 2
jobs (`redis`, `django`, `jenkins`, `dvc`, `opensearch`, `ray`, `dotnet`, `oauth2`,
`openwebui`, `tflite`) and will land on their own. **Their ids, parents and aliases are
decided and recorded on HIR-72**, so the next review is a lookup, not a re-argument.

**All 17 alias strings were added regardless of frequency, because an alias cannot widen
the chart** — it only stops a phrase counting as nothing. That is where the German
duplicates go: "Container-Orchestrierung" → `containerization`, "Retrieval-Pipelines" →
`rag`, "Tool-Engineering" → `tool-calling`, "produktiver Betrieb von KI-Modellen" →
`mlops`, "Training von KI Modellen" → `model-development`. Also folded:
"orchestration frameworks" / "agent orchestration" → `llm-orchestration`, "memory systems"
→ `agent-state-management`, "knowledge base design" → `rag`, "cloud functions" →
`serverless`, "multi-step reasoning" → `chain-of-thought`, "tracing" → `observability`,
"enterprise architecture" → `software-architecture`, "web application development" →
`full-stack-development`.

**"Data analytics" is not an alias of `data-science`,** though it was one for a few hours.
The two are different jobs — analytics describes and reports, data science models and
predicts — and folding the first into the second would have inflated `data-science` with
business-analytics postings and made the chart's most load-bearing row mean less. It is a
new entry when it earns one, not a spelling of an existing skill, and it is back in the
queue until it does. This is what the taxonomy/README.md rule "aliases are the same thing
spelled differently" is for: convenience is not sameness.

**Two findings that corrected the issue's own reading of the data, both from `merged.json`:**

- **"Tracking" in 2 postings is two different skills, not corroboration.** golden_037 quotes
  `Tracking` in a web-app stack list (web analytics); golden_040 quotes `tracking` inside
  "detection, classification, segmentation, tracking" (object tracking in video). A bare
  `tracking` alias would have silently merged a marketing term into a vision skill. Left
  out, in both senses. That leaves **"Context engineering" as the only label in the run two
  different companies actually asked for** — and it has 0 queue rows, so it does not land.
- **"Triton" can now be disambiguated, and still resolves to nothing.** 2026-10-20 left
  bare "Triton" out as ambiguous between NVIDIA's server and OpenAI's kernel language.
  golden_035 names both, separately ("CUDA or Triton", and "Triton Inference Server"), so
  `triton-inference-server` is an entry with `nvidia triton` as an alias, `triton-kernels`
  is a decided-but-unlanded id (0 queue rows), and **bare "Triton" is deliberately still
  not an alias of either** — the 2026-10-20 reasoning survives intact. The queue has
  "triton" at 2 jobs and those rows stay pending, unresolvable on purpose.

**What stays out, and why, so it is not re-litigated:** all 17 paid-social labels from
golden_048, which was already ruled a marketing role (2026-10-27). The 45 method and format
names from golden_035 — AWQ, GPTQ, SmoothQuant, FP8/INT4/INT8/MXFP4/NVFP4, EAGLE, Medusa,
FlashInfer, LMCache, WideEP, prefill–decode disaggregation, NVLink, InfiniBand, RoCE,
NCCL — because the level above each of them is a decided id, so one posting's vocabulary
does not become 45 chart rows with document frequency 1. Twenty-two phrases too broad to
count ("Data", "Infrastructure", "Scalability", "Integration", bare "Security"). Twelve
responsibilities rather than skills, including golden_035's four "diagnose the bottleneck"
phrases. Ten working methods (Agile, Scrum, Freigabeprozesse, Qualitätssicherung,
Prototyping) and "Open-source contributions".

**Every job re-extracts on the next poll.** `extractor_version` hashes the system prompt,
which contains the taxonomy block, so any edit here — a new alias as much as a new entry —
invalidates every stamp. Per AGENTS.md as of HIR-94, the merge is the approval for that;
nothing waits before the PR.

**13 Golden labels added across 6 Goldens, on the 2026-10-20 precedent** — a label the
taxonomy could not express before is a missing gold label, so adding it is taxonomy-driven
rather than tuning. golden_035 gains 8 of the 9 new entries, which is the clearest evidence
the gating worked: it is the inference posting the whole issue came from.
`requirement` follows LABELING.md's section rule in every case, which puts the four serving
engines from the "Must-haves" stack list (`kserve`, `nvidia-dynamo`, `ray-serve`,
`triton-inference-server`) at `required` and the four from "Nice-to-haves" (`cuda`,
`knowledge-distillation`, `quantization`, `speculative-decoding`) at `nice_to_have`, even
where the same skill also appears in the responsibilities — responsibilities alone are not
an ask. The rest: `chain-of-thought` from "multi-step reasoning" in golden_018 and
golden_032, `llm-orchestration` in golden_044, `agent-state-management` from "memory
systems" in golden_045, `spring-boot` from "Spring/SpringBoot" in golden_047.

**One existing label was narrowed, not added.** golden_035's `tensorrt` quoted
"TensorRT-LLM, Triton Inference Server, NVIDIA Dynamo, Ray Serve" — one span standing in
for four tools, because three of them had no id to go to. Now they do, so the quote is
`TensorRT-LLM` and each engine carries its own. An over-broad `raw_text` is the shape a
taxonomy gap leaves behind in the answer key, and it is worth looking for the next time
entries land.

**What did not change: golden_038.** It was a relabel candidate only through the
"data analytics" → `data-science` alias, and that alias is gone, so it keeps its labels.

---

## 2026-10-30 — The skill tree, made readable: names only, three hues, branches by greedy split (HIR-81)

The tree shipped correct and unusable. Four decisions from the follow-up.

**The two shares move to a tooltip; the name stays on the drawing.** The 2026-10-30 entry
put both percentages on the node, on the argument that the gap is the feature and a
tooltip hides it. Thirty two-line labels do not fit: each needs ~24px of height at the
~930px the card renders at, and they collided in five places. One line per node halves
that. The gap is still on the drawing — it is the band between the ring (mentioned) and
the solid core (required) — and the exact pair is one hover or Tab away. Both numbers are
in every node's `aria-label` besides, so a screen reader never depends on the tip.

Where there is any gap at all the band is held open to `MIN_BAND`, because at a small
radius a true 19-in-20 ratio draws as a hairline. A skill required every time it is
mentioned keeps a solid circle: the floor never invents a gap that is not there. Worth
knowing for whoever reads the picture: on this corpus required ≈ mentioned for most skills
(Python 76/75, TypeScript 13/13), so the encoding has less signal here than the Snowflake
example suggests. MLOps (20% / 12%) is what it looks like when there is something to see.

**Three hues, not one per branch.** A tree shows every branch at once, so it is an
*all-pairs* form in the dataviz sense, not the adjacent-pairs case a bar chart is.
`scripts/validate_palette.js` on the reference palette against our white card:

- 3 slots `#2a78d6` / `#eb6834` / `#1baf7a` — ALL CHECKS PASS (worst all-pairs CVD ΔE 9.2,
  normal-vision 24.0; aqua is a 2.82:1 contrast WARN, relieved by the always-visible names)
- 4 slots — FAIL the hard normal-vision floor, yellow↔orange ΔE 13.7 against a floor of 15
- 6 slots — FAIL that *and* CVD separation (ΔE 3.2, protan)

So the three largest branches are coloured and everything else is ink: the skill's own
"past three, fold to Other" rule. Dark steps `#3987e5` / `#d95926` / `#199e70` on `#1a1a19`
pass all six checks and are recorded in `web/src/styles.css` against the day the dashboard
gets a dark mode — it has none today, so none was added for one card.

**A branch is a lobe found by greedy split, not a root.** One hue per top-level subtree
does not work here: the tree normally has a single root (python) whose one big child holds
most of the nodes, so every node would be one colour. Instead the largest branch is split
into its children, repeatedly, until none holds more than `TRUNK_SHARE` of the tree; the
heads that were split are the trunk and stay neutral. On the open set that yields
Cloud(14), Agents(4), APIs(2), CI/CD(2), Evaluation(2) under a python→llms trunk, and it
stays sane across city, seniority and window filters. A branch under `MIN_BRANCH` nodes
never takes a hue off a real lobe.

A knowing deviation, recorded rather than hidden: dataviz says colour follows the entity,
never its rank, and here the hue is assigned by branch rank. There is nothing stable to
pin it to — the branch *set* is recomputed per filter, and Cloud is a branch under one
filter and trunk under another. The legend names the three coloured branches, so identity
is never colour-alone.

**Labels are placed by a de-collision pass, so non-overlap is an invariant.** A name sits
beside its node and slides vertically, in half-label steps, until its box touches no other
name, no node and not the hub; a leader line is drawn when it moved. Nodes are placed
most-prevalent first, so the skills a reader goes looking for keep their natural spot.

Two alternatives were weighed and rejected. Lowering `MAX_NODES` to 20–24 is one constant,
but it buys legibility by deleting skills and makes nothing invariant — it only makes
today's corpus happen to fit. "More ring spacing" is a visual no-op: `size` is derived from
`RING × max_depth` and every radius and type size is scaled by `size / 1000`, so growing
`RING` grows the whole picture in lockstep and nothing gains room on screen. The real
levers are rendered pixels, shorter labels and placement — which is also why the card is
now collapsed by default and last on the page: opened deliberately, it can have the width.

Python has no font metrics, so a label's width is estimated per character and deliberately
over-estimated. Checked against the browser's own `getBBox` across all 30 labels: the
estimate is 1.04–1.6× the real width, never under. That is what makes
`test_no_two_labels_overlap_at_thirty_nodes` a guarantee rather than a coincidence. If the
pass ever runs out of steps it sets `label_placed: False` and the test fails — *that* is
the signal to lower `MAX_NODES`, so the two levers compose instead of competing.

Display names now go *into* `build_tree` rather than being attached to its output: a
label's width decides the layout, so the tree cannot place anything without them.

---

## 2026-10-30 — The repo guards the branch, not the memory of it (HIR-88)

Three commits landed on the wrong branch this week. The expensive one was the HIR-70 /
HIR-85 tangle: HIR-69 made production experience a fourth per-job attribute while HIR-70's
held-out labeling was still mid-flight, and work for the two moved between branches that
looked interchangeable because every branch here is `chandlershortlidge/hir-NN-...`. The
cost was not a lost commit — it was that a merge of main into HIR-70 surfaced the overlap
as a red test rather than a conflict (DECISIONS 2026-10-29, HIR-85), so the question "which
ticket is this change for?" got answered after the fact, by reading a diff.

**The guard is a hook, and the hook reads a file, not the branch name.** `.githooks/pre-commit`
refuses a commit on `main`/`master`, requires a `TICKET` file at the repo root, and refuses
if the current branch name does not contain the id in `TICKET` (case-insensitively, since
branch names are lowercase and issue ids are not). `TICKET` is gitignored: it is a statement
about the working copy, not about the history, and it must not travel in a merge.

Why a separate file at all, when the branch name already carries the id: a name only says
what the branch was created for. `TICKET` is written deliberately at the start of a session,
so the check compares an intention against a branch instead of comparing a branch to itself.
A mismatch is exactly the case that cost us this week, and the hook's message says to stop
and decide rather than offering a fix — rewriting `TICKET` to match the branch would pass
the check and lose the signal.

**The hook is the backstop; the first action of the session is the fix.** AGENTS.md opens
with it, ahead of everything else in the project block: ask which ticket this session is
for if the prompt does not name one, switch to that ticket's branch — freshly cut from an
up-to-date main, or the existing one — and only then write the id to `TICKET`. The rule it
replaces is "never inherit whatever branch the terminal is on": between sessions the
terminal is left wherever the last one ended, and reading that as a statement of intent is
how all three wrong-branch commits happened. A branch is now chosen, never inherited.

Ordering it first is the point, not decoration. An agent that reads the code before fixing
the branch has already spent the part of the session where switching is free — by the time
the hook says no, there is a diff to move, and moving it is where the mistakes live.

**Scoped to sessions that will commit.** The first version said "every session", which
charges a ticket question to anyone who only wanted a question answered — a cost paid on
the sessions the rule was never about. A read-only session now stays where it is. The seam
that creates is the session that starts as a question and becomes a change; the rule names
it and puts the switch *before the first edit* rather than before the first commit, which
is the same free moment the ordering above is protecting. The hook still refuses the commit
if that is missed, so the narrowing costs a backstop, not the guard.

**Not chosen.** A commit-msg hook parsing the ticket out of the message: it fires after the
message is written, catches nothing about where the commit lands, and would push the id into
every subject line. A `prepare-commit-msg` hook that fills the id in: helpful, but it makes
a wrong branch easier to commit to, not harder. A CI check on the PR: too late — by then the
commits exist on the branch they shouldn't be on.

**The hook is advisory by construction.** Git will not run hooks a repository ships, so
`git config core.hooksPath .githooks` is a one-time step per clone (README, AGENTS.md), and
`--no-verify` still bypasses it. That is accepted: the goal is to make the wrong branch
noisy, not impossible.

Alongside it, `.github/pull_request_template.md` with three headings — Testing, Risk, How
to revert. Same reasoning at the other end of the branch: the facts a reviewer needs are the
ones the author has and forgets to write down.

---

## 2026-10-30 — The skill tree reads the conditional asymmetry the other way round, and a parent is the nearest gateway, not the trunk (HIR-81)

v1 of the skill tree is a static SVG with a radial layout computed live from the
co-occurrence of the filtered job set: `app/skill_tree.py` does every count and every
coordinate, `web/src/SkillTree.jsx` only draws them. Three decisions in it are worth
recording, because two of them contradict the issue and the third was tried and reverted.

**Direction: the more prevalent skill is the parent.** HIR-81 gives two rules — depth is
prevalence, and direction is the conditional-probability asymmetry — and its worked example
reads the asymmetry so that the *rarer* skill is the parent ("P(observability | evaluation)
high and P(evaluation | observability) low, so evaluation is the parent" — which means
observability is the more common of the two). Taken literally that puts Snowflake above
Python and there is no trunk at all, so the two rules cannot both hold. Depth-is-prevalence
is the one that carries the picture, so the asymmetry is read the other way: a parent is
always *strictly* more prevalent than its child. This also makes the graph a forest for
free — an edge can never close a cycle — and means two equally common skills are never
parent and child, because neither direction has an asymmetry to read.

**A parent is the least prevalent skill that still qualifies, not the most.** Taking the
most prevalent qualifying parent — the obvious reading of "high conditional probability" —
makes every node a direct child of Python, because almost everything co-occurs with Python:
a two-ring star, the hairball the issue wanted avoided, just drawn radially. Taking the
*least* prevalent skill that the child's jobs still ask for at least `MIN_CONDITIONAL`
(0.6) of the time gives the specialization paths that are the point:
python → llms → agents → rag → prompt-engineering → tool-calling.

**Both shares on every node, so the tree ignores the requirement filter.** Each node
carries mentioned % and required % over the same denominator (Leoson's Snowflake
observation: 17% mentioned, 3% required). *Superseded later the same day by "The skill
tree, made readable" at the top of this log, on where they are shown: the numbers moved to
a hover/focus tooltip and the ring/core encoding carries the gap on the drawing. The rule
that both are reported, over one denominator, stands.* There is
therefore nothing for `requirement` to choose, and `/api/skills/tree` ignores it along with
the skill selection — the tree maps the whole filtered market, and selecting a skill only
highlights it. Every other filter (city, seniority, German, degree, production, window)
still narrows the job set the tree is drawn over.

**Tried and reverted: equalizing arc length instead of angle.** Giving each leaf a slice of
1/depth rather than a flat one makes every leaf's *arc* equal — an inner ring is shorter,
so an equal angle near the centre buys less room. It reads worse: it squeezes exactly the
long deep branches that carry the picture. Equal angular slices stayed. Label crowding was
instead handled by capping the drawing at `MAX_NODES` = 30; what still overlaps is a branch
whose child sits at nearly its own angle one ring out (Machine Learning and PyTorch). The
fix for that is a de-collision pass with leader lines, which v1 does not need; pulling a
branch's label back along its own spoke was tried and is not it — the label slides across
the node it names.

The personal overlay (your skills lit up, the shortest path to a target cluster) waits for
HIR-14, as HIR-81 says.

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
> - **`sample`** — the spot-check, drawn seeded from the three-way-agreed labels and put
>   back to `?` so `apply` cannot pass without it. n=15 of 79, seed 0 — 19% of the agreed
>   pool, the 15–20% HIR-70 asked for. It was **meant** to be the one number a person
>   produced, and it is not (see the correction below); `--answered-by` now records who
>   answered instead of letting the field's name assume it.
>
> **What a model decided is recorded as such.** A Golden carries `adjudicated` (fields a
> person decided) and `adjudicated_by_model` (fields the judge or the third labeler
> settled) separately, plus `third_labeler` where one read the posting.
> `seniority_reviewed` / `attrs_reviewed` keep their meaning — a person looked at this —
> so they stay false for anything only a model touched. `apply` counts the spot-check error
> rate over the drawn sample rather than over every agreed label, and records who answered it.
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
> **Answered outside the queue:** all 15 spot-check labels came back `ok` — from a model,
> not a person; see the correction below. Of the 21
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
Wilson [0.000, 0.204]** — a sample drawn seeded from the three-way-agreed pool and answered
by a fourth model, not by a person.

### The numbers this process produced (2026-10-30)

Run `20261027T110516Z_label`, 24 postings, A `claude-opus-5-5` vs B `gpt-6.1-sol`, judge and
third labeler `gemini-4-argon`, extractor `claude-sonnet-5-5` (never a labeler).

| what it measures | result |
|---|---|
| labeler agreement, A vs B, skills | P 0.932 / R 0.974 / F1 0.953 (tp 301, B-only 22, A-only 8) |
| labeler agreement, requirement on shared ids | 0.993 |
| labeler agreement, attributes | seniority 24/24, German 24/24, degree 23/24 |
| third labeler vs the agreed labels | **0 of 79 differed**, Wilson 95% [0.000, 0.046] |
| fourth-model check of the three-way-agreed labels | **0 errors of 15**, Wilson 95% [0.000, 0.204] — `claude-fable-5-1`, not a person |
| adjudication split, fields | **45 decided by a person, 50 by a model** |

Each number answers a different question, and the weakest one is the one that counts.
Agreement measures whether two readers coincide, not whether they are right. The third
labeler's 0/79 is drawn from the pool two models already agreed on — the easy cases by
construction, since every hard one was queued — so it bounds how often three independent
readers of an easy label all err, not how good the answer key is. The 0/15 adds a fourth
reader to that same easy pool, and its interval is wide on top of that: 15 labels cannot rule
out a 20% error rate.

**Correction, 2026-10-30: no label in this process was checked by a person.** The 15-label
spot-check was answered by `claude-fable-5-1` in a side conversation, and was recorded at the
time as a human sample and reported as the one number a person's attention bought. It is not.
The Goldens carry `spot_checked_by: "claude-fable-5-1 (assistant)"` instead of
`spot_checked: true`, and `seniority_reviewed` / `attrs_reviewed` are false wherever only
that check touched a field — those flags mean a person looked, and `apply` now takes the
answerer from the record instead of assuming one. What a person did decide is unchanged, and
it is the 45 in the row above: the queue adjudication, every disagreement, every judge split.

It also makes the fourth reader a partly correlated one. `claude-fable-5-1` shares a family
with labeler A (`claude-opus-5-5`), and this entry already records what that costs — the
two-Claude smoke run agreed 43/43 and measured nothing. A cross-family checker was the right
choice for the judge and the third labeler, and would have been here.

**A human spot-check is still open.** Until one is done, the error rate on this answer key is
four models agreeing with each other.

> **Closed 2026-11-02 (HIR-92).** A person read a seeded sample of 30 labels from this batch:
> **0 errors of 30, Wilson 95% [0.000, 0.114]**. See the 2026-11-02 entry for the protocol.
> This paragraph records the state between 10-30 and 11-02; it is no longer the current one.

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
(HIR-55): 26 Goldens, provenance per label, and an error rate with an interval on it — a
model-produced error rate, per the correction above, which is the gate's weakest joint.

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
- **Both phrasings of the residence sentence count** (HIR-109, 2026-11-03). As first
  written, the check only read *imperative* sentences ("must be located in the US"), so
  Clera's "Remote within the United States." — a plain declarative LOCATION line — was
  stored as Remote (EU). That was this rule failing to run, not the accepted risk above:
  the posting has a residence sentence, and an unambiguous one. The declarative shapes
  ("Remote within/in/from <country>", "This role is based in <country>", and a bare
  "Based in <country>." on its own line) now count too, for the same country list. No
  policy changed, and the accepted risk is untouched — a remote posting whose JD says
  nothing about residence still gets in. Still **not** residence evidence, because each
  has a live counter-example: a USD salary band (EU companies quote USD), "visa
  sponsorship is not available" (Clera's own *Berlin* posting carries that sentence), and
  a company fact with no job-or-person subject ("Acme is based in the United States").
  Promoting any of those is a policy change and goes to Chandler.
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
