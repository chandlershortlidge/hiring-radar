# Eval 20261119T115637Z_dev_x2-74fe9359b6

- split: `dev`, goldens: 58, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-74fe9359b6`, taxonomy v12

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.918 | 0.912 | 0.922 |
| recall | 0.894 | 0.891 | 0.897 |
| f1 | 0.906 | 0.902 | 0.909 |
| requirement_accuracy | 0.937 | 0.934 | 0.940 |
| seniority_accuracy | 0.960 | 0.931 | 0.983 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.879 | 0.862 | 0.897 |
| production_accuracy | 0.967 | 0.950 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.999 | 1.000 |
| group_f1 | 0.724 | 0.690 | 0.747 |
| rank_spearman | 0.919 | 0.916 | 0.920 |
| top10_overlap | 0.867 | 0.800 | 0.900 |

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
| 6 | rag | aws |
| 7 | cloud | cloud |
| 8 | machine-learning | machine-learning |
| 9 | aws | ci-cd |
| 10 | ai-deployment | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 45
- ai-deployment: 43
- ai-ml: 37
- apis: 15
- ml-engineering: 12
- model-development: 10
- evaluation: 9
- software-architecture: 8
- llms: 7
- data-science: 6
- data-privacy-and-security: 6
- workflow-automation: 6
- frontend-development: 5
- cloud: 4
- prompt-engineering: 3

## Most-frequent extras (all runs)

- testing: 14
- llm-orchestration: 8
- data-pipelines: 8
- git: 8
- access-control: 6
- mcp: 6
- observability: 6
- multi-agent-systems: 6
- tool-calling: 6
- data-engineering: 6
- context-engineering: 6
- a-b-testing: 6
- ai-ml: 5
- software-engineering: 5
- claude-code: 4

## Proposed new skills (all runs)

- CUDA Graphs: 3
- FPGA/ASIC: 3
- Triton: 3
- Datadog: 3
- Mastra: 3
- Svelte: 3
- Vercel AI SDK: 3
- Django: 3
- AWS CDK: 3
- AWS CloudFormation: 2
- FusionAuth: 2
- Retool: 2
- Hex: 1
- Looker: 1
- Model routing: 1
