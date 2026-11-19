# Labeling run 20261108T182552Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v12
- postings picked 14, labeled by both 14, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.902, recall 0.987, F1 0.942 (tp 147, B-only 16, A-only 2)
- requirement, on ids both gave: 1.000
- seniority: 0.857 (12/14)
- german: 1.000 (14/14)
- degree: 0.857 (12/14)

## Merge

- accepted on agreement: 110 skills, 32 attributes
- review queue: 4 check-failed, 22 disagreement, 14 in-scope, 80 spot-check, 39 uncertain
- spot-check: 80 of 142 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_107 german: A 'sehr gute Deutsch- und Englischkenntnisse' vs B 'verfügst über sehr gute Deutsch- und Englischkenntnisse'
- golden_107 degree: A 'abgeschlossenes Studium der Informatik, Ingenieurinformatik, Data Science oder einer vergleichbaren Fachrichtung' vs B 'verfügst über ein abgeschlossenes Studium der Informatik, Ingenieurinformatik, Data Science oder einer vergleichbaren Fachrichtung'
- golden_108 german: A 'Fließende Deutschkenntnisse (mind. Level B2-C1)' vs B 'Fließende Deutschkenntnisse (mind. Level B2-C1).'
- golden_108 degree: A 'Erfolgreiches Studium in Naturwissenschaften, Informatik oder eine vergleichbare Qualifikation' vs B 'Erfolgreiches Studium in Naturwissenschaften, Informatik oder eine vergleichbare Qualifikation.'
- golden_109 degree: A 'Optional: Ein abgeschlossenes Hochschulstudium in (Wirtschafts-) Informatik oder eine vergleichbare Ausbildung sind von Vorteil' vs B 'Optional: Ein abgeschlossenes Hochschulstudium in (Wirtschafts-) Informatik oder eine vergleichbare Ausbildung sind von Vorteil.'
- golden_112 seniority: A 'Mindestens drei Jahre Erfahrung in der Softwareentwicklung' vs B 'Mindestens drei Jahre Erfahrung in der Softwareentwicklung mit Python'
- golden_113 degree: A 'abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz' vs B 'abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit\nIT-Kompetenz'
- golden_114 seniority: A '(2026/27 Graduate)' vs B '2026/27 Graduate'
- golden_115 seniority: A '3+ years' vs B '3+ years in machine learning or applied AI engineering'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI-gestützte Personalisierung, AKS, Agile Methoden, Agile methods, Alerting, Algorithms, Arc42, Audit logging, Automated deployments, Azure Cognitive Services, Azure Document Intelligence, Azure Landing Zones, Azure Machine Learning, Azure OpenAI, Azure Storage, Azure Synapse Pipelines, BDD, BDD (Behavior-Driven Development), Bitbucket, Cloud Foundry, Cloud Foundry (nice_to_have, 'idealerweise'), Cloud and Kubernetes troubleshooting, Cloud-native architectures, Container/image security, Copilot Studio, DDD, DDD (Domain-Driven Design), Data structures, Data structures and algorithms, Database architecture, Databases, Databases (generic), Datengetriebene Ansätze, Document processing, EKS, GKE, GitLab, High-availability solutions, IT management, Kustomize, Logging, Low-Code/No-Code platforms, Low-Code/No-Code-Plattformen, Microsoft Azure AI Stack, Microsoft Copilot Studio, Object-oriented programming, Performance optimization, Predictive Marketing, Predictive Marketing / Customer Intelligence / AI-gestützte Personalisierung (domain), Product ownership, Retrieval, STACKIT SKE, Site reliability engineering, Synapse Pipeline, TLS and certificate management, TLS/certificates, Vibe Engineering, Web Development, Web development, arc42, document processing

## Spot-check error rate (after review)

- 9 errors in 80 reviewed labels = 0.113
- 95% Wilson interval: 0.060 to 0.200

Wrong labels found:
- golden_108 skill `claude-code` -> {"raw_text": "Claude Code"}
- golden_109 skill `docker` -> {"raw_text": "Docker"}
- golden_109 skill `spring-boot` -> {"raw_text": "Spring Boot"}
- golden_113 skill `ci-cd` -> {"raw_text": "CI/CD-Pipeline"}
- golden_118 skill `gitops` -> {"raw_text": "GitOps"}
- golden_118 skill `infrastructure-as-code` -> {"raw_text": "Infrastructure as Code"}
- golden_118 skill `secrets-management` -> {"raw_text": "Secrets Management"}
- golden_120 skill `networking` -> {"raw_text": "Networking"}
- golden_120 skill `terraform` -> {"raw_text": "Terraform"}
