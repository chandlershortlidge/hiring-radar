# Eval 20261120T174216Z_heldout_x2-848aaff6a5

- split: `heldout`, goldens: 60, repeats: 3
- model: `claude-haiku-5-5`, extractor: `x2-848aaff6a5`, taxonomy v12, output cap 8192, prompt trial `hir-368-round-3.md`

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.974 | 0.973 | 0.975 |
| recall | 0.917 | 0.912 | 0.922 |
| f1 | 0.945 | 0.943 | 0.947 |
| requirement_accuracy | 0.981 | 0.977 | 0.985 |
| seniority_accuracy | 0.883 | 0.883 | 0.883 |
| german_accuracy | 0.967 | 0.967 | 0.967 |
| degree_accuracy | 0.872 | 0.867 | 0.883 |
| production_accuracy | 0.750 | 0.750 | 0.750 |
| production_signal_agreement | — | — | — |
| grounding_accuracy | 0.995 | 0.991 | 0.999 |
| group_f1 | 0.843 | 0.797 | 0.887 |
| rank_spearman | 0.961 | 0.957 | 0.964 |
| top10_overlap | 0.700 | 0.700 | 0.700 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 0 | — | — |
| nice_to_have | 1 | — | 0.000 |
| none | 3 | 0.750 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 0 | 0 | 0 |
| nice_to_have | 0 | 0 | 1 |
| none | 0 | 0 | 3 |

Signal agreement where the class was right: — over 0 Goldens.

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
| 8 | ai-ml | azure |
| 9 | ci-cd | machine-learning |
| 10 | ai-deployment | aws |

## Most-missed skills (all runs)

- ai-deployment: 24
- ai-ml: 23
- software-engineering: 20
- cybersecurity: 11
- cloud: 10
- testing: 8
- apis: 8
- software-architecture: 8
- backend-development: 8
- data-science: 7
- data-privacy-and-security: 6
- distributed-systems: 5
- full-stack-development: 5
- evaluation: 5
- ai-infrastructure: 4

## Most-frequent extras (all runs)

- context-engineering: 9
- access-control: 8
- mlops: 4
- serverless: 4
- machine-learning: 3
- workflow-automation: 3
- ai-developer-tooling: 2
- llms: 2
- agents: 2
- networking: 2
- github-actions: 2
- data-privacy-and-security: 2
- ml-engineering: 2
- gcp: 2
- distributed-systems: 1

## Proposed new skills (all runs)

- OpenAPI: 5
- Sandboxed code execution: 4
- Amazon EKS: 4
- Polars: 3
- SciPy: 3
- Survival Analysis: 3
- Appium: 3
- Cypress: 3
- Robot Framework: 3
- Selenium: 3
- Prototyping: 3
- SAP BTP: 3
- SAP Business AI: 3
- SAP Joule: 3
- AWS AgentCore: 3
