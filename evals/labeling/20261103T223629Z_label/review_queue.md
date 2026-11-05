# Review queue - 20261103T223629Z_label

157 items from 15 postings. Labeler A: `claude-opus-5-5` (anthropic).
Labeler B: `gpt-6.1-sol` (openai). Extractor (not a labeler): `claude-sonnet-5-5`.

Work through every item and replace the `?` on its `DECISION:` line. `scripts/agent_label.py
apply --run 20261103T223629Z_label` refuses while any `?` is left, then writes the Goldens.

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

Spot-check items are a seeded random sample (80 of 137 accepted labels,
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

## 1. golden_049 - scope `in_scope` (in-scope)

> Data Scientist, Proprietary Research

- point72 · Data Scientist, Proprietary Research
- New York · en · greenhouse · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 2. golden_050 - scope `in_scope` (in-scope)

> AI Research Engineer, Inference

- wehrtyou · AI Research Engineer, Inference
- New York · en · greenhouse · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 3. golden_051 - scope `in_scope` (in-scope)

> Software Engineer, Forward Deployed AI Solutions

- ramp · Software Engineer, Forward Deployed AI Solutions
- New York · en · ashby · 18 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 4. golden_052 - scope `in_scope` (in-scope)

> Senior Machine Learning Engineer, Personalization

- spotify · Senior Machine Learning Engineer, Personalization
- New York · en · lever · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 5. golden_053 - scope `in_scope` (in-scope)

> Data Scientist

- ramp · Data Scientist
- New York · en · ashby · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 6. golden_054 - scope `in_scope` (in-scope)

> Research Engineer

- wehrtyou · Research Engineer
- New York · en · greenhouse · 4 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 7. golden_055 - scope `in_scope` (in-scope)

> Applied Scientist Intern

- ramp · Applied Scientist Intern
- New York · en · ashby · 19 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 8. golden_056 - scope `in_scope` (in-scope)

> Machine Learning Researcher - Intern

- point72 · Machine Learning Researcher - Intern
- New York · en · greenhouse · 0 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 9. golden_057 - scope `in_scope` (in-scope)

> Machine Learning Engineer, GenAI Technology

- point72 · Machine Learning Engineer, GenAI Technology
- New York · en · greenhouse · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 10. golden_058 - scope `in_scope` (in-scope)

> Research Engineer, Benchmarks & Evaluation

- ramp · Research Engineer, Benchmarks & Evaluation
- New York · en · ashby · 6 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 11. golden_059 - scope `in_scope` (in-scope)

> Applied AI Engineer

- wehrtyou · Applied AI Engineer
- New York · en · greenhouse · 11 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 12. golden_060 - scope `in_scope` (in-scope)

> Cubist Data Scientist

- point72 · Cubist Data Scientist
- New York · en · greenhouse · 5 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 13. golden_061 - scope `in_scope` (in-scope)

> Quantitative Researcher - Machine Learning

- point72 · Quantitative Researcher - Machine Learning
- New York · en · greenhouse · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 14. golden_062 - scope `in_scope` (in-scope)

> ROLE/RESPONSIBILTIES:

- point72 · NLP Engineer
- New York · en · greenhouse · 8 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 15. golden_063 - scope `in_scope` (in-scope)

> AI Solutions Engineer

- ramp · AI Solutions Engineer
- New York · en · ashby · 2 skills labeled

Options: `yes` (already filled in) / `no <why>` - `no` keeps it out of the Goldens

DECISION: yes

## 16. golden_051 - attribute `seniority` (disagreement)

> ...THE ROLE As a software engineer on the AI Solutions team, you will co-lead customer engagements with an AI Solutions Strategist. The Strategist owns business discovery, ROI narrative,...

- A: value=null · basis=null · signal=null
- B: value="senior" · basis="inferred" · signal="you will co-lead customer engagements with an AI Solutions Strategist."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 17. golden_052 - skill `ai-ml` (disagreement)

> ...learning systems. - You are curious about emerging AI technologies, including large language models and agentic systems, and...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI technologies"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 18. golden_052 - skill `evaluation` (disagreement)

> ...You understand how to design and evaluate experiments, interpret model performance, and translate technical findings into product...

- A: (did not label this)
- B: `evaluation` · required · raw_text: "interpret model performance"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 19. golden_052 - skill `ml-engineering` (disagreement)

> ...within the squad. Who You Are - You have experience building, deploying, and improving machine learning systems in production environments. - You have a strong...

- A: (did not label this)
- B: `ml-engineering` · required · raw_text: "building, deploying, and improving machine learning systems"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 20. golden_053 - skill `data-science` (disagreement)

> ...action WHAT YOU NEED - Minimum of 4 years of industry experience as a Data Scientist - Strong knowledge of SQL (preferably Redshift,...

- A: (did not label this)
- B: `data-science` · required · raw_text: "industry experience as a Data Scientist"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 21. golden_054 - skill `software-engineering` (disagreement)

> ...Research) trading teams. These roles require exceptional programming fundamentals, a strong user focus, and the ability to thrive in a...

- A: (did not label this)
- B: `software-engineering` · required · raw_text: "programming fundamentals"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 22. golden_055 - attribute `degree` (disagreement)

> ...strategy and user-facing features WHAT YOU NEED - B.S., M.S. or Ph.D. Student: currently pursuing a degree in Data Science, Computer...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="B.S., M.S. or Ph.D. Student"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="B.S., M.S. or Ph.D. Student: currently pursuing a degree in Data Science, Computer Science, Math, Physics, Economics, Statistics, or other quantitative fields with an expected graduation date between Dec 2027 - 2029. Graduate degrees are preferred, but not a must."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 23. golden_056 - attribute `degree` (disagreement)

> ...markets and human behavior. DESIRABLE CANDIDATES - Students enrolled in a PhD program in machine learning, computer science, statistics, or a related field. - Superb analytical and quantitative skills, along with...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="Students enrolled in a PhD program in machine learning, computer science, statistics, or a related field"
- B: value="phd" · requirement="nice_to_have" · or_equivalent=false · signal="Students enrolled in a PhD program in machine learning, computer science, statistics, or a related field."

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 24. golden_056 - skill `python` (disagreement)

> ...financial markets - Strong scientific programming in Python, R or Matlab. - Empirical, detail-oriented mindset. -...

- A: `python` · required · raw_text: "Python"
- B: `python` · nice_to_have · raw_text: "Python"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 25. golden_056 - skill `r-lang` (disagreement)

> Machine Learning Researcher - Intern JOB DESCRIPTION Researchers are...

- A: `r-lang` · required · raw_text: "R"
- B: `r-lang` · nice_to_have · raw_text: "R"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 26. golden_057 - skill `ai-ml` (disagreement)

> ...scalable artificial intelligence/machine learning (AI/ML) architectures and systems. Collaborate with data...

- A: (did not label this)
- B: `ai-ml` · required · raw_text: "AI/ML"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 27. golden_058 - skill `llms` (disagreement)

> ...on - Design graders: rubrics, programmatic checks and llm-as-judge, calibrated against human agreement, with a clear...

- A: (did not label this)
- B: `llms` · required · raw_text: "LLM"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 28. golden_059 - skill `software-architecture` (disagreement)

> ...Strong Python proficiency required - Excellent software design, debugging, and problem-solving skills required -...

- A: (did not label this)
- B: `software-architecture` · required · raw_text: "software design"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 29. golden_059 - skill `testing` (disagreement)

> ...infrastructure - Security sandboxing, policy enforcement, adversarial testing, or governance for AI systems - Forward-deployed...

- A: (did not label this)
- B: `testing` · nice_to_have · raw_text: "adversarial testing"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 30. golden_063 - skill `data-privacy-and-security` (disagreement)

> ...helps companies deploy and manage AI with greater control, security, and cost efficiency. This is a product-focused,...

- A: (did not label this)
- B: `data-privacy-and-security` · required · raw_text: "security"

Options: `A` / `B` / `both` / `drop`

DECISION: ?

## 31. golden_049 - attribute `seniority` (uncertain)

> ...tools - Masters/PhD in a quantitative discipline w/ 1+ year of professional experience - Strong programming skills in Python (preferred), R,...

- A: value="junior" · basis="inferred" · signal="1+ year of professional experience"
- B: value="junior" · basis="inferred" · signal="1+ year of professional experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 32. golden_049 - skill `python` (uncertain)

> ...of professional experience - Strong programming skills in Python (preferred), R, Spark, SQL - Exceptional understanding of statistics...

- A: `python` · nice_to_have · raw_text: "Python (preferred)"
- B: `python` · nice_to_have · raw_text: "Python (preferred)"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 33. golden_050 - attribute `seniority` (uncertain)

> ...CUDA Graphs, FPGA/ASIC experience - Must have two or more years work experience building deep learning systems, for any domain: robotics,...

- A: value="junior" · basis="inferred" · signal="two or more years work experience"
- B: value="junior" · basis="inferred" · signal="two or more years work experience"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 34. golden_050 - skill `llms` (uncertain)

> ...methods between areas of application is highly valued - LLM experience is valuable, but not necessary - Finance experience is not required The estimated base...

- A: `llms` · nice_to_have · raw_text: "LLM experience is valuable, but not necessary"
- B: `llms` · nice_to_have · raw_text: "LLM experience is valuable, but not necessary"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 35. golden_051 - skill `ai-deployment` (uncertain)

> ...ML/GenAI, including problem decomposition, evaluation, and deployment trade-offs. - Strong coding ability in at least one of: Python,...

- A: `ai-deployment` · required · raw_text: "deployment trade-offs"
- B: `ai-deployment` · required · raw_text: "deployment trade-offs"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: drop

## 36. golden_051 - skill `software-architecture` (uncertain)

> ...through production implementation. - Experience in solutions architecture, technical consulting, forward deployed engineering, or...

- A: `software-architecture` · required · raw_text: "solutions architecture"
- B: `software-architecture` · required · raw_text: "solutions architecture"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 37. golden_051 - skill `software-engineering` (uncertain)

> ...AI Solutions projects. WHAT YOU NEED - Experience shipping production software in high-ownership environments. - Ability to work...

- A: `software-engineering` · required · raw_text: "shipping production software"
- B: `software-engineering` · required · raw_text: "shipping production software"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 38. golden_052 - skill `agents` (uncertain)

> ...AI technologies, including large language models and agentic systems, and interested in their potential to improve discovery...

- A: `agents` · required · raw_text: "agentic systems"
- B: `agents` · required · raw_text: "agentic systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 39. golden_052 - skill `ai-deployment` (uncertain)

> ...the squad. Who You Are - You have experience building, deploying, and improving machine learning systems in production environments. - You have a strong understanding of...

- A: `ai-deployment` · required · raw_text: "deploying, and improving machine learning systems in production"
- B: `ai-deployment` · required · raw_text: "deploying, and improving machine learning systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 40. golden_052 - skill `llms` (uncertain)

> ...You are curious about emerging AI technologies, including large language models and agentic systems, and interested in their potential to...

- A: `llms` · required · raw_text: "large language models"
- B: `llms` · required · raw_text: "large language models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 41. golden_053 - attribute `seniority` (uncertain)

> ...those insights into action WHAT YOU NEED - Minimum of 4 years of industry experience as a Data Scientist - Strong knowledge of SQL (preferably Redshift,...

- A: value="mid" · basis="inferred" · signal="Minimum of 4 years of industry experience as a Data Scientist"
- B: value="mid" · basis="inferred" · signal="Minimum of 4 years of industry experience as a Data Scientist"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 42. golden_053 - skill `bigquery` (uncertain)

> ...- Strong knowledge of SQL (preferably Redshift, Snowflake, BigQuery) and how to write efficient SQL queries - Familiarity...

- A: `bigquery` · nice_to_have · raw_text: "BigQuery"
- B: `bigquery` · nice_to_have · raw_text: "BigQuery"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 43. golden_053 - skill `snowflake` (uncertain)

> ...as a Data Scientist - Strong knowledge of SQL (preferably Redshift, Snowflake, BigQuery) and how to write efficient SQL queries -...

- A: `snowflake` · nice_to_have · raw_text: "preferably Redshift, Snowflake"
- B: `snowflake` · nice_to_have · raw_text: "Snowflake"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 44. golden_054 - skill `cpp` (uncertain)

> ...etc.) - Candidates should be prepared for technical interviews in either Python or C++. While there is no hard language requirement for RE roles,...

- A: `cpp` · required · raw_text: "interviews in either Python or C++"
- B: `cpp` · required · raw_text: "technical interviews in either Python or C++"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 45. golden_054 - skill `python` (uncertain)

> ...etc.) - Candidates should be prepared for technical interviews in either Python or C++. While there is no hard language requirement for RE roles,...

- A: `python` · required · raw_text: "interviews in either Python or C++"
- B: `python` · required · raw_text: "technical interviews in either Python or C++"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 46. golden_054 - skill `scikit-learn` (uncertain)

> ...ML and data-oriented libraries is a big plus (e.g. pandas, scikit, pytorch, etc.) - Candidates should be prepared for...

- A: `scikit-learn` · nice_to_have · raw_text: "scikit"
- B: `scikit-learn` · nice_to_have · raw_text: "scikit"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 47. golden_055 - skill `ai-ml` (uncertain)

> ...learning, statistics, probability, and optimization - Strong Interest or Experience with AI: curiosity and drive to integrate cutting edge LLMs and...

- A: `ai-ml` · required · raw_text: "Strong Interest or Experience with AI"
- B: `ai-ml` · required · raw_text: "Strong Interest or Experience with AI"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 48. golden_055 - skill `evaluation` (uncertain)

> ...Experience: track record of curating datasets and building/evaluating ML models - Strong Communication: ability to clearly explain...

- A: `evaluation` · required · raw_text: "building/evaluating ML models"
- B: `evaluation` · required · raw_text: "evaluating ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 49. golden_055 - skill `model-development` (uncertain)

> ...Experience: track record of curating datasets and building/evaluating ML models - Strong Communication: ability to clearly explain...

- A: `model-development` · required · raw_text: "building/evaluating ML models"
- B: `model-development` · required · raw_text: "building/evaluating ML models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 50. golden_057 - attribute `seniority` (uncertain)

> ...in computer science, engineering, or a related field. 3-7 years of experience in AI/ML engineering, with a proven track record of...

- A: value="mid" · basis="inferred" · signal="3-7 years of experience"
- B: value="mid" · basis="inferred" · signal="3-7 years of experience in AI/ML engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 51. golden_057 - skill `machine-learning` (uncertain)

> ...record of successful project delivery. Strong expertise in machine learning frameworks and libraries, such as TensorFlow, PyTorch, and/or...

- A: `machine-learning` · required · raw_text: "machine learning frameworks and libraries"
- B: `machine-learning` · required · raw_text: "machine learning frameworks and libraries"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 52. golden_057 - skill `ml-engineering` (uncertain)

> ...or a related field. 3-7 years of experience in AI/ML engineering, with a proven track record of successful project...

- A: `ml-engineering` · required · raw_text: "AI/ML engineering"
- B: `ml-engineering` · required · raw_text: "AI/ML engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 53. golden_058 - skill `agents` (uncertain)

> ...team - Built RL environments or verifiers for agentic tasks - Published benchmark or evaluation research (NeurIPS...

- A: `agents` · nice_to_have · raw_text: "agentic tasks"
- B: `agents` · nice_to_have · raw_text: "agentic tasks"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 54. golden_058 - skill `fine-tuning` (uncertain)

> ...a delta is noise - Working knowledge of post-training (SFT, RL with verifiable rewards) and how evals feed into it...

- A: `fine-tuning` · required · raw_text: "SFT"
- B: `fine-tuning` · required · raw_text: "SFT"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 55. golden_059 - skill `ai-ml` (uncertain)

> ...and operating substantial software systems required - Demonstrated engagement with modern AI systems, tools, or research required Experience in one or more of...

- A: `ai-ml` · required · raw_text: "Demonstrated engagement with modern AI systems"
- B: `ai-ml` · required · raw_text: "modern AI systems, tools, or research"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 56. golden_059 - skill `evaluation` (uncertain)

> ...fine-tuning, reinforcement learning, or alignment - AI-agent architecture, evaluation, or tool-use environments - Distributed systems, model...

- A: `evaluation` · nice_to_have · raw_text: "AI-agent architecture, evaluation"
- B: `evaluation` · nice_to_have · raw_text: "evaluation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 57. golden_059 - skill `ml-engineering` (uncertain)

> ...in one or more of the following is helpful: - Machine learning research or engineering, including post-training, fine-tuning, reinforcement...

- A: `ml-engineering` · nice_to_have · raw_text: "Machine learning research or engineering"
- B: `ml-engineering` · nice_to_have · raw_text: "Machine learning research or engineering"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 58. golden_059 - skill `software-engineering` (uncertain)

> ...and problem-solving skills required - Experience building and operating substantial software systems required - Demonstrated engagement with modern AI...

- A: `software-engineering` · required · raw_text: "building and operating substantial software systems"
- B: `software-engineering` · required · raw_text: "building and operating substantial software systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 59. golden_059 - skill `tool-calling` (uncertain)

> ...or alignment - AI-agent architecture, evaluation, or tool-use environments - Distributed systems, model serving, orchestration, or...

- A: `tool-calling` · nice_to_have · raw_text: "tool-use environments"
- B: `tool-calling` · nice_to_have · raw_text: "tool-use environments"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 60. golden_061 - attribute `degree` (uncertain)

> ...identify emerging opportunities. DESIRABLE CANDIDATES: - Master’s or PhD in machine learning, computer science, statistics, or related fields. - Knowledge and experience in any of the following areas...

- A: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s or PhD in machine learning, computer science, statistics, or related fields"
- B: value="phd" · requirement="required" · or_equivalent=false · signal="Master’s or PhD in machine learning, computer science, statistics, or related fields."

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 61. golden_061 - skill `git` (uncertain)

> ...environment, and general software engineering principles (source control, testing, collaborative workflow). - Excellent written...

- A: `git` · required · raw_text: "source control"
- B: `git` · required · raw_text: "source control"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 62. golden_061 - skill `jax` (uncertain)

> ...proficiency in machine learning libraries such as Torch, JAX or TensorFlow. - Competence in Python, cluster...

- A: `jax` · required · raw_text: "JAX"
- B: `jax` · required · raw_text: "JAX"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 63. golden_061 - skill `machine-learning` (uncertain)

> ...reinforcement learning, LLMs. - Prior research experience utilizing machine learning over large, possibly noisy, data sets. - Strong...

- A: `machine-learning` · required · raw_text: "utilizing machine learning"
- B: `machine-learning` · required · raw_text: "Prior research experience utilizing machine learning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 64. golden_061 - skill `python` (uncertain)

> ...such as Torch, JAX or TensorFlow. - Competence in Python, cluster environment, and general software engineering...

- A: `python` · required · raw_text: "Python"
- B: `python` · required · raw_text: "Python"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 65. golden_061 - skill `pytorch` (uncertain)

> ...Strong proficiency in machine learning libraries such as Torch, JAX or TensorFlow. - Competence in Python, cluster...

- A: `pytorch` · required · raw_text: "Torch"
- B: `pytorch` · required · raw_text: "Torch"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 66. golden_061 - skill `software-engineering` (uncertain)

> ...Competence in Python, cluster environment, and general software engineering principles (source control, testing, collaborative workflow). -...

- A: `software-engineering` · required · raw_text: "general software engineering principles"
- B: `software-engineering` · required · raw_text: "software engineering principles"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 67. golden_061 - skill `tensorflow` (uncertain)

> ...in machine learning libraries such as Torch, JAX or TensorFlow. - Competence in Python, cluster environment, and general...

- A: `tensorflow` · required · raw_text: "TensorFlow"
- B: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 68. golden_061 - skill `testing` (uncertain)

> ...general software engineering principles (source control, testing, collaborative workflow). - Excellent written and verbal...

- A: `testing` · required · raw_text: "testing"
- B: `testing` · required · raw_text: "testing"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ok

## 69. golden_062 - skill `agents` (uncertain)

> ...modern NLP solutions, including the use of LLMs, agents, RAG, open-source models fine-tuning and deployment,...

- A: `agents` · required · raw_text: "agents"
- B: `agents` · required · raw_text: "agents"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 70. golden_062 - skill `ai-deployment` (uncertain)

> ...including the use of LLMs, agents, RAG, open-source models fine-tuning and deployment, etc. Responsibilities include: - Exploring and...

- A: `ai-deployment` · required · raw_text: "fine-tuning and deployment"
- B: `ai-deployment` · required · raw_text: "deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 71. golden_062 - skill `fine-tuning` (uncertain)

> ...including the use of LLMs, agents, RAG, open-source models fine-tuning and deployment, etc. Responsibilities include: -...

- A: `fine-tuning` · required · raw_text: "fine-tuning"
- B: `fine-tuning` · required · raw_text: "fine-tuning"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 72. golden_062 - skill `open-source-llms` (uncertain)

> ...NLP solutions, including the use of LLMs, agents, RAG, open-source models fine-tuning and deployment, etc. Responsibilities...

- A: `open-source-llms` · required · raw_text: "open-source models"
- B: `open-source-llms` · required · raw_text: "open-source models"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 73. golden_062 - skill `rag` (uncertain)

> ...modern NLP solutions, including the use of LLMs, agents, RAG, open-source models fine-tuning and deployment,...

- A: `rag` · required · raw_text: "RAG"
- B: `rag` · required · raw_text: "RAG"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 74. golden_063 - skill `ai-deployment` (uncertain)

> ...model routing, usage controls, data governance, or enterprise AI deployment. - Experience selling to developers, IT, Security,...

- A: `ai-deployment` · nice_to_have · raw_text: "enterprise AI deployment"
- B: `ai-deployment` · nice_to_have · raw_text: "enterprise AI deployment"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 75. golden_063 - skill `ai-infrastructure` (uncertain)

> ...motion rather than simply inherit one. NICE TO HAVE - Experience selling AI infrastructure, AI applications or agents, developer tools, data...

- A: `ai-infrastructure` · nice_to_have · raw_text: "Experience selling AI infrastructure"
- B: `ai-infrastructure` · nice_to_have · raw_text: "AI infrastructure"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 76. golden_063 - skill `ai-ml` (uncertain)

> ...ownership of deal strategy, momentum, and results. - Technical fluency across modern AI systems, including applications and agents, model capabilities and...

- A: `ai-ml` · required · raw_text: "Technical fluency across modern AI systems"
- B: `ai-ml` · required · raw_text: "Technical fluency across modern AI systems"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 77. golden_063 - skill `workflow-automation` (uncertain)

> ...data platforms, security products, finance technology, or workflow automation software. - Experience helping launch a new product or develop an...

- A: `workflow-automation` · nice_to_have · raw_text: "workflow automation software"
- B: `workflow-automation` · nice_to_have · raw_text: "workflow automation"

Options: `ok` (keep as agreed) / `A` / `B` / `drop`

DECISION: ?

## 78. golden_049 - attribute `degree` (spot-check)

> ...learning, statistical models, and data mining tools - Masters/PhD in a quantitative discipline w/ 1+ year of professional experience - Strong...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="Masters/PhD in a quantitative discipline"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 79. golden_049 - attribute `german` (spot-check)

> Data Scientist, Proprietary Research

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 80. golden_050 - attribute `degree` (spot-check)

> AI Research Engineer, Inference

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 81. golden_050 - attribute `german` (spot-check)

> AI Research Engineer, Inference

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 82. golden_050 - skill `cuda` (spot-check)

> ...Strong engineering skills, especially any of: CUDA/Triton/Pallas/CuTe DSL kernel development, lower-level...

- agreed label: `cuda` · required · raw_text: "CUDA"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 83. golden_050 - skill `deep-learning` (spot-check)

> ...experience - Must have two or more years work experience building deep learning systems, for any domain: robotics, biology, chemistry, physics,...

- agreed label: `deep-learning` · required · raw_text: "building deep learning systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 84. golden_050 - skill `jax` (spot-check)

> ...DSL kernel development, lower-level PyTorch/JAX/XLA development, CUDA Graphs, FPGA/ASIC experience - Must...

- agreed label: `jax` · required · raw_text: "JAX"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 85. golden_050 - skill `pytorch` (spot-check)

> ...DSL kernel development, lower-level PyTorch/JAX/XLA development, CUDA Graphs, FPGA/ASIC experience -...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 86. golden_051 - attribute `degree` (spot-check)

> Software Engineer, Forward Deployed AI Solutions

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 87. golden_051 - skill `aws` (spot-check)

> ...infrastructure. - Experience with cloud architecture on AWS, GCP, or Azure, and distributed systems patterns. -...

- agreed label: `aws` · required · raw_text: "AWS"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 88. golden_051 - skill `azure` (spot-check)

> ...- Experience with cloud architecture on AWS, GCP, or Azure, and distributed systems patterns. - Experience building...

- agreed label: `azure` · required · raw_text: "Azure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 89. golden_051 - skill `cloud` (spot-check)

> ...APIs, integrations, data pipelines, customer systems, and cloud infrastructure. - Experience with cloud architecture on AWS, GCP, or...

- agreed label: `cloud` · required · raw_text: "cloud infrastructure"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 90. golden_051 - skill `go` (spot-check)

> ...in at least one of: Python, TypeScript/JavaScript, Java, Go, or similar. - Ability to design secure, scalable systems and...

- agreed label: `go` · required · raw_text: "Go, or similar"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 91. golden_051 - skill `javascript` (spot-check)

> ...coding ability in at least one of: Python, TypeScript/JavaScript, Java, Go, or similar. - Ability to design secure,...

- agreed label: `javascript` · required · raw_text: "JavaScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 92. golden_051 - skill `llms` (spot-check)

> ...and distributed systems patterns. - Experience building LLM systems, including RAG, agents, monitoring, and evals. -...

- agreed label: `llms` · required · raw_text: "LLM systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 93. golden_051 - skill `machine-learning` (spot-check)

> ...or pre-sales engineering. - Strong fundamentals in ML/GenAI, including problem decomposition, evaluation, and...

- agreed label: `machine-learning` · required · raw_text: "ML/GenAI"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 94. golden_051 - skill `python` (spot-check)

> ...trade-offs. - Strong coding ability in at least one of: Python, TypeScript/JavaScript, Java, Go, or similar. - Ability...

- agreed label: `python` · required · raw_text: "Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 95. golden_051 - skill `rag` (spot-check)

> ...alerting, incident response, and runbooks - Leverage core Ramp primitives to build efficiently, reusing...

- agreed label: `rag` · required · raw_text: "RAG"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 96. golden_051 - skill `typescript` (spot-check)

> ...- Strong coding ability in at least one of: Python, TypeScript/JavaScript, Java, Go, or similar. - Ability to design...

- agreed label: `typescript` · required · raw_text: "TypeScript"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 97. golden_052 - attribute `degree` (spot-check)

> Senior Machine Learning Engineer, Personalization

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 98. golden_052 - attribute `seniority` (spot-check)

> Senior Machine Learning Engineer, Personalization The Personalization team makes deciding...

- agreed label: value="senior" · basis="stated" · signal="Senior Machine Learning Engineer"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 99. golden_052 - skill `backend-development` (spot-check)

> ...tools. - You have experience and a desire to lean into backend engineering at Spotify scale. - You understand how to design and...

- agreed label: `backend-development` · required · raw_text: "backend engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 100. golden_052 - skill `recommender-systems` (spot-check)

> ...approaches for information retrieval, search ranking, recommendation systems, or personalization. - You are proficient in Python and...

- agreed label: `recommender-systems` · required · raw_text: "recommendation systems"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 101. golden_053 - attribute `degree` (spot-check)

> Data Scientist

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 102. golden_053 - attribute `german` (spot-check)

> Data Scientist

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 103. golden_053 - skill `business-intelligence` (spot-check)

> ...how to write efficient SQL queries - Familiarity with BI tools (preferably Looker, Omni, Sigma, Hex or equivalent) and...

- agreed label: `business-intelligence` · required · raw_text: "BI tools"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 104. golden_053 - skill `git` (spot-check)

> ...on analytics engineering development cycle (data modeling, version control, documentation + testing, best practices for codebase...

- agreed label: `git` · nice_to_have · raw_text: "version control"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 105. golden_054 - skill `deep-learning` (spot-check)

> ...real hands-on experience with quant research and/or ML/Deep Learning platforms. - Experience with python numerical, ML and data-oriented...

- agreed label: `deep-learning` · nice_to_have · raw_text: "Deep Learning platforms"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 106. golden_055 - attribute `german` (spot-check)

> Applied Scientist Intern

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 107. golden_055 - attribute `seniority` (spot-check)

> Applied Scientist Intern ABOUT RAMP Ramp is building the smart infrastructure for...

- agreed label: value="junior" · basis="stated" · signal="Applied Scientist Intern"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 108. golden_055 - skill `agents` (spot-check)

> ...AI: curiosity and drive to integrate cutting edge LLMs and agents into applied solutions - Python Proficiency: good grasp of common Data Science...

- agreed label: `agents` · required · raw_text: "agents into applied solutions"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 109. golden_055 - skill `dagster` (spot-check)

> ...leveraging modern data orchestration platforms (Airflow, Dagster, Prefect, Metaflow) COMPENSATION - The monthly rate...

- agreed label: `dagster` · nice_to_have · raw_text: "Dagster"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 110. golden_055 - skill `git` (spot-check)

> ...engineering best practices applied to ML including version control (Git), testing, and writing maintainable code - Data...

- agreed label: `git` · nice_to_have · raw_text: "version control (Git)"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 111. golden_055 - skill `llms` (spot-check)

> ...Interest or Experience with AI: curiosity and drive to integrate cutting edge LLMs and agents into applied solutions - Python Proficiency:...

- agreed label: `llms` · required · raw_text: "integrate cutting edge LLMs"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 112. golden_055 - skill `machine-learning` (spot-check)

> ...ML Fundamentals: solid understanding of the mathematical foundations of machine learning, statistics, probability, and optimization - Strong...

- agreed label: `machine-learning` · required · raw_text: "foundations of machine learning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 113. golden_055 - skill `metaflow` (spot-check)

> ...data orchestration platforms (Airflow, Dagster, Prefect, Metaflow) COMPENSATION - The monthly rate for this...

- agreed label: `metaflow` · nice_to_have · raw_text: "Metaflow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 114. golden_055 - skill `numpy` (spot-check)

> ...of common Data Science libraries (pandas, scikit-learn, NumPy, PyTorch, etc.) - SQL Knowledge: experience wrangling...

- agreed label: `numpy` · required · raw_text: "NumPy"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 115. golden_055 - skill `pandas` (spot-check)

> ...Proficiency: good grasp of common Data Science libraries (pandas, scikit-learn, NumPy, PyTorch, etc.) - SQL Knowledge:...

- agreed label: `pandas` · required · raw_text: "pandas"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 116. golden_055 - skill `python` (spot-check)

> ...cutting edge LLMs and agents into applied solutions - Python Proficiency: good grasp of common Data Science libraries (pandas,...

- agreed label: `python` · required · raw_text: "Python Proficiency"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 117. golden_055 - skill `pytorch` (spot-check)

> ...Data Science libraries (pandas, scikit-learn, NumPy, PyTorch, etc.) - SQL Knowledge: experience wrangling data in a...

- agreed label: `pytorch` · required · raw_text: "PyTorch"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 118. golden_055 - skill `scikit-learn` (spot-check)

> ...good grasp of common Data Science libraries (pandas, scikit-learn, NumPy, PyTorch, etc.) - SQL Knowledge: experience...

- agreed label: `scikit-learn` · required · raw_text: "scikit-learn"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 119. golden_055 - skill `snowflake` (spot-check)

> ...experience wrangling data in a modern data warehouse (e.g. Snowflake, BigQuery, Redshift, Clickhouse) - Practical Experience:...

- agreed label: `snowflake` · required · raw_text: "Snowflake"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 120. golden_055 - skill `software-engineering` (spot-check)

> ...for the field - Production ML Mindset: knowledge of software engineering best practices applied to ML including version control (Git), testing,...

- agreed label: `software-engineering` · nice_to_have · raw_text: "software engineering best practices"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 121. golden_055 - skill `statistics` (spot-check)

> ...of the mathematical foundations of machine learning, statistics, probability, and optimization - Strong Interest or Experience with...

- agreed label: `statistics` · required · raw_text: "statistics, probability"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 122. golden_056 - attribute `seniority` (spot-check)

> Machine Learning Researcher - Intern JOB DESCRIPTION Researchers are responsible for...

- agreed label: value="junior" · basis="stated" · signal="Intern"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 123. golden_057 - attribute `degree` (spot-check)

> ...standards and best practices in AI/ML. What’s required Bachelor's or master's degree in computer science, engineering, or a related field. 3-7 years of experience in AI/ML engineering, with a...

- agreed label: value="master" · requirement="required" · or_equivalent=false · signal="Bachelor's or master's degree in computer science, engineering, or a related field"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 124. golden_057 - attribute `german` (spot-check)

> Machine Learning Engineer, GenAI Technology

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 125. golden_057 - skill `cpp` (spot-check)

> ...in programming languages such as Python, Java, or C++. Excellent problem-solving skills with the ability to work...

- agreed label: `cpp` · required · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 126. golden_057 - skill `java` (spot-check)

> ...in programming languages such as Python, Java, or C++. Excellent problem-solving skills with the ability...

- agreed label: `java` · required · raw_text: "Java"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 127. golden_057 - skill `tensorflow` (spot-check)

> ...in machine learning frameworks and libraries, such as TensorFlow, PyTorch, and/or Scikit-learn. Proficiency in programming...

- agreed label: `tensorflow` · required · raw_text: "TensorFlow"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 128. golden_058 - attribute `german` (spot-check)

> Research Engineer, Benchmarks & Evaluation

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 129. golden_058 - attribute `seniority` (spot-check)

> Research Engineer, Benchmarks & Evaluation

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 130. golden_058 - skill `python` (spot-check)

> ...or evals that people used to make real decisions - Strong Python and software engineering; your eval code is reproducible...

- agreed label: `python` · required · raw_text: "Strong Python"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 131. golden_058 - skill `reinforcement-learning` (spot-check)

> ...is noise - Working knowledge of post-training (SFT, RL with verifiable rewards) and how evals feed into it - Comfort with SQL and large...

- agreed label: `reinforcement-learning` · required · raw_text: "RL with verifiable rewards"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 132. golden_058 - skill `software-engineering` (spot-check)

> ...people used to make real decisions - Strong Python and software engineering; your eval code is reproducible and fast - Statistical...

- agreed label: `software-engineering` · required · raw_text: "software engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 133. golden_058 - skill `sql` (spot-check)

> ...rewards) and how evals feed into it - Comfort with SQL and large datasets; you'll work directly from production...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 134. golden_059 - attribute `german` (spot-check)

> Applied AI Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 135. golden_059 - attribute `seniority` (spot-check)

> Applied AI Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 136. golden_059 - skill `agent-architecture` (spot-check)

> ...fine-tuning, reinforcement learning, or alignment - AI-agent architecture, evaluation, or tool-use environments - Distributed...

- agreed label: `agent-architecture` · nice_to_have · raw_text: "AI-agent architecture"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 137. golden_059 - skill `cpp` (spot-check)

> ...capabilities - Linux, systems performance, networking, C++, or TypeScript The estimated base salary range for this...

- agreed label: `cpp` · nice_to_have · raw_text: "C++"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 138. golden_059 - skill `fine-tuning` (spot-check)

> ...learning research or engineering, including post-training, fine-tuning, reinforcement learning, or alignment - AI-agent...

- agreed label: `fine-tuning` · nice_to_have · raw_text: "fine-tuning"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 139. golden_059 - skill `linux` (spot-check)

> ...to discover, build, and operationalize new capabilities - Linux, systems performance, networking, C++, or TypeScript The...

- agreed label: `linux` · nice_to_have · raw_text: "Linux"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 140. golden_059 - skill `machine-learning` (spot-check)

> ...in one or more of the following is helpful: - Machine learning research or engineering, including post-training, fine-tuning,...

- agreed label: `machine-learning` · nice_to_have · raw_text: "Machine learning research"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 141. golden_059 - skill `python` (spot-check)

> ...field, or equivalent practical experience required - Strong Python proficiency required - Excellent software design, debugging, and...

- agreed label: `python` · required · raw_text: "Strong Python proficiency"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 142. golden_059 - skill `reinforcement-learning` (spot-check)

> ...or engineering, including post-training, fine-tuning, reinforcement learning, or alignment - AI-agent architecture, evaluation, or tool-use...

- agreed label: `reinforcement-learning` · nice_to_have · raw_text: "reinforcement learning, or alignment"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 143. golden_060 - attribute `degree` (spot-check)

> ...to be shared with investment teams REQUIREMENTS - Masters in Financial Engineering, Statistics, Computer Science or other disciplines involving rigorous quantitative analysis - Strong programming skills in Python and SQL -...

- agreed label: value="master" · requirement="required" · or_equivalent=false · signal="Masters in Financial Engineering, Statistics, Computer Science or other disciplines involving rigorous quantitative analysis"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 144. golden_060 - attribute `seniority` (spot-check)

> Cubist Data Scientist

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 145. golden_060 - skill `linux` (spot-check)

> ...skills in Python and SQL - Experience working with AWS, Linux and Airflow preferred but not required - Financial...

- agreed label: `linux` · nice_to_have · raw_text: "Linux"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 146. golden_060 - skill `sql` (spot-check)

> ...analysis - Strong programming skills in Python and SQL - Experience working with AWS, Linux and Airflow...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 147. golden_061 - attribute `german` (spot-check)

> Quantitative Researcher - Machine Learning

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 148. golden_061 - attribute `seniority` (spot-check)

> Quantitative Researcher - Machine Learning

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 149. golden_062 - attribute `degree` (spot-check)

> ...philosophy and direct portfolio impact. REQUIREMENTS: - Bachelor, Master’s or PhD graduate or candidate in computer science or another quantitative discipline - Experience in NLP, particularly LLMs. - Proficient in...

- agreed label: value="phd" · requirement="required" · or_equivalent=false · signal="Bachelor, Master’s or PhD graduate or candidate in computer science or another quantitative discipline"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 150. golden_062 - attribute `german` (spot-check)

> ROLE/RESPONSIBILTIES:

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 151. golden_062 - skill `data-science` (spot-check)

> ...software engineering principles (github, testing, etc.) - Data science stack familiarity - Interest in financial markets -...

- agreed label: `data-science` · required · raw_text: "Data science stack"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 152. golden_062 - skill `software-engineering` (spot-check)

> ...NLP, particularly LLMs. - Proficient in Python, SQL and general software engineering principles (github, testing, etc.) - Data science stack...

- agreed label: `software-engineering` · required · raw_text: "general software engineering principles"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 153. golden_062 - skill `sql` (spot-check)

> ...in NLP, particularly LLMs. - Proficient in Python, SQL and general software engineering principles (github,...

- agreed label: `sql` · required · raw_text: "SQL"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 154. golden_063 - attribute `degree` (spot-check)

> AI Solutions Engineer

- agreed label: value=null · requirement=null · or_equivalent=false · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 155. golden_063 - attribute `german` (spot-check)

> AI Solutions Engineer

- agreed label: value=null · basis=null · signal=null

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 156. golden_063 - attribute `seniority` (spot-check)

> ...motion from the ground up. WHAT YOU’LL BRING - 5+ years of experience in Solutions Engineering, Solutions Consulting, technical sales, Solutions...

- agreed label: value="senior" · basis="inferred" · signal="5+ years of experience in Solutions Engineering"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok

## 157. golden_063 - skill `agents` (spot-check)

> ...results. - Technical fluency across modern AI systems, including applications and agents, model capabilities and limitations, APIs, integrations,...

- agreed label: `agents` · required · raw_text: "including applications and agents"

Options: `ok` (correct) / `drop` (not a real label) / JSON (what it should be)

DECISION: ok
