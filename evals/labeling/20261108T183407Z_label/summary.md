# Labeling run 20261108T183407Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v10
- postings picked 13, labeled by both 13, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.969, recall 0.975, F1 0.972 (tp 158, B-only 5, A-only 4)
- requirement, on ids both gave: 0.987
- seniority: 0.846 (11/13)
- german: 1.000 (13/13)
- degree: 1.000 (13/13)

## Merge

- accepted on agreement: 132 skills, 32 attributes
- review queue: 11 disagreement, 13 in-scope, 1 mapping, 80 spot-check, 29 uncertain
- spot-check: 80 of 164 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_054 degree: A 'Abgeschlossenes Studium der Informatik, Wirtschaftsinformatik oder vergleichbare Qualifikation' vs B 'Abgeschlossenes Studium der Informatik, Wirtschaftsinformatik oder vergleichbare Qualifikation.'
- golden_056 seniority: A '7 years of experience in software or data engineering' vs B '7 years of experience'
- golden_056 degree: A "Bachelor's degree in Computer Science, a related field, or equivalent practical experience" vs B "Bachelor's degree in Computer Science, a related field, or equivalent practical experience."
- golden_061 german: A 'Sehr gute Deutschkenntnisse (C1 oder höher)' vs B 'Sehr gute Deutschkenntnisse (C1 oder höher).'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI frameworks, AWS Glue, AWS Glue (nice_to_have), AWS Lake Formation (nice_to_have), Agent skills, Agentic skills, Agile methodologies, Agile ways of working, Agile working methods, Amazon Lex, Azure AI, Backlog work, Blue/green deployments, Chatbots, Classification Models, Classification models, Clustering, Code Review, Code quality assessment, Code review, Context Window Management, Context window, Context window management, Customer-managed encryption keys, Data Engineering, Data Vault, Data engineering, Data residency, Dataflow, Definition of Done, Design patterns, Encryption at rest and in transit, Encryption at rest and in transit using CMEK, End-to-end software development lifecycle, Famulor, Google Cloud Dataflow, Google Cloud Pub/Sub, JSON, Jenkins, Jira, Keras, Kiro CLI, LLM hallucinations, Lake Formation, Microsoft Copilot Studio, Microsoft Copilot Studio (nice_to_have), Microsoft Foundry Agents Service, Microsoft Foundry Agents Service (nice_to_have), Microsoft Power Automate, Microsoft SQL Server, Model identification, Prompt injection, Pub/Sub, Re-ranking, SAFe, SAFe (nice_to_have), SDLC, Scrum, Security standards, Shell scripting, Star Schema, System administration, Systemadministration, Technical demo development, Technical discovery and PRD development, Text-to-Speech (TTS), Text-to-speech, Token cost, Token cost understanding, Trunk-based development, VPN technologies, Vertex AI Agent Builder, Vertical task slicing, Voice AI platforms, Voice-AI platforms, Voicebots, Web development, Webhooks, blue/green deployments, data engineering, design patterns, modern AI frameworks, trunk-based development
