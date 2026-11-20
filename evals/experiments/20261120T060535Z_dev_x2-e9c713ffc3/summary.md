# Eval 20261120T060535Z_dev_x2-e9c713ffc3

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-haiku-5-5`, extractor: `x2-e9c713ffc3`, taxonomy v12, output cap 8192, prompt trial `hir-368-broad-skills.md`

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.937 | 0.935 | 0.941 |
| recall | 0.912 | 0.903 | 0.919 |
| f1 | 0.924 | 0.919 | 0.927 |
| requirement_accuracy | 0.945 | 0.943 | 0.947 |
| seniority_accuracy | 0.915 | 0.915 | 0.915 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.981 | 0.958 | 1.000 |
| production_accuracy | 0.850 | 0.850 | 0.850 |
| production_signal_agreement | 0.963 | 0.889 | 1.000 |
| grounding_accuracy | 0.995 | 0.992 | 0.998 |
| group_f1 | 0.823 | 0.727 | 0.874 |
| rank_spearman | 0.957 | 0.952 | 0.963 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 0.727 | 1.000 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 1.000 | 0.727 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 1 | 0 |
| none | 3 | 0 | 8 |

Signal agreement where the class was right: 0.889 over 9 Goldens.

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
| 8 | machine-learning | ci-cd |
| 9 | aws | aws |
| 10 | ai-ml | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 44
- ai-deployment: 37
- ai-ml: 25
- apis: 12
- ml-engineering: 10
- software-architecture: 10
- cloud: 9
- agents: 8
- model-development: 8
- evaluation: 6
- data-science: 6
- backend-development: 6
- frontend-development: 6
- machine-learning: 5
- mlops: 5

## Most-frequent extras (all runs)

- testing: 15
- observability: 12
- ai-ml: 10
- data-engineering: 9
- data-pipelines: 8
- data-privacy-and-security: 7
- ai-deployment: 7
- cloud: 7
- llm-orchestration: 6
- access-control: 6
- tool-calling: 6
- context-engineering: 6
- software-architecture: 5
- ci-cd: 5
- software-engineering: 4

## Proposed new skills (all runs)

- Looker: 6
- Triton: 5
- Dataflow: 5
- Design Patterns: 5
- Pub/Sub: 5
- JSON: 4
- SAFe: 4
- Scrum: 4
- ASIC: 3
- CUDA Graphs: 3
- CuTe DSL: 3
- FPGA: 3
- Pallas: 3
- XLA: 3
- Information Retrieval: 3
