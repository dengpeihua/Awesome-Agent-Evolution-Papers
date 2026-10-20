from __future__ import annotations

import asyncio
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from typing import Final

import httpx

from .models import Paper
from .topics import MIN_PUBLICATION_DATE, normalize_topics

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
        author_nodes = entry.findall(f"{{{ATOM}}}author")
        author_affiliations = [
            tuple(
                affiliation
                for affiliation in (
                    _normalized_text(node.text)
                    for node in author.findall(f"{{{ARXIV}}}affiliation")
                )
                if affiliation
            )
            for author in author_nodes
        ]
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=_normalized_text(entry.findtext(f"{{{ATOM}}}title")),
                abstract=_normalized_text(entry.findtext(f"{{{ATOM}}}summary")),
                authors=tuple(
                    _normalized_text(author.findtext(f"{{{ATOM}}}name")) for author in author_nodes
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
                topics=normalize_topics((topic,)),
                doi=_normalized_text(entry.findtext(f"{{{ARXIV}}}doi")),
                comment=_normalized_text(entry.findtext(f"{{{ARXIV}}}comment")),
                journal_ref=_normalized_text(entry.findtext(f"{{{ARXIV}}}journal_ref")),
                affiliations=tuple(
                    dict.fromkeys(
                        affiliation
                        for affiliations in author_affiliations
                        for affiliation in affiliations
                    )
                ),
                first_author_affiliations=(author_affiliations[0] if author_affiliations else ()),
                affiliation_source=("arXiv author metadata" if any(author_affiliations) else ""),
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
        max_retries: int = 3,
        retry_base_seconds: float = 5.0,
    ) -> None:
        self._client = client
        self.request_delay_seconds = request_delay_seconds
        self.max_retries = max_retries
        self.retry_base_seconds = retry_base_seconds

    @property
    def discovery_revision(self) -> str:
        """Fingerprint the active queries so taxonomy changes trigger a rescan."""
        payload = json.dumps(
            self.topic_queries(),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return f"arxiv-{hashlib.sha256(payload).hexdigest()[:16]}"

    async def _request_page(
        self,
        client: httpx.AsyncClient,
        *,
        params: dict[str, str | int],
    ) -> httpx.Response:
        for attempt in range(self.max_retries + 1):
            try:
                response = await client.get(self.API_URL, params=params)
            except httpx.RequestError:
                if attempt == self.max_retries:
                    raise
                delay = self.retry_base_seconds * (2**attempt)
                if delay > 0:
                    await asyncio.sleep(delay)
                continue
            if response.status_code not in {429, 503}:
                response.raise_for_status()
                return response
            if attempt == self.max_retries:
                response.raise_for_status()
            retry_after = response.headers.get("Retry-After", "").strip()
            try:
                delay = float(retry_after)
            except ValueError:
                delay = self.retry_base_seconds * (2**attempt)
            if delay > 0:
                await asyncio.sleep(delay)
        raise RuntimeError("arXiv retry loop exited unexpectedly")

    @staticmethod
    def topic_queries() -> dict[str, str]:
        """Return queries for all four requested research tracks."""
        return {
            "long-horizon-agent": (
                '(all:"long-horizon" OR all:"long horizon" OR all:"long trajectories" '
                'OR all:"long-running tasks" OR all:"multi-step tasks") '
                'AND (all:"agent" OR all:"agentic") '
                'AND (all:"LLM" OR all:"language model" OR all:"language agents")'
            ),
            "reinforcement-learning": (
                '(ti:"reinforcement learning" OR abs:"reinforcement learning" '
                'OR ti:"RLHF" OR abs:"RLHF" OR ti:"GRPO" OR abs:"GRPO" '
                'OR ti:"RLAIF" OR abs:"RLAIF" OR ti:"RLVR" OR abs:"RLVR") '
                'AND (ti:"language model" OR abs:"language model" '
                'OR ti:"LLM" OR abs:"LLM" OR ti:"LLMs" OR abs:"LLMs" '
                'OR ti:"vision-language" OR abs:"vision-language")'
            ),
            "agent-llm-self-evolution": (
                '((all:"self-evolving" OR all:"self-improving" '
                'OR all:"recursive self-improvement" '
                'OR all:"self-improving language model" '
                'OR all:"iterative self-improvement" '
                'OR all:"self-rewarding language model" '
                'OR all:"self-generated feedback" '
                'OR all:"agent self-evolution" OR all:"evolving agent" '
                'OR all:"evolving skills" OR all:"self-consolidation") '
                'AND (all:"agent" OR all:"agentic" OR all:"LLM" '
                'OR all:"large language model" OR all:"foundation model"))'
            ),
            "llm-continual-training": (
                '((all:"continual learning" OR all:"continual training" '
                'OR all:"continual adaptation" OR all:"continual pre-training" '
                'OR all:"continual post-training" OR all:"continual fine-tuning" '
                'OR all:"online adaptation" OR all:"lifelong learning" '
                'OR all:"life-long learning" OR all:"catastrophic forgetting") '
                'AND (all:"large language model" OR all:"language model" '
                'OR all:"foundation model" OR all:"LLM"))'
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
            request_index = 0
            for topic, query in queries:
                start = 0
                while True:
                    if request_index and self.request_delay_seconds > 0:
                        await asyncio.sleep(self.request_delay_seconds)
                    response = await self._request_page(
                        client,
                        params={
                            "search_query": (
                                f"({query}) AND submittedDate:[202505010000 TO "
                                f"{datetime.now(UTC):%Y%m%d%H%M}]"
                            ),
                            "start": start,
                            "max_results": max_results_per_topic,
                            "sortBy": "lastUpdatedDate",
                            "sortOrder": "descending",
                        },
                    )
                    request_index += 1
                    page = parse_arxiv_feed(response.text, topic=topic)
                    if not page:
                        break
                    recent = [
                        paper for paper in page if max(paper.published, paper.updated) >= since
                    ]
                    for paper in recent:
                        if paper.published < MIN_PUBLICATION_DATE:
                            continue
                        existing = merged.get(paper.arxiv_id)
                        merged[paper.arxiv_id] = existing.merge(paper) if existing else paper
                    if len(page) < max_results_per_topic or len(recent) < len(page):
                        break
                    start += len(page)
        finally:
            if owns_client:
                await client.aclose()
        return sorted(merged.values(), key=lambda paper: paper.updated, reverse=True)
