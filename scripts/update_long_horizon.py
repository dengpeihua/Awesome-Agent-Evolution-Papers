# ruff: noqa: E402
"""Backfill the new track and explicitly requested papers without sending notifications."""

from __future__ import annotations

import asyncio
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent_paper_digest.archive import ArchiveRepository
from agent_paper_digest.arxiv import ArxivSource, parse_arxiv_feed
from agent_paper_digest.candidates import CandidateRepository
from agent_paper_digest.highlight import classify_highlights, is_eligible
from agent_paper_digest.state import DigestStateStore
from agent_paper_digest.topics import LONG_HORIZON_TOPIC, MIN_PUBLICATION_DATE, REQUESTED_TOPIC
from scripts.recurate_repository import _write_audit, _write_report


class LongHorizonSource(ArxivSource):
    @staticmethod
    def topic_queries():
        return {LONG_HORIZON_TOPIC: ArxivSource.topic_queries()[LONG_HORIZON_TOPIC]}


async def main():
    ids = ["2606.30406", "2609.30837", "2505.10978", "2601.18225"]
    source = ArxivSource()
    async with httpx.AsyncClient(timeout=45, follow_redirects=True) as client:
        response = await source._request_page(
            client, params={"id_list": ",".join(ids), "max_results": 10}
        )
    requested = parse_arxiv_feed(response.text, topic=REQUESTED_TOPIC)
    if {p.arxiv_id for p in requested} != set(ids):
        raise RuntimeError("Incomplete requested-paper response; refusing partial import")
    enriched = []
    for p in requested:
        evidence = f"Official paper: https://arxiv.org/html/{p.arxiv_id}"
        if p.arxiv_id == "2606.30406":
            p = replace(
                p,
                affiliations=("Peking University", "LLM Core, Xiaomi"),
                first_author_affiliations=("Peking University", "LLM Core, Xiaomi (internship)"),
                affiliation_source=evidence,
            )
        elif p.arxiv_id == "2609.30837":
            p = replace(
                p,
                affiliations=("Shanghai Jiao Tong University", "Alibaba Group"),
                first_author_affiliations=("Shanghai Jiao Tong University", "GAIR"),
                affiliation_source=evidence,
                github_url="https://github.com/TURLEing/MOPD-Router",
            )
        elif p.arxiv_id == "2601.18225":
            p = replace(
                p,
                affiliations=("Alibaba Group",),
                first_author_affiliations=("Alibaba Group",),
                affiliation_source=evidence,
                github_url="https://github.com/ShopAgent-Team/ShopSimulator",
            )
        else:
            p = replace(
                p,
                venue="NeurIPS 2025",
                venue_source="NeurIPS proceedings",
                acceptance_evidence="Published at NeurIPS 2025: https://papers.nips.cc/paper_files/paper/2025/file/420c9f777c0b4f78d515e53cf74d58b2-Paper-Conference.pdf",
                affiliations=("Nanyang Technological University", "Skywork AI"),
                first_author_affiliations=("Nanyang Technological University",),
                affiliation_source="https://openreview.net/pdf?id=QXEhBMNrCW",
                github_url="https://github.com/langfengQ/verl-agent",
            )
        enriched.append(p)
        print("Verified requested paper:", p.arxiv_id, p.title, flush=True)
    recent = await LongHorizonSource().fetch(since=MIN_PUBLICATION_DATE, max_results_per_topic=100)
    print("Fetched long-horizon candidates:", len(recent), flush=True)
    archive = ArchiveRepository(ROOT)
    candidates = CandidateRepository(ROOT)
    pool = [
        classify_highlights(p) for p in candidates.merge([*archive._load(), *recent, *enriched])
    ]
    candidates.save(pool)
    known = {p.arxiv_id for p in archive._load()}
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    state = DigestStateStore(ROOT)
    queued = state.stage(
        now, tuple(p.arxiv_id for p in pool if is_eligible(p) and p.arxiv_id not in known)
    )
    result = archive.update(
        now.date(),
        pool,
        carryover_ids=queued.pending_paper_ids,
        coverage_start=MIN_PUBLICATION_DATE,
        coverage_end=now,
    )
    public = archive.replace_dataset(list(result.all_papers))
    _write_audit(ROOT, pool, public)
    _write_report(ROOT, pool, public)
    assert set(ids) <= {p.arxiv_id for p in public}
    print(
        "Public:", len(public), "Long-horizon:", sum(LONG_HORIZON_TOPIC in p.topics for p in public)
    )
    print("Delivery cursor preserved; new IDs queued for the next normal digest.")


if __name__ == "__main__":
    asyncio.run(main())
