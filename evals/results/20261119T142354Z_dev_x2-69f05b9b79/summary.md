# Eval 20261119T142354Z_dev_x2-69f05b9b79

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-69f05b9b79`, taxonomy v12

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.910 | 0.908 | 0.913 |
| recall | 0.902 | 0.900 | 0.904 |
| f1 | 0.906 | 0.904 | 0.907 |
| requirement_accuracy | 0.948 | 0.947 | 0.949 |
| seniority_accuracy | 0.958 | 0.944 | 0.972 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.972 | 0.972 | 0.972 |
| production_accuracy | 0.933 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.998 | 0.998 | 0.999 |
| group_f1 | 0.719 | 0.713 | 0.726 |
| rank_spearman | 0.932 | 0.927 | 0.939 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 0.889 | 1.000 |
| nice_to_have | 1 | — | 0.000 |
| none | 11 | 0.909 | 0.909 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 0 | 1 |
| none | 1 | 0 | 10 |

Signal agreement where the class was right: 1.000 over 8 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | agents |
| 4 | agents | cloud |
| 5 | evaluation | rag |
| 6 | cloud | ci-cd |
| 7 | rag | evaluation |
| 8 | machine-learning | machine-learning |
| 9 | aws | aws |
| 10 | ai-ml | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 46
- ai-ml: 46
- ai-deployment: 45
- apis: 12
- ml-engineering: 12
- model-development: 11
- mlops: 10
- evaluation: 9
- software-architecture: 9
- data-privacy-and-security: 9
- frontend-development: 7
- data-science: 6
- workflow-automation: 5
- backend-development: 5
- cybersecurity: 5

## Most-frequent extras (all runs)

- testing: 16
- observability: 15
- ci-cd: 11
- data-pipelines: 8
- vector-search: 7
- software-architecture: 7
- git: 7
- software-engineering: 6
- llm-orchestration: 6
- access-control: 6
- kubernetes: 6
- mcp: 6
- ai-deployment: 6
- tool-calling: 6
- context-engineering: 6

## Proposed new skills (all runs)

- Apache Beam: 3
- Mastra: 3
- Vercel AI SDK: 3
- AWS CDK: 3
- Classification Models: 3
- Clustering: 3
- Keras: 3
- Re-ranking: 3
- Microsoft SQL Server: 3
- AWS Glue: 3
- AWS Lake Formation: 3
- Datadog: 2
- FusionAuth: 2
- Retool: 2
- Svelte: 2
