# 2026 Agent Evolution Literature Audit

## Scope

- Cutoff: 2026-08-12 (Asia/Shanghai request date)
- Tracks: Agent Self-Evolving, Agent Memory, LLM Continual Training
- Sources used for candidate recall: three specialist, continuously maintained
  literature indexes listed in `data/backfill_2026_audit.json`
- Canonical verification: arXiv paper pages and ACL Anthology; GitHub REST API for
  stars; exact-title Google Scholar checks for prioritized papers

## Search strategy

The search combined strong phrase families rather than one literal query:

1. self-evolving, self-improving, agent evolution, evolving agents, evolving
   skills, harness evolution, and self-consolidation;
2. agent memory, agentic memory, long-term or episodic memory for agents,
   memory-augmented agents, memory governance, and memory evaluation;
3. continual learning, continual adaptation/training/pretraining/fine-tuning,
   lifelong learning, knowledge updating, and catastrophic forgetting for LLMs or
   foundation models.

Specialist lists supplied candidate recall. Titles alone were not treated as final
metadata: each included record was fetched again from its canonical paper page.
Search/API failures were not converted into invented records or metrics.

## Result

The verified corpus contains **547 unique papers**:

| Month | Unique papers |
| --- | ---: |
| 2026-01 | 78 |
| 2026-02 | 63 |
| 2026-03 | 71 |
| 2026-04 | 69 |
| 2026-05 | 104 |
| 2026-06 | 98 |
| 2026-07 | 61 |
| 2026-08 (through Aug 12) | 3 |

Because papers may belong to multiple tracks, track totals overlap: 97
Self-Evolving, 462 Agent Memory, and 33 LLM Continual Training papers.

The enrichment pass verified 111 GitHub star snapshots, 33 prioritized citation
snapshots, 4 industry flags, and 7 top-venue flags. The complete machine-readable
evidence is in `data/papers.json`; unresolved metrics remain null.

## Limitations

- 2026 is still in progress, and arXiv revisions can change titles, abstracts, and
  code links after the cutoff.
- Citation and star counts are time-sensitive and are deliberately not inferred
  when a source is unavailable.
- Industry affiliation is conservative: an official company-owned repository alone
  is not treated as proof unless supported by a paper or official research page.
- This is a high-recall technical corpus. Domain-specific application papers remain
  included when agent memory or evolution is itself a central method.
