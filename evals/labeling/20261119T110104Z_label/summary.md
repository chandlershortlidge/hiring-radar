# Labeling run 20261119T110104Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-sonnet-5-5`; taxonomy v11
- postings picked 9, labeled by both 9, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.943, recall 0.983, F1 0.963 (tp 116, B-only 7, A-only 2)
- requirement, on ids both gave: 0.983
- seniority: 1.000 (9/9)
- german: 1.000 (9/9)
- degree: 1.000 (9/9)

## Merge

- accepted on agreement: 88 skills, 26 attributes
- review queue: 11 disagreement, 9 in-scope, 80 spot-check, 27 uncertain
- spot-check: 80 of 114 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_097 degree: A 'PhD in a quantitative field (statistics, computer science, applied mathematics, computational biology, physics, or related) with a strong research track record, or equivalent demonstrated expertise' vs B 'PhD in a quantitative field (statistics, computer science, applied mathematics, computational biology, physics, or related) with a strong research track record, or equivalent demonstrated expertise with 5+ years of experience post PhD.'
- golden_098 seniority: A 'Principal Scientist' vs B 'Principal Scientist, Machine Learning'
- golden_098 degree: A 'Master’s, or PhD in a relevant field' vs B 'Master’s, or PhD in a relevant field (e.g., machine learning, mathematics, statistics, computational sciences)'
- golden_099 degree: A 'Ph.D. in machine learning, computational chemistry, chemical physics, computer science, applied mathematics, or a related discipline' vs B 'Ph.D.\xa0in machine learning, computational chemistry, chemical physics, computer science, applied mathematics, or a related discipline with 2+ years of industry experience, or M.S. degree with 6+ years of industry experience'
- golden_100 degree: A 'PhD, MS, or equivalent experience' vs B 'PhD, MS, or equivalent experience in computational biology, machine learning, bioengineering, computer science, systems biology, quantitative biology, translational science, or a related field.'
- golden_102 degree: A 'PhD in machine learning, computational science, Earth science, atmospheric science, hydrology, AI, computer science, or a related quantitative discipline' vs B 'PhD in machine learning, computational science, Earth science, atmospheric science, hydrology, AI, computer science, or a related quantitative discipline.'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- ADMET, AI cost governance / FinOps, AWS Batch, AWS CDK, AWS ECS, AWS EKS, Active learning, Agent harness development, Agreement analysis, Algorithm design and implementation, Amazon Redshift, Argo, Argo Workflows, Autoscaling, Bayesian model comparison and weighting, Bayesian modeling / Bayesian model comparison, Biological foundation models, Biophysics/molecular dynamics, Chromophore decomposition, Cost governance / FinOps, DFT, DGL, DVC, Data assimilation, Data cleaning, Data contract design, Data contracts, Data contracts and lineage, Data curation, Data integration, Data lineage, Data warehouses, Databases, Density functional theory, DiffDock, Diffusion models, Diffusion theory, Docking, Docking pipelines, Docking rescoring, Durable retries, Electronic structure methods, Endpoint selection, Equivariant architectures, Evolutionary programming, Feedback-loop frameworks, FinOps / cost governance, Flow models, FlowNet-9 architecture, Gaussian, Generative modeling, Generative modeling (diffusion/flow/VAEs), Generative models (molecular), Genetic/evolutionary algorithms, Genomic foundation models, Gradio, Graph neural networks, Human study methodology, Hybrid physics-ML methods, IRB-governed protocols, Idempotency, Image registration, Imaging, Individual baseline and temporal change modeling, Informatics software, LakeFS, Large-scale computational experimentation, Large-scale computational infrastructure for ML training, Longitudinal study designs, ML systems, Mass spectrometry, Measurement calibration, Measurement sampling, Modern ML frameworks, Molecular design modeling, Molecular design models, Molecular docking / ADMET, Molecular dynamics, Molecular modeling, Molecular representation, Monte Carlo simulation, Multimodal modeling, ORCA, Parallel/distributed computation, Parallel/distributed execution, Population-based search, Pose quality metrics, Post-training, Probabilistic programming, Protein design, Protein language models, Protein modeling, Protein modeling/design, Proteomics/mass spec, PyTorch Geometric, Q-Chem, Quality-diversity methods, Quantum chemistry, Reaction modeling, Redshift, Reference measurements, Remote sensing data, Replay, Representation learning, SDK design, Sandboxed code execution, Scalable data processing, Scientific ML, Scientific data analysis, Scientific discovery platforms, Signal processing, Spatiotemporal modeling, Stateful execution, Structure-based design, Variational autoencoders, Within-subject study designs, Workflow orchestration, Workflow orchestration (durable execution), gnina
