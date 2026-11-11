# Eval 20261111T093831Z_dev_x2-7873e921da

- split: `dev`, goldens: 35, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-7873e921da`, taxonomy v10

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.910 | 0.907 | 0.911 |
| recall | 0.934 | 0.934 | 0.934 |
| f1 | 0.922 | 0.920 | 0.923 |
| requirement_accuracy | 0.948 | 0.948 | 0.948 |
| seniority_accuracy | 1.000 | 1.000 | 1.000 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.971 | 0.971 | 0.971 |
| production_accuracy | 0.950 | 0.950 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 1.000 | 1.000 | 1.000 |
| rank_spearman | 0.944 | 0.938 | 0.947 |
| top10_overlap | 0.800 | 0.800 | 0.800 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 1.000 | 1.000 |
| nice_to_have | 1 | — | 0.000 |
| none | 11 | 0.917 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 0 | 1 |
| none | 0 | 0 | 11 |

Signal agreement where the class was right: 1.000 over 8 Goldens.

Errors in run 1: 0

## Top 10 skills, run 1

| # | gold | predicted |
|---|---|---|
| 1 | llms | llms |
| 2 | python | python |
| 3 | rag | rag |
| 4 | agents | agents |
| 5 | software-engineering | ci-cd |
| 6 | cloud | evaluation |
| 7 | evaluation | aws |
| 8 | aws | cloud |
| 9 | ci-cd | gcp |
| 10 | apis | observability |

## Most-missed skills (all runs)

- ai-deployment: 24
- software-engineering: 21
- ai-ml: 15
- apis: 12
- model-development: 6
- frontend-development: 6
- evaluation: 5
- cloud: 4
- prompt-engineering: 3
- ml-engineering: 3
- agents: 3
- model-serving: 3
- workflow-automation: 3
- model-versioning: 2
- devops: 2

## Most-frequent extras (all runs)

- testing: 15
- data-pipelines: 9
- mcp: 6
- observability: 6
- fine-tuning: 6
- tool-calling: 6
- git: 6
- streamlit: 6
- software-engineering: 5
- data-privacy-and-security: 5
- software-architecture: 5
- machine-learning: 4
- llm-guardrails: 4
- ci-cd: 4
- jupyter-notebooks: 3

## Proposed new skills (all runs)

- Datadog: 2
- Mastra: 2
- NestJS: 2
- Svelte: 2
- Vercel AI SDK: 1
- Azure AI Foundry: 1
- Django: 1
- Apache Beam: 1
