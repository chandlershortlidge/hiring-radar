## Decisions taken

<!-- Only judgment calls (AGENTS.md "Deciding alone vs. stopping"). One sentence each:
what, why, how to undo. Plain words — a reader who hasn't seen the code should be able
to say "fine" or "no". Mechanical choices don't belong here. "None" is a valid answer. -->

## Needs Chandler

<!-- Only things that block the merge: questions you stopped on, one line each, with the
options. Also posted on the Linear issue with an @mention. "None" if nothing blocks. -->

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

A metric down more than 0.02 is on the stop list: say so here, label the PR
needs-chandler, and don't merge. -->

## Testing

<!-- What you ran and what it said. Commands and their result, not "tests pass". -->

## Risk

<!-- What could break, and what is outside the blast radius. "None" needs a reason. -->

## How to revert

<!-- The steps back out: a plain revert, or the migration / config / data that has to be
undone with it. -->
