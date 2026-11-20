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

A run also records the output cap it ran under (`meta.max_tokens`), because the run id and
the extractor fingerprint do not encode it: two runs of one model under different caps
would otherwise look identical afterwards.

| run | what it measured | ticket |
|---|---|---|
| `20261119T150606Z_dev_x2-8425c19abb` | Claude Haiku 5.5 at the live 4096-token output cap. 34 of 213 readings were cut off at the cap and returned nothing, so this measures the cap, not the model. Kept as the record of that failure rate. | HIR-223 |
| `20261119T155329Z_dev_x2-8425c19abb` | Claude Haiku 5.5 at an 8192-token output cap, no failures. The comparison against the Claude Sonnet 5.5 baseline of the same day. | HIR-223 |
| `20261120T060535Z_dev_x2-e9c713ffc3` | Claude Haiku 5.5 at an 8192-token cap with the trial rule in `trials/hir-368-broad-skills.md` (report a broad skill whenever its name is written). Broad-skill misses (cloud, machine learning, agents, LLMs) fell from 56 to 26 over 213 readings. | HIR-368 |

## Prompt trials

`trials/` holds instructions measured with `scripts/run_eval.py --prompt-trial <file>`. The
file's text is added after the extractor's rules for that run only; the live prompt in
`app/extract.py` is untouched, and the run gets its own extractor version, hashed from the
prompt it was actually sent, with the file's name and text in `summary.json` under
`meta.prompt_trial`. Adopting a trial means copying it into `app/extract.py`, which goes
through the eval gate like any prompt change.
