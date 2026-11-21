# Eval 20261120T171942Z_dev_x2-9b923cba1e

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-9b923cba1e`, taxonomy v12, output cap 4096, prompt trial `hir-368-round-3.md`

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.903 | 0.902 | 0.904 |
| recall | 0.908 | 0.906 | 0.913 |
| f1 | 0.906 | 0.905 | 0.907 |
| requirement_accuracy | 0.955 | 0.948 | 0.960 |
| seniority_accuracy | 0.972 | 0.958 | 0.986 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.972 | 0.958 | 0.986 |
| production_accuracy | 0.917 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.998 | 0.999 |
| group_f1 | 0.703 | 0.671 | 0.729 |
| rank_spearman | 0.938 | 0.930 | 0.943 |
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
| 6 | cloud | software-engineering |
| 7 | rag | evaluation |
| 8 | machine-learning | machine-learning |
| 9 | aws | ci-cd |
| 10 | ai-ml | aws |

## Most-missed skills (all runs)

- ai-deployment: 44
- software-engineering: 38
- ai-ml: 35
- ml-engineering: 12
- apis: 11
- mlops: 10
- model-development: 9
- evaluation: 8
- software-architecture: 8
- data-science: 6
- data-privacy-and-security: 6
- cybersecurity: 5
- workflow-automation: 4
- prompt-engineering: 3
- agents: 3

## Most-frequent extras (all runs)

- observability: 16
- testing: 15
- software-engineering: 11
- data-pipelines: 11
- agents: 10
- machine-learning: 8
- software-architecture: 8
- ci-cd: 8
- llm-orchestration: 7
- cloud: 7
- git: 7
- access-control: 6
- kubernetes: 6
- mcp: 6
- ai-ml: 6

## Proposed new skills (all runs)

- Django: 3
- AWS Glue: 3
- AWS Lake Formation: 3
- Triton: 2
- AWS CDK: 2
- Mastra: 2
- Vercel AI SDK: 2
- CUDA Graphs: 1
- FPGA: 1
- Dataleap: 1
- Apache Beam: 1
- Datadog: 1
- Svelte: 1
- Optimization: 1
- Keras: 1
