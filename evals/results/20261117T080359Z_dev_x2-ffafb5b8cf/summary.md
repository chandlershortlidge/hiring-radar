# Eval 20261117T080359Z_dev_x2-ffafb5b8cf

- split: `dev`, goldens: 58, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-ffafb5b8cf`, taxonomy v11

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.922 | 0.920 | 0.924 |
| recall | 0.899 | 0.897 | 0.902 |
| f1 | 0.910 | 0.909 | 0.913 |
| requirement_accuracy | 0.939 | 0.938 | 0.940 |
| seniority_accuracy | 0.960 | 0.948 | 0.966 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.879 | 0.879 | 0.879 |
| production_accuracy | 0.967 | 0.950 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 1.000 | 0.999 | 1.000 |
| group_f1 | 0.734 | 0.730 | 0.738 |
| rank_spearman | 0.934 | 0.933 | 0.936 |
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
| 6 | rag | machine-learning |
| 7 | cloud | aws |
| 8 | machine-learning | ci-cd |
| 9 | aws | cloud |
| 10 | ai-deployment | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 44
- ai-deployment: 41
- ai-ml: 37
- apis: 12
- ml-engineering: 12
- model-development: 11
- cloud: 7
- evaluation: 7
- software-architecture: 7
- data-science: 6
- agents: 6
- workflow-automation: 6
- frontend-development: 5
- llms: 5
- data-privacy-and-security: 4

## Most-frequent extras (all runs)

- testing: 13
- llm-orchestration: 10
- data-pipelines: 9
- git: 9
- a-b-testing: 8
- llm-guardrails: 8
- software-engineering: 6
- mcp: 6
- observability: 6
- ai-deployment: 6
- tool-calling: 6
- workflow-automation: 5
- data-privacy-and-security: 4
- multi-agent-systems: 4
- software-architecture: 4

## Proposed new skills (all runs)

- Triton: 5
- Datadog: 3
- FusionAuth: 3
- Mastra: 3
- Retool: 3
- Svelte: 3
- Vercel AI SDK: 3
- ASIC: 2
- CUDA Graphs: 2
- CuTe DSL: 2
- FPGA: 2
- Pallas: 2
- XLA: 2
- AWS CDK: 2
- Apache Beam: 2
