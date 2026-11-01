# Eval 20261101T100707Z_dev_x2-7e68bbee42

- split: `dev`, goldens: 20, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-7e68bbee42`, taxonomy v5

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.881 | 0.877 | 0.884 |
| recall | 0.970 | 0.967 | 0.973 |
| f1 | 0.924 | 0.923 | 0.925 |
| requirement_accuracy | 0.993 | 0.991 | 0.994 |
| seniority_accuracy | 0.967 | 0.950 | 1.000 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.950 | 0.950 | 0.950 |
| production_accuracy | 0.950 | 0.950 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.907 | 0.902 | 0.913 |
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
| 6 | apis | apis |
| 7 | aws | aws |
| 8 | cloud | ci-cd |
| 9 | prompt-engineering | langchain |
| 10 | ci-cd | testing |

## Most-missed skills (all runs)

- software-engineering: 6
- ai-deployment: 6
- apis: 5
- llms: 5
- prompt-engineering: 3
- ml-engineering: 3
- cloud: 1
- ai-ml: 1

## Most-frequent extras (all runs)

- testing: 12
- software-engineering: 6
- observability: 6
- tool-calling: 6
- data-pipelines: 5
- fine-tuning: 5
- chain-of-thought: 4
- jupyter-notebooks: 3
- aws-s3: 3
- llm-orchestration: 3
- azure: 3
- claude-code: 3
- claude-enterprise: 3
- event-driven-systems: 3
- kubernetes: 3

## Proposed new skills (all runs)

