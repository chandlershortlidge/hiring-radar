# Labeling run 20261108T182552Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v10
- postings picked 14, labeled by both 14, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.963, recall 0.978, F1 0.970 (tp 131, B-only 5, A-only 3)
- requirement, on ids both gave: 1.000
- seniority: 0.857 (12/14)
- german: 1.000 (14/14)
- degree: 0.929 (13/14)

## Merge

- accepted on agreement: 103 skills, 30 attributes
- review queue: 11 disagreement, 14 in-scope, 80 spot-check, 37 uncertain
- spot-check: 80 of 133 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_050 german: A 'Fließende Deutschkenntnisse (mind. Level B2-C1)' vs B 'Fließende Deutschkenntnisse (mind. Level B2-C1).'
- golden_050 degree: A 'Erfolgreiches Studium in Naturwissenschaften, Informatik oder eine vergleichbare Qualifikation' vs B 'Erfolgreiches Studium in Naturwissenschaften, Informatik oder eine vergleichbare Qualifikation.'
- golden_054 seniority: A 'Mindestens drei Jahre Erfahrung in der Softwareentwicklung mit Python' vs B 'Mindestens drei Jahre Erfahrung'
- golden_055 degree: A 'abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz' vs B 'ein abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz'
- golden_061 degree: A 'abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation' vs B 'abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- ACL, AI-assisted personalization, AI-driven personalization / predictive marketing, AKS, AKS (nice_to_have), Agile Methoden, Agile methods, Alerting, Algorithms, Angular, Arc42, Argo CD, Audit Logging, Audit logging, Automated deployments, Azure AI Foundry, Azure AI Search, Azure Cognitive Services, Azure Data Factory, Azure Data Lake Storage, Azure Data Lake Storage Gen2, Azure DevOps, Azure Document Intelligence, Azure Functions, Azure Key Vault, Azure Landing Zones, Azure Machine Learning, Azure OpenAI, Azure Private Endpoints, Azure SQL Database, Azure Storage, Azure Synapse Pipeline, Azure VNets, Azure VNets / Private Endpoints, BDD, Bitbucket, Cloud Foundry, Cloud Foundry (nice_to_have, 'idealerweise'), Cloud and Kubernetes troubleshooting, Cloud-native architecture, Container and image security, Container/Image security, Copilot Studio, DDD, Data Engineering, Data engineering, Data lake development, Data structures, Data structures and algorithms, Data warehouse / data lake, Data warehousing, Database architecture, Databases, Databases (general), Datengetriebene Ansätze, Document processing, Domain-driven design (DDD), EKS, EKS (nice_to_have), GKE, GKE (nice_to_have), GitLab, High availability, IAM, IAM/RBAC, IT Management, IT-Management, Identity Management, Kustomize, Least privilege, Logging, Low-Code/No-Code platforms, Low-Code/No-Code-Plattformen, Microsoft Azure AI Stack, Microsoft Copilot Studio, Microsoft Entra ID, Microsoft Foundry, Microsoft Power Automate, MongoDB, MongoDB (nice_to_have), Network Policies, Object-oriented programming, OpenShift, OpenShift (nice_to_have), Performance optimization, Power Automate, Private Endpoints, Product Ownership, RBAC, RBAC/ACL, Retrieval, SRE, STACKIT SKE, STACKIT SKE (nice_to_have), Secrets Management, Security Reviews, Security by Design, Service Endpoints, Sicherheitskonzepte, Site reliability engineering, Synapse Pipeline, TLS and certificates, TLS/certificates, Understanding software performance implications, Vibe Engineering, Web Development, automated deployments, data-driven approaches, logging / alerting
