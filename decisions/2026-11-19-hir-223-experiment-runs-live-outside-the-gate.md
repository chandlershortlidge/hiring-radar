## 2026-11-19 — an eval run of a model we don't use is committed outside the gate's folder (HIR-223)

HIR-223 measures a cheaper model, Claude Haiku 5.5, on the same test postings the live
model was measured on, so the two can be compared. That run's per-posting results are worth
keeping: the question it feeds — whether to switch the model that reads postings — will want
them again.

But the eval gate picks its baseline as the newest committed run under `evals/results/`,
with no filter on which model produced it. Committing a Haiku run there would have made it
the baseline, so the next change to the extractor or the skill list would have been scored
against a model nobody is using, and every such branch would have been told its extractor
differed from the measured one until a new live-model run displaced it.

**Decided:** a run that measures something the live system does not run — another model, a
prompt trial — is committed under `evals/experiments/<run_id>/`, never under
`evals/results/`. `scripts/run_eval.py` is unchanged; the directory is moved by hand before
committing. `evals/experiments/README.md` says so, and two tests pin it:
`test_experiment_runs_are_never_the_baseline` in `tests/test_eval_table.py` and the
`evals/experiments/...` case in `tests/test_eval_gate.py`. Both passed with no change to
either script, because the baseline picker and the CI gate are already anchored on
`evals/results/`.

**Why not change the gate instead** (filter the baseline by the model in use): that would
change how quality is measured, which is Chandler's to think through, and it is not needed
to answer this ticket. The folder keeps the evidence without touching the rule.

**To undo:** delete `evals/experiments/`. Nothing reads it; the gate never did.

Decided by the senior agent on the worker's question, 2026-11-19. Not on Chandler's list:
the gate's rule, the stored jobs, the money and what visitors see are all untouched.
