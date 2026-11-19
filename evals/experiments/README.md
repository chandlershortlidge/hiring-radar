# evals/experiments/

Eval runs that measure something the live system does **not** run: another model, a prompt
trial, a setting we were only asking about. They are committed so their numbers can be
checked and re-read later, per posting, long after the session that produced them.

**A run in here is never the eval gate's baseline.** The gate compares a branch against the
newest committed run under `evals/results/` and does not filter by model, so a run of a
different model committed there would quietly become the thing the next extractor change is
measured against — a regression against a model nobody is using. Two tests pin that line:
`test_experiment_runs_are_never_the_baseline` in `tests/test_eval_table.py` and the
`evals/experiments/...` case in `tests/test_eval_gate.py`.

`scripts/run_eval.py` always writes to `evals/results/<run_id>/`. Move the directory here
by hand before committing it:

```bash
mv evals/results/<run_id> evals/experiments/<run_id>
```

Both reporting scripts take a path, so a run in here still compares against the current
baseline:

```bash
uv run python scripts/eval_table.py evals/experiments/<run_id>    # scores vs the baseline
uv run python scripts/eval_cost.py evals/experiments/<run_id>     # what it cost per reading
```

| run | what it measured | ticket |
|---|---|---|
| `20261119T150606Z_dev_x2-8425c19abb` | Claude Haiku 5.5 reading the dev postings, against the Claude Sonnet 5.5 baseline of the same day | HIR-223 |
