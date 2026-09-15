# Awesome Agent Evolution Papers

<div align="center">

A daily collection of papers on **Agent/LLM self-evolution, self-improving systems, and recursive self-improvement**, **agent memory**, and **LLM continual training**,
powered by AstrBot.

The bot resumes from its last successful delivery after downtime, prioritizes
verified industry-affiliated work (especially first authors), and marks explicit
top-conference or top-journal publications without promoting under-review claims.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![AstrBot](https://img.shields.io/badge/AstrBot-4.26+-76bad9)
![Update](https://img.shields.io/badge/update-daily-brightgreen)

</div>

## 🚀 Quick Start

See [Deployment Guide](docs/deployment.md) to install the AstrBot plugin,
configure an enterprise WeChat group webhook, and enable GitHub sync.

## 📊 Statistics

| Metric | Count |
| --- | ---: |
| Total papers | 67 |
| Agent/LLM self-evolution & self-improvement | 35 |
| Agent memory | 31 |
| LLM continual training | 15 |
| Daily archives | 7 |

## 📚 Table of Contents

- [Highlighted Papers](#highlighted-papers)
- [Monthly Index](#monthly-index)
- [Latest Papers](#latest-papers)
- [Daily Archive](#daily-archive)
- [Dataset](data/papers.json)
- [Curation Policy](docs/curation.md)
- [Literature Audit](allinone.md)
- [Deployment Guide](docs/deployment.md)

## 🌟 Highlighted Papers

> Every listed paper is topic-relevant and has at least one verified qualifier: CCF-A (AI), ECCV/EMNLP, big-tech affiliation, or high citation count.

| Paper | Published | Venue | Why it matters | Metrics |
| --- | --- | --- | --- | --- |
| [Retrieval-Augmented LLM Agents: Learning to Learn from Experience](https://arxiv.org/abs/2603.18272v2) | 2026-03-18 | EMNLP 2026 | 🚨 First-author industry profile: NAVER<br>🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 5 (Semantic Scholar) |
| [A Programming Paradigm for Spatiotemporal Composability](https://arxiv.org/abs/2608.25512v1) | 2026-08-26 | arXiv | 🚨 First-author industry affiliation: DeepSeek | Citations: 7 (Semantic Scholar) |
| [FinEvo-Bench: A Longitudinal Benchmark for Self-Evolving Agents in Professional Financial Workflows](https://arxiv.org/abs/2608.06144v1) | 2026-08-06 | arXiv | 🚨 First-author industry affiliation: Alibaba | Citations: 1 (Semantic Scholar) |
| [Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents](https://arxiv.org/abs/2601.01885) | 2026-01-05 | ACL 2026 (Main) | 📈 Highly cited<br>🏢 Industry: Alibaba Group<br>🏆 CCF-A: ACL 2026 (Main) | [GitHub ★ 33](https://github.com/y1y5/AgeMem)<br>Citations: 75 (Google Scholar) |
| [MCCE: A Framework for Multi-LLM Collaborative Search in Discrete Spaces with Similarity-Filtered Preference Learning](https://arxiv.org/abs/2510.06270v2) | 2025-10-06 | ICML 2026 | 🏆 CCF-A: ICML 2026 | Citations: 1 (Semantic Scholar) |
| [Diffract: Spectral View of LLM Domain Adaptation](https://arxiv.org/abs/2608.10850v1) | 2026-08-11 | ICML 2026 | 🏆 CCF-A: ICML 2026 | Citations: 0 (Semantic Scholar) |
| [DiffuseAgent-MI: Distributionally-Grounded,Tool-Integrated Self-Evolving Agents for Faithful Visual Reasoning](https://arxiv.org/abs/2608.00540v1) | 2026-08-01 | ICML 2026 | 🏆 CCF-A: ICML 2026 | Citations: 0 (Semantic Scholar) |
| [SLoRA: Balancing Plasticity and Forgetting in Large Language Models for Continual Learning](https://aclanthology.org/2026.acl-long.247/) | 2026-07-01 | ACL 2026 (Main) | 🏆 CCF-A: ACL 2026 (Main) | [GitHub ★ 0](https://github.com/alina1031/SLoRA) |
| [Mem$^2$Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation](https://arxiv.org/abs/2604.10923) | 2026-04-13 | ACL 2026 (Main) | 🏆 CCF-A: ACL 2026 (Main) | [GitHub ★ 1](https://github.com/BUAA-IRIP-LLM/Mem2Evolve)<br>Citations: 9 (Google Scholar) |
| [CoMAP: Co-Evolving World Models and Agent Policies for LLM Agents](https://arxiv.org/abs/2606.02372v2) | 2026-06-01 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 3 (Semantic Scholar) |
| [DynaTokens: Controlling Token Dynamics for Continual Video-Language Understanding](https://arxiv.org/abs/2603.06662v3) | 2026-03-02 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 3 (Semantic Scholar) |
| [PEAR: Permutation-Equivariant Adaptive Routing Multi-Agent Debate](https://arxiv.org/abs/2606.20621v2) | 2026-05-26 | EMNLP | 🏅 ECCV / EMNLP: EMNLP | Citations: 0 (Semantic Scholar) |
| [KItCAT: Knowledge Injection via Input Corruption for Auto-regressive Training](https://arxiv.org/abs/2609.00082v1) | 2026-08-31 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [Seeing the Unseen: Visual Similarity for Pixel Language Model Adaptation](https://arxiv.org/abs/2608.30541v1) | 2026-08-31 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [EvoSkill Injection: Red-Teaming Autonomous Skill Generation and Evolution in Self-Evolving Agents](https://arxiv.org/abs/2608.30429v1) | 2026-08-31 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [DMV-Bench: Diagnosing Long-Horizon Multimodal Agents' Visual Memory with Incidental Cue Injection](https://arxiv.org/abs/2606.27499v2) | 2026-06-25 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | [GitHub ★ 3](https://github.com/yyyujintang/DMV-Bench)<br>Citations: 0 (Semantic Scholar) |
| [Counter with Evidence! A Multi-Agent Memory Efficient Reasoning Framework for Hate Category Informed Counterspeech Generation](https://arxiv.org/abs/2608.23152v3) | 2026-08-24 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [SIC-Agents: Benchmarking and Building an Adaptive Simulator for Pediatric Serious Illness Communication Training](https://arxiv.org/abs/2608.29481v1) | 2026-08-30 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [E2Rank: Unifying Text Embedding and Listwise Reranking for Effective and Efficient Search](https://arxiv.org/abs/2510.22733v3) | 2025-10-26 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 3 (Semantic Scholar) |
| [Learning What to Share and What to Personalize: Hierarchical Strategy Co-Evolution for Agent Memory](https://arxiv.org/abs/2608.25329v1) | 2026-08-26 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [Time is Not a Label: Continuous Phase Rotation for Temporal Knowledge Graphs and Agentic Memory](https://arxiv.org/abs/2604.11544v2) | 2026-04-13 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 3 (Semantic Scholar) |
| [SSE-Bio: A Structured Self-Evolving Agent with Agentic Retrieval Policy for Multi-Hop Biomedical Reasoning](https://arxiv.org/abs/2608.22132v1) | 2026-08-22 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [MemWM: Memory-Augmented Text-Based World Model](https://arxiv.org/abs/2608.07107v2) | 2026-08-07 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 0 (Semantic Scholar) |
| [GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents](https://arxiv.org/abs/2605.29668v3) | 2026-05-28 | EMNLP 2026 | 🏅 ECCV / EMNLP: EMNLP 2026 | Citations: 6 (Semantic Scholar) |
| [VDC-Agent: When Video Detailed Captioners Evolve Themselves via Agentic Self-Reflection](https://arxiv.org/abs/2511.19436v2) | 2025-11-24 | ECCV 2026 | 🏅 ECCV / EMNLP: ECCV 2026 | Citations: 4 (Semantic Scholar) |
| [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://arxiv.org/abs/2605.23904) | 2026-05-22 | arXiv | 🔥 Very popular code<br>📈 Highly cited<br>🏢 Industry: Microsoft Research | [GitHub ★ 15,927](https://github.com/microsoft/SkillOpt)<br>Citations: 37 (Google Scholar) |
| [Hyperagents](https://arxiv.org/abs/2603.19461) | 2026-03-19 | arXiv | 🔥 Very popular code<br>📈 Highly cited<br>🏢 Industry: Meta | [GitHub ★ 2,675](https://github.com/facebookresearch/HyperAgents)<br>Citations: 33 (Google Scholar) |
| [How Do Large Language Models Learn Concepts During Continual Pre-Training?](https://arxiv.org/abs/2601.03570v2) | 2026-01-07 | arXiv.org | 🏢 Industry: Meta | Citations: 3 (Semantic Scholar) |
| [Skill Self-Play: Pushing the Frontier of LLM Capability with Co-Evolving Skills](https://arxiv.org/abs/2607.22529) | 2026-07-24 | arXiv.org | ⭐ Popular code<br>🏢 Industry: Alibaba / Qwen | [GitHub ★ 119](https://github.com/Qwen-Applications/skill-self-play)<br>Citations: 1 (Semantic Scholar) |
| [CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery](https://arxiv.org/abs/2604.01658v3) | 2026-04-02 | arXiv.org | 📈 Highly cited | Citations: 33 (Semantic Scholar) |
| [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](https://arxiv.org/abs/2607.08448v4) | 2026-07-09 | arXiv.org | 📈 Highly cited | Citations: 11 (Semantic Scholar) |
| [SinLlama -- A Large Language Model for Sinhala](https://arxiv.org/abs/2508.09115v5) | 2025-08-12 | Moratuwa Engineering Research Conference | 📈 Highly cited | Citations: 10 (Semantic Scholar) |
| [Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978v2) | 2026-05-13 | arXiv.org | 📈 Highly cited | Citations: 10 (Semantic Scholar) |
| [MemGUI-Bench: Benchmarking Memory of Mobile GUI Agents in Dynamic Environments](https://arxiv.org/abs/2602.06075v3) | 2026-02-03 | arXiv.org | 📈 Highly cited | Citations: 15 (Semantic Scholar) |
| [MemMark: State-Evolution Attribution Watermarking for Agent Long-Term Memory Systems](https://arxiv.org/abs/2605.25002v4) | 2026-05-24 | arXiv.org | 📈 Highly cited | Citations: 15 (Semantic Scholar) |
| [Towards general embodied intelligence: integrating large language models, knowledge bases, and reasoning capabilities to build the next generation of AI agents](https://arxiv.org/abs/2608.19794v1) | 2026-08-20 | International Journal of Hydromechatronics | 📈 Highly cited | Citations: 10 (Semantic Scholar) |
| [A Systematic Survey on Large Language Models for Evolutionary Optimization: From Modeling to Solving](https://arxiv.org/abs/2509.08269v7) | 2025-09-10 | IEEE Computational Intelligence Magazine | 📈 Highly cited | Citations: 15 (Semantic Scholar) |
| [FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery](https://arxiv.org/abs/2602.14670v2) | 2026-02-16 | Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 | 📈 Highly cited | Citations: 13 (Semantic Scholar) |
| [CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification](https://arxiv.org/abs/2604.01687v3) | 2026-04-02 | COLM | 📈 Highly cited | Citations: 94 (Semantic Scholar) |
| [REMAC: Self-Reflective and Self-Evolving Multi-Agent Collaboration for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2503.22122v2) | 2025-03-28 | Pattern Recognition | 📈 Highly cited | Citations: 11 (Semantic Scholar) |
| [WebChoreArena: Evaluating Web Browsing Agents on Realistic Tedious Web Tasks](https://arxiv.org/abs/2506.01952v2) | 2025-06-02 | arXiv.org | 📈 Highly cited | Citations: 28 (Semantic Scholar) |
| [Self-Distillation Enables Continual Learning](https://arxiv.org/abs/2601.19897v2) | 2026-01-27 | arXiv.org | 📈 Highly cited | Citations: 169 (Semantic Scholar) |
| [Memory in the LLM Era: Modular Architectures and Strategies in a Unified Framework](https://arxiv.org/abs/2604.01707v3) | 2026-04-02 | arXiv.org | 📈 Highly cited | Citations: 12 (Semantic Scholar) |
| [SkillMOO: Multi-Objective Optimization of Agent Skills for Software Engineering](https://arxiv.org/abs/2604.09297v3) | 2026-04-10 | arXiv.org | 📈 Highly cited | Citations: 11 (Semantic Scholar) |
| [Contextual Agentic Memory is a Memo, Not True Memory](https://arxiv.org/abs/2604.27707v2) | 2026-04-30 | arXiv.org | 📈 Highly cited | Citations: 12 (Semantic Scholar) |
| [A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents](https://arxiv.org/abs/2602.06052v4) | 2026-01-14 | TMLR | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 183](https://github.com/AgentMemoryWorld/Awesome-Agent-Memory)<br>Citations: 35 (Semantic Scholar) |
| [Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents](https://arxiv.org/abs/2602.10226v3) | 2026-02-10 | arXiv.org | 📈 Highly cited | Citations: 19 (Semantic Scholar) |
| [Continual Learning for VLMs: A Survey and Taxonomy Beyond Forgetting](https://arxiv.org/abs/2508.04227v3) | 2025-08-06 | arXiv.org | 📈 Highly cited | Citations: 21 (Semantic Scholar) |
| [Library Drift: Diagnosing and Fixing a Silent Failure Mode in Self-Evolving LLM Skill Libraries](https://arxiv.org/abs/2605.19576v3) | 2026-05-19 | arXiv.org | 📈 Highly cited | [GitHub ★ 2](https://github.com/amazon-science/Self-Evolving-Agents-Ratchet)<br>Citations: 10 (Semantic Scholar) |
| [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227) | 2026-07-14 | arXiv.org | 📈 Highly cited | Citations: 18 (Semantic Scholar) |
| [Danus: Orchestrating Mathematical Reasoning Agents with Fact-Graph Memory](https://arxiv.org/abs/2607.06447) | 2026-07-07 | arXiv.org | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 167](https://github.com/frenzymath/Danus)<br>Citations: 13 (Semantic Scholar) |
| [MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation](https://arxiv.org/abs/2605.27366) | 2026-05-26 | arXiv.org | 📈 Highly cited | Citations: 18 (Semantic Scholar) |
| [Toward Efficient Agents: Memory, Tool learning, and Planning](https://arxiv.org/abs/2601.14192) | 2026-01-20 | arXiv.org | 📈 Highly cited | Citations: 10 (Semantic Scholar) |
| [MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents](https://arxiv.org/abs/2602.02474) | 2026-02-02 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 560](https://github.com/ViktorAxelsen/MemSkill)<br>Citations: 22 (Google Scholar) |
| [Anatomy of Agentic Memory: Taxonomy and Empirical Analysis of Evaluation and System Limitations](https://arxiv.org/abs/2602.19320) | 2026-02-22 | arXiv | 📈 Highly cited | Citations: 21 (Google Scholar) |
| [Beyond RAG for Agent Memory: Retrieval by Decoupling and Aggregation](https://arxiv.org/abs/2602.02007) | 2026-02-02 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 119](https://github.com/HU-xiaobai/xMemory)<br>Citations: 17 (Google Scholar) |
| [TiMem: Temporal-Hierarchical Memory Consolidation for Long-Horizon Conversational Agents](https://arxiv.org/abs/2601.02845) | 2026-01-06 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 169](https://github.com/TiMEM-AI/timem)<br>Citations: 15 (Google Scholar) |
| [RISE: Self-Improving Robot Policy with Compositional World Model](https://arxiv.org/abs/2602.11075) | 2026-02-11 | RSS 2026 | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 338](https://github.com/OpenDriveLab/RISE)<br>Citations: 23 (Google Scholar) |
| [MAGMA: A Multi-Graph based Agentic Memory Architecture for AI Agents](https://arxiv.org/abs/2601.03236) | 2026-01-06 | arXiv | 📈 Highly cited | Citations: 43 (Google Scholar) |
| [Omni-SimpleMem: Autoresearch-Guided Discovery of Lifelong Multimodal Agent Memory](https://arxiv.org/abs/2604.01007) | 2026-04-01 | arXiv | 🔥 Very popular code<br>📈 Highly cited | [GitHub ★ 3,687](https://github.com/aiming-lab/SimpleMem)<br>Citations: 10 (Google Scholar) |
| [Memento-Skills: Let Agents Design Agents](https://arxiv.org/abs/2603.18743) | 2026-03-19 | arXiv | 🔥 Very popular code<br>📈 Highly cited | [GitHub ★ 1,541](https://github.com/Memento-Teams/Memento-Skills)<br>Citations: 36 (Google Scholar) |
| [Controlled Self-Evolution for Algorithmic Code Optimization](https://arxiv.org/abs/2601.07348) | 2026-01-12 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 131](https://github.com/QuantaAlpha/EvoControl)<br>Citations: 10 (Google Scholar) |
| [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/abs/2601.03192) | 2026-01-06 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 166](https://github.com/MemTensor/MemRL)<br>Citations: 70 (Google Scholar) |
| [SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning](https://arxiv.org/abs/2602.08234) | 2026-02-09 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 937](https://github.com/aiming-lab/SkillRL)<br>Citations: 131 (Google Scholar) |
| [PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents](https://arxiv.org/abs/2603.03296) | 2026-02-06 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 284](https://github.com/TIMAN-group/PlugMem)<br>Citations: 15 (Google Scholar) |
| [Graph-based Agent Memory: Taxonomy, Techniques, and Applications](https://arxiv.org/abs/2602.05665) | 2026-02-05 | arXiv | ⭐ Popular code<br>📈 Highly cited | [GitHub ★ 332](https://github.com/DEEP-PolyU/Awesome-GraphMemory)<br>Citations: 31 (Google Scholar) |
| [SimpleMem: Efficient Lifelong Memory for LLM Agents](https://arxiv.org/abs/2601.02553) | 2026-01-05 | arXiv | 🔥 Very popular code<br>📈 Highly cited | [GitHub ★ 3,687](https://github.com/aiming-lab/SimpleMem)<br>Citations: 18 (Google Scholar) |

## 🗓️ Monthly Index

| Month | Papers | Agent/LLM Self-Improvement | Memory | Continual Training |
| --- | ---: | ---: | ---: | ---: |
| [2025-03](papers/2025/03/README.md) | 1 | 1 | 0 | 0 |
| [2025-06](papers/2025/06/README.md) | 1 | 0 | 1 | 0 |
| [2025-08](papers/2025/08/README.md) | 2 | 0 | 0 | 2 |
| [2025-09](papers/2025/09/README.md) | 1 | 1 | 0 | 0 |
| [2025-10](papers/2025/10/README.md) | 2 | 1 | 0 | 2 |
| [2025-11](papers/2025/11/README.md) | 1 | 1 | 0 | 0 |
| [2026-01](papers/2026/01/README.md) | 10 | 3 | 7 | 3 |
| [2026-02](papers/2026/02/README.md) | 10 | 6 | 7 | 0 |
| [2026-03](papers/2026/03/README.md) | 4 | 1 | 2 | 2 |
| [2026-04](papers/2026/04/README.md) | 8 | 5 | 5 | 1 |
| [2026-05](papers/2026/05/README.md) | 7 | 6 | 3 | 0 |
| [2026-06](papers/2026/06/README.md) | 2 | 1 | 1 | 0 |
| [2026-07](papers/2026/07/README.md) | 5 | 2 | 2 | 1 |
| [2026-08](papers/2026/08/README.md) | 13 | 7 | 3 | 4 |
| [2026-09](papers/2026/09/README.md) | 0 | 0 | 0 | 0 |

## 📝 Latest Papers

| Published | Track | Paper | Links |
| --- | --- | --- | --- |
| 2026-08-31 | LLM Continual Training & Continual Learning | [KItCAT: Knowledge Injection via Input Corruption for Auto-regressive Training](https://arxiv.org/abs/2609.00082v1) | [Paper](https://arxiv.org/abs/2609.00082v1) / [PDF](https://arxiv.org/pdf/2609.00082v1) |
| 2026-08-31 | LLM Continual Training & Continual Learning | [Seeing the Unseen: Visual Similarity for Pixel Language Model Adaptation](https://arxiv.org/abs/2608.30541v1) | [Paper](https://arxiv.org/abs/2608.30541v1) / [PDF](https://arxiv.org/pdf/2608.30541v1) |
| 2026-08-31 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [EvoSkill Injection: Red-Teaming Autonomous Skill Generation and Evolution in Self-Evolving Agents](https://arxiv.org/abs/2608.30429v1) | [Paper](https://arxiv.org/abs/2608.30429v1) / [PDF](https://arxiv.org/pdf/2608.30429v1) |
| 2026-08-30 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [SIC-Agents: Benchmarking and Building an Adaptive Simulator for Pediatric Serious Illness Communication Training](https://arxiv.org/abs/2608.29481v1) | [Paper](https://arxiv.org/abs/2608.29481v1) / [PDF](https://arxiv.org/pdf/2608.29481v1) |
| 2026-08-26 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [A Programming Paradigm for Spatiotemporal Composability](https://arxiv.org/abs/2608.25512v1) | [Paper](https://arxiv.org/abs/2608.25512v1) / [PDF](https://arxiv.org/pdf/2608.25512v1) |
| 2026-08-26 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement, Agent Memory | [Learning What to Share and What to Personalize: Hierarchical Strategy Co-Evolution for Agent Memory](https://arxiv.org/abs/2608.25329v1) | [Paper](https://arxiv.org/abs/2608.25329v1) / [PDF](https://arxiv.org/pdf/2608.25329v1) |
| 2026-08-24 | Agent Memory | [Counter with Evidence! A Multi-Agent Memory Efficient Reasoning Framework for Hate Category Informed Counterspeech Generation](https://arxiv.org/abs/2608.23152v3) | [Paper](https://arxiv.org/abs/2608.23152v3) / [PDF](https://arxiv.org/pdf/2608.23152v3) |
| 2026-08-22 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [SSE-Bio: A Structured Self-Evolving Agent with Agentic Retrieval Policy for Multi-Hop Biomedical Reasoning](https://arxiv.org/abs/2608.22132v1) | [Paper](https://arxiv.org/abs/2608.22132v1) / [PDF](https://arxiv.org/pdf/2608.22132v1) |
| 2026-08-20 | LLM Continual Training & Continual Learning | [Towards general embodied intelligence: integrating large language models, knowledge bases, and reasoning capabilities to build the next generation of AI agents](https://arxiv.org/abs/2608.19794v1) | [Paper](https://arxiv.org/abs/2608.19794v1) / [PDF](https://arxiv.org/pdf/2608.19794v1) |
| 2026-08-11 | LLM Continual Training & Continual Learning | [Diffract: Spectral View of LLM Domain Adaptation](https://arxiv.org/abs/2608.10850v1) | [Paper](https://arxiv.org/abs/2608.10850v1) / [PDF](https://arxiv.org/pdf/2608.10850v1) |
| 2026-08-07 | Agent Memory | [MemWM: Memory-Augmented Text-Based World Model](https://arxiv.org/abs/2608.07107v2) | [Paper](https://arxiv.org/abs/2608.07107v2) / [PDF](https://arxiv.org/pdf/2608.07107v2) |
| 2026-08-06 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [FinEvo-Bench: A Longitudinal Benchmark for Self-Evolving Agents in Professional Financial Workflows](https://arxiv.org/abs/2608.06144v1) | [Paper](https://arxiv.org/abs/2608.06144v1) / [PDF](https://arxiv.org/pdf/2608.06144v1) |
| 2026-08-01 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [DiffuseAgent-MI: Distributionally-Grounded,Tool-Integrated Self-Evolving Agents for Faithful Visual Reasoning](https://arxiv.org/abs/2608.00540v1) | [Paper](https://arxiv.org/abs/2608.00540v1) / [PDF](https://arxiv.org/pdf/2608.00540v1) |
| 2026-07-24 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [Skill Self-Play: Pushing the Frontier of LLM Capability with Co-Evolving Skills](https://arxiv.org/abs/2607.22529) | [Paper](https://arxiv.org/abs/2607.22529) / [PDF](https://arxiv.org/pdf/2607.22529) |
| 2026-07-14 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227) | [Paper](https://arxiv.org/abs/2607.12227) / [PDF](https://arxiv.org/pdf/2607.12227) |
| 2026-07-09 | Agent Memory | [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](https://arxiv.org/abs/2607.08448v4) | [Paper](https://arxiv.org/abs/2607.08448v4) / [PDF](https://arxiv.org/pdf/2607.08448v4) |
| 2026-07-07 | Agent Memory | [Danus: Orchestrating Mathematical Reasoning Agents with Fact-Graph Memory](https://arxiv.org/abs/2607.06447) | [Paper](https://arxiv.org/abs/2607.06447) / [PDF](https://arxiv.org/pdf/2607.06447) |
| 2026-07-01 | LLM Continual Training & Continual Learning | [SLoRA: Balancing Plasticity and Forgetting in Large Language Models for Continual Learning](https://aclanthology.org/2026.acl-long.247/) | [Paper](https://aclanthology.org/2026.acl-long.247/) / [PDF](https://aclanthology.org/2026.acl-long.247.pdf) |
| 2026-06-25 | Agent Memory | [DMV-Bench: Diagnosing Long-Horizon Multimodal Agents' Visual Memory with Incidental Cue Injection](https://arxiv.org/abs/2606.27499v2) | [Paper](https://arxiv.org/abs/2606.27499v2) / [PDF](https://arxiv.org/pdf/2606.27499v2) |
| 2026-06-01 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [CoMAP: Co-Evolving World Models and Agent Policies for LLM Agents](https://arxiv.org/abs/2606.02372v2) | [Paper](https://arxiv.org/abs/2606.02372v2) / [PDF](https://arxiv.org/pdf/2606.02372v2) |
| 2026-05-28 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents](https://arxiv.org/abs/2605.29668v3) | [Paper](https://arxiv.org/abs/2605.29668v3) / [PDF](https://arxiv.org/pdf/2605.29668v3) |
| 2026-05-26 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [PEAR: Permutation-Equivariant Adaptive Routing Multi-Agent Debate](https://arxiv.org/abs/2606.20621v2) | [Paper](https://arxiv.org/abs/2606.20621v2) / [PDF](https://arxiv.org/pdf/2606.20621v2) |
| 2026-05-26 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement, Agent Memory | [MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation](https://arxiv.org/abs/2605.27366) | [Paper](https://arxiv.org/abs/2605.27366) / [PDF](https://arxiv.org/pdf/2605.27366) |
| 2026-05-24 | Agent Memory | [MemMark: State-Evolution Attribution Watermarking for Agent Long-Term Memory Systems](https://arxiv.org/abs/2605.25002v4) | [Paper](https://arxiv.org/abs/2605.25002v4) / [PDF](https://arxiv.org/pdf/2605.25002v4) |
| 2026-05-22 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://arxiv.org/abs/2605.23904) | [Paper](https://arxiv.org/abs/2605.23904) / [PDF](https://arxiv.org/pdf/2605.23904) |
| 2026-05-19 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement | [Library Drift: Diagnosing and Fixing a Silent Failure Mode in Self-Evolving LLM Skill Libraries](https://arxiv.org/abs/2605.19576v3) | [Paper](https://arxiv.org/abs/2605.19576v3) / [PDF](https://arxiv.org/pdf/2605.19576v3) |
| 2026-05-13 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement, Agent Memory | [Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978v2) | [Paper](https://arxiv.org/abs/2605.12978v2) / [PDF](https://arxiv.org/pdf/2605.12978v2) |
| 2026-04-30 | Agent Memory | [Contextual Agentic Memory is a Memo, Not True Memory](https://arxiv.org/abs/2604.27707v2) | [Paper](https://arxiv.org/abs/2604.27707v2) / [PDF](https://arxiv.org/pdf/2604.27707v2) |
| 2026-04-13 | Agent Memory | [Time is Not a Label: Continuous Phase Rotation for Temporal Knowledge Graphs and Agentic Memory](https://arxiv.org/abs/2604.11544v2) | [Paper](https://arxiv.org/abs/2604.11544v2) / [PDF](https://arxiv.org/pdf/2604.11544v2) |
| 2026-04-13 | Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement, Agent Memory | [Mem$^2$Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation](https://arxiv.org/abs/2604.10923) | [Paper](https://arxiv.org/abs/2604.10923) / [PDF](https://arxiv.org/pdf/2604.10923) |

## 🗓️ Daily Archive

- [2026-09-12](papers/2026/09/2026-09-12.md)
- [2026-09-10](papers/2026/09/2026-09-10.md)
- [2026-09-09](papers/2026/09/2026-09-09.md)
- [2026-09-05](papers/2026/09/2026-09-05.md)
- [2026-08-25](papers/2026/08/2026-08-25.md)
- [2026-07-28](papers/2026/07/2026-07-28.md)
- [2026-07-16](papers/2026/07/2026-07-16.md)

## 🔎 Scope and Verification

- **Agent & LLM Self-Evolution:** self-evolving, self-improving, recursive self-improvement, self-refinement, self-feedback reinforcement, and co-evolving agents or language models
- **Agent Memory:** long-term, memory-augmented, and persistent agent memory
- **LLM Continual Training:** continual pre/post-training, lifelong and online adaptation, retention, and catastrophic-forgetting mitigation
- **Public inclusion:** topic relevance plus CCF-A (AI), ECCV/EMNLP, verified big-tech affiliation, or at least 10 citations
- **Conference papers:** only Full/Regular main-track papers qualify by venue; Findings, workshop, demo, and short papers do not
- **Code stars:** displayed as context but never qualify a paper by themselves
- **Industry / venue:** marked only when supported by publication metadata, the paper, a publisher, or an official project page
- Missing metrics are shown as `n/a`, never guessed. Stars and citations are time-sensitive snapshots.

## License

Code is released under the MIT License. Paper metadata remains subject to its source terms.
