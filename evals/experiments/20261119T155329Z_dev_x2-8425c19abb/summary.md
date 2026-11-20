# Eval 20261119T155329Z_dev_x2-8425c19abb

- split: `dev`, goldens: 71, repeats: 3
- model: `claude-haiku-5-5`, extractor: `x2-8425c19abb`, taxonomy v12, output cap 8192

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.956 | 0.953 | 0.960 |
| recall | 0.879 | 0.873 | 0.884 |
| f1 | 0.916 | 0.914 | 0.918 |
| requirement_accuracy | 0.942 | 0.940 | 0.945 |
| seniority_accuracy | 0.930 | 0.915 | 0.944 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.986 | 0.986 | 0.986 |
| production_accuracy | 0.883 | 0.850 | 0.900 |
| production_signal_agreement | 0.963 | 0.889 | 1.000 |
| grounding_accuracy | 0.997 | 0.994 | 1.000 |
| group_f1 | 0.848 | 0.839 | 0.864 |
| rank_spearman | 0.948 | 0.942 | 0.955 |
| top10_overlap | 0.800 | 0.800 | 0.800 |

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
| 6 | cloud | aws |
| 7 | rag | ci-cd |
| 8 | machine-learning | cloud |
| 9 | aws | machine-learning |
| 10 | ai-ml | gcp |

## Most-missed skills (all runs)

- software-engineering: 55
- ai-deployment: 40
- ai-ml: 37
- cloud: 19
- apis: 14
- machine-learning: 13
- agents: 12
- ml-engineering: 12
- llms: 12
- evaluation: 9
- model-development: 9
- software-architecture: 8
- backend-development: 8
- data-science: 7
- deep-learning: 6

## Most-frequent extras (all runs)

- testing: 14
- data-engineering: 8
- data-privacy-and-security: 7
- observability: 6
- tool-calling: 6
- context-engineering: 6
- ai-deployment: 5
- data-pipelines: 4
- ci-cd: 4
- llm-orchestration: 4
- jupyter-notebooks: 3
- software-engineering: 3
- aws-s3: 3
- serverless: 3
- chain-of-thought: 3

## Proposed new skills (all runs)

- Looker: 6
- Dataflow: 5
- Pub/Sub: 5
- Design Patterns: 5
- Triton: 4
- Data Mining: 3
- ASIC: 3
- CUDA Graphs: 3
- CuTe DSL: 3
- FPGA: 3
- Pallas: 3
- XLA: 3
- Fivetran: 3
- Hex: 3
- Hightouch: 3
