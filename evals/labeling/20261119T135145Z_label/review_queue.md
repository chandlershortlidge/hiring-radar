# Review queue - 20261119T135145Z_label

166 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T135145Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 201 accepted labels,
seed 0) of labels A and B already agreed on. They measure the error rate that
agreement alone cannot: two labelers can agree and both be wrong. They print the posting
excerpt and the agreed label only - no `A:`/`B:` lines - so you check the label against the
posting rather than against the labelers, who by construction both said the same thing.

The first 15 items ask whether each posting belongs in the held-out set at all.
They come pre-answered `yes`, so leaving them alone keeps every posting. Answer `no <why>`
and that posting is written to `evals/goldens/excluded.json` with your reason instead of
becoming a Golden, and neither this script nor `new_goldens.py` will pick it again. Use it
for a posting that got past the title and city filters but is not the job market we
measure - a marketing role, a listing in the wrong field. The rest of that posting's items
are then ignored, so you can answer `no` and skip them.

## 1. golden_094 - scope `in_scope` (in-scope)

> Staff Machine Learning Engineer, Growth

- metropolis · Staff Machine Learning Engineer, Growth
- Seattle · en · greenhouse · 13 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> Senior Software Engineer, AI Agentic Platform

- metropolis · Senior Software Engineer, AI Agentic Platform
- Seattle · en · greenhouse · 32 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> AI Inference Infrastructure Software Engineer (Kubernetes / Cloud)

- elastix · AI Inference Infrastructure Software Engineer (Kubernetes / Cloud)
- Seattle · en · ashby · 15 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> Machine Learning Engineer

- elastix · Machine Learning Engineer
- Seattle · en · ashby · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> Research Engineer, Robotics - Roboticist

- thealleninstitute · Research Engineer, Robotics - Roboticist
- Seattle · en · greenhouse · 7 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> AI Compiler and Performance Engineer

- elastix · AI Compiler and Performance Engineer
- Seattle · en · ashby · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> Research Engineer, Robotics: Physics Simulation and Sim-to-Real

- thealleninstitute · Research Engineer, Robotics: Physics Simulation and Sim-to-Real
- Seattle · en · greenhouse · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> Hardware Design Engineer, AI Inference Engine

- elastix · Hardware Design Engineer, AI Inference Engine
- Seattle · en · ashby · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> Senior Data Scientist, Growth Marketing

- metropolis · Senior Data Scientist, Growth Marketing
- Seattle · en · greenhouse · 15 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_103 - scope `in_scope` (in-scope)

> Senior Research Engineer, Olmo + Molmo

- thealleninstitute · Senior Research Engineer, Olmo + Molmo
- Seattle · en · greenhouse · 14 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_104 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer

- axon · Senior Machine Learning Engineer
- Seattle · en · greenhouse · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_105 - scope `in_scope` (in-scope)

> Senior Software Engineer, Axon AI

- axon · Senior Software Engineer, Axon AI
- Seattle · en · greenhouse · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_106 - scope `in_scope` (in-scope)

> AI Software Engineer

- elastix · AI Software Engineer
- Seattle · en · ashby · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_107 - scope `in_scope` (in-scope)

> Machine Learning Research Scientist

- elastix · Machine Learning Research Scientist
- Seattle · en · ashby · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_108 - scope `in_scope` (in-scope)

> Research Engineer, Climate Modeling

- thealleninstitute · Research Engineer, Climate Modeling
- Seattle · en · greenhouse · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_095 - attribute `degree` (disagreement)

> ...team While not required, these are a plus: - Advanced degree in Computer Science, Machine Learning, or related technical field - Experience building customized agent harnesses,...

- A: value="master" · requirement="nice_to_have" · or_equivalent=false · signal="Advanced degree in Computer Science, Machine Learning, or related technical field"
- B: value="bachelor" · requirement="nice_to_have" · or_equivalent=false · signal="Advanced degree in Computer Science, Machine Learning, or related technical field"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under the degree rule, `degree` is the lowest level the posting names, and the only level named is "Advanced degree" (a master's or higher), so `master` is right while B's `bachelor` has no support in the text; the nice_to_have requirement and or_equivalent=false are correct under the "While not required… a plus" framing.

DECISION: A

## 17. golden_095 - skill `agent-architecture` (disagreement)

> ...production environments - 2+ years of hands-on experience architecting and deploying agentic AI systems, LLM orchestration frameworks, or AI platform tooling -...

- A: (did not label this)
- B: `agent-architecture` · required · raw_text: "architecting and deploying agentic AI systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification "2+ years of hands-on experience architecting and deploying agentic AI systems" names a skill, not just a job title or a bare years line, so labeler B's required agent-architecture tag stands (rule 3 also favors the required mention).

DECISION: B

## 18. golden_095 - skill `ai-deployment` (disagreement)

> ...2+ years of hands-on experience architecting and deploying agentic AI systems, LLM orchestration frameworks, or AI platform tooling -...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying agentic AI systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'What we're looking for' bullet requiring 2+ years of 'architecting and deploying agentic AI systems' is a qualification that names the skill, and rule 3 makes that required mention control, so B's required label with the verbatim quote is correct.

DECISION: B

## 19. golden_095 - skill `software-engineering` (disagreement)

> ...patterns What we're looking for - 6+ years of backend software engineering experience with deep focus on distributed systems,...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only quoted mention, "6+ years of backend software engineering experience," is a years-of-experience line, which does not count as naming a skill, and the excerpt shows no other mention of software engineering as a skill.

DECISION: drop

## 20. golden_096 - skill `model-development` (disagreement)

> ...in OS configuration tooling. - Familiarity with AI inference and/or training workflows and the operational patterns around them. - Pragmatic,...

- A: (did not label this)
- B: `model-development` · required · raw_text: "AI inference and/or training workflows"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rules 1 and 3, the required qualification bullet "Familiarity with AI inference and/or training workflows" names training workflows, which supports model-development as required, and labeler B's raw_text quotes it accurately; the operational framing is a weaker match, so this is a close call.

DECISION: ?

## 21. golden_096 - skill `model-serving` (disagreement)

> ...servers and runtimes (e.g., Triton, vLLM, TGI) and model-serving patterns (batching, streaming, KV-cache aware routing). -...

- A: `model-serving` · nice_to_have · raw_text: "model-serving patterns"
- B: `model-serving` · required · raw_text: "running ML or inference services at scale on Kubernetes in production"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3, the only model-serving mention visible in the excerpt is "model-serving patterns" in the Preferred/Bonus Qualifications section, so it is nice_to_have, and labeler B's quoted required phrase does not appear in the posting excerpt.

DECISION: A

## 22. golden_097 - skill `inference-optimization` (disagreement)

> ...generative machine learning models. - Experience with optimizing the performance of machine learning models. - Experience leading research initiatives in Machine...

- A: (did not label this)
- B: `inference-optimization` · nice_to_have · raw_text: "optimizing the performance of machine learning models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 5, the posting never names inference or serving; "optimizing the performance of machine learning models" is a generic performance-optimization phrase that does not support the narrower inference-optimization skill.

DECISION: drop

## 23. golden_097 - skill `llms` (disagreement)

> ...Qualifications: - Experience with training generative machine learning models. - Experience with optimizing the performance of machine...

- A: (did not label this)
- B: `llms` · nice_to_have · raw_text: "generative machine learning models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 5, "generative machine learning models" is a broader category than LLMs and does not name LLMs, so adding `llms` would be inferring a specific skill the text does not state.

DECISION: drop

## 24. golden_098 - attribute `seniority` (disagreement)

> ...You’ll Need: Minimum Qualifications: - Master’s with 3+ years of experience, or PhD, in robotics, control or a related field. Strong...

- A: value="mid" · basis="inferred" · signal="3+ years of experience"
- B: value="senior" · basis="inferred" · signal="Lead the setup, calibration, maintenance and tuning of our robots"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 4, the 'Lead the setup, calibration, maintenance and tuning' signal is a responsibility rather than something the candidate is asked for, while the 'Minimum Qualifications' line requiring 3+ years of experience directly supports a mid-level reading.

DECISION: A

## 25. golden_098 - skill `computer-vision` (disagreement)

> ...Hand-eye and multi-camera calibration, depth sensing and 3D perception on hardware. - Open-source contributions or publications at robotics...

- A: (did not label this)
- B: `computer-vision` · nice_to_have · raw_text: "3D perception on hardware"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Preferred Qualifications bullet names 3D perception and depth sensing, which are computer-vision skills, so the nice_to_have tag with the verbatim raw_text "3D perception on hardware" holds even though the word "computer vision" never appears.

DECISION: ?

## 26. golden_098 - skill `model-development` (disagreement)

> ...for 3D printing or machining. - Robot learning: you have trained or deployed learned policies (imitation learning, RL or VLA) on real robots, and are...

- A: (did not label this)
- B: `model-development` · required · raw_text: "trained or deployed learned policies"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required Minimum Qualifications bullet on robot learning names training or deploying learned policies, and rule 3 makes that required mention decisive, so the model-development label with its required tag and raw_text stands.

DECISION: ?

## 27. golden_098 - skill `software-architecture` (disagreement)

> ...of arms with grippers or hands. - System design: you have designed robot software systems end to end (control loops at 500 Hz to 1 kHz, state estimation, data...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designed robot software systems end to end"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under Minimum Qualifications, rule 1 applies: the "System design" bullet requires having "designed robot software systems end to end" with data flow and interfaces, which is software architecture work the posting actually asks for, so labeler B's required tag stands.

DECISION: ?

## 28. golden_099 - skill `machine-learning` (disagreement)

> ...or algorithmic optimization for deep learning - Deep expertise on ML frameworks (e.g., PyTorch, TensorFlow, JAX) and understanding of ML...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "Deep expertise on ML frameworks"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required-qualifications line "Deep expertise on ML frameworks" names ML expertise, and under rule 3 that required mention wins over labeler A's omission, so the required machine-learning label stands.

DECISION: B

## 29. golden_101 - skill `machine-learning` (disagreement)

> ...- Experience with hardware implementation of ML optimization techniques (e.g., sparsity, quantization, pruning). - Proficiency...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "ML optimization techniques"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 3, the required bullets name ML work ("Deep understanding of modern AI/ML models" and "hardware implementation of ML optimization techniques"), and B's quoted raw_text "ML optimization techniques" is a verbatim required mention, so B's label stands (rule 1 is also met since this is a qualification bullet).

DECISION: B

## 30. golden_102 - skill `data-science` (disagreement)

> ...robust, and well-commented code to produce high-quality data science procedures 4 Days in Office: Metropolis values in-person...

- A: (did not label this)
- B: `data-science` · nice_to_have · raw_text: "data science procedures"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'plus' bullet asking for code that produces 'high-quality data science procedures' is a qualification that names data science, and under rule 3 the mention is nice_to_have since it sits under 'While not required,' so labeler B's tag and raw_text are supported.

DECISION: B

## 31. golden_103 - skill `testing` (disagreement)

> ...fundamentals — performant, scalable systems and confident debugging - Proficiency in Python and a major ML framework...

- A: (did not label this)
- B: `testing` · required · raw_text: "confident debugging"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 5, the posting never names testing; "confident debugging" is a different skill, and labeler A did not tag testing, so the testing label should not be in the key.

DECISION: drop

## 32. golden_104 - skill `ai-ml` (disagreement)

> ...engineering experience, including a proven track record of deploying AI/ML models to production in the cloud. - Strong experience with cloud architecture...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "deploying AI/ML models to production"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'What You Bring' bullet requiring 'a proven track record of deploying AI/ML models to production in the cloud' is a qualification that names the skill, and under rule 3 that required mention wins, so labeler B's required ai-ml label stands.

DECISION: B

## 33. golden_104 - skill `machine-learning` (disagreement)

> ...as code. - Proficiency in Python and C++, with experience using ML frameworks such as PyTorch or TensorFlow. - Advanced, hands-on...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "experience using ML frameworks"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification bullets name ML directly ("deploying AI/ML models to production" and "experience using ML frameworks such as PyTorch or TensorFlow"), so labeler B's required machine-learning label is supported and its raw_text appears verbatim in the posting.

DECISION: B

## 34. golden_105 - skill `software-architecture` (disagreement)

> ...technical leadership (standards, tooling, workflows, architectural direction). - Experience operating in Product environments where...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architectural direction"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the preferred-qualifications bullet on a track record of technical leadership names "architectural direction" as a skill area, so the nice_to_have software-architecture tag from labeler B stands.

DECISION: B

## 35. golden_105 - skill `software-engineering` (disagreement)

> ...Bachelor’s degree or equivalent experience. - 9+ years of software development experience, including ownership of complex product...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software development"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only mention, "9+ years of software development experience," is a years-of-experience line, which does not count as a named skill, and rule 5 bars adding a broad skill the qualifications do not otherwise name.

DECISION: drop

## 36. golden_108 - skill `ai-deployment` (disagreement)

> ...You’ll Need: - 2-4 years of experience building and deploying a relevant ML application in a practical or academic research setting and be fluent...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying a relevant ML application"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification 'building and deploying a relevant ML application' names a skill rather than just a title or years line, and rule 3 supports the required mention quoted by labeler B.

DECISION: B

## 37. golden_108 - skill `model-development` (disagreement)

> ...or applied mathematics/statistics. - Experience in developing ML training code for use in a cloud computing environment. - Demonstrated...

- A: (did not label this)
- B: `model-development` · required · raw_text: "developing ML training code"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification bullet "Experience in developing ML training code for use in a cloud computing environment" names ML development work, and under rule 3 that required mention, quoted as "developing ML training code", supports labeler B's required model-development tag.

DECISION: ?

## 38. golden_094 - attribute `degree` (uncertain)

> ...machine learning organization What we're looking for - PhD in Computer Science, Statistics, Economics, Applied Mathematics, Industrial Engineering, Operational Research, or a related STEM field with 6+ years of relevant experience, or MS with 8+ years...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in Computer Science, Statistics, Economics, Applied Mathematics, Industrial Engineering, Operational Research, or a related STEM field"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in Computer Science, Statistics, Economics, Applied Mathematics, Industrial Engineering, Operational Research, or a related STEM field with 6+ years of relevant experience, or MS with 8+ years experiences with equivalent publications."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "MS with 8+ years experiences with equivalent publications"} - Under the rule, `degree` is the lowest level named, and the posting names an MS alternative ('or MS with 8+ years experiences'), so the level is master rather than phd.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "MS with 8+ years experiences with equivalent publications"}

## 39. golden_094 - skill `agents` (uncertain)

> ...with Spark, and workflow orchestration via Airflow. - Experience building agentic AI solutions for pricing is highly desirable. - Proficient programming skills in Python and SQL....

- A: `agents` · nice_to_have · raw_text: "Experience building agentic AI solutions for pricing is highly desirable"
- B: `agents` · nice_to_have · raw_text: "Experience building agentic AI solutions for pricing is highly desirable."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the qualification sentence "Experience building agentic AI solutions for pricing is highly desirable" names the skill, and it is the only mention, so nice_to_have is correct and the agreed raw_text is verbatim.

DECISION: ok

## 40. golden_094 - skill `ai-deployment` (uncertain)

> ...owning and leading projects from inception to production, successfully deploying models and driving measurable business impact - Solid...

- A: `ai-deployment` · required · raw_text: "successfully deploying models"
- B: `ai-deployment` · required · raw_text: "deploying models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What we're looking for' bullet requiring 'successfully deploying models' is a qualification naming the skill, and rule 3 makes that required mention decisive, so the agreed required label and quote stand.

DECISION: ok

## 41. golden_095 - skill `async-processing` (uncertain)

> ...in Python or Java/TypeScript with production expertise in async concurrency, API design, and system performance tuning - Production...

- A: `async-processing` · required · raw_text: "async concurrency"
- B: `async-processing` · required · raw_text: "async concurrency"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What we're looking for' bullet names 'production expertise in async concurrency' as a requirement, and under rule 3 that required mention supports the agreed required async-processing label with its quoted raw_text.

DECISION: ok

## 42. golden_095 - skill `data-privacy-and-security` (uncertain)

> ...loops - Security compliance expertise regarding data privacy, prompt injection defenses, secrets management, and access...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "data privacy"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "Security compliance expertise regarding data privacy"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the nice-to-have bullet names data privacy as part of its security compliance expertise, the quoted "data privacy" appears verbatim, and the "not required" framing correctly makes it nice_to_have.

DECISION: ok

## 43. golden_095 - skill `mcp` (uncertain)

> ...orchestration frameworks and protocols such as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in...

- A: `mcp` · required · raw_text: "Anthropic MCP"
- B: `mcp` · required · raw_text: "Anthropic MCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What we're looking for' bullet asks for production experience with 'Anthropic MCP' as a named protocol, and rule 3 makes that required mention determinative, with the raw_text quoted verbatim.

DECISION: ok

## 44. golden_096 - attribute `degree` (uncertain)

> ...shipping iteratively. Preferred/Bonus Qualifications: - MS/PhD in Computer Science, Software Engineering, or a related field. - Experience with inference servers and runtimes (e.g.,...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="MS/PhD in Computer Science, Software Engineering, or a related field"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="MS/PhD in Computer Science, Software Engineering, or a related field."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Minimum BS in Computer Science, Software Engineering, or a related field"} - Under the rule, `degree` is the lowest level named, so the required 'Minimum BS' (a bare requirements-list mention, hence `required`) governs and the optional 'MS/PhD' preference is not recorded, which makes the agreed phd/nice_to_have label wrong.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Minimum BS in Computer Science, Software Engineering, or a related field"}

## 45. golden_096 - skill `apis` (uncertain)

> ...for latency-sensitive services. - Experience building customer facing API platforms including onboarding, API keys/auth management, and usage...

- A: `apis` · nice_to_have · raw_text: "customer facing API platforms"
- B: `apis` · nice_to_have · raw_text: "API platforms"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred/Bonus qualification bullet names the skill of building customer-facing API platforms (onboarding, key/auth management, metering), which is building APIs rather than consuming them under rule 2, and the nice_to_have level matches the Preferred section.

DECISION: ok

## 46. golden_096 - skill `networking` (uncertain)

> ...in Kubernetes, scheduling, drivers, device plugins, MIG, networking, and storage considerations. - Solid coding skills in Python, Bash and proficiency...

- A: `networking` · required · raw_text: "networking, and storage considerations"
- B: `networking` · required · raw_text: "networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Required Qualifications bullet on accelerated workloads in Kubernetes names networking, and under rule 3 that required mention makes the agreed required label correct; the raw_text appears verbatim in the posting.

DECISION: ok

## 47. golden_097 - skill `ai-deployment` (uncertain)

> ...Computer Engineering, or a related field. - 3+ years of machine learning R&D and deployment experience. - Strong proficiency in one or more programming...

- A: `ai-deployment` · required · raw_text: "machine learning R&D and deployment experience"
- B: `ai-deployment` · required · raw_text: "machine learning R&D and deployment experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only support is the years-of-experience line "3+ years of machine learning R&D and deployment experience," which does not count as a named skill, and no other required mention of AI deployment appears.

DECISION: ?

## 48. golden_097 - skill `model-development` (uncertain)

> ...Qualifications: - Experience with training generative machine learning models. - Experience with optimizing the performance of machine...

- A: `model-development` · nice_to_have · raw_text: "training generative machine learning models"
- B: `model-development` · nice_to_have · raw_text: "training generative machine learning models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bonus-qualifications bullet "Experience with training generative machine learning models" names a skill, and its placement under Preferred/Bonus supports the nice_to_have requirement, so the agreed label stands.

DECISION: ok

## 49. golden_098 - attribute `degree` (uncertain)

> ...You’ll Need: Minimum Qualifications: - Master’s with 3+ years of experience, or PhD, in robotics, control or a related field. Strong candidates with a bachelor’s and 3+ years of...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s with 3+ years of experience, or PhD, in robotics, control or a related field"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s with 3+ years of experience, or PhD, in robotics, control or a related field. Strong candidates with a bachelor’s and 3+ years of industry experience are also considered."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Strong candidates with a bachelor’s and 3+ years of industry experience are also considered"} - Under the lowest-level rule the least a candidate must hold is a bachelor's, since the minimum qualifications explicitly admit bachelor's-plus-experience candidates, so the agreed phd (a highest-level reading) is wrong.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Strong candidates with a bachelor’s and 3+ years of industry experience are also considered"}

## 50. golden_098 - skill `reinforcement-learning` (uncertain)

> ...machining. - Robot learning: you have trained or deployed learned policies (imitation learning, RL or VLA) on real robots, and are comfortable with PyTorch and at...

- A: `reinforcement-learning` · required · raw_text: "learned policies (imitation learning, RL or VLA)"
- B: `reinforcement-learning` · required · raw_text: "RL"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Minimum Qualifications bullet names RL as one of the accepted forms of trained learned policies, and rule 3 makes that required mention control, so the agreed required label and quote stand.

DECISION: ok

## 51. golden_099 - attribute `degree` (uncertain)

> ...inference engine. REQUIRED QUALIFICATIONS - BS/MS/PhD in Computer Science, Software Engineering, or a related field. - Deep experience building compilers, optimizing...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="BS/MS/PhD in Computer Science, Software Engineering, or a related field."
- B: value="phd" · requirement="required" · or_equivalent=false · signal="BS/MS/PhD in Computer Science, Software Engineering, or a related field."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "BS/MS/PhD in Computer Science, Software Engineering, or a related field."} - Under the lowest-level rule, the posting's required qualification 'BS/MS/PhD' makes bachelor the degree, not the phd the agreed label recorded under the older highest-level rule.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "BS/MS/PhD in Computer Science, Software Engineering, or a related field."}

## 52. golden_099 - skill `deep-learning` (uncertain)

> ...and parallel execution - Quantization, sparsity, or algorithmic optimization for deep learning - Deep expertise on ML frameworks (e.g., PyTorch,...

- A: `deep-learning` · required · raw_text: "algorithmic optimization for deep learning"
- B: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required-qualifications bullet names deep learning in "Quantization, sparsity, or algorithmic optimization for deep learning", and rule 3 says a required mention wins, so the agreed required label and quoted raw_text stand.

DECISION: ok

## 53. golden_099 - skill `llms` (uncertain)

> ...Strong understanding of one or more of the following: - LLM architectures and transformer internals - MLIR, LLVM, XLA, TVM,...

- A: `llms` · required · raw_text: "LLM architectures"
- B: `llms` · required · raw_text: "LLM architectures"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the REQUIRED QUALIFICATIONS bullet names LLM architectures as an option in a required list, and Rule 3 makes that required mention decisive, so the agreed required label with raw_text "LLM architectures" stands.

DECISION: ok

## 54. golden_099 - skill `quantization` (uncertain)

> ...if improving inference efficiency requires inventing new quantization schemes, rethinking graph-level optimizations, or...

- A: `quantization` · required · raw_text: "Quantization"
- B: `quantization` · required · raw_text: "Quantization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 4, the only visible mention of quantization is in the ROLE SUMMARY as something the company may do ('if improving inference efficiency requires inventing new quantization schemes'), not a candidate requirement, and the excerpt is cut off before any qualifications list where the agreed raw_text 'Quantization' would need to appear.

DECISION: drop

## 55. golden_099 - skill `transformers` (uncertain)

> ...of one or more of the following: - LLM architectures and transformer internals - MLIR, LLVM, XLA, TVM, Triton, or similar compiler...

- A: `transformers` · required · raw_text: "transformer internals"
- B: `transformers` · required · raw_text: "transformer internals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 3, the mention 'transformer internals' appears verbatim in the REQUIRED QUALIFICATIONS section, so the agreed required tag and raw_text stand, though the 'one or more of the following' wording makes it one option among several.

DECISION: ok

## 56. golden_100 - attribute `degree` (uncertain)

> ...trust it. What You’ll Need: Minimum Qualifications: - PhD in robotics, mechanical engineering, applied mathematics, physics, computer graphics or a related field, or a Masters + 3 years of experience. Exceptional candidates with a bachelor’s degree and 3+...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in robotics, mechanical engineering, applied mathematics, physics, computer graphics or a related field, or a Masters + 3 years of experience"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in robotics, mechanical engineering, applied mathematics, physics, computer graphics or a related field, or a Masters + 3 years of experience. Exceptional candidates with a bachelor’s degree and 3+ years of relevant industry experience are also welcome to apply."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_100 - attribute `seniority` (uncertain)

> ...physics, computer graphics or a related field, or a Masters + 3 years of experience. Exceptional candidates with a bachelor’s degree and 3+...

- A: value="mid" · basis="inferred" · signal="a Masters + 3 years of experience"
- B: value="mid" · basis="inferred" · signal="Masters + 3 years of experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, a years-of-experience qualification line does not count as a seniority signal, and the posting names no seniority level (no junior, mid, senior or similar), so the inferred "mid" is unsupported and the attribute should be null.

DECISION: ?

## 58. golden_100 - skill `reinforcement-learning` (uncertain)

> ...for physics (CUDA, NVIDIA Warp or JAX) and experience scaling simulation for reinforcement or imitation learning. - Experience with deformable, cable or FEM simulation...

- A: `reinforcement-learning` · nice_to_have · raw_text: "scaling simulation for reinforcement or imitation learning"
- B: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement or imitation learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_101 - skill `ai-ml` (uncertain)

> ...hardware for AI/ML acceleration. - Deep understanding of modern AI/ML models, particularly LLMs, and their computational...

- A: `ai-ml` · required · raw_text: "modern AI/ML models"
- B: `ai-ml` · required · raw_text: "AI/ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification 'Deep understanding of modern AI/ML models, particularly LLMs' names the skill directly, and the agreed raw_text 'modern AI/ML models' appears verbatim, so the required label stands (rule 3).

DECISION: ok

## 60. golden_101 - skill `distributed-systems` (uncertain)

> ...on-chip interconnects, parallel processing, and distributed computing. - Excellent problem-solving skills and the ability to...

- A: `distributed-systems` · required · raw_text: "distributed computing"
- B: `distributed-systems` · required · raw_text: "distributed computing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Required Qualifications bullet explicitly names "distributed computing" as a required understanding, and rule 3 makes that required mention decisive, so the agreed label stands.

DECISION: ok

## 61. golden_101 - skill `networking` (uncertain)

> ...and deploying hardware accelerators in the cloud. - High-speed inter-chip networking experience What We Offer: - A chance to be a foundational...

- A: `networking` · nice_to_have · raw_text: "High-speed inter-chip networking experience"
- B: `networking` · nice_to_have · raw_text: "High-speed inter-chip networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred/Bonus bullet "High-speed inter-chip networking experience" is a qualification that names networking as a skill, and the nice_to_have requirement matches the preferred section heading.

DECISION: ok

## 62. golden_102 - skill `machine-learning` (uncertain)

> ...Robyn and LightweightMMM - Hands-on experience with machine learning frameworks such as scikit-learn, TensorFlow, or PyTorch applied to...

- A: `machine-learning` · nice_to_have · raw_text: "machine learning frameworks"
- B: `machine-learning` · nice_to_have · raw_text: "machine learning frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "Hands-on experience with machine learning frameworks such as scikit-learn, TensorFlow, or PyTorch" is a qualification naming the skill, and it sits under "While not required, these are a plus," so nice_to_have and the quoted raw_text are correct.

DECISION: ok

## 63. golden_103 - attribute `degree` (uncertain)

> ...deep learning and/or foundation models — whether through a PhD in ML or equivalent hands-on industry work. You're a curious, agile engineer who can generate ideas,...

- A: value="phd" · requirement="required" · or_equivalent=true · signal="PhD in ML or equivalent hands-on industry work"
- B: value="phd" · requirement="required" · or_equivalent=true · signal="a PhD in ML or equivalent hands-on industry work"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": true, "degree_signal": "BS or MSc in Computer Science, Statistics, Engineering, Applied Mathematics, or a related quantitative field (or equivalent experience)"} - Under the degree rule the label is the lowest level named, and the Education line requires a BS or MSc (bare mention, so required, with 'or equivalent experience'), so the agreed 'phd' from the older highest-level rule is wrong.

DECISION: {"degree": "bachelor", "degree_or_equivalent": true, "degree_requirement": "required", "degree_signal": "BS or MSc in Computer Science, Statistics, Engineering, Applied Mathematics, or a related quantitative field (or equivalent experience)"}

## 64. golden_103 - skill `agent-state-management` (uncertain)

> ...and evaluating both - Agentic systems knowledge — tools, memory, and long-running workflows - Strong software engineering fundamentals — performant,...

- A: `agent-state-management` · required · raw_text: "memory, and long-running workflows"
- B: `agent-state-management` · required · raw_text: "Agentic systems knowledge — tools, memory"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What You'll Need' bullet 'Agentic systems knowledge — tools, memory, and long-running workflows' is a qualification that names the skill, and the agreed raw_text 'memory, and long-running workflows' appears verbatim in it (rule 3), so the required label stands.

DECISION: ok

## 65. golden_103 - skill `ai-deployment` (uncertain)

> ...— data preprocessing, model training, evaluation, inference, and deployment - Experience with end-to-end model development — dataset...

- A: `ai-deployment` · required · raw_text: "inference, and deployment"
- B: `ai-deployment` · required · raw_text: "model training, evaluation, inference, and deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet names deployment ("inference, and deployment") as part of its ML infrastructure experience list, so the agreed required ai-deployment label stands; the years-of-experience clause alone would not have counted.

DECISION: ok

## 66. golden_103 - skill `ai-infrastructure` (uncertain)

> ...You’ll Need: - 8 years of industry experience w 4+ years of ML infrastructure experience — data preprocessing, model training, evaluation,...

- A: `ai-infrastructure` · required · raw_text: "4+ years of ML infrastructure experience"
- B: `ai-infrastructure` · required · raw_text: "ML infrastructure experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, "4+ years of ML infrastructure experience" is a years-of-experience line like the rule's "experience as a software engineer" example, so it does not establish the ai-infrastructure skill, and no other required mention in the excerpt names it.

DECISION: ?

## 67. golden_103 - skill `aws` (uncertain)

> ...Familiarity with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and collaboration skills...

- A: `aws` · required · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the 'What You'll Need' bullet 'Familiarity with cloud and containerization (e.g., GCP, AWS, Docker)' is a qualification naming AWS, the required raw_text 'AWS' appears verbatim, and Rule 5 is not triggered because AWS itself is named rather than inferred from a parent category.

DECISION: ok

## 68. golden_103 - skill `gcp` (uncertain)

> ...Familiarity with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and collaboration...

- A: `gcp` · required · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What You'll Need' bullet asks for familiarity with cloud platforms and explicitly names GCP as one of them, so the qualification names the skill as required, and the agreed raw_text "GCP" appears in the posting.

DECISION: ok

## 69. golden_103 - skill `observability` (uncertain)

> ...— dataset construction, training, fine-tuning, evaluation, profiling, and monitoring - Familiarity with modern model architectures — including...

- A: `observability` · required · raw_text: "profiling, and monitoring"
- B: `observability` · required · raw_text: "monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the 'What You'll Need' qualifications, rule 1 applies because the bullet asks for experience with 'profiling, and monitoring' as part of end-to-end model development, and monitoring is a named observability practice, so the agreed required label stands.

DECISION: ?

## 70. golden_103 - skill `tool-calling` (uncertain)

> ...LLaVA), and experience training and evaluating both - Agentic systems knowledge — tools, memory, and long-running workflows - Strong software...

- A: `tool-calling` · required · raw_text: "Agentic systems knowledge — tools"
- B: `tool-calling` · required · raw_text: "Agentic systems knowledge — tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet "Agentic systems knowledge — tools, memory, and long-running workflows" names tools in an agentic context, which is tool-calling, and rule 3 makes that required mention decisive, so the agreed label stands.

DECISION: ok

## 71. golden_104 - attribute `degree` (uncertain)

> ...scientists, engineers, and product managers. Preferred - Master’s degree or PhD in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field. - Experience with LLMOps, including model evaluation,...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s degree or PhD in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field."
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s degree or PhD in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Bachelor’s degree in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field."} - Under the degree rule the label is the lowest level named, so the required bachelor's in 'What You Bring' applies, and the optional Master's/PhD under 'Preferred' is not recorded, as the agreed phd label reflects the older highest-level rule.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Bachelor’s degree in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field."}

## 72. golden_104 - skill `data-privacy-and-security` (uncertain)

> ...large-scale models. - Familiarity with model encryption, privacy-preserving machine learning, and secure AI techniques. Benefits that Benefit You -...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving machine learning"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving machine learning, and secure AI techniques"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred bullet "Familiarity with model encryption, privacy-preserving machine learning, and secure AI techniques" is a qualification that names the skill, so the agreed nice_to_have label and the verbatim raw_text are correct.

DECISION: ok

## 73. golden_105 - skill `ai-developer-tooling` (uncertain)

> ...in production. - Demonstrated, heavy AI-native delivery: consistent use of AI across the SDLC with concrete examples of faster delivery and...

- A: `ai-developer-tooling` · required · raw_text: "consistent use of AI across the SDLC"
- B: `ai-developer-tooling` · required · raw_text: "AI-native delivery: consistent use of AI across the SDLC"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required qualification bullet "Demonstrated, heavy AI-native delivery... consistent use of AI across the SDLC" names AI use in the development workflow, and rule 3 makes that required mention decisive, so the agreed required label stands.

DECISION: ok

## 74. golden_105 - skill `ai-ml` (uncertain)

> ...0→1→initial scale delivery. - Experience integrating AI/LLM capabilities into product experiences responsibly. - Track record of...

- A: `ai-ml` · nice_to_have · raw_text: "AI/LLM capabilities"
- B: `ai-ml` · nice_to_have · raw_text: "integrating AI/LLM capabilities into product experiences responsibly"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Preferred Qualifications, the bullet 'Experience integrating AI/LLM capabilities into product experiences responsibly' names an AI/ML skill (rule 1), so nice_to_have and the verbatim raw_text 'AI/LLM capabilities' are correct as agreed.

DECISION: ok

## 75. golden_105 - skill `cloud` (uncertain)

> ...decisions stick. - Experience designing, building, and operating cloud-native systems that scale, including reliability and observability best...

- A: `cloud` · required · raw_text: "operating cloud-native systems that scale"
- B: `cloud` · required · raw_text: "cloud-native systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Required Skills bullet names cloud-native systems as a qualification, and the agreed raw_text "operating cloud-native systems that scale" appears verbatim, so the required `cloud` label stands.

DECISION: ok

## 76. golden_106 - skill `ai-infrastructure` (uncertain)

> ...years of professional experience in systems programming, ML infrastructure, or distributed inference. - Proficient in C++ and...

- A: `ai-infrastructure` · required · raw_text: "ML infrastructure"
- B: `ai-infrastructure` · required · raw_text: "ML infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only mention of ML infrastructure is inside the '3+ years of professional experience in ... ML infrastructure' line, which is a years-of-experience line and does not count as a named skill.

DECISION: ?

## 77. golden_106 - skill `docker` (uncertain)

> ...workloads. - Familiarity with containerized deployments (Docker/Kubernetes). - Exposure to distributed systems or large-scale...

- A: `docker` · nice_to_have · raw_text: "Docker/Kubernetes"
- B: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the PREFERRED / BONUS bullet "Familiarity with containerized deployments (Docker/Kubernetes)" names Docker as a nice-to-have, and the agreed raw_text "Docker/Kubernetes" appears verbatim in the posting.

DECISION: ok

## 78. golden_106 - skill `kubernetes` (uncertain)

> ...workloads. - Familiarity with containerized deployments (Docker/Kubernetes). - Exposure to distributed systems or large-scale...

- A: `kubernetes` · nice_to_have · raw_text: "Docker/Kubernetes"
- B: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "Familiarity with containerized deployments (Docker/Kubernetes)" names Kubernetes, the raw_text appears verbatim, and its placement under PREFERRED / BONUS makes nice_to_have the correct requirement level.

DECISION: ok

## 79. golden_106 - skill `model-serving` (uncertain)

> ...analysis skills. - Deep familiarity with one or more LLM serving frameworks (vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference, etc.)....

- A: `model-serving` · required · raw_text: "LLM serving frameworks"
- B: `model-serving` · required · raw_text: "LLM serving frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the REQUIRED QUALIFICATIONS bullet asks for 'Deep familiarity with one or more LLM serving frameworks,' and Rule 3 makes that required mention decisive, so the agreed required model-serving label with raw_text 'LLM serving frameworks' stands.

DECISION: ok

## 80. golden_107 - attribute `seniority` (uncertain)

> ...advance state-of-the-art in the generative AI domain. - Define and lead high impact applied research initiatives. - Writing high-quality code, designing and performing...

- A: value="senior" · basis="inferred" · signal="Define and lead high impact applied research initiatives."
- B: value="senior" · basis="inferred" · signal="3+ years of experience leading Machine Learning research initiatives."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 4, the responsibility-line signal is backed by a required qualification ('3+ years of experience leading Machine Learning research initiatives'), so the inferred 'senior' value stands with its verbatim signal.

DECISION: ok

## 81. golden_107 - skill `docker` (uncertain)

> ...containerization and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a...

- A: `docker` · nice_to_have · raw_text: "Docker"
- B: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred/Bonus bullet "Experience with containerization and orchestration technologies (e.g., Docker, Kubernetes)" is a qualification naming the skill, so it counts; it is correctly marked nice_to_have, and "Docker" appears verbatim in the posting.

DECISION: ok

## 82. golden_107 - skill `kubernetes` (uncertain)

> ...and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a foundational...

- A: `kubernetes` · nice_to_have · raw_text: "Kubernetes"
- B: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the preferred-qualifications bullet "Experience with containerization and orchestration technologies (e.g., Docker, Kubernetes)" names Kubernetes, so it counts as a nice_to_have skill, and the raw_text "Kubernetes" appears verbatim in the posting.

DECISION: ok

## 83. golden_107 - skill `machine-learning` (uncertain)

> ...or a related field. - 3+ years of experience leading Machine Learning research initiatives. - Demonstrated history of research with publications in...

- A: `machine-learning` · required · raw_text: "Machine Learning research initiatives"
- B: `machine-learning` · required · raw_text: "Machine Learning research"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required bullet '3+ years of experience leading Machine Learning research initiatives' names machine learning as a skill, not just a title or years line, and rule 3 makes that required mention decisive.

DECISION: ok

## 84. golden_108 - attribute `degree` (uncertain)

> ...excellent communications skills. It's A Bonus If You: - Have a Ph. D. in computer or computational science, atmospheric science or a related geophysical science, or...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Have a Ph. D. in computer or computational science"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Have a Ph. D. in computer or computational science, atmospheric science or a related geophysical science, or applied mathematics/statistics"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "A B.Sc. in computer or computational science"} - Under the rule's lowest-level test, the required 'What You'll Need' bachelor's (B.Sc.) sets the degree, and the Ph.D. under 'It's A Bonus If You' is a welcomed higher level that is not recorded, so the agreed phd/nice_to_have label is wrong.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "A B.Sc. in computer or computational science"}

## 85. golden_108 - attribute `seniority` (uncertain)

> ...to interested user groups. What You’ll Need: - 2-4 years of experience building and deploying a relevant ML application in a...

- A: value="mid" · basis="inferred" · signal="2-4 years of experience"
- B: value="mid" · basis="inferred" · signal="2-4 years of experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Rule 1 bars a years-of-experience line from counting as a skill, but seniority is an attribute, not a skill, and the quoted "2-4 years of experience" appears verbatim and supports an inferred mid level.

DECISION: ok

## 86. golden_108 - skill `cloud` (uncertain)

> ...mathematics/statistics. - Experience in developing ML training code for use in a cloud computing environment. - Demonstrated excellent communications skills. It's A...

- A: `cloud` · required · raw_text: "ML training code for use in a cloud computing environment"
- B: `cloud` · required · raw_text: "cloud computing environment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the 'What You'll Need' section names cloud computing as a required experience area ('ML training code for use in a cloud computing environment'), and Rule 3 confirms the required mention, so the agreed label and raw_text stand.

DECISION: ok

## 87. golden_094 - attribute `german` (spot-check)

> Staff Machine Learning Engineer, Growth

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_094 - skill `ai-developer-tooling` (spot-check)

> ...Proficient programming skills in Python and SQL. Power user of AI coding tools. - Exceptional communication skills with the ability to...

- agreed label: `ai-developer-tooling` · required · raw_text: "Power user of AI coding tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_094 - skill `forecasting` (spot-check)

> ...learning modeling and statistics, specifically leveraging time series forecasting, probabilistic models, and deep learning models -...

- agreed label: `forecasting` · required · raw_text: "time series forecasting"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_095 - attribute `german` (spot-check)

> Senior Software Engineer, AI Agentic Platform

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_095 - attribute `seniority` (spot-check)

> Senior Software Engineer, AI Agentic Platform Who we are The real world is the...

- agreed label: value="senior" · basis="stated" · signal="Senior Software Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_095 - skill `ai-developer-tooling` (spot-check)

> ...and caching patterns - Demonstrated experience leveraging AI-powered development tools such as Claude Code, GitHub Copilot, or similar agentic...

- agreed label: `ai-developer-tooling` · required · raw_text: "AI-powered development tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_095 - skill `autogen` (spot-check)

> ...protocols such as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in microservices...

- agreed label: `autogen` · required · raw_text: "AutoGen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_095 - skill `claude-code` (spot-check)

> ...experience leveraging AI-powered development tools such as Claude Code, GitHub Copilot, or similar agentic coding tools for...

- agreed label: `claude-code` · required · raw_text: "such as Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_095 - skill `cloud` (spot-check)

> ...architecture, container orchestration (Kubernetes), and cloud platforms (AWS) - Observability and LLMOps expertise, including...

- agreed label: `cloud` · required · raw_text: "cloud platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_095 - skill `containerization` (spot-check)

> ...or LlamaIndex - Expertise in microservices architecture, container orchestration (Kubernetes), and cloud platforms (AWS) - Observability...

- agreed label: `containerization` · required · raw_text: "container orchestration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_095 - skill `fine-tuning` (spot-check)

> ...field - Experience building customized agent harnesses, fine-tuning models, or implementing RLHF/RLAIF optimization loops - Security...

- agreed label: `fine-tuning` · nice_to_have · raw_text: "fine-tuning models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_095 - skill `google-adk` (spot-check)

> ...frameworks and protocols such as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in microservices...

- agreed label: `google-adk` · required · raw_text: "Google ADK"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_095 - skill `java` (spot-check)

> ...+ Frameworks: TypeScript, React, Scala (principally), Java (limited) - Datastores: MySQL, PostgreSQL, Snowflake - Cloud:...

- agreed label: `java` · required · raw_text: "Java (limited)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_095 - skill `llamaindex` (spot-check)

> ...as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in microservices architecture, container...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_095 - skill `llm-orchestration` (spot-check)

> ...experience architecting and deploying agentic AI systems, LLM orchestration frameworks, or AI platform tooling - Strong proficiency in Python or...

- agreed label: `llm-orchestration` · required · raw_text: "LLM orchestration frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_095 - skill `llmops` (spot-check)

> ...and cloud platforms (AWS) - Observability and LLMOps expertise, including metrics, distributed tracing, structured...

- agreed label: `llmops` · required · raw_text: "LLMOps expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 103. golden_095 - skill `observability` (spot-check)

> ...orchestration (Kubernetes), and cloud platforms (AWS) - Observability and LLMOps expertise, including metrics, distributed tracing, structured...

- agreed label: `observability` · required · raw_text: "Observability and LLMOps expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_095 - skill `vector-databases` (spot-check)

> ...and data systems knowledge including relational databases, vector databases, event streaming (Kafka, SQS), and caching patterns -...

- agreed label: `vector-databases` · required · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_096 - skill `argocd` (spot-check)

> ...state (Ansible, Puppet, Salt) and GitOps workflows (Argo CD, Flux). - Experience in OS configuration tooling. -...

- agreed label: `argocd` · required · raw_text: "Argo CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_096 - skill `gcp` (spot-check)

> ...clusters. - 2–3 years of production experience operating workloads on AWS or GCP. - Proven track record running ML or inference services...

- agreed label: `gcp` · required · raw_text: "operating workloads on AWS or GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_096 - skill `gitops` (spot-check)

> ...OS configuration state (Ansible, Puppet, Salt) and GitOps workflows (Argo CD, Flux). - Experience in OS configuration...

- agreed label: `gitops` · required · raw_text: "GitOps workflows"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_096 - skill `observability` (spot-check)

> ...accelerators beyond GPUs (FPGAs, custom ASICs). - Background in observability, SRE, or performance engineering for latency-sensitive...

- agreed label: `observability` · nice_to_have · raw_text: "Background in observability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_096 - skill `python` (spot-check)

> ...plugins, MIG, networking, and storage considerations. - Solid coding skills in Python, Bash and proficiency in Go - Proficient in configuring...

- agreed label: `python` · required · raw_text: "Solid coding skills in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_096 - skill `triton-inference-server` (spot-check)

> ...- Experience with inference servers and runtimes (e.g., Triton, vLLM, TGI) and model-serving patterns (batching,...

- agreed label: `triton-inference-server` · nice_to_have · raw_text: "Triton"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_097 - attribute `degree` (spot-check)

> ...our inference solutions. Required Qualifications: - PhD/MS in Computer Science, Computer Engineering, or a related field. - 3+ years of machine learning R&D and deployment...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="PhD/MS in Computer Science, Computer Engineering, or a related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "PhD/MS in Computer Science, Computer Engineering, or a related field"} - Under the rule's lowest-level test, the posting names both PhD and MS, and MS is the lower level, so the degree is master, not the phd recorded under the older highest-level rule; the mention is a bare entry in Required Qualifications, so it stays required with no equivalent-experience clause.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "PhD/MS in Computer Science, Computer Engineering, or a related field"}

## 112. golden_097 - skill `containerization` (spot-check)

> ...cloud platforms (AWS, GCP, Azure). - Experience with containerization and orchestration technologies (e.g., Docker,...

- agreed label: `containerization` · nice_to_have · raw_text: "containerization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_097 - skill `cpp` (spot-check)

> ...in one or more programming languages such as Python, or C++. - Proficiency in at least one ML framework (e.g.,...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_097 - skill `docker` (spot-check)

> ...containerization and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_097 - skill `kubernetes` (spot-check)

> ...and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a foundational...

- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_097 - skill `nlp` (spot-check)

> ...leading research initiatives in Machine Learning, Natural Language Processing, and related fields. - Familiarity with performance...

- agreed label: `nlp` · nice_to_have · raw_text: "Natural Language Processing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_097 - skill `python` (spot-check)

> ...proficiency in one or more programming languages such as Python, or C++. - Proficiency in at least one ML framework...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_097 - skill `pytorch` (spot-check)

> ...C++. - Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Solid understanding of software...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_097 - skill `tensorflow` (spot-check)

> ...- Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Solid understanding of software engineering...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_097 - skill `testing` (spot-check)

> ...best practices, including data structures, algorithms, and testing. - Excellent problem-solving abilities and a knack for...

- agreed label: `testing` · required · raw_text: "testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_098 - attribute `german` (spot-check)

> Research Engineer, Robotics - Roboticist

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_098 - skill `python` (spot-check)

> ...can reason about latency, reliability and failure modes. Strong Python; solid real-time C++. - Mechanical design: you have...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_098 - skill `pytorch` (spot-check)

> ...(imitation learning, RL or VLA) on real robots, and are comfortable with PyTorch and at least one simulation ecosystem (Isaac Lab, MuJoCo...

- agreed label: `pytorch` · required · raw_text: "comfortable with PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_099 - skill `python` (spot-check)

> ...frameworks at a systems level. - Strong proficiency in one or more programming languages such as Python and C++. - Strong understanding of one or more of the...

- agreed label: `python` · required · raw_text: "one or more programming languages such as Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_099 - skill `testing` (spot-check)

> ...best practices, including data structures, algorithms, and testing. - Thinking in terms of latency, cycles, memory...

- agreed label: `testing` · required · raw_text: "testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_100 - attribute `german` (spot-check)

> Research Engineer, Robotics: Physics Simulation and Sim-to-Real

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_100 - skill `python` (spot-check)

> ...result quantitatively against real-world recordings. - Proficiency in Python and C++, experience with robot description formats (URDF,...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_101 - skill `cloud` (spot-check)

> ...research publications or open-source projects. - Understanding of cloud computing environments and deploying hardware accelerators in the cloud. -...

- agreed label: `cloud` · nice_to_have · raw_text: "Understanding of cloud computing environments"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_101 - skill `quantization` (spot-check)

> ...of ML optimization techniques (e.g., sparsity, quantization, pruning). - Proficiency in Verilog or SystemVerilog for...

- agreed label: `quantization` · required · raw_text: "quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_102 - attribute `degree` (spot-check)

> ...high-output processes What we're looking for - Bachelor’s or Master’s degree in Computer Science, Mathematics, Statistics, Economics, or a related quantitative field - 6+ years of proven experience as a Data Scientist or...

- agreed label: value="master" · requirement="required" · or_equivalent=false · signal="Bachelor’s or Master’s degree in Computer Science, Mathematics, Statistics, Economics, or a related quantitative field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Bachelor’s or Master’s degree in Computer Science, Mathematics, Statistics, Economics, or a related quantitative field"} - Under the degree rule, `degree` is the lowest level named, and "Bachelor's or Master's" therefore gives `bachelor`, not the older highest-level `master`; the bare mention in the requirements list stays `required`, and the "related quantitative field" wording widens the field only, so `degree_or_equivalent` stays false.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Bachelor’s or Master’s degree in Computer Science, Mathematics, Statistics, Economics, or a related quantitative field"}

## 131. golden_102 - skill `causal-inference` (spot-check)

> ...Hands-on experience with statistical experimentation and causal inference techniques such as A/B testing, geo-testing, synthetic controls, and...

- agreed label: `causal-inference` · required · raw_text: "causal inference techniques"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_102 - skill `dbt` (spot-check)

> ...data warehouses and modern data tools such as Snowflake, dbt, Looker, and Tableau - Familiarity with Media Mix...

- agreed label: `dbt` · nice_to_have · raw_text: "dbt"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_102 - skill `pytorch` (spot-check)

> ...learning frameworks such as scikit-learn, TensorFlow, or PyTorch applied to user segmentation or churn prediction -...

- agreed label: `pytorch` · nice_to_have · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_102 - skill `sagemaker` (spot-check)

> ...Experience with cloud platforms, including AWS S3, SageMaker, and Airflow - Experience with cloud data warehouses and...

- agreed label: `sagemaker` · nice_to_have · raw_text: "SageMaker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_102 - skill `scikit-learn` (spot-check)

> ...experience with machine learning frameworks such as scikit-learn, TensorFlow, or PyTorch applied to user segmentation or...

- agreed label: `scikit-learn` · nice_to_have · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_102 - skill `sql` (spot-check)

> ...media, or adtech - Advanced proficiency in Python and SQL for complex data manipulation, statistical modeling, and predictive analytics - Deep...

- agreed label: `sql` · required · raw_text: "SQL for complex data manipulation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 137. golden_102 - skill `statistics` (spot-check)

> ...in Python and SQL for complex data manipulation, statistical modeling, and predictive analytics - Deep domain expertise in...

- agreed label: `statistics` · required · raw_text: "statistical modeling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 138. golden_102 - skill `tableau` (spot-check)

> ...and modern data tools such as Snowflake, dbt, Looker, and Tableau - Familiarity with Media Mix Modeling (MMM) frameworks...

- agreed label: `tableau` · nice_to_have · raw_text: "Tableau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_103 - attribute `seniority` (spot-check)

> Senior Research Engineer, Olmo + Molmo Persons in these roles are expected to work...

- agreed label: value="senior" · basis="stated" · signal="Senior Research Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 140. golden_103 - skill `containerization` (spot-check)

> ...pick up new tools as needed - Familiarity with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and...

- agreed label: `containerization` · required · raw_text: "containerization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_103 - skill `docker` (spot-check)

> ...with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and collaboration skills — we're...

- agreed label: `docker` · required · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 142. golden_103 - skill `evaluation` (spot-check)

> ...of ML infrastructure experience — data preprocessing, model training, evaluation, inference, and deployment - Experience with end-to-end...

- agreed label: `evaluation` · required · raw_text: "model training, evaluation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_103 - skill `fine-tuning` (spot-check)

> ...model development — dataset construction, training, fine-tuning, evaluation, profiling, and monitoring - Familiarity with...

- agreed label: `fine-tuning` · required · raw_text: "fine-tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 144. golden_103 - skill `jax` (spot-check)

> ...Proficiency in Python and a major ML framework (PyTorch, JAX, or TensorFlow), with the flexibility to pick up new tools...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 145. golden_103 - skill `model-development` (spot-check)

> ...evaluation, inference, and deployment - Experience with end-to-end model development — dataset construction, training, fine-tuning, evaluation,...

- agreed label: `model-development` · required · raw_text: "end-to-end model development"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 146. golden_103 - skill `pytorch` (spot-check)

> ...Proficiency in Python and a major ML framework (PyTorch, JAX, or TensorFlow), with the flexibility to pick up new...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 147. golden_104 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer Join Axon and be a Force for Good. At Axon, we’re on a...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 148. golden_104 - skill `cpp` (spot-check)

> ...and infrastructure as code. - Proficiency in Python and C++, with experience using ML frameworks such as PyTorch or...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_104 - skill `fine-tuning` (spot-check)

> ...and production deployment. - Hands-on experience fine-tuning and optimizing large-scale models. - Familiarity with model encryption, privacy-preserving...

- agreed label: `fine-tuning` · nice_to_have · raw_text: "fine-tuning and optimizing large-scale models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 150. golden_104 - skill `knowledge-distillation` (spot-check)

> ...including model evaluation, monitoring, quantization, distillation/teacher-student approaches, and production deployment. - Hands-on experience...

- agreed label: `knowledge-distillation` · nice_to_have · raw_text: "distillation/teacher-student approaches"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_104 - skill `llmops` (spot-check)

> ...Mathematics, or another highly technical field. - Experience with LLMOps, including model evaluation, monitoring, quantization,...

- agreed label: `llmops` · nice_to_have · raw_text: "Experience with LLMOps"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_104 - skill `quantization` (spot-check)

> ...models, including approaches such as model distillation, quantization, and scalable evaluation. - Solve challenging...

- agreed label: `quantization` · nice_to_have · raw_text: "quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_104 - skill `software-architecture` (spot-check)

> ...dive deep into complex system architectures. - Excellent software architecture and design skills, with a focus on building robust, scalable, maintainable...

- agreed label: `software-architecture` · required · raw_text: "software architecture and design skills"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_104 - skill `software-engineering` (spot-check)

> ...or another highly technical field. - 6+ years of software engineering experience, including a proven track record of deploying AI/ML models...

- agreed label: `software-engineering` · required · raw_text: "software engineering experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_104 - skill `tensorflow` (spot-check)

> ...with experience using ML frameworks such as PyTorch or TensorFlow. - Advanced, hands-on knowledge of Linux environments and...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_105 - attribute `german` (spot-check)

> Senior Software Engineer, Axon AI

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 157. golden_106 - skill `cpp` (spot-check)

> ...ML infrastructure, or distributed inference. - Proficient in C++ and Python, with strong debugging and performance analysis...

- agreed label: `cpp` · required · raw_text: "Proficient in C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 158. golden_106 - skill `deepspeed` (spot-check)

> ...more LLM serving frameworks (vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference, etc.). - Understanding of model deployment internals —...

- agreed label: `deepspeed` · required · raw_text: "DeepSpeed-Inference"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 159. golden_106 - skill `vllm` (spot-check)

> ...Deep familiarity with one or more LLM serving frameworks (vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference, etc.). - Understanding of model deployment internals —...

- agreed label: `vllm` · required · raw_text: "vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 160. golden_107 - skill `aws` (spot-check)

> ...techniques. - Experience with cloud platforms (AWS, GCP, Azure). - Experience with containerization and...

- agreed label: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 161. golden_107 - skill `gcp` (spot-check)

> ...techniques. - Experience with cloud platforms (AWS, GCP, Azure). - Experience with containerization and...

- agreed label: `gcp` · nice_to_have · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 162. golden_107 - skill `jax` (spot-check)

> ...in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Strong proficiency in one or more programming...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 163. golden_107 - skill `python` (spot-check)

> ...proficiency in one or more programming languages such as Python, or C++. - Strong communication skills and a proven...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 164. golden_107 - skill `pytorch` (spot-check)

> ...VLMs. - Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Strong proficiency in one or more...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 165. golden_107 - skill `tensorflow` (spot-check)

> ...- Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Strong proficiency in one or more programming...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 166. golden_108 - skill `python` (spot-check)

> ...in a practical or academic research setting and be fluent in Python and collaborative coding practices. - A B.Sc. in computer...

- agreed label: `python` · required · raw_text: "fluent in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 167. golden_101 - attribute `degree` (rule-change)

> ...engineering team. Required Qualifications: - BS, MS or PhD in Computer Engineering, Electrical Engineering, or a related field. - Proven experience (5+ years) in hardware design, with...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="BS, MS or PhD in Computer Engineering, Electrical Engineering, or a related field."

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "BS, MS or PhD in Computer Engineering, Electrical Engineering, or a related field."} - Under the degree rule, `degree` is the lowest level named, and "BS, MS or PhD" names bachelor as the least a candidate must hold; the bare mention in Required Qualifications is `required`, and the "related field" wording widens the field, not the requirement, so or_equivalent is false.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "BS, MS or PhD in Computer Engineering, Electrical Engineering, or a related field."}

## 168. golden_106 - attribute `degree` (rule-change)

> ...kernels and PCIe drivers. REQUIRED QUALIFICATIONS - BS/MS/PhD in Computer Science, Electrical/Computer Engineering, or related field. - 3+ years of professional experience in systems...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="BS/MS/PhD in Computer Science, Electrical/Computer Engineering, or related field"

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "BS/MS/PhD in Computer Science, Electrical/Computer Engineering, or related field"} - Under the degree rule, `degree` is the lowest level named, and the posting names BS/MS/PhD, so the label should be `bachelor` rather than the older highest-level `phd`; the bare mention in the required qualifications stays `required`, and 'related field' widens the field only, so `degree_or_equivalent` stays false.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "BS/MS/PhD in Computer Science, Electrical/Computer Engineering, or related field"}

## 169. golden_094 - groups `alternative_group` (groups)

> Staff Machine Learning Engineer, Growth

- `a-b-testing` · required · raw_text: "A/B testing, DiD, Bandits"
- `agents` · nice_to_have · raw_text: "Experience building agentic AI solutions for pricing is highly desirable"
- `ai-deployment` · required · raw_text: "successfully deploying models"
- `ai-developer-tooling` · required · raw_text: "Power user of AI coding tools"
- `airflow` · required · raw_text: "workflow orchestration via Airflow"
- `apache-spark` · required · raw_text: "distributed processing with Spark"
- `aws` · required · raw_text: "AWS data storage"
- `causal-inference` · required · raw_text: "Solid understanding of causal inference"
- `data-pipelines` · required · raw_text: "data pipeline development"
- `deep-learning` · required · raw_text: "deep learning models"
- `forecasting` · required · raw_text: "time series forecasting"
- `machine-learning` · required · raw_text: "Strong experience in machine learning modeling"
- `python` · required · raw_text: "Python"
- `sql` · required · raw_text: "SQL"
- `statistics` · required · raw_text: "machine learning modeling and statistics"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for its skills together, with no 'at least one of' or 'X, Y or Z' marker: 'A/B testing, DiD, Bandits and uplift modeling' is a set of methods used jointly, and Python, SQL, Spark, Airflow and AWS are each required alongside the others, so under the rule's 'Not alternatives' clause no group applies.

DECISION: []

## 170. golden_095 - groups `alternative_group` (groups)

> Senior Software Engineer, AI Agentic Platform

- `agent-architecture` · required · raw_text: "architecting and deploying agentic AI systems"
- `agent-harnesses` · nice_to_have · raw_text: "building customized agent harnesses"
- `agents` · required · raw_text: "agentic AI systems"
- `ai-deployment` · required · raw_text: "deploying agentic AI systems"
- `ai-developer-tooling` · required · raw_text: "AI-powered development tools"
- `api-design` · required · raw_text: "API design"
- `async-processing` · required · raw_text: "async concurrency"
- `autogen` · required · raw_text: "AutoGen"
- `aws` · required · raw_text: "cloud platforms (AWS)"
- `backend-development` · required · raw_text: "backend software engineering"
- `claude-code` · required · raw_text: "such as Claude Code"
- `cloud` · required · raw_text: "cloud platforms"
- `containerization` · required · raw_text: "container orchestration"
- `data-privacy-and-security` · nice_to_have · raw_text: "data privacy"
- `distributed-systems` · required · raw_text: "deep focus on distributed systems"
- `fine-tuning` · nice_to_have · raw_text: "fine-tuning models"
- `git` · required · raw_text: "Version control: Git & GitHub"
- `github-copilot` · required · raw_text: "GitHub Copilot"
- `google-adk` · required · raw_text: "Google ADK"
- `java` · required · raw_text: "Java (limited)"
- `kafka` · required · raw_text: "Kafka"
- `kubernetes` · required · raw_text: "Kubernetes"
- `langgraph` · required · raw_text: "LangGraph"
- `llamaindex` · required · raw_text: "LlamaIndex"
- `llm-orchestration` · required · raw_text: "LLM orchestration frameworks"
- `llmops` · required · raw_text: "LLMOps expertise"
- `mcp` · required · raw_text: "Anthropic MCP"
- `microservices` · required · raw_text: "microservices architecture"
- `mysql` · required · raw_text: "MySQL"
- `observability` · required · raw_text: "Observability and LLMOps expertise"
- `postgresql` · required · raw_text: "PostgreSQL"
- `python` · required · raw_text: "Strong proficiency in Python"
- `react` · required · raw_text: "React"
- `scala` · required · raw_text: "Scala (principally)"
- `secrets-management` · nice_to_have · raw_text: "secrets management"
- `snowflake` · required · raw_text: "Snowflake"
- `typescript` · required · raw_text: "Languages + Frameworks: TypeScript"
- `vector-databases` · required · raw_text: "vector databases"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["langgraph", "google-adk", "autogen", "llamaindex"]] - The 'such as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex' list is one ask with examples, so the labeled members form a group. MCP is left out because the responsibilities separately ask for 'MCP integrations', and the Python/Java/TypeScript and Claude Code/Copilot sets are dropped because their members also appear as unmarked stack entries, which the rule says leaves a group.

DECISION: [["autogen", "google-adk", "langgraph", "llamaindex"]]

## 171. golden_096 - groups `alternative_group` (groups)

> AI Inference Infrastructure Software Engineer (Kubernetes / Cloud)

- `ansible` · required · raw_text: "Ansible"
- `apis` · nice_to_have · raw_text: "customer facing API platforms"
- `argocd` · required · raw_text: "Argo CD"
- `aws` · required · raw_text: "operating workloads on AWS or GCP"
- `bash` · required · raw_text: "Bash"
- `gcp` · required · raw_text: "operating workloads on AWS or GCP"
- `gitops` · required · raw_text: "GitOps workflows"
- `go` · required · raw_text: "proficiency in Go"
- `infrastructure-as-code` · required · raw_text: "infrastructure-as-code"
- `kubernetes` · required · raw_text: "hands-on Kubernetes experience"
- `linux` · required · raw_text: "Proficient in configuring and leveraging Linux OS in production"
- `model-development` · required · raw_text: "AI inference and/or training workflows"
- `model-serving` · nice_to_have · raw_text: "model-serving patterns"
- `networking` · required · raw_text: "networking, and storage considerations"
- `observability` · nice_to_have · raw_text: "Background in observability"
- `python` · required · raw_text: "Solid coding skills in Python"
- `terraform` · required · raw_text: "Terraform"
- `triton-inference-server` · nice_to_have · raw_text: "Triton"
- `vllm` · nice_to_have · raw_text: "vLLM"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The only alternative marker is "operating workloads on AWS or GCP", but the responsibilities separately ask to "Manage and harden our AWS, GCP, and on-prem infrastructure", so aws and gcp are each asked for on their own and leave the group. The other parenthetical examples (Terraform/Pulumi, Ansible/Puppet/Salt, Argo CD/Flux) include only one labeled skill or name a broad parent alongside its examples, so they form no group.

DECISION: ?

## 172. golden_097 - groups `alternative_group` (groups)

> Machine Learning Engineer

- `ai-deployment` · required · raw_text: "machine learning R&D and deployment experience"
- `aws` · nice_to_have · raw_text: "AWS"
- `azure` · nice_to_have · raw_text: "Azure"
- `cloud` · nice_to_have · raw_text: "cloud platforms"
- `containerization` · nice_to_have · raw_text: "containerization"
- `cpp` · required · raw_text: "C++"
- `docker` · nice_to_have · raw_text: "Docker"
- `gcp` · nice_to_have · raw_text: "GCP"
- `jax` · required · raw_text: "JAX"
- `kubernetes` · nice_to_have · raw_text: "Kubernetes"
- `machine-learning` · required · raw_text: "3+ years of machine learning R&D"
- `model-development` · nice_to_have · raw_text: "training generative machine learning models"
- `nlp` · nice_to_have · raw_text: "Natural Language Processing"
- `python` · required · raw_text: "Python"
- `pytorch` · required · raw_text: "PyTorch"
- `software-engineering` · required · raw_text: "software engineering best practices"
- `tensorflow` · required · raw_text: "TensorFlow"
- `testing` · required · raw_text: "testing"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["python", "cpp"], ["pytorch", "tensorflow", "jax"], ["aws", "gcp", "azure"], ["docker", "kubernetes"]] - Under the alternative_group rule, each example list offered for a single ask (programming language such as Python or C++; ML framework e.g. PyTorch, TensorFlow or JAX; cloud platforms AWS, GCP or Azure; containerization e.g. Docker or Kubernetes) forms a group, with the broad parents 'cloud' and 'containerization' kept out, and none of these skills is asked on its own elsewhere.

DECISION: [["aws", "azure", "gcp"], ["cpp", "python"], ["docker", "kubernetes"], ["jax", "pytorch", "tensorflow"]]

## 173. golden_098 - groups `alternative_group` (groups)

> Research Engineer, Robotics - Roboticist

- `ci-cd` · nice_to_have · raw_text: "CI/CD"
- `computer-vision` · nice_to_have · raw_text: "3D perception on hardware"
- `containerization` · nice_to_have · raw_text: "containerization"
- `cpp` · required · raw_text: "solid real-time C++"
- `linux` · nice_to_have · raw_text: "real-time Linux"
- `model-development` · required · raw_text: "trained or deployed learned policies"
- `python` · required · raw_text: "Strong Python"
- `pytorch` · required · raw_text: "comfortable with PyTorch"
- `reinforcement-learning` · required · raw_text: "learned policies (imitation learning, RL or VLA)"
- `ros` · nice_to_have · raw_text: "ROS 2"
- `software-architecture` · required · raw_text: "designed robot software systems end to end"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The only one-of set in the posting is the learned-policy examples (imitation learning, RL or VLA), but only reinforcement-learning is among the labeled skills, so the group would have fewer than two members; the other skills (python, cpp, pytorch, ros, linux) are asked together or on their own, not as alternatives.

DECISION: []

## 174. golden_099 - groups `alternative_group` (groups)

> AI Compiler and Performance Engineer

- `ai-deployment` · required · raw_text: "ML model deployment challenges"
- `cpp` · required · raw_text: "C++"
- `deep-learning` · required · raw_text: "algorithmic optimization for deep learning"
- `jax` · required · raw_text: "JAX"
- `llms` · required · raw_text: "LLM architectures"
- `machine-learning` · required · raw_text: "Deep expertise on ML frameworks"
- `python` · required · raw_text: "one or more programming languages such as Python"
- `pytorch` · required · raw_text: "e.g., PyTorch"
- `software-engineering` · required · raw_text: "software engineering best practices"
- `tensorflow` · required · raw_text: "TensorFlow"
- `testing` · required · raw_text: "testing"
- `transformers` · required · raw_text: "transformer internals"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["python", "cpp"], ["pytorch", "tensorflow", "jax"]] - Under the alternative_group rule, "one or more programming languages such as Python and C++" and "Deep expertise on ML frameworks (e.g., PyTorch, TensorFlow, JAX)" each offer examples for a single ask, so each set is one group, while "machine-learning" stays out as the broad parent. The "one or more of the following" list is left ungrouped because llms and transformers share one bullet joined by "and", so grouping llms with deep-learning would wrongly imply llms alone suffices.

DECISION: [["cpp", "python"], ["jax", "pytorch", "tensorflow"]]

## 175. golden_100 - groups `alternative_group` (groups)

> Research Engineer, Robotics: Physics Simulation and Sim-to-Real

- `cpp` · required · raw_text: "C++"
- `cuda` · nice_to_have · raw_text: "CUDA"
- `jax` · nice_to_have · raw_text: "JAX"
- `python` · required · raw_text: "Proficiency in Python"
- `reinforcement-learning` · nice_to_have · raw_text: "scaling simulation for reinforcement or imitation learning"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["cuda", "jax"]] - The preferred qualification 'GPU programming for physics (CUDA, NVIDIA Warp or JAX)' offers its examples as one ask, so under the rule's example-list marker cuda and jax form a group. Python and C++ are asked together as required skills, so they are not alternatives, and reinforcement-learning is the only skill from its phrase, so it cannot form a group.

DECISION: [["cuda", "jax"]]

## 176. golden_101 - groups `alternative_group` (groups)

> Hardware Design Engineer, AI Inference Engine

- `ai-ml` · required · raw_text: "modern AI/ML models"
- `cloud` · nice_to_have · raw_text: "Understanding of cloud computing environments"
- `distributed-systems` · required · raw_text: "distributed computing"
- `llms` · required · raw_text: "particularly LLMs"
- `machine-learning` · required · raw_text: "ML optimization techniques"
- `networking` · nice_to_have · raw_text: "High-speed inter-chip networking experience"
- `quantization` · required · raw_text: "quantization"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The only example-list ask ('ML optimization techniques (e.g., sparsity, quantization, pruning)') yields just one labeled skill, `quantization`, and a group needs at least two skills from this item, so no group forms.

DECISION: []

## 177. golden_102 - groups `alternative_group` (groups)

> Senior Data Scientist, Growth Marketing

- `a-b-testing` · required · raw_text: "A/B testing"
- `airflow` · nice_to_have · raw_text: "Airflow"
- `aws-s3` · nice_to_have · raw_text: "AWS S3"
- `causal-inference` · required · raw_text: "causal inference techniques"
- `cloud` · nice_to_have · raw_text: "Experience with cloud platforms"
- `data-science` · nice_to_have · raw_text: "data science procedures"
- `dbt` · nice_to_have · raw_text: "dbt"
- `machine-learning` · nice_to_have · raw_text: "machine learning frameworks"
- `python` · required · raw_text: "Advanced proficiency in Python"
- `pytorch` · nice_to_have · raw_text: "PyTorch"
- `sagemaker` · nice_to_have · raw_text: "SageMaker"
- `scikit-learn` · nice_to_have · raw_text: "scikit-learn"
- `snowflake` · nice_to_have · raw_text: "Snowflake"
- `sql` · required · raw_text: "SQL for complex data manipulation"
- `statistics` · required · raw_text: "statistical modeling"
- `tableau` · nice_to_have · raw_text: "Tableau"
- `tensorflow` · nice_to_have · raw_text: "TensorFlow"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["scikit-learn", "tensorflow", "pytorch"]] - The posting offers scikit-learn, TensorFlow, or PyTorch as examples of one ask ("machine learning frameworks such as ... or ..."), which is the rule's "X, Y or Z" alternative marker, while the 'and'-joined lists (AWS S3, SageMaker, Airflow; Snowflake, dbt, Looker, Tableau) are skills asked together and so not grouped.

DECISION: [["pytorch", "scikit-learn", "tensorflow"]]

## 178. golden_103 - groups `alternative_group` (groups)

> Senior Research Engineer, Olmo + Molmo

- `agent-state-management` · required · raw_text: "memory, and long-running workflows"
- `agents` · required · raw_text: "Agentic systems knowledge"
- `ai-deployment` · required · raw_text: "inference, and deployment"
- `ai-infrastructure` · required · raw_text: "4+ years of ML infrastructure experience"
- `aws` · required · raw_text: "AWS"
- `cloud` · required · raw_text: "Familiarity with cloud"
- `containerization` · required · raw_text: "containerization"
- `deep-learning` · required · raw_text: "extensive experience with deep learning"
- `docker` · required · raw_text: "Docker"
- `evaluation` · required · raw_text: "model training, evaluation"
- `fine-tuning` · required · raw_text: "fine-tuning"
- `gcp` · required · raw_text: "GCP"
- `jax` · required · raw_text: "JAX"
- `llms` · required · raw_text: "LLMs (MoEs, long-context models)"
- `model-development` · required · raw_text: "end-to-end model development"
- `observability` · required · raw_text: "profiling, and monitoring"
- `python` · required · raw_text: "Proficiency in Python"
- `pytorch` · required · raw_text: "PyTorch"
- `software-engineering` · required · raw_text: "Strong software engineering fundamentals"
- `tensorflow` · required · raw_text: "or TensorFlow"
- `tool-calling` · required · raw_text: "Agentic systems knowledge — tools"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "jax", "tensorflow"], ["gcp", "aws"]] - The 'major ML framework (PyTorch, JAX, or TensorFlow)' ask is met by any one of the three, so they form group 1; under the 'examples offered for a single ask' marker, GCP and AWS are alternative examples of the cloud part of the ask, while Docker is the containerization example and cannot stand in for cloud, so it stays out and 'cloud' stays out as the broad parent.

DECISION: [["aws", "gcp"], ["jax", "pytorch", "tensorflow"]]

## 179. golden_104 - groups `alternative_group` (groups)

> Senior Machine Learning Engineer

- `ai-deployment` · required · raw_text: "deploying AI/ML models to production"
- `ai-ml` · required · raw_text: "deploying AI/ML models to production"
- `cloud` · required · raw_text: "cloud architecture"
- `cpp` · required · raw_text: "C++"
- `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving machine learning"
- `evaluation` · nice_to_have · raw_text: "model evaluation"
- `fine-tuning` · nice_to_have · raw_text: "fine-tuning and optimizing large-scale models"
- `infrastructure-as-code` · required · raw_text: "infrastructure as code"
- `knowledge-distillation` · nice_to_have · raw_text: "distillation/teacher-student approaches"
- `linux` · required · raw_text: "Linux environments and systems"
- `llmops` · nice_to_have · raw_text: "Experience with LLMOps"
- `machine-learning` · required · raw_text: "experience using ML frameworks"
- `observability` · nice_to_have · raw_text: "monitoring"
- `python` · required · raw_text: "Python"
- `pytorch` · required · raw_text: "PyTorch"
- `quantization` · nice_to_have · raw_text: "quantization"
- `software-architecture` · required · raw_text: "software architecture and design skills"
- `software-engineering` · required · raw_text: "software engineering experience"
- `tensorflow` · required · raw_text: "TensorFlow"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "tensorflow"]] - The posting's 'experience using ML frameworks such as PyTorch or TensorFlow' offers one of two examples for a single ask, so under the alternative_group markers the two skills form one group, while the broad 'machine-learning' skill stays out as a broad parent of its examples.

DECISION: [["pytorch", "tensorflow"]]

## 180. golden_105 - groups `alternative_group` (groups)

> Senior Software Engineer, Axon AI

- `ai-developer-tooling` · required · raw_text: "consistent use of AI across the SDLC"
- `ai-ml` · nice_to_have · raw_text: "AI/LLM capabilities"
- `cloud` · required · raw_text: "operating cloud-native systems that scale"
- `llms` · nice_to_have · raw_text: "AI/LLM capabilities"
- `observability` · required · raw_text: "observability best practices"
- `software-architecture` · nice_to_have · raw_text: "architectural direction"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - No skills are offered in place of each other: "AI/LLM capabilities" names a broad skill (ai-ml) alongside its example (llms), which the rule excludes as a broad skill named with its examples, and the other labeled skills each come from a single ask with no alternative markers.

DECISION: []

## 181. golden_106 - groups `alternative_group` (groups)

> AI Software Engineer

- `ai-deployment` · required · raw_text: "model deployment internals"
- `ai-infrastructure` · required · raw_text: "ML infrastructure"
- `containerization` · nice_to_have · raw_text: "containerized deployments"
- `cpp` · required · raw_text: "Proficient in C++"
- `cuda` · required · raw_text: "CUDA"
- `deepspeed` · required · raw_text: "DeepSpeed-Inference"
- `distributed-systems` · nice_to_have · raw_text: "Exposure to distributed systems"
- `docker` · nice_to_have · raw_text: "Docker/Kubernetes"
- `kubernetes` · nice_to_have · raw_text: "Docker/Kubernetes"
- `model-serving` · required · raw_text: "LLM serving frameworks"
- `python` · required · raw_text: "C++ and Python"
- `sglang` · required · raw_text: "SGLang, TensorRT-LLM"
- `tensorrt` · required · raw_text: "TensorRT-LLM, DeepSpeed-Inference"
- `vllm` · required · raw_text: "vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The 'one or more of' list in the required qualifications would group vllm, sglang, tensorrt and deepspeed, but the role summary asks for vllm, SGLang and TensorRT-LLM together as frameworks the engineer hacks, an unmarked tech-stack entry, so those three leave the group and only deepspeed remains, below the two-skill minimum.

DECISION: ?

## 182. golden_107 - groups `alternative_group` (groups)

> Machine Learning Research Scientist

- `aws` · nice_to_have · raw_text: "AWS"
- `azure` · nice_to_have · raw_text: "Azure"
- `cloud` · nice_to_have · raw_text: "cloud platforms"
- `containerization` · nice_to_have · raw_text: "containerization and orchestration technologies"
- `cpp` · required · raw_text: "C++"
- `docker` · nice_to_have · raw_text: "Docker"
- `gcp` · nice_to_have · raw_text: "GCP"
- `jax` · required · raw_text: "JAX"
- `kubernetes` · nice_to_have · raw_text: "Kubernetes"
- `llms` · required · raw_text: "generative models such as LLMs"
- `machine-learning` · required · raw_text: "Machine Learning research initiatives"
- `python` · required · raw_text: "Python"
- `pytorch` · required · raw_text: "PyTorch"
- `tensorflow` · required · raw_text: "TensorFlow"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "tensorflow", "jax"], ["python", "cpp"], ["aws", "gcp", "azure"]] - The rule's markers 'at least one of' and 'such as X, Y or Z' cover the ML frameworks, the languages, and the cloud platforms (with 'cloud' excluded as the broad parent), while docker and kubernetes stay ungrouped because the 'containerization and orchestration technologies' ask needs both categories, so one example does not meet it.

DECISION: [["aws", "azure", "gcp"], ["cpp", "python"], ["jax", "pytorch", "tensorflow"]]

## 183. golden_108 - groups `alternative_group` (groups)

> Research Engineer, Climate Modeling

- `ai-deployment` · required · raw_text: "deploying a relevant ML application"
- `cloud` · required · raw_text: "ML training code for use in a cloud computing environment"
- `jax` · nice_to_have · raw_text: "experience writing machine learning code in JAX"
- `machine-learning` · required · raw_text: "building and deploying a relevant ML application"
- `model-development` · required · raw_text: "developing ML training code"
- `python` · required · raw_text: "fluent in Python"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - No part of the posting offers one skill in place of another: its requirements are skills asked for together ("fluent in Python", "experience building and deploying", "cloud computing environment"), and the JAX mention is a standalone bonus, so no alternative_group marker applies.

DECISION: []

## 184. golden_095 - skill `agent-harnesses` (disagreement)

> ...Machine Learning, or related technical field - Experience building customized agent harnesses, fine-tuning models, or implementing RLHF/RLAIF...

- A: (did not label this)
- B: `agent-harnesses` · nice_to_have · raw_text: "building customized agent harnesses"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the nice-to-have qualification bullet names agent harnesses ('Experience building customized agent harnesses'), and the raw_text quotes that wording exactly, so labeler B's nice_to_have label stands.

DECISION: B
