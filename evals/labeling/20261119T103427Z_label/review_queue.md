# Review queue - 20261119T103427Z_label

155 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261119T103427Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 177 accepted labels,
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

> Sr. Staff Engineer, AI Datacenter Thermal Management & Control Plane

- tenstorrent · Sr. Staff Engineer, AI Datacenter Thermal Management & Control Plane
- Austin · en · greenhouse · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_095 - scope `in_scope` (in-scope)

> AI/ML Physical Design Flow Engineer

- tenstorrent · AI/ML Physical Design Flow Engineer
- Austin · en · greenhouse · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_096 - scope `in_scope` (in-scope)

> Staff R&D AI Engineer

- webai · Staff R&D AI Engineer
- Austin · en · ashby · 21 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_097 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer, Agentic Systems (Active Secret Clearance)

- striveworks · Senior Machine Learning Engineer, Agentic Systems (Active Secret Clearance)
- Austin · en · greenhouse · 31 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_098 - scope `in_scope` (in-scope)

> Data Scientist (Active Secret Clearance)

- striveworks · Data Scientist (Active Secret Clearance)
- Austin · en · greenhouse · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_099 - scope `in_scope` (in-scope)

> Machine Learning Engineer

- avride · Machine Learning Engineer
- Austin · en · greenhouse · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_100 - scope `in_scope` (in-scope)

> AI Accelerator Architect

- tenstorrent · AI Accelerator Architect
- Austin · en · greenhouse · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_101 - scope `in_scope` (in-scope)

> Staff Machine Learning Engineer

- webai · Staff Machine Learning Engineer
- Austin · en · ashby · 9 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_102 - scope `in_scope` (in-scope)

> Lead Data Scientist – Autonomous Driving

- avride · Lead Data Scientist – Autonomous Driving
- Austin · en · greenhouse · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_103 - scope `in_scope` (in-scope)

> Junior Machine Learning Engineer

- striveworks · Junior Machine Learning Engineer
- Austin · en · greenhouse · 16 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_104 - scope `in_scope` (in-scope)

> AI Research Scientist

- webai · AI Research Scientist
- Austin · en · ashby · 12 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_105 - scope `in_scope` (in-scope)

> Physical Design Methodology Engineer, AI HW IP

- tenstorrent · Physical Design Methodology Engineer, AI HW IP
- Austin · en · greenhouse · 1 skill labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_106 - scope `in_scope` (in-scope)

> Staff Design Verification Engineer, AI HW

- tenstorrent · Staff Design Verification Engineer, AI HW
- Austin · en · greenhouse · 3 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_107 - scope `in_scope` (in-scope)

> Software Engineer – ML Platform

- avride · Software Engineer – ML Platform
- Austin · en · greenhouse · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_108 - scope `in_scope` (in-scope)

> Special Notice:

- webai · Senior Forward Deployed AI Engineer
- Austin · en · ashby · 10 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_094 - skill `distributed-systems` (disagreement)

> ...experience. - You have architected and delivered complex distributed control systems, industrial automation, datacenter infrastructure, or...

- A: (did not label this)
- B: `distributed-systems` · required · raw_text: "distributed control systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_094 - skill `networking` (disagreement)

> ...protocols such as Modbus, BACnet, OPC UA, MQTT, and Ethernet-based control networks, along with telemetry, real-time monitoring, and fault...

- A: (did not label this)
- B: `networking` · required · raw_text: "Ethernet-based control networks"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Who You Are' bullet says the candidate is experienced with 'Ethernet-based control networks', which names a networking skill as a qualification, and under rule 3 that required mention wins over A's omission.

DECISION: B

## 18. golden_094 - skill `software-architecture` (disagreement)

> ...and fault detection. - You can set technical direction, make architecture decisions, and lead complex cross-functional engineering programs...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "make architecture decisions"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_095 - attribute `seniority` (disagreement)

> ...or Computer Engineering (or equivalent experience) with 5+ years in Physical Design CAD methodology at advanced nodes. - Proven track record improving PPA and/or runtime on...

- A: value="senior" · basis="inferred" · signal="5+ years in Physical Design CAD methodology at advanced nodes"
- B: value=null · basis=null · signal=null

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the "5+ years" is a years-of-experience requirement, which does not count as a qualification signal, and the posting explicitly says it welcomes various experience levels and that offers may differ from the level posted, so no seniority is supported.

DECISION: ?

## 20. golden_095 - skill `machine-learning` (disagreement)

> ...flows. - Strong Python/Tcl and data skills, with interest or experience in ML frameworks (PyTorch, TensorFlow), and the ability to drive complex...

- A: (did not label this)
- B: `machine-learning` · nice_to_have · raw_text: "interest or experience in ML frameworks"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Who you are' qualification bullet names ML frameworks (PyTorch, TensorFlow) as a candidate attribute, and the 'What we need' ML mentions are role responsibilities that rule 4 excludes, so B's nice_to_have machine-learning tag with that raw_text is right.

DECISION: B

## 21. golden_096 - skill `ml-engineering` (disagreement)

> ...& Skills: - 7+ years of experience in AI/ML engineering with 4+ years focusing on deep learning and neural network...

- A: (did not label this)
- B: `ml-engineering` · required · raw_text: "AI/ML engineering"

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only quoted mention, "7+ years of experience in AI/ML engineering", is a years-of-experience line, which does not name a skill, and the visible qualifications don't otherwise name ML engineering as a skill.

DECISION: drop

## 22. golden_097 - skill `ai-ml` (disagreement)

> ...and optimizing LLM-powered agents and agentic workflows - Experience integrating AI systems with external tools, APIs, MCP servers, and enterprise...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Experience integrating AI systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Rule 1 applies: the required qualification bullets name AI/ML work (LLM-powered agents, machine learning, TensorFlow/PyTorch), and B's quoted raw_text "Experience integrating AI systems" appears verbatim as a required bullet, so the ai-ml skill belongs in the key.

DECISION: B

## 23. golden_097 - skill `software-architecture` (disagreement)

> ...science, or a related discipline - Knowledge of relevant architectures and design patterns for client-server systems (e.g., asynchronous programming, REST, GraphQL, React,...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the nice-to-have bullet names "architectures and design patterns for client-server systems" as a qualification, which supports software-architecture; the nice_to_have requirement and the verbatim raw_text are correct, so labeler B's version stands.

DECISION: B

## 24. golden_098 - skill `software-engineering` (disagreement)

> ...knowledge of TensorFlow, PyTorch, and/or scikit-learn - Exposure to software development life cycle and tools - Active Secret (or above) US security clearance and US...

- A: `software-engineering` · required · raw_text: "Exposure to software development life cycle and tools"
- B: `software-engineering` · nice_to_have · raw_text: "Experience developing software"

Options: `A` / `B` / `both` / `drop`

PROPOSED: A - Under rule 3, the required mention wins: the required qualification bullet "Exposure to software development life cycle and tools" names software-engineering practice, which outweighs the nice-to-have "Experience developing software" that labeler B cited.

DECISION: A

## 25. golden_099 - skill `ai-deployment` (disagreement)

> ...of the real difficulty lives. What we're looking for - You've shipped a neural network, not just trained one. At least three years taking models from data collection...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "You've shipped a neural network, not just trained one."

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the quoted sentence sits in the "What we're looking for" qualifications and names deploying a model to production or hardware, which is the ai-deployment skill, and rule 3 makes the required mention stand.

DECISION: B

## 26. golden_099 - skill `model-development` (disagreement)

> ...neural network, not just trained one. At least three years taking models from data collection through training to something that ran in production or on real hardware,...

- A: (did not label this)
- B: `model-development` · required · raw_text: "taking models from data collection through training"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualification sentence "At least three years taking models from data collection through training to something that ran in production" names model development as a requirement, and rule 3 makes that required mention decisive, so B's required tag and quoted raw_text are right.

DECISION: B

## 27. golden_100 - attribute `degree` (disagreement)

> ...models for architecture exploration. What You Bring - A Bachelor’s degree in EE/ECE/CE/CS or a related field (MS or PhD preferred). - Strong foundational experience in RTL design with a...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="A Bachelor’s degree in EE/ECE/CE/CS or a related field (MS or PhD preferred)"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="A Bachelor’s degree in EE/ECE/CE/CS or a related field (MS or PhD preferred)."

Options: `A` / `B` / `both` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "A Bachelor’s degree in EE/ECE/CE/CS or a related field"} - Under the degree rule the label is the lowest level named, so the Bachelor's is recorded and the welcomed MS/PhD is not, and the bare mention in the 'What You Bring' requirements list is required.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "A Bachelor’s degree in EE/ECE/CE/CS or a related field"}

## 28. golden_100 - attribute `seniority` (disagreement)

> AI Accelerator Architect Tenstorrent is leading the industry on cutting-edge AI...

- A: value="senior" · basis="stated" · signal="AI Accelerator Architect"
- B: value=null · basis=null · signal=null

Options: `A` / `B` / `both` / `drop`

PROPOSED: drop - Under rule 1, the only signal is the job title "AI Accelerator Architect", which does not count, and the excerpt has no stated seniority word, so the attribute should be null.

DECISION: drop

## 29. golden_101 - attribute `degree` (disagreement)

> ...and best practices. Qualifications: - Advanced degree (Ph.D. preferred) in Computer Science, or a related field. - Proven track record of building and innovations...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="Advanced degree (Ph.D. preferred) in Computer Science, or a related field"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Advanced degree (Ph.D. preferred) in Computer Science, or a related field."

Options: `A` / `B` / `both` / `drop`

PROPOSED: {"degree": "master", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Advanced degree (Ph.D. preferred) in Computer Science, or a related field"} - Under the degree rule the label is the lowest level named, and the posting requires an advanced degree (master-level) while only welcoming a Ph.D., which per the 2026-11-19 decision is not recorded, so neither labeler's phd is correct.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Advanced degree (Ph.D. preferred) in Computer Science, or a related field"}

## 30. golden_101 - skill `ai-deployment` (disagreement)

> ...will have a proven track record of developing and deploying advanced AI models. You will lead core product initiatives across on-device...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying advanced AI models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the sentence "The ideal candidate will have a proven track record of developing and deploying advanced AI models" is a qualification that names deployment, and the required framing and verbatim raw_text support B's tag under rule 3.

DECISION: B

## 31. golden_101 - skill `model-development` (disagreement)

> ...The ideal candidate will have a proven track record of developing and deploying advanced AI models. You will lead core product initiatives across on-device...

- A: (did not label this)
- B: `model-development` · required · raw_text: "developing and deploying advanced AI models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the qualification sentence "The ideal candidate will have a proven track record of developing and deploying advanced AI models" names a skill, and under rule 3 its firm "will have" wording makes it a required mention that outweighs labeler A's omission.

DECISION: B

## 32. golden_103 - skill `model-development` (disagreement)

> ...least one systems programming language - Exposure to the development and use of machine learning models, through either coursework or practical experience -...

- A: (did not label this)
- B: `model-development` · required · raw_text: "development and use of machine learning models"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under Rule 1, the required qualification bullet "Exposure to the development and use of machine learning models" names the skill, and under Rule 3 that required mention wins, so B's required tag with that raw_text is supported.

DECISION: B

## 33. golden_104 - skill `data-privacy-and-security` (disagreement)

> ...learning, or multimodal learning - Familiarity with privacy-preserving ML techniques such as federated learning - Experience contributing to...

- A: (did not label this)
- B: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving ML techniques"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the Preferred Skills bullet "Familiarity with privacy-preserving ML techniques such as federated learning" is a named qualification, so the skill counts, and labeler B's nice_to_have requirement and raw_text match that bullet word for word.

DECISION: B

## 34. golden_105 - attribute `seniority` (disagreement)

> ...run them without you. What We Need - An Engineer with 5+ years developing and supporting physical design methodology or CAD flows in production use. - Expertise with industry-standard...

- A: value="senior" · basis="inferred" · signal="5+ years developing and supporting physical design methodology or CAD flows"
- B: value=null · basis=null · signal=null

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, a years-of-experience line ('5+ years developing and supporting physical design methodology') does not count as qualifying evidence, and the posting has no other explicit seniority wording, so the seniority value should be null.

DECISION: ?

## 35. golden_105 - skill `ai-ml` (disagreement)

> ...manual steps and making PPA exploration repeatable. - Building with AI as part of how you develop flows, and opinionated about where LLMs and ML-driven...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Building with AI as part of how you develop flows"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_105 - skill `workflow-automation` (disagreement)

> ...on daily. - Automation-minded, happiest when you are removing manual steps and making PPA exploration repeatable. - Building with AI as part of how you develop flows, and...

- A: (did not label this)
- B: `workflow-automation` · required · raw_text: "removing manual steps and making PPA exploration repeatable"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Who You Are' bullet describes the candidate as 'automation-minded' and 'removing manual steps,' which is a candidate qualification naming workflow automation, and rule 3 supports keeping the required tag on that quote.

DECISION: ?

## 37. golden_107 - skill `distributed-systems` (disagreement)

> ...training, training data pipelines - Track record of optimizing resource usage and performance in distributed environments #LI-MS1 Candidates are required to be authorized to...

- A: (did not label this)
- B: `distributed-systems` · nice_to_have · raw_text: "optimizing resource usage and performance in distributed environments"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the 'Nice to have' qualification bullet 'Track record of optimizing resource usage and performance in distributed environments' names distributed-systems experience as a requested skill, and the nice_to_have level matches the section heading.

DECISION: B

## 38. golden_107 - skill `software-architecture` (disagreement)

> ...in Python or Go; C++ is a plus - Track record of designing and building scalable, maintainable systems and services - Experience operating production services end-to-end:...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designing and building scalable, maintainable systems and services"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required 'What you will need' bullet asks for 'designing and building scalable, maintainable systems and services', which is a named qualification covering software architecture, and B's raw_text quotes it word for word.

DECISION: ?

## 39. golden_108 - skill `ai-ml` (disagreement)

> ...- Proven track record of deploying and maintaining machine learning/AI systems in production. - Strong expertise in ML frameworks such...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "machine learning/AI systems"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required qualification bullet "Proven track record of deploying and maintaining machine learning/AI systems in production" names the ML/AI skill, and rule 3 makes that required mention decisive, so B's labeling stands.

DECISION: B

## 40. golden_108 - skill `mlops` (disagreement)

> ...clearance - Proven track record of deploying and maintaining machine learning/AI systems in production. - Strong expertise in ML frameworks such as PyTorch,...

- A: (did not label this)
- B: `mlops` · required · raw_text: "maintaining machine learning/AI systems in production"

Options: `A` / `B` / `both` / `drop`

PROPOSED: B - Under rule 1, the required bullet "Proven track record of deploying and maintaining machine learning/AI systems in production" names a qualification skill that is MLOps, and rule 3 makes that required mention count, so B's labeling stands.

DECISION: ?

## 41. golden_094 - skill `observability` (uncertain)

> ...and Ethernet-based control networks, along with telemetry, real-time monitoring, and fault detection. - You can set technical direction,...

- A: `observability` · required · raw_text: "real-time monitoring"
- B: `observability` · required · raw_text: "real-time monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Who You Are' bullet 'You are experienced with ... telemetry, real-time monitoring, and fault detection' is a qualification that names monitoring and telemetry, so observability is a required skill and the agreed raw_text quotes that mention, per rule 3.

DECISION: ok

## 42. golden_096 - skill `ai-deployment` (uncertain)

> ...in PyTorch and/or TensorFlow with experience training and deploying large-scale models - Experience with transformer architectures, attention...

- A: `ai-deployment` · required · raw_text: "deploying large-scale models"
- B: `ai-deployment` · required · raw_text: "deploying large-scale models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1 the qualifications bullet "Proficiency in PyTorch and/or TensorFlow with experience training and deploying large-scale models" is a required skill mention, and the agreed raw_text is quoted verbatim from it, so the label stands (the MLOps "deployment pipelines" bullet also supports it under rule 3).

DECISION: ok

## 43. golden_096 - skill `ai-ml` (uncertain)

> ...& Skills: - 7+ years of experience in AI/ML engineering with 4+ years focusing on deep learning and neural network...

- A: `ai-ml` · required · raw_text: "AI/ML engineering"
- B: `ai-ml` · required · raw_text: "AI/ML engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "Strong expertise in both computer vision and natural language processing with hands-on model development experience"} - Under rule 1 the agreed raw_text "AI/ML engineering" sits in a years-of-experience line that does not count, so I replaced it with a qualifying required sentence that names the skill, keeping the required requirement under rule 3.

DECISION: ?

## 44. golden_096 - skill `knowledge-distillation` (uncertain)

> ...and model optimization techniques (quantization, pruning, distillation) - Experience with embodied AI research or projects...

- A: `knowledge-distillation` · nice_to_have · raw_text: "distillation"
- B: `knowledge-distillation` · nice_to_have · raw_text: "distillation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet "Familiarity with edge AI deployment and model optimization techniques (quantization, pruning, distillation)" names distillation as a skill, so the agreed nice_to_have label and the verbatim raw_text "distillation" (rule 3) are correct.

DECISION: ok

## 45. golden_096 - skill `quantization` (uncertain)

> ...with edge AI deployment and model optimization techniques (quantization, pruning, distillation) - Experience with embodied AI...

- A: `quantization` · nice_to_have · raw_text: "quantization"
- B: `quantization` · nice_to_have · raw_text: "quantization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Qualifications bullet names quantization as a technique ('model optimization techniques (quantization, pruning, distillation)'), so it counts; it is correctly marked nice_to_have and the raw_text appears verbatim.

DECISION: ok

## 46. golden_097 - attribute `degree` (uncertain)

> ...to put them into practice. What we’re looking for - A BS degree in computer science, machine learning, or a related discipline and 6+ years relevant experience - Demonstrated...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the degree rule, the lowest level named is the required BS, so `bachelor` with `required` is correct; the optional advanced degree is not recorded, and "and 6+ years" is a conjunction, not an "or equivalent experience" substitute, so `or_equivalent=false` stands.

DECISION: ok

## 47. golden_097 - skill `async-processing` (uncertain)

> ...and design patterns for client-server systems (e.g., asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience...

- A: `async-processing` · nice_to_have · raw_text: "asynchronous programming"
- B: `async-processing` · nice_to_have · raw_text: "asynchronous programming"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the nice-to-have bullet names "asynchronous programming" as a knowledge area for client-server systems, so the skill is counted, and the section heading correctly sets requirement to nice_to_have.

DECISION: ok

## 48. golden_098 - attribute `degree` (uncertain)

> ...to put them into practice. What we’re looking for - A BS degree in computer science, machine learning, mathematics, or a related discipline and 2+ years of relevant experience - Proficiency in...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, mathematics, or a related discipline"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, mathematics, or a related discipline"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the degree rule, `degree` is the lowest level named, and the required bachelor's ('A BS degree in computer science, machine learning, mathematics, or a related discipline') is the minimum, while the advanced degree is welcomed but not recorded, so `bachelor`, `required`, `or_equivalent=false`, and the quoted signal are all correct as agreed.

DECISION: ok

## 49. golden_098 - attribute `seniority` (uncertain)

> ...machine learning, mathematics, or a related discipline and 2+ years of relevant experience - Proficiency in machine learning and data science, with...

- A: value="junior" · basis="inferred" · signal="2+ years of relevant experience"
- B: value="junior" · basis="inferred" · signal="2+ years of relevant experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only support for seniority is a years-of-experience line ("2+ years of relevant experience"), which does not count, so the attribute should be null rather than "junior".

DECISION: ?

## 50. golden_098 - skill `agents` (uncertain)

> ...demonstrated application to image data, video data, or agentic systems - Proficiency in implementing and analyzing data...

- A: `agents` · required · raw_text: "agentic systems"
- B: `agents` · required · raw_text: "agentic systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required bullet "Proficiency in machine learning and data science, with demonstrated application to image data, video data, or agentic systems" names agentic systems as a required qualification, so the agreed `agents` skill as required with raw_text "agentic systems" stands (rule 3 also supports the required mention).

DECISION: ok

## 51. golden_099 - skill `inference-optimization` (uncertain)

> ...when it's the right call. Things that would stand out - You've made a model meaningfully faster on target hardware and can explain what you gave up to get there. - You've...

- A: `inference-optimization` · nice_to_have · raw_text: "You've made a model meaningfully faster on target hardware"
- B: `inference-optimization` · nice_to_have · raw_text: "You've made a model meaningfully faster on target hardware"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "You've made a model meaningfully faster on target hardware" is a qualification line in the "Things that would stand out" section, so it names the skill and nice_to_have is the right requirement level, with the raw_text quoted verbatim.

DECISION: ok

## 52. golden_099 - skill `machine-learning` (uncertain)

> ...in production or on real hardware, and stayed working. - Real depth in one modern ML area — computer vision, large language models, or generative...

- A: `machine-learning` · required · raw_text: "Real depth in one modern ML area"
- B: `machine-learning` · required · raw_text: "Real depth in one modern ML area"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'What we're looking for' qualification 'Real depth in one modern ML area' is a required bullet that names machine learning, and the agreed required label and raw_text quote support it.

DECISION: ok

## 53. golden_101 - skill `apache-spark` (uncertain)

> ...GCP). - Knowledge of Big Data technologies (Hadoop, Spark). - Familiarity with containerization and orchestration...

- A: `apache-spark` · nice_to_have · raw_text: "Spark"
- B: `apache-spark` · nice_to_have · raw_text: "Spark"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Skills bullet "Knowledge of Big Data technologies (Hadoop, Spark)" is a qualification naming Spark, its nice_to_have status matches the Preferred heading, and the raw_text "Spark" appears verbatim, so the agreed label stands.

DECISION: ok

## 54. golden_101 - skill `aws` (uncertain)

> ...Skills: - Experience with cloud computing services (AWS, Azure, GCP). - Knowledge of Big Data technologies...

- A: `aws` · nice_to_have · raw_text: "AWS"
- B: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the preferred-skills bullet 'Experience with cloud computing services (AWS, Azure, GCP)' names AWS as a qualification, and 'AWS' appears verbatim, so the agreed nice_to_have label is correct.

DECISION: ok

## 55. golden_101 - skill `azure` (uncertain)

> ...- Experience with cloud computing services (AWS, Azure, GCP). - Knowledge of Big Data technologies (Hadoop,...

- A: `azure` · nice_to_have · raw_text: "Azure"
- B: `azure` · nice_to_have · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the Preferred Skills bullet "Experience with cloud computing services (AWS, Azure, GCP)" names Azure as a qualification, so the agreed nice_to_have label with raw_text "Azure" is correct and Rule 5 does not apply because Azure is named explicitly.

DECISION: ok

## 56. golden_101 - skill `gcp` (uncertain)

> ...- Experience with cloud computing services (AWS, Azure, GCP). - Knowledge of Big Data technologies (Hadoop,...

- A: `gcp` · nice_to_have · raw_text: "GCP"
- B: `gcp` · nice_to_have · raw_text: "GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_101 - skill `hadoop` (uncertain)

> ...Azure, GCP). - Knowledge of Big Data technologies (Hadoop, Spark). - Familiarity with containerization and...

- A: `hadoop` · nice_to_have · raw_text: "Hadoop"
- B: `hadoop` · nice_to_have · raw_text: "Hadoop"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the Preferred Skills bullet "Knowledge of Big Data technologies (Hadoop, Spark)" names Hadoop as a qualification, so the agreed nice_to_have label and the raw_text "Hadoop" are correct as they stand.

DECISION: ok

## 58. golden_102 - skill `data-pipelines` (uncertain)

> ...Python and SQL; you can independently run experiments and ship analyses and pipelines end to end. - Leadership: proven technical leadership, mentoring,...

- A: `data-pipelines` · required · raw_text: "ship analyses and pipelines end to end"
- B: `data-pipelines` · required · raw_text: "ship analyses and pipelines end to end"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required 'What you'll need' Coding bullet names building pipelines ('ship analyses and pipelines end to end'), and rule 3 makes that required mention decisive, so the agreed required label and raw_text stand.

DECISION: ok

## 59. golden_103 - attribute `degree` (uncertain)

> ...to put them into practice. What we’re looking for - A BS degree in computer science, machine learning, or a related discipline and 0–2 years of relevant experience - Strong proficiency...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the degree rule the label is the lowest level named, which here is the required BS (bachelor), and the master's is listed as optional, so it is not recorded; the "or a related discipline" wording widens the field, not the requirement, so or_equivalent=false and the agreed signal is accurate.

DECISION: ok

## 60. golden_103 - skill `agents` (uncertain)

> ...on structured and unstructured data - Experience with agentic workflows, LLM evaluation, testing, observability, or guardrails -...

- A: `agents` · nice_to_have · raw_text: "agentic workflows"
- B: `agents` · nice_to_have · raw_text: "agentic workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the bullet "Experience with agentic workflows, LLM evaluation, testing, observability, or guardrails" names the skill, and the section heading marks it as nice_to_have, so the agreed label and the quoted raw_text "agentic workflows" (which appears verbatim) are supported.

DECISION: ok

## 61. golden_103 - skill `async-processing` (uncertain)

> ...Podman, or Kubernetes (K8s) - Experience working with asynchronous programming, concurrency, or event-driven architectures - Active...

- A: `async-processing` · nice_to_have · raw_text: "asynchronous programming"
- B: `async-processing` · nice_to_have · raw_text: "asynchronous programming"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "Experience working with asynchronous programming, concurrency, or event-driven architectures" names the skill, and it sits under the heading saying the section "isn't required," so nice_to_have and the quoted raw_text "asynchronous programming" are correct as agreed.

DECISION: ok

## 62. golden_103 - skill `cloud` (uncertain)

> ...implementing and deploying software in containerized or cloud environments, using tools such as Docker, Podman, or Kubernetes...

- A: `cloud` · nice_to_have · raw_text: "cloud environments"
- B: `cloud` · nice_to_have · raw_text: "cloud environments"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet "Experience implementing and deploying software in containerized or cloud environments" names cloud deployment as a skill, and it sits under the heading saying the section is not required, so nice_to_have and the verbatim raw_text "cloud environments" are right.

DECISION: ok

## 63. golden_103 - skill `containerization` (uncertain)

> ...Experience implementing and deploying software in containerized or cloud environments, using tools such as Docker, Podman,...

- A: `containerization` · nice_to_have · raw_text: "containerized"
- B: `containerization` · nice_to_have · raw_text: "containerized"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the bullet under the 'isn't required, but we'd love to see it' heading names containerized environments and Docker/Kubernetes, so containerization counts as nice_to_have, and the quoted raw_text 'containerized' appears verbatim in the posting.

DECISION: ok

## 64. golden_103 - skill `software-architecture` (uncertain)

> ...modern AI application patterns - Knowledge of relevant architectures and design patterns for client-server systems - Experience implementing and deploying software in...

- A: `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"
- B: `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the nice-to-have bullet 'Knowledge of relevant architectures and design patterns for client-server systems' is a qualification that names software architecture, and the agreed nice_to_have requirement and verbatim raw_text match the posting's 'isn't required' section.

DECISION: ok

## 65. golden_104 - attribute `degree` (uncertain)

> ...Mathematics, or a related field Preferred Skills - Master’s or PhD in Machine Learning, Computer Science, AI, or a related field - Experience...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s or PhD in Machine Learning"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s or PhD in Machine Learning, Computer Science, AI, or a related field"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "Bachelor’s degree in Computer Science, Engineering, Mathematics, or a related field"} - Under the degree rule the label is the lowest level named, and the Qualifications list gives a bare, required Bachelor's degree, while the Master's or PhD appears only under Preferred Skills and so is not recorded.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "Bachelor’s degree in Computer Science, Engineering, Mathematics, or a related field"}

## 66. golden_104 - skill `evaluation` (uncertain)

> ...- Experience building datasets, designing experiments, and validating ML model performance - Deep understanding of optimization techniques...

- A: `evaluation` · required · raw_text: "validating ML model performance"
- B: `evaluation` · required · raw_text: "validating ML model performance"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the required Qualifications bullet "Experience building datasets, designing experiments, and validating ML model performance" names model evaluation, and Rule 3 keeps the required mention quoted as raw_text, so the agreed label stands.

DECISION: ok

## 67. golden_104 - skill `machine-learning` (uncertain)

> ...- 4+ years of experience (can be graduate research) in machine learning research, AI model development, or related fields - Strong...

- A: `machine-learning` · required · raw_text: "machine learning research"
- B: `machine-learning` · required · raw_text: "machine learning research"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: drop - Under rule 1, the only quoted mention of machine learning is inside the years-of-experience line ("4+ years of experience ... in machine learning research"), which does not count; the qualification bullets name deep learning, frameworks, and model training instead.

DECISION: ?

## 68. golden_104 - skill `model-development` (uncertain)

> ...(can be graduate research) in machine learning research, AI model development, or related fields - Strong expertise in deep learning...

- A: `model-development` · required · raw_text: "AI model development"
- B: `model-development` · required · raw_text: "training and fine-tuning large-scale models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: {"requirement": "required", "raw_text": "Hands-on experience training and fine-tuning large-scale models"} - Under rule 1 the labeled quote sits in a years-of-experience line, which does not count, but the separate qualification bullet 'Hands-on experience training and fine-tuning large-scale models' names model work and supports the skill as required, so rule 3 points to that quote.

DECISION: ?

## 69. golden_105 - skill `llms` (uncertain)

> ...Building with AI as part of how you develop flows, and opinionated about where LLMs and ML-driven optimization genuinely help versus where they do not. - An effective partner to...

- A: `llms` · required · raw_text: "opinionated about where LLMs and ML-driven optimization genuinely help"
- B: `llms` · required · raw_text: "LLMs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Who You Are' bullet names LLMs as a candidate trait rather than a responsibility, and under rule 3 the required framing of that profile section, quoted in the raw_text, supports keeping it as required.

DECISION: ok

## 70. golden_105 - skill `machine-learning` (uncertain)

> ...you develop flows, and opinionated about where LLMs and ML-driven optimization genuinely help versus where they do not. - An effective partner to...

- A: `machine-learning` · required · raw_text: "ML-driven optimization genuinely help"
- B: `machine-learning` · required · raw_text: "ML-driven optimization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Who You Are' bullet names ML-driven optimization as a candidate attribute the posting expects, and under rule 3 that mention is the required one quoted in raw_text, so the agreed label stands.

DECISION: ok

## 71. golden_106 - attribute `seniority` (uncertain)

> Staff Design Verification Engineer, AI HW Tenstorrent is leading the industry on cutting-edge AI...

- A: value="senior" · basis="stated" · signal="Staff Design Verification Engineer, AI HW"
- B: value="senior" · basis="stated" · signal="Staff Design Verification Engineer, AI HW"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Rule 1 excludes job titles only as skill evidence, and this is a seniority attribute, where the explicit title term "Staff" is a reasonable stated basis for "senior" and the agreed signal appears verbatim in the posting.

DECISION: ok

## 72. golden_106 - skill `ci-cd` (uncertain)

> ...Python, or Bash scripting for automate builds, parse logs, manage CI pipelines. - Skilled in coverage-driven verification and confident...

- A: `ci-cd` · required · raw_text: "manage CI pipelines"
- B: `ci-cd` · required · raw_text: "manage CI pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the 'Who You Are' bullet 'Proficient in Linux environments with Python, or Bash scripting for automate builds, parse logs, manage CI pipelines' is a qualification that names CI pipeline management, and the quoted raw_text appears verbatim, so the required ci-cd label stands (rules 1 and 3).

DECISION: ok

## 73. golden_107 - skill `networking` (uncertain)

> ...pressure - Solid Linux and systems debugging skills: performance investigation, networking, storage/IO - Ability to troubleshoot complex production...

- A: `networking` · required · raw_text: "performance investigation, networking"
- B: `networking` · required · raw_text: "networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under rule 1, the required 'What you will need' bullet names networking as part of the Linux and systems debugging skills, and rule 3 confirms the required quote 'performance investigation, networking' is the determining mention.

DECISION: ok

## 74. golden_108 - skill `ai-deployment` (uncertain)

> ...- Active US Security clearance - Proven track record of deploying and maintaining machine learning/AI systems in production. - Strong expertise in ML frameworks such as PyTorch,...

- A: `ai-deployment` · required · raw_text: "deploying and maintaining machine learning/AI systems in production"
- B: `ai-deployment` · required · raw_text: "deploying and maintaining machine learning/AI systems in production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under the "Required Skills & Qualifications" heading, the bullet "Proven track record of deploying and maintaining machine learning/AI systems in production" names the skill as a requirement, so under rules 1 and 3 the agreed required label stands.

DECISION: ok

## 75. golden_108 - skill `data-privacy-and-security` (uncertain)

> ...in developing full stack applications - Knowledge of privacy-preserving AI and secure compute environments. - Master’s degree in a relevant technical...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving AI and secure compute environments"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving AI and secure compute environments"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

PROPOSED: ok - Under Rule 1, the Preferred Qualifications bullet "Knowledge of privacy-preserving AI and secure compute environments" names a qualifying skill in data privacy and security, and the nice_to_have requirement and quoted raw_text match the posting verbatim.

DECISION: ok

## 76. golden_094 - attribute `degree` (spot-check)

> ...differ from the one in this posting. Who You Are - You have a BS, MS, or PhD in Electrical, Mechanical, Computer, or Controls Engineering, or a related technical discipline, and 12+ years of relevant engineering experience. - You...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="You have a BS, MS, or PhD in Electrical, Mechanical, Computer, or Controls Engineering, or a related technical discipline"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "bachelor", "degree_requirement": "required", "degree_or_equivalent": false, "degree_signal": "You have a BS, MS, or PhD in Electrical, Mechanical, Computer, or Controls Engineering, or a related technical discipline"} - Under the degree rule, the label is the lowest level named, and the posting names BS, MS, and PhD, so the level is bachelor; the bare mention in the requirements list stays required, and 'or a related technical discipline' widens the field, not the requirement, so or_equivalent is false.

DECISION: {"degree": "bachelor", "degree_or_equivalent": false, "degree_requirement": "required", "degree_signal": "You have a BS, MS, or PhD in Electrical, Mechanical, Computer, or Controls Engineering, or a related technical discipline"}

## 77. golden_095 - attribute `degree` (spot-check)

> ...differ from the one in this posting. Who you are - BS in Electrical or Computer Engineering (or equivalent experience) with 5+ years in Physical Design CAD methodology at...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="BS in Electrical or Computer Engineering (or equivalent experience)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The only level named is 'BS in Electrical or Computer Engineering', so the lowest-level rule gives bachelor. It sits as a bare mention in the requirements list, so it is required, and 'or equivalent experience' sets degree_or_equivalent to true, with the signal quoted verbatim.

DECISION: ok

## 78. golden_096 - attribute `seniority` (spot-check)

> Staff R&D AI Engineer About Us: We are establishing the first distributed Al...

- agreed label: value="senior" · basis="stated" · signal="Staff R&D AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 79. golden_096 - skill `aws` (spot-check)

> ...on AI solutions - Experience with cloud platforms (AWS, GCP, Azure) and containerization technologies -...

- agreed label: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 80. golden_096 - skill `cloud` (spot-check)

> ...prototype and iterate on AI solutions - Experience with cloud platforms (AWS, GCP, Azure) and containerization technologies -...

- agreed label: `cloud` · nice_to_have · raw_text: "cloud platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 81. golden_096 - skill `containerization` (spot-check)

> ...- Experience with cloud platforms (AWS, GCP, Azure) and containerization technologies - Background in safety-critical AI systems or AI...

- agreed label: `containerization` · nice_to_have · raw_text: "containerization technologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 82. golden_096 - skill `deep-learning` (spot-check)

> ...experience in AI/ML engineering with 4+ years focusing on deep learning and neural network development - Strong understanding of...

- agreed label: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_096 - skill `distributed-training` (spot-check)

> ...tracking - Strong programming skills in Python with experience in distributed training and model optimization - Understanding of sequential...

- agreed label: `distributed-training` · required · raw_text: "experience in distributed training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_096 - skill `model-development` (spot-check)

> ...both computer vision and natural language processing with hands-on model development experience - Proficiency in PyTorch and/or TensorFlow with...

- agreed label: `model-development` · required · raw_text: "hands-on model development experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_096 - skill `model-versioning` (spot-check)

> ...fundamentals - Experience with MLOps practices including model versioning, monitoring, and deployment pipelines - Proven ability...

- agreed label: `model-versioning` · required · raw_text: "model versioning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 86. golden_096 - skill `nlp` (spot-check)

> ...etc.) - Strong expertise in both computer vision and natural language processing with hands-on model development experience - Proficiency...

- agreed label: `nlp` · required · raw_text: "natural language processing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_096 - skill `observability` (spot-check)

> ...with MLOps practices including model versioning, monitoring, and deployment pipelines - Proven ability to work...

- agreed label: `observability` · required · raw_text: "monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_096 - skill `tensorflow` (spot-check)

> ...development experience - Proficiency in PyTorch and/or TensorFlow with experience training and deploying large-scale...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_097 - skill `angular` (spot-check)

> ...asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience implementing and deploying software into...

- agreed label: `angular` · nice_to_have · raw_text: "Angular"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_097 - skill `apis` (spot-check)

> ...Experience integrating AI systems with external tools, APIs, MCP servers, and enterprise data sources - Experience...

- agreed label: `apis` · required · raw_text: "APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_097 - skill `ci-cd` (spot-check)

> ...and processes (Agile, version control, issue tracking, CI/CD, debugging, etc.) - Active Secret (or above) US security...

- agreed label: `ci-cd` · required · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_097 - skill `cloud` (spot-check)

> ...implementing and deploying software into containerized or cloud environments (e.g., Docker, Kubernetes [K8s], infrastructure as code,...

- agreed label: `cloud` · nice_to_have · raw_text: "cloud environments"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_097 - skill `cpp` (spot-check)

> ...at least one systems programming language (e.g., Go, Rust, C++, Java, Scala) - Proficiency with modern software...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_097 - skill `docker` (spot-check)

> ...software into containerized or cloud environments (e.g., Docker, Kubernetes [K8s], infrastructure as code, major cloud...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_097 - skill `java` (spot-check)

> ...one systems programming language (e.g., Go, Rust, C++, Java, Scala) - Proficiency with modern software engineering...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_097 - skill `mcp` (spot-check)

> ...integrating AI systems with external tools, APIs, MCP servers, and enterprise data sources - Experience developing...

- agreed label: `mcp` · required · raw_text: "MCP servers"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_097 - skill `pytorch` (spot-check)

> ...essential, as is knowledge of libraries like TensorFlow, PyTorch, and/or scikit-learn - Strong software engineering...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_097 - skill `rag` (spot-check)

> ...performance, reliability, and safety - Familiarity with retrieval-augmented generation (RAG), tool use, planning, and multi-agent architectures -...

- agreed label: `rag` · required · raw_text: "retrieval-augmented generation (RAG)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_097 - skill `react` (spot-check)

> ...systems (e.g., asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience implementing and deploying...

- agreed label: `react` · nice_to_have · raw_text: "React"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_097 - skill `tensorflow` (spot-check)

> ...in Python is essential, as is knowledge of libraries like TensorFlow, PyTorch, and/or scikit-learn - Strong software...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_097 - skill `vue` (spot-check)

> ...(e.g., asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience implementing and deploying...

- agreed label: `vue` · nice_to_have · raw_text: "Vue"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_098 - attribute `german` (spot-check)

> Data Scientist (Active Secret Clearance)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 103. golden_098 - skill `ai-deployment` (spot-check)

> ...machine learning, mathematics, or a related discipline - Experience deploying machine learning and data science solutions to production environments - Exposure to DevOps and to cloud infrastructure -...

- agreed label: `ai-deployment` · nice_to_have · raw_text: "Experience deploying machine learning and data science solutions to production environments"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_098 - skill `data-pipelines` (spot-check)

> ...telemetry, graphs, or other) - Experience implementing ETL pipelines, data pipelines, and/or workflow automation - Experience developing...

- agreed label: `data-pipelines` · nice_to_have · raw_text: "ETL pipelines, data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 105. golden_098 - skill `data-science` (spot-check)

> ...related discipline and 2+ years of relevant experience - Proficiency in machine learning and data science, with demonstrated application to image data, video data,...

- agreed label: `data-science` · required · raw_text: "Proficiency in machine learning and data science"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_098 - skill `go` (spot-check)

> ...— Dr. Jim Rebesco, Cofounder and CEO, Striveworks The government’s demand for AI is growing far faster than the...

- agreed label: `go` · nice_to_have · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_098 - skill `python` (spot-check)

> ...and analyzing data structures and algorithms - Excellence in Python and knowledge of TensorFlow, PyTorch, and/or...

- agreed label: `python` · required · raw_text: "Excellence in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_098 - skill `rust` (spot-check)

> ...degrade in the real world. And when performance drops, trust goes with it. Striveworks was built to solve that...

- agreed label: `rust` · nice_to_have · raw_text: "Rust"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_098 - skill `scikit-learn` (spot-check)

> ...Excellence in Python and knowledge of TensorFlow, PyTorch, and/or scikit-learn - Exposure to software development life cycle and...

- agreed label: `scikit-learn` · required · raw_text: "and/or scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_098 - skill `tensorflow` (spot-check)

> ...and algorithms - Excellence in Python and knowledge of TensorFlow, PyTorch, and/or scikit-learn - Exposure to software...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_099 - attribute `german` (spot-check)

> Machine Learning Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_099 - attribute `seniority` (spot-check)

> ...You've shipped a neural network, not just trained one. At least three years taking models from data collection through training to...

- agreed label: value="mid" · basis="inferred" · signal="At least three years"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_099 - skill `computer-vision` (spot-check)

> ...and stayed working. - Real depth in one modern ML area — computer vision, large language models, or generative modelling. We'd...

- agreed label: `computer-vision` · required · raw_text: "computer vision"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_099 - skill `sql` (spot-check)

> ...who own it. - Comfort with large-scale data tooling and SQL — you can get your own data without waiting on someone...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_100 - attribute `german` (spot-check)

> AI Accelerator Architect

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 116. golden_101 - skill `kubernetes` (spot-check)

> ...containerization and orchestration technologies (Docker, Kubernetes). - Publications or presentations in recognized Machine...

- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_101 - skill `pytorch` (spot-check)

> ...and machine learning frameworks like TensorFlow and/or PyTorch. - Demonstrated ability to lead complex projects and...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_101 - skill `tensorflow` (spot-check)

> ...skills in Python and machine learning frameworks like TensorFlow and/or PyTorch. - Demonstrated ability to lead complex...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_102 - attribute `degree` (spot-check)

> ...to have - Formal training in statistics (for example, MS or PhD in Statistics, Applied Statistics, Biostatistics, Econometrics, or a quantitative field with rigorous statistical coursework). - Familiarity with...

- agreed label: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="MS or PhD in Statistics, Applied Statistics, Biostatistics, Econometrics, or a quantitative field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: {"degree": "master", "degree_requirement": "nice_to_have", "degree_or_equivalent": false, "degree_signal": "MS or PhD in Statistics, Applied Statistics, Biostatistics, Econometrics, or a quantitative field"} - Under the degree rule, 'MS or PhD' means the lowest named level, master, not phd, and the mention sits under the optional Nice to have section, so it is nice_to_have.

DECISION: {"degree": "master", "degree_or_equivalent": false, "degree_requirement": "nice_to_have", "degree_signal": "MS or PhD in Statistics, Applied Statistics, Biostatistics, Econometrics, or a quantitative field"}

## 120. golden_102 - skill `python` (spot-check)

> ...methods for evaluating change and uncertainty. - Coding: strong Python and SQL; you can independently run experiments and ship...

- agreed label: `python` · required · raw_text: "strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_103 - attribute `seniority` (spot-check)

> Junior Machine Learning Engineer “In 36 months, agentic AI systems will be an operating...

- agreed label: value="junior" · basis="stated" · signal="Junior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_103 - skill `docker` (spot-check)

> ...containerized or cloud environments, using tools such as Docker, Podman, or Kubernetes (K8s) - Experience working with...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_103 - skill `embeddings` (spot-check)

> ...or guardrails - Familiarity with vector databases, embeddings, retrieval-augmented generation (RAG), or other modern AI...

- agreed label: `embeddings` · nice_to_have · raw_text: "embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_103 - skill `python` (spot-check)

> ...related discipline and 0–2 years of relevant experience - Strong proficiency in Python including experience with libraries and frameworks like...

- agreed label: `python` · required · raw_text: "Strong proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_103 - skill `pytorch` (spot-check)

> ...including experience with libraries and frameworks like PyTorch, TensorFlow, and/or scikit-learn - Strong software...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_103 - skill `rag` (spot-check)

> ...Familiarity with vector databases, embeddings, retrieval-augmented generation (RAG), or other modern AI application patterns - Knowledge of...

- agreed label: `rag` · nice_to_have · raw_text: "retrieval-augmented generation (RAG)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_103 - skill `scikit-learn` (spot-check)

> ...libraries and frameworks like PyTorch, TensorFlow, and/or scikit-learn - Strong software engineering fundamentals and experience...

- agreed label: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_103 - skill `software-engineering` (spot-check)

> ...like PyTorch, TensorFlow, and/or scikit-learn - Strong software engineering fundamentals and experience with at least one systems programming...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering fundamentals"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_103 - skill `tensorflow` (spot-check)

> ...experience with libraries and frameworks like PyTorch, TensorFlow, and/or scikit-learn - Strong software engineering...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_103 - skill `testing` (spot-check)

> ...billions of dollars invested. The models perform in testing, but they degrade in the real world. And when performance...

- agreed label: `testing` · nice_to_have · raw_text: "testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_103 - skill `vector-databases` (spot-check)

> ...testing, observability, or guardrails - Familiarity with vector databases, embeddings, retrieval-augmented generation (RAG), or...

- agreed label: `vector-databases` · nice_to_have · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_104 - attribute `seniority` (spot-check)

> ...with webAI’s strategic priorities Qualifications: - 4+ years of experience (can be graduate research) in machine learning research,...

- agreed label: value="mid" · basis="inferred" · signal="4+ years of experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_104 - skill `deep-learning` (spot-check)

> ...development, or related fields - Strong expertise in deep learning architectures including transformers, CNNs, RNNs, and diffusion models...

- agreed label: `deep-learning` · required · raw_text: "deep learning architectures"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_104 - skill `distributed-training` (spot-check)

> ...Learning, Computer Science, AI, or a related field - Experience with distributed training, edge inference, or on-device ML - Research experience...

- agreed label: `distributed-training` · nice_to_have · raw_text: "Experience with distributed training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 135. golden_104 - skill `jax` (spot-check)

> ...Python and ML frameworks such as PyTorch, TensorFlow, or JAX - Experience building datasets, designing experiments,...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_104 - skill `llms` (spot-check)

> ...distributed training, edge inference, or on-device ML - Research experience in generative AI, reinforcement learning, or multimodal learning -...

- agreed label: `llms` · nice_to_have · raw_text: "Research experience in generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 137. golden_104 - skill `python` (spot-check)

> ...experience training and fine-tuning large-scale models - Proficiency in Python and ML frameworks such as PyTorch, TensorFlow, or JAX -...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 138. golden_104 - skill `quantization` (spot-check)

> ...- Deep understanding of optimization techniques including quantization, distillation, pruning, and hardware-aware training - Strong problem-solving...

- agreed label: `quantization` · required · raw_text: "quantization, distillation, pruning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 139. golden_104 - skill `transformers` (spot-check)

> ...Strong expertise in deep learning architectures including transformers, CNNs, RNNs, and diffusion models - Hands-on experience training and...

- agreed label: `transformers` · required · raw_text: "transformers, CNNs, RNNs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 140. golden_105 - attribute `degree` (spot-check)

> Physical Design Methodology Engineer, AI HW IP

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

PROPOSED: ok - The posting names no degree at all ("education" appears only in the generic compensation sentence), and the degree rule says the label is `null` when no degree is mentioned, so the agreed null is correct.

DECISION: ok

## 141. golden_105 - attribute `german` (spot-check)

> Physical Design Methodology Engineer, AI HW IP

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_106 - attribute `german` (spot-check)

> Staff Design Verification Engineer, AI HW

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_106 - skill `bash` (spot-check)

> ...Proficient in Linux environments with Python, or Bash scripting for automate builds, parse logs, manage CI pipelines. -...

- agreed label: `bash` · required · raw_text: "Bash scripting"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 144. golden_106 - skill `python` (spot-check)

> ...specs and waveforms. - Proficient in Linux environments with Python, or Bash scripting for automate builds, parse logs, manage CI pipelines. -...

- agreed label: `python` · required · raw_text: "with Python, or Bash scripting"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_107 - attribute `seniority` (spot-check)

> Software Engineer – ML Platform

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_107 - skill `apis` (spot-check)

> ...Experience operating production services end-to-end: APIs, reliability practices, observability - Deep knowledge of...

- agreed label: `apis` · required · raw_text: "APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 147. golden_107 - skill `cpp` (spot-check)

> ...you will need - Strong proficiency in Python or Go; C++ is a plus - Track record of designing and building scalable,...

- agreed label: `cpp` · nice_to_have · raw_text: "C++ is a plus"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 148. golden_107 - skill `data-pipelines` (spot-check)

> ...ML training systems: GPU scheduling, distributed training, training data pipelines - Track record of optimizing resource usage and...

- agreed label: `data-pipelines` · nice_to_have · raw_text: "training data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_107 - skill `kubernetes` (spot-check)

> ...end-to-end: APIs, reliability practices, observability - Deep knowledge of Kubernetes: how scheduling, resource management, controllers, and pod...

- agreed label: `kubernetes` · required · raw_text: "Deep knowledge of Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 150. golden_107 - skill `ray` (spot-check)

> ...and traces and drive them to resolution Nice to have - Experience with Argo Workflows, Ray, MLflow, or comparable distributed ML tooling - Hands-on...

- agreed label: `ray` · nice_to_have · raw_text: "Experience with Argo Workflows, Ray"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 151. golden_108 - skill `devops` (spot-check)

> ...hardware. - Familiarity with distributed systems, DevOps tooling, and performance tuning. - Prior experience in a...

- agreed label: `devops` · nice_to_have · raw_text: "DevOps tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 152. golden_108 - skill `distributed-systems` (spot-check)

> ...on edge devices or consumer hardware. - Familiarity with distributed systems, DevOps tooling, and performance tuning. - Prior...

- agreed label: `distributed-systems` · nice_to_have · raw_text: "distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_108 - skill `onnx` (spot-check)

> ...expertise in ML frameworks such as PyTorch, TensorFlow, ONNX, JAX, etc. - Experience debugging complex systems...

- agreed label: `onnx` · required · raw_text: "ONNX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 154. golden_108 - skill `pytorch` (spot-check)

> ...production. - Strong expertise in ML frameworks such as PyTorch, TensorFlow, ONNX, JAX, etc. - Experience debugging...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_108 - skill `software-engineering` (spot-check)

> ...Skills & Qualifications: - 5+ years of combined experience in software engineering and machine learning. - Active US Security clearance -...

- agreed label: `software-engineering` · required · raw_text: "experience in software engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_108 - attribute `degree` (rule-change)

> ...privacy-preserving AI and secure compute environments. - Master’s degree in a relevant technical discipline. We at webAI are committed to living out the core values...

- agreed label: value="master" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s degree in a relevant technical discipline."

Options: `ok` (right under today's rule) / `drop` / JSON (what it should be)

PROPOSED: ok - The posting names only one degree level, a Master's degree, so the lowest-named-level rule still yields `master`, and it sits under the 'Preferred Qualifications' heading, which marks it optional, so `nice_to_have` and the quoted signal also stand.

DECISION: ok

## 157. golden_094 - groups `alternative_group` (groups)

> Sr. Staff Engineer, AI Datacenter Thermal Management & Control Plane

- `distributed-systems` · required · raw_text: "distributed control systems"
- `networking` · required · raw_text: "Ethernet-based control networks"
- `observability` · required · raw_text: "real-time monitoring"
- `software-architecture` · required · raw_text: "make architecture decisions"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - None of the four labeled skills (distributed-systems, networking, observability, software-architecture) is offered as an alternative to another under an 'at least one of' or 'X, Y or Z' marker, so the alternative_group rule yields no group.

DECISION: []

## 158. golden_095 - groups `alternative_group` (groups)

> AI/ML Physical Design Flow Engineer

- `machine-learning` · nice_to_have · raw_text: "interest or experience in ML frameworks"
- `python` · required · raw_text: "Strong Python/Tcl"
- `pytorch` · nice_to_have · raw_text: "interest or experience in ML frameworks (PyTorch, TensorFlow)"
- `tensorflow` · nice_to_have · raw_text: "interest or experience in ML frameworks (PyTorch, TensorFlow)"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "tensorflow"]] - The ask 'interest or experience in ML frameworks' is given with examples in parentheses (PyTorch, TensorFlow), so any one example meets it, as in the rule's 'cloud platforms (GCP, AWS or Azure)' case; the broad parent 'machine-learning' stays out of the group.

DECISION: [["pytorch", "tensorflow"]]

## 159. golden_096 - groups `alternative_group` (groups)

> Staff R&D AI Engineer

- `ai-deployment` · required · raw_text: "deploying large-scale models"
- `ai-ml` · required · raw_text: "AI/ML engineering"
- `aws` · nice_to_have · raw_text: "AWS"
- `azure` · nice_to_have · raw_text: "Azure"
- `cloud` · nice_to_have · raw_text: "cloud platforms"
- `computer-vision` · required · raw_text: "Strong expertise in both computer vision"
- `containerization` · nice_to_have · raw_text: "containerization technologies"
- `deep-learning` · required · raw_text: "deep learning"
- `deepspeed` · nice_to_have · raw_text: "DeepSpeed"
- `distributed-training` · required · raw_text: "experience in distributed training"
- `fine-tuning` · required · raw_text: "large language model fine-tuning"
- `gcp` · nice_to_have · raw_text: "GCP"
- `knowledge-distillation` · nice_to_have · raw_text: "distillation"
- `llms` · required · raw_text: "large language model fine-tuning"
- `mlops` · required · raw_text: "MLOps practices"
- `model-development` · required · raw_text: "hands-on model development experience"
- `model-versioning` · required · raw_text: "model versioning"
- `nlp` · required · raw_text: "natural language processing"
- `observability` · required · raw_text: "monitoring"
- `python` · required · raw_text: "Python"
- `pytorch` · required · raw_text: "PyTorch"
- `quantization` · nice_to_have · raw_text: "quantization"
- `reinforcement-learning` · required · raw_text: "reinforcement learning algorithms"
- `tensorflow` · required · raw_text: "TensorFlow"
- `transformers` · required · raw_text: "transformer architectures"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "tensorflow"], ["aws", "gcp", "azure"]] - The posting says "PyTorch and/or TensorFlow", which matches the and/or marker, and lists "cloud platforms (AWS, GCP, Azure)" as examples for a single ask, so each set groups its members while `cloud` stays out and the quantization/pruning/distillation list, which has no alternative marker, is not grouped.

DECISION: [["aws", "azure", "gcp"], ["pytorch", "tensorflow"]]

## 160. golden_097 - groups `alternative_group` (groups)

> Senior Machine Learning Engineer, Agentic Systems (Active Secret Clearance)

- `agents` · required · raw_text: "LLM-powered agents and agentic workflows"
- `ai-ml` · required · raw_text: "Experience integrating AI systems"
- `angular` · nice_to_have · raw_text: "Angular"
- `apis` · required · raw_text: "APIs"
- `async-processing` · nice_to_have · raw_text: "asynchronous programming"
- `ci-cd` · required · raw_text: "CI/CD"
- `cloud` · nice_to_have · raw_text: "cloud environments"
- `containerization` · nice_to_have · raw_text: "containerized"
- `cpp` · required · raw_text: "C++"
- `data-pipelines` · required · raw_text: "ETL pipelines"
- `docker` · nice_to_have · raw_text: "Docker"
- `evaluation` · required · raw_text: "evaluation approaches and frameworks"
- `git` · required · raw_text: "version control"
- `go` · required · raw_text: "Go"
- `graphql` · nice_to_have · raw_text: "GraphQL"
- `infrastructure-as-code` · nice_to_have · raw_text: "infrastructure as code"
- `java` · required · raw_text: "Java"
- `kubernetes` · nice_to_have · raw_text: "Kubernetes [K8s]"
- `llms` · required · raw_text: "LLM-powered"
- `machine-learning` · required · raw_text: "machine learning, and other production analytics"
- `mcp` · required · raw_text: "MCP servers"
- `multi-agent-systems` · required · raw_text: "multi-agent architectures"
- `python` · required · raw_text: "excellence in Python is essential"
- `pytorch` · required · raw_text: "PyTorch"
- `rag` · required · raw_text: "retrieval-augmented generation (RAG)"
- `react` · nice_to_have · raw_text: "React"
- `rust` · required · raw_text: "Rust"
- `scala` · required · raw_text: "Scala"
- `scikit-learn` · required · raw_text: "and/or scikit-learn"
- `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"
- `software-engineering` · required · raw_text: "Strong software engineering fundamentals"
- `tensorflow` · required · raw_text: "TensorFlow"
- `tool-calling` · required · raw_text: "tool use"
- `vue` · nice_to_have · raw_text: "Vue"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["go", "rust", "cpp", "java", "scala"], ["tensorflow", "pytorch", "scikit-learn"], ["docker", "kubernetes", "infrastructure-as-code"], ["react", "vue", "angular", "graphql", "async-processing"]] - Under the rule's 'examples offered for a single ask' marker, each parenthesised 'e.g.' or 'and/or' list counts as one ask met by any one member (the systems-language list, the TensorFlow/PyTorch/scikit-learn list, the containerized-or-cloud deployment examples, and the client-server examples), while the broad parents (cloud, containerization, software-architecture) and the unmarked skills stay out.

DECISION: [["angular", "async-processing", "graphql", "react", "vue"], ["cpp", "go", "java", "rust", "scala"], ["docker", "infrastructure-as-code", "kubernetes"], ["pytorch", "scikit-learn", "tensorflow"]]

## 161. golden_098 - groups `alternative_group` (groups)

> Data Scientist (Active Secret Clearance)

- `agents` · required · raw_text: "agentic systems"
- `ai-deployment` · nice_to_have · raw_text: "Experience deploying machine learning and data science solutions to production environments"
- `cloud` · nice_to_have · raw_text: "cloud infrastructure"
- `cpp` · nice_to_have · raw_text: "C++"
- `data-pipelines` · nice_to_have · raw_text: "ETL pipelines, data pipelines"
- `data-science` · required · raw_text: "Proficiency in machine learning and data science"
- `devops` · nice_to_have · raw_text: "Exposure to DevOps"
- `go` · nice_to_have · raw_text: "Go"
- `java` · nice_to_have · raw_text: "Java"
- `machine-learning` · required · raw_text: "Proficiency in machine learning"
- `python` · required · raw_text: "Excellence in Python"
- `pytorch` · required · raw_text: "PyTorch"
- `rust` · nice_to_have · raw_text: "Rust"
- `scala` · nice_to_have · raw_text: "Scala"
- `scikit-learn` · required · raw_text: "and/or scikit-learn"
- `software-engineering` · required · raw_text: "Exposure to software development life cycle and tools"
- `tensorflow` · required · raw_text: "TensorFlow"
- `workflow-automation` · nice_to_have · raw_text: "and/or workflow automation"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["tensorflow", "pytorch", "scikit-learn"], ["data-pipelines", "workflow-automation"], ["go", "rust", "cpp", "java", "scala"]] - Under the alternative_group markers, the 'knowledge of TensorFlow, PyTorch, and/or scikit-learn' list, the 'ETL pipelines, data pipelines, and/or workflow automation' list, and the 'systems programming language (e.g., Go, Rust, C++, Java, Scala, etc.)' examples each offer any one member for a single ask, and none of these members is asked for elsewhere in the posting.

DECISION: [["cpp", "go", "java", "rust", "scala"], ["data-pipelines", "workflow-automation"], ["pytorch", "scikit-learn", "tensorflow"]]

## 162. golden_099 - groups `alternative_group` (groups)

> Machine Learning Engineer

- `ai-deployment` · required · raw_text: "You've shipped a neural network, not just trained one."
- `computer-vision` · required · raw_text: "computer vision"
- `cpp` · required · raw_text: "Enough C++ to be useful"
- `deep-learning` · required · raw_text: "a modern deep learning framework"
- `inference-optimization` · nice_to_have · raw_text: "You've made a model meaningfully faster on target hardware"
- `llms` · required · raw_text: "large language models"
- `machine-learning` · required · raw_text: "Real depth in one modern ML area"
- `model-development` · required · raw_text: "taking models from data collection through training"
- `python` · required · raw_text: "Python"
- `sql` · required · raw_text: "SQL"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["computer-vision", "llms"]] - The posting asks for 'real depth in one modern ML area — computer vision, large language models, or generative modelling', an 'X, Y or Z' marker for one ask, so the labelled computer-vision and llms skills form a group, while the broad machine-learning parent stays out as a skill named alongside its examples.

DECISION: [["computer-vision", "llms"]]

## 163. golden_101 - groups `alternative_group` (groups)

> Staff Machine Learning Engineer

- `ai-deployment` · required · raw_text: "deploying advanced AI models"
- `apache-spark` · nice_to_have · raw_text: "Spark"
- `aws` · nice_to_have · raw_text: "AWS"
- `azure` · nice_to_have · raw_text: "Azure"
- `cloud` · nice_to_have · raw_text: "Experience with cloud computing services"
- `containerization` · nice_to_have · raw_text: "Familiarity with containerization"
- `docker` · nice_to_have · raw_text: "Docker"
- `gcp` · nice_to_have · raw_text: "GCP"
- `hadoop` · nice_to_have · raw_text: "Hadoop"
- `kubernetes` · nice_to_have · raw_text: "Kubernetes"
- `llms` · required · raw_text: "specific expertise in Large Language Models"
- `machine-learning` · required · raw_text: "6 years of experience in machine learning"
- `model-development` · required · raw_text: "developing and deploying advanced AI models"
- `python` · required · raw_text: "Strong programming skills in Python"
- `pytorch` · required · raw_text: "PyTorch"
- `tensorflow` · required · raw_text: "TensorFlow"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["tensorflow", "pytorch"], ["aws", "azure", "gcp"], ["hadoop", "apache-spark"]] - Under the rule's markers, "TensorFlow and/or PyTorch" is an 'and/or' set, and the parenthetical lists "(AWS, Azure, GCP)" and "(Hadoop, Spark)" are examples offered for the single asks "cloud computing services" and "Big Data technologies", so any one meets each ask; "containerization and orchestration (Docker, Kubernetes)" is left ungrouped because it asks for both categories together.

DECISION: [["apache-spark", "hadoop"], ["aws", "azure", "gcp"], ["pytorch", "tensorflow"]]

## 164. golden_102 - groups `alternative_group` (groups)

> Lead Data Scientist – Autonomous Driving

- `data-pipelines` · required · raw_text: "ship analyses and pipelines end to end"
- `python` · required · raw_text: "strong Python"
- `sql` · required · raw_text: "SQL"
- `statistics` · required · raw_text: "strong background in statistical reasoning and methods"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - The posting asks for Python and SQL together and lists no 'at least one of' or 'X or Y' alternatives among the labeled skills, so under the alternative_group rule's 'Not alternatives' clause no group applies.

DECISION: []

## 165. golden_103 - groups `alternative_group` (groups)

> Junior Machine Learning Engineer

- `agents` · nice_to_have · raw_text: "agentic workflows"
- `async-processing` · nice_to_have · raw_text: "asynchronous programming"
- `cloud` · nice_to_have · raw_text: "cloud environments"
- `containerization` · nice_to_have · raw_text: "containerized"
- `docker` · nice_to_have · raw_text: "Docker"
- `embeddings` · nice_to_have · raw_text: "embeddings"
- `evaluation` · nice_to_have · raw_text: "LLM evaluation"
- `event-driven-systems` · nice_to_have · raw_text: "event-driven architectures"
- `kubernetes` · nice_to_have · raw_text: "Kubernetes (K8s)"
- `llm-guardrails` · nice_to_have · raw_text: "guardrails"
- `machine-learning` · required · raw_text: "development and use of machine learning models"
- `model-development` · required · raw_text: "development and use of machine learning models"
- `observability` · nice_to_have · raw_text: "observability"
- `python` · required · raw_text: "Strong proficiency in Python"
- `pytorch` · required · raw_text: "PyTorch"
- `rag` · nice_to_have · raw_text: "retrieval-augmented generation (RAG)"
- `scikit-learn` · required · raw_text: "scikit-learn"
- `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"
- `software-engineering` · required · raw_text: "Strong software engineering fundamentals"
- `tensorflow` · required · raw_text: "TensorFlow"
- `testing` · nice_to_have · raw_text: "testing"
- `vector-databases` · nice_to_have · raw_text: "vector databases"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "tensorflow", "scikit-learn"], ["docker", "kubernetes"], ["agents", "evaluation", "testing", "observability", "llm-guardrails"], ["vector-databases", "embeddings", "rag"], ["async-processing", "event-driven-systems"]] - Each bullet asks for one thing that any one listed example meets ("libraries and frameworks like X, Y, and/or Z", "tools such as X, Y, or Z", "X, Y, Z, or W"), so under the alternative_group rule each becomes a group of its labelled skills, with the broad parents (containerization, cloud, software-engineering) and the 'or other' phrasing left out.

DECISION: [["agents", "evaluation", "llm-guardrails", "observability", "testing"], ["async-processing", "event-driven-systems"], ["docker", "kubernetes"], ["embeddings", "rag", "vector-databases"], ["pytorch", "scikit-learn", "tensorflow"]]

## 166. golden_104 - groups `alternative_group` (groups)

> AI Research Scientist

- `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving ML techniques"
- `deep-learning` · required · raw_text: "deep learning architectures"
- `distributed-training` · nice_to_have · raw_text: "Experience with distributed training"
- `evaluation` · required · raw_text: "validating ML model performance"
- `fine-tuning` · required · raw_text: "fine-tuning large-scale models"
- `jax` · required · raw_text: "JAX"
- `knowledge-distillation` · required · raw_text: "distillation"
- `llms` · nice_to_have · raw_text: "Research experience in generative AI"
- `machine-learning` · required · raw_text: "machine learning research"
- `model-development` · required · raw_text: "AI model development"
- `python` · required · raw_text: "Proficiency in Python"
- `pytorch` · required · raw_text: "PyTorch"
- `quantization` · required · raw_text: "quantization, distillation, pruning"
- `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning"
- `tensorflow` · required · raw_text: "TensorFlow"
- `transformers` · required · raw_text: "transformers, CNNs, RNNs"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "tensorflow", "jax"]] - The qualifications ask for "ML frameworks such as PyTorch, TensorFlow, or JAX", where the "X, Y or Z" and "such as" markers offer any one example for a single ask, so these three form one group, while Python is asked separately and stays out.

DECISION: ?

## 167. golden_105 - groups `alternative_group` (groups)

> Physical Design Methodology Engineer, AI HW IP

- `ai-ml` · required · raw_text: "Building with AI as part of how you develop flows"
- `llms` · required · raw_text: "opinionated about where LLMs and ML-driven optimization genuinely help"
- `machine-learning` · required · raw_text: "ML-driven optimization genuinely help"
- `python` · required · raw_text: "Python"
- `workflow-automation` · required · raw_text: "removing manual steps and making PPA exploration repeatable"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [] - Under the alternative_group rule, a group needs at least two of the listed skills offered in place of each other, and the posting's only alternative-style list (scripting languages: Tcl, Python, Perl) has just python among the listed skills, while the other listed skills are joined by 'and' or stand alone, so no group forms.

DECISION: []

## 168. golden_106 - groups `alternative_group` (groups)

> Staff Design Verification Engineer, AI HW

- `bash` · required · raw_text: "Bash scripting"
- `ci-cd` · required · raw_text: "manage CI pipelines"
- `linux` · required · raw_text: "Proficient in Linux environments"
- `python` · required · raw_text: "with Python, or Bash scripting"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["bash", "python"]] - The alternative_group rule's markers include 'X, Y or Z' and 'X or Y', and 'Proficient in Linux environments with Python, or Bash scripting' offers either scripting language for one ask, while bash appears nowhere else as a standalone requirement, so bash and python form one group and linux and ci-cd stay out.

DECISION: ?

## 169. golden_107 - groups `alternative_group` (groups)

> Software Engineer – ML Platform

- `apis` · required · raw_text: "APIs"
- `cpp` · nice_to_have · raw_text: "C++ is a plus"
- `data-pipelines` · nice_to_have · raw_text: "training data pipelines"
- `distributed-systems` · nice_to_have · raw_text: "optimizing resource usage and performance in distributed environments"
- `distributed-training` · nice_to_have · raw_text: "distributed training"
- `go` · required · raw_text: "Python or Go"
- `kubernetes` · required · raw_text: "Deep knowledge of Kubernetes"
- `linux` · required · raw_text: "Solid Linux"
- `mlflow` · nice_to_have · raw_text: "MLflow"
- `networking` · required · raw_text: "performance investigation, networking"
- `observability` · required · raw_text: "reliability practices, observability"
- `python` · required · raw_text: "Strong proficiency in Python or Go"
- `ray` · nice_to_have · raw_text: "Experience with Argo Workflows, Ray"
- `software-architecture` · required · raw_text: "designing and building scalable, maintainable systems and services"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["go", "python"]] - The 'Strong proficiency in Python or Go' line is an 'X or Y' alternative for one ask, so python and go form a group; the Argo/Ray/MLflow 'or comparable' list is not grouped because Ray is also required on its own via the Ray-based SDK responsibility, which leaves only mlflow.

DECISION: [["go", "python"]]

## 170. golden_108 - groups `alternative_group` (groups)

> Special Notice:

- `ai-deployment` · required · raw_text: "deploying and maintaining machine learning/AI systems in production"
- `ai-ml` · required · raw_text: "machine learning/AI systems"
- `data-pipelines` · required · raw_text: "systems involving data pipelines"
- `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving AI and secure compute environments"
- `devops` · nice_to_have · raw_text: "DevOps tooling"
- `distributed-systems` · nice_to_have · raw_text: "distributed systems"
- `full-stack-development` · nice_to_have · raw_text: "developing full stack applications"
- `jax` · required · raw_text: "JAX"
- `machine-learning` · required · raw_text: "software engineering and machine learning"
- `mlops` · required · raw_text: "maintaining machine learning/AI systems in production"
- `onnx` · required · raw_text: "ONNX"
- `pytorch` · required · raw_text: "PyTorch"
- `software-engineering` · required · raw_text: "experience in software engineering"
- `tensorflow` · required · raw_text: "TensorFlow"

Options: a JSON list of groups of the skill ids below, e.g. `[["bash", "python"]]`, or `[]` when no skills are offered in place of each other

PROPOSED: [["pytorch", "tensorflow", "onnx", "jax"]] - The ask for ML frameworks is an example list offered for a single ask ('frameworks such as PyTorch, TensorFlow, ONNX, JAX, etc.'), so any one meets it, 'etc.' adds nothing, and none of the four is asked for on its own elsewhere in the posting.

DECISION: [["jax", "onnx", "pytorch", "tensorflow"]]
