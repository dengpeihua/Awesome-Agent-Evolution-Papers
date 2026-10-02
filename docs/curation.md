# Curation and Verification Policy

## Four research tracks

- Agent / LLM Self-Evolution and Self-Improvement.
- Agent Memory.
- LLM Continual Training and Continual Learning.
- Reinforcement Learning, including general RL, RLHF, RLAIF, and GRPO.

All topical papers are eligible, including fresh preprints without citations or
known affiliations. Priority labels do not change publication-date ordering.
The broad arXiv queries support recall; keyword matches can include peripheral
papers and are not a guarantee of substantive relevance.

## Priority labels and evidence

- Major-company team: paper-specific affiliation evidence.
- Major-company first author: first-author affiliation, or an explicitly labeled
  Semantic Scholar profile fallback. Profiles may reflect current employment,
  not employment at publication time.
- Selected venues: AAAI, NeurIPS, ACL, CVPR, ICCV, ICML, IJCAI, Artificial
  Intelligence, TPAMI, IJCV, JMLR, ECCV, EMNLP, ICLR, Nature, Science, and Nature
  Machine Intelligence. This is a maintained watchlist, not every venue worldwide.
- Acceptance requires explicit acceptance comments, journal references, or
  publication metadata. Submitted, under-review, workshop, Findings, demo and
  short-paper records do not receive main-track acceptance labels.
- At least 10 citations and code popularity are additional contextual signals.

`acceptance_first_seen` records when this bot first observed acceptance evidence;
it never asserts that the paper was accepted on that day. Old preprints are
rechecked and included again when their priority evidence changes. Indexing
latency and missing metadata mean same-day or exhaustive detection is not assured.
Official arXiv is the discovery source; Semantic Scholar enriches known records.
Papers absent from those sources are not guaranteed to be discovered.

## Delivery and recovery

Daily at 09:00 Asia/Shanghai by default, and on startup, the bot scans from its last
successful notification-and-Git publication cursor. It paginates until the entire
interval is covered; a rolling lookback overlaps delayed index entries. Query
changes retain the configurable historical rescan. Every matching paper is sent
in batches; `max_push_papers` is a batch size, not a total cap.

Git publication occurs before notification. Missing notification configuration,
disabled pushing, or a failed delivery never advances the cursor. Pending IDs
survive retries. If the final state publication fails, local success is rolled
back. Retries are at-least-once: a partially sent batch or ambiguous network
failure can cause duplicate messages, but not intentionally dropped papers.
Scheduled failures retry after 15 minutes while AstrBot is running.

`data/coverage_windows.json` preserves daily coverage through archive rebuilds.
README, daily overview, monthly lists, dataset and message batches sort by
publication time descending. Daily pages also include topic sections and a
separate priority table; priority does not reorder any individual list.

## Rebuild

Run `.venv/Scripts/python.exe scripts/recurate_repository.py` to reclassify stored
metadata and regenerate indexes and the audit. This does not claim successful
notification and does not advance the delivery cursor.
