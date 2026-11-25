# Labeling run 20261125T135346Z_label

- labeler A: `claude-opus-5-5` (anthropic); labeler B: `gpt-6.1-sol` (openai)
- extractor (excluded as a labeler): `claude-haiku-5-5`; taxonomy v14
- postings picked 15, labeled by both 15, failed 0

## Labeler agreement (A as reference)

- skills: precision 0.924, recall 0.985, F1 0.954 (tp 257, B-only 21, A-only 4)
- requirement, on ids both gave: 0.981
- seniority: 0.800 (12/15)
- german: 1.000 (15/15)
- degree: 1.000 (15/15)

## Merge

- accepted on agreement: 208 skills, 37 attributes
- review queue: 32 disagreement, 15 in-scope, 80 spot-check, 49 uncertain
- spot-check: 80 of 245 accepted labels, seed 0

Agreed value, different quoted signal (A's kept):
- golden_149 seniority: A 'Applications Development Senior Programmer Analyst' vs B 'Senior Programmer Analyst'
- golden_151 seniority: A 'Als Private AI Architect (w/m/x)' vs B 'Private AI Architect'
- golden_152 seniority: A '7-10+ years in data engineering, analytics platforms or AI data roles' vs B '7-10+ years in data engineering, analytics platforms or AI data roles within large or complex organizations.'
- golden_154 seniority: A '(Junior) Forward Deployed Engineer' vs B '(Junior)'
- golden_158 degree: A 'Master’s or Bachelor’s degree in Computer Science' vs B 'Master’s or Bachelor’s degree in Computer Science, Statistics, Machine Learning, or a related quantitative field.'

No taxonomy entry fits (a taxonomy gap, never a Golden label):
- AI cost optimization, AI for robotics, AI safety, AI workload performance, scalability and availability optimization, Anthropic Console, Anthropic implementation guidance, Authentication concepts, CLIP, CMDB, Camera calibration, Chunking, CircleCI, Claude, Claude Chat and Cowork, Claude models, Cloud-native application development, Cloud-native applications, Container and Kubernetes configuration, Container and Kubernetes scheduling, Container and Kubernetes storage, Continuous evaluation pipelines, Continuous training pipelines, Coordinate transformations, Cosmos, DINOv2, DSPy, DVC, Data curation, Data exchange patterns, Data governance and compliance controls, Data integration, Data platforms, Data readiness assessments, Data transformation, Dataset versioning, DeepSeek, Demonstration data collection, Deployment on NVIDIA embedded platforms, Developer tooling, Dex-Net, Diffusion models, Diffusion policies, Distributed Inference, Distributed compute, Distributed computing, Distributed inference, Document analysis, Drift Detection, Drift detection, End-to-end learned models for robotics, Enterprise integrations, Enterprise knowledge workflows, Enterprise tool ecosystem integration, EtherCAT, Feature stores, Flow Designer, GPT, GPU drivers, GPU infrastructure, GPU memory management, Gazebo, GenAI application optimisation, Grasp generation, GraspNet, Hallucination mitigation, Hand-eye calibration, Hands-on operation of real robotic hardware, Haystack, Human oversight, Hybrid environments, Identity federation, Imitation learning, Infrastructure automation, Infrastructure reliability, Infrastructure troubleshooting, IntegrationHub, Isaac Lab, Isaac Sim, KV caching, Knowledge management, Large-scale demonstration data collection, Learned grasp generation, Llama, MIG (Multi-Instance GPU), ML infrastructure, Mistral, Modern data platforms, MuJoCo, Multi-GPU computing, NVIDIA AGX, NVIDIA GPU computing, NVIDIA Isaac Lab, NVIDIA Isaac Sim, NVIDIA Isaac Sim/Lab, NVIDIA Jetson / embedded platforms, NVIDIA Jetson Orin, NVIDIA MIG, NVIDIA Stack, NVIDIA Xavier, NVIDIA stack, Now Assist, OPC UA, Object-oriented programming, Ollama, Omniverse, On-premises environments, Open-source contribution, PCL, PCL (Point Cloud Library), PLCs, Penetration testing, Pipeline debugging, Point cloud processing, Private AI, Problem decomposition, Product engineering, Production support, Prompt and version management, Qwen, Real robot hardware experience, Responsible AI, Robot forward and inverse kinematics, Robot kinematics, Robot learning simulation frameworks, Robotics, SAM, SAM (Segment Anything), SciPy, Scripting, Secure cloud deployment practices, Security tooling, Self-supervised learning, Self-supervised vision backbones, ServiceNow, ServiceNow AI Agents, ServiceNow development and configuration, ServiceNow scripting, ServiceNow workflow and task tables, Sim-to-real transfer, Simulation, Software deployment to production, Solutions architecture, Sovereign AI, Storage, Structured outputs, Synthetic data, Systems and enterprise integration, TGI, Technical consulting involving AI system development or deployment, Teleoperation, Teleoperation setups, Text2SQL, Token usage, Virtual Agent, Vision-Language-Action models, World models, YOLO, data governance, data integration, data readiness assessments, enterprise tool ecosystem integration, feature stores, modern data platforms, multi-GPU jobs, vectorization
