# Awesome Agent Evolution Papers

<div align="center">

A daily collection of papers on **agent self-evolution**, **agent memory**,
and **LLM continual training**, powered by AstrBot.

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
| Total papers | 837 |
| Agent self-evolving | 250 |
| Agent memory | 548 |
| LLM continual training | 95 |
| Daily archives | 3 |

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

> Signals are independently verified. A paper is highlighted when it has popular code, strong citation traction, an industry affiliation, or a top-venue publication.

| Paper | Published | Venue | Why it matters | Metrics |
| --- | --- | --- | --- | --- |
| [FinEvo-Bench: A Longitudinal Benchmark for Self-Evolving Agents in Professional Financial Workflows](https://arxiv.org/abs/2608.06144v1) | 2026-08-06 | arXiv | 🚨 First-author industry affiliation: Alibaba | — |
| [Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents](https://arxiv.org/abs/2601.01885) | 2026-01-05 | ACL 2026 (Main) | 📈 Highly cited<br>🏢 Industry: Alibaba Group<br>🏆 Top venue: ACL 2026 (Main) | [GitHub ★ 33](https://github.com/y1y5/AgeMem)<br>Citations: 75 (Google Scholar) |
| [InjecMEM: Memory Injection Attack on LLM Agent Memory Systems](https://arxiv.org/abs/2608.23471v1) | 2026-08-24 | COLM 2026 | 🏆 Top venue: COLM 2026 | — |
| [SSE-Bio: A Structured Self-Evolving Agent with Agentic Retrieval Policy for Multi-Hop Biomedical Reasoning](https://arxiv.org/abs/2608.22132v1) | 2026-08-22 | EMNLP 2026 | 🏆 Top venue: EMNLP 2026 | — |
| [MemWM: Memory-Augmented Text-Based World Model](https://arxiv.org/abs/2608.07107v2) | 2026-08-07 | EMNLP 2026 | 🏆 Top venue: EMNLP 2026 | — |
| [GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents](https://arxiv.org/abs/2605.29668v3) | 2026-05-28 | EMNLP 2026 | 🏆 Top venue: EMNLP 2026 | — |
| [FlowEvo: Self-Evolving Agents through the Co-Evolution of Workflows and Executable Skills](https://arxiv.org/abs/2607.21596v2) | 2026-04-18 | COLM 2026 | 🏆 Top venue: COLM 2026 | — |
| [Matching Accuracy, Different Geometry: Evolution Strategies vs GRPO in LLM Post-Training](https://arxiv.org/abs/2604.01499v3) | 2026-04-02 | COLM 2026 | 🏆 Top venue: COLM 2026 | — |
| [On The Statistical Limits of Self-Improving Agents](https://arxiv.org/abs/2510.04399v3) | 2025-10-05 | TMLR 2026 | 🏆 Top venue: TMLR 2026 | — |
| [Diffract: Spectral View of LLM Domain Adaptation](https://arxiv.org/abs/2608.10850v1) | 2026-08-11 | ICML 2026 | 🏆 Top venue: ICML 2026 | — |
| [VDC-Agent: When Video Detailed Captioners Evolve Themselves via Agentic Self-Reflection](https://arxiv.org/abs/2511.19436v2) | 2025-11-24 | ECCV 2026 | 🏆 Top venue: ECCV 2026 | — |
| [CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification](https://arxiv.org/abs/2604.01687v3) | 2026-04-02 | COLM | 🏆 Top venue: COLM | — |
| [EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents](https://arxiv.org/abs/2608.05446v1) | 2026-08-05 | COLM 2026 | 🏆 Top venue: COLM 2026 | — |
| [A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents](https://arxiv.org/abs/2602.06052v4) | 2026-01-14 | TMLR | ⭐ Popular code<br>🏆 Top venue: TMLR | [GitHub ★ 183](https://github.com/AgentMemoryWorld/Awesome-Agent-Memory) |
| [DiffuseAgent-MI: Distributionally-Grounded,Tool-Integrated Self-Evolving Agents for Faithful Visual Reasoning](https://arxiv.org/abs/2608.00540v1) | 2026-08-01 | ICML 2026 | 🏆 Top venue: ICML 2026 | — |
| [SLoRA: Balancing Plasticity and Forgetting in Large Language Models for Continual Learning](https://aclanthology.org/2026.acl-long.247/) | 2026-07-01 | ACL 2026 (Main) | 🏆 Top venue: ACL 2026 (Main) | [GitHub ★ 0](https://github.com/alina1031/SLoRA) |
| [Self-evolving LLM agents with in-distribution Optimization](https://arxiv.org/abs/2606.07367) | 2026-06-05 | ICML 2026 | 🏆 Top venue: ICML 2026 | Citations: 3 (Google Scholar) |
| [RISE: Self-Improving Robot Policy with Compositional World Model](https://arxiv.org/abs/2602.11075) | 2026-02-11 | RSS 2026 | ⭐ Popular code<br>📈 Highly cited<br>🏆 Top venue: RSS 2026 | [GitHub ★ 338](https://github.com/OpenDriveLab/RISE)<br>Citations: 23 (Google Scholar) |
| [Autonomous Evolution of EDA Tools: Multi-Agent Self-Evolved ABC](https://arxiv.org/abs/2604.15082) | 2026-04-16 | DAC 2026 | 🏆 Top venue: DAC 2026 | Citations: 7 (Google Scholar) |
| [Mem$^2$Evolve: Towards Self-Evolving Agents via Co-Evolutionary Capability Expansion and Experience Distillation](https://arxiv.org/abs/2604.10923) | 2026-04-13 | ACL 2026 (Main) | 🏆 Top venue: ACL 2026 (Main) | [GitHub ★ 1](https://github.com/BUAA-IRIP-LLM/Mem2Evolve)<br>Citations: 9 (Google Scholar) |
| [Continual-learning for Modelling Low-Resource Languages from Large Language Models](https://arxiv.org/abs/2601.05874) | 2026-01-09 | EACL 2026 (Main) | 🏆 Top venue: EACL 2026 (Main) | — |
| [How Do Large Language Models Learn Concepts During Continual Pre-Training?](https://arxiv.org/abs/2601.03570v2) | 2026-01-07 | arXiv | 🏢 Industry: Meta | — |
| [Skill Self-Play: Pushing the Frontier of LLM Capability with Co-Evolving Skills](https://arxiv.org/abs/2607.22529) | 2026-07-24 | arXiv | ⭐ Popular code<br>🏢 Industry: Alibaba / Qwen | [GitHub ★ 119](https://github.com/Qwen-Applications/skill-self-play)<br>Citations: 1 (Google Scholar) |
| [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://arxiv.org/abs/2605.23904) | 2026-05-22 | arXiv | 🔥 Very popular code<br>📈 Highly cited<br>🏢 Industry: Microsoft Research | [GitHub ★ 15,927](https://github.com/microsoft/SkillOpt)<br>Citations: 37 (Google Scholar) |
| [Hyperagents](https://arxiv.org/abs/2603.19461) | 2026-03-19 | arXiv | 🔥 Very popular code<br>📈 Highly cited<br>🏢 Industry: Meta | [GitHub ★ 2,675](https://github.com/facebookresearch/HyperAgents)<br>Citations: 33 (Google Scholar) |
| [SEED: Self-Evolving On-Policy Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2607.14777) | 2026-07-16 | arXiv | ⭐ Popular code | [GitHub ★ 226](https://github.com/jinyangwu/SEED)<br>Citations: 5 (Google Scholar) |
| [A Self-Evolving Agent for Longitudinal Personal Health Management](https://arxiv.org/abs/2607.13940) | 2026-07-15 | arXiv | ⭐ Popular code | [GitHub ★ 162](https://github.com/HC-Guo/HealthClaw) |
| [Self-Improvements in Modern Agentic Systems: A Survey](https://arxiv.org/abs/2607.13104) | 2026-07-14 | arXiv | ⭐ Popular code | [GitHub ★ 350](https://github.com/selfimproving-agent/awesome-Self-Improving-Agents)<br>Citations: 3 (Google Scholar) |
| [Danus: Orchestrating Mathematical Reasoning Agents with Fact-Graph Memory](https://arxiv.org/abs/2607.06447) | 2026-07-07 | arXiv | ⭐ Popular code | [GitHub ★ 167](https://github.com/frenzymath/Danus)<br>Citations: 7 (Google Scholar) |
| [Are We Ready For An Agent-Native Memory System?](https://arxiv.org/abs/2606.24775) | 2026-06-23 | arXiv | ⭐ Popular code | [GitHub ★ 132](https://github.com/OpenDataBox/MemoryData)<br>Citations: 3 (Google Scholar) |

## 🗓️ Monthly Index

| Month | Papers | Self-Evolving | Memory | Continual Training |
| --- | ---: | ---: | ---: | ---: |
| [2025-03](papers/2025/03/README.md) | 1 | 1 | 0 | 0 |
| [2025-06](papers/2025/06/README.md) | 1 | 0 | 1 | 0 |
| [2025-08](papers/2025/08/README.md) | 1 | 0 | 0 | 1 |
| [2025-09](papers/2025/09/README.md) | 4 | 1 | 0 | 3 |
| [2025-10](papers/2025/10/README.md) | 1 | 1 | 0 | 0 |
| [2025-11](papers/2025/11/README.md) | 1 | 1 | 0 | 0 |
| [2025-12](papers/2025/12/README.md) | 1 | 0 | 0 | 1 |
| [2026-01](papers/2026/01/README.md) | 81 | 14 | 65 | 8 |
| [2026-02](papers/2026/02/README.md) | 67 | 14 | 53 | 6 |
| [2026-03](papers/2026/03/README.md) | 72 | 12 | 61 | 7 |
| [2026-04](papers/2026/04/README.md) | 77 | 12 | 65 | 6 |
| [2026-05](papers/2026/05/README.md) | 113 | 24 | 94 | 6 |
| [2026-06](papers/2026/06/README.md) | 107 | 26 | 81 | 6 |
| [2026-07](papers/2026/07/README.md) | 115 | 46 | 63 | 11 |
| [2026-08](papers/2026/08/README.md) | 195 | 98 | 65 | 40 |

## 📝 Latest Papers

| Published | Track | Paper | Links |
| --- | --- | --- | --- |
| 2026-08-24 | Agent Self-Evolving | [Prime Agent: A Self-Improving RLM Harness](https://arxiv.org/abs/2608.23552v1) | [Paper](https://arxiv.org/abs/2608.23552v1) / [PDF](https://arxiv.org/pdf/2608.23552v1) |
| 2026-08-24 | Agent Memory | [InjecMEM: Memory Injection Attack on LLM Agent Memory Systems](https://arxiv.org/abs/2608.23471v1) | [Paper](https://arxiv.org/abs/2608.23471v1) / [PDF](https://arxiv.org/pdf/2608.23471v1) |
| 2026-08-24 | Agent Memory | [Dual-Grained Agent Memory and Shapley Context Attribution for Multimodal Agentic Learner](https://arxiv.org/abs/2608.23268v1) | [Paper](https://arxiv.org/abs/2608.23268v1) / [PDF](https://arxiv.org/pdf/2608.23268v1) |
| 2026-08-24 | Agent Memory | [Counter with Evidence! A Multi-Agent Memory Efficient Reasoning Framework for Hate Category Informed Counterspeech Generation](https://arxiv.org/abs/2608.23152v1) | [Paper](https://arxiv.org/abs/2608.23152v1) / [PDF](https://arxiv.org/pdf/2608.23152v1) |
| 2026-08-24 | Agent Self-Evolving | [GSAR: Goal-State-Anchor Rewards for Mobile GUI Agents with Self-Evolving Data Synthesis](https://arxiv.org/abs/2608.22847v1) | [Paper](https://arxiv.org/abs/2608.22847v1) / [PDF](https://arxiv.org/pdf/2608.22847v1) |
| 2026-08-24 | Agent Self-Evolving | [TRACE: A Self-Evolving Skill Bank for Consistent, Limit-Aware LLM Agents](https://arxiv.org/abs/2608.22793v1) | [Paper](https://arxiv.org/abs/2608.22793v1) / [PDF](https://arxiv.org/pdf/2608.22793v1) |
| 2026-08-24 | Agent Memory | [The Retriever Should Remember: Experience-Amortized Reranking for Long-Term Agent Memory](https://arxiv.org/abs/2608.22767v1) | [Paper](https://arxiv.org/abs/2608.22767v1) / [PDF](https://arxiv.org/pdf/2608.22767v1) |
| 2026-08-24 | Agent Memory | [The Compaction Cliff in Long-Running AI Agent Memory](https://arxiv.org/abs/2608.22752v1) | [Paper](https://arxiv.org/abs/2608.22752v1) / [PDF](https://arxiv.org/pdf/2608.22752v1) |
| 2026-08-23 | Agent Self-Evolving | [Coalition-Aware Skill Reliability for Self-Evolving Agents](https://arxiv.org/abs/2608.22610v1) | [Paper](https://arxiv.org/abs/2608.22610v1) / [PDF](https://arxiv.org/pdf/2608.22610v1) |
| 2026-08-23 | Agent Self-Evolving | [CONTRAMEM: Learning Self-Evolving Procedural Memory from Contrasting Multi-Model Trajectories](https://arxiv.org/abs/2608.22533v1) | [Paper](https://arxiv.org/abs/2608.22533v1) / [PDF](https://arxiv.org/pdf/2608.22533v1) |
| 2026-08-23 | Agent Self-Evolving | [When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents](https://arxiv.org/abs/2608.22339v1) | [Paper](https://arxiv.org/abs/2608.22339v1) / [PDF](https://arxiv.org/pdf/2608.22339v1) |
| 2026-08-23 | Agent Memory | [HERO: Human-profile Enhanced Retrieval Optimization Framework for Long-term Agent Memory](https://arxiv.org/abs/2608.22310v1) | [Paper](https://arxiv.org/abs/2608.22310v1) / [PDF](https://arxiv.org/pdf/2608.22310v1) |
| 2026-08-23 | Agent Memory | [Dual-Layer Agentic Memory with Fast Write Routing and Slow Consolidation](https://arxiv.org/abs/2608.22215v1) | [Paper](https://arxiv.org/abs/2608.22215v1) / [PDF](https://arxiv.org/pdf/2608.22215v1) |
| 2026-08-23 | Agent Self-Evolving | [BehaviorWorldGen: Closing the Loop between Action Models and World Simulators via Controllable Behavior-Aware Structured World Generation](https://arxiv.org/abs/2608.22187v1) | [Paper](https://arxiv.org/abs/2608.22187v1) / [PDF](https://arxiv.org/pdf/2608.22187v1) |
| 2026-08-22 | Agent Self-Evolving | [SSE-Bio: A Structured Self-Evolving Agent with Agentic Retrieval Policy for Multi-Hop Biomedical Reasoning](https://arxiv.org/abs/2608.22132v1) | [Paper](https://arxiv.org/abs/2608.22132v1) / [PDF](https://arxiv.org/pdf/2608.22132v1) |
| 2026-08-22 | Agent Memory | [MEMORY Wins All: Indirect Bias Injection Attacks via Social Media Feeds](https://arxiv.org/abs/2608.22061v1) | [Paper](https://arxiv.org/abs/2608.22061v1) / [PDF](https://arxiv.org/pdf/2608.22061v1) |
| 2026-08-22 | Agent Memory | [MemGuard: Persisting Verifier Signals for LLM-Agent Memory Governance](https://arxiv.org/abs/2608.21867v1) | [Paper](https://arxiv.org/abs/2608.21867v1) / [PDF](https://arxiv.org/pdf/2608.21867v1) |
| 2026-08-22 | Agent Memory | [MSM-Mem: A Universal Medical Structured Multimodal Memory Framework for Medical AI Agents](https://arxiv.org/abs/2608.21810v1) | [Paper](https://arxiv.org/abs/2608.21810v1) / [PDF](https://arxiv.org/pdf/2608.21810v1) |
| 2026-08-21 | LLM Continual Training | [Anchoring Bias: A Persistent Fairness Backdoor Attack against MLLMs under Continual Learning](https://arxiv.org/abs/2608.21577v1) | [Paper](https://arxiv.org/abs/2608.21577v1) / [PDF](https://arxiv.org/pdf/2608.21577v1) |
| 2026-08-21 | Agent Memory | [Utility Under Attack: Agent Memory Poisoning and the Limits of Content Screening and Provenance Ranking](https://arxiv.org/abs/2608.21230v1) | [Paper](https://arxiv.org/abs/2608.21230v1) / [PDF](https://arxiv.org/pdf/2608.21230v1) |
| 2026-08-21 | Agent Self-Evolving | [Graph Engineering in the Era of LLM Agents: From Individual Intelligence to System Intelligence](https://arxiv.org/abs/2608.21156v1) | [Paper](https://arxiv.org/abs/2608.21156v1) / [PDF](https://arxiv.org/pdf/2608.21156v1) |
| 2026-08-21 | LLM Continual Training | [TASSO: TAsk-Specific Subspace Optimization for Continual Learning of Vision-Language Models](https://arxiv.org/abs/2608.21487v1) | [Paper](https://arxiv.org/abs/2608.21487v1) / [PDF](https://arxiv.org/pdf/2608.21487v1) |
| 2026-08-21 | LLM Continual Training | [Quantization-Aware Healing: A Practical Recipe for Recovering Compressed, 4-Bit LLMs](https://arxiv.org/abs/2608.20953v1) | [Paper](https://arxiv.org/abs/2608.20953v1) / [PDF](https://arxiv.org/pdf/2608.20953v1) |
| 2026-08-21 | Agent Memory, Agent Self-Evolving | [ForeDreamer: A Self-Evolving Dual-Agent Memory Architecture for Future Event Prediction](https://arxiv.org/abs/2608.20920v2) | [Paper](https://arxiv.org/abs/2608.20920v2) / [PDF](https://arxiv.org/pdf/2608.20920v2) |
| 2026-08-21 | LLM Continual Training | [ResiliFlow: An Open Transport World Model for Infrastructure Perception and Disaster Resilience](https://arxiv.org/abs/2608.20709v1) | [Paper](https://arxiv.org/abs/2608.20709v1) / [PDF](https://arxiv.org/pdf/2608.20709v1) |
| 2026-08-21 | Agent Self-Evolving | [ArtiMo: Agent-Driven Articulated Mesh Animation](https://arxiv.org/abs/2608.20699v1) | [Paper](https://arxiv.org/abs/2608.20699v1) / [PDF](https://arxiv.org/pdf/2608.20699v1) |
| 2026-08-21 | Agent Memory | [DreamBench-SWE: A Multi-Session Memory-Hygiene Benchmark for Software Agents](https://arxiv.org/abs/2608.20664v1) | [Paper](https://arxiv.org/abs/2608.20664v1) / [PDF](https://arxiv.org/pdf/2608.20664v1) |
| 2026-08-21 | Agent Memory | [Weighted Memory Tree: Remembering What Matters for Long-Horizon LLM Agents](https://arxiv.org/abs/2608.20631v1) | [Paper](https://arxiv.org/abs/2608.20631v1) / [PDF](https://arxiv.org/pdf/2608.20631v1) |
| 2026-08-20 | Agent Self-Evolving | [AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement](https://arxiv.org/abs/2608.20318v1) | [Paper](https://arxiv.org/abs/2608.20318v1) / [PDF](https://arxiv.org/pdf/2608.20318v1) |
| 2026-08-20 | LLM Continual Training | [SCoRD: Semantic-Assisted Continual Retriever-Reranker Distillation for LLM-Based Recommendation](https://arxiv.org/abs/2608.19998v1) | [Paper](https://arxiv.org/abs/2608.19998v1) / [PDF](https://arxiv.org/pdf/2608.19998v1) |

## 🗓️ Daily Archive

- [2026-08-25](papers/2026/08/2026-08-25.md)
- [2026-07-28](papers/2026/07/2026-07-28.md)
- [2026-07-16](papers/2026/07/2026-07-16.md)

## 🔎 Scope and Verification

- **Agent Self-Evolving:** self-evolving, self-improving, and evolving agents
- **Agent Memory:** long-term, memory-augmented, and persistent agent memory
- **LLM Continual Training:** continual, lifelong, and post-deployment LLM learning
- **Very popular code:** at least 1,000 GitHub stars; **popular code:** at least 100 stars
- **Highly cited:** at least 10 citations for a 2026 paper; every count records its source and snapshot date
- **Industry / top venue:** marked only when verified from the paper, publisher, or official project page
- Missing metrics are shown as `n/a`, never guessed. Stars and citations are time-sensitive snapshots.

## License

Code is released under the MIT License. Paper metadata remains subject to its source terms.
