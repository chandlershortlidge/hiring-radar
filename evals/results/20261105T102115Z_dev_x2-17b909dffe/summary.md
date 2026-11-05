# Eval 20261105T102115Z_dev_x2-17b909dffe

- split: `dev`, goldens: 20, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-17b909dffe`, taxonomy v8

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.881 | 0.878 | 0.883 |
| recall | 0.966 | 0.964 | 0.967 |
| f1 | 0.922 | 0.919 | 0.924 |
| requirement_accuracy | 0.987 | 0.985 | 0.988 |
| seniority_accuracy | 0.950 | 0.950 | 0.950 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.950 | 0.950 | 0.950 |
| production_accuracy | 0.950 | 0.950 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.998 | 0.997 | 1.000 |
| rank_spearman | 0.898 | 0.878 | 0.909 |
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

- apis: 9
- software-engineering: 7
- ai-deployment: 6
- prompt-engineering: 3
- ml-engineering: 3
- ai-ml: 3
- llms: 2
- agent-architecture: 1

## Most-frequent extras (all runs)

- testing: 12
- software-engineering: 6
- observability: 6
- tool-calling: 6
- data-pipelines: 6
- software-architecture: 5
- data-privacy-and-security: 4
- llm-guardrails: 4
- jupyter-notebooks: 3
- llm-orchestration: 3
- azure: 3
- claude-code: 3
- claude-enterprise: 3
- event-driven-systems: 3
- kubernetes: 3

## Proposed new skills (all runs)

