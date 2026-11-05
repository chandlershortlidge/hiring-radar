# Eval 20261105T100120Z_dev_x2-3d3b911b0a

- split: `dev`, goldens: 20, repeats: 1
- model: `claude-sonnet-5-5`, extractor: `x2-3d3b911b0a`, taxonomy v9

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.879 | 0.879 | 0.879 |
| recall | 0.973 | 0.973 | 0.973 |
| f1 | 0.924 | 0.924 | 0.924 |
| requirement_accuracy | 0.991 | 0.991 | 0.991 |
| seniority_accuracy | 0.950 | 0.950 | 0.950 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.950 | 0.950 | 0.950 |
| production_accuracy | 1.000 | 1.000 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.896 | 0.896 | 0.896 |
| top10_overlap | 0.800 | 0.800 | 0.800 |

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

- software-engineering: 3
- apis: 2
- ai-deployment: 2
- prompt-engineering: 1
- ml-engineering: 1

## Most-frequent extras (all runs)

- testing: 4
- data-pipelines: 3
- software-engineering: 2
- observability: 2
- software-architecture: 2
- tool-calling: 2
- jupyter-notebooks: 1
- aws-s3: 1
- llm-orchestration: 1
- azure: 1
- claude-code: 1
- claude-enterprise: 1
- event-driven-systems: 1
- kubernetes: 1
- llm-guardrails: 1

## Proposed new skills (all runs)

