# Eval 20261111T073740Z_dev_x2-1462204f48

- split: `dev`, goldens: 20, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-1462204f48`, taxonomy v11

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.866 | 0.864 | 0.869 |
| recall | 0.961 | 0.958 | 0.964 |
| f1 | 0.911 | 0.910 | 0.913 |
| requirement_accuracy | 0.988 | 0.988 | 0.988 |
| seniority_accuracy | 0.933 | 0.900 | 0.950 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.950 | 0.950 | 0.950 |
| production_accuracy | 0.917 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.997 | 1.000 |
| rank_spearman | 0.887 | 0.881 | 0.895 |
| top10_overlap | 0.833 | 0.800 | 0.900 |

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
| 1 | llms | llms |
| 2 | python | python |
| 3 | rag | rag |
| 4 | agents | agents |
| 5 | evaluation | evaluation |
| 6 | apis | aws |
| 7 | aws | ci-cd |
| 8 | cloud | cloud |
| 9 | prompt-engineering | langchain |
| 10 | ci-cd | testing |

## Most-missed skills (all runs)

- software-engineering: 9
- apis: 7
- ai-deployment: 6
- evaluation: 3
- prompt-engineering: 3
- ml-engineering: 3
- agent-architecture: 3
- persistence: 3
- ai-ml: 1
- llms: 1

## Most-frequent extras (all runs)

- testing: 12
- data-pipelines: 8
- machine-learning: 6
- software-engineering: 6
- observability: 6
- fine-tuning: 6
- tool-calling: 6
- llm-guardrails: 5
- software-architecture: 5
- jupyter-notebooks: 3
- aws-s3: 3
- llm-orchestration: 3
- serverless: 3
- azure: 3
- claude-code: 3

## Proposed new skills (all runs)

