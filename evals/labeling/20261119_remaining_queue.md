# What is left for Chandler - eight city batches of 19 Nov

Each item lives in its batch's `review_queue.md`; answer it there on its `DECISION:` line.
Groups run hardest first. Within a group, items are sorted by field, then batch.

| Batch | Labels | Settled by models | Left for you | of which spot-check |
|---|---:|---:|---:|---:|
| 20261119T103427Z_label | 155 | 125 | 30 | 15 |
| 20261119T110104Z_label | 129 | 111 | 18 | 15 |
| 20261119T112034Z_label | 165 | 135 | 30 | 15 |
| 20261119T114422Z_label | 156 | 124 | 32 | 15 |
| 20261119T135145Z_label | 168 | 139 | 29 | 15 |
| 20261119T140709Z_label | 157 | 132 | 25 | 15 |
| 20261119T141542Z_label | 159 | 128 | 31 | 15 |
| 20261119T142629Z_label | 153 | 120 | 33 | 15 |
| **all eight** | 1242 | 1014 | 228 | 120 |

| Group | Items |
|---|---:|
| 1. The two models split | 58 |
| 2. No model could rule | 32 |
| 3. Degree: the two models split | 0 |
| 4. Any-one-of groups the two models did not settle | 17 |
| 5. Agreed labels a third model read differently | 1 |
| 6. Random spot-check | 120 |

## 1. The two models split (58)

A labeler disagreement where the proposer and the judge (two different companies' models) gave different answers. Read the excerpt, pick `A`, `B`, `both`, `drop`, or write the value.

### 20261119T103427Z_label item 19 - golden_095 `seniority` (disagreement)
> ...or Computer Engineering (or equivalent experience) with 5+ years in Physical Design CAD methodology at advanced nodes. - Proven track record improving PPA and/or runtime on...
- A: value="senior" · basis="inferred" · signal="5+ years in Physical Design CAD methodology at advanced nodes"
- B: value=null · basis=null · signal=null
- proposer: B - Under rule 1, the "5+ years" is a years-of-experience requirement, which does not count as a qualification signal, and the posting explicitly says it welcomes various experience levels and that offers may differ from the level posted, s
- judge: A - Under Rule 3, a required qualification bullet explicitly specifying '5+ years in Physical Design CAD methodology at advanced nodes' serves as the determining mention to infer seniority.

### 20261119T103427Z_label item 34 - golden_105 `seniority` (disagreement)
> ...run them without you. What We Need - An Engineer with 5+ years developing and supporting physical design methodology or CAD flows in production use. - Expertise with industry-standard...
- A: value="senior" · basis="inferred" · signal="5+ years developing and supporting physical design methodology or CAD flows"
- B: value=null · basis=null · signal=null
- proposer: B - Under rule 1, a years-of-experience line ('5+ years developing and supporting physical design methodology') does not count as qualifying evidence, and the posting has no other explicit seniority wording, so the seniority value should be
- judge: A - Rule 1 excludes years-of-experience lines from counting as skills, not from serving as an inferred seniority signal, and 5+ years of experience supports inferring senior level.

### 20261119T103427Z_label item 49 - golden_098 `seniority` (uncertain)
> ...machine learning, mathematics, or a related discipline and 2+ years of relevant experience - Proficiency in machine learning and data science, with...
- A: value="junior" · basis="inferred" · signal="2+ years of relevant experience"
- B: value="junior" · basis="inferred" · signal="2+ years of relevant experience"
- proposer: drop - Under rule 1, the only support for seniority is a years-of-experience line ("2+ years of relevant experience"), which does not count, so the attribute should be null rather than "junior".
- judge: ok - Rule 1 excludes years-of-experience lines from counting as skills, not from serving as the inferred signal for the seniority attribute, which is properly inferred as junior from '2+ years of relevant experience'.

### 20261119T112034Z_label item 23 - golden_097 `seniority` (disagreement)
> ...training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML systems deployment with specific focus on cluster...
- A: value="mid" · basis="inferred" · signal="Ideally, 3-5 years of relevant experience"
- B: value="senior" · basis="stated" · signal="Member of Technical Staff"
- proposer: drop - Under rule 1 a years-of-experience line does not establish seniority, and A's only signal is the hedged "Ideally, 3-5 years" nice-to-have. B's quoted signal "Member of Technical Staff" does not appear in the excerpt, so the attribute
- judge: A - The posting explicitly states 'Ideally, 3-5 years of relevant experience' under Required Experience, which is the standard basis for inferring mid-level seniority (Rule 1 applies to skill extraction, not the seniority attribute).

### 20261119T135145Z_label item 57 - golden_100 `seniority` (uncertain)
> ...physics, computer graphics or a related field, or a Masters + 3 years of experience. Exceptional candidates with a bachelor’s degree and 3+...
- A: value="mid" · basis="inferred" · signal="a Masters + 3 years of experience"
- B: value="mid" · basis="inferred" · signal="Masters + 3 years of experience"
- proposer: drop - Under rule 1, a years-of-experience qualification line does not count as a seniority signal, and the posting names no seniority level (no junior, mid, senior or similar), so the inferred "mid" is unsupported and the attribute should 
- judge: ok - Rule 1 excludes years-of-experience lines from counting as skills, not from serving as an inferred seniority signal, so 'a Masters + 3 years of experience' properly supports inferring 'mid' seniority.

### 20261119T141542Z_label item 51 - golden_096 `seniority` (uncertain)
> ...own end-to-end AI projects from discovery to production, leading architecture, testing, and governance efforts. Responsibilities include prototyping AI workflows,...
- A: value="senior" · basis="inferred" · signal="leading architecture, testing, and governance efforts"
- B: value="senior" · basis="inferred" · signal="leading architecture, testing, and governance efforts"
- proposer: drop - Under rule 4, the only support for seniority is responsibilities ('You'll own end-to-end AI projects', 'leading architecture...'), and the posting never asks the candidate for a seniority level, title, or years of experience, so the 
- judge: ok - Inferring seniority from high-level ownership and leadership duties ('leading architecture, testing, and governance efforts') is valid when no explicit title or years of experience are stated, as Rule 4 applies to skills rather than role se

### 20261119T141542Z_label item 56 - golden_099 `seniority` (uncertain)
> ...like IRS form completion. • Lead & Future-Proof: Guide offshore mid-level engineers through code reviews and architectural alignment, while building Model Context Protocol (MCP) servers to...
- A: value="senior" · basis="inferred" · signal="Guide offshore mid-level engineers through code reviews and architectural alignment"
- B: value="senior" · basis="inferred" · signal="Guide offshore mid-level engineers through code reviews and architectural alignment"
- proposer: drop - Under rule 4, the only signal for "senior" is the "Lead & Future-Proof" bullet under What You'll Do, which is a responsibility the candidate is not asked to have, and the only stated requirement is 3+ years, which does not support se
- judge: ok - While Rule 4 excludes responsibilities from counting as required candidate skills, job duties like guiding mid-level engineers directly define the seniority level of the role itself.

### 20261119T103427Z_label item 36 - golden_105 `workflow-automation` (disagreement)
> ...on daily. - Automation-minded, happiest when you are removing manual steps and making PPA exploration repeatable. - Building with AI as part of how you develop flows, and...
- A: (did not label this)
- B: `workflow-automation` · required · raw_text: "removing manual steps and making PPA exploration repeatable"
- proposer: B - Under rule 1, the 'Who You Are' bullet describes the candidate as 'automation-minded' and 'removing manual steps,' which is a candidate qualification naming workflow automation, and rule 3 supports keeping the required tag on that quote
- judge: drop - Under Rule 5, the posting never actually names the skill 'workflow automation', only referring generally to being 'automation-minded' and 'removing manual steps' in CAD/PPA flows.

### 20261119T103427Z_label item 38 - golden_107 `software-architecture` (disagreement)
> ...in Python or Go; C++ is a plus - Track record of designing and building scalable, maintainable systems and services - Experience operating production services end-to-end:...
- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designing and building scalable, maintainable systems and services"
- proposer: B - Under rule 1, the required 'What you will need' bullet asks for 'designing and building scalable, maintainable systems and services', which is a named qualification covering software architecture, and B's raw_text quotes it word for wor
- judge: drop - Under Rule 5, the posting asks for 'designing and building scalable, maintainable systems and services' (which corresponds to system design or software development), and we must not add a broad skill like software-architecture that the text

### 20261119T103427Z_label item 40 - golden_108 `mlops` (disagreement)
> ...clearance - Proven track record of deploying and maintaining machine learning/AI systems in production. - Strong expertise in ML frameworks such as PyTorch,...
- A: (did not label this)
- B: `mlops` · required · raw_text: "maintaining machine learning/AI systems in production"
- proposer: B - Under rule 1, the required bullet "Proven track record of deploying and maintaining machine learning/AI systems in production" names a qualification skill that is MLOps, and rule 3 makes that required mention count, so B's labeling stan
- judge: drop - Under Rule 5, the posting does not name the skill 'MLOps' directly, so a broad or parent skill should not be inferred from a description of deploying and maintaining ML systems.

### 20261119T103427Z_label item 43 - golden_096 `ai-ml` (uncertain)
> ...& Skills: - 7+ years of experience in AI/ML engineering with 4+ years focusing on deep learning and neural network...
- A: `ai-ml` · required · raw_text: "AI/ML engineering"
- B: `ai-ml` · required · raw_text: "AI/ML engineering"
- proposer: {"requirement": "required", "raw_text": "Strong expertise in both computer vision and natural language processing with hands-on model development experience"} - Under rule 1 the agreed raw_text "AI/ML engineering" sits in a years-of-experie
- judge: drop - The only explicit mention of AI/ML in the qualifications is in a years-of-experience line which does not count under Rule 1, and we do not add a broad parent skill from specific sub-skills like computer vision or NLP under Rule 5.

### 20261119T103427Z_label item 67 - golden_104 `machine-learning` (uncertain)
> ...- 4+ years of experience (can be graduate research) in machine learning research, AI model development, or related fields - Strong...
- A: `machine-learning` · required · raw_text: "machine learning research"
- B: `machine-learning` · required · raw_text: "machine learning research"
- proposer: drop - Under rule 1, the only quoted mention of machine learning is inside the years-of-experience line ("4+ years of experience ... in machine learning research"), which does not count; the qualification bullets name deep learning, framewo
- judge: ok - Under rule 1, a qualification bullet that names a skill ('machine learning research') counts, as the exclusion only applies to job-title years-of-experience lines like 'experience as a software engineer'.

### 20261119T103427Z_label item 68 - golden_104 `model-development` (uncertain)
> ...(can be graduate research) in machine learning research, AI model development, or related fields - Strong expertise in deep learning...
- A: `model-development` · required · raw_text: "AI model development"
- B: `model-development` · required · raw_text: "training and fine-tuning large-scale models"
- proposer: {"requirement": "required", "raw_text": "Hands-on experience training and fine-tuning large-scale models"} - Under rule 1 the labeled quote sits in a years-of-experience line, which does not count, but the separate qualification bullet 'Han
- judge: ok - Under Rule 1, a qualification bullet that names a specific skill ('AI model development') counts even if it also mentions years of experience, unlike a generic job-title years-of-experience line.

### 20261119T112034Z_label item 20 - golden_095 `software-engineering` (disagreement)
> ...product experiences. - Commercial experience writing critical production code and working with microservices. - Experience designing...
- A: (did not label this)
- B: `software-engineering` · nice_to_have · raw_text: "writing critical production code"
- proposer: B - Under rule 1, the nice-to-have bullet "Commercial experience writing critical production code" is a qualification that names a software engineering skill, and the quoted raw_text appears verbatim in the posting.
- judge: drop - Under rule 5, do not add the broad parent skill `software-engineering` when the text does not name it.

### 20261119T112034Z_label item 25 - golden_097 `aws` (disagreement)
> ...We work with Kubernetes, Slurm, Python, C++, PyTorch, and primarily on AWS. As an AI Infrastructure Engineer, you will be partnering...
- A: `aws` · required · raw_text: "primarily on AWS"
- B: (did not label this)
- proposer: A - Under rule 1, the sentence "We work with ... and primarily on AWS" names AWS as the platform the candidate will work on, and rule 3 keeps a mention that the text supports, so labeler A's aws skill stands.
- judge: drop - Under rules 1 and 4, a general overview sentence describing the team's tech stack ('We work with ... and primarily on AWS') is not a qualification asking the candidate for the skill, so it does not count.

### 20261119T112034Z_label item 27 - golden_098 `software-engineering` (disagreement)
> ...advanced coding skills in Python and proven experience building and maintaining scalable codebases. - You enjoy mentoring junior colleagues and have prior...
- A: (did not label this)
- B: `software-engineering` · required · raw_text: "building and maintaining scalable codebases"
- proposer: B - Under rule 1, the qualification bullet 'proven experience building and maintaining scalable codebases' is a required qualification that names the skill, and rule 3 makes that required mention control, so B's label stands.
- judge: drop - Under Rule 5, the text asks for 'building and maintaining scalable codebases' and does not explicitly name the broad skill 'software-engineering'.

### 20261119T112034Z_label item 29 - golden_100 `llm-orchestration` (disagreement)
> ...- Experience implementing RAG pipelines, tool use, or multi-step AI workflows - Strong understanding of AI system evaluation,...
- A: (did not label this)
- B: `llm-orchestration` · required · raw_text: "multi-step AI workflows"
- proposer: B - Under rule 1, the required qualification bullet "Experience implementing RAG pipelines, tool use, or multi-step AI workflows" names the skill, and it sits in the WHO YOU ARE list rather than a "plus" line, so labeler B's required tag an
- judge: drop - Under Rule 5, the posting says 'multi-step AI workflows' and does not explicitly name the skill 'llm-orchestration'.

### 20261119T112034Z_label item 50 - golden_094 `mlops` (uncertain)
> ...domain. Nice to have - Experience training ML models and operating them in production, at scale. #LI-Hybrid Unleash Your Potential When you join...
- A: `mlops` · nice_to_have · raw_text: "operating them in production, at scale"
- B: `mlops` · nice_to_have · raw_text: "Experience training ML models and operating them in production, at scale."
- proposer: ok - Under rule 1 the nice-to-have bullet names the skill by describing training ML models and operating them in production at scale, which is MLOps, and rule 3 is satisfied because the agreed raw_text appears verbatim and no required menti
- judge: drop - Under rule 1 and rule 5, the posting does not name the skill 'MLOps' (describing 'operating them in production, at scale' for ML models does not permit adding a broad/inferred skill label the text does not name).

### 20261119T112034Z_label item 57 - golden_097 `ai-deployment` (uncertain)
> ...training jobs and high-availability inference services - Ideally, 3-5 years of relevant experience in ML systems deployment with specific focus on cluster orchestration and resource...
- A: `ai-deployment` · nice_to_have · raw_text: "Ideally, 3-5 years of relevant experience in ML systems deployment"
- B: `ai-deployment` · nice_to_have · raw_text: "Ideally, 3-5 years of relevant experience in ML systems deployment"
- proposer: {"requirement": "required", "raw_text": "Experience supporting both long-running training jobs and high-availability inference services"} - Under rule 1 the agreed quote is a years-of-experience line that cannot count, and under rule 3 a re
- judge: ok - Under Rule 1, a qualification bullet naming a specific skill ('ML systems deployment') counts even if it includes a years-of-experience qualifier, unlike a generic job-title years line.

### 20261119T112034Z_label item 59 - golden_097 `devops` (uncertain)
> ...cluster administration and HPC workload management - Previous roles in SRE, DevOps, or Platform Engineering with focus on ML infrastructure - Experience supporting...
- A: `devops` · required · raw_text: "Previous roles in SRE, DevOps, or Platform Engineering"
- B: `devops` · required · raw_text: "Previous roles in SRE, DevOps, or Platform Engineering"
- proposer: drop - Under rule 1, the only devops mention is "Previous roles in SRE, DevOps, or Platform Engineering," which names job titles rather than a skill, and rule 5 bars adding devops from the broader GitOps or infrastructure-as-code wording.
- judge: ok - Under rule 1, 'Previous roles in SRE, DevOps, or Platform Engineering' is a qualification bullet naming DevOps as a required domain background rather than a mere job-title experience line.

### 20261119T112034Z_label item 69 - golden_104 `llms` (uncertain)
> ...levels in the UK. We’re looking for people who have built generative AI products and are eager to lead AI efforts end-to-end, from early...
- A: `llms` · required · raw_text: "built generative AI products"
- B: `llms` · required · raw_text: "have built generative AI products"
- proposer: ok - Under rule 3, the required qualification "built generative AI products" is a qualification bullet that names the skill (rule 1), and the agreed llms label fits it, so I see no grounds to change it.
- judge: drop - The text asks for people who have 'built generative AI products' and does not specifically name LLMs, so under Rule 5 we do not add a skill the text does not name.

### 20261119T114422Z_label item 17 - golden_098 `open-source-llms` (disagreement)
> ...benchmarks used by the community - Contributions to open-source LLM training projects or tools WHAT WE OFFER - High-impact AI projects that are...
- A: (did not label this)
- B: `open-source-llms` · nice_to_have · raw_text: "open-source LLM training projects or tools"
- proposer: B - Under rule 1, the preferred-qualifications bullet "Contributions to open-source LLM training projects or tools" is a qualification that names the skill, and its nice_to_have requirement matches the section heading, so B's labeling stand
- judge: drop - Under rule 5, the bullet asks for contributions to open-source LLM training projects or tools (open-source tooling for LLM training), rather than open-source LLMs themselves.

### 20261119T114422Z_label item 24 - golden_102 `fine-tuning` (disagreement)
> ...with language-model training or post-training. - Experience with agent or gaming...
- A: `fine-tuning` · nice_to_have · raw_text: "post-training"
- B: (did not label this)
- proposer: A - Under rule 1, the Preferred qualifications bullet "Experience with language-model training or post-training" names a skill, and post-training is effectively fine-tuning, so the labeler's nice_to_have fine-tuning tag with raw_text "post-
- judge: drop - Under rule 1 and rule 5, the posting names 'post-training' (which includes RLHF, DPO, etc.) rather than specifically naming 'fine-tuning', so a specific skill not named in the text should not be inferred.

### 20261119T114422Z_label item 25 - golden_102 `model-development` (disagreement)
> ...qualifications - Experience with language-model training or post-training. - Experience with agent or gaming...
- A: (did not label this)
- B: `model-development` · nice_to_have · raw_text: "language-model training"
- proposer: B - Under rule 1, the Preferred qualifications bullet "Experience with language-model training or post-training" names a skill that maps to model-development as a nice_to_have, and the raw_text quote supports that, while rule 5 is not viola
- judge: drop - Under Rule 5, the text names specific LLM skills ('language-model training or post-training') rather than the broad parent skill 'model-development'.

### 20261119T114422Z_label item 28 - golden_103 `event-driven-systems` (disagreement)
> ...that use tools and execute multi-step workflows - Experience building or maintaining event-sourced systems - Python programming skills - Experience with AI or ML...
- A: `event-driven-systems` · nice_to_have · raw_text: "Experience building or maintaining event-sourced systems"
- B: (did not label this)
- proposer: A - Under rule 1, the nice-to-have bullet "Experience building or maintaining event-sourced systems" is a qualification sentence that names an event-driven skill, and rule 5 is not triggered because event-sourced systems is the named skill 
- judge: drop - Under rule 5, the posting names 'event-sourced systems' (event sourcing) rather than the broader parent skill 'event-driven-systems'.

### 20261119T114422Z_label item 30 - golden_104 `model-development` (disagreement)
> ...review and architecture decisions. - Proven experience training and deploying language models to production. - Experience preparing large-scale training datasets:...
- A: (did not label this)
- B: `model-development` · required · raw_text: "training and deploying language models to production"
- proposer: B - Under Rule 1, the MINIMUM QUALIFICATIONS bullet "Proven experience training and deploying language models to production" names model development as a required skill, and Rule 3 makes that required mention decisive over labeler A's omiss
- judge: drop - Under Rule 5, the phrase 'training and deploying language models to production' does not name the broad skill `model-development`.

### 20261119T114422Z_label item 52 - golden_098 `model-development` (uncertain)
> ...years of ML engineering experience - Proven experience training and deploying language models to production (embedding models, encoder models, or large...
- A: `model-development` · required · raw_text: "training and deploying language models"
- B: `model-development` · required · raw_text: "training and deploying language models to production"
- proposer: ok - Under rule 1, the MINIMUM QUALIFICATIONS bullet asking for "Proven experience training and deploying language models to production" names model development as a required skill, and the agreed raw_text appears verbatim in that bullet.
- judge: drop - Under Rule 5, the posting asks for 'training and deploying language models' rather than naming the broad parent skill 'model-development'.

### 20261119T114422Z_label item 55 - golden_099 `data-privacy-and-security` (uncertain)
> ...to apply machine learning to member safety, with care for data privacy and the consequences of incorrect...
- A: `data-privacy-and-security` · required · raw_text: "care for data privacy"
- B: `data-privacy-and-security` · required · raw_text: "care for data privacy"
- proposer: ok - Under rule 1, the required qualification bullet names data privacy as something the candidate must care about, and rule 3 makes that required mention count, so the agreed required label with raw_text "care for data privacy" stands.
- judge: drop - Under Rule 1, asking for motivation and 'care for data privacy' is an attitudinal statement rather than a qualification asking for data privacy and security as a skill.

### 20261119T114422Z_label item 60 - golden_100 `llms` (uncertain)
> ...systems, usage metering, FinOps data, Terraform or GenAI systems is considered an advantage. How do you work? You take ownership of your work from...
- A: `llms` · nice_to_have · raw_text: "GenAI systems is considered an advantage"
- B: `llms` · nice_to_have · raw_text: "GenAI systems"
- proposer: ok - Under rule 1, the advantage sentence explicitly names "GenAI systems", which is a reasonable match for `llms` at nice_to_have, and the agreed raw_text appears word for word in the posting.
- judge: drop - Under rule 1 and rule 5, the posting names 'GenAI systems', not LLMs specifically, so `llms` is not directly named in the text.

### 20261119T114422Z_label item 61 - golden_100 `observability` (uncertain)
> ...Kubernetes (EKS) on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and OpenTelemetry. - CI/CD: GitHub Actions. At DPG Media, we are open to...
- A: `observability` · required · raw_text: "Observability: Grafana, Prometheus and OpenTelemetry"
- B: `observability` · required · raw_text: "Observability"
- proposer: ok - Under rule 1 the bullet naming Grafana, Prometheus and OpenTelemetry under observability is a skill-naming sentence, and rule 3 keeps the agreed required status since nothing in the excerpt marks it optional, though the 'Our stack' fra
- judge: drop - Under rules 1 and 4, a bullet under 'Our stack' merely describes the team's tech environment and is not a qualification bullet or sentence asking the candidate for the skill.

### 20261119T135145Z_label item 20 - golden_096 `model-development` (disagreement)
> ...in OS configuration tooling. - Familiarity with AI inference and/or training workflows and the operational patterns around them. - Pragmatic,...
- A: (did not label this)
- B: `model-development` · required · raw_text: "AI inference and/or training workflows"
- proposer: B - Under rules 1 and 3, the required qualification bullet "Familiarity with AI inference and/or training workflows" names training workflows, which supports model-development as required, and labeler B's raw_text quotes it accurately; the 
- judge: drop - Under Rule 5, familiarity with the operational patterns around AI inference and training workflows for an infrastructure role does not actually name or ask for the skill of developing models (`model-development`).

### 20261119T135145Z_label item 25 - golden_098 `computer-vision` (disagreement)
> ...Hand-eye and multi-camera calibration, depth sensing and 3D perception on hardware. - Open-source contributions or publications at robotics...
- A: (did not label this)
- B: `computer-vision` · nice_to_have · raw_text: "3D perception on hardware"
- proposer: B - Under rule 1, the Preferred Qualifications bullet names 3D perception and depth sensing, which are computer-vision skills, so the nice_to_have tag with the verbatim raw_text "3D perception on hardware" holds even though the word "comput
- judge: drop - Under rule 5, do not add a broad or parent skill like computer-vision when the text does not name it.

### 20261119T135145Z_label item 26 - golden_098 `model-development` (disagreement)
> ...for 3D printing or machining. - Robot learning: you have trained or deployed learned policies (imitation learning, RL or VLA) on real robots, and are...
- A: (did not label this)
- B: `model-development` · required · raw_text: "trained or deployed learned policies"
- proposer: B - Under rule 1, the required Minimum Qualifications bullet on robot learning names training or deploying learned policies, and rule 3 makes that required mention decisive, so the model-development label with its required tag and raw_text 
- judge: drop - Under Rule 5, the posting asks for having 'trained or deployed learned policies' and does not name 'model development'.

### 20261119T135145Z_label item 27 - golden_098 `software-architecture` (disagreement)
> ...of arms with grippers or hands. - System design: you have designed robot software systems end to end (control loops at 500 Hz to 1 kHz, state estimation, data...
- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designed robot software systems end to end"
- proposer: B - Under Minimum Qualifications, rule 1 applies: the "System design" bullet requires having "designed robot software systems end to end" with data flow and interfaces, which is software architecture work the posting actually asks for, so l
- judge: drop - Under Rule 5, the posting asks for 'System design' ('designed robot software systems end to end') rather than naming software architecture, so we should not add a skill the text does not name.

### 20261119T135145Z_label item 37 - golden_108 `model-development` (disagreement)
> ...or applied mathematics/statistics. - Experience in developing ML training code for use in a cloud computing environment. - Demonstrated...
- A: (did not label this)
- B: `model-development` · required · raw_text: "developing ML training code"
- proposer: B - Under rule 1, the required qualification bullet "Experience in developing ML training code for use in a cloud computing environment" names ML development work, and under rule 3 that required mention, quoted as "developing ML training co
- judge: {'requirement': 'nice_to_have', 'raw_text': 'model development'} - Under Rule 1 and Rule 5, the explicit mention of 'model development' appears only in the bonus qualification section, whereas the required section names 'developing ML training code' rather than model development itself.

### 20261119T135145Z_label item 47 - golden_097 `ai-deployment` (uncertain)
> ...Computer Engineering, or a related field. - 3+ years of machine learning R&D and deployment experience. - Strong proficiency in one or more programming...
- A: `ai-deployment` · required · raw_text: "machine learning R&D and deployment experience"
- B: `ai-deployment` · required · raw_text: "machine learning R&D and deployment experience"
- proposer: drop - Under rule 1, the only support is the years-of-experience line "3+ years of machine learning R&D and deployment experience," which does not count as a named skill, and no other required mention of AI deployment appears.
- judge: ok - Under Rule 1, a qualification bullet that names a specific skill ('machine learning R&D and deployment experience') counts, unlike a generic role-tenure line.

### 20261119T135145Z_label item 66 - golden_103 `ai-infrastructure` (uncertain)
> ...You’ll Need: - 8 years of industry experience w 4+ years of ML infrastructure experience — data preprocessing, model training, evaluation,...
- A: `ai-infrastructure` · required · raw_text: "4+ years of ML infrastructure experience"
- B: `ai-infrastructure` · required · raw_text: "ML infrastructure experience"
- proposer: drop - Under rule 1, "4+ years of ML infrastructure experience" is a years-of-experience line like the rule's "experience as a software engineer" example, so it does not establish the ai-infrastructure skill, and no other required mention i
- judge: ok - Under rule 1, a qualification bullet that names a specific skill ('4+ years of ML infrastructure experience') counts, unlike a generic role-tenure line.

### 20261119T135145Z_label item 69 - golden_103 `observability` (uncertain)
> ...— dataset construction, training, fine-tuning, evaluation, profiling, and monitoring - Familiarity with modern model architectures — including...
- A: `observability` · required · raw_text: "profiling, and monitoring"
- B: `observability` · required · raw_text: "monitoring"
- proposer: ok - Under the 'What You'll Need' qualifications, rule 1 applies because the bullet asks for experience with 'profiling, and monitoring' as part of end-to-end model development, and monitoring is a named observability practice, so the agree
- judge: drop - Under Rule 5, the posting asks for model 'monitoring' in the context of end-to-end model development, not the broader parent skill 'observability' which is never named.

### 20261119T135145Z_label item 76 - golden_106 `ai-infrastructure` (uncertain)
> ...years of professional experience in systems programming, ML infrastructure, or distributed inference. - Proficient in C++ and...
- A: `ai-infrastructure` · required · raw_text: "ML infrastructure"
- B: `ai-infrastructure` · required · raw_text: "ML infrastructure"
- proposer: drop - Under rule 1, the only mention of ML infrastructure is inside the '3+ years of professional experience in ... ML infrastructure' line, which is a years-of-experience line and does not count as a named skill.
- judge: ok - Under Rule 1, 'ML infrastructure' is explicitly named as a specific technical domain in a qualification bullet rather than a generic job-title years-of-experience line.

### 20261119T140709Z_label item 32 - golden_106 `model-development` (disagreement)
> ...understanding of the mathematical foundations of ML. • Building and sustaining training and essential metric workflows for large-scale datasets. • Excellent communication and analytical skills....
- A: (did not label this)
- B: `model-development` · required · raw_text: "Building and sustaining training and essential metric workflows for large-scale datasets."
- proposer: B - Under rule 1, the required qualification bullet under "What We Need To See" names building training and metric workflows for ML, which supports model-development, and rule 3 says a required mention wins, so B's required label stands.
- judge: {'requirement': 'nice_to_have', 'raw_text': 'developing and shipping deep learning models'} - Under rule 1 and rule 5, the required bullet only names building training and metric workflows, whereas 'developing and shipping deep learning models' in the preferred section explicitly names model development.

### 20261119T140709Z_label item 52 - golden_099 `ai-ml` (uncertain)
> ...engineering, analytics engineering, data architecture or AI/ML delivery. • Production experience with Snowflake Cortex, including...
- A: `ai-ml` · required · raw_text: "AI/ML delivery"
- B: `ai-ml` · required · raw_text: "AI/ML delivery"
- proposer: {"requirement": "required", "raw_text": "Solid understanding of RAG, embeddings, text-to-SQL, prompt engineering"} - Under rule 1 the agreed quote "AI/ML delivery" sits in a years-of-experience line and doesn't count, but the required quali
- judge: ok - Under Rule 1, a qualification bullet that names the skill ('AI/ML delivery') counts, and only years-of-experience lines naming a job title (like 'experience as a software engineer') are excluded.

### 20261119T140709Z_label item 56 - golden_101 `observability` (uncertain)
> ...control: Git & GitHub - AI Tooling: Copilot on GitHub - Observability: Datadog 4 Days in Office: Metropolis values in-person...
- A: `observability` · required · raw_text: "Observability: Datadog"
- B: `observability` · required · raw_text: "Observability"
- proposer: ok - Under rule 1, "Observability: Datadog" is a bullet naming the skill, and it falls outside the "While not required, these are a plus" list, so the agreed required level stands under rule 3.
- judge: drop - Under rules 1 and 4, 'Observability: Datadog' is a category label in an informational 'Our Stack' section, not a qualification bullet asking the candidate for the skill.

### 20261119T140709Z_label item 63 - golden_105 `ai-deployment` (uncertain)
> ...for AI services • Cloud engineering and secure AI deployment on AWS, Azure, or GCP • API integration with SIEM, SOAR,...
- A: `ai-deployment` · required · raw_text: "secure AI deployment"
- B: `ai-deployment` · required · raw_text: "deploy production AI applications"
- proposer: {"requirement": "required", "raw_text": "experience building or deploying AI/ML solutions"} - Under rule 3, the required preamble ('must have... experience building or deploying AI/ML solutions') is the determining mention, and the agreed r
- judge: ok - Under Rule 1, a qualification bullet under the 'Must Have' section explicitly names the skill as 'secure AI deployment', making the agreed label and quote accurate.

### 20261119T141542Z_label item 32 - golden_097 `python` (disagreement)
> AI-Driven Full Stack Engineer (Python & ML Infra) Turing is seeking a Software Engineering Evaluator to...
- A: `python` · required · raw_text: "Python & ML Infra"
- B: (did not label this)
- proposer: {"requirement": "required", "raw_text": "Focus will be on Python across backend services"} - Under rule 1 the title fragment "Python & ML Infra" does not count, so I anchor python to the body sentence naming Python as the focus of the evalu
- judge: drop - Under Rule 1, the job title fragment ('Python & ML Infra') does not count, and under Rule 4, the description of the role's focus ('Focus will be on Python...') is a responsibility rather than a candidate qualification.

### 20261119T141542Z_label item 34 - golden_098 `workflow-automation` (disagreement)
> ...present solutions across diverse audiences Experience with Google Docs automation preferred Proficiency with IDEs such as VSCode, Microsoft Office,...
- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "Google Docs automation preferred"
- proposer: B - Under rule 1, the qualification sentence "Experience with Google Docs automation preferred" names an automation skill, and rule 3 supports B's nice_to_have tag because the quoted raw_text is the word-for-word "preferred" mention.
- judge: drop - Under Rule 5, 'Google Docs automation' refers to automating a specific document application and does not name the broad 'workflow-automation' skill.

### 20261119T141542Z_label item 46 - golden_105 `model-development` (disagreement)
> ...segmentation (YOLO family, DETR-style models), including training, tuning, and production deployment. • Hands-on experience...
- A: (did not label this)
- B: `model-development` · required · raw_text: "training"
- proposer: B - Under rule 1, the requirement bullet "Deep hands-on experience with object detection and segmentation... including training, tuning, and production deployment" names model training as a qualification, and rule 3 says a required mention 
- judge: drop - Under Rule 5, the broad skill `model-development` should not be added when the posting only names specific activities like "training" and "tuning" rather than model development.

### 20261119T141542Z_label item 57 - golden_099 `backend-development` (uncertain)
> ...Fabric, Snowflake, or Databricks). • Proven experience supporting the data backend for active, production AI applications and unstructured...
- A: `backend-development` · required · raw_text: "supporting the data backend"
- B: `backend-development` · required · raw_text: "supporting the data backend"
- proposer: ok - Under rule 1, the required qualification 'Proven experience supporting the data backend for active, production AI applications' names backend work, and the agreed required label with that raw_text is supported by the posting.
- judge: drop - Under Rule 5, 'supporting the data backend' in a Data Engineer qualification refers to data infrastructure rather than explicitly naming backend software development.

### 20261119T141542Z_label item 67 - golden_100 `mlops` (uncertain)
> ...and debugging user issues What You’ll Need to Succeed • 5+ years of experience in MLOps, Software engineering, Data engineering, or a related...
- A: `mlops` · required · raw_text: "5+ years of experience in MLOps"
- B: `mlops` · required · raw_text: "5+ years of experience in MLOps"
- proposer: drop - Under rule 1, the only required mention of MLOps is the years-of-experience line "5+ years of experience in MLOps," which does not count, and the other MLOps mentions are responsibilities, which rule 4 excludes.
- judge: ok - Under Rule 1, '5+ years of experience in MLOps' is a qualification bullet that explicitly names the skill MLOps rather than a job title line like 'experience as a software engineer'.

### 20261119T141542Z_label item 71 - golden_101 `cloud` (uncertain)
> ...& Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability engineering, software engineering, or a...
- A: `cloud` · required · raw_text: "cloud engineering"
- B: `cloud` · required · raw_text: "cloud engineering"
- proposer: {"requirement": "required", "raw_text": "cloud security fundamentals"} - Under rule 1, the agreed raw_text "cloud engineering" sits in a years-of-experience line and doesn't count, but the required list under "Required Skills & Experience" 
- judge: ok - Under Rule 1, a qualification bullet that names a skill ('cloud engineering') counts, while 'cloud security fundamentals' names a security skill rather than the parent 'cloud' skill.

### 20261119T142629Z_label item 18 - golden_095 `workflow-automation` (disagreement)
> ...AI testing frameworks, autonomous testing agents or intelligent automation solutions - Working knowledge of large-scale distributed systems...
- A: (did not label this)
- B: `workflow-automation` · nice_to_have · raw_text: "intelligent automation solutions"
- proposer: B - Under rule 1, the Preferred Qualifications sentence 'building AI testing frameworks, autonomous testing agents or intelligent automation solutions' names an automation skill as a qualification, and the nice_to_have requirement and quote
- judge: drop - Under rule 5, the phrase 'intelligent automation solutions' refers to AI testing automation rather than expressly naming workflow automation, so the skill should be dropped.

### 20261119T142629Z_label item 21 - golden_101 `machine-learning` (disagreement)
> ...& Scalable Systems TikTok USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search, and e-commerce systems. You...
- A: `machine-learning` · required · raw_text: "seeking a PhD-level candidate to advance machine learning"
- B: (did not label this)
- proposer: A - Under rule 1, the sentence "seeking a PhD-level candidate to advance machine learning" is a candidate-facing qualification that names the skill, not just the job title, and under rule 3 the required framing stands, so labeler A's requir
- judge: drop - Under rules 1 and 4, 'seeking a PhD-level candidate to advance machine learning' describes the role's objective/responsibility rather than a qualification asking the candidate to possess machine learning skill, and the job title does not co

### 20261119T142629Z_label item 22 - golden_101 `recommender-systems` (disagreement)
> ...USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search, and e-commerce systems. You will design scalable...
- A: `recommender-systems` · required · raw_text: "advance machine learning across recommendation"
- B: (did not label this)
- proposer: A - Under rule 3, the candidate is sought "to advance machine learning across recommendation" systems, so the required mention of recommendation work stands as labeled by A, and rule 4 does not exclude it because the candidate is explicitly
- judge: drop - Under rule 4, the excerpt only describes the responsibilities and scope of the role ('to advance machine learning across recommendation... systems') rather than asking the candidate for recommender systems as a qualification.

### 20261119T142629Z_label item 26 - golden_104 `data-pipelines` (disagreement)
> ...systems • Understand that the hardest problems are in data ingestion, normalization, temporal alignment and ground truth •...
- A: (did not label this)
- B: `data-pipelines` · required · raw_text: "data ingestion"
- proposer: B - Under rule 1, the 'Who you are' qualification sentence names data ingestion ('the hardest problems are in data ingestion, normalization, temporal alignment'), which supports data-pipelines as required, and rule 3 keeps that required men
- judge: drop - Under Rule 5, the posting mentions 'data ingestion' as a conceptual problem rather than naming the broader skill 'data-pipelines'.

### 20261119T142629Z_label item 27 - golden_106 `mlops` (disagreement)
> ...capabilities. What you'll need to succeed 8+ years building and operating production ML systems, ideally in fraud, abuse, risk, identity, trust & safety,...
- A: (did not label this)
- B: `mlops` · required · raw_text: "building and operating production ML systems"
- proposer: B - Under rule 3, the required qualification "building and operating production ML systems" (with the required bullet on taking ML systems to production deployment and monitoring) supports mlops, and labeler A did not label it, so B's requi
- judge: drop - Under Rule 5, the posting never names MLOps, so we do not infer or add a skill that the text does not name.

### 20261119T142629Z_label item 42 - golden_097 `nlp` (uncertain)
> ...in one or more of the following fields: Machine Learning, Natural Language Processing (NLP), or Computer Vision. • Proficiency in software development...
- A: `nlp` · required · raw_text: "Natural Language Processing (NLP)"
- B: `nlp` · required · raw_text: "Natural Language Processing (NLP)"
- proposer: {"requirement": "nice_to_have", "raw_text": "multilingual NLP"} - Under rule 1 the required 'Natural Language Processing (NLP)' is only inside a years-of-experience line, which does not count, but the preferred bullet 'Proficiency in multil
- judge: ok - Under Rule 1, a qualification bullet that names a specific skill like 'Natural Language Processing (NLP)' counts even if it includes a years-of-experience requirement, as Rule 1 only excludes generic job-title experience lines.

### 20261119T142629Z_label item 48 - golden_100 `software-engineering` (uncertain)
> ...engineering, or a related field.- At least 3 years of experience in software engineering and be proficient in developing using common programming...
- A: `software-engineering` · required · raw_text: "experience in software engineering"
- B: `software-engineering` · required · raw_text: "experience in software engineering"
- proposer: drop - Under rule 1, the only mention is the years-of-experience line "At least 3 years of experience in software engineering," which does not count as a skill, and the other occurrence is a degree field in the education line, so the skill 
- judge: ok - Under Rule 1, a qualification bullet that names a skill ('experience in software engineering') counts, as it is not a job title line ('experience as a software engineer').

### 20261119T142629Z_label item 53 - golden_103 `devops` (uncertain)
> ...of experience in software engineering, ML engineering, or MLOps/DevOps, focusing on the ML lifecycle (continuous training, model...
- A: `devops` · required · raw_text: "MLOps/DevOps"
- B: `devops` · required · raw_text: "DevOps"
- proposer: drop - Under rule 1, the only mention of DevOps is inside the 8+ years of experience line ('experience in software engineering, ML engineering, or MLOps/DevOps'), which is a years-of-experience line and does not count as naming a skill; the
- judge: ok - Under Rule 1, a qualification bullet that names a skill counts; the rule only excludes generic job-role experience lines ("experience as a software engineer"), not specific technical skills like DevOps named in a qualifications sentence.

### 20261119T142629Z_label item 66 - golden_106 `observability` (uncertain)
> ...guiding ML systems from feature engineering to production deployment and monitoring. Strong software/data engineering skills across ML,...
- A: `observability` · required · raw_text: "production deployment and monitoring"
- B: `observability` · required · raw_text: "monitoring"
- proposer: ok - Under rule 1, the required qualification bullet names monitoring of production ML systems ("production deployment and monitoring"), which is a reasonable mapping to observability, and rule 5 doesn't block it because the text names moni
- judge: drop - Under Rule 5, the text only mentions ML model monitoring ('production deployment and monitoring'), which does not directly name the broader infrastructure skill 'observability'.

## 2. No model could rule (32)

A labeler disagreement the proposer answered unusably (no valid answer, or `ok` on a disagreement), so the judge never saw it.

### 20261119T141542Z_label item 52 - golden_098 `seniority` (uncertain)
> ...Specific Knowledge and Skills Bachelor's Degree 2+ years of experience in software development Legal authorization to work in the U.S. indefinitely is...
- A: value="junior" · basis="inferred" · signal="2+ years of experience in software development"
- B: value="junior" · basis="inferred" · signal="2+ years of experience in software development"

### 20261119T103427Z_label item 16 - golden_094 `distributed-systems` (disagreement)
> ...experience. - You have architected and delivered complex distributed control systems, industrial automation, datacenter infrastructure, or...
- A: (did not label this)
- B: `distributed-systems` · required · raw_text: "distributed control systems"

### 20261119T103427Z_label item 18 - golden_094 `software-architecture` (disagreement)
> ...and fault detection. - You can set technical direction, make architecture decisions, and lead complex cross-functional engineering programs...
- A: (did not label this)
- B: `software-architecture` · required · raw_text: "make architecture decisions"

### 20261119T103427Z_label item 35 - golden_105 `ai-ml` (disagreement)
> ...manual steps and making PPA exploration repeatable. - Building with AI as part of how you develop flows, and opinionated about where LLMs and ML-driven...
- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Building with AI as part of how you develop flows"

### 20261119T103427Z_label item 56 - golden_101 `gcp` (uncertain)
> ...- Experience with cloud computing services (AWS, Azure, GCP). - Knowledge of Big Data technologies (Hadoop,...
- A: `gcp` · nice_to_have · raw_text: "GCP"
- B: `gcp` · nice_to_have · raw_text: "GCP"

### 20261119T110104Z_label item 11 - golden_095 `agents` (disagreement)
> ...and interpretation. FL127 is an AI-native company. Team members direct AI agents in their daily work for literature synthesis, study design, data analysis, and code. We are looking for someone who wants to work this way. KEY RESPONSIBILITIES - Ground e...
- A: (did not label this)
- B: `agents` · nice_to_have · raw_text: "Team members direct AI agents in their daily work for literature synthesis, study design, data analysis, and code. We are looking for someone who wants to work this way."

### 20261119T110104Z_label item 16 - golden_100 `hallucination-detection` (disagreement)
> ...biology, scientific credibility, model limitations, hallucination risk, interpretability, and validation. - Experience leading...
- A: `hallucination-detection` · required · raw_text: "hallucination risk"
- B: (did not label this)

### 20261119T110104Z_label item 19 - golden_101 `llms` (disagreement)
> ...spec, cheminformatics/docking/ADMET, biophysics/MD, and LLM/agentic automation. - MLOps expertise: data contracts and lineage (e.g.,...
- A: `llms` · nice_to_have · raw_text: "LLM/agentic automation"
- B: `llms` · required · raw_text: "spin up LLM based agents"

### 20261119T112034Z_label item 16 - golden_094 `machine-learning` (disagreement)
> ...shape over time. - Curiosity and enthusiasm for AI. Experience training ML models and operating them in production at scale is a significant...
- A: (did not label this)
- B: `machine-learning` · nice_to_have · raw_text: "Experience training ML models"

### 20261119T112034Z_label item 34 - golden_103 `ai-infrastructure` (disagreement)
> ...Building agent harnesses, distributed training systems, or scalable inference infrastructure. - Large-scale retrieval, ranking, or recommendation...
- A: `ai-infrastructure` · nice_to_have · raw_text: "scalable inference infrastructure"
- B: (did not label this)

### 20261119T112034Z_label item 54 - golden_095 `explainable-ai` (uncertain)
> ...working in regulated environments or with products where explainability, auditability and customer trust are especially...
- A: `explainable-ai` · nice_to_have · raw_text: "explainability"
- B: `explainable-ai` · nice_to_have · raw_text: "explainability"

### 20261119T112034Z_label item 64 - golden_100 `agents` (uncertain)
> ...building and deploying LLM-powered applications or AI agents in production - Experience with modern LLM tooling such as LangChain,...
- A: `agents` · required · raw_text: "AI agents in production"
- B: `agents` · required · raw_text: "AI agents"

### 20261119T114422Z_label item 26 - golden_102 `recommender-systems` (disagreement)
> ...with human evaluation, LLM-as-judge calibration, recommendation metrics or online experimentation. - Contributions to evaluation...
- A: `recommender-systems` · nice_to_have · raw_text: "recommendation metrics"
- B: (did not label this)

### 20261119T114422Z_label item 43 - golden_097 `full-stack-development` (uncertain)
> ...code. Ideally experienced in Go, Python or TypeScript. Backend or full-stack background both fine. - Real hands-on experience with agents or...
- A: `full-stack-development` · required · raw_text: "Backend or full-stack background"
- B: `full-stack-development` · required · raw_text: "full-stack background"

### 20261119T114422Z_label item 53 - golden_098 `transformers` (uncertain)
> ...with production experience using training libraries (Transformers, DeepSpeed, Accelerate) - Strong software engineering practices:...
- A: `transformers` · required · raw_text: "Transformers, DeepSpeed"
- B: `transformers` · required · raw_text: "Transformers"

### 20261119T114422Z_label item 72 - golden_105 `distributed-systems` (uncertain)
> ...for availability, reliability and scalability, with varied interests in algorithms and distributed systems. Responsibilities - Be on an on-call (PagerDuty)...
- A: `distributed-systems` · nice_to_have · raw_text: "interests in algorithms and distributed systems"
- B: `distributed-systems` · nice_to_have · raw_text: "with varied interests in algorithms and distributed systems"

### 20261119T135145Z_label item 58 - golden_100 `reinforcement-learning` (uncertain)
> ...for physics (CUDA, NVIDIA Warp or JAX) and experience scaling simulation for reinforcement or imitation learning. - Experience with deformable, cable or FEM simulation...
- A: `reinforcement-learning` · nice_to_have · raw_text: "scaling simulation for reinforcement or imitation learning"
- B: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement or imitation learning"

### 20261119T140709Z_label item 24 - golden_103 `evaluation` (disagreement)
> ...strategy across client engagements - Establishing rigorous AI evaluation standards covering failure modes, bias, drift,...
- A: `evaluation` · nice_to_have · raw_text: "AI evaluation"
- B: `evaluation` · required · raw_text: "AI evaluation standards"

### 20261119T140709Z_label item 29 - golden_105 `software-architecture` (disagreement)
> ...contributing to engineering workshops, live prototyping, architecture reviews, and client demos. • Experience building cyber evaluation...
- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architecture reviews"

### 20261119T140709Z_label item 34 - golden_108 `data-privacy-and-security` (disagreement)
> ...and data integration experience • Strong understanding of secure healthcare application development AI Experience • Experience building AI-powered...
- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "secure healthcare application development"

### 20261119T140709Z_label item 46 - golden_096 `machine-learning` (uncertain)
> ...and model capabilities. Required Qualifications • 8+ years of experience in machine learning, data, or software engineering, including 3+ years...
- A: `machine-learning` · required · raw_text: "8+ years of experience in machine learning"
- B: `machine-learning` · required · raw_text: "Hands-on experience with graph machine learning is required."

### 20261119T140709Z_label item 64 - golden_105 `aws` (uncertain)
> ...services • Cloud engineering and secure AI deployment on AWS, Azure, or GCP • API integration with SIEM, SOAR, EDR,...
- A: `aws` · required · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

### 20261119T141542Z_label item 19 - golden_094 `data-modeling` (disagreement)
> ...or similar - Familiarity with semantic layer creation, conceptual modeling, and query optimization - Applying complex data analysis...
- A: `data-modeling` · nice_to_have · raw_text: "conceptual modeling"
- B: `data-modeling` · required · raw_text: "conceptual modeling"

### 20261119T141542Z_label item 35 - golden_099 `structured-data-extraction` (disagreement)
> ...data backend for active, production AI applications and unstructured document parsing. • Proficiency with AI coding tools and strong...
- A: `structured-data-extraction` · required · raw_text: "unstructured document parsing"
- B: (did not label this)

### 20261119T141542Z_label item 41 - golden_101 `mlops` (disagreement)
> ...RAG, vector search, or shared enterprise AI platforms.-GenAIOps, MLOps, AgentOps, model/endpoint lifecycle management, prompt/agent...
- A: `mlops` · nice_to_have · raw_text: "GenAIOps, MLOps, AgentOps"
- B: `mlops` · required · raw_text: "model and endpoint operations"

### 20261119T141542Z_label item 83 - golden_105 `prompt-engineering` (uncertain)
> ...LLaVA-, Qwen-VL-, or PaliGemma-style models): fine-tuning, prompting, grounding, and evaluation. • Experience with VLAs or...
- A: `prompt-engineering` · required · raw_text: "prompting"
- B: `prompt-engineering` · required · raw_text: "prompting"

### 20261119T142629Z_label item 45 - golden_100 `distributed-systems` (uncertain)
> ...languages (such as Python and Golang).- In-depth understanding of distributed computing and principles and technologies of large-scale data...
- A: `distributed-systems` · required · raw_text: "understanding of distributed computing"
- B: `distributed-systems` · required · raw_text: "distributed computing"

### 20261119T142629Z_label item 47 - golden_100 `python` (uncertain)
> ...in developing using common programming languages (such as Python and Golang).- In-depth understanding of distributed...
- A: `python` · required · raw_text: "Python"
- B: `python` · required · raw_text: "Python"

### 20261119T142629Z_label item 71 - golden_108 `agent-state-management` (uncertain)
> ...(e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience...
- A: `agent-state-management` · nice_to_have · raw_text: "Guardrails, Memory"
- B: `agent-state-management` · nice_to_have · raw_text: "Memory"

### 20261119T135145Z_label item 56 - golden_100 `degree` (uncertain)
> ...trust it. What You’ll Need: Minimum Qualifications: - PhD in robotics, mechanical engineering, applied mathematics, physics, computer graphics or a related field, or a Masters + 3 years of experience. Exceptional candidates with a bachelor’s degree and 3+...
- A: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in robotics, mechanical engineering, applied mathematics, physics, computer graphics or a related field, or a Masters + 3 years of experience"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in robotics, mechanical engineering, applied mathematics, physics, computer graphics or a related field, or a Masters + 3 years of experience. Exceptional candidates with a bachelor’s degree and 3+ years of relevant industry experience are also welcome to apply."
- proposer: no usable answer (its reply was not in the form asked for), so the judge never saw it

### 20261119T142629Z_label item 49 - golden_101 `degree` (uncertain)
> ...& Scalable Systems TikTok USDS Joint Venture is seeking a PhD-level candidate to advance machine learning across recommendation, search,...
- A: value="phd" · requirement="required" · or_equivalent=false · signal="PhD-level candidate"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="PhD-level candidate"
- proposer: no usable answer (its reply was not in the form asked for), so the judge never saw it

### 20261119T142629Z_label item 69 - golden_108 `degree` (uncertain)
> ...developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields plus at least 2 years of experience developing AI and ML...
- A: value="master" · requirement="required" · or_equivalent=false · signal="a Master's degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields"
- B: value="master" · requirement="required" · or_equivalent=false · signal="Bachelor's Degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields plus at least 4 years of experience developing AI and ML algorithms or technologies, or a Master's degree in Computer Science, AI, Electrical Engineering, Computer Engineering, or related fields plus at least 2 years of experience developing AI and ML algorithms or technologies"
- proposer: no usable answer (its reply was not in the form asked for), so the judge never saw it

## 3. Degree: the two models split (0)

These batches were labelled before the rule changed to *record the lowest degree level the posting names* (a 'Bachelor's, MS or PhD preferred' posting is `bachelor`). Every degree label was read again under that rule by the proposer and the judge; where they agreed it is settled. None are left here: the two models agreed on all 77 they both answered. The three where the proposer gave no usable answer are at the end of group 2; answer those by the new rule.

## 4. Any-one-of groups the two models did not settle (17)

Which of a posting's skills it accepts *any one of* ("Python, or Bash scripting": Python and Bash share a group; each keeps its own required or nice-to-have). The proposer and the judge each read the whole posting under the labelling guide's alternative_group section; where they named the same groups it is settled. Here they did not, or one gave no usable answer. Write the groups as a list of skill-id lists, e.g. `[["bash", "python"]]`, or `[]` for none. Only the skills listed can be grouped.

### 20261119T103427Z_label item 166 - golden_104 `alternative_group` (groups)
> AI Research Scientist
- skill: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving ML techniques"
- skill: `deep-learning` · required · raw_text: "deep learning architectures"
- skill: `distributed-training` · nice_to_have · raw_text: "Experience with distributed training"
- skill: `evaluation` · required · raw_text: "validating ML model performance"
- skill: `fine-tuning` · required · raw_text: "fine-tuning large-scale models"
- skill: `jax` · required · raw_text: "JAX"
- skill: `knowledge-distillation` · required · raw_text: "distillation"
- skill: `llms` · nice_to_have · raw_text: "Research experience in generative AI"
- skill: `machine-learning` · required · raw_text: "machine learning research"
- skill: `model-development` · required · raw_text: "AI model development"
- skill: `python` · required · raw_text: "Proficiency in Python"
- skill: `pytorch` · required · raw_text: "PyTorch"
- skill: `quantization` · required · raw_text: "quantization, distillation, pruning"
- skill: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning"
- skill: `tensorflow` · required · raw_text: "TensorFlow"
- skill: `transformers` · required · raw_text: "transformers, CNNs, RNNs"
- proposer: [["pytorch", "tensorflow", "jax"]] - The qualifications ask for "ML frameworks such as PyTorch, TensorFlow, or JAX", where the "X, Y or Z" and "such as" markers offer any one example for a single ask, so these three form one group, while Python is asked separately and stays out.
- judge: [["pytorch", "tensorflow", "jax"], ["llms", "reinforcement-learning"]] - Per the Markers rule for 'X, Y or Z' and examples offered for a single ask, 'ML frameworks such as PyTorch, TensorFlow, or JAX' groups pytorch, tensorflow, and jax, and 'Research experience in generative AI, reinforcement learning, or multimodal learning' groups llms and reinforcement-learning (while machine-learning and model-development are also required on their own elsewhere in the posting and leave their group).

### 20261119T103427Z_label item 168 - golden_106 `alternative_group` (groups)
> Staff Design Verification Engineer, AI HW
- skill: `bash` · required · raw_text: "Bash scripting"
- skill: `ci-cd` · required · raw_text: "manage CI pipelines"
- skill: `linux` · required · raw_text: "Proficient in Linux environments"
- skill: `python` · required · raw_text: "with Python, or Bash scripting"
- proposer: [["bash", "python"]] - The alternative_group rule's markers include 'X, Y or Z' and 'X or Y', and 'Proficient in Linux environments with Python, or Bash scripting' offers either scripting language for one ask, while bash appears nowhere else as a standalone requirement, so bash and python form one group and linux and ci-cd stay out.
- judge: [] - Under the rule that 'A skill also asked for on its own elsewhere in the posting... is a requirement on its own: it leaves the group,' Python leaves the 'Python, or Bash scripting' group because 'Build and maintain reusable verification environments... in SystemVerilog and Python' asks for Python on its own, leaving fewer than two skills in the group.

### 20261119T112034Z_label item 167 - golden_095 `alternative_group` (groups)
> Lead Machine Learning Scientist, Business Banking
- skill: `a-b-testing` · nice_to_have · raw_text: "A/B tests"
- skill: `agents` · nice_to_have · raw_text: "agentic workflows"
- skill: `ai-deployment` · required · raw_text: "shipping state-of-the-art ML models to production"
- skill: `ai-ml` · required · raw_text: "thoughtful about responsible ML/AI"
- skill: `evaluation` · nice_to_have · raw_text: "evaluation frameworks"
- skill: `explainable-ai` · nice_to_have · raw_text: "explainability"
- skill: `forecasting` · nice_to_have · raw_text: "forecasting"
- skill: `go` · nice_to_have · raw_text: "keen to learn Go"
- skill: `llms` · nice_to_have · raw_text: "Experience with GenAI, LLMs"
- skill: `machine-learning` · required · raw_text: "leading the development and deployment of advanced Machine Learning models"
- skill: `microservices` · nice_to_have · raw_text: "working with microservices"
- skill: `model-development` · required · raw_text: "development and deployment of advanced Machine Learning models"
- skill: `python` · required · raw_text: "You speak Python fluently"
- skill: `recommender-systems` · nice_to_have · raw_text: "recommendation"
- skill: `scikit-learn` · required · raw_text: "extensive, hands-on experience with scikit-learn"
- skill: `software-engineering` · nice_to_have · raw_text: "writing critical production code"
- skill: `sql` · required · raw_text: "You are comfortable using SQL"
- proposer: [] - The 'Experience with GenAI, LLMs, agentic workflows, retrieval, evaluation frameworks, or human-in-the-loop' list is an 'or' alternative set, but its labeled members llms and evaluation are also asked on their own in the responsibilities (LLM-powered experiences; design robust evaluation), which removes them from the group and leaves fewer than two members, so under the 'a group needs at least two skills' and 'asked on its own elsewhere' rules there is no group.
- judge: [["forecasting", "recommender-systems"], ["agents", "evaluation", "llms"]] - Under the 'X, Y or Z' marker rule, the nice-to-have bullets 'personalisation, ranking, recommendation, forecasting, classification or decisioning problems' and 'Experience with GenAI, LLMs, agentic workflows, retrieval, evaluation frameworks, or human-in-the-loop product experiences' each offer their labeled skills as alternatives for a single ask.

### 20261119T112034Z_label item 175 - golden_103 `alternative_group` (groups)
> Member of Technical Staff (Machine Learning Engineer, Search Agent RL)
- skill: `agent-architecture` · nice_to_have · raw_text: "Building agent harnesses"
- skill: `agents` · required · raw_text: "or agent systems"
- skill: `ai-infrastructure` · nice_to_have · raw_text: "scalable inference infrastructure"
- skill: `distributed-training` · nice_to_have · raw_text: "distributed training systems"
- skill: `evaluation` · required · raw_text: "designing rigorous evaluations"
- skill: `ml-engineering` · required · raw_text: "building and shipping ML systems"
- skill: `model-development` · required · raw_text: "model training"
- skill: `multi-agent-systems` · nice_to_have · raw_text: "Multi-agent training, coordination, or evaluation"
- skill: `recommender-systems` · nice_to_have · raw_text: "recommendation systems"
- skill: `reinforcement-learning` · required · raw_text: "reinforcement learning, search and retrieval"
- skill: `software-engineering` · required · raw_text: "Strong software engineering skills"
- skill: `tool-calling` · nice_to_have · raw_text: "training models to use tools"
- proposer: [] - The 'one or more of' qualification names reinforcement learning and agent systems, but reinforcement learning is also asked on its own in the responsibilities ('Develop LLM post-training methods, including reinforcement learning'), so it leaves the group and only `agents` remains, below the two-skill minimum.
- judge: [["distributed-training", "ai-infrastructure"]] - `reinforcement-learning`, `agents`, and `agent-architecture` are all asked for on their own in the Responsibilities section and thus leave their respective alternative groups, leaving only `distributed-training` and `ai-infrastructure` grouped under the 'X, Y or Z' marker in 'Building agent harnesses, distributed training systems, or scalable inference infrastructure'.

### 20261119T114422Z_label item 160 - golden_097 `alternative_group` (groups)
> Developer Advocate, Toqan (Prosus AI Platform)
- skill: `agents` · required · raw_text: "hands-on experience with agents"
- skill: `ai-developer-tooling` · required · raw_text: "AI coding tools"
- skill: `aws` · required · raw_text: "AWS or GCP"
- skill: `backend-development` · required · raw_text: "Backend or full-stack background"
- skill: `claude-code` · required · raw_text: "Claude Code"
- skill: `cloud` · required · raw_text: "Some cloud experience"
- skill: `codex` · required · raw_text: "Codex"
- skill: `containerization` · nice_to_have · raw_text: "containers"
- skill: `cursor` · required · raw_text: "Cursor"
- skill: `docker` · required · raw_text: "Docker"
- skill: `full-stack-development` · required · raw_text: "Backend or full-stack background"
- skill: `gcp` · required · raw_text: "AWS or GCP"
- skill: `git` · required · raw_text: "Git and GitHub workflows"
- skill: `github-copilot` · required · raw_text: "Copilot"
- skill: `go` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"
- skill: `llms` · required · raw_text: "LLM-based systems"
- skill: `mcp` · required · raw_text: "MCP server infrastructure"
- skill: `python` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"
- skill: `software-engineering` · required · raw_text: "professional software engineering experience"
- skill: `tool-calling` · required · raw_text: "tool call"
- skill: `typescript` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"
- proposer: no usable answer (its reply was not in the form asked for), so the judge never saw it

### 20261119T114422Z_label item 161 - golden_098 `alternative_group` (groups)
> Machine Learning Engineer - LLMs
- skill: `ai-deployment` · required · raw_text: "deploying language models to production"
- skill: `ci-cd` · required · raw_text: "CI/CD"
- skill: `data-pipelines` · nice_to_have · raw_text: "synthetic data generation pipelines"
- skill: `deepspeed` · required · raw_text: "Transformers, DeepSpeed, Accelerate"
- skill: `distributed-systems` · required · raw_text: "deep understanding of distributed systems"
- skill: `distributed-training` · required · raw_text: "distributed training frameworks"
- skill: `embeddings` · required · raw_text: "(embedding models"
- skill: `evaluation` · required · raw_text: "rigorous evaluation"
- skill: `fine-tuning` · required · raw_text: "or fine-tuning"
- skill: `fsdp` · required · raw_text: "FSDP"
- skill: `git` · required · raw_text: "version control"
- skill: `hugging-face` · nice_to_have · raw_text: "released models on Hugging Face"
- skill: `inference-optimization` · nice_to_have · raw_text: "optimizing models for production inference"
- skill: `knowledge-distillation` · nice_to_have · raw_text: "distillation"
- skill: `llms` · required · raw_text: "or large language models"
- skill: `megatron-lm` · required · raw_text: "Megatron-LM, or Axolotl"
- skill: `model-development` · required · raw_text: "training and deploying language models"
- skill: `model-serving` · nice_to_have · raw_text: "serving frameworks"
- skill: `open-source-llms` · nice_to_have · raw_text: "open-source LLM training projects or tools"
- skill: `python` · required · raw_text: "Expert Python"
- skill: `pytorch` · required · raw_text: "PyTorch"
- skill: `quantization` · nice_to_have · raw_text: "quantization"
- skill: `reinforcement-learning` · nice_to_have · raw_text: "other reinforcement learning approaches"
- skill: `software-engineering` · required · raw_text: "Strong software engineering practices"
- skill: `testing` · required · raw_text: "testing"
- skill: `transformers` · required · raw_text: "Transformers, DeepSpeed"
- skill: `vllm` · nice_to_have · raw_text: "vLLM"
- proposer: [["fsdp", "megatron-lm"], ["embeddings", "llms"]] - Under the alternative_group rule, the 'distributed training frameworks (DeepSpeed, FSDP, Megatron-LM, or Axolotl)' ask leaves deepspeed out because it reappears as an unmarked tech-stack entry, so fsdp and megatron-lm remain as a two-skill group, and the 'embedding models, encoder models, or large language models' examples for one training-experience ask group embeddings and llms.
- judge: [["fsdp", "megatron-lm"]] - The distributed training frameworks ask offers DeepSpeed, FSDP, Megatron-LM, or Axolotl as alternatives, leaving `fsdp` and `megatron-lm` grouped after `deepspeed` leaves the group because it is asked for on its own in 'training libraries (Transformers, DeepSpeed, Accelerate)'; similarly, `llms` is required on its own elsewhere in the posting ('Train large language models for our domain'), leaving `embeddings` without a partner.

### 20261119T114422Z_label item 165 - golden_102 `alternative_group` (groups)
> Senior Machine Learning Engineer, Evals
- skill: `a-b-testing` · nice_to_have · raw_text: "online experimentation"
- skill: `agents` · nice_to_have · raw_text: "agent or gaming environments"
- skill: `evaluation` · required · raw_text: "owning evaluation frameworks"
- skill: `fine-tuning` · nice_to_have · raw_text: "post-training"
- skill: `llms` · nice_to_have · raw_text: "language-model training"
- skill: `machine-learning` · required · raw_text: "building and evaluating ML systems"
- skill: `model-development` · nice_to_have · raw_text: "language-model training"
- skill: `python` · required · raw_text: "Strong Python"
- skill: `pytorch` · required · raw_text: "PyTorch"
- skill: `recommender-systems` · nice_to_have · raw_text: "recommendation metrics"
- skill: `software-engineering` · required · raw_text: "reliable production software development"
- skill: `statistics` · required · raw_text: "experimental design and statistics"
- skill: `transformers` · required · raw_text: "Transformers"
- proposer: [["fine-tuning", "model-development"], ["a-b-testing", "recommender-systems"], ["pytorch", "transformers"]] - Under the alternative_group rule's markers ('X or Y' and 'X, Y or comparable' for a single ask), the posting offers post-training or language-model training, human evaluation/LLM-as-judge/recommendation metrics/online experimentation, and PyTorch or Transformers as one-of options, while 'or comparable' adds nothing and llms is left out as it is not clearly a named alternative member.
- judge: [["pytorch", "transformers"], ["fine-tuning", "llms", "model-development"], ["a-b-testing", "recommender-systems"]] - The posting uses 'X, Y or Z' markers to offer 'PyTorch, Transformers or comparable ML libraries' (where 'or comparable' adds nothing), 'language-model training or post-training' (which includes both `llms` and `model-development` labeled from 'language-model training'), and 'human evaluation, LLM-as-judge calibration, recommendation metrics or online experimentation' as alternatives for single asks.

### 20261119T114422Z_label item 166 - golden_103 `alternative_group` (groups)
> Senior Backend Engineer, AI Platform (Toqan)
- skill: `agent-architecture` · required · raw_text: "Familiarity with agentic architectures"
- skill: `agents` · nice_to_have · raw_text: "Hands-on experience building agentic AI systems"
- skill: `ai-developer-tooling` · required · raw_text: "Regular, thoughtful use of AI coding tools"
- skill: `ai-infrastructure` · nice_to_have · raw_text: "Experience with AI or ML infrastructure"
- skill: `ai-ml` · required · raw_text: "the AI and LLM space — not as a trend to track, but as a domain where you've already done hands-on integration work"
- skill: `aws` · required · raw_text: "Hands-on AWS experience"
- skill: `backend-development` · required · raw_text: "building and operating production backend services"
- skill: `ci-cd` · required · raw_text: "Experience with CI/CD"
- skill: `claude-code` · required · raw_text: "Claude Code"
- skill: `cloud` · required · raw_text: "cloud-native services"
- skill: `codex` · required · raw_text: "OpenAI Codex"
- skill: `cursor` · required · raw_text: "Cursor"
- skill: `event-driven-systems` · nice_to_have · raw_text: "Experience building or maintaining event-sourced systems"
- skill: `github-copilot` · required · raw_text: "GitHub Copilot"
- skill: `go` · required · raw_text: "Strong Go programming skills"
- skill: `llms` · required · raw_text: "Experience integrating LLMs"
- skill: `mcp` · required · raw_text: "protocols such as MCP"
- skill: `observability` · required · raw_text: "production observability"
- skill: `python` · nice_to_have · raw_text: "Python programming skills"
- skill: `software-architecture` · required · raw_text: "owning architectural decisions"
- skill: `testing` · required · raw_text: "automated testing"
- skill: `tool-calling` · required · raw_text: "tool-calling systems"
- proposer: [["claude-code", "cursor", "github-copilot", "codex"]] - The line "regular, thoughtful use of AI coding tools ... whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex" gives examples offered for one ask, so under the markers section these four form one group, while the broad `ai-developer-tooling` skill stays out as the parent of its examples.
- judge: [["claude-code", "cursor", "github-copilot", "codex"], ["llms", "tool-calling"]] - Under the Markers bullet ('X, Y or Z' and examples offered for a single ask), 'whether that's Claude Code, Cursor, GitHub Copilot, or OpenAI Codex' groups `claude-code`, `cursor`, `github-copilot`, and `codex` (leaving the broad skill `ai-developer-tooling` out), and 'Experience integrating LLMs, AI models or tool-calling systems into production applications' groups `llms` and `tool-calling`.

### 20261119T135145Z_label item 171 - golden_096 `alternative_group` (groups)
> AI Inference Infrastructure Software Engineer (Kubernetes / Cloud)
- skill: `ansible` · required · raw_text: "Ansible"
- skill: `apis` · nice_to_have · raw_text: "customer facing API platforms"
- skill: `argocd` · required · raw_text: "Argo CD"
- skill: `aws` · required · raw_text: "operating workloads on AWS or GCP"
- skill: `bash` · required · raw_text: "Bash"
- skill: `gcp` · required · raw_text: "operating workloads on AWS or GCP"
- skill: `gitops` · required · raw_text: "GitOps workflows"
- skill: `go` · required · raw_text: "proficiency in Go"
- skill: `infrastructure-as-code` · required · raw_text: "infrastructure-as-code"
- skill: `kubernetes` · required · raw_text: "hands-on Kubernetes experience"
- skill: `linux` · required · raw_text: "Proficient in configuring and leveraging Linux OS in production"
- skill: `model-development` · required · raw_text: "AI inference and/or training workflows"
- skill: `model-serving` · nice_to_have · raw_text: "model-serving patterns"
- skill: `networking` · required · raw_text: "networking, and storage considerations"
- skill: `observability` · nice_to_have · raw_text: "Background in observability"
- skill: `python` · required · raw_text: "Solid coding skills in Python"
- skill: `terraform` · required · raw_text: "Terraform"
- skill: `triton-inference-server` · nice_to_have · raw_text: "Triton"
- skill: `vllm` · nice_to_have · raw_text: "vLLM"
- proposer: [] - The only alternative marker is "operating workloads on AWS or GCP", but the responsibilities separately ask to "Manage and harden our AWS, GCP, and on-prem infrastructure", so aws and gcp are each asked for on their own and leave the group. The other parenthetical examples (Terraform/Pulumi, Ansible/Puppet/Salt, Argo CD/Flux) include only one labeled skill or name a broad parent alongside its examples, so they form no group.
- judge: [["triton-inference-server", "vllm"]] - Under the rule for examples offered for a single ask, 'inference servers and runtimes (e.g., Triton, vLLM, TGI)' groups `triton-inference-server` and `vllm`, whereas `aws` and `gcp` leave their group because they are also asked for together in the responsibilities ('AWS, GCP, and on-prem infrastructure') and the other parenthetical examples have only one labeled skill each.

### 20261119T135145Z_label item 181 - golden_106 `alternative_group` (groups)
> AI Software Engineer
- skill: `ai-deployment` · required · raw_text: "model deployment internals"
- skill: `ai-infrastructure` · required · raw_text: "ML infrastructure"
- skill: `containerization` · nice_to_have · raw_text: "containerized deployments"
- skill: `cpp` · required · raw_text: "Proficient in C++"
- skill: `cuda` · required · raw_text: "CUDA"
- skill: `deepspeed` · required · raw_text: "DeepSpeed-Inference"
- skill: `distributed-systems` · nice_to_have · raw_text: "Exposure to distributed systems"
- skill: `docker` · nice_to_have · raw_text: "Docker/Kubernetes"
- skill: `kubernetes` · nice_to_have · raw_text: "Docker/Kubernetes"
- skill: `model-serving` · required · raw_text: "LLM serving frameworks"
- skill: `python` · required · raw_text: "C++ and Python"
- skill: `sglang` · required · raw_text: "SGLang, TensorRT-LLM"
- skill: `tensorrt` · required · raw_text: "TensorRT-LLM, DeepSpeed-Inference"
- skill: `vllm` · required · raw_text: "vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference"
- proposer: [] - The 'one or more of' list in the required qualifications would group vllm, sglang, tensorrt and deepspeed, but the role summary asks for vllm, SGLang and TensorRT-LLM together as frameworks the engineer hacks, an unmarked tech-stack entry, so those three leave the group and only deepspeed remains, below the two-skill minimum.
- judge: [["vllm", "sglang", "tensorrt", "deepspeed"]] - The posting requires familiarity with 'one or more LLM serving frameworks (vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference, etc.)', and the earlier mention ('frameworks like vLLM, SGLang, and TensorRT-LLM') also offers them as examples for a single ask rather than standalone requirements, so all four remain grouped under the 'one or more of' and example markers.

### 20261119T140709Z_label item 167 - golden_102 `alternative_group` (groups)
> Senior Data Engineer, Taxonomy, AI Data Modeling, MLOps, YouTube Business
- skill: `ai-developer-tooling` · nice_to_have · raw_text: "AI coding tools"
- skill: `apis` · nice_to_have · raw_text: "building APIs"
- skill: `data-pipelines` · required · raw_text: "production ETL/ELT pipelines"
- skill: `embeddings` · nice_to_have · raw_text: "vector embeddings"
- skill: `evaluation` · nice_to_have · raw_text: "evaluation golden sets"
- skill: `llms` · nice_to_have · raw_text: "LLM compute unit economics"
- skill: `machine-learning` · required · raw_text: "machine learning data pipelines"
- skill: `nlp` · required · raw_text: "natural language processing (NLP)"
- skill: `python` · required · raw_text: "Python"
- skill: `sql` · required · raw_text: "SQL for data analysis"
- proposer: no usable answer (its reply was not in the form asked for), so the judge never saw it

### 20261119T141542Z_label item 168 - golden_099 `alternative_group` (groups)
> AI Data Engineer (remote)
- skill: `ai-developer-tooling` · required · raw_text: "Proficiency with AI coding tools"
- skill: `azure` · required · raw_text: "Python, Microsoft Azure"
- skill: `backend-development` · required · raw_text: "supporting the data backend"
- skill: `cloud` · required · raw_text: "modern cloud data platforms"
- skill: `databricks` · required · raw_text: "or Databricks"
- skill: `mcp` · nice_to_have · raw_text: "Bonus: Experience with MCP servers/connectors"
- skill: `microsoft-fabric` · required · raw_text: "Microsoft Fabric"
- skill: `python` · required · raw_text: "Strong proficiency in Python"
- skill: `react` · nice_to_have · raw_text: "Streamlit/React"
- skill: `snowflake` · required · raw_text: "Snowflake"
- skill: `streamlit` · nice_to_have · raw_text: "Streamlit/React"
- skill: `structured-data-extraction` · required · raw_text: "unstructured document parsing"
- proposer: no usable answer (its reply was not in the form asked for), so the judge never saw it
- new rule since the models read it (HIR-390): a slash between two skills of the same kind offers either one, so "Streamlit/React" (in "Bonus: Experience with MCP servers/connectors, Streamlit/React, financial/tax automation, or mentoring offshore teams") puts `streamlit` and `react` in one group.

### 20261119T141542Z_label item 170 - golden_101 `alternative_group` (groups)
> AI DevOps Engineer Azure and GenAI
- skill: `agents` · nice_to_have · raw_text: "AI agents"
- skill: `ai-deployment` · nice_to_have · raw_text: "Deploying/operating GenAI apps"
- skill: `apis` · required · raw_text: "REST APIs"
- skill: `argocd` · nice_to_have · raw_text: "Argo CD"
- skill: `azure` · required · raw_text: "Microsoft Azure environments"
- skill: `azure-ai-foundry` · required · raw_text: "Microsoft Foundry / Azure AI services"
- skill: `azure-devops` · required · raw_text: "Azure DevOps; Azure Boards"
- skill: `azure-key-vault` · required · raw_text: "Key Vault"
- skill: `bash` · required · raw_text: "Python; Bash"
- skill: `ci-cd` · required · raw_text: "CI/CD & Source Control"
- skill: `cloud` · required · raw_text: "cloud engineering"
- skill: `cybersecurity` · required · raw_text: "cloud security fundamentals"
- skill: `databricks` · required · raw_text: "Snowflake/Databricks familiarity"
- skill: `devops` · required · raw_text: "Certifications: Microsoft Azure, GitHub, Kubernetes, Terraform, DevOps, MLOps, or AI engineering"
- skill: `devsecops` · required · raw_text: "DevSecOps scanning"
- skill: `distributed-systems` · required · raw_text: "production support for distributed systems"
- skill: `docker` · required · raw_text: "Docker, Kubernetes, Linux"
- skill: `evaluation` · required · raw_text: "AI application and agent evaluation"
- skill: `event-driven-systems` · required · raw_text: "event-driven integration"
- skill: `git` · required · raw_text: "Git; pull requests"
- skill: `github-actions` · required · raw_text: "GitHub Actions"
- skill: `gitops` · nice_to_have · raw_text: "GitOps/deployment tooling"
- skill: `helm` · required · raw_text: "Kubernetes; Helm"
- skill: `infrastructure-as-code` · required · raw_text: "reusable IaC modules"
- skill: `kubernetes` · required · raw_text: "Docker; Kubernetes; Helm"
- skill: `linux` · required · raw_text: "Linux"
- skill: `llmops` · nice_to_have · raw_text: "GenAIOps"
- skill: `llms` · nice_to_have · raw_text: "LLM-powered services"
- skill: `microservices` · required · raw_text: "microservices"
- skill: `microsoft-entra-id` · required · raw_text: "Entra ID"
- skill: `mlops` · nice_to_have · raw_text: "GenAIOps, MLOps, AgentOps"
- skill: `networking` · required · raw_text: "networking"
- skill: `observability` · required · raw_text: "Monitoring, logging, tracing"
- skill: `openai-api` · required · raw_text: "Azure OpenAI"
- skill: `opentelemetry` · required · raw_text: "Open Telemetry"
- skill: `python` · required · raw_text: "Proficiency in Python"
- skill: `rag` · required · raw_text: "RAG quality"
- skill: `secrets-management` · required · raw_text: "secrets management"
- skill: `snowflake` · required · raw_text: "Snowflake/Databricks familiarity"
- skill: `terraform` · required · raw_text: "Hands-on expertise with Terraform"
- skill: `testing` · required · raw_text: "automated testing"
- skill: `vector-search` · nice_to_have · raw_text: "vector search"
- proposer: [] - The only candidate is the certifications list ('Microsoft Azure, GitHub, Kubernetes, Terraform, DevOps, MLOps, or AI engineering'), but after removing azure, kubernetes and terraform (each asked on its own elsewhere) and mlops (listed on its own in the nice-to-haves), fewer than two skills remain, and the rule requires at least two; the other 'and/or' and example lists either name skills with no labeled id or are required together.
- judge: [["ai-deployment", "llms", "vector-search"]] - The nice-to-have list 'Deploying/operating GenAI apps, LLM-powered services, AI agents, RAG, vector search, or shared enterprise AI platforms' uses the 'X, Y or Z' marker, and after excluding `agents` and `rag` because they are also asked for on their own elsewhere in the posting, `ai-deployment`, `llms`, and `vector-search` remain as a valid group of at least two skills.
- new rule since the models read it (HIR-390): a slash between two skills of the same kind offers either one, so "Snowflake/Databricks familiarity" puts `snowflake` and `databricks` in one group.

### 20261119T142629Z_label item 159 - golden_097 `alternative_group` (groups)
> Senior Machine Learning Engineer, E-Commerce
- skill: `computer-vision` · required · raw_text: "Computer Vision"
- skill: `conversational-ai` · nice_to_have · raw_text: "conversational AI applications"
- skill: `cpp` · required · raw_text: "C++"
- skill: `fine-tuning` · nice_to_have · raw_text: "Experience in fine-tuning"
- skill: `go` · required · raw_text: "Go"
- skill: `java` · required · raw_text: "Java"
- skill: `knowledge-distillation` · nice_to_have · raw_text: "distillation, or reinforcement learning"
- skill: `llms` · nice_to_have · raw_text: "large language models"
- skill: `machine-learning` · required · raw_text: "Machine Learning"
- skill: `nlp` · required · raw_text: "Natural Language Processing (NLP)"
- skill: `python` · required · raw_text: "Python"
- skill: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning for large language models"
- skill: `software-engineering` · required · raw_text: "Proficiency in software development"
- proposer: [["machine-learning", "nlp", "computer-vision"], ["cpp", "python", "go", "java"]] - Under the alternative_group rule's 'X, Y or Z' marker, the minimum qualifications accept 'one or more of' the fields Machine Learning, NLP or Computer Vision, and 'at least one of' the languages C++, Python, Go or Java, with no skill in either set asked for separately elsewhere, while 'software-engineering' stays out as the broad parent.
- judge: [["machine-learning", "computer-vision"], ["cpp", "python", "go", "java"], ["fine-tuning", "knowledge-distillation", "reinforcement-learning"]] - The posting uses the markers 'one or more of', 'at least one of', and 'X, Y or Z' for the field, programming language, and preferred LLM technique sets, while 'nlp' leaves the first group because it is asked for on its own elsewhere ('Proficiency in multilingual NLP') and 'software-engineering' stays out as the broad parent.

### 20261119T142629Z_label item 161 - golden_100 `alternative_group` (groups)
> Machine Learning Platform Engineer, Applied Machine Learning Team San Jose Regular
- skill: `apache-spark` · required · raw_text: "Spark"
- skill: `distributed-systems` · required · raw_text: "understanding of distributed computing"
- skill: `go` · required · raw_text: "Golang"
- skill: `hadoop` · required · raw_text: "Hadoop"
- skill: `python` · required · raw_text: "Python"
- skill: `software-engineering` · required · raw_text: "experience in software engineering"
- proposer: [["apache-spark", "hadoop"]] - The posting gives Hadoop and Spark as examples for one ask ('familiar with related open source tools and frameworks (such as Hadoop, Spark, etc.)'), so any one meets it, which matches the examples-for-a-single-ask marker; Python and Golang are joined by 'and' in 'such as Python and Golang', which the rule excludes as skills asked together.
- judge: [["go", "python"], ["apache-spark", "hadoop"]] - Both 'common programming languages (such as Python and Golang)' and 'open source tools and frameworks (such as Hadoop, Spark, etc.)' offer examples for a single ask, where the 'such as' marker means any one example meets the ask.

### 20261119T142629Z_label item 164 - golden_103 `alternative_group` (groups)
> AI Engineer Lead - Visa Independent Consultants Only
- skill: `a-b-testing` · nice_to_have · raw_text: "A/B testing"
- skill: `agents` · nice_to_have · raw_text: "open-source Agentic AI frameworks"
- skill: `ai-deployment` · required · raw_text: "model deployment"
- skill: `airflow` · required · raw_text: "(Apache Airflow, MLflow)"
- skill: `autogen` · nice_to_have · raw_text: "AutoGen"
- skill: `ci-cd` · required · raw_text: "CI/CD pipelines"
- skill: `containerization` · required · raw_text: "container orchestration"
- skill: `data-privacy-and-security` · nice_to_have · raw_text: "implementing strict access control and encryption mechanisms"
- skill: `devops` · required · raw_text: "MLOps/DevOps"
- skill: `distributed-systems` · required · raw_text: "large-scale data processing and distributed systems"
- skill: `docker` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- skill: `evaluation` · required · raw_text: "model training, evaluation, and deployment"
- skill: `gcp` · required · raw_text: "Google Cloud Platform (GCP)"
- skill: `gitlab-ci` · required · raw_text: "(e.g., Jenkins, GitLab CI)"
- skill: `go` · required · raw_text: "such as Python or Go"
- skill: `google-adk` · nice_to_have · raw_text: "Agent Development Kit"
- skill: `grafana` · nice_to_have · raw_text: "(e.g., Grafana, Datadog)"
- skill: `jenkins` · required · raw_text: "(e.g., Jenkins, GitLab CI)"
- skill: `kubeflow` · required · raw_text: "(Vertex AI, Kubeflow)"
- skill: `kubernetes` · required · raw_text: "container orchestration (e.g., Kubernetes, Docker)"
- skill: `langchain` · nice_to_have · raw_text: "LangChain"
- skill: `llamaindex` · nice_to_have · raw_text: "LlamaIndex"
- skill: `llms` · nice_to_have · raw_text: "Familiarity with Large Language Models (LLMs)"
- skill: `mlflow` · required · raw_text: "(Apache Airflow, MLflow)"
- skill: `mlops` · required · raw_text: "Strong experience with Google Cloud Platform (GCP) MLOps services"
- skill: `model-development` · required · raw_text: "model training"
- skill: `observability` · required · raw_text: "monitoring and alerting"
- skill: `python` · required · raw_text: "such as Python or Go"
- skill: `vertex-ai` · required · raw_text: "(Vertex AI, Kubeflow)"
- proposer: [["python", "go"], ["kubernetes", "docker"], ["jenkins", "gitlab-ci"], ["langchain", "autogen", "llamaindex", "google-adk"], ["airflow", "kubeflow", "mlflow"]] - Each bracketed set is offered as examples for one ask ('such as Python or Go', 'e.g., Kubernetes, Docker', 'e.g., Jenkins, GitLab CI', frameworks 'e.g., LangChain, AutoGen, LlamaIndex, or ... Agent Development Kit', and 'concepts similar to Kubeflow, MLflow, or Apache Airflow'), which the alternative_group markers cover, while the broad parents (ci-cd, agents, mlops) stay out; grafana is left ungrouped because datadog is not a labeled skill.
- judge: [["vertex-ai", "kubeflow", "airflow", "mlflow"], ["python", "go"], ["kubernetes", "docker"], ["jenkins", "gitlab-ci"], ["langchain", "autogen", "llamaindex", "google-adk"]] - Under the markers rule for 'X, Y or Z' and examples offered for a single ask ('such as', 'e.g.'), each set of interchangeable examples forms a group (including 'Vertex AI, Kubeflow' or 'Apache Airflow, MLflow' together as alternatives for one MLOps ask), while broad parents (mlops, containerization, ci-cd, agents) stay out and single labeled skills (grafana) cannot form a two-skill group.

### 20261119T142629Z_label item 168 - golden_108 `alternative_group` (groups)
> AI Engineer 4 (AI Platforms)
- skill: `agent-state-management` · nice_to_have · raw_text: "Guardrails, Memory"
- skill: `agents` · nice_to_have · raw_text: "building agentic AI systems and agentic workflows"
- skill: `ai-deployment` · nice_to_have · raw_text: "deploying scalable and responsible AI solutions"
- skill: `ai-ml` · required · raw_text: "developing AI and ML algorithms or technologies"
- skill: `aws` · nice_to_have · raw_text: "AWS, Google Cloud, Azure"
- skill: `azure` · nice_to_have · raw_text: "AWS, Google Cloud, Azure"
- skill: `cloud` · nice_to_have · raw_text: "cloud platforms"
- skill: `cpp` · nice_to_have · raw_text: "C++"
- skill: `csharp` · nice_to_have · raw_text: "C#"
- skill: `cuda` · required · raw_text: "Python, Go, Scala, CUDA, or Java"
- skill: `distributed-systems` · nice_to_have · raw_text: "designing distributed systems"
- skill: `distributed-training` · nice_to_have · raw_text: "distributed systems for model training"
- skill: `gcp` · nice_to_have · raw_text: "Google Cloud"
- skill: `go` · required · raw_text: "Go"
- skill: `inference-optimization` · nice_to_have · raw_text: "optimizing training and inference software"
- skill: `java` · required · raw_text: "Python, Go, Scala, CUDA, or Java"
- skill: `llm-guardrails` · nice_to_have · raw_text: "Guardrails, Memory"
- skill: `llms` · nice_to_have · raw_text: "LLM Inference"
- skill: `machine-learning` · required · raw_text: "ML algorithms or technologies"
- skill: `model-serving` · nice_to_have · raw_text: "online inference"
- skill: `python` · required · raw_text: "programming with Python"
- skill: `scala` · required · raw_text: "Scala"
- skill: `software-architecture` · nice_to_have · raw_text: "architectural decisions"
- skill: `vector-databases` · nice_to_have · raw_text: "Similarity Search and VectorDBs"
- skill: `vector-search` · nice_to_have · raw_text: "Similarity Search and VectorDBs"
- proposer: [["python", "go", "scala", "cuda", "java"], ["aws", "gcp", "azure"]] - The basic qualification's 'at least 4 years of experience programming with Python, Go, Scala, CUDA, or Java' and the cloud-platform 'e.g. AWS, Google Cloud, Azure' each offer one ask with any one example meeting it, so each gets its own group, while the broad 'cloud' stays out per the rule's broad-skill exclusion. I left out the preferred-qualification examples (LLM Inference, Similarity Search/VectorDBs, Guardrails, Memory) and the C++/C# languages because the 'Similarity Search and VectorDBs' example is a conjunction, not a single member, and the rest are illustrations of a broad ask rather than clear alternatives.
- judge: [["python", "go", "scala", "cuda", "java"], ["aws", "gcp", "azure"], ["llms", "vector-search", "vector-databases", "llm-guardrails", "agent-state-management"], ["cpp", "csharp"]] - The posting uses 'X, Y or Z' and example markers ('e.g.') to offer alternatives for programming languages ('Python, Go, Scala, CUDA, or Java' and 'C++, C#'), cloud platforms ('e.g. AWS, Google Cloud, Azure', keeping 'cloud' out as a broad parent), and AI technologies ('e.g. LLM Inference, Similarity Search and VectorDBs, Guardrails, Memory').

## 5. Agreed labels a third model read differently (1)

A and B agreed; a third labeler from another company, reading the posting blind, did not. Usually the agreed label stands; answer `ok` or write the fix.

### 20261119T141542Z_label item 144 - golden_105 `seniority` (spot-check)
> ...monitoring, and iteration on real-world failures. • Evidence of staff-level impact: setting direction across teams, making sound...
- agreed label: value="senior" · basis="stated" · signal="Evidence of staff-level impact"
- third labeler: {"seniority": "senior", "seniority_basis": "inferred", "seniority_signal": "5+ years building and shipping ML systems"}

## 6. Random spot-check (120)

A seeded random sample of labels all three models agreed on. This is what measures the error rate of the settled labels: answer `ok`, `drop`, or write the fix.

### 20261119T103427Z_label item 111 - golden_099 `german` (spot-check)
> Machine Learning Engineer
- agreed label: value=null · basis=null · signal=null

### 20261119T103427Z_label item 141 - golden_105 `german` (spot-check)
> Physical Design Methodology Engineer, AI HW IP
- agreed label: value=null · basis=null · signal=null

### 20261119T103427Z_label item 142 - golden_106 `german` (spot-check)
> Staff Design Verification Engineer, AI HW
- agreed label: value=null · basis=null · signal=null

### 20261119T110104Z_label item 64 - golden_096 `german` (spot-check)
> Principal Software Engineer - Agentic Platform
- agreed label: value=null · basis=null · signal=null

### 20261119T112034Z_label item 152 - golden_108 `german` (spot-check)
> Applied Value Engineer - AI and Pre-Sales Consultant
- agreed label: value=null · basis=null · signal=null

### 20261119T114422Z_label item 138 - golden_104 `german` (spot-check)
> Senior Machine Learning Engineer – LLMs
- agreed label: value=null · basis=null · signal=null

### 20261119T135145Z_label item 121 - golden_098 `german` (spot-check)
> Research Engineer, Robotics - Roboticist
- agreed label: value=null · basis=null · signal=null

### 20261119T135145Z_label item 126 - golden_100 `german` (spot-check)
> Research Engineer, Robotics: Physics Simulation and Sim-to-Real
- agreed label: value=null · basis=null · signal=null

### 20261119T140709Z_label item 143 - golden_106 `german` (spot-check)
> Senior Machine Learning Engineer, Perception - Autonomous Driving
- agreed label: value=null · basis=null · signal=null

### 20261119T141542Z_label item 143 - golden_105 `german` (spot-check)
> AI Engineer - US Remote
- agreed label: value=null · basis=null · signal=null

### 20261119T141542Z_label item 153 - golden_107 `german` (spot-check)
> W2 role - AI Lead Platform Engineer 12+ years local to IL required
- agreed label: value=null · basis=null · signal=null

### 20261119T142629Z_label item 114 - golden_103 `german` (spot-check)
> AI Engineer Lead - Visa Independent Consultants Only
- agreed label: value=null · basis=null · signal=null

### 20261119T103427Z_label item 132 - golden_104 `seniority` (spot-check)
> ...with webAI’s strategic priorities Qualifications: - 4+ years of experience (can be graduate research) in machine learning research,...
- agreed label: value="mid" · basis="inferred" · signal="4+ years of experience"

### 20261119T103427Z_label item 145 - golden_107 `seniority` (spot-check)
> Software Engineer – ML Platform
- agreed label: value=null · basis=null · signal=null

### 20261119T110104Z_label item 105 - golden_101 `seniority` (spot-check)
> Principal Scientist, Machine Learning - Biomolecules ABOUT PIONEERING...
- agreed label: value="senior" · basis="stated" · signal="Principal Scientist"

### 20261119T112034Z_label item 112 - golden_100 `seniority` (spot-check)
> ...AI platform continues to evolve WHO YOU ARE - 8+ years of professional software engineering experience - Strong proficiency in Python or TypeScript -...
- agreed label: value="senior" · basis="inferred" · signal="8+ years of professional software engineering experience"

### 20261119T112034Z_label item 135 - golden_105 `seniority` (spot-check)
> Staff Software Engineer (Agentic Search) - Runtime About Nebius: Nebius is...
- agreed label: value="senior" · basis="stated" · signal="Staff Software Engineer"

### 20261119T140709Z_label item 122 - golden_102 `seniority` (spot-check)
> Senior Data Engineer, Taxonomy, AI Data Modeling, MLOps, YouTube Business In...
- agreed label: value="senior" · basis="stated" · signal="Senior Data Engineer"

### 20261119T140709Z_label item 131 - golden_105 `seniority` (spot-check)
> ...world. The Opportunity As a Cyber AI Engineer at the Senior Consultant level in EY's Cyber practice, you will work as a...
- agreed label: value="senior" · basis="stated" · signal="Senior Consultant level"

### 20261119T140709Z_label item 144 - golden_106 `seniority` (spot-check)
> Senior Machine Learning Engineer, Perception - Autonomous Driving Intelligent machines...
- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

### 20261119T141542Z_label item 113 - golden_101 `seniority` (spot-check)
> ...MLOps, or AI engineering.Required Skills & Experience-7+ years in DevOps, platform engineering, cloud engineering, site reliability...
- agreed label: value="senior" · basis="inferred" · signal="7+ years in DevOps"

### 20261119T142629Z_label item 83 - golden_095 `seniority` (spot-check)
> ...Go, Java, etc.). - Experience with web and mobile tests - Proven experience building scalable test automation, or productivity tools. - Experience with AI tools, with...
- agreed label: value="mid" · basis="inferred" · signal="Proven experience building scalable test automation"

### 20261119T142629Z_label item 102 - golden_100 `seniority` (spot-check)
> ...science, software engineering, or a related field.- At least 3 years of experience in software engineering and be proficient in developing using common programming...
- agreed label: value="mid" · basis="inferred" · signal="At least 3 years of experience in software engineering"

### 20261119T142629Z_label item 115 - golden_103 `seniority` (spot-check)
> AI Engineer Lead - Visa Independent Consultants Only Key Responsibilities:...
- agreed label: value="senior" · basis="stated" · signal="AI Engineer Lead"

### 20261119T142629Z_label item 136 - golden_105 `seniority` (spot-check)
> Field AI Engineer — Edge
- agreed label: value=null · basis=null · signal=null

### 20261119T142629Z_label item 145 - golden_107 `seniority` (spot-check)
> Senior Staff AI Engineer — Multimodal for Smart Glasses Google LLC in California...
- agreed label: value="senior" · basis="stated" · signal="Senior Staff AI Engineer"

### 20261119T103427Z_label item 83 - golden_096 `distributed-training` (spot-check)
> ...tracking - Strong programming skills in Python with experience in distributed training and model optimization - Understanding of sequential...
- agreed label: `distributed-training` · required · raw_text: "experience in distributed training"

### 20261119T103427Z_label item 86 - golden_096 `nlp` (spot-check)
> ...etc.) - Strong expertise in both computer vision and natural language processing with hands-on model development experience - Proficiency...
- agreed label: `nlp` · required · raw_text: "natural language processing"

### 20261119T103427Z_label item 95 - golden_097 `java` (spot-check)
> ...one systems programming language (e.g., Go, Rust, C++, Java, Scala) - Proficiency with modern software engineering...
- agreed label: `java` · required · raw_text: "Java"

### 20261119T103427Z_label item 96 - golden_097 `mcp` (spot-check)
> ...integrating AI systems with external tools, APIs, MCP servers, and enterprise data sources - Experience developing...
- agreed label: `mcp` · required · raw_text: "MCP servers"

### 20261119T103427Z_label item 105 - golden_098 `data-science` (spot-check)
> ...related discipline and 2+ years of relevant experience - Proficiency in machine learning and data science, with demonstrated application to image data, video data,...
- agreed label: `data-science` · required · raw_text: "Proficiency in machine learning and data science"

### 20261119T103427Z_label item 116 - golden_101 `kubernetes` (spot-check)
> ...containerization and orchestration technologies (Docker, Kubernetes). - Publications or presentations in recognized Machine...
- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

### 20261119T103427Z_label item 124 - golden_103 `python` (spot-check)
> ...related discipline and 0–2 years of relevant experience - Strong proficiency in Python including experience with libraries and frameworks like...
- agreed label: `python` · required · raw_text: "Strong proficiency in Python"

### 20261119T103427Z_label item 128 - golden_103 `software-engineering` (spot-check)
> ...like PyTorch, TensorFlow, and/or scikit-learn - Strong software engineering fundamentals and experience with at least one systems programming...
- agreed label: `software-engineering` · required · raw_text: "Strong software engineering fundamentals"

### 20261119T103427Z_label item 130 - golden_103 `testing` (spot-check)
> ...billions of dollars invested. The models perform in testing, but they degrade in the real world. And when performance...
- agreed label: `testing` · nice_to_have · raw_text: "testing"

### 20261119T103427Z_label item 144 - golden_106 `python` (spot-check)
> ...specs and waveforms. - Proficient in Linux environments with Python, or Bash scripting for automate builds, parse logs, manage CI pipelines. -...
- agreed label: `python` · required · raw_text: "with Python, or Bash scripting"

### 20261119T110104Z_label item 54 - golden_094 `nlp` (spot-check)
> ...Strong foundation in machine learning, deep learning, and natural language processing (NLP) - Proven experience deploying LLM-powered applications in...
- agreed label: `nlp` · required · raw_text: "natural language processing (NLP)"

### 20261119T110104Z_label item 85 - golden_098 `crewai` (spot-check)
> ...frameworks (e.g., Pydantic AI, LangGraph, LangChain, CrewAI, AutoGen). - Experience integrating LLMs and model...
- agreed label: `crewai` · nice_to_have · raw_text: "CrewAI"

### 20261119T110104Z_label item 86 - golden_098 `evaluation` (spot-check)
> ...OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation and feedback-loop frameworks for agentic systems. - Familiarity with sandboxed code execution and agent...
- agreed label: `evaluation` · nice_to_have · raw_text: "evaluation and feedback-loop frameworks for agentic systems"

### 20261119T110104Z_label item 90 - golden_098 `observability` (spot-check)
> ...and agent harness development. - Experience with LLM observability and monitoring tooling and cost-governance / FinOps for AI infrastructure....
- agreed label: `observability` · nice_to_have · raw_text: "LLM observability and monitoring tooling"

### 20261119T110104Z_label item 91 - golden_098 `openai-api` (spot-check)
> ...integrating LLMs and model platforms, including Anthropic, OpenAI, Vertex AI, and Amazon Bedrock, and building evaluation...
- agreed label: `openai-api` · nice_to_have · raw_text: "OpenAI"

### 20261119T110104Z_label item 98 - golden_099 `evaluation` (spot-check)
> ...into model development - Experience developing rigorous model evaluation frameworks, benchmarks, and validation strategies for molecular ML or...
- agreed label: `evaluation` · required · raw_text: "model evaluation frameworks"

### 20261119T110104Z_label item 102 - golden_100 `llms` (spot-check)
> ...forums. Qualifications - Industry-leading expertise in modern LLMs, multimodal modeling, representation learning,...
- agreed label: `llms` · required · raw_text: "modern LLMs"

### 20261119T110104Z_label item 107 - golden_101 `aws` (spot-check)
> ...(e.g., DVC/LakeFS), experiment tracking (MLflow/W&B), secure AWS infrastructure (S3, Batch/ECS/EKS, SageMaker), Docker, IaC...
- agreed label: `aws` · nice_to_have · raw_text: "secure AWS infrastructure"

### 20261119T110104Z_label item 111 - golden_101 `experiment-tracking` (spot-check)
> ...expertise: data contracts and lineage (e.g., DVC/LakeFS), experiment tracking (MLflow/W&B), secure AWS infrastructure (S3,...
- agreed label: `experiment-tracking` · nice_to_have · raw_text: "experiment tracking"

### 20261119T110104Z_label item 112 - golden_101 `fastapi` (spot-check)
> ...search (FAISS/pgvector), and lightweight internal tools (FastAPI, Streamlit/Gradio). - Experience mentoring early hires,...
- agreed label: `fastapi` · nice_to_have · raw_text: "FastAPI"

### 20261119T110104Z_label item 115 - golden_101 `jax` (spot-check)
> ...including Python; modern ML frameworks (PyTorch or JAX/TensorFlow); version control; databases; deep learning architectures;...
- agreed label: `jax` · required · raw_text: "JAX/TensorFlow"

### 20261119T110104Z_label item 116 - golden_101 `mlops` (spot-check)
> ...biophysics/MD, and LLM/agentic automation. - MLOps expertise: data contracts and lineage (e.g., DVC/LakeFS), experiment...
- agreed label: `mlops` · nice_to_have · raw_text: "MLOps expertise"

### 20261119T110104Z_label item 119 - golden_101 `sagemaker` (spot-check)
> ...secure AWS infrastructure (S3, Batch/ECS/EKS, SageMaker), Docker, IaC (Terraform/CDK), and CI/CD (GitHub...
- agreed label: `sagemaker` · nice_to_have · raw_text: "SageMaker"

### 20261119T112034Z_label item 90 - golden_096 `aws` (spot-check)
> ...hands-on experience with cloud platforms (e.g., AWS, Azure, GCP), including architecture, security, and...
- agreed label: `aws` · required · raw_text: "AWS"

### 20261119T112034Z_label item 93 - golden_096 `python` (spot-check)
> ...- You bring deep expertise in software engineering and strong Python skills, focusing on building robust, reusable systems - You...
- agreed label: `python` · required · raw_text: "strong Python skills"

### 20261119T112034Z_label item 102 - golden_097 `networking` (spot-check)
> ...such as PyTorch in distributed training contexts - Strong understanding of networking, storage, and compute resource management for ML...
- agreed label: `networking` · required · raw_text: "Strong understanding of networking"

### 20261119T112034Z_label item 103 - golden_097 `observability` (spot-check)
> ...workloads - Solid debugging and monitoring skills with expertise in observability tools for containerized environments PREFERRED SKILLS -...
- agreed label: `observability` · required · raw_text: "expertise in observability tools"

### 20261119T112034Z_label item 118 - golden_100 `mcp` (spot-check)
> ...LLM tooling such as LangChain, LlamaIndex, Guardrails, MCP, or agent frameworks - Experience implementing RAG...
- agreed label: `mcp` · required · raw_text: "MCP"

### 20261119T112034Z_label item 123 - golden_101 `jax` (spot-check)
> ...work with team leadership and stakeholder management. - Expert with PyTorch or JAX. - Deep experience with Vision Language Models (VLM),...
- agreed label: `jax` · required · raw_text: "Expert with PyTorch or JAX"

### 20261119T112034Z_label item 130 - golden_103 `software-engineering` (spot-check)
> ...learning, search and retrieval, or agent systems. - Strong software engineering skills and the ability to work across model training,...
- agreed label: `software-engineering` · required · raw_text: "Strong software engineering skills"

### 20261119T112034Z_label item 137 - golden_105 `backend-development` (spot-check)
> ...8+ years of experience as a software engineer working on production backend systems - Have strong hands-on expertise in C++ or Rust in...
- agreed label: `backend-development` · required · raw_text: "production backend systems"

### 20261119T112034Z_label item 139 - golden_105 `rust` (spot-check)
> ...and AI R&D. The Product In a rapidly evolving world, trust in AI depends on AI agents being grounded in fresh,...
- agreed label: `rust` · required · raw_text: "Rust"

### 20261119T112034Z_label item 147 - golden_106 `python` (spot-check)
> ...building and deploying data science solutions in Python and related ML libraries. - Strong background in applied...
- agreed label: `python` · required · raw_text: "Python"

### 20261119T112034Z_label item 148 - golden_106 `transformers` (spot-check)
> ...Familiarity with advanced NLP frameworks such as spaCy or Transformers and exposure to AI technologies including Generative AI or...
- agreed label: `transformers` · nice_to_have · raw_text: "Transformers"

### 20261119T112034Z_label item 150 - golden_107 `nlp` (spot-check)
> ...hands-on when it matters. - You bring experience across NLP, audio / music content understanding and recommender...
- agreed label: `nlp` · required · raw_text: "NLP"

### 20261119T114422Z_label item 84 - golden_096 `distributed-systems` (spot-check)
> ...from experience building real projects (or close to it). Bonus points if you've worked with distributed systems. - You've actually used PyTorch and HuggingFace and you...
- agreed label: `distributed-systems` · nice_to_have · raw_text: "Bonus points if you've worked with distributed systems"

### 20261119T114422Z_label item 93 - golden_097 `python` (spot-check)
> ...reading, writing, and debugging production-quality code. Ideally experienced in Go, Python or TypeScript. Backend or full-stack background both fine. - Real...
- agreed label: `python` · nice_to_have · raw_text: "Ideally experienced in Go, Python or TypeScript"

### 20261119T114422Z_label item 104 - golden_099 `computer-vision` (spot-check)
> ...or behavioural data, natural language processing, or computer vision.</li> <li>Familiarity with the production ML lifecycle,...
- agreed label: `computer-vision` · required · raw_text: "computer vision"

### 20261119T114422Z_label item 115 - golden_100 `grafana` (spot-check)
> ...on AWS, Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and OpenTelemetry. - CI/CD: GitHub...
- agreed label: `grafana` · required · raw_text: "Grafana"

### 20261119T114422Z_label item 116 - golden_100 `prometheus` (spot-check)
> ...Terraform, Helm and ArgoCD. - Observability: Grafana, Prometheus and OpenTelemetry. - CI/CD: GitHub Actions. At DPG...
- agreed label: `prometheus` · required · raw_text: "Prometheus"

### 20261119T114422Z_label item 120 - golden_101 `machine-learning` (spot-check)
> ...5+ years experience in a similar role • Deep expertise in data science and machine learning, enabling you to design, train, and implement models in...
- agreed label: `machine-learning` · required · raw_text: "data science and machine learning"

### 20261119T114422Z_label item 121 - golden_101 `mlops` (spot-check)
> ...solutions • Experience with machine learning tools and MLOps systems such as Docker, Databricks, and MLflow • Strong...
- agreed label: `mlops` · required · raw_text: "MLOps systems"

### 20261119T114422Z_label item 134 - golden_103 `mcp` (spot-check)
> ...- Familiarity with agentic architectures and protocols such as MCP, A2A - A systems mindset, with attention to reliability,...
- agreed label: `mcp` · required · raw_text: "protocols such as MCP"

### 20261119T114422Z_label item 136 - golden_103 `testing` (spot-check)
> ...performance and security - Experience with CI/CD, automated testing and production observability - A record of working...
- agreed label: `testing` · required · raw_text: "automated testing"

### 20261119T114422Z_label item 142 - golden_104 `knowledge-distillation` (spot-check)
> ...- Experience optimising models for production inference, including distillation, pruning, quantisation, compression and serving frameworks...
- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "including distillation"

### 20261119T114422Z_label item 143 - golden_104 `megatron-lm` (spot-check)
> ...and data mixture design. - Hands-on experience with distributed training frameworks (Megatron-LM, DeepSpeed, FSDP or Axolotl), including orchestrating...
- agreed label: `megatron-lm` · required · raw_text: "distributed training frameworks (Megatron-LM"

### 20261119T114422Z_label item 146 - golden_104 `reinforcement-learning` (spot-check)
> ...with post-training methods such as RLHF, DPO, GRPO or other reinforcement learning approaches for alignment and instruction following. - Experience...
- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "other reinforcement learning approaches"

### 20261119T114422Z_label item 147 - golden_104 `tensorrt` (spot-check)
> ...quantisation, compression and serving frameworks (vLLM, TensorRT-LLM). - Experience evaluating models through online...
- agreed label: `tensorrt` · nice_to_have · raw_text: "TensorRT-LLM"

### 20261119T114422Z_label item 150 - golden_105 `cloud` (spot-check)
> ...experience in monitoring and observability practices - Advanced knowledge of cloud services - Ability to thrive in a collaborative environment...
- agreed label: `cloud` · required · raw_text: "Advanced knowledge of cloud services"

### 20261119T135145Z_label item 92 - golden_095 `ai-developer-tooling` (spot-check)
> ...and caching patterns - Demonstrated experience leveraging AI-powered development tools such as Claude Code, GitHub Copilot, or similar agentic...
- agreed label: `ai-developer-tooling` · required · raw_text: "AI-powered development tools"

### 20261119T135145Z_label item 104 - golden_095 `vector-databases` (spot-check)
> ...and data systems knowledge including relational databases, vector databases, event streaming (Kafka, SQS), and caching patterns -...
- agreed label: `vector-databases` · required · raw_text: "vector databases"

### 20261119T135145Z_label item 115 - golden_097 `kubernetes` (spot-check)
> ...and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a foundational...
- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

### 20261119T135145Z_label item 124 - golden_099 `python` (spot-check)
> ...frameworks at a systems level. - Strong proficiency in one or more programming languages such as Python and C++. - Strong understanding of one or more of the...
- agreed label: `python` · required · raw_text: "one or more programming languages such as Python"

### 20261119T135145Z_label item 134 - golden_102 `sagemaker` (spot-check)
> ...Experience with cloud platforms, including AWS S3, SageMaker, and Airflow - Experience with cloud data warehouses and...
- agreed label: `sagemaker` · nice_to_have · raw_text: "SageMaker"

### 20261119T135145Z_label item 138 - golden_102 `tableau` (spot-check)
> ...and modern data tools such as Snowflake, dbt, Looker, and Tableau - Familiarity with Media Mix Modeling (MMM) frameworks...
- agreed label: `tableau` · nice_to_have · raw_text: "Tableau"

### 20261119T135145Z_label item 140 - golden_103 `containerization` (spot-check)
> ...pick up new tools as needed - Familiarity with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and...
- agreed label: `containerization` · required · raw_text: "containerization"

### 20261119T135145Z_label item 142 - golden_103 `evaluation` (spot-check)
> ...of ML infrastructure experience — data preprocessing, model training, evaluation, inference, and deployment - Experience with end-to-end...
- agreed label: `evaluation` · required · raw_text: "model training, evaluation"

### 20261119T135145Z_label item 150 - golden_104 `knowledge-distillation` (spot-check)
> ...including model evaluation, monitoring, quantization, distillation/teacher-student approaches, and production deployment. - Hands-on experience...
- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "distillation/teacher-student approaches"

### 20261119T135145Z_label item 151 - golden_104 `llmops` (spot-check)
> ...Mathematics, or another highly technical field. - Experience with LLMOps, including model evaluation, monitoring, quantization,...
- agreed label: `llmops` · nice_to_have · raw_text: "Experience with LLMOps"

### 20261119T135145Z_label item 153 - golden_104 `software-architecture` (spot-check)
> ...dive deep into complex system architectures. - Excellent software architecture and design skills, with a focus on building robust, scalable, maintainable...
- agreed label: `software-architecture` · required · raw_text: "software architecture and design skills"

### 20261119T135145Z_label item 154 - golden_104 `software-engineering` (spot-check)
> ...or another highly technical field. - 6+ years of software engineering experience, including a proven track record of deploying AI/ML models...
- agreed label: `software-engineering` · required · raw_text: "software engineering experience"

### 20261119T135145Z_label item 162 - golden_107 `jax` (spot-check)
> ...in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Strong proficiency in one or more programming...
- agreed label: `jax` · required · raw_text: "JAX"

### 20261119T140709Z_label item 87 - golden_096 `agents` (spot-check)
> ...search plus graph traversal) and connecting knowledge to agent frameworks (e.g., Google ADK, LangGraph) via MCP. • Experience with...
- agreed label: `agents` · nice_to_have · raw_text: "agent frameworks"

### 20261119T140709Z_label item 95 - golden_096 `tensorflow` (spot-check)
> ...and SQL, and proficiency with ML frameworks (PyTorch or TensorFlow, plus scikit-learn). • Hands-on experience with at least one graph database...
- agreed label: `tensorflow` · required · raw_text: "TensorFlow, plus scikit-learn"

### 20261119T140709Z_label item 116 - golden_101 `openai-api` (spot-check)
> ...backend services - Practical experience with LLM APIs (OpenAI, Anthropic, or similar), prompt engineering, and agentic...
- agreed label: `openai-api` · required · raw_text: "OpenAI"

### 20261119T140709Z_label item 117 - golden_101 `postgresql` (spot-check)
> ...Scala (principally), Java (limited) - Datastores: MySQL, PostgreSQL, Snowflake - Cloud: AWS - Version control: Git &...
- agreed label: `postgresql` · required · raw_text: "PostgreSQL"

### 20261119T140709Z_label item 121 - golden_101 `sql` (spot-check)
> ...Familiarity with data engineering fundamentals including SQL, data transformation, and cloud data warehouses such as...
- agreed label: `sql` · required · raw_text: "SQL"

### 20261119T140709Z_label item 135 - golden_105 `evaluation` (spot-check)
> ...building model integrations, tool-calling agents, evaluation harnesses, and secure security-platform connections. • Ability to...
- agreed label: `evaluation` · required · raw_text: "evaluation harnesses"

### 20261119T140709Z_label item 137 - golden_105 `llm-orchestration` (spot-check)
> ...selection, adaptation, and evaluation. • Experience with agent orchestration, model serving, LLM observability, and CI/CD evaluation...
- agreed label: `llm-orchestration` · nice_to_have · raw_text: "agent orchestration"

### 20261119T140709Z_label item 139 - golden_105 `model-selection` (spot-check)
> ...Experience with frontier model providers or cyber-focused model selection, adaptation, and evaluation. • Experience with agent...
- agreed label: `model-selection` · nice_to_have · raw_text: "model selection"

### 20261119T140709Z_label item 147 - golden_106 `tensorflow` (spot-check)
> ...Experience with deep learning frameworks (e.g., PyTorch, Tensor Flow) and a strong understanding of the mathematical...
- agreed label: `tensorflow` · required · raw_text: "Tensor Flow"

### 20261119T140709Z_label item 148 - golden_106 `transformers` (spot-check)
> ...environment. • Advanced Model Knowledge: Familiarity with modern network architectures like Transformers and their application to visual recognition tasks. • AV...
- agreed label: `transformers` · nice_to_have · raw_text: "modern network architectures like Transformers"

### 20261119T140709Z_label item 152 - golden_107 `sql` (spot-check)
> ...The role blends data engineering with AI, requiring strong SQL and Python skills and experience with Cortex components,...
- agreed label: `sql` · required · raw_text: "strong SQL"

### 20261119T141542Z_label item 94 - golden_098 `cloud` (spot-check)
> ...learning applications and language generation systems Cloud & API Architecture to implement complex service-to-service OAuth2...
- agreed label: `cloud` · required · raw_text: "Cloud & API Architecture"

### 20261119T141542Z_label item 102 - golden_099 `databricks` (spot-check)
> ...modern cloud data platforms (Microsoft Fabric, Snowflake, or Databricks). • Proven experience supporting the data backend for...
- agreed label: `databricks` · required · raw_text: "or Databricks"

### 20261119T141542Z_label item 109 - golden_100 `model-serving` (spot-check)
> ...with DevOps and CI/CD practices • Has experience building and scaling model serving tools, i.e building APIs with tight SLAs • Passion for the...
- agreed label: `model-serving` · nice_to_have · raw_text: "building and scaling model serving tools"

### 20261119T141542Z_label item 121 - golden_101 `gitops` (spot-check)
> ...Insights, Datadog, Dynatrace, Splunk, or equivalent).-GitOps/deployment tooling (Argo CD, Helm, or equivalent).-ServiceNow and enterprise...
- agreed label: `gitops` · nice_to_have · raw_text: "GitOps/deployment tooling"

### 20261119T141542Z_label item 124 - golden_101 `microsoft-entra-id` (spot-check)
> ...Learning; Azure OpenAI; AKS; API Management; Key Vault; Entra ID; Azure Monitor-Azure DevOps; Azure Boards; GitHub; GitHub...
- agreed label: `microsoft-entra-id` · required · raw_text: "Entra ID"

### 20261119T141542Z_label item 128 - golden_101 `secrets-management` (spot-check)
> ...Kubernetes, Linux, networking, identity, secrets management, and cloud security fundamentals.-Proficiency in Python...
- agreed label: `secrets-management` · required · raw_text: "secrets management"

### 20261119T141542Z_label item 141 - golden_104 `snowflake` (spot-check)
> ...compute • Knowledge of AWS, SageMaker, Airflow, Kafka, Redis or Snowflake Location and schedule • Chicago, IL • In office four days...
- agreed label: `snowflake` · required · raw_text: "Redis or Snowflake"

### 20261119T141542Z_label item 145 - golden_105 `model-serving` (spot-check)
> ...models from research to production: model optimization, inference serving, monitoring, and iteration on real-world failures. •...
- agreed label: `model-serving` · required · raw_text: "inference serving"

### 20261119T141542Z_label item 147 - golden_105 `pytorch` (spot-check)
> ...or a clear record in adjacent multimodal work. • Strong PyTorch skills and fluency with distributed training, mixed precision,...
- agreed label: `pytorch` · required · raw_text: "Strong PyTorch skills"

### 20261119T141542Z_label item 157 - golden_108 `aws` (spot-check)
> ...and engineers. What You’ll Bring Required • Senior/architect-level AWS expertise, with hands-on Amazon Quick Suite experience • Strong...
- agreed label: `aws` · required · raw_text: "Senior/architect-level AWS expertise"

### 20261119T141542Z_label item 160 - golden_108 `llms` (spot-check)
> ...Strong Python skills and experience building agents and LLM solutions across semantic and knowledge layers • Bedrock agents,...
- agreed label: `llms` · required · raw_text: "LLM solutions"

### 20261119T141542Z_label item 163 - golden_108 `terraform` (spot-check)
> ...Power BI/DAX; SAP, JDE and M3 data concepts • Terraform/CloudFormation, Git, CI/CD, testing and Jira • Experience with the Atlan...
- agreed label: `terraform` · nice_to_have · raw_text: "Terraform/CloudFormation"

### 20261119T142629Z_label item 91 - golden_097 `llms` (spot-check)
> ...fine-tuning, distillation, or reinforcement learning for large language models in conversational AI applications. • Proficiency in...
- agreed label: `llms` · nice_to_have · raw_text: "large language models"

### 20261119T142629Z_label item 119 - golden_103 `distributed-systems` (spot-check)
> ...languages such as Python or Go, and experience with large-scale data processing and distributed systems. Experience working with large-scale production...
- agreed label: `distributed-systems` · required · raw_text: "large-scale data processing and distributed systems"

### 20261119T142629Z_label item 120 - golden_103 `gitlab-ci` (spot-check)
> ...(e.g., Kubernetes, Docker), and CI/CD pipelines (e.g., Jenkins, GitLab CI). Experience with production operations for distributed...
- agreed label: `gitlab-ci` · required · raw_text: "(e.g., Jenkins, GitLab CI)"

### 20261119T142629Z_label item 132 - golden_104 `postgresql` (spot-check)
> ...stackTypeScript, Python, FastAPI, Agentic AI, OpenCV, PostgreSQL, React Native Why candidates should joinCategory-defining...
- agreed label: `postgresql` · required · raw_text: "PostgreSQL"

### 20261119T142629Z_label item 134 - golden_104 `tool-calling` (spot-check)
> ...shipped agent systems in production with orchestration, tool use, state management and human-in-the-loop workflows •...
- agreed label: `tool-calling` · required · raw_text: "tool use"

### 20261119T142629Z_label item 140 - golden_106 `machine-learning` (spot-check)
> ...identity, trust & safety, or other adversarial domains. Solid ML background with practical experience in Python, SQL, and current ML...
- agreed label: `machine-learning` · required · raw_text: "Solid ML background"

### 20261119T142629Z_label item 141 - golden_106 `python` (spot-check)
> ...domains. Solid ML background with practical experience in Python, SQL, and current ML frameworks like PyTorch. Experience...
- agreed label: `python` · required · raw_text: "Python"

### 20261119T142629Z_label item 146 - golden_108 `agents` (spot-check)
> ...utilization, latency, throughput, and cost • Experience in building agentic AI systems and agentic workflows • Passion for staying abreast of the latest AI research...
- agreed label: `agents` · nice_to_have · raw_text: "building agentic AI systems and agentic workflows"

### 20261119T142629Z_label item 149 - golden_108 `cpp` (spot-check)
> ...Search and VectorDBs, Guardrails, Memory) using Python, C++, C#, Java, CUDA, or Golang • Experience developing and...
- agreed label: `cpp` · nice_to_have · raw_text: "C++"
