# Eval 20261121T053931Z_dev_x2-1d09d62944

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-1d09d62944`, taxonomy v12, output cap 4096

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.912 | 0.907 | 0.916 |
| recall | 0.903 | 0.899 | 0.906 |
| f1 | 0.907 | 0.905 | 0.911 |
| requirement_accuracy | 0.956 | 0.955 | 0.958 |
| seniority_accuracy | 0.948 | 0.944 | 0.958 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.986 | 0.972 | 1.000 |
| production_accuracy | 0.900 | 0.900 | 0.900 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.999 | 0.999 |
| group_f1 | 0.852 | 0.838 | 0.870 |
| rank_spearman | 0.934 | 0.931 | 0.936 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

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
| 3 | software-engineering | agents |
| 4 | agents | rag |
| 5 | evaluation | evaluation |
| 6 | cloud | ci-cd |
| 7 | rag | cloud |
| 8 | machine-learning | machine-learning |
| 9 | aws | aws |
| 10 | ai-ml | software-engineering |

## Most-missed skills (all runs)

- ai-deployment: 45
- ai-ml: 45
- software-engineering: 44
- apis: 13
- ml-engineering: 12
- cloud: 10
- mlops: 9
- data-privacy-and-security: 8
- model-development: 8
- software-architecture: 7
- evaluation: 6
- data-science: 6
- workflow-automation: 6
- agents: 5
- frontend-development: 5

## Most-frequent extras (all runs)

- observability: 15
- testing: 14
- ci-cd: 10
- llm-orchestration: 9
- data-pipelines: 9
- vector-search: 7
- mcp: 7
- a-b-testing: 7
- software-engineering: 6
- access-control: 6
- data-privacy-and-security: 6
- kubernetes: 6
- tool-calling: 6
- data-engineering: 6
- context-engineering: 6

## Proposed new skills (all runs)

- CUDA Graphs: 3
- FPGA/ASIC: 3
- Datadog: 3
- Mastra: 3
- Vercel AI SDK: 3
- AWS CDK: 3
- Keras: 3
- OCR: 3
- AWS Glue: 3
- AWS Lake Formation: 3
- Jira: 3
- Scrum: 3
- Classification Models: 2
- Clustering: 2
- Re-ranking: 2
