# Labeling run 20261119T114422Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v11
- postings picked 13, labeled by both 13, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.926, recall 0.978, F1 0.951 (tp 176, B-only 14, A-only 4)
- requirement, on ids both gave: 0.994
- seniority: 1.000 (13/13)
- german: 1.000 (13/13)
- degree: 1.000 (13/13)

## Merge

- accepted on agreement: 133 skills, 37 attributes
- review queue: 19 disagreement, 13 in-scope, 80 spot-check, 44 uncertain
- spot-check: 80 of 170 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_094 degree: A 'A PhD or equivalent industry research experience' vs B 'A PhD or equivalent industry research experience in machine learning, computer science, statistics or a related field.'
- golden_095 degree: A '(MSc or PhD)' vs B 'To have a background in a highly quantitative field, with a focus on AI (MSc or PhD)'
- golden_097 seniority: A '3+ years of professional software engineering experience' vs B '3+ years of professional software engineering experience.'
- golden_106 degree: A 'A PhD or equivalent industry research experience in machine learning, computer science, statistics or a related field' vs B 'A PhD or equivalent industry research experience in machine learning, computer science, statistics or a related field.'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- A2A, A2A (Agent2Agent protocol), Accelerate, Agent harnesses, Agent loops, Agent training environments, Algorithms, Amazon EKS, Availability, reliability and scalability practices, Axolotl, B300, BF16, Bandits, Code review, Content classification, Continual learning, Continued pre-training, DPO, Data deduplication, Data filtering, Data integration, Data mixture design, Data mixture research, Debugging, Decision-model training, Declarative reconcile-based systems, Developer productivity tooling, Distributed training failure debugging, Distributed-training debugging, Domain adaptation, Encoder models, Entity representations, Event sourcing, Experimental design, FP16, FP8, FinOps, Firecracker, Fraud detection, GPU architectures, GRPO, Generative retrieval, Gradient checkpointing, H100, H200, Integration template development, Kubernetes controllers, Kubernetes controllers/operators, Kubernetes operators, Language-model post-training, Large-scale training dataset preparation, Large-scale training-data preparation, Learning rate schedule tuning, Machine learning on tabular or behavioural data, Memory and GPU optimisation, Memory optimization, Mid-training, Mixed precision training, Model compression, Model pruning, Model routing, Multi-model routing, Multi-node job orchestration, Multi-node training job orchestration, Multimodal models, NeMo RL, Online experimentation, Open-source contribution, OpenRLHF, Operating systems, Operational automation, Post-training, Pre-training, Probability theory, Programming and scripting languages, Pruning, RLHF, Recommendation metrics, Reward modelling, Role-based access control, Running inference workloads at scale, Running inference/evaluation workloads at scale, SDK development, Sandboxing / isolation, Sandboxing and isolation, Scaling laws, Semantic IDs, Setup troubleshooting, Site Reliability Engineering (SRE), Site reliability engineering, Storage subsystems, Synthetic data, Synthetic data generation, Synthetic-data generation pipelines, TabICL, TabPFN, Tabular foundation models, Terminal / command line, Terminal usage, Tokenisation, Training data quality assessment, Training dataset preparation, Training dataset preparation (filtering, deduplication, data mixture design), Training dynamics and stability, Training loss instability debugging, Training throughput optimisation, Training throughput optimization, Training-data deduplication, Training-data filtering, Training-data quality assessment, Usage metering, User behaviour modelling, ZeRO, ZeRO optimization, agent training environments, code review, continual learning, continued pre-training / mid-training, data mixture research, entity representations, gVisor, generative retrieval, language-model post-training, memory optimization (gradient checkpointing, mixed precision, ZeRO), model compression, offline RL and bandits, online experiments, operating systems, pre-training / continued pre-training, programming/scripting languages (unspecified), reward modelling, scaling laws, semantic IDs, storage subsystems, synthetic data, synthetic data generation, tabular foundation models, tokenisation, training data preparation (filtering, deduplication, data mixture), user behaviour modelling, verl
