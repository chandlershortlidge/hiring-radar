# Labeling run 20261125T135350Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-haiku-5-5`; taxonomy v14
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.931, recall 0.964, F1 0.947 (tp 161, B-only 12, A-only 6)
- requirement, on ids both gave: 0.975
- seniority: 0.933 (14/15)
- german: 1.000 (15/15)
- degree: 1.000 (15/15)

## Merge

- accepted on agreement: 116 skills, 42 attributes
- review queue: 21 disagreement, 15 in-scope, 1 mapping, 80 spot-check, 43 uncertain
- spot-check: 80 of 158 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_150 degree: A 'Abgeschlossenes fachbezogenes Hochschulstudium oder vergleichbare Qualifikation' vs B 'Abgeschlossenes fachbezogenes Hochschulstudium oder vergleichbare Qualifikation mit fundierter Berufserfahrung (min. 5 Jahre) im DevSecOps- oder Cloud-Platform-Umfeld'
- golden_156 seniority: A 'Senior Full-Stack AI Engineer' vs B 'Senior / Staff Software Engineer'
- golden_158 seniority: A 'Senior AI & RAG Engineer' vs B 'Senior AI & RAG Engineer (m/w/d)'
- golden_158 degree: A 'erfolgreich abgeschlossenes Bachelor- oder Masterstudium' vs B 'erfolgreich abgeschlossenes Bachelor- oder Masterstudium, beispielsweise in Betriebswirtschaftslehre, Wirtschaftsinformatik, Wirtschaftsingenieurwesen oder einem vergleichbaren Studiengang'
- golden_159 seniority: A 'Lead Software Engineer' vs B 'Lead Software Engineer AI Engineering'
- golden_160 seniority: A 'Sr. Staff Applied AI Engineer' vs B 'Sr. Staff Applied AI Engineer, GTM'
- golden_161 seniority: A 'Evidence of staff-level impact' vs B 'staff-level impact'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- 3D perception, AI-assisted code generation, AI-driven data interfaces, Aerospike, Agent skills (reusable skill development), Agent-to-agent (A2A) protocol/frameworks, Agent-to-agent frameworks, Agile development, Alerting workflows, Analytical databases, Analytical engine implementation and scaling, Analytical infrastructure, Anti-abuse systems, Automation tools, Batching, Billing systems, ClickHouse, Cloud-native concepts, Code review, Code-RAG, Compliance, Cost management, DETR, Data governance frameworks, Data platforms, Data quality frameworks, Debugging, Design reviews, Development workflow optimization, Edge / embedded deployment, Edge and embedded deployment, Embedded systems, Embodied and robot-learning models, Evaluation dataset creation, Failure analysis, GPU clusters, GPU computing, GPU profiling, GTM systems integration, Grounding, Harbor, HashiCorp Vault, High-scale production infrastructure, Holdout experiments, Hybrid search, IT-/OT-Infrastruktur, Imitation learning, Inference Engineering, Internet of Things, IoT, Juniper Networks M-Series, KV-cache management, LLM-as-judge, LLaVA, Large-scale data systems, Latency optimization, Logging, Logging / auditing / compliance, Memory hardware, Metadata filtering, Metering systems, Microsoft 365, Mixed precision training, Mixed-precision training, Model optimization, Model review, Multi-sensor fusion, Multi-tenancy, Multimodal learning, Multimodal modeling, Network security, Nexus, OT infrastructure, Object detection, Offline and online evaluation scoring, Open-source contribution, OpenVLA, PaliGemma, Performance optimization, Platform Engineering, Podman, Private cloud, Production systems experience, Programmable logic controllers, Prompt-injection defense, Prototyping, Query execution, Qwen-VL, RIP routing protocol, RLHF, RT-2, Rechenzentrumsstrategien, Refactoring, Release validation, Reporting dashboards, Reranking, Retrieval methods, Reusable AI skill development, Robot learning / embodied AI, SD-WAN, SRE, Scalable system development, Security auditing, Segmentation, Shell scripting, Sim-to-real transfer, Simulation, Simulation / sim-to-real, SonarQube, Source-code retrieval, Sovereign cloud, Speech AI, StarRocks, System integration, Technical documentation, Text-to-SQL, Traffic systems, Video understanding, Vision-language models, Vision-language models (VLMs), Vision-language-action models, Vision-language-action models (VLAs), Web analytics, YOLO, Zero Trust, agile development, alerting, data quality / governance frameworks, incident management, inference systems / high-scale production infrastructure, latency optimization, metering / anti-abuse / billing systems, multi-tenancy, pi0, query execution / performance optimization, text-to-SQL, time-series databases
