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

DECISION: ?

## 17. golden_095 - skill `agent-architecture` (disagreement)

> ...production environments - 2+ years of hands-on experience architecting and deploying agentic AI systems, LLM orchestration frameworks, or AI platform tooling -...

- A: (did not label this)
- B: `agent-architecture` · required · raw_text: "architecting and deploying agentic AI systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_095 - skill `ai-deployment` (disagreement)

> ...2+ years of hands-on experience architecting and deploying agentic AI systems, LLM orchestration frameworks, or AI platform tooling -...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying agentic AI systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_095 - skill `software-engineering` (disagreement)

> ...patterns What we're looking for - 6+ years of backend software engineering experience with deep focus on distributed systems,...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software engineering"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_096 - skill `model-development` (disagreement)

> ...in OS configuration tooling. - Familiarity with AI inference and/or training workflows and the operational patterns around them. - Pragmatic,...

- A: (did not label this)
- B: `model-development` · required · raw_text: "AI inference and/or training workflows"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_096 - skill `model-serving` (disagreement)

> ...servers and runtimes (e.g., Triton, vLLM, TGI) and model-serving patterns (batching, streaming, KV-cache aware routing). -...

- A: `model-serving` · nice_to_have · raw_text: "model-serving patterns"
- B: `model-serving` · required · raw_text: "running ML or inference services at scale on Kubernetes in production"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_097 - skill `inference-optimization` (disagreement)

> ...generative machine learning models. - Experience with optimizing the performance of machine learning models. - Experience leading research initiatives in Machine...

- A: (did not label this)
- B: `inference-optimization` · nice_to_have · raw_text: "optimizing the performance of machine learning models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_097 - skill `llms` (disagreement)

> ...Qualifications: - Experience with training generative machine learning models. - Experience with optimizing the performance of machine...

- A: (did not label this)
- B: `llms` · nice_to_have · raw_text: "generative machine learning models"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_098 - attribute `seniority` (disagreement)

> ...You’ll Need: Minimum Qualifications: - Master’s with 3+ years of experience, or PhD, in robotics, control or a related field. Strong...

- A: value="mid" · basis="inferred" · signal="3+ years of experience"
- B: value="senior" · basis="inferred" · signal="Lead the setup, calibration, maintenance and tuning of our robots"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_098 - skill `computer-vision` (disagreement)

> ...Hand-eye and multi-camera calibration, depth sensing and 3D perception on hardware. - Open-source contributions or publications at robotics...

- A: (did not label this)
- B: `computer-vision` · nice_to_have · raw_text: "3D perception on hardware"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_098 - skill `model-development` (disagreement)

> ...for 3D printing or machining. - Robot learning: you have trained or deployed learned policies (imitation learning, RL or VLA) on real robots, and are...

- A: (did not label this)
- B: `model-development` · required · raw_text: "trained or deployed learned policies"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_098 - skill `software-architecture` (disagreement)

> ...of arms with grippers or hands. - System design: you have designed robot software systems end to end (control loops at 500 Hz to 1 kHz, state estimation, data...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "designed robot software systems end to end"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_099 - skill `machine-learning` (disagreement)

> ...or algorithmic optimization for deep learning - Deep expertise on ML frameworks (e.g., PyTorch, TensorFlow, JAX) and understanding of ML...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "Deep expertise on ML frameworks"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_101 - skill `machine-learning` (disagreement)

> ...- Experience with hardware implementation of ML optimization techniques (e.g., sparsity, quantization, pruning). - Proficiency...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "ML optimization techniques"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_102 - skill `data-science` (disagreement)

> ...robust, and well-commented code to produce high-quality data science procedures 4 Days in Office: Metropolis values in-person...

- A: (did not label this)
- B: `data-science` · nice_to_have · raw_text: "data science procedures"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_103 - skill `testing` (disagreement)

> ...fundamentals — performant, scalable systems and confident debugging - Proficiency in Python and a major ML framework...

- A: (did not label this)
- B: `testing` · required · raw_text: "confident debugging"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 32. golden_104 - skill `ai-ml` (disagreement)

> ...engineering experience, including a proven track record of deploying AI/ML models to production in the cloud. - Strong experience with cloud architecture...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "deploying AI/ML models to production"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 33. golden_104 - skill `machine-learning` (disagreement)

> ...as code. - Proficiency in Python and C++, with experience using ML frameworks such as PyTorch or TensorFlow. - Advanced, hands-on...

- A: (did not label this)
- B: `machine-learning` · required · raw_text: "experience using ML frameworks"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 34. golden_105 - skill `software-architecture` (disagreement)

> ...technical leadership (standards, tooling, workflows, architectural direction). - Experience operating in Product environments where...

- A: (did not label this)
- B: `software-architecture` · nice_to_have · raw_text: "architectural direction"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 35. golden_105 - skill `software-engineering` (disagreement)

> ...Bachelor’s degree or equivalent experience. - 9+ years of software development experience, including ownership of complex product...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "software development"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 36. golden_108 - skill `ai-deployment` (disagreement)

> ...You’ll Need: - 2-4 years of experience building and deploying a relevant ML application in a practical or academic research setting and be fluent...

- A: (did not label this)
- B: `ai-deployment` · required · raw_text: "deploying a relevant ML application"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 37. golden_108 - skill `model-development` (disagreement)

> ...or applied mathematics/statistics. - Experience in developing ML training code for use in a cloud computing environment. - Demonstrated...

- A: (did not label this)
- B: `model-development` · required · raw_text: "developing ML training code"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 38. golden_094 - attribute `degree` (uncertain)

> ...machine learning organization What we're looking for - PhD in Computer Science, Statistics, Economics, Applied Mathematics, Industrial Engineering, Operational Research, or a related STEM field with 6+ years of relevant experience, or MS with 8+ years...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in Computer Science, Statistics, Economics, Applied Mathematics, Industrial Engineering, Operational Research, or a related STEM field"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="PhD in Computer Science, Statistics, Economics, Applied Mathematics, Industrial Engineering, Operational Research, or a related STEM field with 6+ years of relevant experience, or MS with 8+ years experiences with equivalent publications."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_094 - skill `agents` (uncertain)

> ...with Spark, and workflow orchestration via Airflow. - Experience building agentic AI solutions for pricing is highly desirable. - Proficient programming skills in Python and SQL....

- A: `agents` · nice_to_have · raw_text: "Experience building agentic AI solutions for pricing is highly desirable"
- B: `agents` · nice_to_have · raw_text: "Experience building agentic AI solutions for pricing is highly desirable."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_094 - skill `ai-deployment` (uncertain)

> ...owning and leading projects from inception to production, successfully deploying models and driving measurable business impact - Solid...

- A: `ai-deployment` · required · raw_text: "successfully deploying models"
- B: `ai-deployment` · required · raw_text: "deploying models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_095 - skill `async-processing` (uncertain)

> ...in Python or Java/TypeScript with production expertise in async concurrency, API design, and system performance tuning - Production...

- A: `async-processing` · required · raw_text: "async concurrency"
- B: `async-processing` · required · raw_text: "async concurrency"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_095 - skill `data-privacy-and-security` (uncertain)

> ...loops - Security compliance expertise regarding data privacy, prompt injection defenses, secrets management, and access...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "data privacy"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "Security compliance expertise regarding data privacy"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_095 - skill `mcp` (uncertain)

> ...orchestration frameworks and protocols such as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in...

- A: `mcp` · required · raw_text: "Anthropic MCP"
- B: `mcp` · required · raw_text: "Anthropic MCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_096 - attribute `degree` (uncertain)

> ...shipping iteratively. Preferred/Bonus Qualifications: - MS/PhD in Computer Science, Software Engineering, or a related field. - Experience with inference servers and runtimes (e.g.,...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="MS/PhD in Computer Science, Software Engineering, or a related field"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="MS/PhD in Computer Science, Software Engineering, or a related field."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_096 - skill `apis` (uncertain)

> ...for latency-sensitive services. - Experience building customer facing API platforms including onboarding, API keys/auth management, and usage...

- A: `apis` · nice_to_have · raw_text: "customer facing API platforms"
- B: `apis` · nice_to_have · raw_text: "API platforms"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_096 - skill `networking` (uncertain)

> ...in Kubernetes, scheduling, drivers, device plugins, MIG, networking, and storage considerations. - Solid coding skills in Python, Bash and proficiency...

- A: `networking` · required · raw_text: "networking, and storage considerations"
- B: `networking` · required · raw_text: "networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_097 - skill `ai-deployment` (uncertain)

> ...Computer Engineering, or a related field. - 3+ years of machine learning R&D and deployment experience. - Strong proficiency in one or more programming...

- A: `ai-deployment` · required · raw_text: "machine learning R&D and deployment experience"
- B: `ai-deployment` · required · raw_text: "machine learning R&D and deployment experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_097 - skill `model-development` (uncertain)

> ...Qualifications: - Experience with training generative machine learning models. - Experience with optimizing the performance of machine...

- A: `model-development` · nice_to_have · raw_text: "training generative machine learning models"
- B: `model-development` · nice_to_have · raw_text: "training generative machine learning models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_098 - attribute `degree` (uncertain)

> ...You’ll Need: Minimum Qualifications: - Master’s with 3+ years of experience, or PhD, in robotics, control or a related field. Strong candidates with a bachelor’s and 3+ years of...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s with 3+ years of experience, or PhD, in robotics, control or a related field"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s with 3+ years of experience, or PhD, in robotics, control or a related field. Strong candidates with a bachelor’s and 3+ years of industry experience are also considered."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_098 - skill `reinforcement-learning` (uncertain)

> ...machining. - Robot learning: you have trained or deployed learned policies (imitation learning, RL or VLA) on real robots, and are comfortable with PyTorch and at...

- A: `reinforcement-learning` · required · raw_text: "learned policies (imitation learning, RL or VLA)"
- B: `reinforcement-learning` · required · raw_text: "RL"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_099 - attribute `degree` (uncertain)

> ...inference engine. REQUIRED QUALIFICATIONS - BS/MS/PhD in Computer Science, Software Engineering, or a related field. - Deep experience building compilers, optimizing...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="BS/MS/PhD in Computer Science, Software Engineering, or a related field."
- B: value="phd" · requirement="required" · or_equivalent=false · signal="BS/MS/PhD in Computer Science, Software Engineering, or a related field."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 52. golden_099 - skill `deep-learning` (uncertain)

> ...and parallel execution - Quantization, sparsity, or algorithmic optimization for deep learning - Deep expertise on ML frameworks (e.g., PyTorch,...

- A: `deep-learning` · required · raw_text: "algorithmic optimization for deep learning"
- B: `deep-learning` · required · raw_text: "deep learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_099 - skill `llms` (uncertain)

> ...Strong understanding of one or more of the following: - LLM architectures and transformer internals - MLIR, LLVM, XLA, TVM,...

- A: `llms` · required · raw_text: "LLM architectures"
- B: `llms` · required · raw_text: "LLM architectures"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_099 - skill `quantization` (uncertain)

> ...if improving inference efficiency requires inventing new quantization schemes, rethinking graph-level optimizations, or...

- A: `quantization` · required · raw_text: "Quantization"
- B: `quantization` · required · raw_text: "Quantization"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_099 - skill `transformers` (uncertain)

> ...of one or more of the following: - LLM architectures and transformer internals - MLIR, LLVM, XLA, TVM, Triton, or similar compiler...

- A: `transformers` · required · raw_text: "transformer internals"
- B: `transformers` · required · raw_text: "transformer internals"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

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

DECISION: ?

## 60. golden_101 - skill `distributed-systems` (uncertain)

> ...on-chip interconnects, parallel processing, and distributed computing. - Excellent problem-solving skills and the ability to...

- A: `distributed-systems` · required · raw_text: "distributed computing"
- B: `distributed-systems` · required · raw_text: "distributed computing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_101 - skill `networking` (uncertain)

> ...and deploying hardware accelerators in the cloud. - High-speed inter-chip networking experience What We Offer: - A chance to be a foundational...

- A: `networking` · nice_to_have · raw_text: "High-speed inter-chip networking experience"
- B: `networking` · nice_to_have · raw_text: "High-speed inter-chip networking"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_102 - skill `machine-learning` (uncertain)

> ...Robyn and LightweightMMM - Hands-on experience with machine learning frameworks such as scikit-learn, TensorFlow, or PyTorch applied to...

- A: `machine-learning` · nice_to_have · raw_text: "machine learning frameworks"
- B: `machine-learning` · nice_to_have · raw_text: "machine learning frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 63. golden_103 - attribute `degree` (uncertain)

> ...deep learning and/or foundation models — whether through a PhD in ML or equivalent hands-on industry work. You're a curious, agile engineer who can generate ideas,...

- A: value="phd" · requirement="required" · or_equivalent=true · signal="PhD in ML or equivalent hands-on industry work"
- B: value="phd" · requirement="required" · or_equivalent=true · signal="a PhD in ML or equivalent hands-on industry work"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_103 - skill `agent-state-management` (uncertain)

> ...and evaluating both - Agentic systems knowledge — tools, memory, and long-running workflows - Strong software engineering fundamentals — performant,...

- A: `agent-state-management` · required · raw_text: "memory, and long-running workflows"
- B: `agent-state-management` · required · raw_text: "Agentic systems knowledge — tools, memory"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_103 - skill `ai-deployment` (uncertain)

> ...— data preprocessing, model training, evaluation, inference, and deployment - Experience with end-to-end model development — dataset...

- A: `ai-deployment` · required · raw_text: "inference, and deployment"
- B: `ai-deployment` · required · raw_text: "model training, evaluation, inference, and deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_103 - skill `ai-infrastructure` (uncertain)

> ...You’ll Need: - 8 years of industry experience w 4+ years of ML infrastructure experience — data preprocessing, model training, evaluation,...

- A: `ai-infrastructure` · required · raw_text: "4+ years of ML infrastructure experience"
- B: `ai-infrastructure` · required · raw_text: "ML infrastructure experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_103 - skill `aws` (uncertain)

> ...Familiarity with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and collaboration skills...

- A: `aws` · required · raw_text: "AWS"
- B: `aws` · required · raw_text: "AWS"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 68. golden_103 - skill `gcp` (uncertain)

> ...Familiarity with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and collaboration...

- A: `gcp` · required · raw_text: "GCP"
- B: `gcp` · required · raw_text: "GCP"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 69. golden_103 - skill `observability` (uncertain)

> ...— dataset construction, training, fine-tuning, evaluation, profiling, and monitoring - Familiarity with modern model architectures — including...

- A: `observability` · required · raw_text: "profiling, and monitoring"
- B: `observability` · required · raw_text: "monitoring"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_103 - skill `tool-calling` (uncertain)

> ...LLaVA), and experience training and evaluating both - Agentic systems knowledge — tools, memory, and long-running workflows - Strong software...

- A: `tool-calling` · required · raw_text: "Agentic systems knowledge — tools"
- B: `tool-calling` · required · raw_text: "Agentic systems knowledge — tools"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_104 - attribute `degree` (uncertain)

> ...scientists, engineers, and product managers. Preferred - Master’s degree or PhD in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field. - Experience with LLMOps, including model evaluation,...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s degree or PhD in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field."
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Master’s degree or PhD in Computer Science, Engineering, Electronics, Mathematics, or another highly technical field."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_104 - skill `data-privacy-and-security` (uncertain)

> ...large-scale models. - Familiarity with model encryption, privacy-preserving machine learning, and secure AI techniques. Benefits that Benefit You -...

- A: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving machine learning"
- B: `data-privacy-and-security` · nice_to_have · raw_text: "privacy-preserving machine learning, and secure AI techniques"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_105 - skill `ai-developer-tooling` (uncertain)

> ...in production. - Demonstrated, heavy AI-native delivery: consistent use of AI across the SDLC with concrete examples of faster delivery and...

- A: `ai-developer-tooling` · required · raw_text: "consistent use of AI across the SDLC"
- B: `ai-developer-tooling` · required · raw_text: "AI-native delivery: consistent use of AI across the SDLC"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_105 - skill `ai-ml` (uncertain)

> ...0→1→initial scale delivery. - Experience integrating AI/LLM capabilities into product experiences responsibly. - Track record of...

- A: `ai-ml` · nice_to_have · raw_text: "AI/LLM capabilities"
- B: `ai-ml` · nice_to_have · raw_text: "integrating AI/LLM capabilities into product experiences responsibly"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_105 - skill `cloud` (uncertain)

> ...decisions stick. - Experience designing, building, and operating cloud-native systems that scale, including reliability and observability best...

- A: `cloud` · required · raw_text: "operating cloud-native systems that scale"
- B: `cloud` · required · raw_text: "cloud-native systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_106 - skill `ai-infrastructure` (uncertain)

> ...years of professional experience in systems programming, ML infrastructure, or distributed inference. - Proficient in C++ and...

- A: `ai-infrastructure` · required · raw_text: "ML infrastructure"
- B: `ai-infrastructure` · required · raw_text: "ML infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_106 - skill `docker` (uncertain)

> ...workloads. - Familiarity with containerized deployments (Docker/Kubernetes). - Exposure to distributed systems or large-scale...

- A: `docker` · nice_to_have · raw_text: "Docker/Kubernetes"
- B: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_106 - skill `kubernetes` (uncertain)

> ...workloads. - Familiarity with containerized deployments (Docker/Kubernetes). - Exposure to distributed systems or large-scale...

- A: `kubernetes` · nice_to_have · raw_text: "Docker/Kubernetes"
- B: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 79. golden_106 - skill `model-serving` (uncertain)

> ...analysis skills. - Deep familiarity with one or more LLM serving frameworks (vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference, etc.)....

- A: `model-serving` · required · raw_text: "LLM serving frameworks"
- B: `model-serving` · required · raw_text: "LLM serving frameworks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 80. golden_107 - attribute `seniority` (uncertain)

> ...advance state-of-the-art in the generative AI domain. - Define and lead high impact applied research initiatives. - Writing high-quality code, designing and performing...

- A: value="senior" · basis="inferred" · signal="Define and lead high impact applied research initiatives."
- B: value="senior" · basis="inferred" · signal="3+ years of experience leading Machine Learning research initiatives."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 81. golden_107 - skill `docker` (uncertain)

> ...containerization and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a...

- A: `docker` · nice_to_have · raw_text: "Docker"
- B: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 82. golden_107 - skill `kubernetes` (uncertain)

> ...and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a foundational...

- A: `kubernetes` · nice_to_have · raw_text: "Kubernetes"
- B: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 83. golden_107 - skill `machine-learning` (uncertain)

> ...or a related field. - 3+ years of experience leading Machine Learning research initiatives. - Demonstrated history of research with publications in...

- A: `machine-learning` · required · raw_text: "Machine Learning research initiatives"
- B: `machine-learning` · required · raw_text: "Machine Learning research"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 84. golden_108 - attribute `degree` (uncertain)

> ...excellent communications skills. It's A Bonus If You: - Have a Ph. D. in computer or computational science, atmospheric science or a related geophysical science, or...

- A: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Have a Ph. D. in computer or computational science"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Have a Ph. D. in computer or computational science, atmospheric science or a related geophysical science, or applied mathematics/statistics"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 85. golden_108 - attribute `seniority` (uncertain)

> ...to interested user groups. What You’ll Need: - 2-4 years of experience building and deploying a relevant ML application in a...

- A: value="mid" · basis="inferred" · signal="2-4 years of experience"
- B: value="mid" · basis="inferred" · signal="2-4 years of experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 86. golden_108 - skill `cloud` (uncertain)

> ...mathematics/statistics. - Experience in developing ML training code for use in a cloud computing environment. - Demonstrated excellent communications skills. It's A...

- A: `cloud` · required · raw_text: "ML training code for use in a cloud computing environment"
- B: `cloud` · required · raw_text: "cloud computing environment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 87. golden_094 - attribute `german` (spot-check)

> Staff Machine Learning Engineer, Growth

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 88. golden_094 - skill `ai-developer-tooling` (spot-check)

> ...Proficient programming skills in Python and SQL. Power user of AI coding tools. - Exceptional communication skills with the ability to...

- agreed label: `ai-developer-tooling` · required · raw_text: "Power user of AI coding tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 89. golden_094 - skill `forecasting` (spot-check)

> ...learning modeling and statistics, specifically leveraging time series forecasting, probabilistic models, and deep learning models -...

- agreed label: `forecasting` · required · raw_text: "time series forecasting"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 90. golden_095 - attribute `german` (spot-check)

> Senior Software Engineer, AI Agentic Platform

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 91. golden_095 - attribute `seniority` (spot-check)

> Senior Software Engineer, AI Agentic Platform Who we are The real world is the...

- agreed label: value="senior" · basis="stated" · signal="Senior Software Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 92. golden_095 - skill `ai-developer-tooling` (spot-check)

> ...and caching patterns - Demonstrated experience leveraging AI-powered development tools such as Claude Code, GitHub Copilot, or similar agentic...

- agreed label: `ai-developer-tooling` · required · raw_text: "AI-powered development tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 93. golden_095 - skill `autogen` (spot-check)

> ...protocols such as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in microservices...

- agreed label: `autogen` · required · raw_text: "AutoGen"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 94. golden_095 - skill `claude-code` (spot-check)

> ...experience leveraging AI-powered development tools such as Claude Code, GitHub Copilot, or similar agentic coding tools for...

- agreed label: `claude-code` · required · raw_text: "such as Claude Code"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 95. golden_095 - skill `cloud` (spot-check)

> ...architecture, container orchestration (Kubernetes), and cloud platforms (AWS) - Observability and LLMOps expertise, including...

- agreed label: `cloud` · required · raw_text: "cloud platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 96. golden_095 - skill `containerization` (spot-check)

> ...or LlamaIndex - Expertise in microservices architecture, container orchestration (Kubernetes), and cloud platforms (AWS) - Observability...

- agreed label: `containerization` · required · raw_text: "container orchestration"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 97. golden_095 - skill `fine-tuning` (spot-check)

> ...field - Experience building customized agent harnesses, fine-tuning models, or implementing RLHF/RLAIF optimization loops - Security...

- agreed label: `fine-tuning` · nice_to_have · raw_text: "fine-tuning models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 98. golden_095 - skill `google-adk` (spot-check)

> ...frameworks and protocols such as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in microservices...

- agreed label: `google-adk` · required · raw_text: "Google ADK"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 99. golden_095 - skill `java` (spot-check)

> ...+ Frameworks: TypeScript, React, Scala (principally), Java (limited) - Datastores: MySQL, PostgreSQL, Snowflake - Cloud:...

- agreed label: `java` · required · raw_text: "Java (limited)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 100. golden_095 - skill `llamaindex` (spot-check)

> ...as LangGraph, Anthropic MCP, Google ADK, AutoGen, A2A, or LlamaIndex - Expertise in microservices architecture, container...

- agreed label: `llamaindex` · required · raw_text: "LlamaIndex"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 101. golden_095 - skill `llm-orchestration` (spot-check)

> ...experience architecting and deploying agentic AI systems, LLM orchestration frameworks, or AI platform tooling - Strong proficiency in Python or...

- agreed label: `llm-orchestration` · required · raw_text: "LLM orchestration frameworks"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 102. golden_095 - skill `llmops` (spot-check)

> ...and cloud platforms (AWS) - Observability and LLMOps expertise, including metrics, distributed tracing, structured...

- agreed label: `llmops` · required · raw_text: "LLMOps expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 103. golden_095 - skill `observability` (spot-check)

> ...orchestration (Kubernetes), and cloud platforms (AWS) - Observability and LLMOps expertise, including metrics, distributed tracing, structured...

- agreed label: `observability` · required · raw_text: "Observability and LLMOps expertise"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 104. golden_095 - skill `vector-databases` (spot-check)

> ...and data systems knowledge including relational databases, vector databases, event streaming (Kafka, SQS), and caching patterns -...

- agreed label: `vector-databases` · required · raw_text: "vector databases"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 105. golden_096 - skill `argocd` (spot-check)

> ...state (Ansible, Puppet, Salt) and GitOps workflows (Argo CD, Flux). - Experience in OS configuration tooling. -...

- agreed label: `argocd` · required · raw_text: "Argo CD"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 106. golden_096 - skill `gcp` (spot-check)

> ...clusters. - 2–3 years of production experience operating workloads on AWS or GCP. - Proven track record running ML or inference services...

- agreed label: `gcp` · required · raw_text: "operating workloads on AWS or GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 107. golden_096 - skill `gitops` (spot-check)

> ...OS configuration state (Ansible, Puppet, Salt) and GitOps workflows (Argo CD, Flux). - Experience in OS configuration...

- agreed label: `gitops` · required · raw_text: "GitOps workflows"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 108. golden_096 - skill `observability` (spot-check)

> ...accelerators beyond GPUs (FPGAs, custom ASICs). - Background in observability, SRE, or performance engineering for latency-sensitive...

- agreed label: `observability` · nice_to_have · raw_text: "Background in observability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 109. golden_096 - skill `python` (spot-check)

> ...plugins, MIG, networking, and storage considerations. - Solid coding skills in Python, Bash and proficiency in Go - Proficient in configuring...

- agreed label: `python` · required · raw_text: "Solid coding skills in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 110. golden_096 - skill `triton-inference-server` (spot-check)

> ...- Experience with inference servers and runtimes (e.g., Triton, vLLM, TGI) and model-serving patterns (batching,...

- agreed label: `triton-inference-server` · nice_to_have · raw_text: "Triton"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 111. golden_097 - attribute `degree` (spot-check)

> ...our inference solutions. Required Qualifications: - PhD/MS in Computer Science, Computer Engineering, or a related field. - 3+ years of machine learning R&D and deployment...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="PhD/MS in Computer Science, Computer Engineering, or a related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 112. golden_097 - skill `containerization` (spot-check)

> ...cloud platforms (AWS, GCP, Azure). - Experience with containerization and orchestration technologies (e.g., Docker,...

- agreed label: `containerization` · nice_to_have · raw_text: "containerization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 113. golden_097 - skill `cpp` (spot-check)

> ...in one or more programming languages such as Python, or C++. - Proficiency in at least one ML framework (e.g.,...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 114. golden_097 - skill `docker` (spot-check)

> ...containerization and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a...

- agreed label: `docker` · nice_to_have · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 115. golden_097 - skill `kubernetes` (spot-check)

> ...and orchestration technologies (e.g., Docker, Kubernetes). What We Offer: - A chance to be a foundational...

- agreed label: `kubernetes` · nice_to_have · raw_text: "Kubernetes"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 116. golden_097 - skill `nlp` (spot-check)

> ...leading research initiatives in Machine Learning, Natural Language Processing, and related fields. - Familiarity with performance...

- agreed label: `nlp` · nice_to_have · raw_text: "Natural Language Processing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 117. golden_097 - skill `python` (spot-check)

> ...proficiency in one or more programming languages such as Python, or C++. - Proficiency in at least one ML framework...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 118. golden_097 - skill `pytorch` (spot-check)

> ...C++. - Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Solid understanding of software...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 119. golden_097 - skill `tensorflow` (spot-check)

> ...- Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Solid understanding of software engineering...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 120. golden_097 - skill `testing` (spot-check)

> ...best practices, including data structures, algorithms, and testing. - Excellent problem-solving abilities and a knack for...

- agreed label: `testing` · required · raw_text: "testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 121. golden_098 - attribute `german` (spot-check)

> Research Engineer, Robotics - Roboticist

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 122. golden_098 - skill `python` (spot-check)

> ...can reason about latency, reliability and failure modes. Strong Python; solid real-time C++. - Mechanical design: you have...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 123. golden_098 - skill `pytorch` (spot-check)

> ...(imitation learning, RL or VLA) on real robots, and are comfortable with PyTorch and at least one simulation ecosystem (Isaac Lab, MuJoCo...

- agreed label: `pytorch` · required · raw_text: "comfortable with PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 124. golden_099 - skill `python` (spot-check)

> ...frameworks at a systems level. - Strong proficiency in one or more programming languages such as Python and C++. - Strong understanding of one or more of the...

- agreed label: `python` · required · raw_text: "one or more programming languages such as Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 125. golden_099 - skill `testing` (spot-check)

> ...best practices, including data structures, algorithms, and testing. - Thinking in terms of latency, cycles, memory...

- agreed label: `testing` · required · raw_text: "testing"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 126. golden_100 - attribute `german` (spot-check)

> Research Engineer, Robotics: Physics Simulation and Sim-to-Real

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 127. golden_100 - skill `python` (spot-check)

> ...result quantitatively against real-world recordings. - Proficiency in Python and C++, experience with robot description formats (URDF,...

- agreed label: `python` · required · raw_text: "Proficiency in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 128. golden_101 - skill `cloud` (spot-check)

> ...research publications or open-source projects. - Understanding of cloud computing environments and deploying hardware accelerators in the cloud. -...

- agreed label: `cloud` · nice_to_have · raw_text: "Understanding of cloud computing environments"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 129. golden_101 - skill `quantization` (spot-check)

> ...of ML optimization techniques (e.g., sparsity, quantization, pruning). - Proficiency in Verilog or SystemVerilog for...

- agreed label: `quantization` · required · raw_text: "quantization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 130. golden_102 - attribute `degree` (spot-check)

> ...high-output processes What we're looking for - Bachelor’s or Master’s degree in Computer Science, Mathematics, Statistics, Economics, or a related quantitative field - 6+ years of proven experience as a Data Scientist or...

- agreed label: value="master" · requirement="required" · or_equivalent=false · signal="Bachelor’s or Master’s degree in Computer Science, Mathematics, Statistics, Economics, or a related quantitative field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 131. golden_102 - skill `causal-inference` (spot-check)

> ...Hands-on experience with statistical experimentation and causal inference techniques such as A/B testing, geo-testing, synthetic controls, and...

- agreed label: `causal-inference` · required · raw_text: "causal inference techniques"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 132. golden_102 - skill `dbt` (spot-check)

> ...data warehouses and modern data tools such as Snowflake, dbt, Looker, and Tableau - Familiarity with Media Mix...

- agreed label: `dbt` · nice_to_have · raw_text: "dbt"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 133. golden_102 - skill `pytorch` (spot-check)

> ...learning frameworks such as scikit-learn, TensorFlow, or PyTorch applied to user segmentation or churn prediction -...

- agreed label: `pytorch` · nice_to_have · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 134. golden_102 - skill `sagemaker` (spot-check)

> ...Experience with cloud platforms, including AWS S3, SageMaker, and Airflow - Experience with cloud data warehouses and...

- agreed label: `sagemaker` · nice_to_have · raw_text: "SageMaker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 135. golden_102 - skill `scikit-learn` (spot-check)

> ...experience with machine learning frameworks such as scikit-learn, TensorFlow, or PyTorch applied to user segmentation or...

- agreed label: `scikit-learn` · nice_to_have · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 136. golden_102 - skill `sql` (spot-check)

> ...media, or adtech - Advanced proficiency in Python and SQL for complex data manipulation, statistical modeling, and predictive analytics - Deep...

- agreed label: `sql` · required · raw_text: "SQL for complex data manipulation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 137. golden_102 - skill `statistics` (spot-check)

> ...in Python and SQL for complex data manipulation, statistical modeling, and predictive analytics - Deep domain expertise in...

- agreed label: `statistics` · required · raw_text: "statistical modeling"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 138. golden_102 - skill `tableau` (spot-check)

> ...and modern data tools such as Snowflake, dbt, Looker, and Tableau - Familiarity with Media Mix Modeling (MMM) frameworks...

- agreed label: `tableau` · nice_to_have · raw_text: "Tableau"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 139. golden_103 - attribute `seniority` (spot-check)

> Senior Research Engineer, Olmo + Molmo Persons in these roles are expected to work...

- agreed label: value="senior" · basis="stated" · signal="Senior Research Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 140. golden_103 - skill `containerization` (spot-check)

> ...pick up new tools as needed - Familiarity with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and...

- agreed label: `containerization` · required · raw_text: "containerization"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 141. golden_103 - skill `docker` (spot-check)

> ...with cloud and containerization (e.g., GCP, AWS, Docker) - Strong communication and collaboration skills — we're...

- agreed label: `docker` · required · raw_text: "Docker"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 142. golden_103 - skill `evaluation` (spot-check)

> ...of ML infrastructure experience — data preprocessing, model training, evaluation, inference, and deployment - Experience with end-to-end...

- agreed label: `evaluation` · required · raw_text: "model training, evaluation"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 143. golden_103 - skill `fine-tuning` (spot-check)

> ...model development — dataset construction, training, fine-tuning, evaluation, profiling, and monitoring - Familiarity with...

- agreed label: `fine-tuning` · required · raw_text: "fine-tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 144. golden_103 - skill `jax` (spot-check)

> ...Proficiency in Python and a major ML framework (PyTorch, JAX, or TensorFlow), with the flexibility to pick up new tools...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 145. golden_103 - skill `model-development` (spot-check)

> ...evaluation, inference, and deployment - Experience with end-to-end model development — dataset construction, training, fine-tuning, evaluation,...

- agreed label: `model-development` · required · raw_text: "end-to-end model development"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 146. golden_103 - skill `pytorch` (spot-check)

> ...Proficiency in Python and a major ML framework (PyTorch, JAX, or TensorFlow), with the flexibility to pick up new...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 147. golden_104 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer Join Axon and be a Force for Good. At Axon, we’re on a...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 148. golden_104 - skill `cpp` (spot-check)

> ...and infrastructure as code. - Proficiency in Python and C++, with experience using ML frameworks such as PyTorch or...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 149. golden_104 - skill `fine-tuning` (spot-check)

> ...and production deployment. - Hands-on experience fine-tuning and optimizing large-scale models. - Familiarity with model encryption, privacy-preserving...

- agreed label: `fine-tuning` · nice_to_have · raw_text: "fine-tuning and optimizing large-scale models"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

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

DECISION: ?

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

DECISION: ?

## 156. golden_105 - attribute `german` (spot-check)

> Senior Software Engineer, Axon AI

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 157. golden_106 - skill `cpp` (spot-check)

> ...ML infrastructure, or distributed inference. - Proficient in C++ and Python, with strong debugging and performance analysis...

- agreed label: `cpp` · required · raw_text: "Proficient in C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 158. golden_106 - skill `deepspeed` (spot-check)

> ...more LLM serving frameworks (vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference, etc.). - Understanding of model deployment internals —...

- agreed label: `deepspeed` · required · raw_text: "DeepSpeed-Inference"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 159. golden_106 - skill `vllm` (spot-check)

> ...Deep familiarity with one or more LLM serving frameworks (vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference, etc.). - Understanding of model deployment internals —...

- agreed label: `vllm` · required · raw_text: "vLLM, SGLang, TensorRT-LLM, DeepSpeed-Inference"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 160. golden_107 - skill `aws` (spot-check)

> ...techniques. - Experience with cloud platforms (AWS, GCP, Azure). - Experience with containerization and...

- agreed label: `aws` · nice_to_have · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 161. golden_107 - skill `gcp` (spot-check)

> ...techniques. - Experience with cloud platforms (AWS, GCP, Azure). - Experience with containerization and...

- agreed label: `gcp` · nice_to_have · raw_text: "GCP"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 162. golden_107 - skill `jax` (spot-check)

> ...in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Strong proficiency in one or more programming...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 163. golden_107 - skill `python` (spot-check)

> ...proficiency in one or more programming languages such as Python, or C++. - Strong communication skills and a proven...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 164. golden_107 - skill `pytorch` (spot-check)

> ...VLMs. - Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Strong proficiency in one or more...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 165. golden_107 - skill `tensorflow` (spot-check)

> ...- Proficiency in at least one ML framework (e.g., PyTorch, TensorFlow, JAX). - Strong proficiency in one or more programming...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?

## 166. golden_108 - skill `python` (spot-check)

> ...in a practical or academic research setting and be fluent in Python and collaborative coding practices. - A B.Sc. in computer...

- agreed label: `python` · required · raw_text: "fluent in Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ?
