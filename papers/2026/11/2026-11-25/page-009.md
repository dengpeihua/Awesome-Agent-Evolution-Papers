> **410 papers** · Page 9/9 · Newest first across all pages

[1](../2026-11-25.md) · [2](page-002.md) · [3](page-003.md) · [4](page-004.md) · [5](page-005.md) · [6](page-006.md) · [7](page-007.md) · [8](page-008.md) · [9](page-009.md)

# Daily Papers · 2026-11-25

> Prepared **10** new, promoted, or retried paper(s) across three research tracks plus explicitly requested papers. Lists are newest publication first.
> Catch-up window: **2026-10-21T02:29:20.628748+08:00** → **2026-11-25T02:26:21.960682+08:00**.

[← Back to index](../../../../README.md)

## All Updates · Newest First

| Published | Track | Paper | Signals |
| --- | --- | --- | --- |
| 2025-07-26 | Long-Horizon Task Agents | [Prometheus: Towards Long-Horizon Codebase Navigation for Repository-Level Problem Solving](https://arxiv.org/abs/2507.19942v2) | 📈 Highly cited |
| 2025-07-21 | Reinforcement Learning | [Stabilizing Knowledge, Promoting Reasoning: Dual-Token Constraints for RLVR](https://arxiv.org/abs/2507.15778v3) | 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified) |
| 2025-07-04 | Long-Horizon Task Agents | [LogicGuard: Improving Embodied LLM agents through Temporal Logic based Critics](https://arxiv.org/abs/2507.03293v2) | 📈 Highly cited |
| 2025-06-18 | Long-Horizon Task Agents | [Specification-based Security Evaluation of Real-World Agents Tool-Calling under Long-Horizon Context Tasks](https://arxiv.org/abs/2506.15253v3) | — |
| 2025-06-10 | Long-Horizon Task Agents | [Fact-Augmented Lookahead Planning for LLM Agents](https://arxiv.org/abs/2506.09171v2) | 📈 Highly cited |
| 2025-06-03 | Reinforcement Learning | [BNPO: Beta Normalization Policy Optimization](https://arxiv.org/abs/2506.02864v2) | — |
| 2025-06-01 | Reinforcement Learning | [Doubly Robust Alignment for Large Language Models](https://arxiv.org/abs/2506.01183v3) | 🏆 CCF-A: NeurIPS 2025<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified) |
| 2025-05-30 | Reinforcement Learning | [HARDTESTGEN: A High-Quality RL Verifier Generation Pipeline for LLM Algorithmic Coding](https://arxiv.org/abs/2505.24098v2) | 🏅 Selected top venue: ICLR 2026<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified) |
| 2025-05-29 | Reinforcement Learning | [VisualSphinx: Large-Scale Synthetic Vision Logic Puzzles for RL](https://arxiv.org/abs/2505.23977v2) | — |
| 2025-05-19 | Reinforcement Learning | [Optimizing Anytime Reasoning via Budget Relative Policy Optimization](https://arxiv.org/abs/2505.13438v4) | — |

## 🚨 Priority Watch

| Paper | Signals | Venue / affiliation evidence |
| --- | --- | --- |
| [Prometheus: Towards Long-Horizon Codebase Navigation for Repository-Level Problem Solving](https://arxiv.org/abs/2507.19942v2) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Stabilizing Knowledge, Promoting Reasoning: Dual-Token Constraints for RLVR](https://arxiv.org/abs/2507.15778v3) | 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified) | arXiv comment: Accepted to NeurIPS 2026 |
| [LogicGuard: Improving Embodied LLM agents through Temporal Logic based Critics](https://arxiv.org/abs/2507.03293v2) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Fact-Augmented Lookahead Planning for LLM Agents](https://arxiv.org/abs/2506.09171v2) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Doubly Robust Alignment for Large Language Models](https://arxiv.org/abs/2506.01183v3) | 🏆 CCF-A: NeurIPS 2025<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified) | arXiv comment: Accepted to NeurIPS 2025 |
| [HARDTESTGEN: A High-Quality RL Verifier Generation Pipeline for LLM Algorithmic Coding](https://arxiv.org/abs/2505.24098v2) | 🏅 Selected top venue: ICLR 2026<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified) | arXiv comment: Original version was published at ICLR 2026. This is the expanded version with more details |

## Reinforcement Learning

### [Stabilizing Knowledge, Promoting Reasoning: Dual-Token Constraints for RLVR](https://arxiv.org/abs/2507.15778v3)

- **Authors:** Runze Liu, Jiakang Wang, Fuzheng Zhang, Xiu Li, Guorui Zhou, Kun Gai, Ling Pan
- **Published:** 2025-07-21
- **Priority:** 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified)
- **Venue:** NeurIPS 2026
- **Affiliations:** n/a
- **Categories:** cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2507.15778v3) · [PDF](https://arxiv.org/pdf/2507.15778v3)

Reinforcement Learning with Verifiable Rewards (RLVR) has become an effective post-training method for improving the reasoning abilities of Large Language Models (LLMs). However, existing methods mainly apply uniform optimization constraints across all tokens, ignoring their heterogeneous roles. Prior work shows that high-entropy tokens are closely tied to reasoning, while low-entropy tokens primarily encode factual knowledge, and recent approaches attempt to exploit this distinction by isolating token updates via masking or asynchronous training. We argue that retaining training signals across token types can lead to more effective learning. To address this, we propose Archer, an entropy-aware RLVR framework with dual-token constraints that preserves joint optimization while modulating update strength across token types. Our method introduces response-level entropy normalization for stable token classification and applies differentiated clipping ranges and KL regularization to encourage exploration on reasoning tokens while preserving knowledge tokens. Experiments on mathematical reasoning and code generation benchmarks show that Archer consistently outperforms strong baselines across multiple model scales, improving both pass@1 and pass@K performance. These results highlight the importance of respecting sequence-level dependencies when designing fine-grained RL optimization strategies for LLMs. The code is available at https://github.com/wizard-III/ArcherCodeR.

### [BNPO: Beta Normalization Policy Optimization](https://arxiv.org/abs/2506.02864v2)

- **Authors:** Changyi Xiao, Mengdi Zhang, Yixin Cao
- **Published:** 2025-06-03
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2506.02864v2) · [PDF](https://arxiv.org/pdf/2506.02864v2)

Reinforcement learning with rule-based, binary-valued reward functions has been shown to significantly enhance the reasoning capabilities of large language models. These models typically rely on REINFORCE-based policy optimization methods, such as REINFORCE with baseline and group relative policy optimization (GRPO). However, a key limitation is that existing methods either ignore reward normalization or use static normalization schemes, which fail to adapt to the evolving policy during training. This mismatch can lead to unstable gradient estimates and hinder training stability. To address this issue, we propose Beta Normalization Policy Optimization (BNPO), a novel method that adaptively normalizes rewards using a Beta distribution with dynamically updated parameters. By aligning normalization with the changing policy distribution, BNPO enables more accurate, lower-variance gradient estimation and promotes stable training dynamics. We provide theoretical analysis showing that BNPO reduces variance and generalizes both REINFORCE and GRPO under binary-valued rewards. In addition, we introduce an advantage decomposition mechanism to extend BNPO to more complex reward settings. Experimental results demonstrate that BNPO achieves state-of-the-art performance among policy optimization methods on reasoning tasks.

### [Doubly Robust Alignment for Large Language Models](https://arxiv.org/abs/2506.01183v3)

- **Authors:** Erhan Xu, Kai Ye, Hongyi Zhou, Luhan Zhu, Francesco Quinzan, Chengchun Shi
- **Published:** 2025-06-01
- **Priority:** 🏆 CCF-A: NeurIPS 2025<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified)
- **Venue:** NeurIPS 2025
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI, stat.ML
- **Links:** [Paper](https://arxiv.org/abs/2506.01183v3) · [PDF](https://arxiv.org/pdf/2506.01183v3)

This paper studies reinforcement learning from human feedback (RLHF) for aligning large language models with human preferences. While RLHF has demonstrated promising results, many algorithms are highly sensitive to misspecifications in the underlying preference model (e.g., the Bradley-Terry model), the reference policy, or the reward function, resulting in undesirable fine-tuning. To address model misspecification, we propose a doubly robust preference optimization algorithm that remains consistent when either the preference model or the reference policy is correctly specified (without requiring both). Our proposal demonstrates superior and more robust performance than state-of-the-art algorithms, both in theory and in practice. The code is available at https://github.com/DRPO4LLM/DRPO4LLM

### [HARDTESTGEN: A High-Quality RL Verifier Generation Pipeline for LLM Algorithmic Coding](https://arxiv.org/abs/2505.24098v2)

- **Authors:** Zhongmou He, Yee Man Choi, Kexun Zhang, Jiabao Ji, Junting Zhou, Dejia Xu, Ivan Bercovich, Aidan Zhang, Yixiao Zeng, Lei Li
- **Published:** 2025-05-30
- **Priority:** 🏅 Selected top venue: ICLR 2026<br>📣 Acceptance first observed: 2026-11-25 (actual acceptance date unverified)
- **Venue:** ICLR 2026
- **Affiliations:** n/a
- **Categories:** cs.CL, cs.AI, cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2505.24098v2) · [PDF](https://arxiv.org/pdf/2505.24098v2)

Verifiers provide important reward signals for reinforcement learning of large language models (LLMs). However, it is challenging to develop or create reliable verifiers, especially for code generation tasks. A well-disguised wrong solution program may only be detected by carefully human-written edge cases that are difficult to synthesize automatically. To address this issue, we propose HARDTESTGEN, an approach to synthesize high-quality test cases for algorithmic coding problems. We curate a comprehensive algorithmic programming dataset HARDTESTS with 26.6k problems and high-quality synthetic tests. Compared with existing tests, HARDTESTGEN tests demonstrate significantly higher accuracy in verifying LLM-generated code (+11.22 percentage points in precision, the percentage of actually correct code within the predicted correct ones). We also show that downstream post-training -- including rejection sampling and reinforcement learning (RL) -- using HARDTESTS verifier results in improved performance of LLM code generation. We open-source our dataset and synthesis pipeline at https://leililab.github.io/HardTests/.

### [VisualSphinx: Large-Scale Synthetic Vision Logic Puzzles for RL](https://arxiv.org/abs/2505.23977v2)

- **Authors:** Yichen Feng, Zhangchen Xu, Fengqing Jiang, Yuetai Li, Bhaskar Ramasubramanian, Luyao Niu, Bill Yuchen Lin, Radha Poovendran
- **Published:** 2025-05-29
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.CV, cs.AI, cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2505.23977v2) · [PDF](https://arxiv.org/pdf/2505.23977v2)

Vision language models (VLMs) are expected to perform effective multimodal reasoning and make logically coherent decisions, which is critical to tasks such as diagram understanding and spatial problem solving. However, current VLM reasoning lacks large-scale and well-structured training datasets. To bridge this gap, we propose VisualSphinx, a first-of-its-kind large-scale synthetic visual logical reasoning training dataset. To tackle the challenge of image synthesis with grounded answers, we propose a rule-to-image synthesis pipeline that extracts and expands puzzle rules from seed questions and generates executable rendering programs for puzzle assembly. Using standard GRPO with binary correctness rewards as a validation recipe, experiments show that VLMs trained on VisualSphinx benefit from the logical coherence and readability of our dataset and exhibit improved performance on logical reasoning tasks. The enhanced reasoning capabilities developed from VisualSphinx also benefit other reasoning tasks such as algebraic reasoning, arithmetic reasoning and geometry reasoning.

### [Optimizing Anytime Reasoning via Budget Relative Policy Optimization](https://arxiv.org/abs/2505.13438v4)

- **Authors:** Penghui Qi, Zichen Liu, Tianyu Pang, Chao Du, Wee Sun Lee, Min Lin
- **Published:** 2025-05-19
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI, cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2505.13438v4) · [PDF](https://arxiv.org/pdf/2505.13438v4)

Scaling test-time compute is crucial for enhancing the reasoning capabilities of large language models (LLMs). Existing approaches typically employ reinforcement learning (RL) to maximize a verifiable reward obtained at the end of reasoning traces. However, such methods optimize only the final performance under a large and fixed token budget, which hinders efficiency in both training and deployment. In this work, we present a novel framework, AnytimeReasoner, to optimize anytime reasoning performance, which aims to improve token efficiency and the flexibility of reasoning under varying token budget constraints. To achieve this, we truncate the complete thinking process to fit within sampled token budgets from a prior distribution, compelling the model to summarize the optimal answer for each truncated thinking for verification. This introduces verifiable dense rewards into the reasoning process, facilitating more effective credit assignment in RL optimization. We then optimize the thinking and summary policies in a decoupled manner to maximize the cumulative reward. Additionally, we introduce a novel variance reduction technique, Budget Relative Policy Optimization (BRPO), to enhance the robustness and efficiency of the learning process when reinforcing the thinking policy. Empirical results in mathematical reasoning tasks demonstrate that our method consistently outperforms GRPO across all thinking budgets under various prior distributions, enhancing both training and token efficiency.

## Long-Horizon Task Agents

### [Prometheus: Towards Long-Horizon Codebase Navigation for Repository-Level Problem Solving](https://arxiv.org/abs/2507.19942v2)

- **Authors:** Yue Pan, Zimin Chen, Siyu Lu, Zhaoyang Chu, Xiang Li, Han Li, Yang Feng, Claire Le Goues, Federica Sarro, Martin Monperrus, He Ye
- **Published:** 2025-07-26
- **Priority:** 📈 Highly cited
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.SE
- **Links:** [Paper](https://arxiv.org/abs/2507.19942v2) · [PDF](https://arxiv.org/pdf/2507.19942v2)

Large Language Models (LLMs) have shown remarkable capabilities in automating software engineering tasks, spurring the emergence of coding agents that scaffold LLMs with external tools to resolve repository-level problems. However, existing agents still struggle to navigate large-scale codebases, as the Needle-in-a-Haystack problem persists even with million-token context windows, where relevant evidence is often overwhelmed by large volumes of irrelevant code and documentation. Prior codebase navigation approaches, including embedding-based retrieval, file-system exploration, and graph-based retrieval, address parts of this challenge but fail to capture the temporal continuity of agent reasoning, rendering agents stateless and causing repeated repository traversals that hinder scalable planning and reasoning. To address these limitations, we present Prometheus, a memory-centric coding agent framework for long-horizon codebase navigation. Prometheus represents the repository as a unified knowledge graph to encode semantic dependencies and employs a context engine augmented with working memory that retains and reuses previously explored contexts to ensure continuity across reasoning steps. Built upon this engine, Prometheus integrates memory-enhanced navigation into a multi-agent system for automated issue resolution, encompassing issue classification, bug reproduction, patch generation, and verification. Comprehensive experiments are conducted on two widely used issue resolution benchmarks, i.e., SWE-bench Verified and SWE-PolyBench Verified. Powered by GPT-5, Prometheus achieves state-of-the-art performance with 74.4% and 33.8% resolution rates on the two benchmarks, ranking Top-6 and Top-1 among open-source agent systems, respectively. Our data and code are available at https://github.com/EuniAI/Prometheus.

### [LogicGuard: Improving Embodied LLM agents through Temporal Logic based Critics](https://arxiv.org/abs/2507.03293v2)

- **Authors:** Anand Gokhale, Vaibhav Srivastava, Francesco Bullo
- **Published:** 2025-07-04
- **Priority:** 📈 Highly cited
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.AI, cs.CL, cs.LG, eess.SY
- **Links:** [Paper](https://arxiv.org/abs/2507.03293v2) · [PDF](https://arxiv.org/pdf/2507.03293v2)

Large language models (LLMs) have shown promise in zero-shot and single step reasoning and decision making problems, but in long horizon sequential planning tasks, their errors compound, often leading to unreliable or inefficient behavior. We introduce LogicGuard, a modular actor-critic architecture in which an LLM actor is guided by a trajectory level LLM critic that communicates through Linear Temporal Logic (LTL). Our setup combines the reasoning strengths of language models with the guarantees of formal logic. The actor selects high-level actions from natural language observations, while the critic analyzes full trajectories and proposes new LTL constraints that shield the actor from future unsafe or inefficient behavior. LogicGuard supports both fixed safety rules and adaptive, learned constraints, and is model-agnostic: any LLM-based planner can serve as the actor, with LogicGuard acting as a logic-generating wrapper. We formalize planning as graph traversal under symbolic constraints, allowing LogicGuard to analyze failed or suboptimal trajectories and generate new temporal logic rules that improve future behavior. To demonstrate generality, we evaluate LogicGuard across two distinct settings: short-horizon general tasks and long-horizon specialist tasks. On the Behavior benchmark of 100 household tasks, LogicGuard increases task completion rates by 25% over a baseline InnerMonologue planner. On the Minecraft diamond-mining task, which is long-horizon and requires multiple interdependent subgoals, LogicGuard improves both efficiency and safety compared to SayCan and InnerMonologue. These results show that enabling LLMs to supervise each other through temporal logic yields more reliable, efficient and safe decision-making for both embodied agents.

### [Specification-based Security Evaluation of Real-World Agents Tool-Calling under Long-Horizon Context Tasks](https://arxiv.org/abs/2506.15253v3)

- **Authors:** Yuchuan Fu, Minghe Wang, Xiaohan Yuan, Chenlin Zou, Kaitong Jia, Jinfeng Li, Dongxia Wang
- **Published:** 2025-06-18
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.CR, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2506.15253v3) · [PDF](https://arxiv.org/pdf/2506.15253v3)

As large language model (LLM) agents are increasingly deployed in long-horizon unattended scenarios, security evaluation of them before deployment becomes increasingly essential and challenging. Existing evaluation methods mainly follow the paradigms of LLM-as-a-Judge or Agent-as-a-Judge. However, such judges are themselves often vulnerable to hallucination and can even be affected by perturbations. Furthermore, because capturing full environment states at every step is often prohibitively expensive in open-ended environments, existing evaluations typically rely on textual logs and the final environment state. As a result, they may miss transient violations that are overwritten before the trajectory ends or never reflected in textual logs. We present RAS-Eval, a specification-based security evaluation framework for LLM agents. RAS-Eval uniformly expresses utility and security objectives as Linear Temporal Logic (LTL) specifications over tool-call trajectories and dynamic environment observations, and verifies them with an off-the-shelf model checker. This design addresses both limitations above. First, unlike LLM-as-a-Judge and Agent-as-a-Judge, RAS-Eval derives deterministic verdicts from formally defined properties, eliminating evaluator-side uncertainty and remaining reliable even for long-horizon trajectories. Second, RAS-Eval observes exactly the states on which the verdict depends, making it affordable to monitor the environment throughout execution and detect transient violations that leave little trace in the logs or final environment state. Moreover, we design a multi-agent-based dataset construction pipeline. Using it, we construct a benchmark (https://github.com/lanzer-tree/RAS-Eval) of 200 normal tasks and 800 attack tasks spanning four attack surfaces: indirect prompt injection, tool poisoning, skill code injection, and tool code injection.

### [Fact-Augmented Lookahead Planning for LLM Agents](https://arxiv.org/abs/2506.09171v2)

- **Authors:** Samuel Holt, Max Ruiz Luyten, Thomas Pouplin, Mihaela van der Schaar
- **Published:** 2025-06-10
- **Priority:** 📈 Highly cited
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI, cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2506.09171v2) · [PDF](https://arxiv.org/pdf/2506.09171v2)

Large Language Models (LLMs) are increasingly capable, but LLM agents still struggle to plan effectively in interactive, partially observable, long-horizon environments when search is unguided or recent history is insufficient. We introduce LWM-Planner, a fact-augmented lookahead planning framework that improves agent behavior purely through in-context learning. After each episode, the agent extracts task-critical atomic facts from its trajectories, validates candidates with a lightweight predictive-consistency filter (and optionally compresses them), and uses the resulting fact set to condition action proposal, single-step latent world-model simulation, and state-value estimation. Planning then proceeds via recursive, depth-limited lookahead over candidate trajectories conditioned on the accumulated facts and recent history, enabling online improvement without parameter updates. We provide abstraction-style motivation: treating facts as reducing state aliasing (proxy $ε_{\mathrm{sim}}$) and fact-conditioned simulation as lowering one-step error (proxy $δ_{\mathrm{model}}$), without claiming formal guarantees. Empirically, on text FrozenLake variants, CrafterMini, and ALFWorld, the approach improves cumulative return over ReAct/Reflexion and search-only baselines, suggesting that additional test-time search is most useful when grounded by compact, experience-derived facts.
