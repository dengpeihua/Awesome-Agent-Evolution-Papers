# Curation and Verification Policy

The public repository contains a deliberately small, evidence-backed collection.
Every paper must first make a substantive contribution to at least one research
track and then satisfy at least one qualification criterion.

## Required research scope

- **Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement:** an
  agent or language model improves its policy, harness, skills, tools, training
  procedure, reasoning, workflow, memory, or collaboration structure over repeated
  experience and feedback cycles. This includes self-refinement, self-reward, and
  reinforcement learning from self-generated feedback when improvement is central.
- **Agent Memory:** storage, writing, retrieval, consolidation, forgetting,
  governance, security, or evaluation is central to an LLM agent.
- **LLM Continual Training & Continual Learning:** an LLM or foundation model is
  continually pretrained, post-trained, fine-tuned, aligned, or adapted while
  addressing retention, transfer, online learning, or catastrophic forgetting.

Traditional continual learning without an LLM/foundation-model component and
generic model-memory or cache papers without an agent contribution are excluded.

## Qualification criteria

An in-scope paper is made public only when at least one of these is verified:

1. A Full/Regular paper in a CCF-A venue from the Artificial Intelligence category:
   AAAI, NeurIPS, ACL, CVPR, ICCV, ICML, IJCAI, Artificial Intelligence, TPAMI,
   IJCV, or JMLR.
2. A Full/Regular paper at ECCV or EMNLP.
3. The paper is from a major technology company, or its first author is affiliated
   with one. Paper-specific affiliations are preferred; a first-author profile may
   be used as a clearly labeled fallback.
4. The paper has at least 10 source-attributed citations.

Findings, workshop, demo, short, summary, industry-track, submitted, and
under-review papers do not qualify through venue status. They can still qualify
independently through big-tech authorship or citations. GitHub stars are displayed
as context but never qualify a paper by themselves.

## Metadata and evidence

arXiv and specialist literature lists supply candidate recall, not automatic
acceptance. Publication metadata, arXiv comments/journal references, DOI-backed
publisher pages, Semantic Scholar, and paper-specific affiliation evidence are used
for qualification. `arXiv.org`, `CoRR`, and `preprint` are never treated as venues.

Semantic Scholar author profiles are weaker than paper-specific affiliations. A
big-tech affiliation on the first author's profile can satisfy the requested
first-author rule, but a company found only on a coauthor profile cannot.

The machine-readable public corpus is
[`data/papers.json`](../data/papers.json), and the current policy audit is
[`data/curation_audit.json`](../data/curation_audit.json).

## Candidate pool and daily promotion

Topically relevant but unqualified papers are kept only in the ignored local file
`.paper_digest/candidates.json`. Each daily run refreshes publication, citation, and
author evidence for that pool. A candidate enters the public repository and the
daily push as soon as it gains a valid qualifier.

`data/digest_state.json` records the most recent fully successful run and pending
notification IDs. After downtime, the bot resumes from that cursor instead of
limiting retrieval to the current day.

## Rebuilding the repository

To apply the current strict policy to the stored candidate pool and regenerate the
dataset, daily pages, monthly pages, README, and audit files:

```powershell
.\.venv\Scripts\python.exe scripts\recurate_repository.py
```

The broader historical discovery script remains in `scripts/backfill_2026.py` for
candidate collection; `ArchiveRepository` always reapplies this strict public
eligibility policy before publishing its output.
