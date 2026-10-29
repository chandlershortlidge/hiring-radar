# Eval 20261029T110558Z_dev_x2-52603296d5

- split: `dev`, goldens: 20, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-52603296d5`, taxonomy v4

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.875 | 0.874 | 0.876 |
| recall | 0.967 | 0.964 | 0.970 |
| f1 | 0.919 | 0.918 | 0.921 |
| requirement_accuracy | 0.989 | 0.988 | 0.991 |
| seniority_accuracy | 0.817 | 0.800 | 0.850 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.950 | 0.950 | 0.950 |
| production_accuracy | 0.833 | 0.800 | 0.900 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.906 | 0.901 | 0.911 |
| top10_overlap | 0.733 | 0.700 | 0.800 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 0.857 | 0.750 |
| nice_to_have | 1 | — | 0.000 |
| none | 11 | 0.769 | 0.909 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 6 | 0 | 2 |
| nice_to_have | 0 | 0 | 1 |
| none | 1 | 0 | 10 |

Signal agreement where the class was right: 1.000 over 6 Goldens.

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

- software-engineering: 8
- apis: 7
- ai-deployment: 6
- prompt-engineering: 3
- ml-engineering: 3
- ai-ml: 3
- cloud: 3

## Most-frequent extras (all runs)

- testing: 12
- data-pipelines: 9
- observability: 8
- software-engineering: 6
- tool-calling: 6
- software-architecture: 5
- llm-guardrails: 4
- jupyter-notebooks: 3
- llm-orchestration: 3
- azure: 3
- claude-code: 3
- claude-enterprise: 3
- event-driven-systems: 3
- kubernetes: 3
- mcp: 3

## Proposed new skills (all runs)

