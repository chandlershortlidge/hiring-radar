# Eval 20261111T182024Z_dev_x2-ffafb5b8cf

- split: `dev`, goldens: 35, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-ffafb5b8cf`, taxonomy v11

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.910 | 0.908 | 0.912 |
| recall | 0.917 | 0.914 | 0.921 |
| f1 | 0.913 | 0.911 | 0.916 |
| requirement_accuracy | 0.961 | 0.960 | 0.961 |
| seniority_accuracy | 0.952 | 0.943 | 0.971 |
| german_accuracy | 1.000 | 1.000 | 1.000 |
| degree_accuracy | 0.971 | 0.971 | 0.971 |
| production_accuracy | 0.933 | 0.900 | 0.950 |
| production_signal_agreement | 1.000 | 1.000 | 1.000 |
| grounding_accuracy | 0.999 | 0.998 | 1.000 |
| group_f1 | 0.747 | 0.734 | 0.756 |
| rank_spearman | 0.927 | 0.920 | 0.932 |
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
| 5 | software-engineering | cloud |
| 6 | cloud | ci-cd |
| 7 | evaluation | evaluation |
| 8 | aws | aws |
| 9 | ci-cd | gcp |
| 10 | apis | observability |

## Most-missed skills (all runs)

- software-engineering: 25
- ai-deployment: 24
- apis: 13
- ai-ml: 13
- frontend-development: 6
- model-development: 5
- prompt-engineering: 3
- ml-engineering: 3
- recommender-systems: 3
- persistence: 3
- agents: 3
- model-serving: 3
- ray: 3
- aws: 3
- aws-bedrock: 3

## Most-frequent extras (all runs)

- testing: 14
- git: 9
- data-pipelines: 8
- software-engineering: 6
- mcp: 6
- observability: 6
- tool-calling: 6
- llm-orchestration: 5
- vector-search: 5
- chain-of-thought: 5
- software-architecture: 5
- apis: 4
- workflow-automation: 4
- jupyter-notebooks: 3
- aws-s3: 3

## Proposed new skills (all runs)

- Triton: 3
- Apache Beam: 3
- Mastra: 3
- Vercel AI SDK: 3
- Django: 3
- AWS CDK: 3
- CloudFormation: 1
- AWS CloudFormation: 1
