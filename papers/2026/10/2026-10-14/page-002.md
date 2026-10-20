> **60 papers** · Page 2/2 · Newest first across all pages

[1](../2026-10-14.md) · [2](page-002.md)

# Daily Papers · 2026-10-14

> Prepared **10** new, promoted, or retried paper(s) across five research tracks plus explicitly requested papers. Lists are newest publication first.
> Catch-up window: **2026-10-13T19:01:05.125248+08:00** → **2026-10-14T21:19:53.201647+08:00**.

[← Back to index](../../../../README.md)

## All Updates · Newest First

| Published | Track | Paper | Signals |
| --- | --- | --- | --- |
| 2026-05-27 | Agent/LLM Self-Improvement | [Self-Improving Language Models with Bidirectional Evolutionary Search](https://arxiv.org/abs/2605.28814v2) | — |
| 2026-05-20 | Agent Memory, Long-Horizon Task Agents | [Memory-R2: Fair Credit Assignment for Long-Horizon Memory-Augmented LLM Agents](https://arxiv.org/abs/2605.21768v1) | 📈 Highly cited |
| 2026-05-15 | Agent Memory | [RecMem: Recurrence-based Memory Consolidation for Efficient and Effective Long-Running LLM Agents](https://arxiv.org/abs/2605.16045) | 📈 Highly cited<br>🏆 CCF-A: Annual Meeting of the Association for Computational Linguistics<br>📣 Acceptance first observed: 2026-10-03 (actual acceptance date unverified) |
| 2026-04-17 | Reinforcement Learning | [Improving Heart-Focused Medical Question Answering in LLMs via Variance-Aware Rubric Rewards with GRPO](https://arxiv.org/abs/2606.05174v2) | — |
| 2026-03-20 | Agent Memory, LLM Continual Training | [All-Mem: Agentic Lifelong Memory via Dynamic Topology Evolution](https://arxiv.org/abs/2603.19595) | 📈 Highly cited |
| 2026-03-17 | Agent Memory | [Chronos: Temporal-Aware Conversational Agents with Structured Event Retrieval for Long-Term Memory](https://arxiv.org/abs/2603.16862) | 📈 Highly cited |
| 2026-03-09 | Agent Memory | [Multi-Agent Memory from a Computer Architecture Perspective: Visions and Challenges Ahead](https://arxiv.org/abs/2603.10062) | 📈 Highly cited |
| 2026-03-03 | Agent Memory | [Multi-Agent Debate with Memory Masking](https://arxiv.org/abs/2603.20215) | 📈 Highly cited |
| 2026-02-08 | Reinforcement Learning | [Process Rewards for Outcome-Guided Reasoning Steps in LLM Reinforcement Learning](https://arxiv.org/abs/2604.02341v2) | — |
| 2026-01-16 | Agent/LLM Self-Improvement | [ReCreate: Reasoning and Creating Domain Agents Driven by Experience](https://arxiv.org/abs/2601.11100v3) | 📈 Highly cited<br>🏆 CCF-A: Annual Meeting of the Association for Computational Linguistics<br>📣 Acceptance first observed: 2026-10-14 (actual acceptance date unverified) |

## 🚨 Priority Watch

| Paper | Signals | Venue / affiliation evidence |
| --- | --- | --- |
| [Memory-R2: Fair Credit Assignment for Long-Horizon Memory-Augmented LLM Agents](https://arxiv.org/abs/2605.21768v1) | 📈 Highly cited | Centre for Information and Language Processing, LMU Munich |
| [RecMem: Recurrence-based Memory Consolidation for Efficient and Effective Long-Running LLM Agents](https://arxiv.org/abs/2605.16045) | 📈 Highly cited<br>🏆 CCF-A: Annual Meeting of the Association for Computational Linguistics<br>📣 Acceptance first observed: 2026-10-03 (actual acceptance date unverified) | Semantic Scholar publication metadata: Annual Meeting of the Association for Computational Linguistics |
| [All-Mem: Agentic Lifelong Memory via Dynamic Topology Evolution](https://arxiv.org/abs/2603.19595) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Chronos: Temporal-Aware Conversational Agents with Structured Event Retrieval for Long-Term Memory](https://arxiv.org/abs/2603.16862) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Multi-Agent Memory from a Computer Architecture Perspective: Visions and Challenges Ahead](https://arxiv.org/abs/2603.10062) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Multi-Agent Debate with Memory Masking](https://arxiv.org/abs/2603.20215) | 📈 Highly cited | First author: Hong Kong Baptist University (Semantic Scholar author profiles) |
| [ReCreate: Reasoning and Creating Domain Agents Driven by Experience](https://arxiv.org/abs/2601.11100v3) | 📈 Highly cited<br>🏆 CCF-A: Annual Meeting of the Association for Computational Linguistics<br>📣 Acceptance first observed: 2026-10-14 (actual acceptance date unverified) | Semantic Scholar publication metadata: Annual Meeting of the Association for Computational Linguistics |

## Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement

### [Self-Improving Language Models with Bidirectional Evolutionary Search](https://arxiv.org/abs/2605.28814v2)

- **Authors:** Guowei Xu, Zhenting Qi, Huangyuan Su, Weirui Ye, Himabindu Lakkaraju, Sham M. Kakade, Yilun Du
- **Published:** 2026-05-27
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** Tsinghua University
- **Categories:** cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2605.28814v2) · [PDF](https://arxiv.org/pdf/2605.28814v2)

Search has been proposed as an effective method for self-improving language models and agentic systems, both for post-training sample generation and for inference. However, widely used methods such as best-of-N sampling and tree search face two fundamental limitations: they are guided by sparse verification signals, and they construct candidates primarily through autoregressive expansion, restricting exploration to regions with substantial model probability mass. To address these, we propose Bidirectional Evolutionary Search (BES), a search framework that couples forward candidate evolution with backward goal decomposition. In the forward search, BES augments standard expansion with evolution operators that recombine partial trajectories to generate candidates that are difficult to obtain from a single model rollout. In the backward search, BES recursively decomposes the original task into checkable sub-goals, producing dense intermediate feedback that guides forward search. We provide motivation illustrating that candidates generated by expansion-only search may be confined to a narrow entropy shell, while evolution operators may escape it. Experiments show that on challenging post-training tasks where mainstream post-training algorithms fail to improve, BES enables consistent gains. At inference time, BES outperforms existing open-source frameworks on three open problem solving benchmarks in both average and best-case performance, and outperforms majority voting and Monte Carlo Tree Search on mathematical reasoning and competitive programming benchmarks. Code and trained models are available at https://github.com/Embodied-Minds-Lab/BES.

### [ReCreate: Reasoning and Creating Domain Agents Driven by Experience](https://arxiv.org/abs/2601.11100v3)

- **Authors:** Zhezheng Hao, Hong Wang, Jian Luo, Jianqing Zhang, Yuyan Zhou, Qiang Lin, Can Wang, Hande Dong, Jiawei Chen
- **Published:** 2026-01-16
- **Priority:** 📈 Highly cited<br>🏆 CCF-A: Annual Meeting of the Association for Computational Linguistics<br>📣 Acceptance first observed: 2026-10-14 (actual acceptance date unverified)
- **Venue:** Annual Meeting of the Association for Computational Linguistics
- **Affiliations:** n/a
- **Categories:** cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2601.11100v3) · [PDF](https://arxiv.org/pdf/2601.11100v3)

Large Language Model (LLM) agents are reshaping the industrial landscape. However, most practical agents still rely on human-designed scaffolds, making their creation and adaptation across diverse domains labor-intensive. This situation poses a central question: can we automatically create and evolve domain agents through interaction experience in real-world environments? While recent approaches have sought to automate agent creation, several treat scaffold optimization as a black-box procedure guided primarily by final performance metrics. Such strategies overlook critical evidence explaining why an agent succeeds or fails and often incur high computational costs. To address these limitations, we propose ReCreate, an experience-driven framework for creating and evolving specialized domain agents. ReCreate systematically leverages agent interaction histories to identify the causes of success and failure and guide targeted scaffold updates. Specifically, we introduce an agent-as-optimizer paradigm in which an optimizer agent actively inspects execution experience and iteratively refines the task agent's scaffold through three key components: (i) an experience storage and retrieval mechanism for on-demand evidence inspection; (ii) a reasoning-creating synergy pipeline that translates execution evidence into updates to prompts, workflows, tools, and memory; and (iii) hierarchical updates that consolidate instance-level refinements into reusable domain-level improvements. Experiments across thirteen evaluation settings spanning four domains show that ReCreate consistently outperforms human-designed agents and existing automated agent generation and self-evolving baselines, even when evolving from minimal seed scaffolds.

## Agent Memory

### [Memory-R2: Fair Credit Assignment for Long-Horizon Memory-Augmented LLM Agents](https://arxiv.org/abs/2605.21768v1)

- **Authors:** Sikuan Yan, Ahmed Bahloul, Ercong Nie, Susanna Schwarzmann, Riccardo Trivisonno, Volker Tresp, Yunpu Ma
- **Published:** 2026-05-20
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** Centre for Information and Language Processing, LMU Munich
- **Categories:** cs.LG, cs.MA
- **Links:** [Paper](https://arxiv.org/abs/2605.21768v1) · [PDF](https://arxiv.org/pdf/2605.21768v1)

Memory-augmented LLM agents enable interactions that extend beyond finite context windows by storing, updating, and reusing information across sessions. However, training such agents with reinforcement learning in multi-session environments is challenging because memory turns the agent's past actions into part of its future environment. Once different rollouts write, update, or delete different memories, they no longer share the same intermediate memory state, making trajectory-level comparisons fundamentally unfair. This violates a key assumption behind group-relative methods such as GRPO, where rollouts are compared as if they were sampled from the same effective environment. Consequently, trajectory-level rewards provide noisy or biased credit signals for long-horizon memory operations. To address this challenge, we introduce Memory-R2, a training framework for long-horizon memory-augmented LLM agents. Its core algorithm, LoGo-GRPO, combines local and global group-relative optimization. The global objective preserves end-to-end learning from long-horizon trajectory-level rewards, while local rerollouts compare different memory-operation outcomes from the same intermediate memory state, yielding fairer group comparisons and more precise supervision for memory construction. Beyond credit assignment, Memory-R2 jointly optimizes memory formation and memory evolution with a shared-parameter co-learning design, where a fact extractor and a memory manager are instantiated from the same LLM backbone through role-specific prompts. To stabilize multi-step RL over long memory horizons, we adopt a progressive curriculum that increases the training horizon from 8 to 16 to 32 sessions. Together, these components provide an effective training paradigm for memory-augmented LLM agents in long-horizon multi-session settings.

### [RecMem: Recurrence-based Memory Consolidation for Efficient and Effective Long-Running LLM Agents](https://arxiv.org/abs/2605.16045)

- **Authors:** Dai, Zijie, Deng, Shiyuan, Guan, Sheng, Tian, Yizhou, Yao, Xin, Yan, Xiao, Cheng, James
- **Published:** 2026-05-15
- **Priority:** 📈 Highly cited<br>🏆 CCF-A: Annual Meeting of the Association for Computational Linguistics<br>📣 Acceptance first observed: 2026-10-03 (actual acceptance date unverified)
- **Venue:** Annual Meeting of the Association for Computational Linguistics
- **Affiliations:** n/a
- **Categories:** cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2605.16045) · [PDF](https://arxiv.org/pdf/2605.16045)

Memory systems often organize user-agent interactions as retrievable external memory and are crucial for long-running agents by overcoming the limited context windows of LLMs. However, existing memory systems invoke LLMs to process every incoming interaction for memory extraction, and such an eager memory consolidation scheme leads to substantial token consumption. To tackle this problem, we propose RecMem by rethinking when memory consolidation should be conducted. RecMem stores incoming interactions in a subconscious memory layer and encode them using lightweight embedding models for retrieval. LLMs are only invoked to extract episodic and semantic memory when sustained recurrence are observed for semantically similar interactions. Such recurrence-based consolidation works because these interactions correspond to a semantic cluster with rich information and thus are worth extraction and summarization. To improve accuracy, RecMem also incorporates a semantic refinement mechanism that recovers the fine-grained facts omitted by memory extraction. Experiments show that RecMem reduces the memory construction token cost of three SOTA memory systems by up to 87% while exceeding their accuracy.

### [All-Mem: Agentic Lifelong Memory via Dynamic Topology Evolution](https://arxiv.org/abs/2603.19595)

- **Authors:** Lv, Can, Chang, Heng, Tao, Shengyu, Chen, Mingju, Fan, Zhaoxin, Zhang, Ziwei, Guo, Yuchen, Zhou, Shiji
- **Published:** 2026-03-20
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.IR
- **Links:** [Paper](https://arxiv.org/abs/2603.19595) · [PDF](https://arxiv.org/pdf/2603.19595) · [Code](https://github.com/LvCan926/All-Mem)

Lifelong interactive agents are expected to assist users over months or years, which requires continually writing long term memories while retrieving the right evidence for each new query under fixed context and latency budgets. Existing memory systems often degrade as histories grow, yielding redundant, outdated, or noisy retrieved contexts. We present \textbf{All-Mem}, an online/offline lifelong memory framework that maintains a topology structured memory bank via explicit, non destructive consolidation, avoiding the irreversible information loss typical of summarization based compression. In online operation, it anchors retrieval on a bounded visible surface to keep coarse search cost bounded. Periodically offline, an LLM diagnoser proposes confidence scored topology edits executed with gating using three operators: Split, Merge, and Update, while preserving immutable evidence for traceability. At query time, typed links enable hop bounded, budgeted expansion from active anchors to archived evidence when needed. Experiments on \textbf{LoCoMo} and \textbf{LongMemEval-s} show improved retrieval and QA over representative baselines. The code is available at https://github.com/LvCan926/All-Mem.

### [Chronos: Temporal-Aware Conversational Agents with Structured Event Retrieval for Long-Term Memory](https://arxiv.org/abs/2603.16862)

- **Authors:** Sen, Sahil, Lumer, Elias, Gulati, Anmol, Subbiah, Vamse Kumar
- **Published:** 2026-03-17
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2603.16862) · [PDF](https://arxiv.org/pdf/2603.16862)

Recent advances in Large Language Models (LLMs) have enabled conversational AI agents to engage in extended multi-turn interactions spanning weeks or months. However, existing memory systems struggle to reason over temporally grounded facts and preferences that evolve across months of interaction and lack effective retrieval strategies for multi-hop, time-sensitive queries over long dialogue histories. We introduce Chronos, a novel temporal-aware memory framework that decomposes raw dialogue into subject-verb-object event tuples with resolved datetime ranges and entity aliases, indexing them in a structured event calendar alongside a turn calendar that preserves full conversational context. At query time, Chronos applies dynamic prompting to generate tailored retrieval guidance for each question, directing the agent on what to retrieve, how to filter across time ranges, and how to approach multi-hop reasoning through an iterative tool-calling loop over both calendars. We evaluate Chronos with 8 LLMs, both open-source and closed-source, on the LongMemEvalS benchmark comprising 500 questions spanning six categories of dialogue history tasks. Chronos Low achieves 92.60% and Chronos High scores 95.60% accuracy, setting a new state of the art with an improvement of 7.67% over the best prior system. Ablation results reveal the events calendar accounts for a 58.9% gain on the baseline while all other components yield improvements between 15.5% and 22.3%. Notably, Chronos Low alone surpasses prior approaches evaluated under their strongest model configurations.

### [Multi-Agent Memory from a Computer Architecture Perspective: Visions and Challenges Ahead](https://arxiv.org/abs/2603.10062)

- **Authors:** Yu, Zhongming, Yu, Naicheng, Zhang, Hejia, Ni, Wentao, Yin, Mingrui, Yang, Jiaying, Zhao, Yujie, Zhao, Jishen
- **Published:** 2026-03-09
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.AR
- **Links:** [Paper](https://arxiv.org/abs/2603.10062) · [PDF](https://arxiv.org/pdf/2603.10062)

As LLM agents evolve into collaborative multi-agent systems, their memory requirements grow rapidly in complexity. This position paper frames multi-agent memory as a computer architecture problem. We distinguish shared and distributed memory paradigms, propose a three-layer memory hierarchy (I/O, cache, and memory), and identify two critical protocol gaps: cache sharing across agents and structured memory access control. We argue that the most pressing open challenge is multi-agent memory consistency. Our architectural framing provides a foundation for building reliable, scalable multi-agent systems.

### [Multi-Agent Debate with Memory Masking](https://arxiv.org/abs/2603.20215)

- **Authors:** Tian, Hongduan, Feng, Xiao, Zhao, Ziyuan, Zhu, Xiangyu, Yan, Rolan, Han, Bo
- **Published:** 2026-03-03
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** Hong Kong Baptist University
- **Categories:** cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2603.20215) · [PDF](https://arxiv.org/pdf/2603.20215)

Large language models (LLMs) have recently demonstrated impressive capabilities in reasoning tasks. Currently, mainstream LLM reasoning frameworks predominantly focus on scaling up inference-time sampling to enhance performance. In particular, among all LLM reasoning frameworks, *multi-agent debate* (MAD), which employs multiple LLMs as agents to perform reasoning in the way of multi-round debate, has emerged as a powerful reasoning paradigm since it allows agents to access previous memories to alleviate fallacious content and refine their reasoning iteratively in each debate round. However, although MAD significantly improves the reasoning capabilities of LLMs, in this paper, we observe that there remain erroneous memories, and LLM agents are vulnerable to these erroneous memories. To explore this phenomenon, we provide a theoretical insight that the performance of MAD is highly dependent on the quality of memories derived from the previous debate, indicating that the existence of erroneous memories poses a threat to the performance of MAD. To address this problem, we introduce a simple yet effective multi-agent debate framework, *multi-agent debate with memory masking* (MAD-M$^2$), to improve the robustness of MAD by allowing LLM agents to mask erroneous memories from the previous debate round at the beginning of each debate round. In this way, MAD-M$^2$ can polish the contextual information before each debate round by preserving informative and meaningful memories while discarding the erroneous memories. Extensive experiments and analyses on mainstream mathematical and logical reasoning benchmarks demonstrate that MAD-M$^2$ can identify the erroneous memories and achieve better performance in reasoning than MAD.

## LLM Continual Training & Continual Learning

### [All-Mem: Agentic Lifelong Memory via Dynamic Topology Evolution](https://arxiv.org/abs/2603.19595)

- **Authors:** Lv, Can, Chang, Heng, Tao, Shengyu, Chen, Mingju, Fan, Zhaoxin, Zhang, Ziwei, Guo, Yuchen, Zhou, Shiji
- **Published:** 2026-03-20
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.IR
- **Links:** [Paper](https://arxiv.org/abs/2603.19595) · [PDF](https://arxiv.org/pdf/2603.19595) · [Code](https://github.com/LvCan926/All-Mem)

Lifelong interactive agents are expected to assist users over months or years, which requires continually writing long term memories while retrieving the right evidence for each new query under fixed context and latency budgets. Existing memory systems often degrade as histories grow, yielding redundant, outdated, or noisy retrieved contexts. We present \textbf{All-Mem}, an online/offline lifelong memory framework that maintains a topology structured memory bank via explicit, non destructive consolidation, avoiding the irreversible information loss typical of summarization based compression. In online operation, it anchors retrieval on a bounded visible surface to keep coarse search cost bounded. Periodically offline, an LLM diagnoser proposes confidence scored topology edits executed with gating using three operators: Split, Merge, and Update, while preserving immutable evidence for traceability. At query time, typed links enable hop bounded, budgeted expansion from active anchors to archived evidence when needed. Experiments on \textbf{LoCoMo} and \textbf{LongMemEval-s} show improved retrieval and QA over representative baselines. The code is available at https://github.com/LvCan926/All-Mem.

## Reinforcement Learning

### [Improving Heart-Focused Medical Question Answering in LLMs via Variance-Aware Rubric Rewards with GRPO](https://arxiv.org/abs/2606.05174v2)

- **Authors:** Arash Ahmadi, Parisa Masnadi Khiabani, Sarah Sharif, Charles Nicholson, David Ebert, Aswathy K. Vaikom House, Mike Banad
- **Published:** 2026-04-17
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.CL, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2606.05174v2) · [PDF](https://arxiv.org/pdf/2606.05174v2)

Large language models can support medical question answering, but privacy, cost, and reliability still limit their clinical use in focused domains. Can rubric-based reinforcement learning bring a locally deployable model close to much larger systems? We study Group Relative Policy Optimization (GRPO) for heart-focused medical question answering with rubric supervision from RaR-Medicine. Rather than rely on binary rubric aggregation or a single overall score, our variance-aware reward framework builds continuous rewards from criterion-level outcomes. It preserves partial credit and reduces reward sparsity. We adapt a Qwen3-14B policy with low-rank adapters and quantized weights. On a held-out heart-related HealthBench subset, the best GRPO variant improves accuracy from 0.362 to 0.502 and F1 from 0.532 to 0.668 over the base model, close to GPT-OSS-120B. An independent clinician rated most responses clinically acceptable (61%) and patient ready (63%), both above the automated accuracy; fewer than 2% were unsafe. Taken together, the results support rubric-based reinforcement learning as a practical route for focused medical language models.

### [Process Rewards for Outcome-Guided Reasoning Steps in LLM Reinforcement Learning](https://arxiv.org/abs/2604.02341v2)

- **Authors:** Mohammad Rezaei, Jens Lehmann, Sahar Vahdati
- **Published:** 2026-02-08
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2604.02341v2) · [PDF](https://arxiv.org/pdf/2604.02341v2)

Mathematical reasoning in large language models has improved substantially with reinforcement learning using verifiable rewards, where final answers can be checked automatically and converted into reliable training signals. Most such pipelines optimize outcome correctness only, which yields sparse feedback for long, multi-step solutions and offers limited guidance on intermediate reasoning errors. Recent work therefore introduces process reward models (PRMs) to score intermediate steps and provide denser supervision. In practice, PRM scores are often imperfectly aligned with final correctness and can reward locally fluent reasoning that still ends in an incorrect answer. When optimized as absolute rewards, such signals can amplify fluent failure modes and induce reward hacking. We propose PROGRS, a framework that leverages PRMs while keeping outcome correctness dominant. PROGRS treats process rewards as relative preferences within outcome groups rather than absolute targets. We introduce outcome-conditioned centering, which shifts PRM scores of incorrect trajectories to have zero mean within each prompt group. It removes systematic bias while preserving informative rankings. PROGRS combines a frozen quantile-regression PRM with a multi-scale coherence evaluator. We integrate the resulting centered process bonus into Group Relative Policy Optimization (GRPO) without auxiliary objectives or additional trainable components. Across MATH-500, AMC, AIME, MinervaMath, and OlympiadBench, PROGRS consistently improves Pass@1 over outcome-only baselines and achieves stronger performance with fewer rollouts. These results show that outcome-conditioned centering enables safe and effective use of process rewards for mathematical reasoning.

## Long-Horizon Task Agents

### [Memory-R2: Fair Credit Assignment for Long-Horizon Memory-Augmented LLM Agents](https://arxiv.org/abs/2605.21768v1)

- **Authors:** Sikuan Yan, Ahmed Bahloul, Ercong Nie, Susanna Schwarzmann, Riccardo Trivisonno, Volker Tresp, Yunpu Ma
- **Published:** 2026-05-20
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** Centre for Information and Language Processing, LMU Munich
- **Categories:** cs.LG, cs.MA
- **Links:** [Paper](https://arxiv.org/abs/2605.21768v1) · [PDF](https://arxiv.org/pdf/2605.21768v1)

Memory-augmented LLM agents enable interactions that extend beyond finite context windows by storing, updating, and reusing information across sessions. However, training such agents with reinforcement learning in multi-session environments is challenging because memory turns the agent's past actions into part of its future environment. Once different rollouts write, update, or delete different memories, they no longer share the same intermediate memory state, making trajectory-level comparisons fundamentally unfair. This violates a key assumption behind group-relative methods such as GRPO, where rollouts are compared as if they were sampled from the same effective environment. Consequently, trajectory-level rewards provide noisy or biased credit signals for long-horizon memory operations. To address this challenge, we introduce Memory-R2, a training framework for long-horizon memory-augmented LLM agents. Its core algorithm, LoGo-GRPO, combines local and global group-relative optimization. The global objective preserves end-to-end learning from long-horizon trajectory-level rewards, while local rerollouts compare different memory-operation outcomes from the same intermediate memory state, yielding fairer group comparisons and more precise supervision for memory construction. Beyond credit assignment, Memory-R2 jointly optimizes memory formation and memory evolution with a shared-parameter co-learning design, where a fact extractor and a memory manager are instantiated from the same LLM backbone through role-specific prompts. To stabilize multi-step RL over long memory horizons, we adopt a progressive curriculum that increases the training horizon from 8 to 16 to 32 sessions. Together, these components provide an effective training paradigm for memory-augmented LLM agents in long-horizon multi-session settings.
