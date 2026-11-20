# Labeling run 20261119T140709Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v11
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.934, recall 0.994, F1 0.963 (tp 170, B-only 12, A-only 1)
- requirement, on ids both gave: 0.971
- seniority: 0.933 (14/15)
- german: 1.000 (15/15)
- degree: 0.933 (14/15)

## Merge

- accepted on agreement: 123 skills, 41 attributes
- review queue: 20 disagreement, 15 in-scope, 80 spot-check, 44 uncertain
- spot-check: 80 of 164 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_098 seniority: A 'ML Engineer Intern' vs B 'Remote ML Engineer Intern – Gaming Data & AI'
- golden_099 degree: A 'A BS in Computer Science, Engineering or a related field, or equivalent practical experience' vs B 'A BS in Computer Science, Engineering or a related field, or equivalent practical experience.'
- golden_105 seniority: A 'Senior Consultant level' vs B 'Cyber - AI Engineer - Senior - Consulting'
- golden_106 degree: A 'MS or PhD in Computer Science, Engineering, or a related field, or equivalent experience' vs B 'MS or PhD in Computer Science, Engineering, or a related field, or equivalent experience.'
- golden_108 seniority: A 'One senior engineer (8-10+ years)' vs B 'senior engineer (8-10+ years)'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI red teaming, AI_AGG, AI_CLASSIFY, AI_COMPLETE, AI_EMBED, AI_EXTRACT, Adversarial testing, Amazon Neptune, Analytics engineering, Application security, Automated remediation, Azure AI Services, Azure API Management, Azure App Services, Azure Functions, Azure Storage, Big data, C, CCSP certification, CISSP / CCSP certifications, CISSP certification, Classical predictive modeling, Cloud data warehouses, Code-security platform integration, Collibra, Context window management, Cortex AI Functions (AISQL), Cortex AI Functions examples, Cortex Agents, Cortex Analyst, Cortex Analyst / Semantic Models or Views, Cortex Search, Cost and latency tuning, Cypher, DGL, Data architecture, Data engineering, Data engineering / data transformation, Data governance, Data governance tools, Data integration, Data mesh / data products, Data transformation, Data-mesh delivery, Data-product delivery, Database design, Datadog, Debugging, Debugging and troubleshooting, Deployment in regulated or restricted environments, Detection engineering, Distributed data warehouses, Document AI, Document intelligence, EDR, EDR integration, Embedding-based matching, Enterprise identity, Enterprise identity (SSO, role-based access), Entity resolution, Entity resolution tools (Splink, Zingg, Senzing), Evaluation dataset construction, GQL, General-purpose programming, Google Dataplex, Graph databases, Graph databases (Neo4j, Amazon Neptune, TigerGraph), Graph machine learning, Graph machine learning / link prediction, Graph query languages, Graph query languages (Cypher/GQL, SPARQL, Gremlin), Graph traversal, Gremlin, HIPAA-compliant application development, HL7 FHIR APIs, HL7 FHIR APIs and healthcare interoperability standards, Human-in-the-loop workflows, Hybrid retrieval, Identity and access management, Incident response automation, Informatica, Knowledge retrieval, Large-scale infrastructure, LiDAR/camera perception, Lightweight classifiers, Link prediction, Linked data, LoRA, MITRE ATLAS, ML and LLM compute-cost optimization, ML frameworks, Master data management, Master data management / data governance tools (Collibra, Informatica, Google Dataplex), Metadata management platforms, Model adaptation, Model drift, Model integration, Model metric workflows, Model optimization, Model registry, Multi-sensor fusion, Multi-user concurrency, Neo4j, OWASP Top 10 for LLMs, OWL, Ontology / semantic-web standards (RDF, OWL, SHACL, SKOS), Ontology design, Ontology modeling, Open-source contribution, PEFT (LoRA/QLoRA), Palantir Foundry Ontology, Parameter-efficient fine-tuning, Performance tuning, Probabilistic matching, Prompt injection, Property-graph modeling, Prototyping, PyTorch Geometric, PyTorch Geometric / DGL, QLoRA, RDF, Rights-management platforms, Role-based access control, SAS, SHACL, SIEM, SIEM integration, SKOS, SOAR, SOAR integration, SPARQL, Sandboxing, Scalability, Secure AI operations, Secure code review, Secure engineering, Secure security-platform integration, Security architecture, Security operations, Semantic Views, Semantic layers, Semantic model governance and versioning, Semantic search, Semantic-web standards, Senzing, Single sign-on, SnowPro certification, Snowflake CoWork / Snowflake Intelligence, Snowflake Cortex, Snowflake Native Apps, Snowflake Semantic Models, Snowflake Semantic Views, Snowpark, Splink, Summarization, Systems engineering, Talend, Technical documentation, Text classification, Text-to-SQL, Threat investigation, TigerGraph, VBA, Versioned taxonomies, Vulnerability analysis, Vulnerability-management platform integration, Wikibase, Wikidata, Wikidata / Wikibase, Palantir Foundry Ontology, Workflow orchestration, Zingg, data engineering, data warehousing, large-scale infrastructure, lightweight classifiers, metadata management, multi-sensor fusion, ontology design, performance tuning, security and governance, semantic layers, taxonomy versioning, text classification, text-to-SQL

Third labeller (HIR-379) read the labelling inputs of commit cc2ea69 - skill list v11, guide before the 19 Nov degree rule - the same question A and B were asked. Degree items were left for a person in the proposer, judge and third-labeller steps.
