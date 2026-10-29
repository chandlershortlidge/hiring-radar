# Eval 20261029T154143Z_heldout_x2-2e0cac6944

- split: `heldout`, goldens: 4, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-2e0cac6944`, taxonomy v4

| metric | mean | min | max |
|---|---|---|---|
| precision | 1.000 | 1.000 | 1.000 |
| recall | 0.924 | 0.912 | 0.947 |
| f1 | 0.960 | 0.954 | 0.973 |
| requirement_accuracy | 0.981 | 0.963 | 1.000 |
| seniority_accuracy | 1.000 | 1.000 | 1.000 |
| german_accuracy | 0.750 | 0.750 | 0.750 |
| degree_accuracy | 0.750 | 0.750 | 0.750 |
| production_accuracy | 1.000 | 1.000 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.763 | 0.752 | 0.786 |
| top10_overlap | 0.800 | 0.800 | 0.800 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 0 | — | — |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 3 | 1.000 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 0 | 0 | 0 |
| nice_to_have | 0 | 1 | 0 |
| none | 0 | 0 | 3 |

Signal agreement where the class was right: 1.000 over 1 Goldens.

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
- observability: 2
- software-engineering: 2

## Most-frequent extras (all runs)


## Proposed new skills (all runs)

- SciPy: 3
- Survival Analysis: 3
- Polars: 2

## Scope of the production score (hand-written 2026-10-29, after the run)

**Production experience is scored out of sample for the first time here: 1.000 in all three
runs, n=4, signal agreement 1.000.** This supersedes the "no out-of-sample score" note on
`20261029T150158Z_heldout_x2-2e0cac6944`, which ran at the same extractor hash before
golden_021–024 carried production labels (entered 2026-10-29 from two blind labelers,
`evals/labeling/20261029T153540Z_heldout_production/`, with golden_024 adjudicated).

**The set has no `required` case, so this run tests false positives only.** Gold is three
not-mentioned and one `nice_to_have`:

| class | support | what 1.000 means here |
|---|---|---|
| `required` | **0** | nothing measured — no evidence either way |
| `nice_to_have` | 1 | one optional-marker case, right 3/3, right clause |
| none | 3 | three decoys correctly rejected 3/3 |

So the result says the extractor does not invent a production demand where the postings
make none — on three postings whose production mentions are all responsibilities
("models that run in production", "from first idea to production", "der Weg vom Prototyp
in die Produktion", "das Deployment von Machine-Learning-Modellen"). It says nothing about
whether a real demand is caught. **Required recall is still measured only on dev** (8/8 at
this hash, tuned on), and the dev set's one standing weakness is a missed demand
(golden_011, wrong 3/3), which this split cannot see. A held-out `required` case is the
gap to close next.

**One finding worth keeping.** golden_024's `nice_to_have` rests on "Erfahrung mit dem
Betrieb, der Überwachung oder der Fehlerbehebung bei einem ML-Modell oder einer
Datenpipeline." — an operate demand under an optional heading, carrying **no production
word at all**. The extractor quoted that clause character for character. The candidate rule
deferred on 2026-10-29 — *the production object is necessary, the verb is not* — would have
labeled this posting not mentioned and broken the case. The two labelers split on exactly
that question. Evidence against applying that rule, and a reason the held-out set was worth
labeling before touching the prompt again.
