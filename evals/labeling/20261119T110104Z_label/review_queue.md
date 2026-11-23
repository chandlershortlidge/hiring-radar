# Review queue - 20261119T110104Z_label

127 items from 9 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T110104Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 114 accepted labels,
seed 0) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong. They print the posting
excerpt and the agreed label only - no `A:`/`B:` lines - so you check the label against the
posting rather than against the labelers, who by construction both said the same thing.

The first 9 items ask whether each posting belongs in the held-out set at all.
They come pre-answered `yes`, so leaving them alone keeps every posting. Answer `no <why>`
and that posting is written to `evals/goldens/excluded.json` with your reason instead of
becoming a Golden, and neither this script nor `new_goldens.py` will pick it again. Use it
for a posting that got past the title and city filters but is not the job market we
measure - a marketing role, a listing in the wrong field. The rest of that posting's items
are then ignored, so you can answer `no` and skip them.

## 1. golden_094 - scope `in_scope` (in-scope)

> Senior ML Engineer

- flagshippioneeringinc · Senior ML Engineer
- Boston · en · greenhouse · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> Scientist, Machine Learning (Human Physiology)

- flagshippioneeringinc · Scientist, Machine Learning (Human Physiology)
- Boston · en · greenhouse · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> Principal Software Engineer - Agentic Platform

- flagshippioneeringinc · Principal Software Engineer - Agentic Platform
- Boston · en · greenhouse · 19 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> Principal AI Scientist, Autonomous Discovery

- flagshippioneeringinc · Principal AI Scientist, Autonomous Discovery
- Boston · en · greenhouse · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> Principal Scientist, Machine Learning

- flagshippioneeringinc · Principal Scientist, Machine Learning
- Boston · en · greenhouse · 20 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> (Senior) Scientist, Machine Learning

- flagshippioneeringinc · (Senior) Scientist, Machine Learning
- Boston · en · greenhouse · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> Principal Scientist, Machine Learning - Multimodal Biological Reasoning

- flagshippioneeringinc · Principal Scientist, Machine Learning - Multimodal Biological Reasoning
- Boston · en · greenhouse · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> Principal Scientist, Machine Learning - Biomolecules

- flagshippioneeringinc · Principal Scientist, Machine Learning - Biomolecules
- Boston · en · greenhouse · 27 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> Senior Machine Learning Scientist, Climate & Hydrology

- flagshippioneeringinc · Senior Machine Learning Scientist, Climate & Hydrology
- Boston · en · greenhouse · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_094 - skill `ai-deployment` (disagreement)

> ...and natural language processing (NLP) - Proven experience deploying LLM-powered applications in production environments, including experience with frameworks such as PyTorch,...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying LLM-powered applications in production environments"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualifications line "Proven experience deploying LLM-powered applications in production environments" names the skill as a required qualification, and rule 3 makes that required mention decisive, so labeler B's ai-deployment tag stands.

DECISION: B

## 11. golden_095 - skill `agents` (disagreement)

> ...and interpretation. FL127 is an AI-native company. Team members direct AI agents in their daily work for literature synthesis, study design, data analysis, and code. We are looking for someone who wants to work this way. KEY RESPONSIBILITIES - Ground each measured signal in...

- A: (did not label this)
- B: `agents` · nice_to_have · raw_text: "Team members direct AI agents in their daily work for literature synthesis, study design, data analysis, and code. We are looking for someone who wants to work this way."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 12. golden_096 - skill `software-architecture` (disagreement)

> ...development experience. - Demonstrated track record architecting and maintaining large-scale distributed systems in production at technology companies. -...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "architecting and maintaining large-scale distributed systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under Rule 1, the qualification bullet "Demonstrated track record architecting and maintaining large-scale distributed systems" names the skill as a required qualification, and Labeler A did not label it, so B's required tag with that raw_text stands (Rule 3).

DECISION: B

## 13. golden_096 - skill `software-engineering` (disagreement)

> ...Engineering, or a related field, with 10+ years of professional software development experience. - Demonstrated track record architecting...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "professional software development experience"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only mention is inside the years-of-experience line "10+ years of professional software development experience", which does not count, and rule 5 bars adding the broad parent skill from the surrounding distributed-systems and architecture bullets.

DECISION: drop

## 14. golden_098 - skill `machine-learning` (disagreement)

> ...across multiple core tools and concepts, including Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version control; databases;...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "modern ML frameworks"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualifications name ML work ("progression of AI/ML models" and "modern ML frameworks" in the required list), so machine-learning is a required skill and labeler B's version stands, with its quoted raw_text appearing in the posting.

DECISION: B

## 15. golden_100 - skill `data-science` (disagreement)

> ...biology, AI-for-biology, AI-enabled drug discovery, translational data science, biological foundation models, or scientific discovery...

- A: (did not label this)
- B: `data-science` · required · raw_text: "translational data science"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under Qualifications, the bullet 'Deep experience in ... translational data science' names data science as a required qualification, so rules 1 and 3 support B's required tag, and the text is specific enough that rule 5 does not block it.

DECISION: B

## 16. golden_100 - skill `hallucination-detection` (disagreement)

> ...biology, scientific credibility, model limitations, hallucination risk, interpretability, and validation. - Experience leading...

- A: `hallucination-detection` · required · raw_text: "hallucination risk"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_100 - skill `machine-learning` (disagreement)

> ...learning, fine-tuning, post-training, benchmarking, and ML systems. - Deep experience in computational biology,...

- A: `machine-learning` · required · raw_text: "ML systems"
- B: (did not label this)

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 1, the Qualifications bullet naming "ML systems" is a required skill mention, and the abbreviation "ML" points to machine-learning, so labeler A's required tag with raw_text "ML systems" stands.

DECISION: A

## 18. golden_101 - skill `agents` (disagreement)

> ...spec, cheminformatics/docking/ADMET, biophysics/MD, and LLM/agentic automation. - MLOps expertise: data contracts and lineage (e.g.,...

- A: `agents` · nice_to_have · raw_text: "LLM/agentic automation"
- B: `agents` · required · raw_text: "spin up LLM based agents"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3 only a verifiable required mention would override, and the only agents-related text visible is "LLM/agentic automation" under the Preferred Qualifications heading, so nice_to_have fits; B's quote "spin up LLM based agents" does not appear in the visible excerpt, which is cut off at "acting...", so it cannot be confirmed as a required mention.

DECISION: A

## 19. golden_101 - skill `llms` (disagreement)

> ...spec, cheminformatics/docking/ADMET, biophysics/MD, and LLM/agentic automation. - MLOps expertise: data contracts and lineage (e.g.,...

- A: `llms` · nice_to_have · raw_text: "LLM/agentic automation"
- B: `llms` · required · raw_text: "spin up LLM based agents"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_101 - skill `workflow-automation` (disagreement)

> ...or docking pipelines the next and then spin up LLM based agents that automate scientific workflows. KEY RESPONSIBILITIES - Program Leadership: Lead...

- A: (did not label this)
- B: `workflow-automation` · required · raw_text: "agents that automate scientific workflows"

Options: `A` / `B` / `both` / `drop`

PROPOSED: {"requirement": "nice_to_have", "raw_text": "agents that automate scientific workflows"} - Under rule 1 the skill is named in a sentence describing the ideal candidate, so it counts, but under rule 3 the only mention is framed as 'ideal candidate' rather than a requirement, so it should be nice_to_have, not required.

DECISION: {"requirement": "nice_to_have", "raw_text": "agents that automate scientific workflows"}

## 21. golden_094 - skill `evaluation` (uncertain)

> ...tools for ML development, large-scale data pipelines, and standard evaluation protocols - Experience owning systems end-to-end in a production...

- A: `evaluation` · required · raw_text: "standard evaluation protocols"
- B: `evaluation` · required · raw_text: "standard evaluation protocols"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet "Proficiency in Python and tools for ML development, large-scale data pipelines, and standard evaluation protocols" names evaluation as a skill, and rule 3 supports the required label with the quoted raw_text "standard evaluation protocols", which appears verbatim in the posting.

DECISION: ok

## 22. golden_094 - skill `llm-orchestration` (uncertain)

> ...as PyTorch, vLLM, or LangGraph - Hands-on experience with RAG, agentic orchestration, or multi-agent systems is strongly preferred -...

- A: `llm-orchestration` · nice_to_have · raw_text: "RAG, agentic orchestration"
- B: `llm-orchestration` · nice_to_have · raw_text: "agentic orchestration, or multi-agent systems is strongly preferred"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 3, the agreed nice_to_have label with raw_text "RAG, agentic orchestration" is verbatim and matches the "strongly preferred" sentence; the only other candidate, LangGraph in the required deployment line, is a framework example not clearly named as orchestration, so I'm not overriding it under rules 3 or 5.

DECISION: ok

## 23. golden_094 - skill `observability` (uncertain)

> ...owning systems end-to-end in a production environment, including monitoring and iterating post-deployment - Self-motivated and...

- A: `observability` · required · raw_text: "including monitoring"
- B: `observability` · required · raw_text: "monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "Experience owning systems end-to-end in a production environment, including monitoring and iterating post-deployment" sits in the Professional Experience & Qualifications section and is not marked preferred, so the required observability mention stands and the quoted raw_text appears verbatim.

DECISION: ok

## 24. golden_096 - skill `ai-infrastructure` (uncertain)

> ...and monitoring tooling and cost-governance / FinOps for AI infrastructure. - Background in scientific domains such as biology,...

- A: `ai-infrastructure` · nice_to_have · raw_text: "FinOps for AI infrastructure"
- B: `ai-infrastructure` · nice_to_have · raw_text: "AI infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet names experience with cost-governance/FinOps for AI infrastructure, so the skill counts, and nice_to_have fits the preferred section with the raw_text quoted verbatim.

DECISION: ok

## 25. golden_096 - skill `api-design` (uncertain)

> ...operationally excellent production. - Experience designing SDKs, APIs, and data contracts that serve multiple downstream...

- A: `api-design` · required · raw_text: "designing SDKs, APIs"
- B: `api-design` · required · raw_text: "designing SDKs, APIs, and data contracts"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet "Experience designing SDKs, APIs, and data contracts" names designing APIs, which is the api-design skill (rule 2 does not apply because the candidate is building APIs, not consuming them), so the agreed label stands.

DECISION: ok

## 26. golden_096 - skill `cloud` (uncertain)

> ...execution, idempotency, durable retries, and replay. - Strong cloud-native engineering on AWS with infrastructure-as-code, containerization, and...

- A: `cloud` · required · raw_text: "Strong cloud-native engineering"
- B: `cloud` · required · raw_text: "cloud-native engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualifications bullet "Strong cloud-native engineering on AWS..." names cloud as a required skill, and the agreed raw_text quotes it verbatim, so the agreed label stands.

DECISION: ok

## 27. golden_096 - skill `observability` (uncertain)

> ...Proven ability to take systems from prototype to hardened, observable, operationally excellent production. - Experience designing SDKs, APIs, and data contracts...

- A: `observability` · required · raw_text: "hardened, observable, operationally excellent production"
- B: `observability` · required · raw_text: "observable"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet asks for a candidate who can take systems to production that are "observable", which names the observability skill, and rule 3 makes that required mention control.

DECISION: ok

## 28. golden_097 - skill `causal-inference` (uncertain)

> ...with 5+ years of experience post PhD. - Deep expertise in advanced Bayesian causal modeling and/or evolutionary programming — e.g., probabilistic...

- A: `causal-inference` · required · raw_text: "advanced Bayesian causal modeling"
- B: `causal-inference` · required · raw_text: "Bayesian causal modeling"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Qualifications bullet names "advanced Bayesian causal modeling" as a required expertise, and rule 3 keeps the required mention with its quoted raw_text, so the agreed label stands.

DECISION: ok

## 29. golden_098 - skill `ai-infrastructure` (uncertain)

> ...observability and monitoring tooling and cost-governance / FinOps for AI infrastructure. WHY PIONEERING INTELLIGENCE - Operate at the...

- A: `ai-infrastructure` · nice_to_have · raw_text: "FinOps for AI infrastructure"
- B: `ai-infrastructure` · nice_to_have · raw_text: "AI infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the PREFERRED QUALIFICATIONS bullet names experience with FinOps for AI infrastructure, the agreed raw_text is a verbatim substring, and nice_to_have fits the preferred section.

DECISION: ok

## 30. golden_098 - skill `ai-ml` (uncertain)

> ...of sustained independent thought and creativity driving high impact, cross disciplinary AI/ML projects. - Successful track record of leadership and...

- A: `ai-ml` · required · raw_text: "high impact, cross disciplinary AI/ML projects"
- B: `ai-ml` · required · raw_text: "cross disciplinary AI/ML projects"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1 the phrase sits in a qualifications bullet, and under rule 3 the required bullets also name AI/ML models and ML frameworks, so the required ai-ml tag with this raw_text is correct as agreed.

DECISION: ok

## 31. golden_098 - skill `cheminformatics` (uncertain)

> ...modeling/design, proteomics/mass spec, multi-omics, cheminformatics/docking/ADMET, biophysics/MD, and scientific literature mining, with the...

- A: `cheminformatics` · nice_to_have · raw_text: "cheminformatics/docking/ADMET"
- B: `cheminformatics` · nice_to_have · raw_text: "cheminformatics"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the PREFERRED QUALIFICATIONS bullet names cheminformatics explicitly as a domain the candidate should have breadth in, and the agreed raw_text "cheminformatics/docking/ADMET" appears verbatim in the posting, so the nice_to_have label stands.

DECISION: ok

## 32. golden_099 - attribute `seniority` (uncertain)

> (Senior) Scientist, Machine Learning What if… you could join an organization that creates,...

- A: value="senior" · basis="stated" · signal="(Senior) Scientist, Machine Learning"
- B: value="senior" · basis="stated" · signal="(Senior) Scientist, Machine Learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Rule 1 excludes job titles as skill evidence, but seniority is a level attribute rather than a skill, and the title's explicit "(Senior)" is the stated level, so the agreed value stands.

DECISION: ok

## 33. golden_099 - skill `chemical-descriptors` (uncertain)

> ...quantum chemistry, DFT, electronic structure methods, or post-DFT descriptors. - Experience building molecular ML models including...

- A: `chemical-descriptors` · required · raw_text: "post-DFT descriptors"
- B: `chemical-descriptors` · required · raw_text: "post-DFT descriptors"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualifications bullet "Experience with quantum chemistry, DFT, electronic structure methods, or post-DFT descriptors" names the skill as a required qualification (only the publications line is marked "a strong plus"), and rule 3 keeps the required mention with its quoted raw_text.

DECISION: ok

## 34. golden_099 - skill `cheminformatics` (uncertain)

> ...as PyTorch, PyTorch Geometric, DGL, or related tools and cheminformatics and molecular modeling toolkits such as RDKit, ORCA, Gaussian, Q-Chem, or related software...

- A: `cheminformatics` · nice_to_have · raw_text: "cheminformatics and molecular modeling toolkits"
- B: `cheminformatics` · nice_to_have · raw_text: "cheminformatics"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification sentence explicitly names cheminformatics toolkits, and the trailing "is preferred" applies to that whole list, so nice_to_have with the quoted raw_text is correct (rule 5 is not triggered because the skill is named directly).

DECISION: ok

## 35. golden_099 - skill `deep-learning` (uncertain)

> ...molecular ML models including graph neural networks, geometric deep learning, equivariant architectures, diffusion models, or related...

- A: `deep-learning` · required · raw_text: "geometric deep learning"
- B: `deep-learning` · required · raw_text: "geometric deep learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualifications bullet "Experience building molecular ML models including ... geometric deep learning" names the skill, and rule 3 makes that required mention determine the label, so the agreed required tag with that raw_text stands.

DECISION: ok

## 36. golden_099 - skill `model-development` (uncertain)

> ...is preferred - Experience with scalable data processing, model training, and analysis workflows for large scientific datasets -...

- A: `model-development` · required · raw_text: "model training"
- B: `model-development` · required · raw_text: "model training"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 3, the required qualification bullet "Experience with scalable data processing, model training, and analysis workflows" (not marked preferred) supports the required `model-development` label, and the raw_text "model training" appears verbatim in the posting.

DECISION: ok

## 37. golden_099 - skill `python` (uncertain)

> ...large-scale scientific datasets from multiple sources - Proficiency with Python and modern ML frameworks such as PyTorch, PyTorch...

- A: `python` · nice_to_have · raw_text: "Proficiency with Python"
- B: `python` · nice_to_have · raw_text: "Proficiency with Python and modern ML frameworks such as PyTorch, PyTorch Geometric, DGL, or related tools and cheminformatics and molecular modeling toolkits such as RDKit, ORCA, Gaussian, Q-Chem, or related software is preferred"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification bullet names Python, and the trailing "is preferred" applies to the whole sentence, so nice_to_have with raw_text "Proficiency with Python" (verbatim in the posting) is correct as agreed.

DECISION: ok

## 38. golden_099 - skill `pytorch` (uncertain)

> ...Proficiency with Python and modern ML frameworks such as PyTorch, PyTorch Geometric, DGL, or related tools and...

- A: `pytorch` · nice_to_have · raw_text: "PyTorch"
- B: `pytorch` · nice_to_have · raw_text: "PyTorch"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualifications sentence ('Proficiency with Python and modern ML frameworks such as PyTorch... is preferred') names PyTorch, and the 'preferred' wording supports nice_to_have, with raw_text 'PyTorch' appearing verbatim in the posting.

DECISION: ok

## 39. golden_099 - skill `rdkit` (uncertain)

> ...cheminformatics and molecular modeling toolkits such as RDKit, ORCA, Gaussian, Q-Chem, or related software is...

- A: `rdkit` · nice_to_have · raw_text: "RDKit"
- B: `rdkit` · nice_to_have · raw_text: "RDKit"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification bullet names RDKit as one of the toolkits for which experience is preferred, so the agreed nice_to_have label with raw_text "RDKit" is correct as it stands.

DECISION: ok

## 40. golden_100 - skill `agents` (uncertain)

> ...protein language models, genomic foundation models, scientific agents, or AI discovery platforms. - Experience working across...

- A: `agents` · required · raw_text: "scientific agents"
- B: `agents` · required · raw_text: "scientific agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Requirements (rule 1), the bullet names "scientific agents" as an accepted experience area, so the required `agents` label with that verbatim raw_text holds (rule 3).

DECISION: ok

## 41. golden_100 - skill `ai-deployment` (uncertain)

> ...serving multiple scientific programs. - Experience deploying AI/ML for biology systems into scientific workflows at...

- A: `ai-deployment` · required · raw_text: "deploying AI/ML"
- B: `ai-deployment` · required · raw_text: "deploying AI/ML for biology systems into scientific workflows at enterprise scale"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Requirements bullet "Experience deploying AI/ML for biology systems into scientific workflows at enterprise scale" is a qualification that names AI deployment, and the agreed raw_text "deploying AI/ML" appears verbatim, so the required label stands.

DECISION: ok

## 42. golden_100 - skill `ai-ml` (uncertain)

> ...multiple scientific programs. - Experience deploying AI/ML for biology systems into scientific workflows at enterprise scale. -...

- A: `ai-ml` · required · raw_text: "AI/ML for biology systems"
- B: `ai-ml` · required · raw_text: "AI/ML"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Requirements bullet 'Experience deploying AI/ML for biology systems into scientific workflows at enterprise scale' names AI/ML as a required qualification, and the agreed raw_text appears verbatim in it.

DECISION: ok

## 43. golden_100 - skill `evaluation` (uncertain)

> ...multimodal modeling, representation learning, fine-tuning, post-training, benchmarking, and ML systems. - Deep experience in computational...

- A: `evaluation` · required · raw_text: "post-training, benchmarking"
- B: `evaluation` · required · raw_text: "benchmarking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification bullet names 'benchmarking' as a required ML skill, and benchmarking is the same skill as the agreed 'evaluation' label, so this is a near-synonym mapping rather than a broader parent skill under rule 5.

DECISION: ok

## 44. golden_100 - skill `explainable-ai` (uncertain)

> ...credibility, model limitations, hallucination risk, interpretability, and validation. - Experience leading small, high-caliber...

- A: `explainable-ai` · required · raw_text: "interpretability"
- B: `explainable-ai` · required · raw_text: "interpretability"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Qualifications bullet names interpretability as something the candidate must have strong judgment about, and rule 3 makes that required mention control, so the agreed explainable-ai label with raw_text "interpretability" stands.

DECISION: ok

## 45. golden_101 - skill `ai-ml` (uncertain)

> ...independent thought and creativity driving high impact, cross disciplinary AI/ML projects. - Successful track record of leadership and...

- A: `ai-ml` · required · raw_text: "cross disciplinary AI/ML projects"
- B: `ai-ml` · required · raw_text: "AI/ML projects"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualifications section names AI/ML work in the quoted bullet "cross disciplinary AI/ML projects", and the same section also requires ML frameworks and AI/ML model progression, so the agreed required `ai-ml` label stands.

DECISION: ok

## 46. golden_102 - skill `evaluation` (uncertain)

> ...or related approaches is strongly preferred. - Ability to design rigorous evaluation frameworks, performance metrics, and benchmarking approaches for...

- A: `evaluation` · required · raw_text: "design rigorous evaluation frameworks"
- B: `evaluation` · required · raw_text: "evaluation frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "Ability to design rigorous evaluation frameworks..." sits in the PROFESSIONAL EXPERIENCE & QUALIFICATIONS section with no preferred qualifier, so the required tag and the quoted raw_text hold up under rules 1 and 3.

DECISION: ok

## 47. golden_102 - skill `machine-learning` (uncertain)

> ...AWS ecosystem. - Strong programming skills in Python and experience with modern ML frameworks such as PyTorch - Background in scientific ML,...

- A: `machine-learning` · required · raw_text: "experience with modern ML frameworks"
- B: `machine-learning` · required · raw_text: "Demonstrated experience with ML-accelerated weather, climate, or hydrology models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the PROFESSIONAL EXPERIENCE & QUALIFICATIONS heading, the required bullet asks for experience with modern ML frameworks (rule 1), and the quoted raw_text appears verbatim, so the agreed machine-learning label with required status stands.

DECISION: ok

## 48. golden_094 - attribute `degree` (spot-check)

> ...stakeholders Professional Experience & Qualifications - Master's degree (or above) in Computer Science, Machine Learning, AI, or a related field; equivalent practical experience considered - 5+ years of professional experience in applied machine...

- agreed label: value="master" · requirement="required" · or_equivalent=true · signal="Master's degree (or above) in Computer Science, Machine Learning, AI, or a related field; equivalent practical experience considered"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only level named is Master's, and the rule explicitly maps "Master's degree (or above)" to `master`; the bare requirements-list mention makes it `required`, and "equivalent practical experience considered" correctly sets `degree_or_equivalent` to true, so the agreed label stands.

DECISION: ok

## 49. golden_094 - attribute `german` (spot-check)

> Senior ML Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 50. golden_094 - skill `deep-learning` (spot-check)

> ...machine learning - Strong foundation in machine learning, deep learning, and natural language processing (NLP) - Proven...

- agreed label: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 51. golden_094 - skill `langgraph` (spot-check)

> ...experience with frameworks such as PyTorch, vLLM, or LangGraph - Hands-on experience with RAG, agentic orchestration, or...

- agreed label: `langgraph` · required · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 52. golden_094 - skill `llms` (spot-check)

> ...and natural language processing (NLP) - Proven experience deploying LLM-powered applications in production environments, including experience with...

- agreed label: `llms` · required · raw_text: "deploying LLM-powered applications"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 53. golden_094 - skill `machine-learning` (spot-check)

> ...of professional experience in applied machine learning - Strong foundation in machine learning, deep learning, and natural language processing (NLP) -...

- agreed label: `machine-learning` · required · raw_text: "Strong foundation in machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 54. golden_094 - skill `nlp` (spot-check)

> ...Strong foundation in machine learning, deep learning, and natural language processing (NLP) - Proven experience deploying LLM-powered applications in...

- agreed label: `nlp` · required · raw_text: "natural language processing (NLP)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 55. golden_094 - skill `pytorch` (spot-check)

> ...environments, including experience with frameworks such as PyTorch, vLLM, or LangGraph - Hands-on experience with RAG,...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 56. golden_094 - skill `rag` (spot-check)

> ...with frameworks such as PyTorch, vLLM, or LangGraph - Hands-on experience with RAG, agentic orchestration, or multi-agent systems is strongly...

- agreed label: `rag` · nice_to_have · raw_text: "Hands-on experience with RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 57. golden_094 - skill `vllm` (spot-check)

> ...including experience with frameworks such as PyTorch, vLLM, or LangGraph - Hands-on experience with RAG, agentic...

- agreed label: `vllm` · required · raw_text: "vLLM"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 58. golden_095 - attribute `degree` (spot-check)

> ...to the measurement pipeline REQUIRED QUALIFICATIONS - PhD in biomedical engineering, physiology, bioengineering, biophotonics, or a related field, or an MD/PhD, with substantial applied machine learning experience -...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in biomedical engineering, physiology, bioengineering, biophotonics, or a related field, or an MD/PhD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only degree level named is PhD (the MD/PhD is still a PhD-level credential), it sits in the required qualifications with no optional marking, and no equivalent-experience clause appears, so the agreed label matches the degree section's lowest-level rule.

DECISION: ok

## 59. golden_095 - attribute `german` (spot-check)

> Scientist, Machine Learning (Human Physiology)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 60. golden_095 - skill `machine-learning` (spot-check)

> ...biophotonics, or a related field, or an MD/PhD, with substantial applied machine learning experience - Deep knowledge of human physiology in an area such as...

- agreed label: `machine-learning` · required · raw_text: "substantial applied machine learning experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 61. golden_095 - skill `python` (spot-check)

> ...including within-subject and longitudinal designs - Proficiency in Python and the modern ML stack, and comfort working inside an...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 62. golden_095 - skill `statistics` (spot-check)

> ...IRB-governed protocols, and agreement analysis - Statistical modeling on small human datasets, including within-subject and...

- agreed label: `statistics` · required · raw_text: "Statistical modeling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 63. golden_096 - attribute `degree` (spot-check)

> ...scientists. Professional Experience & Qualifications - B.S. or M.S. in Computer Science, Engineering, or a related field, with 10+ years of professional software development...

- agreed label: value="master" · requirement="required" · or_equivalent=false · signal="B.S. or M.S. in Computer Science, Engineering, or a related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "B.S. or M.S. in Computer Science, Engineering, or a related field"} - Under the degree rule, "B.S. or M.S." records the lowest level named, so the degree is bachelor, not the highest level the older labels recorded as master; the requirement stays required as a bare mention in the qualifications list, and no equivalent-experience clause is present.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "B.S. or M.S. in Computer Science, Engineering, or a related field"}

## 64. golden_096 - attribute `german` (spot-check)

> Principal Software Engineer - Agentic Platform

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 65. golden_096 - skill `autogen` (spot-check)

> ...(e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience integrating LLMs and model platforms,...

- agreed label: `autogen` · nice_to_have · raw_text: "AutoGen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 66. golden_096 - skill `aws` (spot-check)

> ...idempotency, durable retries, and replay. - Strong cloud-native engineering on AWS with infrastructure-as-code, containerization, and...

- agreed label: `aws` · required · raw_text: "cloud-native engineering on AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 67. golden_096 - skill `aws-bedrock` (spot-check)

> ...platforms, including Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation and feedback-loop frameworks for...

- agreed label: `aws-bedrock` · nice_to_have · raw_text: "Amazon Bedrock"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 68. golden_096 - skill `distributed-systems` (spot-check)

> ...Demonstrated track record architecting and maintaining large-scale distributed systems in production at technology companies. -...

- agreed label: `distributed-systems` · required · raw_text: "large-scale distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 69. golden_096 - skill `evaluation` (spot-check)

> ...Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation and feedback-loop frameworks for agentic systems. - Familiarity with sandboxed code...

- agreed label: `evaluation` · nice_to_have · raw_text: "building evaluation and feedback-loop frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 70. golden_096 - skill `event-driven-systems` (spot-check)

> ...Deep expertise in workflow orchestration and event-driven architecture, including stateful execution, idempotency, durable...

- agreed label: `event-driven-systems` · required · raw_text: "event-driven architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 71. golden_096 - skill `infrastructure-as-code` (spot-check)

> ...and replay. - Strong cloud-native engineering on AWS with infrastructure-as-code, containerization, and autoscaling. - Proven ability to take systems from...

- agreed label: `infrastructure-as-code` · required · raw_text: "with infrastructure-as-code, containerization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 72. golden_096 - skill `langchain` (spot-check)

> ...orchestration frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience integrating LLMs and...

- agreed label: `langchain` · nice_to_have · raw_text: "LangChain"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 73. golden_096 - skill `langgraph` (spot-check)

> ...AI and orchestration frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience integrating...

- agreed label: `langgraph` · nice_to_have · raw_text: "LangGraph"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 74. golden_096 - skill `llms` (spot-check)

> ...Experience integrating LLMs and model platforms, including Anthropic, OpenAI, Vertex...

- agreed label: `llms` · nice_to_have · raw_text: "integrating LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 75. golden_096 - skill `openai-api` (spot-check)

> ...integrating LLMs and model platforms, including Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation...

- agreed label: `openai-api` · nice_to_have · raw_text: "OpenAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 76. golden_096 - skill `pydanticai` (spot-check)

> ...with agentic AI and orchestration frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience...

- agreed label: `pydanticai` · nice_to_have · raw_text: "Pydantic AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 77. golden_096 - skill `vertex-ai` (spot-check)

> ...LLMs and model platforms, including Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation and...

- agreed label: `vertex-ai` · nice_to_have · raw_text: "Vertex AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 78. golden_097 - attribute `degree` (spot-check)

> ...prototypes, and external publications. Qualifications - PhD in a quantitative field (statistics, computer science, applied mathematics, computational biology, physics, or related) with a strong research track record, or equivalent demonstrated expertise with 5+ years of experience post PhD. - Deep expertise in...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="PhD in a quantitative field (statistics, computer science, applied mathematics, computational biology, physics, or related) with a strong research track record, or equivalent demonstrated expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only degree level named is PhD, so under the lowest-level rule `phd` stands; it is a bare entry in the qualifications list, so `required`, and the "or equivalent demonstrated expertise" wording makes `degree_or_equivalent` true, with the signal quoted verbatim.

DECISION: ok

## 79. golden_097 - skill `software-engineering` (spot-check)

> ...and bring them to working, validated implementations. - Strong software engineering skills and comfort running computational experiments at scale...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 80. golden_098 - attribute `degree` (spot-check)

> ...action. PROFESSIONAL EXPERIENCE & QUALIFICATIONS - Master’s, or PhD in a relevant field (e.g., machine learning, mathematics, statistics,...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s, or PhD in a relevant field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Master’s, or PhD in a relevant field"} - Under the degree rule, `degree` is the lowest level named, and this posting names Master's and PhD, so the level is `master`; the bare mention in the qualifications list makes it `required`, and no 'or equivalent experience' wording appears.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Master’s, or PhD in a relevant field"}

## 81. golden_098 - attribute `seniority` (spot-check)

> Principal Scientist, Machine Learning ABOUT PIONEERING...

- agreed label: value="senior" · basis="stated" · signal="Principal Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 82. golden_098 - skill `agents` (spot-check)

> ...and agentic workflows. - Hands-on experience with agentic AI and orchestration frameworks (e.g., Pydantic AI,...

- agreed label: `agents` · nice_to_have · raw_text: "agentic AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_098 - skill `anthropic-api` (spot-check)

> ...Experience integrating LLMs and model platforms, including Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building...

- agreed label: `anthropic-api` · nice_to_have · raw_text: "Anthropic"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 84. golden_098 - skill `autogen` (spot-check)

> ...(e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience integrating LLMs and model platforms,...

- agreed label: `autogen` · nice_to_have · raw_text: "AutoGen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_098 - skill `crewai` (spot-check)

> ...frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience integrating LLMs and model...

- agreed label: `crewai` · nice_to_have · raw_text: "CrewAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_098 - skill `evaluation` (spot-check)

> ...OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation and feedback-loop frameworks for agentic systems. - Familiarity with sandboxed code execution and agent...

- agreed label: `evaluation` · nice_to_have · raw_text: "evaluation and feedback-loop frameworks for agentic systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_098 - skill `git` (spot-check)

> ...Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version control; databases; deep learning architectures; and relevant...

- agreed label: `git` · required · raw_text: "version control"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_098 - skill `llm-orchestration` (spot-check)

> ...workflows. - Hands-on experience with agentic AI and orchestration frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI,...

- agreed label: `llm-orchestration` · nice_to_have · raw_text: "orchestration frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_098 - skill `llms` (spot-check)

> ...LangGraph, LangChain, CrewAI, AutoGen). - Experience integrating LLMs and model platforms, including Anthropic, OpenAI, Vertex...

- agreed label: `llms` · nice_to_have · raw_text: "integrating LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_098 - skill `observability` (spot-check)

> ...and agent harness development. - Experience with LLM observability and monitoring tooling and cost-governance / FinOps for AI infrastructure....

- agreed label: `observability` · nice_to_have · raw_text: "LLM observability and monitoring tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_098 - skill `openai-api` (spot-check)

> ...integrating LLMs and model platforms, including Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation...

- agreed label: `openai-api` · nice_to_have · raw_text: "OpenAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_098 - skill `pydanticai` (spot-check)

> ...with agentic AI and orchestration frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience...

- agreed label: `pydanticai` · nice_to_have · raw_text: "Pydantic AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_098 - skill `python` (spot-check)

> ...Depth across multiple core tools and concepts, including Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_098 - skill `pytorch` (spot-check)

> ...and concepts, including Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version control; databases; deep...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_098 - skill `tensorflow` (spot-check)

> ...including Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version control; databases; deep learning architectures;...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_098 - skill `vertex-ai` (spot-check)

> ...LLMs and model platforms, including Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation and...

- agreed label: `vertex-ai` · nice_to_have · raw_text: "Vertex AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_099 - attribute `german` (spot-check)

> (Senior) Scientist, Machine Learning

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_099 - skill `evaluation` (spot-check)

> ...into model development - Experience developing rigorous model evaluation frameworks, benchmarks, and validation strategies for molecular ML or...

- agreed label: `evaluation` · required · raw_text: "model evaluation frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_100 - attribute `german` (spot-check)

> Principal Scientist, Machine Learning - Multimodal Biological Reasoning

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_100 - attribute `seniority` (spot-check)

> Principal Scientist, Machine Learning - Multimodal Biological Reasoning About...

- agreed label: value="senior" · basis="stated" · signal="Principal Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_100 - skill `fine-tuning` (spot-check)

> ...modern LLMs, multimodal modeling, representation learning, fine-tuning, post-training, benchmarking, and ML systems. - Deep...

- agreed label: `fine-tuning` · required · raw_text: "fine-tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_100 - skill `llms` (spot-check)

> ...forums. Qualifications - Industry-leading expertise in modern LLMs, multimodal modeling, representation learning,...

- agreed label: `llms` · required · raw_text: "modern LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_101 - attribute `degree` (spot-check)

> ...and action. PROFESSIONAL EXPERIENCE & QUALIFICATIONS - Master’s, or PhD in a relevant field (e.g., machine learning, mathematics, statistics,...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s, or PhD in a relevant field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Master’s, or PhD in a relevant field"} - Under the degree rule the label is the lowest level named, and this posting names Master's alongside PhD in a bare requirements list, so the level is master, not the phd the older highest-level rule recorded.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Master’s, or PhD in a relevant field"}

## 104. golden_101 - attribute `german` (spot-check)

> Principal Scientist, Machine Learning - Biomolecules

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 105. golden_101 - attribute `seniority` (spot-check)

> Principal Scientist, Machine Learning - Biomolecules ABOUT PIONEERING...

- agreed label: value="senior" · basis="stated" · signal="Principal Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_101 - skill `airflow` (spot-check)

> ...and pose quality metrics. - Workflow orchestration (Airflow/Prefect/Argo), data warehouses (Redshift/Snowflake),...

- agreed label: `airflow` · nice_to_have · raw_text: "Airflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_101 - skill `aws` (spot-check)

> ...(e.g., DVC/LakeFS), experiment tracking (MLflow/W&B), secure AWS infrastructure (S3, Batch/ECS/EKS, SageMaker), Docker, IaC...

- agreed label: `aws` · nice_to_have · raw_text: "secure AWS infrastructure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_101 - skill `cheminformatics` (spot-check)

> ...such as protein modeling/design, proteomics/mass spec, cheminformatics/docking/ADMET, biophysics/MD, and LLM/agentic automation. - MLOps...

- agreed label: `cheminformatics` · nice_to_have · raw_text: "cheminformatics/docking/ADMET"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_101 - skill `ci-cd` (spot-check)

> ...SageMaker), Docker, IaC (Terraform/CDK), and CI/CD (GitHub Actions). - Generative modeling...

- agreed label: `ci-cd` · nice_to_have · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_101 - skill `deep-learning` (spot-check)

> ...(PyTorch or JAX/TensorFlow); version control; databases; deep learning architectures; and relevant informatics software. - Consistent record...

- agreed label: `deep-learning` · required · raw_text: "deep learning architectures"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_101 - skill `experiment-tracking` (spot-check)

> ...expertise: data contracts and lineage (e.g., DVC/LakeFS), experiment tracking (MLflow/W&B), secure AWS infrastructure (S3,...

- agreed label: `experiment-tracking` · nice_to_have · raw_text: "experiment tracking"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_101 - skill `fastapi` (spot-check)

> ...search (FAISS/pgvector), and lightweight internal tools (FastAPI, Streamlit/Gradio). - Experience mentoring early hires,...

- agreed label: `fastapi` · nice_to_have · raw_text: "FastAPI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_101 - skill `github-actions` (spot-check)

> ...SageMaker), Docker, IaC (Terraform/CDK), and CI/CD (GitHub Actions). - Generative modeling (diffusion/flow/VAEs) for...

- agreed label: `github-actions` · nice_to_have · raw_text: "GitHub Actions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_101 - skill `infrastructure-as-code` (spot-check)

> ...AWS infrastructure (S3, Batch/ECS/EKS, SageMaker), Docker, IaC (Terraform/CDK), and CI/CD (GitHub Actions). -...

- agreed label: `infrastructure-as-code` · nice_to_have · raw_text: "IaC"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_101 - skill `jax` (spot-check)

> ...including Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version control; databases; deep learning architectures;...

- agreed label: `jax` · required · raw_text: "JAX/TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_101 - skill `mlops` (spot-check)

> ...biophysics/MD, and LLM/agentic automation. - MLOps expertise: data contracts and lineage (e.g., DVC/LakeFS), experiment...

- agreed label: `mlops` · nice_to_have · raw_text: "MLOps expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_101 - skill `pgvector` (spot-check)

> ...data warehouses (Redshift/Snowflake), vector search (FAISS/pgvector), and lightweight internal tools (FastAPI,...

- agreed label: `pgvector` · nice_to_have · raw_text: "pgvector"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_101 - skill `pytorch` (spot-check)

> ...and concepts, including Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version control; databases; deep...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_101 - skill `sagemaker` (spot-check)

> ...secure AWS infrastructure (S3, Batch/ECS/EKS, SageMaker), Docker, IaC (Terraform/CDK), and CI/CD (GitHub...

- agreed label: `sagemaker` · nice_to_have · raw_text: "SageMaker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_101 - skill `snowflake` (spot-check)

> ...(Airflow/Prefect/Argo), data warehouses (Redshift/Snowflake), vector search (FAISS/pgvector), and lightweight internal...

- agreed label: `snowflake` · nice_to_have · raw_text: "Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_101 - skill `terraform` (spot-check)

> ...(S3, Batch/ECS/EKS, SageMaker), Docker, IaC (Terraform/CDK), and CI/CD (GitHub Actions). - Generative modeling...

- agreed label: `terraform` · nice_to_have · raw_text: "Terraform"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_101 - skill `weights-and-biases` (spot-check)

> ...lineage (e.g., DVC/LakeFS), experiment tracking (MLflow/W&B), secure AWS infrastructure (S3, Batch/ECS/EKS,...

- agreed label: `weights-and-biases` · nice_to_have · raw_text: "W&B"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_102 - attribute `degree` (spot-check)

> ...leadership. PROFESSIONAL EXPERIENCE & QUALIFICATIONS - PhD in machine learning, computational science, Earth science, atmospheric science, hydrology, AI, computer science, or a related quantitative discipline. - 5+ years of postdoctoral, industry, or applied...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in machine learning, computational science, Earth science, atmospheric science, hydrology, AI, computer science, or a related quantitative discipline"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only degree named is the PhD, listed bare in the qualifications, so `phd` and `required` are correct; 'or a related quantitative discipline' widens the field rather than accepting experience, so `or_equivalent` stays false, and the signal quote matches the posting.

DECISION: ok

## 124. golden_102 - attribute `german` (spot-check)

> Senior Machine Learning Scientist, Climate & Hydrology

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_102 - attribute `seniority` (spot-check)

> Senior Machine Learning Scientist, Climate & Hydrology COMPANY DESCRIPTION Flagship...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Scientist"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_102 - skill `aws` (spot-check)

> ...preprocess, and train on large-scale climate datasets, preferably in the AWS ecosystem. - Strong programming skills in Python and experience...

- agreed label: `aws` · nice_to_have · raw_text: "preferably in the AWS ecosystem"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_102 - skill `pytorch` (spot-check)

> ...Strong programming skills in Python and experience with modern ML frameworks such as PyTorch - Background in scientific ML, spatiotemporal modeling,...

- agreed label: `pytorch` · required · raw_text: "modern ML frameworks such as PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_099 - attribute `degree` (rule-change)

> ...teams PROFESSIONAL EXPERIENCE & QUALIFICATIONS - Ph.D. in machine learning, computational chemistry, chemical physics, computer science, applied mathematics, or a related discipline with 2+ years of industry experience, or M.S. degree with...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="Ph.D. in machine learning, computational chemistry, chemical physics, computer science, applied mathematics, or a related discipline"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "M.S. degree with 6+ years of industry experience"} - Under the degree rule the label is the lowest level named, and the posting's alternative path still requires an M.S. (master) with 6+ years of experience, so the agreed 'phd' label records the higher level; the experience path substitutes for the PhD, not for the degree, so or_equivalent stays false.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "M.S. degree with 6+ years of industry experience"}

## 129. golden_100 - attribute `degree` (rule-change)

> ...creation and scientific discovery. Requirements - PhD, MS, or equivalent experience in computational biology, machine learning,...

- agreed label: value="phd" · requirement="required" · or_equivalent=true · signal="PhD, MS, or equivalent experience"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": true, "degree_signal": "PhD, MS, or equivalent experience"} - Under the degree rule, `degree` is the lowest level named, and this posting names both PhD and MS in "PhD, MS, or equivalent experience", so the label should be master, not the older highest-level phd.

DECISION: {"degree": "master", "degree_or_equivalent": true, "degree_requirement": "required", "degree_signal": "PhD, MS, or equivalent experience"}

## 130. golden_094 - groups `alternative_group` (groups)

> Senior ML Engineer

- `ai-deployment` · required · raw_text: "deploying LLM-powered applications in production environments"
- `data-pipelines` · required · raw_text: "large-scale data pipelines"
- `deep-learning` · required · raw_text: "deep learning"
- `evaluation` · required · raw_text: "standard evaluation protocols"
- `langgraph` · required · raw_text: "LangGraph"
- `llm-orchestration` · nice_to_have · raw_text: "RAG, agentic orchestration"
- `llms` · required · raw_text: "deploying LLM-powered applications"
- `machine-learning` · required · raw_text: "Strong foundation in machine learning"
- `multi-agent-systems` · nice_to_have · raw_text: "multi-agent systems is strongly preferred"
- `nlp` · required · raw_text: "natural language processing (NLP)"
- `observability` · required · raw_text: "including monitoring"
- `python` · required · raw_text: "Proficiency in Python"
- `pytorch` · required · raw_text: "PyTorch"
- `rag` · nice_to_have · raw_text: "Hands-on experience with RAG"
- `vllm` · required · raw_text: "vLLM"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "vllm", "langgraph"]] - The qualifications offer frameworks "such as PyTorch, vLLM, or LangGraph" as examples for one ask (deploying LLM-powered applications), so under the alternative_group rule's example marker these three share a group. The RAG / agentic orchestration / multi-agent list is left ungrouped because rag and llm-orchestration are also asked on their own in the responsibilities, which takes them out of the group, leaving multi-agent-systems alone and below the two-skill minimum.

DECISION: [["langgraph", "pytorch", "vllm"]]

## 131. golden_095 - groups `alternative_group` (groups)

> Scientist, Machine Learning (Human Physiology)

- `agents` · nice_to_have · raw_text: "Team members direct AI agents in their daily work for literature synthesis, study design, data analysis, and code. We are looking for someone who wants to work this way."
- `machine-learning` · required · raw_text: "substantial applied machine learning experience"
- `python` · required · raw_text: "Proficiency in Python"
- `statistics` · required · raw_text: "Statistical modeling"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - None of the four labeled skills (agents, machine-learning, python, statistics) is offered in place of another; the posting asks for them together or as a single requirement, with no 'one of', 'or', or example-set marker, so the alternative_group rule yields no group.

DECISION: []

## 132. golden_096 - groups `alternative_group` (groups)

> Principal Software Engineer - Agentic Platform

- `agent-harnesses` · nice_to_have · raw_text: "agent harness development"
- `agents` · nice_to_have · raw_text: "agentic AI and orchestration frameworks"
- `ai-infrastructure` · nice_to_have · raw_text: "FinOps for AI infrastructure"
- `anthropic-api` · nice_to_have · raw_text: "Anthropic"
- `api-design` · required · raw_text: "designing SDKs, APIs"
- `apis` · required · raw_text: "designing SDKs, APIs, and data contracts"
- `autogen` · nice_to_have · raw_text: "AutoGen"
- `aws` · required · raw_text: "cloud-native engineering on AWS"
- `aws-bedrock` · nice_to_have · raw_text: "Amazon Bedrock"
- `cloud` · required · raw_text: "Strong cloud-native engineering"
- `containerization` · required · raw_text: "containerization, and autoscaling"
- `crewai` · nice_to_have · raw_text: "CrewAI"
- `distributed-systems` · required · raw_text: "large-scale distributed systems"
- `evaluation` · nice_to_have · raw_text: "building evaluation and feedback-loop frameworks"
- `event-driven-systems` · required · raw_text: "event-driven architecture"
- `infrastructure-as-code` · required · raw_text: "with infrastructure-as-code, containerization"
- `langchain` · nice_to_have · raw_text: "LangChain"
- `langgraph` · nice_to_have · raw_text: "LangGraph"
- `llm-orchestration` · nice_to_have · raw_text: "orchestration frameworks"
- `llms` · nice_to_have · raw_text: "integrating LLMs"
- `observability` · required · raw_text: "hardened, observable, operationally excellent production"
- `openai-api` · nice_to_have · raw_text: "OpenAI"
- `pydanticai` · nice_to_have · raw_text: "Pydantic AI"
- `software-architecture` · required · raw_text: "architecting and maintaining large-scale distributed systems"
- `vertex-ai` · nice_to_have · raw_text: "Vertex AI"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pydanticai", "langgraph", "langchain", "crewai", "autogen"]] - The Preferred Qualifications ask for hands-on experience with agentic AI and orchestration frameworks, with "e.g." giving five examples for that single ask, so any one meets it; the broad parents `agents` and `llm-orchestration` stay out, and the model platforms (Anthropic, OpenAI, Vertex AI, Bedrock) are joined by "including ... and" rather than offered as alternatives, so they form no group.

DECISION: [["autogen", "crewai", "langchain", "langgraph", "pydanticai"]]

## 133. golden_097 - groups `alternative_group` (groups)

> Principal AI Scientist, Autonomous Discovery

- `causal-inference` · required · raw_text: "advanced Bayesian causal modeling"
- `software-engineering` · required · raw_text: "Strong software engineering skills"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The only labeled skills are causal-inference and software-engineering, and the posting asks for both separately, not as alternatives; the 'and/or' alternative is between causal modeling and evolutionary programming, which has no skill id in this item, so no group can be formed.

DECISION: []

## 134. golden_098 - groups `alternative_group` (groups)

> Principal Scientist, Machine Learning

- `agent-harnesses` · nice_to_have · raw_text: "agent harness development"
- `agents` · nice_to_have · raw_text: "agentic AI"
- `ai-infrastructure` · nice_to_have · raw_text: "FinOps for AI infrastructure"
- `ai-ml` · required · raw_text: "high impact, cross disciplinary AI/ML projects"
- `anthropic-api` · nice_to_have · raw_text: "Anthropic"
- `autogen` · nice_to_have · raw_text: "AutoGen"
- `aws-bedrock` · nice_to_have · raw_text: "Amazon Bedrock"
- `cheminformatics` · nice_to_have · raw_text: "cheminformatics/docking/ADMET"
- `crewai` · nice_to_have · raw_text: "CrewAI"
- `deep-learning` · required · raw_text: "deep learning architectures"
- `evaluation` · nice_to_have · raw_text: "evaluation and feedback-loop frameworks for agentic systems"
- `git` · required · raw_text: "version control"
- `jax` · required · raw_text: "JAX"
- `langchain` · nice_to_have · raw_text: "LangChain"
- `langgraph` · nice_to_have · raw_text: "LangGraph"
- `llm-orchestration` · nice_to_have · raw_text: "orchestration frameworks"
- `llms` · nice_to_have · raw_text: "integrating LLMs"
- `machine-learning` · required · raw_text: "modern ML frameworks"
- `observability` · nice_to_have · raw_text: "LLM observability and monitoring tooling"
- `openai-api` · nice_to_have · raw_text: "OpenAI"
- `pydanticai` · nice_to_have · raw_text: "Pydantic AI"
- `python` · required · raw_text: "Python"
- `pytorch` · required · raw_text: "PyTorch"
- `tensorflow` · required · raw_text: "TensorFlow"
- `vertex-ai` · nice_to_have · raw_text: "Vertex AI"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "jax", "tensorflow"], ["pydanticai", "langgraph", "langchain", "crewai", "autogen"]] - The 'modern ML frameworks (PyTorch or JAX/TensorFlow)' ask and the 'orchestration frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen)' example list each offer any one skill for a single ask, so each forms a group, while the broad parents 'machine-learning' and 'llm-orchestration' stay out and the 'Anthropic, OpenAI, Vertex AI, and Amazon Bedrock' list is joined by 'and' under 'including' and so is not grouped.

DECISION: [["autogen", "crewai", "langchain", "langgraph", "pydanticai"], ["jax", "pytorch", "tensorflow"]]

## 135. golden_099 - groups `alternative_group` (groups)

> (Senior) Scientist, Machine Learning

- `chemical-descriptors` · required · raw_text: "post-DFT descriptors"
- `cheminformatics` · nice_to_have · raw_text: "cheminformatics and molecular modeling toolkits"
- `deep-learning` · required · raw_text: "geometric deep learning"
- `evaluation` · required · raw_text: "model evaluation frameworks"
- `machine-learning` · required · raw_text: "molecular ML models"
- `model-development` · required · raw_text: "model training"
- `python` · nice_to_have · raw_text: "Proficiency with Python"
- `pytorch` · nice_to_have · raw_text: "PyTorch"
- `rdkit` · nice_to_have · raw_text: "RDKit"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The labeled skills that look like examples of one ask (PyTorch, RDKit, geometric deep learning, post-DFT descriptors) each appear with unlabeled siblings, so no set of two or more labeled skills is offered in place of each other, and cheminformatics is a broad skill named alongside its examples, which the rule keeps out of a group.

DECISION: []

## 136. golden_100 - groups `alternative_group` (groups)

> Principal Scientist, Machine Learning - Multimodal Biological Reasoning

- `agents` · required · raw_text: "scientific agents"
- `ai-deployment` · required · raw_text: "deploying AI/ML"
- `ai-ml` · required · raw_text: "AI/ML for biology systems"
- `data-science` · required · raw_text: "translational data science"
- `evaluation` · required · raw_text: "post-training, benchmarking"
- `explainable-ai` · required · raw_text: "interpretability"
- `fine-tuning` · required · raw_text: "fine-tuning"
- `hallucination-detection` · required · raw_text: "hallucination risk"
- `llms` · required · raw_text: "modern LLMs"
- `machine-learning` · required · raw_text: "ML systems"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The only alternative-style list is the Requirements line 'Experience with LLMs, ... scientific agents, or AI discovery platforms', but `llms` is also asked on its own in the Qualifications ('modern LLMs'), so it leaves any group and only `agents` remains, below the two-skill minimum.

DECISION: []

## 137. golden_101 - groups `alternative_group` (groups)

> Principal Scientist, Machine Learning - Biomolecules

- `agents` · nice_to_have · raw_text: "LLM/agentic automation"
- `ai-ml` · required · raw_text: "cross disciplinary AI/ML projects"
- `airflow` · nice_to_have · raw_text: "Airflow"
- `aws` · nice_to_have · raw_text: "secure AWS infrastructure"
- `aws-s3` · nice_to_have · raw_text: "S3"
- `cheminformatics` · nice_to_have · raw_text: "cheminformatics/docking/ADMET"
- `ci-cd` · nice_to_have · raw_text: "CI/CD"
- `deep-learning` · required · raw_text: "deep learning architectures"
- `docker` · nice_to_have · raw_text: "Docker"
- `experiment-tracking` · nice_to_have · raw_text: "experiment tracking"
- `faiss` · nice_to_have · raw_text: "FAISS"
- `fastapi` · nice_to_have · raw_text: "FastAPI"
- `git` · required · raw_text: "version control"
- `github-actions` · nice_to_have · raw_text: "GitHub Actions"
- `infrastructure-as-code` · nice_to_have · raw_text: "IaC"
- `jax` · required · raw_text: "JAX/TensorFlow"
- `llms` · nice_to_have · raw_text: "LLM/agentic automation"
- `mlflow` · nice_to_have · raw_text: "MLflow"
- `mlops` · nice_to_have · raw_text: "MLOps expertise"
- `pgvector` · nice_to_have · raw_text: "pgvector"
- `prefect` · nice_to_have · raw_text: "Prefect"
- `python` · required · raw_text: "including Python"
- `pytorch` · required · raw_text: "PyTorch"
- `sagemaker` · nice_to_have · raw_text: "SageMaker"
- `snowflake` · nice_to_have · raw_text: "Snowflake"
- `streamlit` · nice_to_have · raw_text: "Streamlit"
- `tensorflow` · required · raw_text: "JAX/TensorFlow"
- `terraform` · nice_to_have · raw_text: "Terraform"
- `vector-search` · nice_to_have · raw_text: "vector search"
- `weights-and-biases` · nice_to_have · raw_text: "W&B"
- `workflow-automation` · nice_to_have · raw_text: "agents that automate scientific workflows"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "jax", "tensorflow"], ["mlflow", "weights-and-biases"], ["airflow", "prefect"], ["fastapi", "streamlit"], ["faiss", "pgvector"]] - Under the rule's markers, each parenthetical gives examples for one ask ('modern ML frameworks (PyTorch or JAX/TensorFlow)', 'experiment tracking (MLflow/W&B)', 'workflow orchestration (Airflow/Prefect/Argo)', 'lightweight internal tools (FastAPI, Streamlit/Gradio)', 'vector search (FAISS/pgvector)'), so any one meets it; the S3/SageMaker and CI/CD or Terraform lists are left out because the broad parent is named alongside examples or the list has no 'or'.

DECISION: [["airflow", "prefect"], ["faiss", "pgvector"], ["fastapi", "streamlit"], ["jax", "pytorch", "tensorflow"], ["mlflow", "weights-and-biases"]]

## 138. golden_102 - groups `alternative_group` (groups)

> Senior Machine Learning Scientist, Climate & Hydrology

- `aws` · nice_to_have · raw_text: "preferably in the AWS ecosystem"
- `evaluation` · required · raw_text: "design rigorous evaluation frameworks"
- `machine-learning` · required · raw_text: "experience with modern ML frameworks"
- `python` · required · raw_text: "Strong programming skills in Python"
- `pytorch` · required · raw_text: "modern ML frameworks such as PyTorch"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting names only one framework (PyTorch, labeled as its own skill) and asks for Python and AWS together or as a preference, with no 'at least one of', 'X or Y', or example set for a single ask, so no two skills are alternatives under the rule.

DECISION: []

## 139. golden_096 - skill `agent-harnesses` (rule-change)

> ...systems. - Familiarity with sandboxed code execution and agent harness development. - Experience with LLM observability and...

- agreed label: `agent-harnesses` · nice_to_have · raw_text: "agent harness development"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet names agent harness development as a skill, and the agreed nice_to_have requirement and verbatim raw_text "agent harness development" both match that bullet.

DECISION: ok

## 140. golden_098 - skill `agent-harnesses` (rule-change)

> ...- Familiarity with sandboxed code execution and agent harness development. - Experience with LLM observability and monitoring...

- agreed label: `agent-harnesses` · nice_to_have · raw_text: "agent harness development"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: ok - Under rule 1, the preferred-qualifications bullet "Familiarity with sandboxed code execution and agent harness development" names the skill directly, so `agent-harnesses` as nice_to_have with the quoted raw_text is correct under rule 5, which adds no broader skill.

DECISION: ok
