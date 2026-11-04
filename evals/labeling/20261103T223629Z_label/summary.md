# Labeling run 20261103T223629Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v8
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.935, recall 1.000, F1 0.966 (tp 144, B-only 10, A-only 0)
- requirement, on ids both gave: 0.986
- seniority: 0.933 (14/15)
- german: 1.000 (15/15)
- degree: 0.867 (13/15)

## Merge

- accepted on agreement: 100 skills, 37 attributes
- review queue: 15 disagreement, 15 in-scope, 80 spot-check, 47 uncertain
- spot-check: 80 of 137 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_054 degree: A "Bachelor's or Master's degree in Computer Science, Engineering, or a related technical field" vs B "Completed a Bachelor's or Master's degree in Computer Science, Engineering, or a related technical field."
- golden_057 degree: A "Bachelor's or master's degree in computer science, engineering, or a related field" vs B "Bachelor's or master's degree in computer science, engineering, or a related field."
- golden_063 seniority: A '5+ years of experience in Solutions Engineering' vs B '5+ years of experience'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI alignment, AI gateways, AI governance, ASIC, Advanced modeling techniques, Algorithms, Amazon Redshift, Analytics engineering development cycle, CUDA Graphs, ClickHouse, Cluster computing environment, Codebase development best practices, Collaborative software development workflow, CuTe DSL, Data flows, Data governance, Data mining tools, Data orchestration, Data platforms, Data processing tools, Data structures, Data structures and algorithms, Data warehouse, Data warehousing, Data wrangling, Dataset curation, Debugging, Developer tools, Experimental design, Experimental design and evaluation, FPGA, FPGA/ASIC, Fivetran, Forward deployed engineering, Forward-deployed engineering, Graph neural networks, Graph neural networks (posting says “neutral”), HELM, HELM evaluation framework, Hex, High-throughput research infrastructure, Hightouch, Information retrieval, Kernel development, Looker, MATLAB, Mathematical optimization, Matlab, Model routing, Modern data stack, Modern sequence models, Omni, Orchestration, Pallas, Personalization, Policy enforcement, Post-training, Pre-sales engineering, Probability, Problem decomposition, Quant research, Redshift, Reporting and dashboarding, Search ranking, Secure and scalable system design, Security (AI systems), Security sandboxing, Sequence models, Sigma, Software deployment, Software design principles, Systems performance, Technical consulting, Technical documentation, Translating methods between application areas, Triton (GPU kernel language), Triton kernel programming, Usage controls, Working with large-scale datasets, XLA, adversarial testing, alignment, analytics engineering, data mining, debugging, experiment design, forward-deployed engineering, high-throughput research infrastructure, information retrieval, large-scale data processing, lm-evaluation-harness, orchestration (unspecified), personalization, policy enforcement, post-training, search ranking, security sandboxing, software design, systems performance, technical documentation, verifiers (eval framework), verifiers evaluation framework
