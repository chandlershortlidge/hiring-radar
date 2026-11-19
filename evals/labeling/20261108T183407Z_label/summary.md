# Labeling run 20261108T183407Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v12
- postings picked 13, labeled by both 13, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.964, recall 0.953, F1 0.959 (tp 163, B-only 6, A-only 8)
- requirement, on ids both gave: 0.988
- seniority: 0.923 (12/13)
- german: 1.000 (13/13)
- degree: 1.000 (13/13)

## Merge

- accepted on agreement: 136 skills, 36 attributes
- review queue: 13 disagreement, 13 in-scope, 2 mapping, 80 spot-check, 27 uncertain
- spot-check: 80 of 172 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_122 seniority: A 'Senior AI Voicebot & Automation Engineer' vs B 'Senior AI Voicebot & Automation Engineer (all gender)'
- golden_126 degree: A 'Abgeschlossenes Studium der Informatik, Wirtschaftsinformatik oder vergleichbare Qualifikation' vs B 'Abgeschlossenes Studium der Informatik, Wirtschaftsinformatik oder vergleichbare Qualifikation.'
- golden_128 seniority: A '7 years of experience in software or data engineering' vs B '7 years of experience'
- golden_128 degree: A "Bachelor's degree in Computer Science, a related field, or equivalent practical experience" vs B "Bachelor's degree in Computer Science, a related field, or equivalent practical experience."
- golden_131 german: A 'Verhandlungssichere Deutsch-' vs B 'Verhandlungssichere Deutsch- und gute Englischkenntnisse'
- golden_133 german: A 'Sehr gute Deutschkenntnisse (C1 oder höher)' vs B 'Sehr gute Deutschkenntnisse (C1 oder höher).'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI frameworks, AI frameworks (generic), AI hallucinations, AWS Bedrock AgentCore, AWS Glue, AWS Glue (nice_to_have, alternative to Lake Formation), AWS Lake Formation (nice_to_have, alternative to AWS Glue), Agentic skills, Agile / SDLC, Agile Arbeitsweisen, Agile methods, Amazon Lex, Azure AI, Backlog management, Blue/green deployments, Classification Models, Classification models, Cloud Native, Clustering, Code review, Customer-managed encryption keys, Data residency, Data technologies, Dataflow, Definition of Done, Design patterns, Encryption / CMEK, Encryption at rest and in transit, Encryption at rest and in transit, including CMEK, Engineering tools (unspecified), Famulor, Google Cloud Dataflow, Google Cloud Pub/Sub, JSON, Jira, Keras, Kiro CLI, Lake Formation, Microsoft Copilot Studio, Microsoft Copilot Studio (nice to have), Microsoft Foundry Agents Service, Microsoft SQL Server, Model identification, Programming languages, Prompt injection, Pub/Sub, Re-ranking, SAFe, SAFe (nice to have), Scrum, Shell scripting, Software design patterns, Software development lifecycle, System administration, T-SQL, Text-to-Speech (TTS), Text-to-speech (TTS), Token cost, Token costs, Trunk-based development, VPN technologies, Vertex AI Agent Builder, Vertical task slicing, Voice-AI platforms, Voicebots, Webhooks
