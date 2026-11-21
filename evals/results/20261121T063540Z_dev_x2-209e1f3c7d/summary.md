# Eval 20261121T063540Z_dev_x2-209e1f3c7d

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-209e1f3c7d`, taxonomy v13, output cap 4096

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.912 | 0.911 | 0.913 |
| recall | 0.899 | 0.890 | 0.906 |
| f1 | 0.906 | 0.900 | 0.910 |
| requirement_accuracy | 0.950 | 0.947 | 0.957 |
| seniority_accuracy | 0.958 | 0.944 | 0.972 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.967 | 0.958 | 0.972 |
| production_accuracy | 0.967 | 0.950 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.999 | 1.000 |
| group_f1 | 0.674 | 0.635 | 0.704 |
| rank_spearman | 0.932 | 0.923 | 0.939 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

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
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | agents |
| 4 | agents | rag |
| 5 | evaluation | ci-cd |
| 6 | cloud | cloud |
| 7 | rag | evaluation |
| 8 | machine-learning | machine-learning |
| 9 | aws | software-engineering |
| 10 | ai-ml | aws |

## Most-missed skills (all runs)

- software-engineering: 45
- ai-deployment: 45
- ai-ml: 40
- apis: 12
- ml-engineering: 12
- model-development: 10
- mlops: 9
- data-privacy-and-security: 8
- cloud: 8
- frontend-development: 7
- evaluation: 7
- software-architecture: 7
- backend-development: 6
- data-science: 6
- devops: 6

## Most-frequent extras (all runs)

- observability: 15
- testing: 13
- data-pipelines: 11
- llm-orchestration: 10
- software-architecture: 9
- ci-cd: 9
- software-engineering: 8
- a-b-testing: 7
- vector-search: 6
- access-control: 6
- kubernetes: 6
- mcp: 6
- tool-calling: 6
- data-engineering: 6
- context-engineering: 6

## Proposed new skills (all runs)

- CUDA Graphs: 3
- FPGA/ASIC: 3
- Mastra: 3
- Vercel AI SDK: 3
- AWS Glue: 3
- AWS Lake Formation: 3
- Datadog: 2
- Classification Models: 1
- Clustering: 1
- Keras: 1
- Re-ranking: 1
- Hex: 1
- Looker: 1
- Apache Beam: 1
- Kiro CLI: 1
