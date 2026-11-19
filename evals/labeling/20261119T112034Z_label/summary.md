# Labeling run 20261119T112034Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v11
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.888, recall 0.946, F1 0.916 (tp 158, B-only 20, A-only 9)
- requirement, on ids both gave: 0.994
- seniority: 0.733 (11/15)
- german: 1.000 (15/15)
- degree: 1.000 (15/15)

## Merge

- accepted on agreement: 124 skills, 40 attributes
- review queue: 32 disagreement, 15 in-scope, 1 mapping, 80 spot-check, 34 uncertain
- spot-check: 80 of 164 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_099 degree: A 'PhD / Master in a relevant field (Computer Science, Statistics, Machine Learning)' vs B 'PhD / Master in a relevant field (Computer Science, Statistics, Machine Learning) — exceptional candidates from other backgrounds welcome.'
- golden_101 seniority: A 'Applied Scientist Lead' vs B 'Lead / Staff Applied Scientist'
- golden_101 degree: A 'PhD / Master in a relevant field (Robotics, Machine Learning)' vs B 'PhD / Master in a relevant field (Robotics, Machine Learning) — exceptional candidates from other backgrounds welcome.'
- golden_106 degree: A 'MSc or PhD in a numerate discipline' vs B 'MSc or PhD in a numerate discipline.'
- golden_108 degree: A 'Masters Degree in computer science, engineering, mathematics, business engineering, business information or related fields , or equivalent work experience preferred' vs B 'Masters Degree in computer science, engineering, mathematics, business engineering, business information or related fields , or equivalent work experience preferred.'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI auditability, AI governance, Agent harnesses, Agentic patterns, Android app shipping, Android architecture, Android development, App performance optimization, Attention mechanisms (Multi-Head / Grouped-Query Attention), Audio / music content understanding, Auditability, Azure AI, Building and operating high-load, low-latency systems, Capture-the-flag participation, Classification, Clean, readable coding, Cloud architecture, Cloud reference architectures, Cluster management and configuration, Code typing, Competitive programming, Compliance, Compute resource allocation and optimization, Container image optimization, Container registries, Container registries / image optimization / multi-stage builds, Coroutines, DBMS internals, Data engineering, Data governance, Data integration, Debugging, Decisioning, Engineering experience, Experiment design, Experimentation infrastructure, Fault-tolerant programming, Flow, GPU cluster management, Gradient boosting, HPC / parallel computing, Hardware-level optimisation, High-load, low-latency systems, High-performance computing, High-performance programming, Hive, Human-in-the-loop, Human-in-the-loop product experiences, Identity and access management, Infrastructure automation, Isaac SIM, Isaac Sim, Jetpack, Job scheduling, Kaggle / data science competitions, Kotlin Coroutines, Kotlin Flow, Kubernetes custom resource definitions, Kubernetes operators and custom controllers, LLM post-training, Large-scale robot data collection, Linear/nonlinear optimization, Long-horizon task execution, Low-level performance tuning, Low-level performance tuning / hardware-level optimisation, ML frameworks, ML libraries, ML lifecycle, ML/AI libraries, Model lifecycle management, Multi-Head Attention, Multi-stage container builds, Multi/Grouped-Query attention, Native Android development, Parallel computing, Personalisation, Platform Engineering, Platform engineering, Production change rollback, Production debugging, Production incident debugging, Production software deployment, Proof-of-Value execution, ROI/TCO modeling, Ranking, Ranking systems, Redshift, Responsible AI practices, Responsible AI principles, Responsible AI/ML, Retrieval, Robot perception, navigation and manipulation, Robotic manipulation, Robotic navigation, Robotic perception, Robotics simulation tools, SRE, Scalable inference infrastructure, Search and retrieval, Sim-to-real transfer, Simulation tools, Site reliability engineering, Slurm multi-cluster federation, Storage management, Supporting training jobs and highly available inference services, Systems programming, Systems-level performance analysis, TabPFN, TabPFN / tabular foundation models, Table question answering, Tabular foundation models, Text-to-SQL, Typing (type annotations), Vision Language Models, Vision Language Models (VLM), Vision-Language-Action (VLA) models, Vision-Language-Action models, Working with large codebases, Working with messy real-world data, World models, YAML configuration management, cloud reference architectures, data engineering, data integration, debugging, gradient boosting, identity and access management, large-scale retrieval / ranking systems, linear/nonlinear optimization, long-horizon task execution, multi-step AI workflows, responsible AI / auditability / governance, search and retrieval (information retrieval), table question answering, text-to-SQL
