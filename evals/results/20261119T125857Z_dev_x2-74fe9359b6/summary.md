# Eval 20261119T125857Z_dev_x2-74fe9359b6

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-74fe9359b6`, taxonomy v12

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.913 | 0.911 | 0.916 |
| recall | 0.890 | 0.881 | 0.896 |
| f1 | 0.901 | 0.898 | 0.904 |
| requirement_accuracy | 0.948 | 0.947 | 0.948 |
| seniority_accuracy | 0.953 | 0.944 | 0.958 |
| german_accuracy | 0.995 | 0.986 | 1.000 |
| degree_accuracy | 0.887 | 0.873 | 0.901 |
| production_accuracy | 0.983 | 0.950 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.998 | 1.000 |
| group_f1 | 0.750 | 0.725 | 0.773 |
| rank_spearman | 0.933 | 0.929 | 0.936 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 1.000 | 1.000 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 1.000 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 1 | 0 |
| none | 0 | 0 | 11 |

Signal agreement where the class was right: 1.000 over 9 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | agents |
| 4 | agents | rag |
| 5 | evaluation | evaluation |
| 6 | cloud | cloud |
| 7 | rag | machine-learning |
| 8 | machine-learning | aws |
| 9 | aws | ci-cd |
| 10 | ai-ml | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 48
- ai-ml: 45
- ai-deployment: 44
- apis: 16
- ml-engineering: 12
- mlops: 11
- software-architecture: 10
- cloud: 9
- evaluation: 9
- data-privacy-and-security: 9
- model-development: 9
- llms: 7
- data-science: 6
- backend-development: 6
- workflow-automation: 6

## Most-frequent extras (all runs)

- observability: 15
- testing: 14
- llm-orchestration: 10
- ci-cd: 10
- git: 8
- software-engineering: 7
- mcp: 7
- data-pipelines: 7
- access-control: 6
- kubernetes: 6
- software-architecture: 6
- tool-calling: 6
- data-engineering: 6
- context-engineering: 6
- a-b-testing: 6

## Proposed new skills (all runs)

- CUDA Graphs: 3
- FPGA/ASIC: 3
- Datadog: 3
- Mastra: 3
- Vercel AI SDK: 3
- Django: 3
- AWS CDK: 3
- Microsoft SQL Server: 3
- VPN: 3
- AWS Glue: 3
- AWS Lake Formation: 3
- Triton: 2
- Apache Beam: 2
- AWS CloudFormation: 2
- Keras: 2
