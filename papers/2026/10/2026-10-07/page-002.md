> **64 papers** · Page 2/2 · Newest first across all pages

[1](../2026-10-07.md) · [2](page-002.md)

# Daily Papers · 2026-10-07

> Prepared **14** new, promoted, or retried paper(s) across four research tracks plus explicitly requested papers. Lists are newest publication first.
> Catch-up window: **2026-10-04T15:25:32.558967+08:00** → **2026-10-07T15:36:34.161200+08:00**.

[← Back to index](../../../../README.md)

## All Updates · Newest First

| Published | Track | Paper | Signals |
| --- | --- | --- | --- |
| 2026-07-23 | Reinforcement Learning | [How Much Can a LoRA Adapter Memorize? Measuring Adapter Capacity in Bits](https://arxiv.org/abs/2607.21351v2) | — |
| 2026-07-13 | LLM Continual Training | [Can a Language Model Learn Facts Continually in Its Weights?](https://arxiv.org/abs/2607.11020v3) | — |
| 2026-07-05 | Reinforcement Learning | [On the effectiveness of reward functions in reinforcement learning for confidence calibration of large language models](https://arxiv.org/abs/2607.04332v2) | — |
| 2026-05-23 | Reinforcement Learning | [Benchmarking the Personalization Capabilities of Large Language Models](https://arxiv.org/abs/2607.20471v2) | — |
| 2026-05-20 | Reinforcement Learning | [Reinforcement Learning over Predictive Distributions for LLM Regression](https://arxiv.org/abs/2605.20740v2) | — |
| 2026-05-10 | Reinforcement Learning, Long-Horizon Task Agents | [PiCA: Pivot-Based Credit Assignment for Search Agentic Reinforcement Learning](https://arxiv.org/abs/2605.09287v3) | — |
| 2026-03-24 | Reinforcement Learning | [Unbiased Reward Modeling from Implicit Feedback for LLM Alignment](https://arxiv.org/abs/2603.23184v2) | 🏆 CCF-A: ICML 2026<br>📣 Acceptance first observed: 2026-10-07 (actual acceptance date unverified) |
| 2025-11-25 | Reinforcement Learning, Long-Horizon Task Agents | [Stabilizing Off-Policy Training for Long-Horizon LLM Agent via Turn-Level Importance Sampling and Clipping-Triggered Normalization](https://arxiv.org/abs/2511.20718v3) | — |
| 2025-11-14 | Reinforcement Learning | [Honesty over Accuracy: Trustworthy Language Models through Reinforced Hesitation](https://arxiv.org/abs/2511.11500v3) | — |
| 2025-10-21 | Agent/LLM Self-Improvement | [A Model Can Help Itself: Reward-Free Self-Training for LLM Reasoning](https://arxiv.org/abs/2510.18814v5) | — |
| 2025-10-01 | Reinforcement Learning | [Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers](https://arxiv.org/abs/2510.00915v5) | 📈 Highly cited |
| 2025-09-29 | Agent/LLM Self-Improvement | [RFG: Self-Improving Diffusion Large Language Models with Reward-Free Guidance](https://arxiv.org/abs/2509.25604v2) | — |
| 2025-08-22 | Reinforcement Learning | [PuzzleJAX: A Benchmark for Reasoning and Learning](https://arxiv.org/abs/2508.16821v2) | — |
| 2025-06-30 | Reinforcement Learning | [Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness](https://arxiv.org/abs/2506.24056v3) | 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-10-07 (actual acceptance date unverified) |

## 🚨 Priority Watch

| Paper | Signals | Venue / affiliation evidence |
| --- | --- | --- |
| [Unbiased Reward Modeling from Implicit Feedback for LLM Alignment](https://arxiv.org/abs/2603.23184v2) | 🏆 CCF-A: ICML 2026<br>📣 Acceptance first observed: 2026-10-07 (actual acceptance date unverified) | arXiv comment: Accepted by ICML 2026<br>First author: zhejiang university (Semantic Scholar author profiles) |
| [Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers](https://arxiv.org/abs/2510.00915v5) | 📈 Highly cited | RIKEN Center for Advanced Intelligence Project |
| [Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness](https://arxiv.org/abs/2506.24056v3) | 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-10-07 (actual acceptance date unverified) | arXiv comment: Accepted at NeurIPS 2026 Main Track (poster). Camera-ready version |

## Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement

### [A Model Can Help Itself: Reward-Free Self-Training for LLM Reasoning](https://arxiv.org/abs/2510.18814v5)

- **Authors:** Mengqi Li, Lei Zhao, Anthony Man-Cho So, Ruoyu Sun, Xiao Li
- **Published:** 2025-10-21
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2510.18814v5) · [PDF](https://arxiv.org/pdf/2510.18814v5)

Can a language model improve reasoning by learning from its own imperfect responses, without rewards or teacher-provided solutions? We present Self-evolving Post-Training (SePT), a simple method that alternates temperature-controlled self-generation with next-token likelihood training. Each round uses the updated model to generate new training responses, with one response per prompt by default and no correctness filtering. Across six mathematical benchmarks, SePT improves a temperature-selected no-training baseline by 11.4 and 6.7 AVG points on Qwen2.5-Math-7B and Qwen2.5-7B, respectively, where AVG averages Pass@1, Pass@8 and Pass@32 across benchmarks. We analyze how sampling temperature shapes the learning signal and investigate the value of the resulting responses. Responses from a SePT-trained model improve a student initialized from the original weights, while their reasoning prefixes help an unchanged model complete solutions, even when matched in length to prefixes from a colder initial model. Comparing next-token predictions at identical contexts also reveals changes in token rankings that decoding-temperature adjustment cannot reproduce. Further evaluations across nine starting models, general reasoning and code generation examine broader applicability. Together, these results show that reward-free self-training can improve both a model's predictions and the supervision it provides. Our code is available at https://github.com/ElementQi/SePT.

### [RFG: Self-Improving Diffusion Large Language Models with Reward-Free Guidance](https://arxiv.org/abs/2509.25604v2)

- **Authors:** Tianlang Chen, Minkai Xu, Jure Leskovec, Stefano Ermon
- **Published:** 2025-09-29
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.CL, cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2509.25604v2) · [PDF](https://arxiv.org/pdf/2509.25604v2)

Diffusion Large Language Models (dLLMs) have shown strong reasoning capabilities, yet further improving them typically requires costly post-training with additional data and supervision. We ask whether a post-trained dLLM can improve itself at inference time without additional training, data, or reward models. This requires a guidance signal from the checkpoints alone that is well-defined on the partially masked intermediate states of dLLMs, which existing methods fail to provide. Here we propose Reward-Free Guidance (RFG), a training-free framework for inference-time self-improvement of dLLMs that derives such a signal from the checkpoints themselves. We theoretically demonstrate that a reward signal for a partially masked state can be parameterized by the log-likelihood ratio between a post-trained policy dLLM and its reference model. In practice, this signal can be obtained using off-the-shelf checkpoints alone. Extensive experiments show that RFG consistently improves state-of-the-art post-trained dLLMs by up to 16.1%. Furthermore, despite being entirely training-free, RFG delivers gains that rival or even surpass resource-intensive reinforcement learning techniques.

## LLM Continual Training & Continual Learning

### [Can a Language Model Learn Facts Continually in Its Weights?](https://arxiv.org/abs/2607.11020v3)

- **Authors:** Charles O'Neill, Max Kirkby, Jonathon Liu, Michael Psenka
- **Published:** 2026-07-13
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.CL, cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2607.11020v3) · [PDF](https://arxiv.org/pdf/2607.11020v3)

Continual learning is a long-standing capability gap between LLMs and humans. Writing new knowledge into a model's weights routinely causes it to forget old knowledge, commonly denoted as "catastrophic forgetting". Various modifications of supervised fine-tuning and distillation aim to mitigate catastrophic forgetting, but quantifying what (or how much) information was forgotten is often difficult. In this paper, we study whether current methods of writing knowledge into weights enable models to learn continually without forgetting. We introduce a framework for studying continual learning in the iterative regime, writing invented facts one at a time into a Qwen3 model already modified by previous writes, and varying the training data, method, and parameter update. Across SFT and off- and on-policy distillation, using LoRA or full fine-tuning, we compare repeated statement training (the same fact repeated in two formats) with varied example training (24 factual restatements) and find that varied examples comprehensively support more flexible use. After twenty sequential writes and merges, the model answers only 1% of questions about earlier facts correctly when every write uses repeated statements, compared with 46% when every write uses varied examples. We additionally show that this retention depends on the data used for the later writes, regardless of training method or parameter update, and that behavioral forgetting of an earlier fact does not erase its presence from the log-probabilities. Together, our framework neatly provides a comparison of performance across training data, training regimes, and parameter update schemes in an iterative learning task.

## Reinforcement Learning

### [How Much Can a LoRA Adapter Memorize? Measuring Adapter Capacity in Bits](https://arxiv.org/abs/2607.21351v2)

- **Authors:** Kaizhen Tan, Heqing Du, Yang Feng
- **Published:** 2026-07-23
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2607.21351v2) · [PDF](https://arxiv.org/pdf/2607.21351v2)

LoRA adapters are often shared on their own, and the amount of information they can hold about their training data bounds what sharing them can reveal. Following Morris et al. (2026), we measure this amount in bits by training adapters on frozen language models to memorize random token sequences. LoRA adapters store 2 to 3.4 bits per trainable parameter, less than full fine-tuning of the same model. The number of parameters alone does not set this amount: at equal size, adapters on MLP layers store more than adapters on attention layers, and a randomly initialized frozen model supports as much storage as a pretrained one once the scale of its output logits can be trained. We then train the same adapter on a task with supervised fine-tuning (SFT) and with GRPO. At the same accuracy, SFT stores about three times as much information specific to its training examples, and it stores most of the bits of secrets planted in the training data, which GRPO does not store because it rarely samples them.

### [On the effectiveness of reward functions in reinforcement learning for confidence calibration of large language models](https://arxiv.org/abs/2607.04332v2)

- **Authors:** Chee Heng Tan, Zhuoyi Lin, Mehul Motani, Wee Sun Lee
- **Published:** 2026-07-05
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2607.04332v2) · [PDF](https://arxiv.org/pdf/2607.04332v2)

In this paper, we consider the setting where large language models (LLMs) are trained using reinforcement learning (RL) to simultaneously improve reasoning accuracy and verbalize their confidence. Our reward scheme uses two functions for rewarding confidence verbalized by the LLM: one for correct answers and the other for incorrect answers. If poorly designed, such a scheme may incentivize an LLM to answer incorrectly in order for its confidence to be calibrated, a phenomenon we term confidence reward hacking. We introduce the notion of non-hackable confidence reward schemes and provide methods for constructing them. We show that selective confidence reward hacking can arise in practical datasets under hackable reward schemes while non-hackable reward schemes are resistant to hacking. Finally, we place some of these schemes along an overconfidence-underconfidence spectrum for RL-based confidence calibration and demonstrate experimentally that they tend to exhibit the corresponding calibration biases relative to other schemes in the spectrum. The code of our experiments is available in https://anonymous.4open.science/r/rl-confidence-calibration-9ED4/README.md.

### [Benchmarking the Personalization Capabilities of Large Language Models](https://arxiv.org/abs/2607.20471v2)

- **Authors:** Ashutosh Srivastava, Siddharth Yedlapati, Vinay Aggarwal, Yaman Kumar Singla, Shashwat Dixit, Jitendra Ajmera, Balaji Krishnamurthy
- **Published:** 2026-05-23
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** Adobe, IIIT-Delhi, SUNY-Buffalo
- **Categories:** cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2607.20471v2) · [PDF](https://arxiv.org/pdf/2607.20471v2)

Personalization is classically a two-party problem: a sender chooses what to say, and a receiver with independent objectives decides whether to act. A salesperson pitching the same analytics product leads with HIPAA compliance for a hospital and real-time reporting for a retailer, expecting a different argument to work on each. Existing LLM personalization benchmarks measure a narrower, one-party property: whether output matches the preferences of the same user it serves-sender and receiver being the same, as when RLHF aligns an assistant to its own user. The two-party case is harder to study automatically, since it needs ground truth linking specific content to an observed receiver action. Sales outreach provides this: a message written for one prospect, recorded against whether it produced a reply, a call, or a closed deal. We introduce SDR-Arena, a framework for benchmarking two-party generative personalization at scale, and SDR-Bench, a public corpus of 50,000 customer success stories across 22 industries and 3500 enterprises. Given only pre-outcome information, an agent must reconstruct the arguments that won the deal, scored by a weighted nugget-recall metric (WCS). The best model, Claude Sonnet 4.6, reaches 55.8% WCS indicating it recovers only half the winning content-a plateau we observe across model families that costly deep-research pipelines do not close. An ablation shows the cause is retrieval, not reasoning: models improve substantially given the facts a human researcher would gather, but rarely find them through web search alone. Two studies with professional SDRs support the metric: only 48% of generated pitches were rated usable without editing, and WCS yields model rankings consistent with evaluation against expert strategies authored independently of any model output.

### [Reinforcement Learning over Predictive Distributions for LLM Regression](https://arxiv.org/abs/2605.20740v2)

- **Authors:** Jungsoo Park, Hyungjoo Chae, Ethan Mendes, Jay DeYoung, Varsha Kishore, Wei Xu, Alan Ritter
- **Published:** 2026-05-20
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** Northeastern University
- **Categories:** cs.LG, cs.AI, cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2605.20740v2) · [PDF](https://arxiv.org/pdf/2605.20740v2)

Large language models (LLMs) have emerged as flexible regressors capable of predicting real-valued quantities from heterogeneous inputs. Yet most LLM regression objectives optimize predictions independently, often yielding poor calibration. We introduce Distribution-Aware Reward (DAR), an on-policy reinforcement learning objective that instead jointly evaluates the empirical predictive distribution formed by multiple predictions for the same input. To translate this distribution-level objective into rollout-level rewards, we assign each prediction credit based on its leave-one-out contribution to the quality of the overall predictive distribution. This encourages predictions that are well-centered and appropriately dispersed around the target. We evaluate on three regression settings: a synthetic task probing interpolation and extrapolation, and two real-world scientific tasks involving code and molecular data. Across tasks, DAR produces better-calibrated uncertainty estimates while consistently reducing prediction error and improving ranking quality over supervised fine-tuning and pointwise reinforcement learning. Together, these results highlight the benefits of distribution-aware training for LLM regression.

### [PiCA: Pivot-Based Credit Assignment for Search Agentic Reinforcement Learning](https://arxiv.org/abs/2605.09287v3)

- **Authors:** Dongyi Liu, Yifan Niu, Qinwen Wang, Han Xiao, Jia Li
- **Published:** 2026-05-10
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2605.09287v3) · [PDF](https://arxiv.org/pdf/2605.09287v3)

Large Language Model (LLM)-based search agents trained with reinforcement learning (RL) have significantly improved the performance of knowledge-intensive tasks. However, existing methods encounter critical challenges in long-horizon credit assignment: (i) Reward Sparsity, where models receive only outcome feedback without step-level guidance to differentiate action quality; (ii) Isolated Credit, where credit is assigned to steps independently, failing to capture sequential dependencies; and (iii) Distributional Shift, where rewards are estimated on templates that deviate from the model's natural generative distribution. To address these issues, we propose Pivot-Based Credit Assignment (PiCA), a novel step reward mechanism that reformulates the search trajectory as a sequential process of cumulative search progress. Unlike prior isolated step rewards, PiCA defines process rewards as success probabilities dependent on the historical context based on Potential-Based Reward Shaping (PBRS). This approach identifies pivot steps, which comprise target golden sub-queries and sub-answers derived from historical trajectories, as information peaks that significantly boost the likelihood of a correct final answer. By anchoring these step rewards to the final task objective, PiCA provides dense, pivot-aware and trajectory-dependent guidance while maintaining distributional consistency. Extensive experiments show that PiCA outperforms existing strong baselines across seven knowledge-intensive QA benchmarks, achieving 15.2% and 4.4% improvements for 3B and 7B models. The consistent performance gains across various models show PiCA's robust generalization. The code is available at https://github.com/novdream/PiCA.

### [Unbiased Reward Modeling from Implicit Feedback for LLM Alignment](https://arxiv.org/abs/2603.23184v2)

- **Authors:** Hao Wang, Haocheng Yang, Licheng Pan, Lei Shen, Xiaoxi Li, Yinuo Wang, Zhichao Chen, Yuan Lu, Haoxuan Li, Zhouchen Lin
- **Published:** 2026-03-24
- **Priority:** 🏆 CCF-A: ICML 2026<br>📣 Acceptance first observed: 2026-10-07 (actual acceptance date unverified)
- **Venue:** ICML 2026
- **Affiliations:** zhejiang university
- **Categories:** cs.CL, cs.AI, stat.AP
- **Links:** [Paper](https://arxiv.org/abs/2603.23184v2) · [PDF](https://arxiv.org/pdf/2603.23184v2)

Despite the success of reinforcement learning from human feedback (RLHF), existing reward modeling methods largely rely on explicit feedback, which is costly to collect and difficult to scale. This work studies implicit reward modeling, learning reward models from implicit user feedback, such as clicks, copies and skips. While scalable and cost-effective, implicit feedback poses two key challenges: It lacks definitive negative samples, which makes standard positive-negative classification methods inapplicable; It suffers from selection bias, where responses have heterogeneous propensities to elicit feedback, which further obscures definitive negative samples. To address these challenges, we propose ImplicitRM, which learns unbiased reward models from implicit feedback. It stratifies training samples into four latent groups using a stratification model and derives a likelihood-maximization objective that is theoretically unbiased, thereby addressing both challenges. Experiments across diverse LLM backbones and benchmark datasets validate that ImplicitRM learns accurate reward models from implicit feedback and improves performance on downstream RLHF tasks.

### [Stabilizing Off-Policy Training for Long-Horizon LLM Agent via Turn-Level Importance Sampling and Clipping-Triggered Normalization](https://arxiv.org/abs/2511.20718v3)

- **Authors:** Chenliang Li, Adel Elmahdy, Alex Boyd, Zhongruo Wang, Siliang Zeng, Alfredo Garcia, Parminder Bhatia, Taha Kass-Hout, Cao Xiao, Mingyi Hong
- **Published:** 2025-11-25
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI, cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2511.20718v3) · [PDF](https://arxiv.org/pdf/2511.20718v3)

Reinforcement learning (RL) algorithms such as PPO and GRPO are widely used to train large language models (LLMs) for multi-turn agentic tasks. However, in off-policy training pipelines, these methods can exhibit unstable optimization dynamics and are prone to perfor- mance collapse. Through empirical analysis, we identify two fundamental sources of instability in this setting: (1) a granularity mismatch between token-level policy optimization and turn- structured interactions, and (2) high-variance and unreliable gradient updates induced by off- policy importance sampling and inaccurate advantage estimation. To address these challenges, we propose SORL, Stabilizing Off-Policy Reinforcement Learning for Long-Horizon Agent Train- ing. SORL introduces mechanisms that align policy optimization with the structure of multi- turn interactions and adaptively suppress unreliable off-policy updates, yielding more conserva- tive and robust learning dynamics. Within this framework, we instantiate two stabilized algo- rithms: SO-PPO and SO-GRPO. Both algorithms are designed to mitigate gradient variance and prevent optimization collapse without requiring careful early stopping or heuristic tuning. We evaluate SO-PPO and SO-GRPO on benchmarks spanning open-domain QA, multi-hop QA, and medical multiple-choice QA, and further assess their transfer to asynchronous RL for mathe- matical reasoning by training on DAPO-Math-17k and validating on AIME-2024. These results demonstrate that SORL provides a practical, scalable, and general framework for stabilizing re- inforcement learning in multi-turn LLM agent training and asynchronous RL for mathematical reasoning.

### [Honesty over Accuracy: Trustworthy Language Models through Reinforced Hesitation](https://arxiv.org/abs/2511.11500v3)

- **Authors:** Mohamad Amin Mohamadi, Tianhao Wang, Zhiyuan Li
- **Published:** 2025-11-14
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2511.11500v3) · [PDF](https://arxiv.org/pdf/2511.11500v3)

Modern language models fail a fundamental requirement of trustworthy intelligence: knowing when not to answer. Despite achieving impressive accuracy on benchmarks, these models produce confident hallucinations, even when wrong answers carry catastrophic consequences. Our evaluations on GSM8K, MedQA and GPQA show frontier models almost never abstain despite explicit warnings of severe penalties, suggesting that prompts cannot override training that rewards any answer over no answer. As a remedy, we propose Reinforced Hesitation (RH): a modification to Reinforcement Learning from Verifiable Rewards (RLVR) to use ternary rewards (+1 correct, 0 abstention, -$λ$ error) instead of binary. Controlled experiments on logic puzzles reveal that varying $λ$ produces distinct models along a Pareto frontier, where each training penalty yields the optimal model for its corresponding risk regime: low penalties produce aggressive answerers, high penalties conservative abstainers. The same frontier holds on MATH Levels 4--5 and on medical QA, where it transfers to an unseen dataset. We then introduce two inference strategies that exploit trained abstention as a coordination signal: cascading routes queries through models with decreasing risk tolerance, while self-cascading re-queries the same model on abstention. Both outperform majority voting with lower computational cost. These results establish abstention as a first-class training objective that transforms ``I don't know'' from failure into a coordination signal, enabling models to earn trust through calibrated honesty about their limits.

### [Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers](https://arxiv.org/abs/2510.00915v5)

- **Authors:** Xin-Qiang Cai, Wei Wang, Feng Liu, Tongliang Liu, Gang Niu, Masashi Sugiyama
- **Published:** 2025-10-01
- **Priority:** 📈 Highly cited
- **Venue:** arXiv.org
- **Affiliations:** RIKEN Center for Advanced Intelligence Project
- **Categories:** cs.LG, cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2510.00915v5) · [PDF](https://arxiv.org/pdf/2510.00915v5)

Reinforcement Learning with Verifiable Rewards (RLVR) replaces costly human labeling with automated verifiers. To reduce verifier hacking, many RLVR systems binarize rewards to $\{0,1\}$, but imperfect verifiers inevitably introduce \emph{false negatives} (rejecting correct answers) and \emph{false positives} (accepting incorrect ones). We formalize verifier unreliability as a stochastic reward channel with asymmetric noise rates $ρ_0$ and $ρ_1$ -- the FP rate and the FN rate, respectively. From this abstraction we derive two lightweight corrections: (i) a \emph{backward} correction that yields an unbiased surrogate reward and thus an unbiased policy-gradient estimator in expectation, and (ii) a \emph{forward} correction that reweights score-function terms so the expected update aligns with the clean gradient direction and requires only the FN rate. We implement both as lightweight hooks in a group relative policy optimization pipeline, both corrections improve RLVR for math reasoning under synthetic and real verifier noise, with the forward variant being more stable under heavier noise. Finally, an appeals mechanism with a lightweight LLM verifier estimates the FN rate online and further improves performance.

### [PuzzleJAX: A Benchmark for Reasoning and Learning](https://arxiv.org/abs/2508.16821v2)

- **Authors:** Sam Earle, Graham Todd, Yuchen Li, Ahmed Khalifa, Muhammad Umair Nasir, Zehua Jiang, Andrzej Banburski-Fahey, Julian Togelius
- **Published:** 2025-08-22
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** University of the Witwatersrand
- **Categories:** cs.AI, cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2508.16821v2) · [PDF](https://arxiv.org/pdf/2508.16821v2)

We introduce PuzzleJAX, a GPU-accelerated puzzle game engine and description language designed to support rapid benchmarking of tree search, reinforcement learning, and LLM reasoning abilities. Unlike existing GPU-accelerated learning environments that provide hard-coded implementations of fixed sets of games, PuzzleJAX allows dynamic compilation of any game expressible in its domain-specific language (DSL). This DSL follows PuzzleScript, which is a popular and accessible online game engine for designing puzzle games. In this paper, we validate in PuzzleJAX several hundred of the thousands of games designed in PuzzleScript by both professional designers and casual creators since its release in 2013, thereby demonstrating PuzzleJAX's coverage of an expansive, expressive, and human-relevant space of tasks. By analyzing the performance of search, learning, and language models on these games, we show that PuzzleJAX can naturally express tasks that are both simple and intuitive to understand, yet often deeply challenging to master, requiring a combination of control, planning, and high-level insight.

### [Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness](https://arxiv.org/abs/2506.24056v3)

- **Authors:** Tung-Ling Li, Hongliang Liu
- **Published:** 2025-06-30
- **Priority:** 🏆 CCF-A: NeurIPS 2026<br>📣 Acceptance first observed: 2026-10-07 (actual acceptance date unverified)
- **Venue:** NeurIPS 2026
- **Affiliations:** n/a
- **Categories:** cs.CR, cs.CL, cs.LG
- **Links:** [Paper](https://arxiv.org/abs/2506.24056v3) · [PDF](https://arxiv.org/pdf/2506.24056v3)

RLHF-style alignment trains language models to refuse unsafe requests, but how much operational margin does this refusal rest on? We introduce the refusal-affirmation logit gap: the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step. This single scalar quantifies the per-prompt safety margin that alignment provides. Empirically, alignment widens the gap on 97.5-99.8% of toxic prompts across three model families, and median gap closure co-varies with True-ASR ranking across suffix strategies (an internal consistency check, since our method optimises gap closure). To validate the metric's practical significance, we present logit-gap steering, a gradient-free, forward-pass-only method that discovers short in-distribution suffixes ($<$10 tokens per component) whose cumulative effect closes the gap. The method requires ${\approx}26{,}000$ forward-pass equivalents per family (${\approx}2$~min on one A100), ${\approx}125\times$ less than a single GCG search. Suffixes discovered on 0.5B--2B models transfer without modification to 72B within family. An 8-suffix ensemble reaches 38-96\% True ASR across 13 models on AdvBench and HarmBench, with most suffixes having $10^{3}$-$10^{4}\times$ lower perplexity than GCG-meaning published perplexity-filter defenses that collapse GCG (64.7%$\to$1.0%) leave our suffixes nearly intact (76.9%$\to$76.0%). These results demonstrate that current alignment margins, while consistently present, can be thin and efficiently measurable, and that defense strategies must account for in-distribution suffixes.

## Long-Horizon Task Agents

### [PiCA: Pivot-Based Credit Assignment for Search Agentic Reinforcement Learning](https://arxiv.org/abs/2605.09287v3)

- **Authors:** Dongyi Liu, Yifan Niu, Qinwen Wang, Han Xiao, Jia Li
- **Published:** 2026-05-10
- **Priority:** —
- **Venue:** arXiv.org
- **Affiliations:** n/a
- **Categories:** cs.AI
- **Links:** [Paper](https://arxiv.org/abs/2605.09287v3) · [PDF](https://arxiv.org/pdf/2605.09287v3)

Large Language Model (LLM)-based search agents trained with reinforcement learning (RL) have significantly improved the performance of knowledge-intensive tasks. However, existing methods encounter critical challenges in long-horizon credit assignment: (i) Reward Sparsity, where models receive only outcome feedback without step-level guidance to differentiate action quality; (ii) Isolated Credit, where credit is assigned to steps independently, failing to capture sequential dependencies; and (iii) Distributional Shift, where rewards are estimated on templates that deviate from the model's natural generative distribution. To address these issues, we propose Pivot-Based Credit Assignment (PiCA), a novel step reward mechanism that reformulates the search trajectory as a sequential process of cumulative search progress. Unlike prior isolated step rewards, PiCA defines process rewards as success probabilities dependent on the historical context based on Potential-Based Reward Shaping (PBRS). This approach identifies pivot steps, which comprise target golden sub-queries and sub-answers derived from historical trajectories, as information peaks that significantly boost the likelihood of a correct final answer. By anchoring these step rewards to the final task objective, PiCA provides dense, pivot-aware and trajectory-dependent guidance while maintaining distributional consistency. Extensive experiments show that PiCA outperforms existing strong baselines across seven knowledge-intensive QA benchmarks, achieving 15.2% and 4.4% improvements for 3B and 7B models. The consistent performance gains across various models show PiCA's robust generalization. The code is available at https://github.com/novdream/PiCA.

### [Stabilizing Off-Policy Training for Long-Horizon LLM Agent via Turn-Level Importance Sampling and Clipping-Triggered Normalization](https://arxiv.org/abs/2511.20718v3)

- **Authors:** Chenliang Li, Adel Elmahdy, Alex Boyd, Zhongruo Wang, Siliang Zeng, Alfredo Garcia, Parminder Bhatia, Taha Kass-Hout, Cao Xiao, Mingyi Hong
- **Published:** 2025-11-25
- **Priority:** —
- **Venue:** arXiv
- **Affiliations:** n/a
- **Categories:** cs.LG, cs.AI, cs.CL
- **Links:** [Paper](https://arxiv.org/abs/2511.20718v3) · [PDF](https://arxiv.org/pdf/2511.20718v3)

Reinforcement learning (RL) algorithms such as PPO and GRPO are widely used to train large language models (LLMs) for multi-turn agentic tasks. However, in off-policy training pipelines, these methods can exhibit unstable optimization dynamics and are prone to perfor- mance collapse. Through empirical analysis, we identify two fundamental sources of instability in this setting: (1) a granularity mismatch between token-level policy optimization and turn- structured interactions, and (2) high-variance and unreliable gradient updates induced by off- policy importance sampling and inaccurate advantage estimation. To address these challenges, we propose SORL, Stabilizing Off-Policy Reinforcement Learning for Long-Horizon Agent Train- ing. SORL introduces mechanisms that align policy optimization with the structure of multi- turn interactions and adaptively suppress unreliable off-policy updates, yielding more conserva- tive and robust learning dynamics. Within this framework, we instantiate two stabilized algo- rithms: SO-PPO and SO-GRPO. Both algorithms are designed to mitigate gradient variance and prevent optimization collapse without requiring careful early stopping or heuristic tuning. We evaluate SO-PPO and SO-GRPO on benchmarks spanning open-domain QA, multi-hop QA, and medical multiple-choice QA, and further assess their transfer to asynchronous RL for mathe- matical reasoning by training on DAPO-Math-17k and validating on AIME-2024. These results demonstrate that SORL provides a practical, scalable, and general framework for stabilizing re- inforcement learning in multi-turn LLM agent training and asynchronous RL for mathematical reasoning.
