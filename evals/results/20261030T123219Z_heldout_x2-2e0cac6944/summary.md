# Eval 20261030T123219Z_heldout_x2-2e0cac6944

- split: `heldout`, goldens: 26, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-2e0cac6944`, taxonomy v4

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.952 | 0.948 | 0.954 |
| recall | 0.888 | 0.884 | 0.890 |
| f1 | 0.919 | 0.915 | 0.921 |
| requirement_accuracy | 0.968 | 0.967 | 0.970 |
| seniority_accuracy | 0.962 | 0.962 | 0.962 |
| german_accuracy | 0.962 | 0.962 | 0.962 |
| degree_accuracy | 0.949 | 0.923 | 0.962 |
| production_accuracy | 1.000 | 1.000 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.933 | 0.923 | 0.939 |
| top10_overlap | 0.667 | 0.600 | 0.700 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 0 | — | — |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 3 | 1.000 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 0 | 0 | 0 |
| nice_to_have | 0 | 1 | 0 |
| none | 0 | 0 | 3 |

Signal agreement where the class was right: 1.000 over 1 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | cloud | kubernetes |
| 4 | ai-deployment | cloud |
| 5 | evaluation | apis |
| 6 | kubernetes | evaluation |
| 7 | software-engineering | agents |
| 8 | ai-ml | aws |
| 9 | apis | observability |
| 10 | observability | pytorch |

## Most-missed skills (all runs)

- ai-deployment: 19
- ai-ml: 18
- software-engineering: 16
- containerization: 6
- backend-development: 5
- cloud: 5
- ai-developer-tooling: 5
- evaluation: 4
- observability: 4
- data-pipelines: 3
- cybersecurity: 3
- model-development: 3
- tool-calling: 3
- workflow-automation: 3
- agents: 3

## Most-frequent extras (all runs)

- agents: 4
- apis: 3
- structured-data-extraction: 3
- statistics: 3
- deep-learning: 3
- kubernetes: 3
- evaluation: 3
- agent-architecture: 3
- backend-development: 3
- networking: 2
- llmops: 2
- mlops: 2
- workflow-automation: 2
- microservices: 2
- llms: 2

## Proposed new skills (all runs)

- SciPy: 3
- Survival Analysis: 3
- Appium: 3
- Azure DevOps: 3
- Cypress: 3
- Jenkins: 3
- Playwright: 3
- Robot Framework: 3
- Selenium: 3
- SAP BTP: 3
- SAP Business AI: 3
- Pinecone: 3
- Redis: 3
- CUDA: 3
- KServe: 3
