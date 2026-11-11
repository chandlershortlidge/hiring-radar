# Eval 20261111T095159Z_dev_x2-1462204f48

- split: `dev`, goldens: 35, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-1462204f48`, taxonomy v11

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.901 | 0.895 | 0.905 |
| recall | 0.925 | 0.912 | 0.934 |
| f1 | 0.913 | 0.909 | 0.919 |
| requirement_accuracy | 0.947 | 0.933 | 0.961 |
| seniority_accuracy | 0.981 | 0.971 | 1.000 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.971 | 0.971 | 0.971 |
| production_accuracy | 0.917 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.938 | 0.927 | 0.947 |
| top10_overlap | 0.833 | 0.800 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 1.000 | 0.875 |
| nice_to_have | 1 | — | 0.000 |
| none | 11 | 0.846 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 7 | 0 | 1 |
| nice_to_have | 0 | 0 | 1 |
| none | 0 | 0 | 11 |

Signal agreement where the class was right: 1.000 over 7 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | llms | llms |
| 2 | python | python |
| 3 | rag | rag |
| 4 | agents | agents |
| 5 | software-engineering | ci-cd |
| 6 | cloud | cloud |
| 7 | evaluation | aws |
| 8 | aws | evaluation |
| 9 | ci-cd | gcp |
| 10 | apis | observability |

## Most-missed skills (all runs)

- software-engineering: 24
- ai-deployment: 24
- ai-ml: 12
- apis: 11
- evaluation: 6
- frontend-development: 6
- model-development: 5
- prompt-engineering: 3
- ml-engineering: 3
- agent-architecture: 3
- persistence: 3
- machine-learning: 3
- agents: 3
- model-serving: 3
- devops: 3

## Most-frequent extras (all runs)

- testing: 15
- data-pipelines: 8
- software-engineering: 6
- llm-guardrails: 6
- mcp: 6
- observability: 6
- tool-calling: 6
- backend-development: 6
- git: 6
- chain-of-thought: 5
- software-architecture: 5
- ci-cd: 5
- llm-orchestration: 4
- api-design: 4
- apis: 4

## Proposed new skills (all runs)

- Datadog: 2
- Mastra: 2
- Vercel AI SDK: 2
- Apache Beam: 2
- FusionAuth: 1
- Retool: 1
- Svelte: 1
