> **115 papers** · Page 3/3 · Newest first across all pages

[1](../2026-10-13.md) · [2](page-002.md) · [3](page-003.md)

# Daily Papers · 2026-10-13

> Prepared **15** new, promoted, or retried paper(s) across four research tracks plus explicitly requested papers. Lists are newest publication first.
> Catch-up window: **2026-10-07T15:36:34.161200+08:00** → **2026-10-13T19:01:05.125248+08:00**.

[← Back to index](../../../../README.md)

## All Updates · Newest First

| Published | Track | Paper | Signals |
| --- | --- | --- | --- |
| 2026-04-16 | Agent/LLM Self-Improvement | [Autogenesis: A Self-Evolving Agent Protocol](https://arxiv.org/abs/2604.15034v6) | 📈 Highly cited |
| 2026-04-15 | Agent/LLM Self-Improvement, Reinforcement Learning | [FiRe: Fine-grained Multimodal Reasoning for Enhanced Image Generation](https://arxiv.org/abs/2604.13491v4) | 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-10-13 (actual acceptance date unverified) |
| 2026-04-13 | Reinforcement Learning | [OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems](https://arxiv.org/abs/2604.11477v2) | — |
| 2026-04-09 | Agent/LLM Self-Improvement | [A Relative-Computability Theory of Self-Improving Agents](https://arxiv.org/abs/2605.27381v3) | — |
| 2026-04-09 | Reinforcement Learning | [An Imperfect Verifier is Good Enough: Learning with Noisy Rewards](https://arxiv.org/abs/2604.07666v2) | 📈 Highly cited |
| 2026-03-17 | Agent/LLM Self-Improvement | [Large Reward Models: Generalizable Online Robot Reward Generation with Vision-Language Models](https://arxiv.org/abs/2603.16065v3) | 📈 Highly cited |
| 2026-03-09 | Reinforcement Learning | [Agentic Critical Training](https://arxiv.org/abs/2603.08706v2) | — |
| 2026-03-06 | Reinforcement Learning | [CORE-Seg: Reasoning-Driven Segmentation for Complex Lesions via Reinforcement Learning](https://arxiv.org/abs/2603.05911v2) | — |
| 2026-02-12 | Reinforcement Learning | [Any House Any Task: Scalable Long-Horizon Planning for Abstract Human Tasks](https://arxiv.org/abs/2602.12244v3) | — |
| 2026-01-30 | Reinforcement Learning | [Why GRPO Needs Normalization: A Local-Curvature Perspective on Adaptive Gradients](https://arxiv.org/abs/2601.23135v2) | 📈 Highly cited |
| 2025-10-01 | Reinforcement Learning | [Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers](https://arxiv.org/abs/2510.00915v5) | 📈 Highly cited |
| 2025-09-23 | LLM Continual Training | [Robotic Ultra-Long-Horizon Manipulation Skills via Human-guided Lifelong Code Generation](https://arxiv.org/abs/2509.18597v3) | — |
| 2025-08-11 | LLM Continual Training | [Optimal Transport Depth Up-Scaling](https://arxiv.org/abs/2508.08011v2) | — |
| 2025-08-04 | Reinforcement Learning | [TIC-GRPO: Provable and Efficient Optimization for Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2508.02833v7) | 📈 Highly cited |
| 2025-07-20 | Reinforcement Learning | [AgentFly: Scaling Agentic Reinforcement Learning with Unified Resource System](https://arxiv.org/abs/2507.14897v2) | — |

## 🚨 Priority Watch

| Paper | Signals | Venue / affiliation evidence |
| --- | --- | --- |
| [Autogenesis: A Self-Evolving Agent Protocol](https://arxiv.org/abs/2604.15034v6) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [FiRe: Fine-grained Multimodal Reasoning for Enhanced Image Generation](https://arxiv.org/abs/2604.13491v4) | 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-10-13 (actual acceptance date unverified) | arXiv comment: Accepted to NeurIPS 2026 |
| [An Imperfect Verifier is Good Enough: Learning with Noisy Rewards](https://arxiv.org/abs/2604.07666v2) | 📈 Highly cited | First author: ETH Zurich (Semantic Scholar author profiles) |
| [Large Reward Models: Generalizable Online Robot Reward Generation with Vision-Language Models](https://arxiv.org/abs/2603.16065v3) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Why GRPO Needs Normalization: A Local-Curvature Perspective on Adaptive Gradients](https://arxiv.org/abs/2601.23135v2) | 📈 Highly cited | Verified metrics snapshot; see Metrics |
| [Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers](https://arxiv.org/abs/2510.00915v5) | 📈 Highly cited | RIKEN Center for Advanced Intelligence Project |
| [TIC-GRPO: Provable and Efficient Optimization for Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2508.02833v7) | 📈 Highly cited | Verified metrics snapshot; see Metrics |

## Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement

### [Autogenesis: A Self-Evolving Agent Protocol](https://arxiv.org/abs/2604.15034v6)

- **Authors:** Wentao Zhang, Zhe Zhao, Haibin Wen, Yingcheng Wu, Cankun Guo, Ming Yin, Bo An
- **Published:** 2026-04-16
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2604.15034v6) · [PDF](https://arxiv.org/pdf/2604.15034v6)

LLM-based agent systems can adapt by revising prompts, constructing tools, and changing other runtime resources. Managing these heterogeneous updates requires a shared lifecycle for identifying targets, assessing candidates, and retaining accepted versions, complementing communication protocols such as A2A and MCP. We introduce AUTOGENESIS PROTOCOL (AGP), which decouples what evolves from how updates are proposed. Its Resource Substrate Protocol Layer (RSPL) represents prompts, agents, tools, environments, and memory as protocol-registered resources with explicit state and versioned interfaces. Its Self-Evolution Protocol Layer (SEPL) specifies candidate proposal, assessment, and commit, with auditable histories and support for restoring retained resource states. We instantiate AGP in AUTOGENESIS SYSTEM (AGS), a self-evolving multi-agent system that retrieves, instantiates, and refines resources during execution. Across reasoning, tool-use, and coding benchmarks, AGS improves over its non-evolving configuration, and repeated reasoning runs report the accompanying output-token cost. Execution cases show a shared update lifecycle across all five resource types.

### [FiRe: Fine-grained Multimodal Reasoning for Enhanced Image Generation](https://arxiv.org/abs/2604.13491v4)

- **Authors:** Yongjin Kim, Yoonjin Oh, Yerin Kim, Hyomin Kim, Jeeyoung Yun, Yujung Heo, Minjun Kim, Sungwoong Kim
- **Published:** 2026-04-15
- **Priority:** 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-10-13 (actual acceptance date unverified)
- **Venue:** NeurIPS 2026
- **Affiliations:** n/a
- **Categories:** cs.CV
- **Links:** [Paper](https://arxiv.org/abs/2604.13491v4) · [PDF](https://arxiv.org/pdf/2604.13491v4)

With the rapid progress of Multimodal Large Language Models (MLLMs), unified MLLMs that jointly perform image understanding and generation have advanced significantly. However, despite the inherent reasoning capabilities of unified MLLMs for self-reflection and self-refinement, their use in text-to-image generation remains largely underexplored. Meanwhile, existing multimodal reasoning-based image generation methods mostly rely on prompt augmentation or holistic image-text alignment judgments, without fine-grained reflection and refinement of detailed prompt attributes, leading to limited fine-grained control. To address this limitation, we propose FiRe, a Fine-grained Multimodal Reasoning method for enhanced image generation by MLLM. In specific, FiRe performs a fine-grained multi-step reasoning by first decomposing the prompt into key visual requirements and then self-judging their satisfaction in the generated image, followed by localized refinement according to self-generated precise feedback. In addition, to further strengthen the MLLM's multimodal reasoning ability, we introduce FiRe-GRPO, a reinforcement learning method tailored to FiRe. Since standard Group Relative Policy Optimization (GRPO) suffers from sparse, outcome-based rewards in multi-step reasoning, we formulate our reasoning process as a step-level decision-making problem, design step-specific rewards, and compute step-level advantages for granular credit assignment within GRPO. Extensive experiments demonstrate that FiRe consistently outperforms competitive text-to-image baselines, including existing reasoning-based methods, with particularly substantial gains on compositional text-to-image benchmarks. Our project page is available at https://ku-agi.github.io/FiRe/

### [A Relative-Computability Theory of Self-Improving Agents](https://arxiv.org/abs/2605.27381v3)

- **Authors:** Chien-Ping Lu
- **Published:** 2026-04-09
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.CC, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2605.27381v3) · [PDF](https://arxiv.org/pdf/2605.27381v3)

Agents increasingly modify the procedures by which they solve tasks and improve themselves. Autonomy over improvement, gains in practical capability, and enlargement of computational reach are distinct properties. We develop an oracle-relative model with mutable solvers, evaluators, and improvers. Uniform simulation keeps every total decision procedure produced by effective self-revision over $A$ within $\mathcal{C}(A)=\{D:D\leq_T A\}$; oracle joins account for additional access, while the relativized limit lemma separates limiting answers from effective completion. A worked model of Boolean rule acquisition makes the distinction constructive. For a known finite-dimensional feature language, we characterize exactly which answers a query history determines, obtain a sharp teacher-query bound, and give a terminating protocol that permits revisions to the query proposer. The learned solver can dispense with the teacher on every input while remaining in the same computability layer. However, uniformly constructing the required feature-span specification from arbitrary effective feature programs is already as hard as the relative halting problem. We also give a conditional criterion for strict ascent and distinguish it from finite behavioral evidence. The framework thus separates acquisition, certification, and computability ascent, identifying both a positive route to verified support removal and the assumptions on which it depends.

### [Large Reward Models: Generalizable Online Robot Reward Generation with Vision-Language Models](https://arxiv.org/abs/2603.16065v3)

- **Authors:** Yanru Wu, Weiduo Yuan, Esteban Martinez Licon, Ang Qi, Vitor Guizilini, Jiageng Mao, Yue Wang
- **Published:** 2026-03-17
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.RO, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2603.16065v3) · [PDF](https://arxiv.org/pdf/2603.16065v3)

Reinforcement Learning (RL) has shown strong potential for improving robotic manipulation policies, yet its practical use remains bottlenecked by the difficulty of specifying reward functions that are both semantically meaningful and reusable across tasks. In this paper, we propose Large Reward Models (LRMs), a framework that adapts foundation VLMs into frame-level reward generators for robot policy refinement. We specialize a state-of-the-art VLM on a multi-source dataset spanning real-world robot trajectories, human-object interactions, and simulated manipulation environments. Unlike prior approaches that mainly evaluate trajectories post-hoc, LRMs expose multiple reward interfaces from visual observations: progress estimation, task completion, and temporal contrastive comparison. Starting from an imitation-learned policy, we use these VLM-derived rewards to guide PPO refinement on held-out long-horizon manipulation tasks. Our experiments show that LRM progress rewards provide the strongest non-privileged online refinement signal, improving the IL baseline and narrowing the gap to privileged environment rewards. We further deploy progress rewards for progress-weighted behavioral cloning on four real-world manipulation tasks spanning two robot platforms, improving over SFT on all four tasks. These results suggest that modality-specific specialization of foundation VLMs can provide practical visual reward signals for both simulated policy refinement and physical robot self-improvement without hand-coded task rewards.

## LLM Continual Training & Continual Learning

### [Robotic Ultra-Long-Horizon Manipulation Skills via Human-guided Lifelong Code Generation](https://arxiv.org/abs/2509.18597v3)

- **Authors:** Yuan Meng, Zhenguo Sun, Max Fest, Xiangtong Yao, Xukun Li, Zhenshan Bing, Alois Knoll
- **Published:** 2025-09-23
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.RO
- **Links:** [Paper](https://arxiv.org/abs/2509.18597v3) · [PDF](https://arxiv.org/pdf/2509.18597v3)

Large language models (LLMs) can translate natural-language instructions for robotic manipulation into executable code, but ambiguity, noisy generations, and limited context windows make ultra-long-horizon tasks unreliable. Closed-loop approaches that rely only on LLM feedback also struggle because LLMs have limited robotic reasoning, even when task errors are obvious to humans. Feedback is often stored in representations that generalize poorly to unseen tasks and can cause catastrophic forgetting as new corrections accumulate. We propose LYRA, a human-guided lifelong skill learning and code generation framework that distills human feedback into modular, reusable skills and incrementally extends their functionality across successive interactions while preserving previously learned behavior. External memory stores learned skills and execution examples; retrieval-augmented generation selects relevant knowledge, while user hints guide reuse when retrieval is insufficient, supporting ultra-long-horizon execution. Experiments on Ravens, Franka Kitchen, LIBERO-long, MetaWorld, and real-world tasks show a 0.93 success rate, up to 27\% higher than baselines, and a 42\% improvement in correction efficiency. LYRA also robustly solves ``build a house'', which requires planning over 20 primitives.

### [Optimal Transport Depth Up-Scaling](https://arxiv.org/abs/2508.08011v2)

- **Authors:** Mingzi Cao, Xi Wang, Nikolaos Aletras
- **Published:** 2025-08-11
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** University of Sheffield
- **Categories:** cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2508.08011v2) · [PDF](https://arxiv.org/pdf/2508.08011v2)

Pre-training Large Language Models (LLMs) from scratch at larger scales yields remarkable performance but incurs substantially high training costs. Depth up-scaling provides an efficient alternative by inserting new layers into a pre-trained LLM, avoiding training from scratch. However, most existing methods copying or averaging base layers for new layer, which misalign functionally corresponding neurons, leading to neuron permutation mismatch that harms performance. To address this issue, we propose Optimal Transport Depth Up-Scaling (OT-DUS), which leverages Optimal Transport (OT) theory to align and fuse functionally corresponding neurons module by module in adjacent base layers for new layer construction. OT-DUS achieves better overall performance in both general and specialized domains than existing methods for continual pre-training and supervised fine-tuning across different model sizes and model families. Our analysis of insertion strategies further finds that inserting new layers at higher positions yields not only stronger performance but also improved training efficiency.

## Reinforcement Learning

### [FiRe: Fine-grained Multimodal Reasoning for Enhanced Image Generation](https://arxiv.org/abs/2604.13491v4)

- **Authors:** Yongjin Kim, Yoonjin Oh, Yerin Kim, Hyomin Kim, Jeeyoung Yun, Yujung Heo, Minjun Kim, Sungwoong Kim
- **Published:** 2026-04-15
- **Priority:** 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-10-13 (actual acceptance date unverified)
- **Venue:** NeurIPS 2026
- **Affiliations:** n/a
- **Categories:** cs.CV
- **Links:** [Paper](https://arxiv.org/abs/2604.13491v4) · [PDF](https://arxiv.org/pdf/2604.13491v4)

With the rapid progress of Multimodal Large Language Models (MLLMs), unified MLLMs that jointly perform image understanding and generation have advanced significantly. However, despite the inherent reasoning capabilities of unified MLLMs for self-reflection and self-refinement, their use in text-to-image generation remains largely underexplored. Meanwhile, existing multimodal reasoning-based image generation methods mostly rely on prompt augmentation or holistic image-text alignment judgments, without fine-grained reflection and refinement of detailed prompt attributes, leading to limited fine-grained control. To address this limitation, we propose FiRe, a Fine-grained Multimodal Reasoning method for enhanced image generation by MLLM. In specific, FiRe performs a fine-grained multi-step reasoning by first decomposing the prompt into key visual requirements and then self-judging their satisfaction in the generated image, followed by localized refinement according to self-generated precise feedback. In addition, to further strengthen the MLLM's multimodal reasoning ability, we introduce FiRe-GRPO, a reinforcement learning method tailored to FiRe. Since standard Group Relative Policy Optimization (GRPO) suffers from sparse, outcome-based rewards in multi-step reasoning, we formulate our reasoning process as a step-level decision-making problem, design step-specific rewards, and compute step-level advantages for granular credit assignment within GRPO. Extensive experiments demonstrate that FiRe consistently outperforms competitive text-to-image baselines, including existing reasoning-based methods, with particularly substantial gains on compositional text-to-image benchmarks. Our project page is available at https://ku-agi.github.io/FiRe/

### [OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems](https://arxiv.org/abs/2604.11477v2)

- **Authors:** Kun Liu, Liqun Chen
- **Published:** 2026-04-13
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.AI, cs.SE, q-fin.TR
- **Links:** [Paper](https://arxiv.org/abs/2604.11477v2) · [PDF](https://arxiv.org/pdf/2604.11477v2)

The alignment of Multi-Agent Systems (MAS) for autonomous software engineering is constrained by evaluator epistemic uncertainty. Current paradigms, such as Reinforcement Learning from Human Feedback (RLHF) and AI Feedback (RLAIF), frequently induce model sycophancy, while execution-based environments suffer from adversarial "Test Evasion" by unconstrained agents. In this paper, we introduce an objective alignment paradigm: Out-of-Money Reinforcement Learning (OOM-RL). By deploying agents into the non-stationary, high-friction reality of live financial markets, we utilize critical capital depletion as an externally imposed negative gradient. Our longitudinal 20-month empirical study chronicles the system's evolution from a high-turnover, sycophantic baseline to a robust, liquidity-aware architecture. We show that the economic consequences of financial loss---real execution costs, slippage, and capital depletion---exposed failure modes not apparent under internal evaluation alone and motivated architectural and governance changes that were later formalized as the Strict Test-Driven Agentic Workflow (STDAW), a Byzantine-inspired uni-directional state lock (RO-Lock) anchored to a deterministically verified >= 95% code coverage constraint matrix. During the final 94-trading-day observation window, the production system exhibited improved execution-aware performance, including an annualized Sharpe ratio of approximately 2.06. These financial results are observational and temporally bounded; they should not be interpreted as evidence of persistent investment alpha or as a causal estimate of STDAW's contribution. The primary contribution of this work is the use of externally imposed economic consequences as an epistemic constraint on agentic development, laying the groundwork for generalized paradigms where real-world resource depletion acts as an objective physical constraint.

### [An Imperfect Verifier is Good Enough: Learning with Noisy Rewards](https://arxiv.org/abs/2604.07666v2)

- **Authors:** Andreas Plesner, Francisco Guzmán, Anish Athalye
- **Published:** 2026-04-09
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** ETH Zurich, MIT
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2604.07666v2) · [PDF](https://arxiv.org/pdf/2604.07666v2)

Reinforcement Learning with Verifiable Rewards (RLVR) is widely used for post-training Large Language Models, but practical verifiers can make errors. We study how the rate and structure of reward noise affect RLVR in code generation, with a preliminary scientific-reasoning check. In multi-seed Qwen3 8B experiments on MBPP, mean validation reward over two fixed late evaluations is within 1 percentage point of the clean baseline at the tested resampled group-rollout noise rates through 20%, and within about 2 points at 30%. Confidence intervals allow larger losses; these point estimates do not establish a general tolerance threshold. We also examine full-program pass@k, four controlled noise structures, two model-based verifiers, and policy models from three families spanning 4B-9B parameters. We derive conditional advantage distributions for symmetric and asymmetric group noise, including retained format penalties, and show why clipping limits simple gradient-scaling arguments. The analysis identifies information preserved by whole-group corruption and limits on interpreting our asymmetric sweep as a precision-recall comparison. Overall, the results indicate that imperfect verification can support effective RLVR in the tested settings, while aggregate error rates alone do not characterize the learning signal.

### [Agentic Critical Training](https://arxiv.org/abs/2603.08706v2)

- **Authors:** Weize Liu, Minghui Liu, Sy-Tuyen Ho, Yongkyun Lee, Andrew Adams Schoen, Souradip Chakraborty, Xiyao Wang, Furong Huang
- **Published:** 2026-03-09
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** Zhejiang University
- **Categories:** cs.AI, cs.CL, cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2603.08706v2) · [PDF](https://arxiv.org/pdf/2603.08706v2)

Imitation learning (IL) teaches language-model agents to reproduce expert actions but not to distinguish them from plausible mistakes. Self-reflection methods expose models to alternatives yet use supervised fine-tuning (SFT) to imitate fixed rationales and actions. We introduce Agentic Critical Training (ACT), which uses reinforcement learning with verifiable rewards (RLVR) to train models to judge actions directly. At each expert-trajectory state, ACT pairs an expert action with an alternative sampled from the initial policy and randomizes their order. The model generates its own reasoning but is rewarded only for selecting the expert action. ACT reuses demonstrations, requires no reference rationales, and allows pair reuse across model sizes. ACT is a warm-up before IL, optionally followed by RL; inference requires no candidate comparison. Across Qwen3-8B and Olmo-3-7B-Instruct on ALFWorld-ID, WebShop, and ScienceWorld, ACT yields average gains of 5.85 points over IL and 4.12 points over IL$\to$RL without ACT, while also improving ALFWorld-OOD. With Olmo on ScienceWorld, the full pipeline gains 15.36 points over CoT prompting and 9.23 points over IL$\to$RL without ACT. Both ACT$\to$IL and the full pipeline outperform supervised reflection baselines. Controls with fixed pairs or matched training durations show that the gains stem from the ACT objective rather than additional data or training. Without reasoning-specific post-training, the standalone ACT checkpoint achieves the highest mean among evaluated models on MATH-500 and GPQA-Diamond, showing that action comparison complements generation.

### [CORE-Seg: Reasoning-Driven Segmentation for Complex Lesions via Reinforcement Learning](https://arxiv.org/abs/2603.05911v2)

- **Authors:** Yuxin Xie, Yuming Chen, Yishan Yang, Yi Zhou, Tao Zhou, Zhen Zhao, Jiacheng Liu, Huazhu Fu
- **Published:** 2026-03-06
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.CV, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2603.05911v2) · [PDF](https://arxiv.org/pdf/2603.05911v2)

Medical image segmentation is undergoing a paradigm shift from conventional visual pattern matching to cognitive reasoning analysis. Although Multimodal Large Language Models (MLLMs) have shown promise in integrating linguistic and visual knowledge, significant gaps remain: existing general MLLMs possess broad common sense but lack the specialized visual reasoning required for complex lesions, whereas traditional segmentation models excel at pixel-level segmentation but lack logical interpretability. In this paper, we introduce ComLesion-14K, the first diverse Chain-of-Thought (CoT) benchmark for reasoning-driven complex lesion segmentation. To accomplish this task, we propose CORE-Seg, an end-to-end framework integrating reasoning with segmentation through a Semantic-Guided Prompt Adapter. We design a progressive training strategy from SFT to GRPO, equipped with an adaptive dual-granularity reward mechanism to mitigate reward sparsity. Our Method achieves state-of-the-art results with a mean Dice of 37.06\% (14.89\% higher than the second-best baseline), while reducing the failure rate to 18.42\%. Project Page: https://xyxl024.github.io/CORE-Seg.github.io/

### [Any House Any Task: Scalable Long-Horizon Planning for Abstract Human Tasks](https://arxiv.org/abs/2602.12244v3)

- **Authors:** Zhihong Liu, Yang Li, Rengming Huang, Cewu Lu, Panpan Cai
- **Published:** 2026-02-12
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.RO
- **Links:** [Paper](https://arxiv.org/abs/2602.12244v3) · [PDF](https://arxiv.org/pdf/2602.12244v3)

Open world language conditioned task planning is crucial for robots operating in large-scale household environments. While many recent works attempt to address this problem using Large Language Models (LLMs) via prompting or training, a key challenge remains scalability. Performance often degrades rapidly with increasing environment size, plan length, instruction ambiguity, and constraint complexity. In this work, we propose Any House Any Task (AHAT), a household task planner optimized for long-horizon planning in large environments given ambiguous human instructions. At its core, AHAT utilizes an LLM trained to map task instructions and textual scene graphs into grounded subgoals defined in the Planning Domain Definition Language (PDDL). These subgoals are subsequently solved to generate feasible and optimal long-horizon plans through explicit symbolic reasoning. To enhance the model's ability to decompose complex and ambiguous intentions, we introduce TGPO, a novel reinforcement learning algorithm that integrates external correction of intermediate reasoning traces into Group Relative Policy Optimization (GRPO). Experiments demonstrate that AHAT achieves significant performance gains over state-of-the-art prompting, planning, and learning methods, particularly in human-style household tasks characterized by brief instructions but requiring complex execution plans.

### [Why GRPO Needs Normalization: A Local-Curvature Perspective on Adaptive Gradients](https://arxiv.org/abs/2601.23135v2)

- **Authors:** Cheng Ge, Caitlyn Heqi Yin, Hao Liang, Jiawei Zhang
- **Published:** 2026-01-30
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2601.23135v2) · [PDF](https://arxiv.org/pdf/2601.23135v2)

Reinforcement learning (RL) has become a key driver of language model reasoning. Among RL algorithms, Group Relative Policy Optimization (GRPO) is the de facto standard, avoiding the need for a critic by using per-prompt baselines and variance normalization. Yet why and when this normalization helps remains unclear. In this work, we answer both questions through the lens of local curvature of the sequence-level policy gradient: standard deviation normalization implements an adaptive gradient. Theoretically, we prove that under mild conditions GRPO attains an improved convergence rate over unnormalized REINFORCE, with gains characterized by the average within-prompt reward standard deviation across prompts and iterations. We further introduce IS-GRPO, an importance-sampling variant of GRPO whose expected update remains aligned with the full gradient, and prove a convergence guarantee of the same form as REINFORCE's, which is tighter in practice during real training runs by a factor we measure. Empirically, on GSM8K and MATH we validate the curvature--variance link and measure the quantities that govern our bounds along real training runs. At 1.5B scale, per-prompt normalization outperforms both unnormalized and globally normalized baselines, with gains that emerge in a middle phase of training where per-prompt variances become heterogeneous. At 7B scale, the normalization schemes become statistically indistinguishable while IS-GRPO retains a small lead, in line with the theory's prediction that the gains require heterogeneity.

### [Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers](https://arxiv.org/abs/2510.00915v5)

- **Authors:** Xin-Qiang Cai, Wei Wang, Feng Liu, Tongliang Liu, Gang Niu, Masashi Sugiyama
- **Published:** 2025-10-01
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** RIKEN Center for Advanced Intelligence Project
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2510.00915v5) · [PDF](https://arxiv.org/pdf/2510.00915v5)

Reinforcement Learning with Verifiable Rewards (RLVR) replaces costly human labeling with automated verifiers. To reduce verifier hacking, many RLVR systems binarize rewards to $\{0,1\}$, but imperfect verifiers inevitably introduce \emph{false negatives} (rejecting correct answers) and \emph{false positives} (accepting incorrect ones). We formalize verifier unreliability as a stochastic reward channel with asymmetric noise rates $ρ_0$ and $ρ_1$ -- the FP rate and the FN rate, respectively. From this abstraction we derive two lightweight corrections: (i) a \emph{backward} correction that yields an unbiased surrogate reward and thus an unbiased policy-gradient estimator in expectation, and (ii) a \emph{forward} correction that reweights score-function terms so the expected update aligns with the clean gradient direction and requires only the FN rate. We implement both as lightweight hooks in a group relative policy optimization pipeline, both corrections improve RLVR for math reasoning under synthetic and real verifier noise, with the forward variant being more stable under heavier noise. Finally, an appeals mechanism with a lightweight LLM verifier estimates the FN rate online and further improves performance.

### [TIC-GRPO: Provable and Efficient Optimization for Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2508.02833v7)

- **Authors:** Lei Pang, Jun Luo, Ruinan Jin
- **Published:** 2025-08-04
- **Priority:** 📈 Highly cited
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2508.02833v7) · [PDF](https://arxiv.org/pdf/2508.02833v7)

Group Relative Policy Optimization (GRPO) trains language models without a value critic using rewards centered within sampled response groups. We study how importance weighting, clipping, and length normalization affect its stochastic updates and propose Trajectory-level Importance-Corrected GRPO (TIC-GRPO), combining an upper importance-ratio cap with a full-trajectory likelihood ratio. Under common maximum-length normalization, a trajectory change of measure gives a score second moment proportional to the response horizon. We propagate this estimate through the actual empirical baseline and all inner updates. With separately optimized constant steps, the sampling term in TIC's stationarity bound has a linear horizon coefficient, versus order three halves for token-level GRPO$_2$. Matching upper and lower bounds separate the capped methods' worst-case response-level variances by a factor $T$. The bounds track prompt count, response-group size, vocabulary size, reward scale, and score regularity; per-response-normalized GRPO also retains a length-covariance term. Experiments at two Qwen3 scales on four reasoning and coding benchmarks evaluate both mechanisms in sampled-token-normalized training.

### [AgentFly: Scaling Agentic Reinforcement Learning with Unified Resource System](https://arxiv.org/abs/2507.14897v2)

- **Authors:** Renxi Wang, Rifo Ahmad Genadi, Bilal El Bouardi, Yongxin Wang, Fajri Koto, Zhengzhong Liu, Timothy Baldwin, Haonan Li
- **Published:** 2025-07-20
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** MBZUAI
- **Categories:** cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2507.14897v2) · [PDF](https://arxiv.org/pdf/2507.14897v2)

Methods to build LLM agents have evolved from prompt engineering and supervised finetuning to agentic reinforcement learning (agentic RL). However, agentic RL remains bottlenecked by its surrounding systems: agents must interact with heterogeneous environments, such as sandboxes, model services, and external APIs. Their allocation, reuse, and lifecycle dominate rollout cost and cap the scale at which training becomes practical. In this work, we present AgentFly, an agentic RL framework built with a unified resource layer that treats each of these environments as a distinct, typed resource scheduled through one engine, with per-tool acquisition for multi-turn reuse, asynchronous backpressure, and rollout versus global-scoped lifecycles. AgentFly adopts a four-layer design: (I) agent layer that abstracts the agent, tool, and reward concepts, decomposing agentic RL into defining agents, tools, and reward functions; (II) rollout layer that composes these into agent loops and computes rewards; (III) context layer that organizes rollouts, injects contextual information, and arranges resources; and (IV) a low-level resource layer that performs resource management. We provide a suite of prebuilt tools and environments, demonstrate successful agent training across multiple tasks and models, and report the first controlled cross-framework throughput comparison against agentic RL frameworks.
