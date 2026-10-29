# Eval 20261029T122622Z_dev_x2-2e0cac6944

- split: `dev`, goldens: 20, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-2e0cac6944`, taxonomy v4

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.881 | 0.878 | 0.883 |
| recall | 0.967 | 0.964 | 0.970 |
| f1 | 0.922 | 0.919 | 0.924 |
| requirement_accuracy | 0.989 | 0.988 | 0.991 |
| seniority_accuracy | 0.817 | 0.800 | 0.850 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.950 | 0.950 | 0.950 |
| production_accuracy | 0.933 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.914 | 0.908 | 0.917 |
| top10_overlap | 0.800 | 0.800 | 0.800 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 1.000 | 1.000 |
| nice_to_have | 1 | — | 0.000 |
| none | 11 | 0.917 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 0 | 1 |
| none | 0 | 0 | 11 |

Signal agreement where the class was right: 1.000 over 8 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | llms | llms |
| 2 | python | python |
| 3 | rag | rag |
| 4 | agents | agents |
| 5 | evaluation | evaluation |
| 6 | apis | aws |
| 7 | aws | ci-cd |
| 8 | cloud | cloud |
| 9 | prompt-engineering | langchain |
| 10 | ci-cd | testing |

## Most-missed skills (all runs)

- software-engineering: 9
- apis: 7
- ai-deployment: 6
- prompt-engineering: 3
- ml-engineering: 3
- ai-ml: 3
- agent-architecture: 1
- evaluation: 1

## Most-frequent extras (all runs)

- testing: 12
- software-engineering: 6
- observability: 6
- tool-calling: 6
- data-pipelines: 6
- llm-guardrails: 4
- jupyter-notebooks: 3
- aws-s3: 3
- llm-orchestration: 3
- azure: 3
- claude-code: 3
- claude-enterprise: 3
- event-driven-systems: 3
- kubernetes: 3
- mcp: 3

## Proposed new skills (all runs)


## Known misses and caveats (hand-written 2026-10-29, after the run)

Production experience: **0.933** mean (0.950 / 0.900 / 0.950), 4 error instances over 3
runs, with both decoy rows at zero — no responsibility read as a requirement, no
code-quality bar read as a requirement, and no wrong-signal error in any run. The two
remaining misses are **accepted, not fixed**: tuning the prompt further on 20 Goldens is
fitting the dev set.

- **golden_011, wrong 3/3** (gold `nice_to_have`, predicted not mentioned, signal `None`).
  "…recommender systems, GenAI, data platforms or production ML would be highly relevant"
  is a bare noun phrase in a list of optional extras, with no build/ship/operate verb, so
  the prompt's verb-against-object test never nominates the clause and the optional-marker
  rule is never reached. `nice_to_have` has **support 1** on dev — one item is not a
  measurement, and that class's precision/recall row is noise in either direction.
- **golden_010, wrong 1 of 3 runs** (gold not mentioned, predicted `required`). The model
  quoted "You would rather ship a working automation in two weeks than a perfect one in
  six months" — a working-style preference: the verb *ship* with no production object. A
  1-of-3 flip, not a systematic error.
- These two point opposite ways (011 wants the object to carry the demand with no verb;
  010 wants the verb to count for nothing without a production object) and are both
  answered by one candidate rule — the production object is necessary, the verb is not.
  Recorded in DECISIONS 2026-10-29 as a candidate for the next iteration, **not applied**.

**Prompt contamination.** `golden_018` is contaminated and its 3/3 correct `required` must
be discounted: "strong Python skills, including writing production-quality code and tests"
is the prompt's own `null` example, 8 words verbatim. Excluding it: 18/19, 17/19, 18/19 —
mean 0.930. `golden_015`, `golden_020` and `golden_006` are close-paraphrase cases (the
prompt teaches their decoy pattern in near-identical wording), so those three correct
rejections are softer than they look. No other Golden shares a 4-gram with the production
rules; `golden_001`/`golden_002` share "degree in computer science" with the degree rule,
which inflates degree, not production.

These are dev numbers, tuned on. The held-out Goldens (021–024) are the real score.
