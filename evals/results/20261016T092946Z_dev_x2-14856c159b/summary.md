# Eval 20261016T092946Z_dev_x2-14856c159b

- split: `dev`, goldens: 20, repeats: 3
- model: `claude-sonnet-5-5`, extractor: `x2-14856c159b`, taxonomy v2

| metric | mean | min | max |
|---|---|---|---|
| precision | 0.901 | 0.888 | 0.908 |
| recall | 0.973 | 0.970 | 0.976 |
| f1 | 0.936 | 0.927 | 0.941 |
| requirement_accuracy | 0.944 | 0.942 | 0.945 |
| rank_spearman | 0.914 | 0.913 | 0.916 |
| top10_overlap | 0.833 | 0.800 | 0.900 |

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
| 10 | ci-cd | prompt-engineering |

## Most-missed skills (all runs)

- software-engineering: 7
- apis: 6
- ai-deployment: 4
- prompt-engineering: 3
- ml-engineering: 3
- recommender-systems: 2
- persistence: 1
- llms: 1

## Most-frequent extras (all runs)

- testing: 12
- software-engineering: 6
- data-pipelines: 6
- tool-calling: 6
- data-privacy-and-security: 5
- observability: 4
- jupyter-notebooks: 3
- aws-s3: 3
- llm-orchestration: 3
- vector-search: 3
- ai-deployment: 3
- api-design: 3
- autogen: 3
- chain-of-thought: 3
- crewai: 3

## Proposed new skills (all runs)

- AWS ECS: 1
- AWS Lambda: 1
