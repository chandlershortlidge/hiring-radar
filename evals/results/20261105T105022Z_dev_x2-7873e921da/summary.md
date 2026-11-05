# Eval 20261105T105022Z_dev_x2-7873e921da

- split: `dev`, goldens: 20, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-7873e921da`, taxonomy v10

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.876 | 0.867 | 0.882 |
| recall | 0.968 | 0.961 | 0.973 |
| f1 | 0.920 | 0.916 | 0.925 |
| requirement_accuracy | 0.990 | 0.988 | 0.991 |
| seniority_accuracy | 0.950 | 0.950 | 0.950 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.950 | 0.950 | 0.950 |
| production_accuracy | 0.950 | 0.900 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.886 | 0.883 | 0.888 |
| top10_overlap | 0.767 | 0.700 | 0.800 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 1.000 | 1.000 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 1.000 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 1 | 0 |
| none | 0 | 0 | 11 |

Signal agreement where the class was right: 1.000 over 9 Goldens.

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

- apis: 8
- software-engineering: 6
- ai-deployment: 6
- prompt-engineering: 3
- ml-engineering: 3
- ai-ml: 3
- evaluation: 2
- cloud: 1

## Most-frequent extras (all runs)

- testing: 12
- software-engineering: 6
- observability: 6
- software-architecture: 6
- tool-calling: 6
- data-pipelines: 5
- llm-guardrails: 4
- chain-of-thought: 4
- jupyter-notebooks: 3
- aws-s3: 3
- llm-orchestration: 3
- serverless: 3
- azure: 3
- claude-code: 3
- claude-enterprise: 3

## Proposed new skills (all runs)

