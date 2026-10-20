# Curation and Verification Policy

## Four research tracks

- Agent / LLM Self-Evolution and Self-Improvement.
- Long-Horizon Task Agents.
- LLM Continual Training and Continual Learning.
- Reinforcement Learning directly related to LLMs / language agents, including RLHF, RLAIF, RLVR, and GRPO.

First publication must be on or after **2025-05-01**. Older papers remain excluded
even when revised or accepted recently. RL requires language-model context plus
a substantive training/research statement. Broad application-only RL, baseline
comparisons and incidental survey mentions do not qualify. Historical RL labels
are recomputed rather than trusted. See `data/rl_screening.json` for title/abstract
evidence; these automated checks are not full-paper verification.

All topical papers are eligible, including fresh preprints without citations or
known affiliations. Priority labels do not change publication-date ordering.
The broad arXiv queries support recall; keyword matches can include peripheral
papers and are not a guarantee of substantive relevance.

## Priority labels and evidence

- Major-company team: paper-specific affiliation evidence.
- Major-company first author: first-author affiliation, or an explicitly labeled
  Semantic Scholar profile fallback. Profiles may reflect current employment,
  not employment at publication time.
- Selected conferences: AAAI, NeurIPS, ACL, CVPR, ICCV, ICML, IJCAI, ECCV, EMNLP, ICLR.
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
Large daily archives use linked pages of 50 papers to stay readable on GitHub.

## Rebuild

Run `.venv/Scripts/python.exe scripts/recurate_repository.py` to reclassify stored
metadata and regenerate indexes and the audit. This does not claim successful
notification and does not advance the delivery cursor.


## Long-horizon task agents (2026-10-21)

The long-horizon track requires language-model context, agent context, and
long-horizon / long-trajectory / extended-task evidence in title or abstract.
A source query tag alone does not establish relevance. Long context alone and
classical control without language agents are insufficient. All active tracks enforce
first publication between 2025-05-01 and the current execution time.

Explicitly requested papers have a separate supplemental label. In particular,
MOPD and MOPD-Router are not automatically treated as continual learning or
long-horizon agent RL merely because they perform on-policy distillation.
Industry and acceptance evidence policies apply unchanged to all new entries.
An acceptance first-observed date does not establish the actual acceptance date;
source coverage and indexing delays preclude a guarantee of exhaustive same-day detection.

Run `python scripts/update_long_horizon.py` to reproduce the full new-track
backfill and the four requested additions. It stages pending notifications but
never advances the successful delivery cursor or sends messages itself.


## Exclusions (2026-10-21)

First publication before 2025-05-01 is excluded. Agent Memory papers are excluded
entirely, including papers also tagged as RL or long-horizon agents. Memory is
not an active discovery topic. Journal articles are excluded using publication
types, venue types, and journal-name evidence; a DOI or conference proceedings
reference alone does not imply journal publication. Unknown publication types
remain subject to later metadata refresh. Explicit requests do not bypass exclusions.

Deleted identifiers remain in `data/excluded_paper_ids.json` to prevent historical
cache entries or alternative queries from restoring removed papers. Curation
rebuilds purge excluded cached candidates and public indexes. The Git history
retains earlier versions; the current published lists use the new policy.

Venue-name checks include TMLR abbreviations and journal series with proceedings-style names.
For example, [ACM identifies PACMMOD as a journal](https://www.acm.org/binaries/content/assets/press-releases/2023/july/acm-pacmmod.pdf).
