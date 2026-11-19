# Labeling run 20261108T184136Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v12
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.959, recall 0.992, F1 0.975 (tp 234, B-only 10, A-only 2)
- requirement, on ids both gave: 1.000
- seniority: 1.000 (15/15)
- german: 1.000 (15/15)
- degree: 1.000 (15/15)

## Merge

- accepted on agreement: 177 skills, 36 attributes
- review queue: 12 disagreement, 15 in-scope, 80 spot-check, 66 uncertain
- spot-check: 80 of 213 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_134 degree: A 'Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in einem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger' vs B 'Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in einem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger, Tech Enthusiast oder Vibe Coder mit Proof Record'
- golden_135 seniority: A 'mindestens 4\nJahre Erfahrung' vs B 'mindestens 4 Jahre Erfahrung'
- golden_139 seniority: A 'Idealerweise hast du bereits 3–5 Jahre in der Softwareentwicklung' vs B 'Idealerweise hast du bereits 3–5 Jahre in der Softwareentwicklung, im AI Engineering oder Machine Learning gearbeitet.'
- golden_140 german: A 'Business-fluent German' vs B 'Business-fluent German and English language skills.'
- golden_140 degree: A 'University degree in Computer Science or a comparable IT-related field' vs B 'University degree in Computer Science or a comparable IT-related field.'
- golden_141 seniority: A 'Senior AI / Reinforcement Learning Engineer' vs B 'Senior AI / Reinforcement Learning Engineer (m/f/d)'
- golden_144 degree: A 'Degree in Engineering, Data Analytics/Science, Computer Science, Mathematics, or a related STEM field' vs B 'Degree in Engineering, Data Analytics/Science, Computer Science, Mathematics, or a related STEM field.'
- golden_145 german: A 'German language skills are desirable' vs B 'German language skills are desirable.'
- golden_148 degree: A 'Abgeschlossenes Studium der Informatik, Data Science, Wirtschaftsinformatik oder einer vergleichbaren Fachrichtung' vs B 'Abgeschlossenes Studium der Informatik, Data Science, Wirtschaftsinformatik oder einer vergleichbaren Fachrichtung.'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- A2A, A2A (Agent2Agent protocol), AI Engineering, AI governance (EU AI Act, GDPR), AI model integration, AWS CodeBuild, AWS CodeBuild/CodePipeline, AWS CodePipeline, AWS Lambda, Accounting software, Agile software development, Amazon EKS, Control theory, DSPy, Data-driven applications, Databases, Deployment, Dynamic code analysis, ERP / accounting software, ERP software, ERP systems, Edge AI, Enterprise application and systems integration, Enterprise application integration, Few-shot learning, Flux, Fuzzing, GenAI application optimisation, Imitation Learning, Imitation learning (IL), Integration architectures, Integration of AI models, Isaac Sim, IsaacSim, JSON, Jakarta EE, Jakarta Enterprise Edition, KI-Governance, LangChain4J, Locomotion and locomanipulation policy training, Locomotion/locomanipulation policy training, Low-Code-/No-Code-Plattformen, Low-code/no-code platforms, ML frameworks, ML frameworks (generic), Microsoft 365, Model optimization, Model pruning, Motion planning, MuJoCo, Multi-tenancy, Multimodal models, Multimodal understanding, Object Detection, Object detection, Object tracking, On-premise / hybrid infrastructure, On-premise and hybrid infrastructure, OpenAPI, Oracle, PPO, Penetration testing, Penetration testing tools, Physics-based simulation, Physics-based simulators, Podman, Power Platform, PowerShell, Programmierung, Proximal Policy Optimization (PPO), Pruning, Pydantic, RL frameworks, RSL-RL, Reinforcement learning frameworks, Reliable production operation, Robot kinematics and dynamics, Robot kinematics/dynamics, SAC, SAP, SaaS applications, Scalability, Scientific research, Scripting, Security toolchain development or operation, Segmentation, Sim-to-real transfer, Soft Actor-Critic (SAC), Software deployment, Specification-driven development, Stable Baselines 3, Static and dynamic code analysis, Static code analysis, Technical proof-of-concept development, Text-to-SQL, Text2SQL, Tracking, Vision-Language Models, Vision-language models, XRechnung / ZUGFeRD e-invoicing standards, secure AI applications, security toolchains

## Spot-check error rate (after review)

- 11 errors in 80 reviewed labels = 0.138
- 95% Wilson interval: 0.079 to 0.230

Wrong labels found:
- golden_136 skill `rag` -> {"raw_text": "RAG"}
- golden_137 skill `azure` -> {"raw_text": "Azure"}
- golden_137 skill `pytorch` -> {"raw_text": "PyTorch"}
- golden_137 skill `tensorflow` -> {"raw_text": "TensorFlow"}
- golden_138 skill `cloud` -> {"raw_text": "Cloud-Plattformen"}
- golden_138 skill `mlops` -> {"raw_text": "MLOps"}
- golden_141 attribute `degree` -> {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Master’s or PhD in robotics, computer science, engineering, or a related field"}
- golden_142 skill `ci-cd` -> {"raw_text": "CI/CD"}
- golden_142 skill `containerization` -> {"raw_text": "Container"}
- golden_142 skill `infrastructure-as-code` -> {"raw_text": "Infrastructure as Code"}
- golden_147 skill `microsoft-entra-id` -> {"raw_text": "Entra ID"}
