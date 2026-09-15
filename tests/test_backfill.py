from dataclasses import replace
from datetime import datetime, timedelta

import pytest

from agent_paper_digest.highlight import classify_highlights, has_industry_qualification
from agent_paper_digest.topics import SELF_EVOLUTION_TOPIC
from scripts import backfill_2026
from tests.test_archive import make_paper


class FakeOfficialArxivSource:
    async def fetch(self, *, since: datetime, max_results_per_topic: int):
        assert since.date() == (
            backfill_2026.CUTOFF
            - timedelta(days=backfill_2026.HISTORICAL_DISCOVERY_DAYS)
        )
        assert max_results_per_topic == 100
        return [
            replace(
                make_paper("2604.18292", topics=(SELF_EVOLUTION_TOPIC,)),
                title=(
                    "Agent-World: Scaling Real-World Environment Synthesis for "
                    "Evolving General Agent Intelligence"
                ),
            )
        ]


@pytest.mark.asyncio
async def test_historical_discovery_merges_official_arxiv_results(monkeypatch) -> None:
    monkeypatch.setattr(backfill_2026, "DISCOVERY_SOURCES", {})

    candidates = await backfill_2026.discover_candidates(
        object(),
        official_source=FakeOfficialArxivSource(),
    )

    assert candidates["2604.18292"] == (SELF_EVOLUTION_TOPIC,)


@pytest.mark.asyncio
async def test_official_discovery_survives_third_party_source_failure(
    monkeypatch,
) -> None:
    monkeypatch.setattr(backfill_2026, "DISCOVERY_SOURCES", {"broken": "https://bad"})

    async def fail_third_party(_client, _url):
        raise RuntimeError("third-party list unavailable")

    monkeypatch.setattr(backfill_2026, "_get", fail_third_party)

    candidates = await backfill_2026.discover_candidates(
        object(),
        official_source=FakeOfficialArxivSource(),
    )

    assert "2604.18292" in candidates


def test_agent_world_has_verified_bytedance_team_evidence() -> None:
    paper = make_paper("2604.18292", topics=(SELF_EVOLUTION_TOPIC,))

    enriched = backfill_2026.apply_known_enrichments([paper])[0]
    classified = classify_highlights(enriched)

    assert enriched.affiliations == (
        "Gaoling School of Artificial Intelligence, Renmin University of China",
        "ByteDance Seed",
    )
    assert enriched.affiliation_source == "Official arXiv HTML and project page"
    assert has_industry_qualification(classified)
