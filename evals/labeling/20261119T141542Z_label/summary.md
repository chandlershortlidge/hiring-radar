# Labeling run 20261119T141542Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v11
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.944, recall 0.965, F1 0.954 (tp 167, B-only 10, A-only 6)
- requirement, on ids both gave: 0.910
- seniority: 1.000 (15/15)
- german: 1.000 (15/15)
- degree: 1.000 (15/15)

## Merge

- accepted on agreement: 118 skills, 41 attributes
- review queue: 31 disagreement, 15 in-scope, 80 spot-check, 38 uncertain
- spot-check: 80 of 159 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_101 seniority: A '7+ years in DevOps' vs B '7+ years in DevOps, platform engineering, cloud engineering, site reliability engineering, software engineering, or a related discipline.'
- golden_101 degree: A "Bachelor's degree in Computer Science, Engineering, Information Technology, or a related discipline, or equivalent practical experience" vs B "Bachelor's degree in Computer Science, Engineering, Information Technology, or a related discipline, or equivalent practical experience."
- golden_108 seniority: A 'senior-to-architect-level engineers' vs B 'Senior/architect-level'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- 3D perception, AI content controls, AI engineering, AI platforms, AI red-team support, AI safety testing, AWS CloudFormation, AWS Glue, AWS IAM, Agent versioning, AgentOps, Agile, Agile methodologies, Amazon Athena, Amazon Quick Suite, Apache Iceberg, Application Insights, Artifact management, Atlan, Atlan data catalog, Audit evidence, Azure AI services, Azure API Management, Azure Boards, Azure Kubernetes Service, Azure Machine Learning, Azure Monitor, Azure OpenAI, Bicep, Big Data tools, CSS, Capacity monitoring, Change and release management, Cloud security, governance, and compliance standards, Cloud-native templating, Code review, Configuration management, Configuration versioning, Configuration-as-code, Cost monitoring, DAX, DETR, Data analysis, Data engineering, Data governance framework design, Data governance frameworks, Data integration, Database management, Databases, Datadog, Dynatrace, Edge / embedded deployment, Edge and embedded deployment, Embedded systems, Embodied and robot-learning models, Encryption, Failure analysis, Feature stores, GPU computing, GPU profiling, GenAIOps, Google Docs, Google Docs automation (preferred), Google Workspace, Google Workspace (preferred), Governed metadata, Grounding, HTML5, IDEs, IT service request management, Identity and access controls, Imitation learning, Incident response, Internet of Things, JSON, JSON/YAML, Jira, Juniper Networks M-Series, LLaVA, LLaVA / Qwen-VL / PaliGemma, ML project lifecycle, Machine tool, Master data management, Memory hardware, Metadata governance, Microsoft Office, Microsoft Office (preferred), Mixed precision training, Mixed-precision training, Model and endpoint lifecycle management, Model management, Model optimization, Model review, Model tuning, Multi-sensor fusion, Multimodal learning, Multimodal modeling, OWL, Object detection, Object detection and segmentation, Ontology development, Ontology development and management, Open-source development, OpenVLA, OpenVLA / RT-2 / pi0, Operational documentation, PaliGemma, Performance tuning and optimization, Pipeline-as-code, Platform engineering, Policy-as-code, PowerShell, Predictive modeling, Problem management, Production support, Programmable logic controllers, Prompt versioning, Prototyping, Pull requests, Query optimization, Qwen-VL, RDF, RLHF post-training, RLHF-style post-training, RT-2, Release automation and controls, Reporting dashboards, Responsible AI governance, Root-cause analysis, Routing Information Protocol, SAP/JDE/M3 data concepts (domain knowledge), SAS, SLI/SLO practices, SPARQL, Safety and approval gates, Scalable system development, Secure software development lifecycle, Segmentation, Semantic and knowledge-layer design, Semantic layer creation, Semantic layers, ServiceNow, Shared enterprise AI platforms, Sim-to-real transfer, Simulation, Simulation / sim-to-real transfer, Site reliability engineering, Splunk, Text-to-SQL, Unstructured document parsing, VSCode, VSCode / IDEs (preferred), Video understanding, Vision-language models, Vision-language models (VLMs), Vision-language-action models, Vision-language-action models / robot learning, Web analytics, Windsurf, YAML, YOLO, cloud security / governance / compliance, feature stores, financial/tax automation (domain), model optimization, pi0
