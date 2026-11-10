# Labeling run 20261103T224145Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v8
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.954, recall 0.992, F1 0.973 (tp 249, B-only 12, A-only 2)
- requirement, on ids both gave: 0.968
- seniority: 1.000 (15/15)
- german: 1.000 (15/15)
- degree: 1.000 (15/15)

## Merge

- accepted on agreement: 205 skills, 41 attributes
- review queue: 22 disagreement, 15 in-scope, 80 spot-check, 40 uncertain
- spot-check: 80 of 246 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_065 german: A 'German (Nice-to-have)' vs B 'German (Nice-to-have): Proficiency in German is a strong plus for collaborating with clients and partners.'
- golden_067 seniority: A 'Staff Machine Learning Engineer' vs B 'Staff Machine Learning Engineer, LLM Inference Optimization'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI tooling ecosystem, AWQ, AWS CDK, AWS CloudFormation, Agent authorization integration, Agile (Scrum, Kanban, SAFe), Agile software development, Algorithm design, Apache Beam, Audio processing, Authentication, Authentication / authorization, Authorization, Azure AI Foundry, Building and operating production data systems, Clean Code, Clean code, Clean coding, Cloud-native architecture, Cloud-native tooling, Code Reviews, Code quality, Code review, Code reviews, Concurrency, Context engineering, Cost and latency optimization, Data Engineering, Data Quality, Data analysis, Data preprocessing, Data quality, Databases, Datadog, Dataleap, Debugging, Developer environments, Developer platforms, Developer tooling, Django, Documentation automation, EAGLE, EU data-residency constraints, Enterprise AI integration, Enterprise standards, FP8, Fault analysis, Fault tolerance, FlashInfer, FusionAuth, GPTQ, High-concurrency processing, INT4, INT8, Inference batching, Inference parallelism, Infrastructure systems, JetBrains ecosystem, KV cache, Kanban, LLM frameworks, LMCache, Load balancing, Logging, Low-code platforms, Low-precision formats (FP8, INT8, INT4, NVFP4, MXFP4), MXFP4, Mastra, Medusa, Memory bandwidth, Message queues, Model optimization, Modern development workflows, Multi-token prediction, NVFP4, Nest.js, On-call and incident practices, Platform specialization, Provider rate-limit and fallback handling, Pull requests, Pydantic, Real-time data streaming, Real-time production systems at scale, Real-time systems, Reliability practices, Retool, Retraining, SAFe, SLOs / on-call / incident practices, Scrum, Service architectures, Service-level objectives, SmoothQuant, Software deployment, Software fundamentals, Software systems integration, Structured outputs, Svelte, Systems debugging, Systems design, Technical documentation, Tool contracts, Transformer attention, Transformer inference internals (KV cache, attention, batching, parallelism), Triton (GPU kernel language), Triton GPU programming, Vercel AI SDK, Vercel ai-sdk, Vision-language model inference, Voice infrastructure, Voice workflows, Workflow orchestration, audio processing, cloud-native tooling, code review, concurrency, context engineering, data preprocessing, developer productivity tooling, fault tolerance, internal developer platforms, load balancing, message queues, modern service architectures, real-time data streaming, real-time systems, voice infrastructure, workflow orchestration
