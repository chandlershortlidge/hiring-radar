# Eval 20261120T174218Z_heldout_x2-9b923cba1e

- split: `heldout`, goldens: 60, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-9b923cba1e`, taxonomy v12, output cap 4096, prompt trial `hir-368-round-3.md`

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.957 | 0.956 | 0.959 |
| recall | 0.889 | 0.874 | 0.912 |
| f1 | 0.922 | 0.913 | 0.934 |
| requirement_accuracy | 0.977 | 0.972 | 0.980 |
| seniority_accuracy | 0.906 | 0.900 | 0.917 |
| german_accuracy | 0.956 | 0.950 | 0.967 |
| degree_accuracy | 0.883 | 0.883 | 0.883 |
| production_accuracy | 1.000 | 1.000 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.998 | 0.998 | 0.999 |
| group_f1 | 0.830 | 0.828 | 0.835 |
| rank_spearman | 0.944 | 0.934 | 0.955 |
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

Errors in run 1: 1

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | python | python |
| 2 | llms | llms |
| 3 | cloud | cloud |
| 4 | kubernetes | agents |
| 5 | software-engineering | kubernetes |
| 6 | agents | rag |
| 7 | rag | ci-cd |
| 8 | ai-ml | machine-learning |
| 9 | ci-cd | apis |
| 10 | ai-deployment | azure |

## Most-missed skills (all runs)

- ai-deployment: 31
- software-engineering: 30
- ai-ml: 23
- cybersecurity: 14
- observability: 9
- apis: 9
- software-architecture: 9
- data-privacy-and-security: 9
- backend-development: 7
- machine-learning: 6
- testing: 5
- ci-cd: 5
- containerization: 5
- docker: 5
- kubernetes: 5

## Most-frequent extras (all runs)

- agents: 9
- context-engineering: 9
- access-control: 9
- machine-learning: 8
- mlops: 6
- apis: 6
- serverless: 6
- workflow-automation: 4
- ai-developer-tooling: 3
- llms: 3
- elasticsearch: 3
- networking: 3
- llmops: 3
- statistics: 3
- ml-engineering: 3

## Proposed new skills (all runs)

- Appium: 3
- Cypress: 3
- Robot Framework: 3
- Selenium: 3
- DVC: 3
- OpenVINO: 3
- TFLite: 3
- PowerShell: 3
- DSPy: 3
- Text2SQL: 3
- Cohere: 2
- Datadog: 2
- Supabase: 2
- SAP BTP: 1
- SAP Business AI: 1
