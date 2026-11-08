# Review queue - 20261108T182552Z_label

142 items from 14 postings. Labeler A: `claude-opus-5-5` (anthropic).
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

Spot-check items are a seeded random sample (80 of 133 accepted labels,
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

## 1. golden_049 - scope `in_scope` (in-scope)

> Generative AI Engineer (all gender)

- ALTEN Consulting Services GmbH · Generative AI Engineer (all gender)
- Hamburg · de · arbeitsagentur · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_050 - scope `in_scope` (in-scope)

> System Platform Engineer KI (m/w/d)

- R+V Allgemeine Versicherung AG · System Platform Engineer KI (m/w/d)
- Hamburg · de · arbeitsagentur · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_051 - scope `in_scope` (in-scope)

> (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) - Hybrid,München,Stuttgart,Nür...

- Randstad Digital · (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) - Hybrid,München,Stuttgart,Nür...
- Hamburg · de · arbeitsagentur · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_052 - scope `in_scope` (in-scope)

> AI Engineer – KI-Enablement & Solutions (m/w/d)

- Löwenstein Med.Techn.GmbH+Co.KG · AI Engineer – KI-Enablement & Solutions (m/w/d)
- Hamburg · de · arbeitsagentur · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_053 - scope `in_scope` (in-scope)

> Senior DevOps Engineer mit KI- und Security-Erfahrung (m/w/d) ARBEITNEHMERÜBERLASSUNG

- ibc AG · Senior DevOps Engineer mit KI- und Security-Erfahrung (m/w/d) ARBEITNEHMERÜBERLASSUNG
- Hamburg · de · arbeitsagentur · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_054 - scope `in_scope` (in-scope)

> AI Engineer / KI-Entwickler – LLM & RAG (m/w/d)

- PTA · AI Engineer / KI-Entwickler – LLM & RAG (m/w/d)
- Hamburg · de · arbeitsagentur · 15 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_055 - scope `in_scope` (in-scope)

> Public Cloud Engineer (m/w/d) Generative AI befristet bis 31.01.2028

- SIGNAL IDUNA · Public Cloud Engineer (m/w/d) Generative AI befristet bis 31.01.2028
- Hamburg · de · arbeitsagentur · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_056 - scope `in_scope` (in-scope)

> Software Engineering /Data and AI Engineering/ IT-Management Consultant (2026/27 Graduate) (m/f/d)

- Netlight · Software Engineering /Data and AI Engineering/ IT-Management Consultant (2026/27 Graduate) (m/f/d)
- Hamburg · en · arbeitnow · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_057 - scope `in_scope` (in-scope)

> Machine Learning Engineer (m/w/d) – Hamburg

- Decisity (CITO GmbH) · Machine Learning Engineer (m/w/d) – Hamburg
- Hamburg · en · arbeitsagentur · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_058 - scope `in_scope` (in-scope)

> Manufacturing Engineer Artificial Intelligence (all gender)

- ALTEN GmbH München · Manufacturing Engineer Artificial Intelligence (all gender)
- Hamburg · de · arbeitsagentur · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_059 - scope `in_scope` (in-scope)

> Allgemein:Daten sind das Gold von morgen! Und Du suchst, förderst und veredelst das Wertvollste, was unsere Kundenbesitzen: Ihre Daten. Dahe

- DYMATRIX GmbH · Senior AI Data Engineer (all genders)
- Hamburg · de · arbeitsagentur · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_060 - scope `in_scope` (in-scope)

> Cloud Platform Engineer (m/w/d) Kubernetes / STACKIT / AI Platform Operations (Hamburg oder Mainz)

- dtms GmbH · Cloud Platform Engineer (m/w/d) Kubernetes / STACKIT / AI Platform Operations (Hamburg oder Mainz)
- Hamburg · de · arbeitsagentur · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_061 - scope `in_scope` (in-scope)

> Public Cloud Engineer (m/w/d) Schwerpunkt Generative AI

- SIGNAL IDUNA Krankenversicherung a. G. · Public Cloud Engineer (m/w/d) Schwerpunkt Generative AI
- Hamburg · de · arbeitsagentur · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_062 - scope `in_scope` (in-scope)

> Azure DevOps Engineer mit Fokus Azure AI (a*)

- Hamburger Energienetze GmbH · Azure DevOps Engineer mit Fokus Azure AI (a*)
- Hamburg · de · arbeitsagentur · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_051 - skill `full-stack-development` (disagreement)

> (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) -...

- A: (did not label this)
- B: `full-stack-development` · required · raw_text: "Fullstack Software Engineer"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 16. golden_052 - attribute `degree` (disagreement)

> ...Nutzer bis Geschäftsführung) **Das bringen Sie mit** * Abgeschlossener technischer Bildungsweg in Bereichen wie Informatik, Data Science, Artificial...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="Abgeschlossener technischer Bildungsweg"
- B: value=null · requirement=null · or_equivalent=false · signal=null

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_054 - skill `ai-ml` (disagreement)

> ...mit Python, davon mindestens ein Jahr in KI-Projekten, die produktiv gegangen sind. Dazu ein Studium der Data...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "KI-Projekten"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_055 - skill `cybersecurity` (disagreement)

> ...mit agilen Methoden und agil geführten Projekten hast idealerweise Kenntnisse von Industriestandards, Sicherheitskonzepten, Richtlinien und regulatorischen Compliance-Anforderungen...

- A: (did not label this)
- B: `cybersecurity` · nice_to_have · raw_text: "hast idealerweise Kenntnisse von Industriestandards, Sicherheitskonzepten"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_057 - skill `rag` (disagreement)

> ...or applied AI engineering • Hands-on experience with LLMs, retrieval and evaluation in production • Strong Python • Experience with document processing or...

- A: `rag` · required · raw_text: "LLMs, retrieval and evaluation in production"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_059 - skill `ai-ml` (disagreement)

> ...Ihre Daten. Daher suchen wir Dich als Senior AI Data Engineer (all genders) für unsere Standorte in...

- A: (did not label this)
- B: `ai-ml` · nice_to_have · raw_text: "AI"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_061 - attribute `seniority` (disagreement)

> ...vorzugsweise GCP) und Terraform (IaC) - verfügst über erste Erfahrungen in der Entwicklung, Bereitstellung und Integration von...

- A: value=null · basis=null · signal=null
- B: value="junior" · basis="inferred" · signal="erste Erfahrungen"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_061 - skill `ai-deployment` (disagreement)

> ...verfügst über erste Erfahrungen in der Entwicklung, Bereitstellung und Integration von Generative AI-Anwendungen im Unternehmenskontext, durch den Aufbau geeigneter...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "Bereitstellung und Integration von Generative AI-Anwendungen"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_062 - attribute `seniority` (disagreement)

> ...mit Terraform und Azure DevOps. * Idealerweise bringst du nachweisbare Erfahrung im Umgang mit dem Microsoft Azure AI Stack, insbesondere...

- A: value=null · basis=null · signal=null
- B: value="mid" · basis="inferred" · signal="nachweisbare Erfahrung"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_062 - skill `active-directory` (disagreement)

> ...DevOps Spezialist gehören Azure DevOps, Git, Terraform, Entra ID, Key Vaults, Private Endpoints, Networking, Landing Zones...

- A: `active-directory` · required · raw_text: "Entra ID"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_062 - skill `openai-api` (disagreement)

> ...von Azure-Ressourcen mit Terraform und Azure DevOps. * Idealerweise bringst du nachweisbare Erfahrung im Umgang mit dem Microsoft Azure AI Stack, insbesondere Azure OpenAI, AI Foundry, Cognitive Services, AI Search und Azure...

- A: `openai-api` · nice_to_have · raw_text: "Idealerweise bringst du nachweisbare Erfahrung im Umgang mit dem Microsoft Azure AI Stack, insbesondere Azure OpenAI"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_049 - attribute `seniority` (uncertain)

> Generative AI Engineer (all gender)

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 27. golden_050 - attribute `seniority` (uncertain)

> System Platform Engineer KI (m/w/d)

- A: value=null · basis=null · signal=null
- B: value=null · basis=null · signal=null

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 28. golden_050 - skill `cloud` (uncertain)

> ...sind von Vorteil. - Erfahrung in der netzwerkseitigen Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke - Praxiserfahrung im Einsatz von Coding Agents (z.B....

- A: `cloud` · required · raw_text: "Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke"
- B: `cloud` · required · raw_text: "Erfahrung in der netzwerkseitigen Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 29. golden_050 - skill `networking` (uncertain)

> ...Lake Storage Gen2), sind von Vorteil. - Erfahrung in der netzwerkseitigen Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke - Praxiserfahrung im Einsatz von Coding Agents (z.B....

- A: `networking` · required · raw_text: "netzwerkseitigen Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke"
- B: `networking` · required · raw_text: "Erfahrung in der netzwerkseitigen Anbindung von Cloud-Umgebungen an Unternehmensnetzwerke"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 30. golden_051 - attribute `degree` (uncertain)

> ...auf mind. C1-Niveau und gute Englischkenntnisse. Optional: Ein abgeschlossenes Hochschulstudium in (Wirtschafts-) Informatik oder eine vergleichbare Ausbildung sind von Vorteil. Du erfüllst nicht alle Qualifikationen 100%? Kein Problem...

- A: value="bachelor" · requirement="nice_to_have" · or_equivalent=true · signal="Optional: Ein abgeschlossenes Hochschulstudium in (Wirtschafts-) Informatik oder eine vergleichbare Ausbildung sind von Vorteil"
- B: value="bachelor" · requirement="nice_to_have" · or_equivalent=true · signal="Optional: Ein abgeschlossenes Hochschulstudium in (Wirtschafts-) Informatik oder eine vergleichbare Ausbildung sind von Vorteil."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 31. golden_051 - attribute `seniority` (uncertain)

> (Senior) Fullstack Software Engineer - Fokus AI (m/w/d) -...

- A: value="senior" · basis="stated" · signal="(Senior) Fullstack Software Engineer"
- B: value="senior" · basis="stated" · signal="(Senior)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 32. golden_051 - skill `cloud` (uncertain)

> ...mit Java (Spring Boot) sowie im Frontend mit Angular. Fundierte Kenntnisse in Cloud-nativen Architekturen, Kubernetes, Docker und idealerweise Cloud Foundry....

- A: `cloud` · required · raw_text: "Fundierte Kenntnisse in Cloud-nativen Architekturen"
- B: `cloud` · required · raw_text: "Cloud-nativen Architekturen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 33. golden_052 - skill `ai-ml` (uncertain)

> ...einer vergleichbaren Fachrichtung * Berufserfahrung in der Entwicklung, Umsetzung und im Betrieb von KI-Lösungen (Agenten, Workflows, API-Integrationen) *...

- A: `ai-ml` · required · raw_text: "Entwicklung, Umsetzung und im Betrieb von KI-Lösungen"
- B: `ai-ml` · required · raw_text: "KI-Lösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 34. golden_052 - skill `workflow-automation` (uncertain)

> ...Umsetzung und im Betrieb von KI-Lösungen (Agenten, Workflows, API-Integrationen) * Anwenderkenntnisse in Low-Code/No-Code-Plattformen (z....

- A: `workflow-automation` · required · raw_text: "Workflows, API-Integrationen"
- B: `workflow-automation` · required · raw_text: "Workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 35. golden_053 - skill `ai-ml` (uncertain)

> ...Berufserfahrung in oben genannten Aufgaben** - **Mindestens ein selbst technisch umgesetztes KI-Projekt** - Fundierte DevOps- und Cloud-Erfahrung - Praktische...

- A: `ai-ml` · required · raw_text: "Mindestens ein selbst technisch umgesetztes KI-Projekt"
- B: `ai-ml` · required · raw_text: "KI-Projekt"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 36. golden_053 - skill `apis` (uncertain)

> ...LLM- und Generative-AI-Lösungen - Technische Anbindung von KI-Services über APIs - Weiterentwicklung von Datenbankarchitekturen,...

- A: `apis` · required · raw_text: "Anbindung von KI-Services über APIs"
- B: `apis` · required · raw_text: "APIs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_053 - skill `ci-cd` (uncertain)

> ...Plattformumgebungen - Konzeption und Automatisierung von CI/CD-Pipelines - Umsetzung von Infrastructure as Code und Cloud-native...

- A: `ci-cd` · required · raw_text: "CI/CD-Pipelines"
- B: `ci-cd` · required · raw_text: "CI/CD-Pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_053 - skill `containerization` (uncertain)

> ...Cloud-native Architekturen - Betrieb und Weiterentwicklung containerisierter Umgebungen mit Docker, Kubernetes oder OpenShift - Umsetzung von...

- A: `containerization` · required · raw_text: "containerisierter Umgebungen"
- B: `containerization` · required · raw_text: "containerisierter Umgebungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_053 - skill `docker` (uncertain)

> ...und Weiterentwicklung containerisierter Umgebungen mit Docker, Kubernetes oder OpenShift - Umsetzung von...

- A: `docker` · required · raw_text: "Docker"
- B: `docker` · required · raw_text: "Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_053 - skill `infrastructure-as-code` (uncertain)

> ...und Automatisierung von CI/CD-Pipelines - Umsetzung von Infrastructure as Code und Cloud-native Architekturen - Betrieb und...

- A: `infrastructure-as-code` · required · raw_text: "Infrastructure as Code"
- B: `infrastructure-as-code` · required · raw_text: "Infrastructure as Code"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_053 - skill `kubernetes` (uncertain)

> ...Weiterentwicklung containerisierter Umgebungen mit Docker, Kubernetes oder OpenShift - Umsetzung von...

- A: `kubernetes` · required · raw_text: "Kubernetes"
- B: `kubernetes` · required · raw_text: "Kubernetes"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_053 - skill `llms` (uncertain)

> ...Integration von KI-, Machine-Learning-, LLM- und Generative-AI-Lösungen - Technische Anbindung von KI-Services über APIs -...

- A: `llms` · required · raw_text: "LLM- und Generative-AI-Lösungen"
- B: `llms` · required · raw_text: "Generative-AI-Lösungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_053 - skill `machine-learning` (uncertain)

> ...im gesamten Software-Lifecycle - Integration von KI-, Machine-Learning-, LLM- und Generative-AI-Lösungen - Technische Anbindung...

- A: `machine-learning` · required · raw_text: "Machine-Learning-"
- B: `machine-learning` · required · raw_text: "Machine-Learning-"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_053 - skill `observability` (uncertain)

> ...und Performance-Optimierungen - Aufbau und Optimierung von Monitoring-, Observability- und SRE-Strukturen - Zusammenarbeit mit Entwicklung,...

- A: `observability` · required · raw_text: "Monitoring-, Observability-"
- B: `observability` · required · raw_text: "Observability-"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_054 - skill `agents` (uncertain)

> ...Dokumentenverarbeitung (etwa Azure Document Intelligence), Agentic AI oder DevSecOps mit Kubernetes und Terraform. ## Warum zur...

- A: `agents` · nice_to_have · raw_text: "Agentic AI"
- B: `agents` · nice_to_have · raw_text: "Agentic AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_054 - skill `apis` (uncertain)

> ...Prompt Engineering, Retrieval-Augmented Generation und die Anbindung von Modellen über APIs, mit LangChain oder einer vergleichbaren Bibliothek. Sie...

- A: `apis` · required · raw_text: "Anbindung von Modellen über APIs"
- B: `apis` · required · raw_text: "Anbindung von Modellen über APIs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_055 - attribute `seniority` (uncertain)

> ...Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in der Entwicklung, Bereitstellung und Integration...

- A: value="junior" · basis="inferred" · signal="verfügst über erste Erfahrungen"
- B: value="junior" · basis="inferred" · signal="erste Erfahrungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_055 - skill `ai-deployment` (uncertain)

> ...(IaC) verfügst über erste Erfahrungen in der Entwicklung, Bereitstellung und Integration von Generative AI-Anwendungen im Unternehmenskontext, durch den Aufbau geeigneter...

- A: `ai-deployment` · required · raw_text: "Bereitstellung und Integration von Generative AI-Anwendungen"
- B: `ai-deployment` · required · raw_text: "Bereitstellung und Integration von Generative AI-Anwendungen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_056 - attribute `degree` (uncertain)

> ...you are - Soon-to-be/recent Graduate (2026/2027) with a relevant Master’s Degree in Computer Science, IT, Business Informatics or similar (or Bachelor's + ≥2yrs of full-time experience) - Full business-level fluency in English - Some hands-on...

- A: value="master" · requirement="required" · or_equivalent=false · signal="relevant Master’s Degree in Computer Science, IT, Business Informatics or similar (or Bachelor's + ≥2yrs of full-time experience)"
- B: value="master" · requirement="required" · or_equivalent=false · signal="Master’s Degree in Computer Science, IT, Business Informatics or similar (or Bachelor's + ≥2yrs of full-time experience)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_056 - skill `cloud` (uncertain)

> ...Fullstack Development, Backend, Data Engineering, Cloud Solutions, Architecture, Web Development, DevOps, and more. Instead...

- A: `cloud` · required · raw_text: "Cloud Solutions"
- B: `cloud` · required · raw_text: "Cloud Solutions"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_056 - skill `software-architecture` (uncertain)

> ...Development, Backend, Data Engineering, Cloud Solutions, Architecture, Web Development, DevOps, and more. Instead of predefined...

- A: `software-architecture` · required · raw_text: "Architecture"
- B: `software-architecture` · required · raw_text: "Architecture"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_057 - skill `ai-ml` (uncertain)

> ...team What you bring • 3+ years in machine learning or applied AI engineering • Hands-on experience with LLMs, retrieval and evaluation...

- A: `ai-ml` · required · raw_text: "applied AI engineering"
- B: `ai-ml` · required · raw_text: "applied AI engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_058 - attribute `seniority` (uncertain)

> ...Digitalisierung und technologische Innovationen - bringst erste praktische Berührungspunkte mit AI-Anwendungen oder datengetriebenen Ansätzen mit -...

- A: value="junior" · basis="inferred" · signal="erste praktische Berührungspunkte"
- B: value="junior" · basis="inferred" · signal="erste praktische Berührungspunkte mit AI-Anwendungen oder datengetriebenen Ansätzen"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_058 - skill `ai-ml` (uncertain)

> ...oder einer vergleichbaren Fachrichtung - verfügst über fundierte Kenntnisse im Bereich Artificial Intelligence und möchtest diese zur Gestaltung moderner Arbeitsabläufe...

- A: `ai-ml` · required · raw_text: "fundierte Kenntnisse im Bereich Artificial Intelligence"
- B: `ai-ml` · required · raw_text: "fundierte Kenntnisse im Bereich Artificial Intelligence"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_059 - attribute `german` (uncertain)

> ...gesammelt – kein Muss, aber ein starkes Plus • Sehr gutes Deutsch, gutes Englisch und ein ordentliches Maß an...

- A: value="nice_to_have" · basis="stated" · signal="Sehr gutes Deutsch"
- B: value="nice_to_have" · basis="stated" · signal="Sehr gutes Deutsch"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_059 - skill `azure` (uncertain)

> ...vorzugsweise im Beratungsumfeld • Gute Kenntnisse rund um die Azure Data Dienste wie z. B. Data Factory, SQL DB, Data Lake Storage,...

- A: `azure` · nice_to_have · raw_text: "Gute Kenntnisse rund um die Azure Data Dienste"
- B: `azure` · nice_to_have · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_059 - skill `business-intelligence` (uncertain)

> ...Functions sowie Interesse an Microsoft Foundry • Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture • Idealerweise hast Du schon erste...

- A: `business-intelligence` · nice_to_have · raw_text: "Interesse an der Entwicklung von DWH / Data Lake und BI"
- B: `business-intelligence` · nice_to_have · raw_text: "Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_059 - skill `cloud` (uncertain)

> ...Functions sowie Interesse an Microsoft Foundry • Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture • Idealerweise hast Du schon erste Erfahrungen mit...

- A: `cloud` · nice_to_have · raw_text: "Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture"
- B: `cloud` · nice_to_have · raw_text: "Starkes Interesse an der Entwicklung von DWH / Data Lake und BI Cloud Architecture"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_059 - skill `databricks` (uncertain)

> ...Dienste wie z. B. Data Factory, SQL DB, Data Lake Storage, Databricks, Functions sowie Interesse an Microsoft Foundry • Starkes...

- A: `databricks` · nice_to_have · raw_text: "Databricks"
- B: `databricks` · nice_to_have · raw_text: "Databricks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_060 - attribute `degree` (uncertain)

> ...und RBAC sowie DSGVO, ISO 27001 und C5 ### Dein Profil - Abgeschlossene IT-Ausbildung oder abgeschlossenes Studium der (Wirtschafts-)Informatik oder vergleichbar - Fundierte Erfahrung im Aufbau und Betrieb von...

- A: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene IT-Ausbildung oder abgeschlossenes Studium der (Wirtschafts-)Informatik oder vergleichbar"
- B: value="bachelor" · requirement="required" · or_equivalent=true · signal="Abgeschlossene IT-Ausbildung oder abgeschlossenes Studium der (Wirtschafts-)Informatik oder vergleichbar"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_060 - skill `cybersecurity` (uncertain)

> ...wie PostgreSQL oder MongoDB - Gutes Verständnis für Kubernetes- und Cloud-Security, insbesondere IAM/RBAC, Network Policies, Secrets...

- A: `cybersecurity` · required · raw_text: "Kubernetes- und Cloud-Security"
- B: `cybersecurity` · required · raw_text: "Kubernetes- und Cloud-Security"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_061 - skill `gcp` (uncertain)

> ...Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) - verfügst über erste Erfahrungen in...

- A: `gcp` · nice_to_have · raw_text: "vorzugsweise GCP"
- B: `gcp` · nice_to_have · raw_text: "vorzugsweise GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_049 - attribute `degree` (spot-check)

> ...our forward thinker DU... - verfügst über ein abgeschlossenes Studium der Informatik, Ingenieurinformatik, Data Science oder einer vergleichbaren Fachrichtung - bringst fundierte Erfahrung in der Entwicklung von...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="abgeschlossenes Studium der Informatik, Ingenieurinformatik, Data Science oder einer vergleichbaren Fachrichtung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 64. golden_049 - attribute `german` (spot-check)

> ...mit Docker, Kubernetes und CI/CD-Pipelines - verfügst über sehr gute Deutsch- und Englischkenntnisse A home where people learn and thrive -...

- agreed label: value="required" · basis="stated" · signal="sehr gute Deutsch- und Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 65. golden_049 - skill `langchain` (spot-check)

> ...in Python sowie Erfahrung mit Frameworks wie LangChain, PyTorch und TensorFlow - besitzt Kenntnisse im Bereich...

- agreed label: `langchain` · required · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 66. golden_049 - skill `llms` (spot-check)

> ...bringst fundierte Erfahrung in der Entwicklung von Generative-AI-, LLM- und RAG-Lösungen mit - hast sehr gute...

- agreed label: `llms` · required · raw_text: "Generative-AI-, LLM-"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 67. golden_049 - skill `mlops` (spot-check)

> ...Frameworks wie LangChain, PyTorch und TensorFlow - besitzt Kenntnisse im Bereich MLOps, Containerisierung und Orchestrierung mit Docker,...

- agreed label: `mlops` · required · raw_text: "Kenntnisse im Bereich MLOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 68. golden_049 - skill `python` (spot-check)

> ...RAG-Lösungen mit - hast sehr gute Programmierkenntnisse in Python sowie Erfahrung mit Frameworks wie LangChain, PyTorch und...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 69. golden_049 - skill `pytorch` (spot-check)

> ...in Python sowie Erfahrung mit Frameworks wie LangChain, PyTorch und TensorFlow - besitzt Kenntnisse im Bereich MLOps,...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 70. golden_049 - skill `rag` (spot-check)

> ...Erfahrung in der Entwicklung von Generative-AI-, LLM- und RAG-Lösungen mit - hast sehr gute Programmierkenntnisse in Python sowie...

- agreed label: `rag` · required · raw_text: "RAG-Lösungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 71. golden_049 - skill `tensorflow` (spot-check)

> ...sowie Erfahrung mit Frameworks wie LangChain, PyTorch und TensorFlow - besitzt Kenntnisse im Bereich MLOps, Containerisierung...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 72. golden_050 - skill `claude-code` (spot-check)

> ...Praxiserfahrung im Einsatz von Coding Agents (z.B. Claude Code oder Codex) sowie ein gutes Verständnis für modernes...

- agreed label: `claude-code` · required · raw_text: "z.B. Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 73. golden_050 - skill `codex` (spot-check)

> ...Praxiserfahrung im Einsatz von Coding Agents (z.B. Claude Code oder Codex) sowie ein gutes Verständnis für modernes AI-assisted...

- agreed label: `codex` · required · raw_text: "z.B. Claude Code oder Codex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 74. golden_050 - skill `data-pipelines` (spot-check)

> ...Informatik oder eine vergleichbare Qualifikation. - Interesse daran, Dichin moderne Data- und Cloud Technologien einzuarbeiten, insbesondere im Umfeld von Azure Machine Learning, Public Cloud, Data Factory/ Synapse Pipeline sowie Data Ingestion (ETL/ELT). - Erfahrung im Erstellen und Debuggen von Docker-Images...

- agreed label: `data-pipelines` · nice_to_have · raw_text: "Interesse daran, Dichin moderne Data- und Cloud Technologien einzuarbeiten, insbesondere im Umfeld von Azure Machine Learning, Public Cloud, Data Factory/ Synapse Pipeline sowie Data Ingestion (ETL/ELT)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 75. golden_050 - skill `python` (spot-check)

> ...und Debuggen von Docker-Images sowie im Umgang mit Terraform und Python. - Kenntnisse in Azure-Infrastrukturen und - Services,...

- agreed label: `python` · required · raw_text: "Terraform und Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 76. golden_051 - skill `ai-developer-tooling` (spot-check)

> ...von AI-gestützten Entwicklungsansätzen (z. B. Copilot, Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und...

- agreed label: `ai-developer-tooling` · required · raw_text: "Agentic Coding)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 77. golden_051 - skill `ci-cd` (spot-check)

> ...B. Copilot, Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und Observability-Standards. Ein agiles Mindset, hohes Qualitätsbewusstsein sowie...

- agreed label: `ci-cd` · required · raw_text: "CI/CD und Observability-Standards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 78. golden_051 - skill `devops` (spot-check)

> ...(z. B. Copilot, Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und Observability-Standards. Ein agiles Mindset,...

- agreed label: `devops` · required · raw_text: "DevOps-Prozessen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 79. golden_051 - skill `docker` (spot-check)

> ...Fundierte Kenntnisse in Cloud-nativen Architekturen, Kubernetes, Docker und idealerweise Cloud Foundry. Erfahrung mit Microservices, RESTful APIs sowie...

- agreed label: `docker` · required · raw_text: "Kubernetes, Docker und idealerweise Cloud Foundry"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 80. golden_051 - skill `github-copilot` (spot-check)

> ...im Einsatz von AI-gestützten Entwicklungsansätzen (z. B. Copilot, Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und...

- agreed label: `github-copilot` · required · raw_text: "(z. B. Copilot, Agentic Coding)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_051 - skill `java` (spot-check)

> ...Practices. Das bringst du mit Mehrjährige Erfahrung in der Softwareentwicklung mit Java (Spring Boot) sowie im Frontend mit Angular. Fundierte...

- agreed label: `java` · required · raw_text: "Softwareentwicklung mit Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_051 - skill `kubernetes` (spot-check)

> ...sowie im Frontend mit Angular. Fundierte Kenntnisse in Cloud-nativen Architekturen, Kubernetes, Docker und idealerweise Cloud Foundry. Erfahrung mit...

- agreed label: `kubernetes` · required · raw_text: "Cloud-nativen Architekturen, Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_051 - skill `microservices` (spot-check)

> ...Kubernetes, Docker und idealerweise Cloud Foundry. Erfahrung mit Microservices, RESTful APIs sowie Software-Architektur-Methoden (z. B....

- agreed label: `microservices` · required · raw_text: "Erfahrung mit Microservices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_051 - skill `observability` (spot-check)

> ...Agentic Coding). Know-how in DevOps-Prozessen, CI/CD und Observability-Standards. Ein agiles Mindset, hohes Qualitätsbewusstsein sowie...

- agreed label: `observability` · required · raw_text: "Observability-Standards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_051 - skill `software-architecture` (spot-check)

> ...Foundry. Erfahrung mit Microservices, RESTful APIs sowie Software-Architektur-Methoden (z. B. DDD, BDD, Arc42). Praktische Erfahrung im Einsatz...

- agreed label: `software-architecture` · required · raw_text: "Software-Architektur-Methoden"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_051 - skill `software-engineering` (spot-check)

> ...von Best Practices. Das bringst du mit Mehrjährige Erfahrung in der Softwareentwicklung mit Java (Spring Boot) sowie im Frontend mit Angular....

- agreed label: `software-engineering` · required · raw_text: "Erfahrung in der Softwareentwicklung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_052 - attribute `german` (spot-check)

> ...in MedTech oder weiteren regulierten Branchen * Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift **Das können Sie von uns erwarten** * Flexible...

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutsch- und Englischkenntnisse in Wort und Schrift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_052 - attribute `seniority` (spot-check)

> AI Engineer – KI-Enablement & Solutions (m/w/d)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_052 - skill `agents` (spot-check)

> ...in der Entwicklung, Umsetzung und im Betrieb von KI-Lösungen (Agenten, Workflows, API-Integrationen) * Anwenderkenntnisse in...

- agreed label: `agents` · required · raw_text: "KI-Lösungen (Agenten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_052 - skill `apis` (spot-check)

> ...und im Betrieb von KI-Lösungen (Agenten, Workflows, API-Integrationen) * Anwenderkenntnisse in Low-Code/No-Code-Plattformen (z....

- agreed label: `apis` · required · raw_text: "API-Integrationen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_052 - skill `data-privacy-and-security` (spot-check)

> ...Agenten-Orchestrierung) * Praktische Berührungen mit Datenschutzkonzepten und Informationssicherheit, idealerweise in regulierten Umfeldern (z. B....

- agreed label: `data-privacy-and-security` · required · raw_text: "Datenschutzkonzepten und Informationssicherheit"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_052 - skill `prompt-engineering` (spot-check)

> ...Studio, Power Automate, n8n) * Erweitertes Know-how im Prompt Engineering für den Enterprise-Einsatz (Systemprompts,...

- agreed label: `prompt-engineering` · required · raw_text: "Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_053 - skill `cybersecurity` (spot-check)

> ...KI-Projekt** - Fundierte DevOps- und Cloud-Erfahrung - Praktische Erfahrung im Bereich IT-Security - Bereitschaft zu vier Office-Tagen pro Woche in Hamburg -...

- agreed label: `cybersecurity` · required · raw_text: "Praktische Erfahrung im Bereich IT-Security"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_053 - skill `devops` (spot-check)

> ...ein selbst technisch umgesetztes KI-Projekt** - Fundierte DevOps- und Cloud-Erfahrung - Praktische Erfahrung im Bereich...

- agreed label: `devops` · required · raw_text: "Fundierte DevOps-"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_054 - attribute `seniority` (spot-check)

> ...oder halten einen Fachvortrag. ## Was Sie mitbringen - Mindestens drei Jahre Erfahrung in der Softwareentwicklung mit Python, davon mindestens ein Jahr in KI-Projekten, die produktiv...

- agreed label: value="mid" · basis="inferred" · signal="Mindestens drei Jahre Erfahrung in der Softwareentwicklung mit Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_054 - skill `aws` (spot-check)

> ...mit mindestens einer Cloud-Plattform wie Microsoft Azure, AWS oder Google Cloud. - Freude am direkten Austausch mit...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_054 - skill `azure` (spot-check)

> ...Dazu Erfahrung mit mindestens einer Cloud-Plattform wie Microsoft Azure, AWS oder Google Cloud. - Freude am direkten Austausch mit...

- agreed label: `azure` · required · raw_text: "Microsoft Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_054 - skill `gcp` (spot-check)

> ...einer Cloud-Plattform wie Microsoft Azure, AWS oder Google Cloud. - Freude am direkten Austausch mit Kunden, auch vor Ort,...

- agreed label: `gcp` · required · raw_text: "Google Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_054 - skill `kubernetes` (spot-check)

> ...Document Intelligence), Agentic AI oder DevSecOps mit Kubernetes und Terraform. ## Warum zur PTA? - KI als zentrale...

- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_054 - skill `langchain` (spot-check)

> ...Generation und die Anbindung von Modellen über APIs, mit LangChain oder einer vergleichbaren Bibliothek. Sie wissen, wie Sprachmodelle funktionieren, und...

- agreed label: `langchain` · required · raw_text: "mit LangChain oder einer vergleichbaren Bibliothek"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_054 - skill `llms` (spot-check)

> ...und Designentscheidungen die Performance beeinflussen. - Praxis mit großen Sprachmodellen: Prompt Engineering, Retrieval-Augmented Generation und...

- agreed label: `llms` · required · raw_text: "Praxis mit großen Sprachmodellen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_054 - skill `prompt-engineering` (spot-check)

> ...beeinflussen. - Praxis mit großen Sprachmodellen: Prompt Engineering, Retrieval-Augmented Generation und die Anbindung von...

- agreed label: `prompt-engineering` · required · raw_text: "Prompt Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_054 - skill `rag` (spot-check)

> ...Praxis mit großen Sprachmodellen: Prompt Engineering, Retrieval-Augmented Generation und die Anbindung von Modellen über APIs, mit LangChain...

- agreed label: `rag` · required · raw_text: "Retrieval-Augmented Generation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_054 - skill `sql` (spot-check)

> ...und verstehen deshalb auch, wo sie an Grenzen stoßen. - Sicherer Umgang mit SQL und unterschiedlichen Datenbanken. Dazu Erfahrung mit...

- agreed label: `sql` · required · raw_text: "Sicherer Umgang mit SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_054 - skill `testing` (spot-check)

> ...von objektorientierter Programmierung über automatisierte Tests bis zum Verständnis, wie Datenstrukturen, Algorithmen und...

- agreed label: `testing` · required · raw_text: "automatisierte Tests"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_055 - attribute `degree` (spot-check)

> ...Gesundheitsmanagement deine Gesundheit Du hast ein abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz hast Erfahrung im Bereich Public Cloud (AWS,...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_055 - skill `azure` (spot-check)

> ...hast Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über...

- agreed label: `azure` · required · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_055 - skill `gcp` (spot-check)

> ...hast Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in...

- agreed label: `gcp` · nice_to_have · raw_text: "vorzugsweise GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_055 - skill `infrastructure-as-code` (spot-check)

> ...Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in der Entwicklung,...

- agreed label: `infrastructure-as-code` · required · raw_text: "IaC"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_055 - skill `llms` (spot-check)

> ...in der Entwicklung, Bereitstellung und Integration von Generative AI-Anwendungen im Unternehmenskontext, durch den Aufbau geeigneter...

- agreed label: `llms` · required · raw_text: "Generative AI-Anwendungen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_055 - skill `terraform` (spot-check)

> ...im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) verfügst über erste Erfahrungen in der Entwicklung,...

- agreed label: `terraform` · required · raw_text: "Terraform (IaC)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_056 - attribute `german` (spot-check)

> Software Engineering /Data and AI Engineering/ IT-Management Consultant (2026/27 Graduate) (m/f/d)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_056 - skill `software-engineering` (spot-check)

> ...experience through internships, working student roles or full-time in Software Engineering, Data Engineering or IT-Management with modern...

- agreed label: `software-engineering` · required · raw_text: "full-time in Software Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_057 - attribute `seniority` (spot-check)

> ...together with the engineering team What you bring • 3+ years in machine learning or applied AI engineering • Hands-on experience with LLMs, retrieval and evaluation...

- agreed label: value="mid" · basis="inferred" · signal="3+ years in machine learning or applied AI engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_057 - skill `evaluation` (spot-check)

> ...engineering • Hands-on experience with LLMs, retrieval and evaluation in production • Strong Python • Experience with document processing or...

- agreed label: `evaluation` · required · raw_text: "evaluation in production"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_057 - skill `machine-learning` (spot-check)

> ...together with the engineering team What you bring • 3+ years in machine learning or applied AI engineering • Hands-on experience with LLMs,...

- agreed label: `machine-learning` · required · raw_text: "3+ years in machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_058 - attribute `degree` (spot-check)

> ...und AI ### Be our forward thinker **DU…** - hast ein abgeschlossenes Studium in Maschinenbau, Produktionstechnik, Luft- und Raumfahrttechnik oder einer vergleichbaren Fachrichtung - verfügst über fundierte Kenntnisse im Bereich Artificial...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=false · signal="abgeschlossenes Studium in Maschinenbau, Produktionstechnik, Luft- und Raumfahrttechnik oder einer vergleichbaren Fachrichtung"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_058 - attribute `german` (spot-check)

> ...und gerne in interdisziplinären Teams - verfügst über sehr gute Deutsch- und Englischkenntnisse Wir wertschätzen Vielfalt und begrüßen daher alle...

- agreed label: value="required" · basis="stated" · signal="sehr gute Deutsch- und Englischkenntnisse"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_059 - attribute `degree` (spot-check)

> Allgemein:Daten sind das Gold von morgen! Und Du suchst, förderst und veredelst das Wertvollste, was unsere Kundenbesitzen: Ihre Daten. Dahe

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_060 - attribute `german` (spot-check)

> ...Betriebsstandards mitzugestalten und zu optimieren - Sehr gute Deutsch- und gute Englischkenntnisse in Wort und Schrift ### Deine Benefits - Attraktives Fixgehalt zzgl....

- agreed label: value="required" · basis="stated" · signal="Sehr gute Deutsch- und gute Englischkenntnisse in Wort und Schrift"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_060 - attribute `seniority` (spot-check)

> Cloud Platform Engineer (m/w/d) Kubernetes / STACKIT / AI Platform Operations (Hamburg oder Mainz)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_060 - skill `ci-cd` (spot-check)

> ...Umfangreiche Kenntnisse in Cloud-Infrastrukturen, CI/CD, Container-Technologien, automatisierten Deployments sowie Infrastructure as Code...

- agreed label: `ci-cd` · required · raw_text: "CI/CD, Container-Technologien"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_060 - skill `cloud` (spot-check)

> ...STACKIT SKE, AKS, EKS, GKE oder OpenShift - Umfangreiche Kenntnisse in Cloud-Infrastrukturen, CI/CD, Container-Technologien, automatisierten...

- agreed label: `cloud` · required · raw_text: "Kenntnisse in Cloud-Infrastrukturen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_060 - skill `gitops` (spot-check)

> ...Container-Technologien, automatisierten Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit...

- agreed label: `gitops` · required · raw_text: "Infrastructure as Code und GitOps, z. B."

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_060 - skill `helm` (spot-check)

> ...as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit Monitoring, Logging und...

- agreed label: `helm` · required · raw_text: "Helm"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_060 - skill `infrastructure-as-code` (spot-check)

> ...CI/CD, Container-Technologien, automatisierten Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder...

- agreed label: `infrastructure-as-code` · required · raw_text: "sowie Infrastructure as Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_060 - skill `postgresql` (spot-check)

> ...Erfahrung mit Monitoring, Logging und Alerting sowie idealerweise mit dem Betrieb zentraler Plattform- und Datenservices wie PostgreSQL oder MongoDB - Gutes Verständnis für Kubernetes- und...

- agreed label: `postgresql` · nice_to_have · raw_text: "idealerweise mit dem Betrieb zentraler Plattform- und Datenservices wie PostgreSQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_060 - skill `terraform` (spot-check)

> ...Deployments sowie Infrastructure as Code und GitOps, z. B. Terraform, Argo CD, Helm oder Kustomize - Erfahrung mit Monitoring,...

- agreed label: `terraform` · required · raw_text: "z. B. Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_061 - attribute `degree` (spot-check)

> ...deine Gesundheit **Du** - hast ein abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation mit IT-Kompetenz - hast einschlägige Erfahrung im Bereich...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="abgeschlossenes IT-Studium oder eine vergleichbare Qualifikation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_061 - skill `aws` (spot-check)

> ...hast einschlägige Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) - verfügst...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_061 - skill `azure` (spot-check)

> ...hast einschlägige Erfahrung im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) - verfügst über...

- agreed label: `azure` · required · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_061 - skill `ci-cd` (spot-check)

> ...Infrastruktur-Komponenten auf Basis von Terraform (CI/CD-Pipeline) - bringst Erfahrungen im Umgang mit...

- agreed label: `ci-cd` · required · raw_text: "CI/CD-Pipeline"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_061 - skill `cloud` (spot-check)

> Public Cloud Engineer (m/w/d) Schwerpunkt Generative AI ### **Das sind...

- agreed label: `cloud` · required · raw_text: "Public Cloud"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_061 - skill `python` (spot-check)

> ...oder Bitbucket mit - bist vertraut mit dem Einsatz von Python als Programmiersprache - verfügst über praktische Erfahrungen mit agilen Methoden...

- agreed label: `python` · required · raw_text: "Python als Programmiersprache"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_061 - skill `terraform` (spot-check)

> ...im Bereich Public Cloud (AWS, Azure, vorzugsweise GCP) und Terraform (IaC) - verfügst über erste Erfahrungen in der Entwicklung,...

- agreed label: `terraform` · required · raw_text: "Terraform (IaC)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_062 - attribute `german` (spot-check)

> Azure DevOps Engineer mit Fokus Azure AI (a*)

- agreed label: value="required" · basis="inferred" · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_062 - skill `azure` (spot-check)

> ...und Pflege von Infrastructure-as-Code-Projekten zur Bereitstellung von Azure-Ressourcen mit Terraform und Azure DevOps. * Idealerweise bringst du...

- agreed label: `azure` · required · raw_text: "Bereitstellung von Azure-Ressourcen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_062 - skill `infrastructure-as-code` (spot-check)

> ...fundierte Kenntnisse in der Entwicklung und Pflege von Infrastructure-as-Code-Projekten zur Bereitstellung von Azure-Ressourcen mit Terraform und...

- agreed label: `infrastructure-as-code` · required · raw_text: "Infrastructure-as-Code-Projekten"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_062 - skill `networking` (spot-check)

> ...Git, Terraform, Entra ID, Key Vaults, Private Endpoints, Networking, Landing Zones sowie Monitoring zu deinem täglichen...

- agreed label: `networking` · required · raw_text: "Networking"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_062 - skill `observability` (spot-check)

> ...Key Vaults, Private Endpoints, Networking, Landing Zones sowie Monitoring zu deinem täglichen Handwerkszeug. * Zudem verfügst du...

- agreed label: `observability` · required · raw_text: "sowie Monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_062 - skill `rag` (spot-check)

> ...im Einsatz von Large Language Models (LLMs) sowie RAG-Technologien und -Architekturen sind von Vorteil. Was uns...

- agreed label: `rag` · nice_to_have · raw_text: "RAG-Technologien"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_062 - skill `terraform` (spot-check)

> ...Infrastructure-as-Code-Projekten zur Bereitstellung von Azure-Ressourcen mit Terraform und Azure DevOps. * Idealerweise bringst du nachweisbare...

- agreed label: `terraform` · required · raw_text: "Azure-Ressourcen mit Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
