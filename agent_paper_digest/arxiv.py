from __future__ import annotations

import asyncio
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Final

import httpx

from .models import Paper

ATOM: Final = "http://www.w3.org/2005/Atom"
ARXIV: Final = "http://arxiv.org/schemas/atom"


def _normalized_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_arxiv_feed(xml: str, *, topic: str) -> list[Paper]:
    """Parse an arXiv Atom response into normalized papers.

    Args:
        xml: Atom XML returned by the arXiv export API.
        topic: Internal topic label associated with the query.

    Returns:
        Papers in the order returned by arXiv.

    Raises:
        xml.etree.ElementTree.ParseError: If the response is malformed XML.
    """
    root = ET.fromstring(xml)
    papers: list[Paper] = []
    for entry in root.findall(f"{{{ATOM}}}entry"):
        raw_id = _normalized_text(entry.findtext(f"{{{ATOM}}}id"))
        arxiv_id = re.sub(r"v\d+$", "", raw_id.rsplit("/", 1)[-1])
        links = entry.findall(f"{{{ATOM}}}link")
        url = next(
            (
                link.attrib.get("href", "")
                for link in links
                if link.attrib.get("rel") == "alternate"
            ),
            f"https://arxiv.org/abs/{arxiv_id}",
        )
        pdf_url = next(
            (
                link.attrib.get("href", "")
                for link in links
                if link.attrib.get("type") == "application/pdf"
            ),
            f"https://arxiv.org/pdf/{arxiv_id}",
        )
        primary = entry.find(f"{{{ARXIV}}}primary_category")
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=_normalized_text(entry.findtext(f"{{{ATOM}}}title")),
                abstract=_normalized_text(entry.findtext(f"{{{ATOM}}}summary")),
                authors=tuple(
                    _normalized_text(author.findtext(f"{{{ATOM}}}name"))
                    for author in entry.findall(f"{{{ATOM}}}author")
                ),
                published=_parse_datetime(entry.findtext(f"{{{ATOM}}}published") or ""),
                updated=_parse_datetime(entry.findtext(f"{{{ATOM}}}updated") or ""),
                url=url,
                pdf_url=pdf_url,
                primary_category=primary.attrib.get("term", "") if primary is not None else "",
                categories=tuple(
                    category.attrib.get("term", "")
                    for category in entry.findall(f"{{{ATOM}}}category")
                    if category.attrib.get("term")
                ),
                topics=(topic,),
            )
        )
    return papers


class ArxivSource:
    """Fetch precise topic searches from the official arXiv export API."""

    API_URL = "https://export.arxiv.org/api/query"

    def __init__(
        self,
        *,
        client: httpx.AsyncClient | None = None,
        request_delay_seconds: float = 3.1,
    ) -> None:
        self._client = client
        self.request_delay_seconds = request_delay_seconds

    @staticmethod
    def topic_queries() -> dict[str, str]:
        """Return high-precision queries for the three requested research tracks."""
        return {
            "agent-self-evolving": (
                '(all:"self-evolving agent" OR all:"self-improving agent" '
                'OR all:"agent self-evolution" OR all:"evolving agent")'
            ),
            "agent-memory": (
                '(all:"agent memory" OR all:"memory-augmented agent" '
                'OR all:"long-term memory agent" OR all:"memory for agents")'
            ),
            "llm-continual-training": (
                '((all:"continual learning" OR all:"continual training" '
                'OR all:"lifelong learning") AND (all:"large language model" '
                'OR all:"language model" OR all:"LLM"))'
            ),
        }

    async def fetch(self, *, since: datetime, max_results_per_topic: int) -> list[Paper]:
        """Fetch recent papers and merge duplicates found by multiple queries.

        Args:
            since: Keep entries published or updated at or after this instant.
            max_results_per_topic: Maximum Atom entries requested per query.

        Returns:
            Deduplicated recent papers ordered by most recent update.
        """
        owns_client = self._client is None
        client = self._client or httpx.AsyncClient(
            timeout=httpx.Timeout(30),
            follow_redirects=True,
            headers={"User-Agent": "Awesome-Agent-Evolution-Papers/0.1"},
        )
        merged: dict[str, Paper] = {}
        queries = list(self.topic_queries().items())
        try:
            for index, (topic, query) in enumerate(queries):
                response = await client.get(
                    self.API_URL,
                    params={
                        "search_query": query,
                        "start": 0,
                        "max_results": max_results_per_topic,
                        "sortBy": "lastUpdatedDate",
                        "sortOrder": "descending",
                    },
                )
                response.raise_for_status()
                for paper in parse_arxiv_feed(response.text, topic=topic):
                    if max(paper.published, paper.updated) < since:
                        continue
                    existing = merged.get(paper.arxiv_id)
                    merged[paper.arxiv_id] = existing.merge(paper) if existing else paper
                if index < len(queries) - 1 and self.request_delay_seconds > 0:
                    await asyncio.sleep(self.request_delay_seconds)
        finally:
            if owns_client:
                await client.aclose()
        return sorted(merged.values(), key=lambda paper: paper.updated, reverse=True)

