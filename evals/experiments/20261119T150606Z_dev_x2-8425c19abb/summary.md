# Eval 20261119T150606Z_dev_x2-8425c19abb

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-haiku-5-5`, extractor: `x2-8425c19abb`, taxonomy v12

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.957 | 0.949 | 0.963 |
| recall | 0.627 | 0.592 | 0.650 |
| f1 | 0.757 | 0.729 | 0.776 |
| requirement_accuracy | 0.939 | 0.926 | 0.945 |
| seniority_accuracy | 0.826 | 0.817 | 0.831 |
| german_accuracy | 0.930 | 0.915 | 0.944 |
| degree_accuracy | 0.915 | 0.901 | 0.944 |
| production_accuracy | 0.867 | 0.850 | 0.900 |
| production_signal_agreement | 0.915 | 0.857 | 1.000 |
| grounding_accuracy | 0.996 | 0.987 | 1.000 |
| group_f1 | 0.849 | 0.811 | 0.917 |
| rank_spearman | 0.888 | 0.885 | 0.890 |
| top10_overlap | 0.833 | 0.800 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 0.800 | 1.000 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 1.000 | 0.818 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 1 | 0 |
| none | 2 | 0 | 9 |

Signal agreement where the class was right: 0.889 over 9 Goldens.

Errors in run 1: 11

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | rag |
| 4 | agents | agents |
| 5 | evaluation | evaluation |
| 6 | cloud | machine-learning |
| 7 | rag | ci-cd |
| 8 | machine-learning | sql |
| 9 | aws | software-engineering |
| 10 | ai-ml | aws |

## Most-missed skills (all runs)

- software-engineering: 59
- ai-deployment: 43
- cloud: 39
- llms: 39
- ai-ml: 39
- agents: 35
- evaluation: 33
- python: 30
- apis: 29
- observability: 23
- rag: 22
- machine-learning: 21
- aws: 20
- prompt-engineering: 18
- testing: 18

## Most-frequent extras (all runs)

- testing: 13
- data-privacy-and-security: 6
- data-engineering: 6
- data-pipelines: 5
- context-engineering: 4
- ai-deployment: 4
- observability: 4
- ai-developer-tooling: 3
- agent-state-management: 3
- tool-calling: 3
- llm-orchestration: 3
- access-control: 3
- azure-ai-foundry: 3
- machine-learning: 3
- jupyter-notebooks: 2

## Proposed new skills (all runs)

- Looker: 5
- Triton: 4
- JSON: 4
- Data Mining: 3
- ASIC: 3
- CUDA Graphs: 3
- CuTe DSL: 3
- FPGA: 3
- Pallas: 3
- XLA: 3
- Hex: 3
- Omni: 3
- Sigma: 3
- Cluster Computing: 3
- Graph Neural Networks: 3
