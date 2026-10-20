> **1403 papers** · Page 29/29 · Newest first across all pages

[1](../2026-10-21.md) · [2](page-002.md) · [3](page-003.md) · [4](page-004.md) · [5](page-005.md) · [6](page-006.md) · [7](page-007.md) · [8](page-008.md) · [9](page-009.md) · [10](page-010.md) · [11](page-011.md) · [12](page-012.md) · [13](page-013.md) · [14](page-014.md) · [15](page-015.md) · [16](page-016.md) · [17](page-017.md) · [18](page-018.md) · [19](page-019.md) · [20](page-020.md) · [21](page-021.md) · [22](page-022.md) · [23](page-023.md) · [24](page-024.md) · [25](page-025.md) · [26](page-026.md) · [27](page-027.md) · [28](page-028.md) · [29](page-029.md)

# Daily Papers · 2026-10-21

> Prepared **3** new, promoted, or retried paper(s) across five research tracks plus explicitly requested papers. Lists are newest publication first.
> Catch-up window: **2025-01-01T00:00:00+00:00** → **2026-10-21T02:02:34.611240+08:00**.

[← Back to index](../../../../README.md)

## All Updates · Newest First

| Published | Track | Paper | Signals |
| --- | --- | --- | --- |
| 2025-02-03 | Reinforcement Learning, Long-Horizon Task Agents | [Reinforcement Learning for Long-Horizon Interactive LLM Agents](https://arxiv.org/abs/2502.01600v3) | — |
| 2025-01-30 | Long-Horizon Task Agents | [Integrating LMM Planners and 3D Skill Policies for Generalizable Manipulation](https://arxiv.org/abs/2501.18733v1) | — |
| 2025-01-16 | Long-Horizon Task Agents | [SOP-Agent: Empower General Purpose AI Agent with Domain-Specific SOPs](https://arxiv.org/abs/2501.09316v1) | — |

## Reinforcement Learning

### [Reinforcement Learning for Long-Horizon Interactive LLM Agents](https://arxiv.org/abs/2502.01600v3)

- **Authors:** Kevin Chen, Marco Cusumano-Towner, Brody Huval, Aleksei Petrenko, Jackson Hamburger, Vladlen Koltun, Philipp Krähenbühl
- **Published:** 2025-02-03
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2502.01600v3) · [PDF](https://arxiv.org/pdf/2502.01600v3)

Interactive digital agents (IDAs) leverage APIs of stateful digital environments to perform tasks in response to user requests. While IDAs powered by instruction-tuned large language models (LLMs) can react to feedback from interface invocations in multi-step exchanges, they have not been trained in their respective digital environments. Prior methods accomplish less than half of tasks in sophisticated benchmarks such as AppWorld. We present a reinforcement learning (RL) approach that trains IDAs directly in their target environments. We formalize this training as a partially observable Markov decision process and derive LOOP, a data- and memory-efficient variant of proximal policy optimization. LOOP uses no value network and maintains exactly one copy of the underlying LLM in memory, making its implementation straightforward and as memory-efficient as fine-tuning a single LLM. A 32-billion-parameter agent trained with LOOP in the AppWorld environment outperforms the much larger OpenAI o1 agent by 9 percentage points (15% relative). To our knowledge, this is the first reported application of RL to IDAs that interact with a stateful, multi-domain, multi-app environment via direct API calls. Our analysis sheds light on the effectiveness of RL in this area, showing that the agent learns to consult the API documentation, avoid unwarranted assumptions, minimize confabulation, and recover from setbacks.

## Long-Horizon Task Agents

### [Reinforcement Learning for Long-Horizon Interactive LLM Agents](https://arxiv.org/abs/2502.01600v3)

- **Authors:** Kevin Chen, Marco Cusumano-Towner, Brody Huval, Aleksei Petrenko, Jackson Hamburger, Vladlen Koltun, Philipp Krähenbühl
- **Published:** 2025-02-03
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2502.01600v3) · [PDF](https://arxiv.org/pdf/2502.01600v3)

Interactive digital agents (IDAs) leverage APIs of stateful digital environments to perform tasks in response to user requests. While IDAs powered by instruction-tuned large language models (LLMs) can react to feedback from interface invocations in multi-step exchanges, they have not been trained in their respective digital environments. Prior methods accomplish less than half of tasks in sophisticated benchmarks such as AppWorld. We present a reinforcement learning (RL) approach that trains IDAs directly in their target environments. We formalize this training as a partially observable Markov decision process and derive LOOP, a data- and memory-efficient variant of proximal policy optimization. LOOP uses no value network and maintains exactly one copy of the underlying LLM in memory, making its implementation straightforward and as memory-efficient as fine-tuning a single LLM. A 32-billion-parameter agent trained with LOOP in the AppWorld environment outperforms the much larger OpenAI o1 agent by 9 percentage points (15% relative). To our knowledge, this is the first reported application of RL to IDAs that interact with a stateful, multi-domain, multi-app environment via direct API calls. Our analysis sheds light on the effectiveness of RL in this area, showing that the agent learns to consult the API documentation, avoid unwarranted assumptions, minimize confabulation, and recover from setbacks.

### [Integrating LMM Planners and 3D Skill Policies for Generalizable Manipulation](https://arxiv.org/abs/2501.18733v1)

- **Authors:** Yuelei Li, Ge Yan, Annabella Macaluso, Mazeyu Ji, Xueyan Zou, Xiaolong Wang
- **Published:** 2025-01-30
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.RO, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2501.18733v1) · [PDF](https://arxiv.org/pdf/2501.18733v1)

The recent advancements in visual reasoning capabilities of large multimodal models (LMMs) and the semantic enrichment of 3D feature fields have expanded the horizons of robotic capabilities. These developments hold significant potential for bridging the gap between high-level reasoning from LMMs and low-level control policies utilizing 3D feature fields. In this work, we introduce LMM-3DP, a framework that can integrate LMM planners and 3D skill Policies. Our approach consists of three key perspectives: high-level planning, low-level control, and effective integration. For high-level planning, LMM-3DP supports dynamic scene understanding for environment disturbances, a critic agent with self-feedback, history policy memorization, and reattempts after failures. For low-level control, LMM-3DP utilizes a semantic-aware 3D feature field for accurate manipulation. In aligning high-level and low-level control for robot actions, language embeddings representing the high-level policy are jointly attended with the 3D feature field in the 3D transformer for seamless integration. We extensively evaluate our approach across multiple skills and long-horizon tasks in a real-world kitchen environment. Our results show a significant 1.45x success rate increase in low-level control and an approximate 1.5x improvement in high-level planning accuracy compared to LLM-based baselines. Demo videos and an overview of LMM-3DP are available at https://lmm-3dp-release.github.io.

### [SOP-Agent: Empower General Purpose AI Agent with Domain-Specific SOPs](https://arxiv.org/abs/2501.09316v1)

- **Authors:** Anbang Ye, Qianran Ma, Jia Chen, Muqi Li, Tong Li, Fujiao Liu, Siqi Mai, Meichen Lu, Haitao Bao, Yang You
- **Published:** 2025-01-16
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2501.09316v1) · [PDF](https://arxiv.org/pdf/2501.09316v1)

Despite significant advancements in general-purpose AI agents, several challenges still hinder their practical application in real-world scenarios. First, the limited planning capabilities of Large Language Models (LLM) restrict AI agents from effectively solving complex tasks that require long-horizon planning. Second, general-purpose AI agents struggle to efficiently utilize domain-specific knowledge and human expertise. In this paper, we introduce the Standard Operational Procedure-guided Agent (SOP-agent), a novel framework for constructing domain-specific agents through pseudocode-style Standard Operational Procedures (SOPs) written in natural language. Formally, we represent a SOP as a decision graph, which is traversed to guide the agent in completing tasks specified by the SOP. We conduct extensive experiments across tasks in multiple domains, including decision-making, search and reasoning, code generation, data cleaning, and grounded customer service. The SOP-agent demonstrates excellent versatility, achieving performance superior to general-purpose agent frameworks and comparable to domain-specific agent systems. Additionally, we introduce the Grounded Customer Service Benchmark, the first benchmark designed to evaluate the grounded decision-making capabilities of AI agents in customer service scenarios based on SOPs.
