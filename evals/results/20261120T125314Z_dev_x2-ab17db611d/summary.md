# Eval 20261120T125314Z_dev_x2-ab17db611d

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-ab17db611d`, taxonomy v12, output cap 4096

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.906 | 0.905 | 0.907 |
| recall | 0.906 | 0.902 | 0.908 |
| f1 | 0.906 | 0.903 | 0.907 |
| requirement_accuracy | 0.949 | 0.947 | 0.950 |
| seniority_accuracy | 0.958 | 0.944 | 0.972 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.953 | 0.944 | 0.958 |
| production_accuracy | 0.933 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.999 | 1.000 |
| group_f1 | 0.726 | 0.707 | 0.743 |
| rank_spearman | 0.932 | 0.931 | 0.933 |
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
| 5 | evaluation | evaluation |
| 6 | cloud | ci-cd |
| 7 | rag | cloud |
| 8 | machine-learning | machine-learning |
| 9 | aws | aws |
| 10 | ai-ml | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 44
- ai-deployment: 43
- ai-ml: 43
- apis: 12
- ml-engineering: 12
- mlops: 9
- cloud: 8
- data-privacy-and-security: 8
- model-development: 8
- software-architecture: 7
- evaluation: 6
- data-science: 6
- devops: 6
- workflow-automation: 6
- frontend-development: 4

## Most-frequent extras (all runs)

- testing: 16
- observability: 15
- llm-orchestration: 10
- software-engineering: 10
- mcp: 9
- ci-cd: 9
- software-architecture: 8
- data-pipelines: 8
- git: 7
- vector-search: 6
- access-control: 6
- kubernetes: 6
- tool-calling: 6
- data-engineering: 6
- context-engineering: 6

## Proposed new skills (all runs)

- CUDA Graphs: 3
- FPGA/ASIC: 3
- Datadog: 3
- FusionAuth: 3
- Mastra: 3
- Retool: 3
- Svelte: 3
- Vercel AI SDK: 3
- Microsoft SQL Server: 3
- AWS Glue: 3
- AWS Lake Formation: 3
- AWS CDK: 2
- Triton: 2
- Classification Models: 1
- Clustering: 1
