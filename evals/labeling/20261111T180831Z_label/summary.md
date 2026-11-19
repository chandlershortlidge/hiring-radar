# Labeling run 20261111T180831Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v11
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.905, recall 0.968, F1 0.936 (tp 153, B-only 16, A-only 5)
- requirement, on ids both gave: 0.993
- seniority: 1.000 (15/15)
- german: 1.000 (15/15)
- degree: 0.933 (14/15)

## Merge

- accepted on agreement: 123 skills, 36 attributes
- review queue: 23 disagreement, 15 in-scope, 80 spot-check, 37 uncertain
- spot-check: 80 of 159 accepted labels, seed 1

Agreed value, different quoted signal (A's kept):
- golden_079 degree: A 'A relevant advanced degree (Masters or PhD)' vs B 'A relevant advanced degree (Masters or PhD) in Machine Learning, Artificial Intelligence, Statistics, or a related field'
- golden_081 seniority: A 'Senior Machine Learning Engineer' vs B 'Senior Machine Learning Engineer, Drive'
- golden_084 seniority: A '4+ years of software engineering, machine learning, or applied AI experience' vs B '4+ years of software engineering, machine learning, or applied AI experience.'
- golden_089 seniority: A 'Lead Data Scientist' vs B 'Lead Data Scientist, Credit Risk'
- golden_090 seniority: A 'Senior Data Scientist' vs B 'Senior Data Scientist - Embedded Insights'
- golden_090 degree: A 'Bachelor’s degree or equivalent work experience' vs B 'Bachelor’s degree or equivalent work experience in Computer Science, Statistics, Engineering, Economics, or a closely related field.'
- golden_092 degree: A "Expect to complete a bachelor's or master's degree in Computer Science, Engineering, or a related technical field in Spring 2027" vs B "Expect to complete a bachelor's or master's degree in Computer Science, Engineering, or a related technical field in Spring 2027."
- golden_093 degree: A 'degree in Computer Science or a related field, or have equivalent practical experience' vs B 'a degree in Computer Science or a related field, or have equivalent practical experience'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI alignment, AI indexing, AI red-teaming, AI workflow development, Abaqus, Access control, Agent planning, Agent reasoning, Ansys, Automation, Autoscaling, Bug bounties, CAD tools, CAE tools, CAE/CAD/PLM tools, COMSOL, CPU/GPU performance profiling, CTFs, Capture-the-flag security exercises, ChatGPT, Classification, Claude, Clustering, Concurrency, Customer intelligence systems, Data flows, Debugging across distributed hosts, Debugging distributed production problems, Decision-making methods, Developer platform engineering, Developer tools, Distributed data processing, Document processing, Engagement modeling, Enterprise AI integration, Estimation, Experiment design, Experimental design, Exploratory data analysis, Failure handling, Feature stores, Feed ranking, Foundation models, Gradient-boosted models, IAM, Identity, Inference runtimes, Interpretability, Isolation, Kubernetes deployment, Large-scale ranking and training infrastructure, Lifecycle modeling, Looker, Mesh data, Microsoft Excel, Model calibration, Model optimization, Multi-stage retrieval and ranking, Multimodal AI, Multimodal AI (appetite only, nice_to_have), NX, Offline and online metrics, Online experimentation, Online feature retrieval, Open-source integration, Operational analysis, Optimization, Optimization / Operations Research, PLM tools, Performance trade-offs, Personalization, Personalization systems, Physics-informed ML, Platform engineering, Prediction, Prisma, Production debugging, Production rollout, Programming language proficiency (no language specified), Prototyping, Ranking, Ranking systems, Resource management, Retrieval, Retrieval systems, Sandboxed / virtualized code execution, Sandboxed or virtualized code execution, Scorecards, Semantic search, Siemens NX, Small language models, Software supply chain security, SolidWorks, Structured knowledge representations, Supabase, Swap-set analysis, Systems programming language, Technical design, Technical enablement, Technical statement-of-work writing, Time series data, Timeouts, Trigger.dev, Typesense, User understanding, Vintage analysis, Vision-Language Models, classification, clustering, data flows, data mining, debugging production systems, exploratory data analysis, inference runtimes, model optimization, multimodal AI, online feature retrieval, optimization, personalization, platform engineering, quantitative analysis, security considerations, small language models, software supply chain security

## Spot-check error rate (after review)

- 6 errors in 80 reviewed labels = 0.075
- 95% Wilson interval: 0.035 to 0.154

Wrong labels found:
- golden_079 attribute `degree` -> {"degree": "master", "degree_requirement": "nice_to_have", "degree_or_equivalent": false, "degree_signal": "A relevant advanced degree (Masters or PhD)"}
- golden_079 skill `github-copilot` -> {"requirement": "nice_to_have", "raw_text": "GitHub Copilot"}
- golden_081 skill `cursor` -> {"requirement": "nice_to_have", "raw_text": "Cursor"}
- golden_084 skill `mcp` -> {"requirement": "nice_to_have", "raw_text": "MCP"}
- golden_091 skill `jax` -> {"requirement": "nice_to_have", "raw_text": "JAX"}
- golden_091 skill `tensorflow` -> {"requirement": "nice_to_have", "raw_text": "TensorFlow"}
