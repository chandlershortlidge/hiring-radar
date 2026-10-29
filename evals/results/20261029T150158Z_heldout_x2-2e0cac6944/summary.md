# Eval 20261029T150158Z_heldout_x2-2e0cac6944

- split: `heldout`, goldens: 4, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-2e0cac6944`, taxonomy v4

| metric | mean | min | max |
|---|---|---|---|
| precision | 1.000 | 1.000 | 1.000 |
| recall | 0.924 | 0.912 | 0.930 |
| f1 | 0.960 | 0.954 | 0.964 |
| requirement_accuracy | 0.968 | 0.962 | 0.981 |
| seniority_accuracy | 1.000 | 1.000 | 1.000 |
| german_accuracy | 0.750 | 0.750 | 0.750 |
| degree_accuracy | 0.750 | 0.750 | 0.750 |
| production_accuracy | — | — | — |
| production_signal_agreement | — | — | — |
| rank_spearman | 0.762 | 0.752 | 0.767 |
| top10_overlap | 0.800 | 0.800 | 0.800 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 0 | — | — |
| nice_to_have | 0 | — | — |
| none | 0 | — | — |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 0 | 0 | 0 |
| nice_to_have | 0 | 0 | 0 |
| none | 0 | 0 | 0 |

Signal agreement where the class was right: — over 0 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | sql | sql |
| 3 | ai-deployment | airflow |
| 4 | airflow | aws |
| 5 | aws | docker |
| 6 | data-pipelines | gcp |
| 7 | docker | git |
| 8 | gcp | kubernetes |
| 9 | git | machine-learning |
| 10 | kubernetes | nosql |

## Most-missed skills (all runs)

- ai-deployment: 6
- data-pipelines: 3
- software-engineering: 3
- evaluation: 1

## Most-frequent extras (all runs)


## Proposed new skills (all runs)

- SciPy: 3
- Survival Analysis: 3
- Polars: 2

## No held-out score for production experience (hand-written 2026-10-29, after the run)

`production_accuracy` and `production_signal_agreement` are `—` and every per-class
support is 0 because **`production_n = 0` in all three runs**: golden_021–024 carry
`seniority`, `german` and `degree` only. They were labeled at the held-out freeze
(DECISIONS 2026-10-16), twelve days before production experience was decided as an
attribute (2026-10-28), so there is nothing for the extractor's production output to be
scored against. The dashes are correct behaviour, not a scoring bug — `run_once` scores
the attribute only for a Golden that carries the key.

The extractor did produce a production value for all four held-out JDs; those predictions
are in `predictions.jsonl` and are **unscored**. They were deliberately not compared by
hand: labeling the held-out set post hoc, by the same labeler whose rules are under test,
is a weaker guarantee than labeling it before the rules were written, and the held-out
labels were not to be read or changed on this run.

**So production has no out-of-sample score yet.** 0.933 on dev (20261029T122622Z) is a
tuned-on number and is the only production figure this branch has. Labeling golden_021–024
for production is the next step and a release decision, together with the
`## Production experience` section `evals/LABELING.md` still owes.

For the attributes that are labeled here, this run is a clean held-out point at
`x2-2e0cac6944`: skills P 1.000 / R 0.924 / F1 0.960, requirement accuracy 0.968,
seniority 1.000 (4/4), German 0.750 (3/4), degree 0.750 (3/4), 0 extraction errors.
