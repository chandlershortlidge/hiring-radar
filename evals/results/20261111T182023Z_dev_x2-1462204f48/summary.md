# Eval 20261111T182023Z_dev_x2-1462204f48

- split: `dev`, goldens: 48, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-1462204f48`, taxonomy v11

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.908 | 0.907 | 0.910 |
| recall | 0.918 | 0.910 | 0.922 |
| f1 | 0.913 | 0.910 | 0.915 |
| requirement_accuracy | 0.948 | 0.935 | 0.960 |
| seniority_accuracy | 0.958 | 0.958 | 0.958 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.889 | 0.875 | 0.896 |
| production_accuracy | 0.917 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.925 | 0.918 | 0.929 |
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
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | rag |
| 4 | agents | agents |
| 5 | evaluation | evaluation |
| 6 | rag | cloud |
| 7 | cloud | machine-learning |
| 8 | aws | aws |
| 9 | machine-learning | ci-cd |
| 10 | apis | testing |

## Most-missed skills (all runs)

- software-engineering: 32
- ai-deployment: 27
- ai-ml: 27
- apis: 12
- ml-engineering: 12
- evaluation: 7
- frontend-development: 6
- data-privacy-and-security: 5
- model-development: 5
- llms: 4
- agents: 4
- prompt-engineering: 3
- persistence: 3
- data-science: 3
- software-architecture: 3

## Most-frequent extras (all runs)

- testing: 17
- data-pipelines: 13
- llm-guardrails: 8
- software-engineering: 6
- mcp: 6
- observability: 6
- tool-calling: 6
- backend-development: 6
- git: 6
- llm-orchestration: 5
- ai-deployment: 5
- software-architecture: 5
- vector-search: 5
- api-design: 4
- ci-cd: 4

## Proposed new skills (all runs)

- CUDA Graphs: 3
- FPGA: 3
- Fivetran: 3
- Hightouch: 3
- Looker: 3
- Redshift: 3
- ASIC: 2
- XLA: 2
- Authentication and Authorization: 1
- Datadog: 1
- Mastra: 1
- Svelte: 1
- Vercel AI SDK: 1
