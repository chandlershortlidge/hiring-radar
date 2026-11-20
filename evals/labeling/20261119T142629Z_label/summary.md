# Labeling run 20261119T142629Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v11
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.922, recall 0.973, F1 0.947 (tp 142, B-only 12, A-only 4)
- requirement, on ids both gave: 0.993
- seniority: 0.933 (14/15)
- german: 1.000 (15/15)
- degree: 1.000 (15/15)

## Merge

- accepted on agreement: 105 skills, 38 attributes
- review queue: 18 disagreement, 15 in-scope, 80 spot-check, 42 uncertain
- spot-check: 80 of 143 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_095 seniority: A 'Proven experience building scalable test automation' vs B 'Proven experience building scalable test automation, or productivity tools.'
- golden_097 degree: A 'MS or PhD in Computer Science, AI, Mathematics, or a related field' vs B 'MS or PhD in Computer Science, AI, Mathematics, or a related field.'
- golden_100 degree: A "A bachelor's or above degree in computer science, software engineering, or a related field" vs B "A bachelor's or above degree in computer science, software engineering, or a related field."
- golden_102 seniority: A '5+ years of production Python and SQL experience' vs B '5+ years of production Python and SQL experience.'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI model governance, AI model governance / lineage tracking, AI tools for testing efficiency, AUC, AWS Athena, AWS Glue, AWS Lake Formation, Access control, Action recognition, Agent Development Kit (internal equivalent), Alerting, Apache Iceberg, Apache Iceberg / lakehouse technologies, Automated control systems, Automated retaining schedules, BLEURT, Behavioral signals, Big data techniques, C, CMMS integration, Citation checks, Continuous training, Cost management, Cross-lingual dialogue modeling, Cross-modal retrieval, Cube semantic layer, Data engineering, Data infrastructure, Data management, Data mining, Data normalization, Data quality testing, Data/concept drift detection, Datadog, Debugging and troubleshooting, Design reviews, Device fingerprinting, ERP integration, ERP/CMMS/WMS/PLC integration, Encryption, End-to-end ML pipelines, Entity resolution, Evaluation dataset creation, Graph/entity data, Historian integration, Human-in-the-loop, Human-in-the-loop systems, Human-in-the-loop workflows, Identity verification, Image segmentation, IoT / sensor data, Large-scale data processing, Latency optimization, Lineage tracking, Machine translation, Matlab, Multi-tenancy, Multimodal AI pipelines, Multimodal classification, Multimodal large models, Multimodal model development and optimization, Network intelligence, OPC-UA, Object detection, On-call incident triage, Ontology, Ontology design, Open-source contribution, PLC integration, Precision/Recall, Producibility, Production operations, Productivity tool development, Quality dashboard development, ROUGE, RTSP, React Native, Real-time risk evaluation, Relational databases, Root-cause analysis, Schema mapping, Service-level objective definition, Site reliability engineering, Structured context systems, Structured outputs, Technical documentation, Temporal alignment, Training software optimization, Trajectory Exact Match, Trino, VPN/proxy detection, Video question answering, WMS integration, Web-search grounding, Working with large-scale datasets, alerting workflows, cost management, latency optimization, multi-tenancy, mypy, pytest, ruff, time-series databases

Third labeller (HIR-379) read the labelling inputs of commit cc2ea69 - skill list v11, guide before the 19 Nov degree rule - the same question A and B were asked. Degree items were left for a person in the proposer, judge and third-labeller steps.
