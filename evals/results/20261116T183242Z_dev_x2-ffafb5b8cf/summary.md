# Eval 20261116T183242Z_dev_x2-ffafb5b8cf

- split: `dev`, goldens: 58, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-ffafb5b8cf`, taxonomy v11

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.919 | 0.918 | 0.920 |
| recall | 0.897 | 0.895 | 0.901 |
| f1 | 0.908 | 0.906 | 0.910 |
| requirement_accuracy | 0.940 | 0.937 | 0.942 |
| seniority_accuracy | 0.937 | 0.931 | 0.948 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.885 | 0.879 | 0.897 |
| production_accuracy | 0.950 | 0.900 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.999 | 1.000 |
| group_f1 | 0.723 | 0.705 | 0.743 |
| rank_spearman | 0.940 | 0.936 | 0.945 |
| top10_overlap | 0.867 | 0.800 | 0.900 |

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
| 4 | agents | evaluation |
| 5 | evaluation | rag |
| 6 | rag | machine-learning |
| 7 | cloud | cloud |
| 8 | machine-learning | aws |
| 9 | aws | ci-cd |
| 10 | ai-deployment | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 45
- ai-deployment: 42
- ai-ml: 38
- apis: 16
- ml-engineering: 12
- model-development: 11
- evaluation: 6
- data-science: 6
- agents: 6
- software-architecture: 6
- workflow-automation: 6
- llms: 4
- data-privacy-and-security: 4
- frontend-development: 4
- mlops: 4

## Most-frequent extras (all runs)

- testing: 16
- llm-orchestration: 9
- data-pipelines: 9
- git: 9
- software-engineering: 6
- mcp: 6
- observability: 6
- tool-calling: 6
- a-b-testing: 6
- workflow-automation: 6
- software-architecture: 5
- llm-guardrails: 5
- serverless: 4
- data-privacy-and-security: 4
- ai-deployment: 4

## Proposed new skills (all runs)

- Looker: 3
- Datadog: 3
- Mastra: 3
- Svelte: 3
- Vercel AI SDK: 3
- AWS CDK: 3
- ASIC: 2
- CUDA Graphs: 2
- CuTe DSL: 2
- FPGA: 2
- Pallas: 2
- Triton: 2
- XLA: 2
- Fivetran: 2
- Hex: 2
