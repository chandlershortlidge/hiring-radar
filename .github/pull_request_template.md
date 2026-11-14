<!-- If this PR changes the agents' own rules — anything under .claude/, AGENTS.md, this
template, .github/workflows/, scripts/rules_gate.py — do NOT write the "Did you authorize
these?" block yourself. The reviewer writes it and adds it here, and the PR waits for
Chandler either way (AGENTS.md "The rules gate"). The "Rules gate" check stays red until
then, by design.

What you DO write for such a PR, as the first three lines of this description, is the
recommendation to approve (AGENTS.md "What Chandler is asked", "Big calls come in two
kinds"), one sentence each, plain words, no ticket ids:

**Recommend:** <what to do>.
**What it is:** <one sentence>.
**Why:** <one sentence>.

Write them above this comment, as plain text. Any other PR has no such lines. -->

## Decisions taken

<!-- Only judgment calls (AGENTS.md "Deciding alone vs. stopping"). One sentence each:
what, why, how to undo. Plain words — a reader who hasn't seen the code should be able
to say "fine" or "no". Mechanical choices don't belong here. "None" is a valid answer. -->

## Decided for you

<!-- Small calls on Chandler's list that the senior agent decided so he was not asked
(AGENTS.md "What Chandler is asked", "Small calls"). One line each, copied unchanged from
the senior agent's reply: what was decided, why, how to undo it. No file or function
names: the Monday summary prints these lines as they are. "None" if there were none. -->

## Needs Chandler

<!-- Only items on the big side of Chandler's list (AGENTS.md "What Chandler is asked")
that block the merge, each as the senior agent wrote it under its heading: **To approve**
(three lines: Recommend / What it is / Why) or **To think about** (the full question, with
options and what he would learn). Also posted on the
Linear issue with an @mention. Anything else goes to the decider, not here. "None" if
nothing blocks. -->

## Escalations

<!-- Every question handed to the decider or the senior agent (AGENTS.md "Escalate to a
stronger agent before a person"), one line each: who asked, what, what was answered.
"None" if there were none. -->

## Follow-ups

<!-- Things worth knowing that do NOT need an answer. Never phrase these as questions.
Two lists, in this order; "None" is fine for either. -->

**Changes what you'd see** — anything that alters the chart, the job list, a count, or
which jobs get in or out. One line each, with the ticket it was filed as.

**Internal** — refactors, test gaps, docs, tooling. One line each, with the ticket.

## Eval (dev)

<!-- Required when the diff touches app/extract.py or taxonomy/skills.json, and only then
(AGENTS.md "The eval gate"). Delete this whole section otherwise.

Paste the output of `uv run python scripts/eval_table.py <run_id>` verbatim, and commit
the evals/results/<run_id>/ directory in this PR — that run is the baseline the next
extractor change is measured against.

Or, if `scripts/eval_table.py --version-check` said MATCH: paste its two version lines and
say the run was skipped because the committed baseline already scored this extractor.

Either stop line puts the PR on Chandler's list - a per-Golden attribute score (seniority,
German, degree, production) that lost more than 2 Goldens, or a skill score down more than
0.02. Say so here, label the PR needs-chandler, and don't merge. The "Goldens worse /
better" column is what decides the attribute rows; their delta is context, so don't read a
0.05 move there as a regression - it is one posting (HIR-164). -->

## Testing

<!-- What you ran and what it said. Commands and their result, not "tests pass". -->

## Risk

<!-- What could break, and what is outside the blast radius. "None" needs a reason. -->

## How to revert

<!-- The steps back out: a plain revert, or the migration / config / data that has to be
undone with it. -->
