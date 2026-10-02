from __future__ import annotations

import asyncio
import time
from collections.abc import Iterable
from datetime import datetime

import httpx

from .archive import TOPIC_TITLES, ArchiveRepository
from .highlight import has_industry_qualification
from .models import Paper


def build_digest_markdown(
    papers: Iterable[Paper],
    *,
    archive_url: str,
    max_papers: int,
    coverage_start: datetime | None = None,
    coverage_end: datetime | None = None,
) -> str:
    """Build concise enterprise WeChat Markdown for one run."""
    all_papers = sorted(papers, key=lambda p: (p.published, p.updated, p.arxiv_id), reverse=True)
    selected = all_papers[:max_papers]
    lines = ["# Agent 研究论文日报", ""]
    if coverage_start and coverage_end:
        lines.extend(
            [
                f"> 补推范围：{coverage_start.isoformat()} → {coverage_end.isoformat()}",
                "",
            ]
        )
    if not selected:
        lines.extend(["> 今日检索完成，未发现尚未归档的新论文。", ""])
    else:
        for paper in selected:
            topics = ", ".join(TOPIC_TITLES.get(topic, topic) for topic in paper.topics)
            lines.append(f"- **{paper.published.date()}** [{paper.title}]({paper.url})")
            lines.append(f"  - {topics}")
            if (
                coverage_end
                and paper.published.astimezone(coverage_end.tzinfo).date() == coverage_end.date()
                and has_industry_qualification(paper)
            ):
                lines.append("  - **🆕 当天新发布的大厂论文**")
            signals = ArchiveRepository._flags(paper)
            if signals != "—":
                lines.append(f"  - **重点：** {signals.replace('<br>', '；')}")
            if paper.acceptance_evidence:
                lines.append(f"  - **依据：** {paper.acceptance_evidence}")
            lines.append("")
        remaining = len(all_papers) - len(selected)
        if remaining > 0:
            lines.extend([f"> {remaining} more paper(s) are available in the archive.", ""])
    if archive_url:
        lines.append(f"[查看完整归档]({archive_url})")
    return "\n".join(lines).strip()


def build_digest_messages(
    papers: Iterable[Paper],
    *,
    archive_url: str,
    max_papers: int,
    coverage_start: datetime | None = None,
    coverage_end: datetime | None = None,
) -> list[str]:
    """Deliver every paper in chronological batches, never discard overflow."""
    if max_papers < 1:
        raise ValueError("max_papers must be positive")
    ordered = sorted(papers, key=lambda p: (p.published, p.updated, p.arxiv_id), reverse=True)
    batches = [ordered[i : i + max_papers] for i in range(0, len(ordered), max_papers)] or [[]]
    return [
        build_digest_markdown(
            batch,
            archive_url=archive_url,
            max_papers=max_papers,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
        )
        + (f"\n\n> 第 {index + 1}/{len(batches)} 批，共 {len(ordered)} 篇。" if ordered else "")
        for index, batch in enumerate(batches)
    ]


def split_markdown(text: str, *, limit: int = 3800) -> list[str]:
    """Split Markdown into chunks that fit the WeCom UTF-8 byte limit."""
    if limit <= 0:
        raise ValueError("limit must be positive")
    chunks: list[str] = []
    current = ""
    for line in text.splitlines(keepends=True):
        remaining = line
        while remaining:
            candidate = current + remaining
            if len(candidate.encode("utf-8")) <= limit:
                current = candidate
                remaining = ""
                continue
            if current:
                chunks.append(current.rstrip())
                current = ""
                continue
            boundary = 0
            byte_count = 0
            for index, character in enumerate(remaining):
                char_bytes = len(character.encode("utf-8"))
                if byte_count + char_bytes > limit:
                    break
                byte_count += char_bytes
                boundary = index + 1
            if boundary == 0:
                raise ValueError("limit is too small for one UTF-8 character")
            chunks.append(remaining[:boundary].rstrip())
            remaining = remaining[boundary:]
    if current:
        chunks.append(current.rstrip())
    return chunks or [""]


class WeComNotifier:
    """Send Markdown through an enterprise WeChat group bot webhook."""

    def __init__(self, webhook_url: str, *, client: httpx.AsyncClient | None = None) -> None:
        if not webhook_url.startswith("https://qyapi.weixin.qq.com/cgi-bin/webhook/send"):
            raise ValueError("Invalid enterprise WeChat group bot webhook URL")
        self.webhook_url = webhook_url
        self._client = client
        self._last_sent_at = 0.0

    async def send(self, markdown: str) -> None:
        """Send one logical message, splitting it when required by WeCom."""
        owns_client = self._client is None
        client = self._client or httpx.AsyncClient(timeout=httpx.Timeout(20))
        try:
            for chunk in split_markdown(markdown):
                # Space requests across batches as well as byte-limit chunks.
                delay = 3.1 - (time.monotonic() - self._last_sent_at)
                if delay > 0:
                    await asyncio.sleep(delay)
                response = await client.post(
                    self.webhook_url,
                    json={"msgtype": "markdown", "markdown": {"content": chunk}},
                )
                response.raise_for_status()
                self._last_sent_at = time.monotonic()
                payload = response.json()
                if payload.get("errcode") != 0:
                    raise RuntimeError(
                        f"Enterprise WeChat rejected the message: {payload.get('errmsg', payload)}"
                    )
        finally:
            if owns_client:
                await client.aclose()
