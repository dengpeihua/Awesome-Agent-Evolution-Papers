from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

import httpx

from .archive import TOPIC_TITLES, ArchiveRepository
from .highlight import highlight_priority
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
    all_papers = sorted(papers, key=highlight_priority, reverse=True)
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
        grouped: dict[str, list[Paper]] = {}
        for paper in selected:
            topic = paper.topics[0] if paper.topics else "other"
            grouped.setdefault(topic, []).append(paper)
        for topic, topic_papers in grouped.items():
            lines.extend([f"## {TOPIC_TITLES.get(topic, topic)}", ""])
            for paper in topic_papers:
                lines.append(f"- [{paper.title}]({paper.url})")
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

    async def send(self, markdown: str) -> None:
        """Send one logical message, splitting it when required by WeCom."""
        owns_client = self._client is None
        client = self._client or httpx.AsyncClient(timeout=httpx.Timeout(20))
        try:
            for chunk in split_markdown(markdown):
                response = await client.post(
                    self.webhook_url,
                    json={"msgtype": "markdown", "markdown": {"content": chunk}},
                )
                response.raise_for_status()
                payload = response.json()
                if payload.get("errcode") != 0:
                    raise RuntimeError(
                        f"Enterprise WeChat rejected the message: {payload.get('errmsg', payload)}"
                    )
        finally:
            if owns_client:
                await client.aclose()
