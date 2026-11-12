# Eval 20261111T174851Z_dev_x2-065fa54eba

- split: `dev`, goldens: 35, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-065fa54eba`, taxonomy v11

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.926 | 0.922 | 0.930 |
| recall | 0.902 | 0.894 | 0.912 |
| f1 | 0.914 | 0.912 | 0.917 |
| requirement_accuracy | 0.958 | 0.945 | 0.966 |
| seniority_accuracy | 0.971 | 0.971 | 0.971 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.971 | 0.971 | 0.971 |
| production_accuracy | 0.983 | 0.950 | 1.000 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 1.000 | 1.000 | 1.000 |
| group_f1 | 0.680 | 0.659 | 0.702 |
| rank_spearman | 0.927 | 0.923 | 0.934 |
| top10_overlap | 0.800 | 0.800 | 0.800 |

## Production experience, run 1

| class | support | precision | recall |
|---|---|---|---|
| required | 8 | 1.000 | 1.000 |
| nice_to_have | 1 | 1.000 | 1.000 |
| none | 11 | 1.000 | 1.000 |

Confusion (rows = gold, cols = predicted):

| gold \ pred | required | nice_to_have | none |
|---|---|---|---|
| required | 8 | 0 | 0 |
| nice_to_have | 0 | 1 | 0 |
| none | 0 | 0 | 11 |

Signal agreement where the class was right: 1.000 over 9 Goldens.

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

- software-engineering: 24
- ai-deployment: 24
- ai-ml: 16
- cloud: 14
- apis: 12
- frontend-development: 7
- model-development: 6
- agents: 4
- evaluation: 4
- workflow-automation: 4
- backend-development: 3
- prompt-engineering: 3
- ml-engineering: 3
- testing: 3
- cyber-ranges: 3

## Most-frequent extras (all runs)

- testing: 12
- data-pipelines: 9
- software-engineering: 6
- llm-orchestration: 6
- data-privacy-and-security: 6
- mcp: 6
- tool-calling: 6
- git: 6
- jupyter-notebooks: 3
- azure: 3
- claude-code: 3
- claude-enterprise: 3
- event-driven-systems: 3
- kubernetes: 3
- observability: 3

## Proposed new skills (all runs)

- AWS CDK: 3
- Django: 2
- Mastra: 2
- Vercel AI SDK: 2
- Apache Beam: 1
- Triton: 1
