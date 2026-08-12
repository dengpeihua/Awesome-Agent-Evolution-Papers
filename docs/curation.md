# Curation and Verification Policy

This repository tracks papers released from **2026-01-01 through 2026-08-12** in
three areas: Agent Self-Evolving, Agent Memory, and LLM Continual Training.

## Inclusion rules

A paper is included when its title or abstract makes a substantive contribution to
at least one track:

- an LLM-based agent improves its policy, harness, skills, tools, memory, workflow,
  or collaboration structure from experience or feedback;
- memory storage, writing, retrieval, consolidation, forgetting, governance,
  security, or evaluation is a central contribution for LLM agents;
- an LLM or foundation model is continually pretrained, fine-tuned, aligned, or
  adapted while addressing retention, transfer, or catastrophic forgetting.

Traditional continual learning without an LLM/foundation-model component and
generic model-memory or cache papers without an agent contribution are excluded.
Application papers are retained when the memory or evolution method itself is a
technical contribution.

## Discovery and metadata verification

Specialist Awesome lists are used only to maximize recall. Every included arXiv
record is then reopened on its official paper page to verify title, authors,
abstract, first-submission date, category, PDF, and any explicit code URL. ACL
papers without a 2026 arXiv identifier are verified on ACL Anthology.

The reproducible backfill is implemented in
[`scripts/backfill_2026.py`](../scripts/backfill_2026.py). Its machine-readable
run summary is [`data/backfill_2026_audit.json`](../data/backfill_2026_audit.json).

## Highlight signals

- **Very popular code:** at least 1,000 GitHub stars.
- **Popular code:** at least 100 GitHub stars.
- **Highly cited:** at least 10 Google Scholar citations for a 2026 paper.
- **Industry:** an affiliation is verified from the paper, publisher page, or an
  official company research page.
- **Top venue:** a full paper at a selective flagship venue. Findings and workshops
  are labeled separately and are not promoted to top-venue status.

Stars and citations are snapshots dated **2026-08-12**. A missing metric is stored
as `null` and rendered as `n/a`; it is never estimated. Repository stars describe
the linked implementation repository, which can host more than one related paper.

## Rebuilding

From the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\backfill_2026.py
```

Use `--skip-citations` to preserve existing citation snapshots while rebuilding
paper metadata and GitHub metrics.
