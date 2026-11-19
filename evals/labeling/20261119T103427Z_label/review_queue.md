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

DECISION: ?

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

DECISION: ?

## 20. golden_095 - skill `machine-learning` (disagreement)

> ...flows. - Strong Python/Tcl and data skills, with interest or experience in ML frameworks (PyTorch, TensorFlow), and the ability to drive complex...

- A: (did not label this)
- B: `machine-learning` · nice_to_have · raw_text: "interest or experience in ML frameworks"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_096 - skill `ml-engineering` (disagreement)

> ...& Skills: - 7+ years of experience in AI/ML engineering with 4+ years focusing on deep learning and neural network...

- A: (did not label this)
- B: `ml-engineering` · required · raw_text: "AI/ML engineering"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_097 - skill `ai-ml` (disagreement)

> ...and optimizing LLM-powered agents and agentic workflows - Experience integrating AI systems with external tools, APIs, MCP servers, and enterprise...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "Experience integrating AI systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_097 - skill `software-architecture` (disagreement)

> ...science, or a related discipline - Knowledge of relevant architectures and design patterns for client-server systems (e.g., asynchronous programming, REST, GraphQL, React,...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_098 - skill `software-engineering` (disagreement)

> ...knowledge of TensorFlow, PyTorch, and/or scikit-learn - Exposure to software development life cycle and tools - Active Secret (or above) US security clearance and US...

- A: `software-engineering` · required · raw_text: "Exposure to software development life cycle and tools"
- B: `software-engineering` · nice_to_have · raw_text: "Experience developing software"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_099 - skill `ai-deployment` (disagreement)

> ...of the real difficulty lives. What we're looking for - You've shipped a neural network, not just trained one. At least three years taking models from data collection...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "You've shipped a neural network, not just trained one."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_099 - skill `model-development` (disagreement)

> ...neural network, not just trained one. At least three years taking models from data collection through training to something that ran in production or on real hardware,...

- A: (did not label this)
- B: `model-development` · required · raw_text: "taking models from data collection through training"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_100 - attribute `degree` (disagreement)

> ...models for architecture exploration. What You Bring - A Bachelor’s degree in EE/ECE/CE/CS or a related field (MS or PhD preferred). - Strong foundational experience in RTL design with a...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="A Bachelor’s degree in EE/ECE/CE/CS or a related field (MS or PhD preferred)"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="A Bachelor’s degree in EE/ECE/CE/CS or a related field (MS or PhD preferred)."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_100 - attribute `seniority` (disagreement)

> AI Accelerator Architect Tenstorrent is leading the industry on cutting-edge AI...

- A: value="senior" · basis="stated" · signal="AI Accelerator Architect"
- B: value=null · basis=null · signal=null

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_101 - attribute `degree` (disagreement)

> ...and best practices. Qualifications: - Advanced degree (Ph.D. preferred) in Computer Science, or a related field. - Proven track record of building and innovations...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="Advanced degree (Ph.D. preferred) in Computer Science, or a related field"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Advanced degree (Ph.D. preferred) in Computer Science, or a related field."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_101 - skill `ai-deployment` (disagreement)

> ...will have a proven track record of developing and deploying advanced AI models. You will lead core product initiatives across on-device...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying advanced AI models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_101 - skill `model-development` (disagreement)

> ...The ideal candidate will have a proven track record of developing and deploying advanced AI models. You will lead core product initiatives across on-device...

- A: (did not label this)
- B: `model-development` · required · raw_text: "developing and deploying advanced AI models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_103 - skill `model-development` (disagreement)

> ...least one systems programming language - Exposure to the development and use of machine learning models, through either coursework or practical experience -...

- A: (did not label this)
- B: `model-development` · required · raw_text: "development and use of machine learning models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_104 - skill `data-privacy-and-security` (disagreement)

> ...learning, or multimodal learning - Familiarity with privacy-preserving ML techniques such as federated learning - Experience contributing to...

- A: (did not label this)
- B: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving ML techniques"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_105 - attribute `seniority` (disagreement)

> ...run them without you. What We Need - An Engineer with 5+ years developing and supporting physical design methodology or CAD flows in production use. - Expertise with industry-standard...

- A: value="senior" · basis="inferred" · signal="5+ years developing and supporting physical design methodology or CAD flows"
- B: value=null · basis=null · signal=null

Options: `A` / `B` / `both` / `drop`

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

DECISION: ?

## 37. golden_107 - skill `distributed-systems` (disagreement)

> ...training, training data pipelines - Track record of optimizing resource usage and performance in distributed environments #LI-MS1 Candidates are required to be authorized to...

- A: (did not label this)
- B: `distributed-systems` · nice_to_have · raw_text: "optimizing resource usage and performance in distributed environments"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 38. golden_107 - skill `software-architecture` (disagreement)

> ...in Python or Go; C++ is a plus - Track record of designing and building scalable, maintainable systems and services - Experience operating production services end-to-end:...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designing and building scalable, maintainable systems and services"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 39. golden_108 - skill `ai-ml` (disagreement)

> ...- Proven track record of deploying and maintaining machine learning/AI systems in production. - Strong expertise in ML frameworks such...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "machine learning/AI systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 40. golden_108 - skill `mlops` (disagreement)

> ...clearance - Proven track record of deploying and maintaining machine learning/AI systems in production. - Strong expertise in ML frameworks such as PyTorch,...

- A: (did not label this)
- B: `mlops` · required · raw_text: "maintaining machine learning/AI systems in production"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 41. golden_094 - skill `observability` (uncertain)

> ...and Ethernet-based control networks, along with telemetry, real-time monitoring, and fault detection. - You can set technical direction,...

- A: `observability` · required · raw_text: "real-time monitoring"
- B: `observability` · required · raw_text: "real-time monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_096 - skill `ai-deployment` (uncertain)

> ...in PyTorch and/or TensorFlow with experience training and deploying large-scale models - Experience with transformer architectures, attention...

- A: `ai-deployment` · required · raw_text: "deploying large-scale models"
- B: `ai-deployment` · required · raw_text: "deploying large-scale models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_096 - skill `ai-ml` (uncertain)

> ...& Skills: - 7+ years of experience in AI/ML engineering with 4+ years focusing on deep learning and neural network...

- A: `ai-ml` · required · raw_text: "AI/ML engineering"
- B: `ai-ml` · required · raw_text: "AI/ML engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_096 - skill `knowledge-distillation` (uncertain)

> ...and model optimization techniques (quantization, pruning, distillation) - Experience with embodied AI research or projects...

- A: `knowledge-distillation` · nice_to_have · raw_text: "distillation"
- B: `knowledge-distillation` · nice_to_have · raw_text: "distillation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_096 - skill `quantization` (uncertain)

> ...with edge AI deployment and model optimization techniques (quantization, pruning, distillation) - Experience with embodied AI...

- A: `quantization` · nice_to_have · raw_text: "quantization"
- B: `quantization` · nice_to_have · raw_text: "quantization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_097 - attribute `degree` (uncertain)

> ...to put them into practice. What we’re looking for - A BS degree in computer science, machine learning, or a related discipline and 6+ years relevant experience - Demonstrated...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_097 - skill `async-processing` (uncertain)

> ...and design patterns for client-server systems (e.g., asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience...

- A: `async-processing` · nice_to_have · raw_text: "asynchronous programming"
- B: `async-processing` · nice_to_have · raw_text: "asynchronous programming"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_098 - attribute `degree` (uncertain)

> ...to put them into practice. What we’re looking for - A BS degree in computer science, machine learning, mathematics, or a related discipline and 2+ years of relevant experience - Proficiency in...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, mathematics, or a related discipline"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, mathematics, or a related discipline"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_098 - attribute `seniority` (uncertain)

> ...machine learning, mathematics, or a related discipline and 2+ years of relevant experience - Proficiency in machine learning and data science, with...

- A: value="junior" · basis="inferred" · signal="2+ years of relevant experience"
- B: value="junior" · basis="inferred" · signal="2+ years of relevant experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_098 - skill `agents` (uncertain)

> ...demonstrated application to image data, video data, or agentic systems - Proficiency in implementing and analyzing data...

- A: `agents` · required · raw_text: "agentic systems"
- B: `agents` · required · raw_text: "agentic systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_099 - skill `inference-optimization` (uncertain)

> ...when it's the right call. Things that would stand out - You've made a model meaningfully faster on target hardware and can explain what you gave up to get there. - You've...

- A: `inference-optimization` · nice_to_have · raw_text: "You've made a model meaningfully faster on target hardware"
- B: `inference-optimization` · nice_to_have · raw_text: "You've made a model meaningfully faster on target hardware"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_099 - skill `machine-learning` (uncertain)

> ...in production or on real hardware, and stayed working. - Real depth in one modern ML area — computer vision, large language models, or generative...

- A: `machine-learning` · required · raw_text: "Real depth in one modern ML area"
- B: `machine-learning` · required · raw_text: "Real depth in one modern ML area"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_101 - skill `apache-spark` (uncertain)

> ...GCP). - Knowledge of Big Data technologies (Hadoop, Spark). - Familiarity with containerization and orchestration...

- A: `apache-spark` · nice_to_have · raw_text: "Spark"
- B: `apache-spark` · nice_to_have · raw_text: "Spark"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_101 - skill `aws` (uncertain)

> ...Skills: - Experience with cloud computing services (AWS, Azure, GCP). - Knowledge of Big Data technologies...

- A: `aws` · nice_to_have · raw_text: "AWS"
- B: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_101 - skill `azure` (uncertain)

> ...- Experience with cloud computing services (AWS, Azure, GCP). - Knowledge of Big Data technologies (Hadoop,...

- A: `azure` · nice_to_have · raw_text: "Azure"
- B: `azure` · nice_to_have · raw_text: "Azure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

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

DECISION: ?

## 58. golden_102 - skill `data-pipelines` (uncertain)

> ...Python and SQL; you can independently run experiments and ship analyses and pipelines end to end. - Leadership: proven technical leadership, mentoring,...

- A: `data-pipelines` · required · raw_text: "ship analyses and pipelines end to end"
- B: `data-pipelines` · required · raw_text: "ship analyses and pipelines end to end"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_103 - attribute `degree` (uncertain)

> ...to put them into practice. What we’re looking for - A BS degree in computer science, machine learning, or a related discipline and 0–2 years of relevant experience - Strong proficiency...

- A: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"
- B: value="bachelor" · requirement="required" · or_equivalent=false · signal="A BS degree in computer science, machine learning, or a related discipline"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 60. golden_103 - skill `agents` (uncertain)

> ...on structured and unstructured data - Experience with agentic workflows, LLM evaluation, testing, observability, or guardrails -...

- A: `agents` · nice_to_have · raw_text: "agentic workflows"
- B: `agents` · nice_to_have · raw_text: "agentic workflows"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_103 - skill `async-processing` (uncertain)

> ...Podman, or Kubernetes (K8s) - Experience working with asynchronous programming, concurrency, or event-driven architectures - Active...

- A: `async-processing` · nice_to_have · raw_text: "asynchronous programming"
- B: `async-processing` · nice_to_have · raw_text: "asynchronous programming"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_103 - skill `cloud` (uncertain)

> ...implementing and deploying software in containerized or cloud environments, using tools such as Docker, Podman, or Kubernetes...

- A: `cloud` · nice_to_have · raw_text: "cloud environments"
- B: `cloud` · nice_to_have · raw_text: "cloud environments"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_103 - skill `containerization` (uncertain)

> ...Experience implementing and deploying software in containerized or cloud environments, using tools such as Docker, Podman,...

- A: `containerization` · nice_to_have · raw_text: "containerized"
- B: `containerization` · nice_to_have · raw_text: "containerized"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_103 - skill `software-architecture` (uncertain)

> ...modern AI application patterns - Knowledge of relevant architectures and design patterns for client-server systems - Experience implementing and deploying software in...

- A: `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"
- B: `software-architecture` · nice_to_have · raw_text: "architectures and design patterns for client-server systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_104 - attribute `degree` (uncertain)

> ...Mathematics, or a related field Preferred Skills - Master’s or PhD in Machine Learning, Computer Science, AI, or a related field - Experience...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s or PhD in Machine Learning"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s or PhD in Machine Learning, Computer Science, AI, or a related field"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_104 - skill `evaluation` (uncertain)

> ...- Experience building datasets, designing experiments, and validating ML model performance - Deep understanding of optimization techniques...

- A: `evaluation` · required · raw_text: "validating ML model performance"
- B: `evaluation` · required · raw_text: "validating ML model performance"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_104 - skill `machine-learning` (uncertain)

> ...- 4+ years of experience (can be graduate research) in machine learning research, AI model development, or related fields - Strong...

- A: `machine-learning` · required · raw_text: "machine learning research"
- B: `machine-learning` · required · raw_text: "machine learning research"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_104 - skill `model-development` (uncertain)

> ...(can be graduate research) in machine learning research, AI model development, or related fields - Strong expertise in deep learning...

- A: `model-development` · required · raw_text: "AI model development"
- B: `model-development` · required · raw_text: "training and fine-tuning large-scale models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_105 - skill `llms` (uncertain)

> ...Building with AI as part of how you develop flows, and opinionated about where LLMs and ML-driven optimization genuinely help versus where they do not. - An effective partner to...

- A: `llms` · required · raw_text: "opinionated about where LLMs and ML-driven optimization genuinely help"
- B: `llms` · required · raw_text: "LLMs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_105 - skill `machine-learning` (uncertain)

> ...you develop flows, and opinionated about where LLMs and ML-driven optimization genuinely help versus where they do not. - An effective partner to...

- A: `machine-learning` · required · raw_text: "ML-driven optimization genuinely help"
- B: `machine-learning` · required · raw_text: "ML-driven optimization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_106 - attribute `seniority` (uncertain)

> Staff Design Verification Engineer, AI HW Tenstorrent is leading the industry on cutting-edge AI...

- A: value="senior" · basis="stated" · signal="Staff Design Verification Engineer, AI HW"
- B: value="senior" · basis="stated" · signal="Staff Design Verification Engineer, AI HW"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_106 - skill `ci-cd` (uncertain)

> ...Python, or Bash scripting for automate builds, parse logs, manage CI pipelines. - Skilled in coverage-driven verification and confident...

- A: `ci-cd` · required · raw_text: "manage CI pipelines"
- B: `ci-cd` · required · raw_text: "manage CI pipelines"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_107 - skill `networking` (uncertain)

> ...pressure - Solid Linux and systems debugging skills: performance investigation, networking, storage/IO - Ability to troubleshoot complex production...

- A: `networking` · required · raw_text: "performance investigation, networking"
- B: `networking` · required · raw_text: "networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_108 - skill `ai-deployment` (uncertain)

> ...- Active US Security clearance - Proven track record of deploying and maintaining machine learning/AI systems in production. - Strong expertise in ML frameworks such as PyTorch,...

- A: `ai-deployment` · required · raw_text: "deploying and maintaining machine learning/AI systems in production"
- B: `ai-deployment` · required · raw_text: "deploying and maintaining machine learning/AI systems in production"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_108 - skill `data-privacy-and-security` (uncertain)

> ...in developing full stack applications - Knowledge of privacy-preserving AI and secure compute environments. - Master’s degree in a relevant technical...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving AI and secure compute environments"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving AI and secure compute environments"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_094 - attribute `degree` (spot-check)

> ...differ from the one in this posting. Who You Are - You have a BS, MS, or PhD in Electrical, Mechanical, Computer, or Controls Engineering, or a related technical discipline, and 12+ years of relevant engineering experience. - You...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="You have a BS, MS, or PhD in Electrical, Mechanical, Computer, or Controls Engineering, or a related technical discipline"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 77. golden_095 - attribute `degree` (spot-check)

> ...differ from the one in this posting. Who you are - BS in Electrical or Computer Engineering (or equivalent experience) with 5+ years in Physical Design CAD methodology at...

- agreed label: value="bachelor" · requirement="required" · or_equivalent=true · signal="BS in Electrical or Computer Engineering (or equivalent experience)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 78. golden_096 - attribute `seniority` (spot-check)

> Staff R&D AI Engineer About Us: We are establishing the first distributed Al...

- agreed label: value="senior" · basis="stated" · signal="Staff R&D AI Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 79. golden_096 - skill `aws` (spot-check)

> ...on AI solutions - Experience with cloud platforms (AWS, GCP, Azure) and containerization technologies -...

- agreed label: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 80. golden_096 - skill `cloud` (spot-check)

> ...prototype and iterate on AI solutions - Experience with cloud platforms (AWS, GCP, Azure) and containerization technologies -...

- agreed label: `cloud` · nice_to_have · raw_text: "cloud platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 81. golden_096 - skill `containerization` (spot-check)

> ...- Experience with cloud platforms (AWS, GCP, Azure) and containerization technologies - Background in safety-critical AI systems or AI...

- agreed label: `containerization` · nice_to_have · raw_text: "containerization technologies"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 82. golden_096 - skill `deep-learning` (spot-check)

> ...experience in AI/ML engineering with 4+ years focusing on deep learning and neural network development - Strong understanding of...

- agreed label: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 83. golden_096 - skill `distributed-training` (spot-check)

> ...tracking - Strong programming skills in Python with experience in distributed training and model optimization - Understanding of sequential...

- agreed label: `distributed-training` · required · raw_text: "experience in distributed training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 84. golden_096 - skill `model-development` (spot-check)

> ...both computer vision and natural language processing with hands-on model development experience - Proficiency in PyTorch and/or TensorFlow with...

- agreed label: `model-development` · required · raw_text: "hands-on model development experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 85. golden_096 - skill `model-versioning` (spot-check)

> ...fundamentals - Experience with MLOps practices including model versioning, monitoring, and deployment pipelines - Proven ability...

- agreed label: `model-versioning` · required · raw_text: "model versioning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 86. golden_096 - skill `nlp` (spot-check)

> ...etc.) - Strong expertise in both computer vision and natural language processing with hands-on model development experience - Proficiency...

- agreed label: `nlp` · required · raw_text: "natural language processing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 87. golden_096 - skill `observability` (spot-check)

> ...with MLOps practices including model versioning, monitoring, and deployment pipelines - Proven ability to work...

- agreed label: `observability` · required · raw_text: "monitoring"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_096 - skill `tensorflow` (spot-check)

> ...development experience - Proficiency in PyTorch and/or TensorFlow with experience training and deploying large-scale...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_097 - skill `angular` (spot-check)

> ...asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience implementing and deploying software into...

- agreed label: `angular` · nice_to_have · raw_text: "Angular"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_097 - skill `apis` (spot-check)

> ...Experience integrating AI systems with external tools, APIs, MCP servers, and enterprise data sources - Experience...

- agreed label: `apis` · required · raw_text: "APIs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_097 - skill `ci-cd` (spot-check)

> ...and processes (Agile, version control, issue tracking, CI/CD, debugging, etc.) - Active Secret (or above) US security...

- agreed label: `ci-cd` · required · raw_text: "CI/CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_097 - skill `cloud` (spot-check)

> ...implementing and deploying software into containerized or cloud environments (e.g., Docker, Kubernetes [K8s], infrastructure as code,...

- agreed label: `cloud` · nice_to_have · raw_text: "cloud environments"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_097 - skill `cpp` (spot-check)

> ...at least one systems programming language (e.g., Go, Rust, C++, Java, Scala) - Proficiency with modern software...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_097 - skill `docker` (spot-check)

> ...software into containerized or cloud environments (e.g., Docker, Kubernetes [K8s], infrastructure as code, major cloud...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

## 98. golden_097 - skill `rag` (spot-check)

> ...performance, reliability, and safety - Familiarity with retrieval-augmented generation (RAG), tool use, planning, and multi-agent architectures -...

- agreed label: `rag` · required · raw_text: "retrieval-augmented generation (RAG)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_097 - skill `react` (spot-check)

> ...systems (e.g., asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience implementing and deploying...

- agreed label: `react` · nice_to_have · raw_text: "React"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_097 - skill `tensorflow` (spot-check)

> ...in Python is essential, as is knowledge of libraries like TensorFlow, PyTorch, and/or scikit-learn - Strong software...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_097 - skill `vue` (spot-check)

> ...(e.g., asynchronous programming, REST, GraphQL, React, Vue, Angular) - Experience implementing and deploying...

- agreed label: `vue` · nice_to_have · raw_text: "Vue"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_098 - attribute `german` (spot-check)

> Data Scientist (Active Secret Clearance)

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_098 - skill `ai-deployment` (spot-check)

> ...machine learning, mathematics, or a related discipline - Experience deploying machine learning and data science solutions to production environments - Exposure to DevOps and to cloud infrastructure -...

- agreed label: `ai-deployment` · nice_to_have · raw_text: "Experience deploying machine learning and data science solutions to production environments"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_098 - skill `data-pipelines` (spot-check)

> ...telemetry, graphs, or other) - Experience implementing ETL pipelines, data pipelines, and/or workflow automation - Experience developing...

- agreed label: `data-pipelines` · nice_to_have · raw_text: "ETL pipelines, data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_098 - skill `data-science` (spot-check)

> ...related discipline and 2+ years of relevant experience - Proficiency in machine learning and data science, with demonstrated application to image data, video data,...

- agreed label: `data-science` · required · raw_text: "Proficiency in machine learning and data science"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_098 - skill `go` (spot-check)

> ...— Dr. Jim Rebesco, Cofounder and CEO, Striveworks The government’s demand for AI is growing far faster than the...

- agreed label: `go` · nice_to_have · raw_text: "Go"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_098 - skill `python` (spot-check)

> ...and analyzing data structures and algorithms - Excellence in Python and knowledge of TensorFlow, PyTorch, and/or...

- agreed label: `python` · required · raw_text: "Excellence in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_098 - skill `rust` (spot-check)

> ...degrade in the real world. And when performance drops, trust goes with it. Striveworks was built to solve that...

- agreed label: `rust` · nice_to_have · raw_text: "Rust"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_098 - skill `scikit-learn` (spot-check)

> ...Excellence in Python and knowledge of TensorFlow, PyTorch, and/or scikit-learn - Exposure to software development life cycle and...

- agreed label: `scikit-learn` · required · raw_text: "and/or scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_098 - skill `tensorflow` (spot-check)

> ...and algorithms - Excellence in Python and knowledge of TensorFlow, PyTorch, and/or scikit-learn - Exposure to software...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_099 - attribute `german` (spot-check)

> Machine Learning Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_099 - attribute `seniority` (spot-check)

> ...You've shipped a neural network, not just trained one. At least three years taking models from data collection through training to...

- agreed label: value="mid" · basis="inferred" · signal="At least three years"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_099 - skill `computer-vision` (spot-check)

> ...and stayed working. - Real depth in one modern ML area — computer vision, large language models, or generative modelling. We'd...

- agreed label: `computer-vision` · required · raw_text: "computer vision"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_099 - skill `sql` (spot-check)

> ...who own it. - Comfort with large-scale data tooling and SQL — you can get your own data without waiting on someone...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_100 - attribute `german` (spot-check)

> AI Accelerator Architect

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_101 - skill `kubernetes` (spot-check)

> ...containerization and orchestration technologies (Docker, Kubernetes). - Publications or presentations in recognized Machine...

- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_101 - skill `pytorch` (spot-check)

> ...and machine learning frameworks like TensorFlow and/or PyTorch. - Demonstrated ability to lead complex projects and...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_101 - skill `tensorflow` (spot-check)

> ...skills in Python and machine learning frameworks like TensorFlow and/or PyTorch. - Demonstrated ability to lead complex...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_102 - attribute `degree` (spot-check)

> ...to have - Formal training in statistics (for example, MS or PhD in Statistics, Applied Statistics, Biostatistics, Econometrics, or a quantitative field with rigorous statistical coursework). - Familiarity with...

- agreed label: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="MS or PhD in Statistics, Applied Statistics, Biostatistics, Econometrics, or a quantitative field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_102 - skill `python` (spot-check)

> ...methods for evaluating change and uncertainty. - Coding: strong Python and SQL; you can independently run experiments and ship...

- agreed label: `python` · required · raw_text: "strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_103 - attribute `seniority` (spot-check)

> Junior Machine Learning Engineer “In 36 months, agentic AI systems will be an operating...

- agreed label: value="junior" · basis="stated" · signal="Junior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_103 - skill `docker` (spot-check)

> ...containerized or cloud environments, using tools such as Docker, Podman, or Kubernetes (K8s) - Experience working with...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_103 - skill `embeddings` (spot-check)

> ...or guardrails - Familiarity with vector databases, embeddings, retrieval-augmented generation (RAG), or other modern AI...

- agreed label: `embeddings` · nice_to_have · raw_text: "embeddings"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_103 - skill `python` (spot-check)

> ...related discipline and 0–2 years of relevant experience - Strong proficiency in Python including experience with libraries and frameworks like...

- agreed label: `python` · required · raw_text: "Strong proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_103 - skill `pytorch` (spot-check)

> ...including experience with libraries and frameworks like PyTorch, TensorFlow, and/or scikit-learn - Strong software...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_103 - skill `rag` (spot-check)

> ...Familiarity with vector databases, embeddings, retrieval-augmented generation (RAG), or other modern AI application patterns - Knowledge of...

- agreed label: `rag` · nice_to_have · raw_text: "retrieval-augmented generation (RAG)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_103 - skill `scikit-learn` (spot-check)

> ...libraries and frameworks like PyTorch, TensorFlow, and/or scikit-learn - Strong software engineering fundamentals and experience...

- agreed label: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_103 - skill `software-engineering` (spot-check)

> ...like PyTorch, TensorFlow, and/or scikit-learn - Strong software engineering fundamentals and experience with at least one systems programming...

- agreed label: `software-engineering` · required · raw_text: "Strong software engineering fundamentals"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_103 - skill `tensorflow` (spot-check)

> ...experience with libraries and frameworks like PyTorch, TensorFlow, and/or scikit-learn - Strong software engineering...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_103 - skill `testing` (spot-check)

> ...billions of dollars invested. The models perform in testing, but they degrade in the real world. And when performance...

- agreed label: `testing` · nice_to_have · raw_text: "testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_103 - skill `vector-databases` (spot-check)

> ...testing, observability, or guardrails - Familiarity with vector databases, embeddings, retrieval-augmented generation (RAG), or...

- agreed label: `vector-databases` · nice_to_have · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_104 - attribute `seniority` (spot-check)

> ...with webAI’s strategic priorities Qualifications: - 4+ years of experience (can be graduate research) in machine learning research,...

- agreed label: value="mid" · basis="inferred" · signal="4+ years of experience"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_104 - skill `deep-learning` (spot-check)

> ...development, or related fields - Strong expertise in deep learning architectures including transformers, CNNs, RNNs, and diffusion models...

- agreed label: `deep-learning` · required · raw_text: "deep learning architectures"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_104 - skill `distributed-training` (spot-check)

> ...Learning, Computer Science, AI, or a related field - Experience with distributed training, edge inference, or on-device ML - Research experience...

- agreed label: `distributed-training` · nice_to_have · raw_text: "Experience with distributed training"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_104 - skill `jax` (spot-check)

> ...Python and ML frameworks such as PyTorch, TensorFlow, or JAX - Experience building datasets, designing experiments,...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_104 - skill `llms` (spot-check)

> ...distributed training, edge inference, or on-device ML - Research experience in generative AI, reinforcement learning, or multimodal learning -...

- agreed label: `llms` · nice_to_have · raw_text: "Research experience in generative AI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_104 - skill `python` (spot-check)

> ...experience training and fine-tuning large-scale models - Proficiency in Python and ML frameworks such as PyTorch, TensorFlow, or JAX -...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_104 - skill `quantization` (spot-check)

> ...- Deep understanding of optimization techniques including quantization, distillation, pruning, and hardware-aware training - Strong problem-solving...

- agreed label: `quantization` · required · raw_text: "quantization, distillation, pruning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_104 - skill `transformers` (spot-check)

> ...Strong expertise in deep learning architectures including transformers, CNNs, RNNs, and diffusion models - Hands-on experience training and...

- agreed label: `transformers` · required · raw_text: "transformers, CNNs, RNNs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_105 - attribute `degree` (spot-check)

> Physical Design Methodology Engineer, AI HW IP

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

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

DECISION: ?

## 147. golden_107 - skill `cpp` (spot-check)

> ...you will need - Strong proficiency in Python or Go; C++ is a plus - Track record of designing and building scalable,...

- agreed label: `cpp` · nice_to_have · raw_text: "C++ is a plus"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_107 - skill `data-pipelines` (spot-check)

> ...ML training systems: GPU scheduling, distributed training, training data pipelines - Track record of optimizing resource usage and...

- agreed label: `data-pipelines` · nice_to_have · raw_text: "training data pipelines"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_107 - skill `kubernetes` (spot-check)

> ...end-to-end: APIs, reliability practices, observability - Deep knowledge of Kubernetes: how scheduling, resource management, controllers, and pod...

- agreed label: `kubernetes` · required · raw_text: "Deep knowledge of Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 150. golden_107 - skill `ray` (spot-check)

> ...and traces and drive them to resolution Nice to have - Experience with Argo Workflows, Ray, MLflow, or comparable distributed ML tooling - Hands-on...

- agreed label: `ray` · nice_to_have · raw_text: "Experience with Argo Workflows, Ray"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 151. golden_108 - skill `devops` (spot-check)

> ...hardware. - Familiarity with distributed systems, DevOps tooling, and performance tuning. - Prior experience in a...

- agreed label: `devops` · nice_to_have · raw_text: "DevOps tooling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 152. golden_108 - skill `distributed-systems` (spot-check)

> ...on edge devices or consumer hardware. - Familiarity with distributed systems, DevOps tooling, and performance tuning. - Prior...

- agreed label: `distributed-systems` · nice_to_have · raw_text: "distributed systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 153. golden_108 - skill `onnx` (spot-check)

> ...expertise in ML frameworks such as PyTorch, TensorFlow, ONNX, JAX, etc. - Experience debugging complex systems...

- agreed label: `onnx` · required · raw_text: "ONNX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 154. golden_108 - skill `pytorch` (spot-check)

> ...production. - Strong expertise in ML frameworks such as PyTorch, TensorFlow, ONNX, JAX, etc. - Experience debugging...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 155. golden_108 - skill `software-engineering` (spot-check)

> ...Skills & Qualifications: - 5+ years of combined experience in software engineering and machine learning. - Active US Security clearance -...

- agreed label: `software-engineering` · required · raw_text: "experience in software engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
