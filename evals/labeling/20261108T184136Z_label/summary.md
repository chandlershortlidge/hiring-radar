# Labeling run 20261108T184136Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v10
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.970, recall 0.982, F1 0.976 (tp 223, B-only 7, A-only 4)
- requirement, on ids both gave: 0.996
- seniority: 1.000 (15/15)
- german: 1.000 (15/15)
- degree: 0.933 (14/15)

## Merge

- accepted on agreement: 192 skills, 35 attributes
- review queue: 13 disagreement, 15 in-scope, 80 spot-check, 39 uncertain
- spot-check: 80 of 227 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_049 german: A 'Fließend Deutsch und Englisch in Wort und Schrift' vs B 'Fließend Deutsch und Englisch\nin Wort und Schrift'
- golden_049 degree: A 'Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in einem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger' vs B 'Abgeschlossenes wissenschaftliches Hochschulstudium (min. Bachelor) in\neinem MINT-Fach, oder vergleichbare Qualifikation als Quereinsteiger,\nTech Enthusiast oder Vibe Coder mit Proof Record'
- golden_051 seniority: A 'Senior AI Engineer' vs B 'Senior AI Engineer / AI Architect'
- golden_054 german: A 'verfügst über gute Deutsch- und Englischkenntnisse' vs B 'gute Deutsch- und Englischkenntnisse'
- golden_055 german: A 'Business-fluent German' vs B 'Business-fluent German and English language skills.'
- golden_055 degree: A 'University degree in Computer Science or a comparable IT-related field' vs B 'University degree in Computer Science or a comparable IT-related field.'
- golden_056 seniority: A 'Senior AI / Reinforcement Learning Engineer' vs B 'Senior AI / Reinforcement Learning Engineer (m/f/d)'
- golden_059 degree: A 'Degree in Engineering, Data Analytics/Science, Computer Science, Mathematics, or a related STEM field' vs B 'Degree in Engineering, Data Analytics/Science, Computer Science, Mathematics, or a related STEM field.'
- golden_060 german: A 'German language skills are desirable' vs B 'German language skills are desirable.'
- golden_063 degree: A 'Abgeschlossenes Studium der Informatik, Data Science, Wirtschaftsinformatik oder einer vergleichbaren Fachrichtung' vs B 'Abgeschlossenes Studium der Informatik, Data Science, Wirtschaftsinformatik oder einer vergleichbaren Fachrichtung.'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- .NET, A2A, A2A (Agent2Agent protocol), AI Engineering, AI governance (EU AI Act, GDPR), AI model integration, AWS CodeBuild, AWS CodeBuild/CodePipeline, AWS CodePipeline, AWS EKS, AWS IAM, AWS Lambda, Accounting and ERP software, Accounting/ERP software, Agile software development, Amazon EKS, ArgoCD, Azure DevOps, Context engineering, Control theory, DSPy, Data engineering, Data engineering tools, Data-driven applications, Databases, Developing or operating security toolchains, Dynamic code analysis, ERP systems, Edge AI, Enterprise application and system integration, Entra ID, Few-shot learning, Flux, Fuzzing, GenAI application optimisation, Imitation Learning, Imitation learning (IL), Integration architectures, Integration of AI models, IsaacSim, JSON, Jakarta Enterprise Edition, Jenkins, KI-Governance, LangChain4J, Locomanipulation policy training, Locomotion policy training, Low-Code-/No-Code-Plattformen, Low-code/no-code platforms, ML frameworks, Microsoft 365, Microsoft Entra ID, Microsoft Power Platform, Model optimization, Model pruning, Motion planning, MuJoCo, Multimodal models, Multimodal understanding, Object Detection, Object detection, On-premise / hybrid infrastructure, On-premise and hybrid infrastructure, OpenAPI, OpenShift, Oracle, Oracle ERP, PPO, Penetration testing tools, Physics-based simulation, Physics-based simulators, Pinecone, Playwright, Podman, Power Platform, PowerShell, Production operations, Programmierung, Pruning, Pydantic, Qdrant, RL frameworks, ROI modeling, RSL-RL, Retrieval, Robot dynamics, Robot kinematics, Robot kinematics/dynamics, SAC, SAP, SAP ERP, SaaS applications, Scalability, Scientific research practice, Scripting, Secure AI applications, Security toolchain development and operation, Segmentation, Sim-to-real transfer, Software deployment, Software security, Specification-driven development, Stable Baselines 3, Static code analysis, TCO modeling, Technical proof-of-concept projects, Text2SQL, Tracking, Training and deployment on humanoid robots, Vision Transformer, Vision transformers, Vision-Language Models, Vision-language models, XRechnung, ZUGFeRD, fuzzing, penetration testing tools, security toolchains, static and dynamic code analysis
