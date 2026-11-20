# Eval 20261120T070628Z_dev_x2-6644e02806

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-haiku-5-5`, extractor: `x2-6644e02806`, taxonomy v12, output cap 8192, prompt trial `hir-368-round-3.md`

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.941 | 0.935 | 0.951 |
| recall | 0.913 | 0.910 | 0.919 |
| f1 | 0.927 | 0.923 | 0.935 |
| requirement_accuracy | 0.944 | 0.943 | 0.946 |
| seniority_accuracy | 0.958 | 0.944 | 0.972 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.981 | 0.972 | 0.986 |
| production_accuracy | 0.900 | 0.900 | 0.900 |
| production_signal_agreement | 0.921 | 0.875 | 1.000 |
| grounding_accuracy | 0.999 | 0.997 | 1.000 |
| group_f1 | 0.857 | 0.830 | 0.874 |
| rank_spearman | 0.956 | 0.949 | 0.965 |
| top10_overlap | 0.900 | 0.900 | 0.900 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 0.875 | 0.875 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 0.909 | 0.909 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 7 | 0 | 1 |
| nice_to_have | 0 | 1 | 0 |
| none | 1 | 0 | 10 |

Signal agreement where the class was right: 0.875 over 8 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | software-engineering | agents |
| 4 | agents | rag |
| 5 | evaluation | cloud |
| 6 | cloud | evaluation |
| 7 | rag | ci-cd |
| 8 | machine-learning | machine-learning |
| 9 | aws | aws |
| 10 | ai-ml | software-engineering |

## Most-missed skills (all runs)

- software-engineering: 44
- ai-deployment: 39
- ai-ml: 26
- apis: 12
- software-architecture: 10
- model-development: 10
- ml-engineering: 9
- cloud: 8
- evaluation: 6
- data-science: 6
- agents: 6
- machine-learning: 5
- backend-development: 5
- frontend-development: 5
- data-engineering: 5

## Most-frequent extras (all runs)

- testing: 15
- observability: 10
- data-engineering: 10
- ai-ml: 10
- data-pipelines: 8
- data-privacy-and-security: 7
- ai-deployment: 7
- software-engineering: 6
- llm-orchestration: 6
- tool-calling: 6
- context-engineering: 6
- cloud: 6
- access-control: 5
- ci-cd: 5
- software-architecture: 5

## Proposed new skills (all runs)

- Looker: 6
- Dataflow: 6
- Design Patterns: 6
- Pub/Sub: 6
- Triton: 5
- SAFe: 5
- JSON: 4
- Voicebots: 4
- Scrum: 4
- Data Mining: 3
- ASIC: 3
- CUDA Graphs: 3
- CuTe DSL: 3
- FPGA: 3
- Pallas: 3
