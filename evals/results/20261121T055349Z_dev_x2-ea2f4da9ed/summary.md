# Eval 20261121T055349Z_dev_x2-ea2f4da9ed

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-ea2f4da9ed`, taxonomy v12, output cap 4096

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.907 | 0.905 | 0.910 |
| recall | 0.896 | 0.890 | 0.903 |
| f1 | 0.901 | 0.898 | 0.907 |
| requirement_accuracy | 0.947 | 0.946 | 0.948 |
| seniority_accuracy | 0.948 | 0.944 | 0.958 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.972 | 0.944 | 0.986 |
| production_accuracy | 0.967 | 0.950 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.998 | 1.000 |
| group_f1 | 0.692 | 0.678 | 0.711 |
| rank_spearman | 0.925 | 0.919 | 0.932 |
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
| 4 | agents | cloud |
| 5 | evaluation | rag |
| 6 | cloud | ci-cd |
| 7 | rag | evaluation |
| 8 | machine-learning | machine-learning |
| 9 | aws | software-engineering |
| 10 | ai-ml | aws |

## Most-missed skills (all runs)

- software-engineering: 45
- ai-deployment: 45
- ai-ml: 45
- apis: 13
- ml-engineering: 12
- model-development: 9
- mlops: 9
- evaluation: 8
- data-privacy-and-security: 8
- data-science: 6
- software-architecture: 6
- frontend-development: 6
- workflow-automation: 6
- backend-development: 5
- cloud: 5

## Most-frequent extras (all runs)

- observability: 15
- testing: 13
- software-engineering: 12
- ci-cd: 12
- software-architecture: 10
- data-pipelines: 10
- llm-orchestration: 8
- access-control: 6
- kubernetes: 6
- mcp: 6
- tool-calling: 6
- context-engineering: 6
- ai-developer-tooling: 6
- git: 6
- a-b-testing: 6

## Proposed new skills (all runs)

- AWS CDK: 3
- AWS Glue: 3
- AWS Lake Formation: 3
- Mastra: 2
- Vercel AI SDK: 2
- Dataflow: 2
- Pub/Sub: 2
- Triton: 2
- Microsoft SQL Server: 1
- VPN: 1
- AWS CloudFormation: 1
- CUDA Graphs: 1
- FPGA/ASIC: 1
- Datadog: 1
- FusionAuth: 1
