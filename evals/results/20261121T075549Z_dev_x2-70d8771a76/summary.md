# Eval 20261121T075549Z_dev_x2-70d8771a76

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-70d8771a76`, taxonomy v14, output cap 4096

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.912 | 0.907 | 0.915 |
| recall | 0.899 | 0.894 | 0.903 |
| f1 | 0.905 | 0.904 | 0.908 |
| requirement_accuracy | 0.945 | 0.944 | 0.946 |
| seniority_accuracy | 0.953 | 0.944 | 0.958 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.972 | 0.972 | 0.972 |
| production_accuracy | 0.967 | 0.950 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.999 | 1.000 |
| group_f1 | 0.682 | 0.682 | 0.682 |
| rank_spearman | 0.928 | 0.920 | 0.934 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 1.000 | 0.875 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 0.917 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 7 | 0 | 1 |
| nice_to_have | 0 | 1 | 0 |
| none | 0 | 0 | 11 |

Signal agreement where the class was right: 1.000 over 8 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | agents |
| 4 | agents | rag |
| 5 | evaluation | evaluation |
| 6 | cloud | machine-learning |
| 7 | rag | ci-cd |
| 8 | machine-learning | cloud |
| 9 | aws | aws |
| 10 | ai-ml | software-engineering |

## Most-missed skills (all runs)

- ai-ml: 46
- software-engineering: 45
- ai-deployment: 44
- apis: 13
- cloud: 12
- ml-engineering: 12
- model-development: 10
- data-privacy-and-security: 9
- mlops: 9
- backend-development: 6
- frontend-development: 6
- evaluation: 6
- data-science: 6
- software-architecture: 6
- agents: 6

## Most-frequent extras (all runs)

- observability: 15
- testing: 15
- data-pipelines: 11
- ci-cd: 10
- llm-orchestration: 9
- mcp: 9
- software-engineering: 6
- access-control: 6
- data-privacy-and-security: 6
- kubernetes: 6
- software-architecture: 6
- tool-calling: 6
- data-engineering: 6
- context-engineering: 6
- git: 6

## Proposed new skills (all runs)

- Datadog: 3
- FusionAuth: 3
- Mastra: 3
- Retool: 3
- Vercel AI SDK: 3
- Svelte: 2
- Jira: 2
- Scrum: 2
- Optimization / Operations Research: 2
- AWS Glue: 2
- AWS Lake Formation: 2
- Django: 1
- Dataflow: 1
- Pub/Sub: 1
- Prisma: 1
