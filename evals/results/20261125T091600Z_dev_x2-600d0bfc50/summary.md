# Eval 20261125T091600Z_dev_x2-600d0bfc50

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-haiku-5-5`, extractor: `x2-600d0bfc50`, taxonomy v14, output cap 8192

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.940 | 0.937 | 0.944 |
| recall | 0.917 | 0.914 | 0.922 |
| f1 | 0.928 | 0.926 | 0.929 |
| requirement_accuracy | 0.948 | 0.944 | 0.951 |
| seniority_accuracy | 0.939 | 0.930 | 0.958 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.981 | 0.972 | 0.986 |
| production_accuracy | 0.883 | 0.850 | 0.950 |
| production_signal_agreement | 0.958 | 0.875 | 1.000 |
| grounding_accuracy | 0.999 | 0.997 | 1.000 |
| group_f1 | 0.817 | 0.735 | 0.869 |
| rank_spearman | 0.959 | 0.953 | 0.964 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 0.778 | 0.875 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 0.900 | 0.818 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 7 | 0 | 1 |
| nice_to_have | 0 | 1 | 0 |
| none | 2 | 0 | 9 |

Signal agreement where the class was right: 1.000 over 8 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | agents |
| 4 | agents | cloud |
| 5 | evaluation | software-engineering |
| 6 | cloud | evaluation |
| 7 | rag | rag |
| 8 | machine-learning | machine-learning |
| 9 | aws | ci-cd |
| 10 | ai-ml | aws |

## Most-missed skills (all runs)

- ai-deployment: 39
- software-engineering: 37
- ai-ml: 30
- apis: 11
- ml-engineering: 8
- data-science: 7
- agents: 7
- software-architecture: 7
- data-privacy-and-security: 7
- model-development: 7
- evaluation: 6
- backend-development: 6
- cloud: 6
- machine-learning: 5
- data-engineering: 5

## Most-frequent extras (all runs)

- testing: 14
- observability: 12
- software-engineering: 9
- data-pipelines: 9
- data-engineering: 8
- ai-deployment: 7
- data-privacy-and-security: 6
- tool-calling: 6
- cloud: 6
- context-engineering: 6
- access-control: 5
- software-architecture: 5
- llm-orchestration: 4
- vector-search: 4
- ci-cd: 4

## Proposed new skills (all runs)

- Design Patterns: 6
- Information Retrieval: 5
- Looker: 5
- SAFe: 5
- Scrum: 5
- Dataflow: 5
- Pub/Sub: 5
- Triton: 4
- JSON: 4
- Data Mining: 3
- ASIC: 3
- CUDA Graphs: 3
- CuTe DSL: 3
- FPGA: 3
- Pallas: 3
