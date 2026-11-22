# Eval 20261122T152055Z_heldout_x2-209e1f3c7d

- split: `heldout`, goldens: 60, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-209e1f3c7d`, taxonomy v13, output cap 4096

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.957 | 0.953 | 0.961 |
| recall | 0.901 | 0.898 | 0.904 |
| f1 | 0.928 | 0.925 | 0.932 |
| requirement_accuracy | 0.980 | 0.978 | 0.981 |
| seniority_accuracy | 0.900 | 0.900 | 0.900 |
| german_accuracy | 0.967 | 0.967 | 0.967 |
| degree_accuracy | 0.900 | 0.900 | 0.900 |
| production_accuracy | 1.000 | 1.000 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.998 | 0.996 | 0.999 |
| group_f1 | 0.830 | 0.822 | 0.844 |
| rank_spearman | 0.924 | 0.916 | 0.931 |
| top10_overlap | 0.700 | 0.700 | 0.700 |

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
| 3 | cloud | cloud |
| 4 | kubernetes | kubernetes |
| 5 | software-engineering | agents |
| 6 | agents | ci-cd |
| 7 | rag | rag |
| 8 | ai-ml | apis |
| 9 | ci-cd | azure |
| 10 | ai-deployment | aws |

## Most-missed skills (all runs)

- ai-deployment: 36
- software-engineering: 35
- ai-ml: 32
- cybersecurity: 16
- cloud: 11
- backend-development: 10
- software-architecture: 9
- data-privacy-and-security: 9
- testing: 8
- observability: 7
- model-serving: 7
- evaluation: 7
- workflow-automation: 6
- apis: 6
- inference-optimization: 5

## Most-frequent extras (all runs)

- context-engineering: 9
- access-control: 9
- agents: 6
- serverless: 6
- structured-data-extraction: 6
- mlops: 5
- ml-engineering: 5
- apis: 4
- ai-developer-tooling: 3
- llms: 3
- networking: 3
- llmops: 3
- statistics: 3
- backend-development: 3
- ai-infrastructure: 3

## Proposed new skills (all runs)

- Appium: 3
- Cypress: 3
- Robot Framework: 3
- Selenium: 3
- PowerShell: 3
- DSPy: 3
- Text2SQL: 3
- DVC: 2
- OpenVINO: 2
- TFLite: 2
- Low-Code/No-Code Platforms: 2
- AWS CloudWatch: 1
- FinOps: 1
- OpenSearch: 1
- SAP: 1
