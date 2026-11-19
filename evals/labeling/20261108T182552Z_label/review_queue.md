# Review queue - 20261108T182552Z_label

159 items from 14 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261108T182552Z_label` refuses while any `?` is left, then writes the Goldens.

What the words mean:

- `A` / `B` - take that labeler's version of this skill or attribute, as printed below.
- `both` - both skills belong in the answer key (only for two ids on one phrase).
- `drop` - this skill is not in the answer key / this attribute is null for this posting.
- `ok` - the agreed value printed below is right; keep it.
- A JSON object writes the value yourself, e.g.
  `DECISION: {"requirement": "nice_to_have", "raw_text": "ideally Kubernetes"}` for a skill,
  or `DECISION: {"seniority": "senior", "seniority_basis": "stated", "seniority_signal": "Lead AI Engineer"}`
  for an attribute. A skill override keeps the printed `skill_id` unless you give one.

Items are grouped by what they ask of you, in the order to work them: the in-scope
questions, then disagreements, then uncertain, then mapping, then the spot-check sample.

Spot-check items are a seeded random sample (80 of 142 accepted labels,
seed 0) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong. They print the posting
excerpt and the agreed label only - no `A:`/`B:` lines - so you check the label against the
posting rather than against the labelers, who by construction both said the same thing.

The first 14 items ask whether each posting belongs in the held-out set at all.
They come pre-answered `yes`, so leaving them alone keeps every posting. Answer `no <why>`
and that posting is written to `evals/goldens/excluded.json` with your reason instead of
becoming a Golden, and neither this script nor `new_goldens.py` will pick it again. Use it
for a posting that got past the title and city filters but is not the job market we
measure - a marketing role, a listing in the wrong field. The rest of that posting's items
are then ignored, so you can answer `no` and skip them.

## 1. golden_107 - scope `in_scope` (in-scope)

> Generative AI Engineer (all gender)

- ALTEN Consulting Services GmbH · Generative AI Engineer (all gender)
- Hamburg · de · arbeitsagentur · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_108 - scope `in_scope` (in-scope)

> System Platform Engineer KI (m/w/d)

- R+V Allgemeine Versicherung AG · System Platform Engineer KI (m/w/d)
- Hamburg · de · arbeitsagentur · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_109 - scope `in_scope` (in-scope)

> (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) - Hybrid,München,Stuttgart,Nür...

- Randstad Digital · (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) - Hybrid,München,Stuttgart,Nür...
- Hamburg · de · arbeitsagentur · 15 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_110 - scope `in_scope` (in-scope)

> AI Engineer – KI-Enablement & Solutions (m/w/d)

- Löwenstein Med.Techn.GmbH+Co.KG · AI Engineer – KI-Enablement & Solutions (m/w/d)
- Hamburg · de · arbeitsagentur · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_111 - scope `in_scope` (in-scope)

> Senior DevOps Engineer mit KI- und Security-Erfahrung (m/w/d) ARBEITNEHMERÜBERLASSUNG

- ibc AG · Senior DevOps Engineer mit KI- und Security-Erfahrung (m/w/d) ARBEITNEHMERÜBERLASSUNG
- Hamburg · de · arbeitsagentur · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_112 - scope `in_scope` (in-scope)

> AI Engineer / KI-Entwickler – LLM & RAG (m/w/d)

- PTA · AI Engineer / KI-Entwickler – LLM & RAG (m/w/d)
- Hamburg · de · arbeitsagentur · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_113 - scope `in_scope` (in-scope)

> Public Cloud Engineer (m/w/d) Generative AI befristet bis 31.01.2028

- SIGNAL IDUNA · Public Cloud Engineer (m/w/d) Generative AI befristet bis 31.01.2028
- Hamburg · de · arbeitsagentur · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_114 - scope `in_scope` (in-scope)

> Software Engineering /Data and AI Engineering/ IT-Management Consultant (2026/27 Graduate) (m/f/d)

- Netlight · Software Engineering /Data and AI Engineering/ IT-Management Consultant (2026/27 Graduate) (m/f/d)
- Hamburg · en · arbeitnow · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_115 - scope `in_scope` (in-scope)

> Machine Learning Engineer (m/w/d) – Hamburg

- Decisity (CITO GmbH) · Machine Learning Engineer (m/w/d) – Hamburg
- Hamburg · en · arbeitsagentur · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_116 - scope `in_scope` (in-scope)

> Manufacturing Engineer Artificial Intelligence (all gender)

- ALTEN GmbH München · Manufacturing Engineer Artificial Intelligence (all gender)
- Hamburg · de · arbeitsagentur · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_117 - scope `in_scope` (in-scope)

> Allgemein:Daten sind das Gold von morgen! Und Du suchst, förderst und veredelst das Wertvollste, was unsere Kundenbesitzen: Ihre Daten. Dahe

- DYMATRIX GmbH · Senior AI Data Engineer (all genders)
- Hamburg · de · arbeitsagentur · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_118 - scope `in_scope` (in-scope)

> Cloud Platform Engineer (m/w/d) Kubernetes / STACKIT / AI Platform Operations (Hamburg oder Mainz)

- dtms GmbH · Cloud Platform Engineer (m/w/d) Kubernetes / STACKIT / AI Platform Operations (Hamburg oder Mainz)
- Hamburg · de · arbeitsagentur · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_119 - scope `in_scope` (in-scope)

> Public Cloud Engineer (m/w/d) Schwerpunkt Generative AI

- SIGNAL IDUNA Krankenversicherung a. G. · Public Cloud Engineer (m/w/d) Schwerpunkt Generative AI
- Hamburg · de · arbeitsagentur · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_120 - scope `in_scope` (in-scope)

> Azure DevOps Engineer mit Fokus Azure AI (a*)

- Hamburger Energienetze GmbH · Azure DevOps Engineer mit Fokus Azure AI (a*)
- Hamburg · de · arbeitsagentur · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_109 - skill `full-stack-development` (disagreement)

> (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) -...

- A: (did not label this)
- B: `full-stack-development` · required · raw_text: "Fullstack Software Engineer"

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 16. golden_110 - attribute `degree` (disagreement)

> ...Nutzer bis Geschäftsführung) **Das bringen Sie mit** * Abgeschlossener technischer Bildungsweg in Bereichen wie Informatik, Data Science, Artificial...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="Abgeschlossener technischer Bildungsweg"
- B: value=null · requirement=null · or_equivalent=false · signal=null

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 17. golden_110 - skill `ai-ml` (disagreement)

> ...Deep Learning oder einer vergleichbaren Fachrichtung * Berufserfahrung in der Entwicklung, Umsetzung und im Betrieb von KI-Lösungen (Agenten, Workflows, API-Integrationen) *...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Berufserfahrung in der Entwicklung, Umsetzung und im Betrieb von KI-Lösungen"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 18. golden_110 - skill `workflow-automation` (disagreement)

> ...Optimierung von Schnittstellen * Generierung KI-gestützter Workflows, stetige Weiterentwicklung integrierter Agenten /...

- A: (did not label this)
- B: `workflow-automation` · required · raw_text: "Workflows"

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 19. golden_111 - skill `apis` (disagreement)

> ...Technische Anbindung von KI-Services über APIs - Weiterentwicklung von Datenbankarchitekturen,...

- A: (did not label this)
- B: `apis` · required · raw_text: "APIs"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 20. golden_111 - skill `ci-cd` (disagreement)

> ...Plattformumgebungen - Konzeption und Automatisierung von CI/CD-Pipelines - Umsetzung von Infrastructure as Code und Cloud-native...

- A: (did not label this)
- B: `ci-cd` · required · raw_text: "CI/CD-Pipelines"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 21. golden_111 - skill `containerization` (disagreement)

> ...Cloud-native Architekturen - Betrieb und Weiterentwicklung containerisierter Umgebungen mit Docker, Kubernetes oder OpenShift - Umsetzung von...

- A: (did not label this)
- B: `containerization` · required · raw_text: "containerisierter Umgebungen"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 22. golden_111 - skill `docker` (disagreement)

> ...und Weiterentwicklung containerisierter Umgebungen mit Docker, Kubernetes oder OpenShift - Umsetzung von...

- A: (did not label this)
- B: `docker` · required · raw_text: "Docker"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 23. golden_111 - skill `infrastructure-as-code` (disagreement)

> ...und Automatisierung von CI/CD-Pipelines - Umsetzung von Infrastructure as Code und Cloud-native Architekturen - Betrieb und...

- A: (did not label this)
- B: `infrastructure-as-code` · required · raw_text: "Infrastructure as Code"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 24. golden_111 - skill `kubernetes` (disagreement)

> ...Weiterentwicklung containerisierter Umgebungen mit Docker, Kubernetes oder OpenShift - Umsetzung von...

- A: (did not label this)
- B: `kubernetes` · required · raw_text: "Kubernetes"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 25. golden_111 - skill `llms` (disagreement)

> ...Integration von KI-, Machine-Learning-, LLM- und Generative-AI-Lösungen - Technische Anbindung von KI-Services über APIs -...

- A: (did not label this)
- B: `llms` · required · raw_text: "LLM- und Generative-AI-Lösungen"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 26. golden_111 - skill `machine-learning` (disagreement)

> ...im gesamten Software-Lifecycle - Integration von KI-, Machine-Learning-, LLM- und Generative-AI-Lösungen - Technische Anbindung...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "Machine-Learning-"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 27. golden_111 - skill `observability` (disagreement)

> ...Aufbau und Optimierung von Monitoring-, Observability- und SRE-Strukturen - Zusammenarbeit mit Entwicklung,...

- A: (did not label this)
- B: `observability` · required · raw_text: "Observability-"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 28. golden_111 - skill `openshift` (disagreement)

> ...containerisierter Umgebungen mit Docker, Kubernetes oder OpenShift - Umsetzung von Security-by-Design-Prinzipien im gesamten...

- A: (did not label this)
- B: `openshift` · required · raw_text: "OpenShift"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 29. golden_113 - skill `ai-deployment` (disagreement)

> ...(IaC) verfügst über erste Erfahrungen in der Entwicklung, Bereitstellung und Integration von Generative AI-Anwendungen im Unternehmenskontext, durch den Aufbau geeigneter...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "Bereitstellung und Integration von\nGenerative AI-Anwendungen"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 30. golden_114 - attribute `degree` (disagreement)

> ...you are - Soon-to-be/recent Graduate (2026/2027) with a relevant Master’s Degree in Computer Science, IT, Business Informatics or similar (or Bachelor's + ≥2yrs of full-time experience) - Full business-level fluency in English - Some hands-on...

- A: value="master" · requirement="required" · or_equivalent=false · signal="relevant Master’s Degree in Computer Science, IT, Business Informatics or similar (or Bachelor's + ≥2yrs of full-time experience)"
- B: value="master" · requirement="required" · or_equivalent=true · signal="Master’s Degree in Computer Science, IT, Business Informatics or similar (or Bachelor's + ≥2yrs of full-time experience)"

Options: `A` / `B` / `both` / `drop`

DECISION: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Master’s Degree in Computer Science, IT, Business Informatics or similar (or Bachelor's + ≥2yrs of full-time experience)"}

## 31. golden_115 - skill `rag` (disagreement)

> ...understanding, structuring and synthesis • Develop retrieval and citation logic so every claim links back to its...

- A: `rag` · required · raw_text: "retrieval"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 32. golden_117 - skill `ai-ml` (disagreement)

> ...Ihre Daten. Daher suchen wir Dich als Senior AI Data Engineer (all genders) für unsere Standorte in...

- A: (did not label this)
- B: `ai-ml` · nice_to_have · raw_text: "AI"

Options: `A` / `B` / `both` / `drop`

DECISION: {"requirement": "nice_to_have", "raw_text": "Leidenschaft für Daten, Azure und AI"}

## 33. golden_117 - skill `software-architecture` (disagreement)

> ...Functions sowie Interesse an Microsoft Foundry • Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture • Idealerweise hast Du schon erste Erfahrungen mit...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture"

Options: `A` / `B` / `both` / `drop`

DECISION: drop

## 34. golden_119 - attribute `seniority` (disagreement)

> ...vorzugsweise GCP) und Terraform (IaC) - verfügst über erste Erfahrungen in der Entwicklung, Bereitstellung und Integration von...

- A: value=null · basis=null · signal=null
- B: value="junior" · basis="inferred" · signal="erste Erfahrungen"

Options: `A` / `B` / `both` / `drop`

DECISION: B

## 35. golden_120 - attribute `seniority` (disagreement)

> ...mit Terraform und Azure DevOps. * Idealerweise bringst du nachweisbare Erfahrung im Umgang mit dem Microsoft Azure AI Stack, insbesondere...

- A: value=null · basis=null · signal=null
- B: value="mid" · basis="inferred" · signal="nachweisbare Erfahrung"

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 36. golden_120 - skill `openai-api` (disagreement)

> ...im Umgang mit dem Microsoft Azure AI Stack, insbesondere Azure OpenAI, AI Foundry, Cognitive Services, AI Search und Azure...

- A: `openai-api` · nice_to_have · raw_text: "Azure OpenAI"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: A

## 37. golden_108 - attribute `seniority` (uncertain)

> System Platform Engineer KI (m/w/d)

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 38. golden_108 - skill `cloud` (uncertain)

> ...sind von Vorteil. - Erfahrung in der netzwerkseitigen Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke - Praxiserfahrung im Einsatz von...

- A: `cloud` · required · raw_text: "Anbindung von Cloud-Umgebungen"
- B: `cloud` · required · raw_text: "Erfahrung in der netzwerkseitigen Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 39. golden_109 - attribute `seniority` (uncertain)

> (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) -...

- A: value="senior" · basis="stated" · signal="(Senior) Fullstack Software Engineer"
- B: value="senior" · basis="stated" · signal="(Senior)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 40. golden_109 - skill `cloud` (uncertain)

> ...mit Java (Spring Boot) sowie im Frontend mit Angular. Fundierte Kenntnisse in Cloud-nativen Architekturen, Kubernetes, Docker und idealerweise Cloud Foundry....

- A: `cloud` · required · raw_text: "Fundierte Kenntnisse in Cloud-nativen Architekturen"
- B: `cloud` · required · raw_text: "Cloud-nativen Architekturen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 41. golden_110 - skill `cybersecurity` (uncertain)

> ...Praktische Berührungen mit Datenschutzkonzepten und Informationssicherheit, idealerweise in regulierten Umfeldern (z. B....

- A: `cybersecurity` · required · raw_text: "Informationssicherheit"
- B: `cybersecurity` · required · raw_text: "Informationssicherheit"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 42. golden_110 - skill `data-privacy-and-security` (uncertain)

> ...Agenten-Orchestrierung) * Praktische Berührungen mit Datenschutzkonzepten und Informationssicherheit, idealerweise in regulierten...

- A: `data-privacy-and-security` · required · raw_text: "Datenschutzkonzepten"
- B: `data-privacy-and-security` · required · raw_text: "Datenschutzkonzepten"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 43. golden_111 - skill `ai-ml` (uncertain)

> ...Berufserfahrung in oben genannten Aufgaben** - **Mindestens ein selbst technisch umgesetztes KI-Projekt** - Fundierte DevOps- und Cloud-Erfahrung - Praktische...

- A: `ai-ml` · required · raw_text: "Mindestens ein selbst technisch umgesetztes KI-Projekt"
- B: `ai-ml` · required · raw_text: "Mindestens ein selbst technisch umgesetztes KI-Projekt"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 44. golden_112 - skill `agents` (uncertain)

> ...Dokumentenverarbeitung (etwa Azure Document Intelligence), Agentic AI oder DevSecOps mit Kubernetes und Terraform. ## Warum zur...

- A: `agents` · nice_to_have · raw_text: "Agentic AI"
- B: `agents` · nice_to_have · raw_text: "Agentic AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 45. golden_112 - skill `ai-ml` (uncertain)

> ...Softwareentwicklung mit Python, davon mindestens ein Jahr in KI-Projekten, die produktiv gegangen sind. Dazu ein Studium der Data...

- A: `ai-ml` · required · raw_text: "in KI-Projekten"
- B: `ai-ml` · required · raw_text: "KI-Projekten, die produktiv gegangen sind"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 46. golden_112 - skill `apis` (uncertain)

> ...Prompt Engineering, Retrieval-Augmented Generation und die Anbindung von Modellen über APIs, mit LangChain oder einer vergleichbaren Bibliothek. Sie...

- A: `apis` · required · raw_text: "Anbindung von Modellen über APIs"
- B: `apis` · required · raw_text: "Anbindung von Modellen über APIs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 47. golden_112 - skill `devsecops` (uncertain)

> ...(etwa Azure Document Intelligence), Agentic AI oder DevSecOps mit Kubernetes und Terraform. ## Warum zur PTA? - KI als...

- A: `devsecops` · nice_to_have · raw_text: "DevSecOps"
- B: `devsecops` · nice_to_have · raw_text: "DevSecOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 48. golden_113 - attribute `seniority` (uncertain)

> ...Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in der Entwicklung, Bereitstellung und Integration...

- A: value="junior" · basis="inferred" · signal="verfügst über erste Erfahrungen"
- B: value="junior" · basis="inferred" · signal="erste\nErfahrungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 49. golden_113 - skill `cybersecurity` (uncertain)

> ...mit agilen Methoden und agil geführten Projekten hast idealerweise Kenntnisse von Industriestandards, Sicherheitskonzepten, Richtlinien und regulatorischen Compliance-Anforderungen...

- A: `cybersecurity` · nice_to_have · raw_text: "idealerweise Kenntnisse von Industriestandards, Sicherheitskonzepten"
- B: `cybersecurity` · nice_to_have · raw_text: "hast idealerweise\nKenntnisse von Industriestandards, Sicherheitskonzepten"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 50. golden_114 - skill `backend-development` (uncertain)

> ...wide technical spectrum, including Fullstack Development, Backend, Data Engineering, Cloud Solutions, Architecture, Web...

- A: `backend-development` · required · raw_text: "Backend"
- B: `backend-development` · required · raw_text: "Backend"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 51. golden_114 - skill `cloud` (uncertain)

> ...Fullstack Development, Backend, Data Engineering, Cloud Solutions, Architecture, Web Development, DevOps, and more. Instead...

- A: `cloud` · required · raw_text: "Cloud Solutions"
- B: `cloud` · required · raw_text: "Cloud Solutions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 52. golden_114 - skill `data-engineering` (uncertain)

> ...student roles or full-time in Software Engineering, Data Engineering or IT-Management with modern technologies, (e.g. Fullstack Development,...

- A: `data-engineering` · required · raw_text: "Data Engineering or IT-Management"
- B: `data-engineering` · required · raw_text: "Data Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 53. golden_114 - skill `devops` (uncertain)

> ...Cloud Solutions, Architecture, Web Development, DevOps, Product Ownership or similar) - Based in Hamburg or willing to relocate to...

- A: `devops` · required · raw_text: "DevOps, Product Ownership"
- B: `devops` · required · raw_text: "DevOps"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 54. golden_114 - skill `full-stack-development` (uncertain)

> ...Engineering or IT-Management with modern technologies, (e.g. Fullstack Development, Backend, Data Engineering, Cloud Solutions, Architecture,...

- A: `full-stack-development` · required · raw_text: "e.g. Fullstack Development"
- B: `full-stack-development` · required · raw_text: "Fullstack Development"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 55. golden_114 - skill `software-architecture` (uncertain)

> ...Development, Backend, Data Engineering, Cloud Solutions, Architecture, Web Development, DevOps, and more. Instead of predefined...

- A: `software-architecture` · required · raw_text: "Architecture"
- B: `software-architecture` · required · raw_text: "Architecture"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 56. golden_114 - skill `software-engineering` (uncertain)

> ...through internships, working student roles or full-time in Software Engineering, Data Engineering or IT-Management with modern technologies, (e.g. Fullstack Development,...

- A: `software-engineering` · required · raw_text: "in Software Engineering, Data Engineering or IT-Management"
- B: `software-engineering` · required · raw_text: "Software Engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 57. golden_115 - skill `ai-ml` (uncertain)

> ...team What you bring • 3+ years in machine learning or applied AI engineering • Hands-on experience with LLMs, retrieval and evaluation...

- A: `ai-ml` · required · raw_text: "applied AI engineering"
- B: `ai-ml` · required · raw_text: "applied AI engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 58. golden_116 - attribute `seniority` (uncertain)

> ...Digitalisierung und technologische Innovationen - bringst erste praktische Berührungspunkte mit AI-Anwendungen oder datengetriebenen Ansätzen mit - arbeitest...

- A: value="junior" · basis="inferred" · signal="erste praktische Berührungspunkte mit AI-Anwendungen"
- B: value="junior" · basis="inferred" · signal="erste praktische Berührungspunkte mit AI-Anwendungen oder datengetriebenen Ansätzen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 59. golden_116 - skill `ai-ml` (uncertain)

> ...oder einer vergleichbaren Fachrichtung - verfügst über fundierte Kenntnisse im Bereich Artificial Intelligence und möchtest diese zur Gestaltung moderner Arbeitsabläufe...

- A: `ai-ml` · required · raw_text: "fundierte Kenntnisse im Bereich Artificial Intelligence"
- B: `ai-ml` · required · raw_text: "fundierte Kenntnisse im Bereich Artificial Intelligence"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 60. golden_117 - attribute `german` (uncertain)

> ...gesammelt – kein Muss, aber ein starkes Plus • Sehr gutes Deutsch, gutes Englisch und ein ordentliches Maß an...

- A: value="nice_to_have" · basis="stated" · signal="Sehr gutes Deutsch"
- B: value="nice_to_have" · basis="stated" · signal="Sehr gutes Deutsch"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 61. golden_117 - skill `azure` (uncertain)

> ...vorzugsweise im Beratungsumfeld • Gute Kenntnisse rund um die Azure Data Dienste wie z. B. Data Factory, SQL DB, Data Lake Storage,...

- A: `azure` · nice_to_have · raw_text: "Gute Kenntnisse rund um die Azure Data Dienste"
- B: `azure` · nice_to_have · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 62. golden_117 - skill `azure-data-factory` (uncertain)

> ...Gute Kenntnisse rund um die Azure Data Dienste wie z. B. Data Factory, SQL DB, Data Lake Storage, Databricks, Functions sowie...

- A: `azure-data-factory` · nice_to_have · raw_text: "Data Factory"
- B: `azure-data-factory` · nice_to_have · raw_text: "Data Factory"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 63. golden_117 - skill `azure-data-lake-storage` (uncertain)

> ...um die Azure Data Dienste wie z. B. Data Factory, SQL DB, Data Lake Storage, Databricks, Functions sowie Interesse an Microsoft...

- A: `azure-data-lake-storage` · nice_to_have · raw_text: "Data Lake Storage"
- B: `azure-data-lake-storage` · nice_to_have · raw_text: "Data Lake Storage"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 64. golden_117 - skill `azure-functions` (uncertain)

> ...z. B. Data Factory, SQL DB, Data Lake Storage, Databricks, Functions sowie Interesse an Microsoft Foundry • Starkes Interesse an der...

- A: `azure-functions` · nice_to_have · raw_text: "Functions sowie"
- B: `azure-functions` · nice_to_have · raw_text: "Functions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 65. golden_117 - skill `azure-sql-database` (uncertain)

> ...rund um die Azure Data Dienste wie z. B. Data Factory, SQL DB, Data Lake Storage, Databricks, Functions sowie Interesse...

- A: `azure-sql-database` · nice_to_have · raw_text: "SQL DB"
- B: `azure-sql-database` · nice_to_have · raw_text: "SQL DB"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 66. golden_117 - skill `cloud` (uncertain)

> ...Functions sowie Interesse an Microsoft Foundry • Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture • Idealerweise hast Du schon erste Erfahrungen mit...

- A: `cloud` · nice_to_have · raw_text: "Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture"
- B: `cloud` · nice_to_have · raw_text: "Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 67. golden_117 - skill `data-engineering` (uncertain)

> ...macht • Mehrjährige Berufserfahrung in der Konzeption und Umsetzung von innovativen Data-Engineering-Lösungen, vorzugsweise im Beratungsumfeld • Gute Kenntnisse rund um...

- A: `data-engineering` · nice_to_have · raw_text: "Umsetzung von innovativen Data-Engineering-Lösungen"
- B: `data-engineering` · nice_to_have · raw_text: "Data-Engineering-Lösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 68. golden_117 - skill `databricks` (uncertain)

> ...Dienste wie z. B. Data Factory, SQL DB, Data Lake Storage, Databricks, Functions sowie Interesse an Microsoft Foundry • Starkes Interesse...

- A: `databricks` · nice_to_have · raw_text: "Databricks, Functions"
- B: `databricks` · nice_to_have · raw_text: "Databricks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 69. golden_118 - attribute `degree` (uncertain)

> ...und RBAC sowie DSGVO, ISO 27001 und C5 ### Dein Profil - Abgeschlossene IT-Ausbildung oder abgeschlossenes Studium der (Wirtschafts-)Informatik oder vergleichbar - Fundierte Erfahrung im Aufbau und Betrieb von...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene IT-Ausbildung oder abgeschlossenes Studium der (Wirtschafts-)Informatik oder vergleichbar"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene IT-Ausbildung oder abgeschlossenes Studium der (Wirtschafts-)Informatik oder vergleichbar"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 70. golden_118 - skill `argocd` (uncertain)

> ...Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit Monitoring, Logging und Alerting sowie...

- A: `argocd` · required · raw_text: "z. B. Terraform, Argo CD, Helm oder Kustomize"
- B: `argocd` · required · raw_text: "Argo CD"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 71. golden_118 - skill `cybersecurity` (uncertain)

> ...Plattform- und Datenservices wie PostgreSQL oder MongoDB - Gutes Verständnis für Kubernetes- und Cloud-Security, insbesondere IAM/RBAC, Network Policies, Secrets...

- A: `cybersecurity` · required · raw_text: "Gutes Verständnis für Kubernetes- und Cloud-Security"
- B: `cybersecurity` · required · raw_text: "Kubernetes- und Cloud-Security"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 72. golden_118 - skill `helm` (uncertain)

> ...Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit Monitoring, Logging und Alerting sowie...

- A: `helm` · required · raw_text: "z. B. Terraform, Argo CD, Helm oder Kustomize"
- B: `helm` · required · raw_text: "Helm"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 73. golden_118 - skill `terraform` (uncertain)

> ...Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit Monitoring, Logging und Alerting sowie...

- A: `terraform` · required · raw_text: "z. B. Terraform, Argo CD, Helm oder Kustomize"
- B: `terraform` · required · raw_text: "Terraform"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 74. golden_119 - skill `cybersecurity` (uncertain)

> ...mit agilen Methoden und agil geführten Projekten - hast idealerweise Kenntnisse von Industriestandards, Sicherheitskonzepten, Richtlinien und regulatorischen Compliance-Anforderungen...

- A: `cybersecurity` · nice_to_have · raw_text: "idealerweise Kenntnisse von Industriestandards, Sicherheitskonzepten"
- B: `cybersecurity` · nice_to_have · raw_text: "hast idealerweise Kenntnisse von Industriestandards, Sicherheitskonzepten"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: A

## 75. golden_120 - skill `azure` (uncertain)

> ...und Pflege von Infrastructure-as-Code-Projekten zur Bereitstellung von Azure-Ressourcen mit Terraform und Azure DevOps. * Idealerweise bringst du...

- A: `azure` · required · raw_text: "Bereitstellung von Azure-Ressourcen"
- B: `azure` · required · raw_text: "Azure-Ressourcen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: B

## 76. golden_107 - skill `ci-cd` (check-failed)

> (not found in the posting) CI/CD-Pipelines mit

- A: `ci-cd` · required · raw_text: "CI/CD-Pipelines mit"
- B: `ci-cd` · required · raw_text: "CI/CD-Pipelines"

Auto-check:
- A: raw_text does not appear in the posting: 'CI/CD-Pipelines mit'

Options: `A` / `B` / `drop`

DECISION: B

## 77. golden_107 - skill `docker` (check-failed)

> (not found in the posting) Docker, Kubernetes und CI/CD-Pipelines mit

- A: `docker` · required · raw_text: "Docker, Kubernetes und CI/CD-Pipelines mit"
- B: `docker` · required · raw_text: "Docker"

Auto-check:
- A: raw_text does not appear in the posting: 'Docker, Kubernetes und CI/CD-Pipelines mit'

Options: `A` / `B` / `drop`

DECISION: B

## 78. golden_107 - skill `kubernetes` (check-failed)

> (not found in the posting) Kubernetes und CI/CD-Pipelines mit

- A: `kubernetes` · required · raw_text: "Kubernetes und CI/CD-Pipelines mit"
- B: `kubernetes` · required · raw_text: "Kubernetes"

Auto-check:
- A: raw_text does not appear in the posting: 'Kubernetes und CI/CD-Pipelines mit'

Options: `A` / `B` / `drop`

DECISION: B

## 79. golden_112 - skill `testing` (check-failed)

> (not found in the posting) automatisierten Tests

- A: `testing` · required · raw_text: "automatisierten Tests"
- B: `testing` · required · raw_text: "automatisierte Tests"

Auto-check:
- A: raw_text does not appear in the posting: 'automatisierten Tests'

Options: `A` / `B` / `drop`

DECISION: B

## 80. golden_107 - attribute `degree` (spot-check)

> ...our forward thinker DU... - verfügst über ein abgeschlossenes Studium der Informatik, Ingenieurinformatik, Data Science oder einer vergleichbaren Fachrichtung - bringst fundierte Erfahrung in der Entwicklung von...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="abgeschlossenes Studium der Informatik, Ingenieurinformatik, Data Science oder einer vergleichbaren Fachrichtung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 81. golden_107 - attribute `german` (spot-check)

> ...mit Docker, Kubernetes und CI/CD-Pipelines - verfügst über sehr gute Deutsch- und Englischkenntnisse A home where people learn and thrive -...

- agreed label: value="required" · basis="stated" · signal="sehr gute Deutsch- und Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 82. golden_107 - skill `python` (spot-check)

> ...Generative-AI-, LLM- und RAG-Lösungen mit - hast sehr gute Programmierkenntnisse in Python sowie Erfahrung mit Frameworks wie LangChain, PyTorch und...

- agreed label: `python` · required · raw_text: "Programmierkenntnisse in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_107 - skill `pytorch` (spot-check)

> ...in Python sowie Erfahrung mit Frameworks wie LangChain, PyTorch und TensorFlow - besitzt Kenntnisse im Bereich MLOps,...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 84. golden_107 - skill `rag` (spot-check)

> ...Erfahrung in der Entwicklung von Generative-AI-, LLM- und RAG-Lösungen mit - hast sehr gute Programmierkenntnisse in Python sowie...

- agreed label: `rag` · required · raw_text: "RAG-Lösungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_107 - skill `tensorflow` (spot-check)

> ...sowie Erfahrung mit Frameworks wie LangChain, PyTorch und TensorFlow - besitzt Kenntnisse im Bereich MLOps, Containerisierung...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 86. golden_108 - attribute `degree` (spot-check)

> ...dabei persönlich weiterentwickeln. **Qualifikationen** - Erfolgreiches Studium in Naturwissenschaften, Informatik oder eine vergleichbare Qualifikation. - Interesse daran, Dichin moderne Data- und Cloud...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="Erfolgreiches Studium in Naturwissenschaften, Informatik oder eine vergleichbare Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 87. golden_108 - attribute `german` (spot-check)

> ...in der Zusammenarbeit interdisziplinären Teams mit. - Fließende Deutschkenntnisse (mind. Level B2-C1). **Zusätzliche Informationen** **Homeoffice:** Flexible...

- agreed label: value="required" · basis="stated" · signal="Fließende Deutschkenntnisse (mind. Level B2-C1)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_108 - skill `access-control` (spot-check)

> ...und - Services, z.B. VNets, Service und Private Endpoints, Identity Management, RBAC/ACL sowie Azure Storage (insbesondere Azure Data Lake Storage...

- agreed label: `access-control` · nice_to_have · raw_text: "Identity Management, RBAC/ACL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_108 - skill `azure` (spot-check)

> ...Docker-Images sowie im Umgang mit Terraform und Python. - Kenntnisse in Azure-Infrastrukturen und - Services, z.B. VNets, Service und Private Endpoints,...

- agreed label: `azure` · nice_to_have · raw_text: "Kenntnisse in Azure-Infrastrukturen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_108 - skill `claude-code` (spot-check)

> ...Praxiserfahrung im Einsatz von Coding Agents (z.B. Claude Code oder Codex) sowie ein gutes Verständnis für modernes...

- agreed label: `claude-code` · required · raw_text: "(z.B. Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Claude Code"}

## 91. golden_108 - skill `terraform` (spot-check)

> ...und Debuggen von Docker-Images sowie im Umgang mit Terraform und Python. - Kenntnisse in Azure-Infrastrukturen und -...

- agreed label: `terraform` · required · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_109 - attribute `german` (spot-check)

> ...auch vor Ort innerhalb Deutschlands zu unterstützen. Verhandlungssichere Deutschkenntnisse auf mind. C1-Niveau und gute Englischkenntnisse. Optional: Ein abgeschlossenes...

- agreed label: value="required" · basis="stated" · signal="Verhandlungssichere Deutschkenntnisse auf mind. C1-Niveau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_109 - skill `angular` (spot-check)

> ...in der Softwareentwicklung mit Java (Spring Boot) sowie im Frontend mit Angular. Fundierte Kenntnisse in Cloud-nativen Architekturen,...

- agreed label: `angular` · required · raw_text: "Frontend mit Angular"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_109 - skill `ci-cd` (spot-check)

> ...B. Copilot, Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und Observability-Standards. Ein agiles Mindset, hohes...

- agreed label: `ci-cd` · required · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_109 - skill `devops` (spot-check)

> ...Entwicklungsansätzen (z. B. Copilot, Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und Observability-Standards. Ein agiles Mindset,...

- agreed label: `devops` · required · raw_text: "Know-how in DevOps-Prozessen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_109 - skill `docker` (spot-check)

> ...Fundierte Kenntnisse in Cloud-nativen Architekturen, Kubernetes, Docker und idealerweise Cloud Foundry. Erfahrung mit Microservices, RESTful APIs...

- agreed label: `docker` · required · raw_text: "Kubernetes, Docker und idealerweise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Docker"}

## 97. golden_109 - skill `frontend-development` (spot-check)

> ...in der Softwareentwicklung mit Java (Spring Boot) sowie im Frontend mit Angular. Fundierte Kenntnisse in Cloud-nativen Architekturen,...

- agreed label: `frontend-development` · required · raw_text: "im Frontend mit Angular"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_109 - skill `java` (spot-check)

> ...Practices. Das bringst du mit Mehrjährige Erfahrung in der Softwareentwicklung mit Java (Spring Boot) sowie im Frontend mit Angular. Fundierte...

- agreed label: `java` · required · raw_text: "Softwareentwicklung mit Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_109 - skill `microservices` (spot-check)

> ...Kubernetes, Docker und idealerweise Cloud Foundry. Erfahrung mit Microservices, RESTful APIs sowie Software-Architektur-Methoden (z. B....

- agreed label: `microservices` · required · raw_text: "Erfahrung mit Microservices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_109 - skill `observability` (spot-check)

> ...Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und Observability-Standards. Ein agiles Mindset, hohes Qualitätsbewusstsein sowie...

- agreed label: `observability` · required · raw_text: "Observability-Standards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_109 - skill `software-architecture` (spot-check)

> ...Foundry. Erfahrung mit Microservices, RESTful APIs sowie Software-Architektur-Methoden (z. B. DDD, BDD, Arc42). Praktische Erfahrung im Einsatz...

- agreed label: `software-architecture` · required · raw_text: "Software-Architektur-Methoden"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_109 - skill `software-engineering` (spot-check)

> ...Weiterentwicklung von Best Practices. Das bringst du mit Mehrjährige Erfahrung in der Softwareentwicklung mit Java (Spring Boot) sowie im Frontend mit Angular....

- agreed label: `software-engineering` · required · raw_text: "Mehrjährige Erfahrung in der Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 103. golden_109 - skill `spring-boot` (spot-check)

> ...mit Mehrjährige Erfahrung in der Softwareentwicklung mit Java (Spring Boot) sowie im Frontend mit Angular. Fundierte Kenntnisse in Cloud-nativen...

- agreed label: `spring-boot` · required · raw_text: "Java (Spring Boot) sowie im Frontend"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Spring Boot"}

## 104. golden_110 - attribute `german` (spot-check)

> ...in MedTech oder weiteren regulierten Branchen * Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift **Das können Sie von uns erwarten** * Flexible...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 105. golden_110 - skill `apis` (spot-check)

> ...und im Betrieb von KI-Lösungen (Agenten, Workflows, API-Integrationen) * Anwenderkenntnisse in Low-Code/No-Code-Plattformen (z....

- agreed label: `apis` · required · raw_text: "API-Integrationen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_111 - attribute `degree` (spot-check)

> Senior DevOps Engineer mit KI- und Security-Erfahrung (m/w/d) ARBEITNEHMERÜBERLASSUNG

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_111 - attribute `german` (spot-check)

> Senior DevOps Engineer mit KI- und Security-Erfahrung (m/w/d) ARBEITNEHMERÜBERLASSUNG

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_111 - skill `cybersecurity` (spot-check)

> ...KI-Projekt** - Fundierte DevOps- und Cloud-Erfahrung - Praktische Erfahrung im Bereich IT-Security - Bereitschaft zu vier Office-Tagen pro Woche in Hamburg -...

- agreed label: `cybersecurity` · required · raw_text: "Praktische Erfahrung im Bereich IT-Security"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_111 - skill `devops` (spot-check)

> ...ein selbst technisch umgesetztes KI-Projekt** - Fundierte DevOps- und Cloud-Erfahrung - Praktische Erfahrung im Bereich IT-Security -...

- agreed label: `devops` · required · raw_text: "Fundierte DevOps- und Cloud-Erfahrung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_112 - attribute `degree` (spot-check)

> ...Jahr in KI-Projekten, die produktiv gegangen sind. Dazu ein Studium der Data Science, Informatik, Mathematik oder eine vergleichbare Qualifikation mit entsprechender Berufserfahrung. - Fundierte Python-Kenntnisse, von objektorientierter...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="ein Studium der Data Science, Informatik, Mathematik oder eine vergleichbare Qualifikation mit entsprechender Berufserfahrung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_112 - skill `aws` (spot-check)

> ...mit mindestens einer Cloud-Plattform wie Microsoft Azure, AWS oder Google Cloud. - Freude am direkten Austausch mit...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 112. golden_112 - skill `azure` (spot-check)

> ...Dazu Erfahrung mit mindestens einer Cloud-Plattform wie Microsoft Azure, AWS oder Google Cloud. - Freude am direkten Austausch mit...

- agreed label: `azure` · required · raw_text: "Microsoft Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_112 - skill `cloud` (spot-check)

> ...SQL und unterschiedlichen Datenbanken. Dazu Erfahrung mit mindestens einer Cloud-Plattform wie Microsoft Azure, AWS oder Google Cloud. - Freude am...

- agreed label: `cloud` · required · raw_text: "mindestens einer Cloud-Plattform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_112 - skill `gcp` (spot-check)

> ...einer Cloud-Plattform wie Microsoft Azure, AWS oder Google Cloud. - Freude am direkten Austausch mit Kunden, auch vor Ort,...

- agreed label: `gcp` · required · raw_text: "Google Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_112 - skill `langchain` (spot-check)

> ...Generation und die Anbindung von Modellen über APIs, mit LangChain oder einer vergleichbaren Bibliothek. Sie wissen, wie Sprachmodelle funktionieren, und...

- agreed label: `langchain` · required · raw_text: "mit LangChain oder einer vergleichbaren Bibliothek"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 116. golden_112 - skill `llms` (spot-check)

> ...und Designentscheidungen die Performance beeinflussen. - Praxis mit großen Sprachmodellen: Prompt Engineering, Retrieval-Augmented Generation und...

- agreed label: `llms` · required · raw_text: "Praxis mit großen Sprachmodellen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_112 - skill `python` (spot-check)

> ...Qualifikation mit entsprechender Berufserfahrung. - Fundierte Python-Kenntnisse, von objektorientierter Programmierung über automatisierte...

- agreed label: `python` · required · raw_text: "Fundierte Python-Kenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_112 - skill `rag` (spot-check)

> ...Praxis mit großen Sprachmodellen: Prompt Engineering, Retrieval-Augmented Generation und die Anbindung von Modellen über APIs, mit LangChain...

- agreed label: `rag` · required · raw_text: "Retrieval-Augmented Generation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_112 - skill `software-engineering` (spot-check)

> ...Sie mitbringen - Mindestens drei Jahre Erfahrung in der Softwareentwicklung mit Python, davon mindestens ein Jahr in KI-Projekten, die...

- agreed label: `software-engineering` · required · raw_text: "Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_112 - skill `sql` (spot-check)

> ...und verstehen deshalb auch, wo sie an Grenzen stoßen. - Sicherer Umgang mit SQL und unterschiedlichen Datenbanken. Dazu Erfahrung mit...

- agreed label: `sql` · required · raw_text: "Sicherer Umgang mit SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_112 - skill `terraform` (spot-check)

> ...Agentic AI oder DevSecOps mit Kubernetes und Terraform. ## Warum zur PTA? - KI als zentrale Strategie: KI ist...

- agreed label: `terraform` · nice_to_have · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_113 - skill `ci-cd` (spot-check)

> ...Aufbau geeigneter Infrastruktur-Komponenten auf Basis von Terraform (CI/CD-Pipeline) bist vertraut mit dem Einsatz von Python...

- agreed label: `ci-cd` · required · raw_text: "Terraform (CI/CD-Pipeline)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "CI/CD-Pipeline"}

## 123. golden_113 - skill `cloud` (spot-check)

> ...eine vergleichbare Qualifikation mit IT-Kompetenz hast Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC)...

- agreed label: `cloud` · required · raw_text: "Erfahrung im Bereich Public Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_113 - skill `gcp` (spot-check)

> ...hast Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in...

- agreed label: `gcp` · nice_to_have · raw_text: "vorzugsweise GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_113 - skill `infrastructure-as-code` (spot-check)

> ...im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in der Entwicklung,...

- agreed label: `infrastructure-as-code` · required · raw_text: "Terraform (IaC)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_113 - skill `llms` (spot-check)

> ...erste Erfahrungen in der Entwicklung, Bereitstellung und Integration von Generative AI-Anwendungen im Unternehmenskontext, durch den Aufbau geeigneter...

- agreed label: `llms` · required · raw_text: "Integration von Generative AI-Anwendungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_113 - skill `terraform` (spot-check)

> ...im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in der Entwicklung,...

- agreed label: `terraform` · required · raw_text: "Terraform (IaC)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_114 - attribute `seniority` (spot-check)

> .../Data and AI Engineering/ IT-Management Consultant (2026/27 Graduate) (m/f/d) About us Netlight is an international digital...

- agreed label: value="junior" · basis="stated" · signal="(2026/27 Graduate)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_115 - attribute `german` (spot-check)

> ...document processing or NLP is a plus • Fluent English; German is a plus What we offer • Hybrid setup: office in Hamburg plus...

- agreed label: value="nice_to_have" · basis="stated" · signal="German is a plus"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_115 - skill `llms` (spot-check)

> ...3+ years in machine learning or applied AI engineering • Hands-on experience with LLMs, retrieval and evaluation in production • Strong Python •...

- agreed label: `llms` · required · raw_text: "Hands-on experience with LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 131. golden_115 - skill `machine-learning` (spot-check)

> ...together with the engineering team What you bring • 3+ years in machine learning or applied AI engineering • Hands-on experience with LLMs,...

- agreed label: `machine-learning` · required · raw_text: "3+ years in machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_115 - skill `python` (spot-check)

> ...with LLMs, retrieval and evaluation in production • Strong Python • Experience with document processing or NLP is a plus •...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_117 - attribute `degree` (spot-check)

> Allgemein:Daten sind das Gold von morgen! Und Du suchst, förderst und veredelst das Wertvollste, was unsere Kundenbesitzen: Ihre Daten. Dahe

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_117 - skill `azure-ai-foundry` (spot-check)

> ...SQL DB, Data Lake Storage, Databricks, Functions sowie Interesse an Microsoft Foundry • Starkes Interesse an der Entwicklung von DWH / Data Lake...

- agreed label: `azure-ai-foundry` · nice_to_have · raw_text: "Interesse an Microsoft Foundry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 135. golden_118 - attribute `german` (spot-check)

> ...Betriebsstandards mitzugestalten und zu optimieren - Sehr gute Deutsch- und gute Englischkenntnisse in Wort und Schrift ### Deine Benefits - Attraktives Fixgehalt zzgl....

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutsch- und gute Englischkenntnisse in Wort und Schrift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_118 - attribute `seniority` (spot-check)

> Cloud Platform Engineer (m/w/d) Kubernetes / STACKIT / AI Platform Operations (Hamburg oder Mainz)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 137. golden_118 - skill `access-control` (spot-check)

> ...für Kubernetes- und Cloud-Security, insbesondere IAM/RBAC, Network Policies, Secrets Management, TLS/Zertifikate,...

- agreed label: `access-control` · required · raw_text: "IAM/RBAC"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 138. golden_118 - skill `gitops` (spot-check)

> ...Container-Technologien, automatisierten Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit...

- agreed label: `gitops` · required · raw_text: "Infrastructure as Code und GitOps, z. B."

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "GitOps"}

## 139. golden_118 - skill `infrastructure-as-code` (spot-check)

> ...Container-Technologien, automatisierten Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit...

- agreed label: `infrastructure-as-code` · required · raw_text: "Infrastructure as Code und GitOps, z. B."

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Infrastructure as Code"}

## 140. golden_118 - skill `mongodb` (spot-check)

> ...Erfahrung mit Monitoring, Logging und Alerting sowie idealerweise mit dem Betrieb zentraler Plattform- und Datenservices wie PostgreSQL oder MongoDB - Gutes Verständnis für Kubernetes- und Cloud-Security,...

- agreed label: `mongodb` · nice_to_have · raw_text: "idealerweise mit dem Betrieb zentraler Plattform- und Datenservices wie PostgreSQL oder MongoDB"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 141. golden_118 - skill `openshift` (spot-check)

> ...im Aufbau und Betrieb von Kubernetes-Plattformen, idealerweise mit Managed Kubernetes wie STACKIT SKE, AKS, EKS, GKE oder OpenShift - Umfangreiche Kenntnisse in Cloud-Infrastrukturen, CI/CD,...

- agreed label: `openshift` · nice_to_have · raw_text: "idealerweise mit Managed Kubernetes wie STACKIT SKE, AKS, EKS, GKE oder OpenShift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 142. golden_118 - skill `secrets-management` (spot-check)

> ...für Kubernetes- und Cloud-Security, insbesondere IAM/RBAC, Network Policies, Secrets Management, TLS/Zertifikate, Container-/Image-Security, Audit Logging...

- agreed label: `secrets-management` · required · raw_text: "Network Policies, Secrets Management"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Secrets Management"}

## 143. golden_119 - attribute `degree` (spot-check)

> ...deine Gesundheit **Du** - hast ein abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz - hast einschlägige Erfahrung im Bereich Public Cloud...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 144. golden_119 - skill `azure` (spot-check)

> ...hast einschlägige Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) - verfügst über...

- agreed label: `azure` · required · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 145. golden_119 - skill `cloud` (spot-check)

> ...Qualifikation mit IT-Kompetenz - hast einschlägige Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) -...

- agreed label: `cloud` · required · raw_text: "Erfahrung im Bereich Public Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 146. golden_119 - skill `gcp` (spot-check)

> ...Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) - verfügst über erste Erfahrungen in...

- agreed label: `gcp` · nice_to_have · raw_text: "vorzugsweise GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 147. golden_119 - skill `git` (spot-check)

> ...(CI/CD-Pipeline) - bringst Erfahrungen im Umgang mit Versionskontrollsystemen wie GitLab, GitHub oder Bitbucket mit - bist vertraut mit dem Einsatz von Python als...

- agreed label: `git` · required · raw_text: "Versionskontrollsystemen wie GitLab, GitHub oder Bitbucket"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 148. golden_119 - skill `infrastructure-as-code` (spot-check)

> ...im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) - verfügst über erste Erfahrungen in der Entwicklung,...

- agreed label: `infrastructure-as-code` · required · raw_text: "Terraform (IaC)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_119 - skill `llms` (spot-check)

> ...in der Entwicklung, Bereitstellung und Integration von Generative AI-Anwendungen im Unternehmenskontext, durch den Aufbau geeigneter...

- agreed label: `llms` · required · raw_text: "Generative AI-Anwendungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 150. golden_120 - attribute `degree` (spot-check)

> ...AI-Use-Cases. Was dich auszeichnet * Du verfügst über ein abgeschlossenes Studium der Informatik, Data Science, Mathematik oder eine vergleichbare Qualifikation. * Als Microsoft Azure DevOps Spezialist gehören Azure...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="abgeschlossenes Studium der Informatik, Data Science, Mathematik oder eine vergleichbare Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 151. golden_120 - attribute `german` (spot-check)

> Azure DevOps Engineer mit Fokus Azure AI (a*)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 152. golden_120 - skill `azure-ai-foundry` (spot-check)

> ...dem Microsoft Azure AI Stack, insbesondere Azure OpenAI, AI Foundry, Cognitive Services, AI Search und Azure DevOps, mit. *...

- agreed label: `azure-ai-foundry` · nice_to_have · raw_text: "AI Foundry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_120 - skill `azure-ai-search` (spot-check)

> ...insbesondere Azure OpenAI, AI Foundry, Cognitive Services, AI Search und Azure DevOps, mit. * Eine strukturierte,...

- agreed label: `azure-ai-search` · nice_to_have · raw_text: "AI Search"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 154. golden_120 - skill `git` (spot-check)

> ...sicher, wirtschaftlich und im Einklang mit der Digitalisierungs- und KI-Strategie erfolgen. * Darüber hinaus...

- agreed label: `git` · required · raw_text: "Git"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_120 - skill `infrastructure-as-code` (spot-check)

> ...fundierte Kenntnisse in der Entwicklung und Pflege von Infrastructure-as-Code-Projekten zur Bereitstellung von Azure-Ressourcen mit Terraform und...

- agreed label: `infrastructure-as-code` · required · raw_text: "Infrastructure-as-Code-Projekten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_120 - skill `microsoft-entra-id` (spot-check)

> ...DevOps Spezialist gehören Azure DevOps, Git, Terraform, Entra ID, Key Vaults, Private Endpoints, Networking, Landing Zones...

- agreed label: `microsoft-entra-id` · required · raw_text: "Entra ID"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 157. golden_120 - skill `networking` (spot-check)

> ...Azure DevOps, Git, Terraform, Entra ID, Key Vaults, Private Endpoints, Networking, Landing Zones sowie Monitoring zu deinem täglichen...

- agreed label: `networking` · required · raw_text: "Private Endpoints, Networking"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Networking"}

## 158. golden_120 - skill `observability` (spot-check)

> ...Vaults, Private Endpoints, Networking, Landing Zones sowie Monitoring zu deinem täglichen Handwerkszeug. * Zudem verfügst du...

- agreed label: `observability` · required · raw_text: "Monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 159. golden_120 - skill `terraform` (spot-check)

> ...Microsoft Azure DevOps Spezialist gehören Azure DevOps, Git, Terraform, Entra ID, Key Vaults, Private Endpoints, Networking,...

- agreed label: `terraform` · required · raw_text: "Git, Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: {"raw_text": "Terraform"}
