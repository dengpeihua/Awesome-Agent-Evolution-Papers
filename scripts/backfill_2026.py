from __future__ import annotations

import argparse
import asyncio
import html
import json
import re
import subprocess
import sys
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agent_paper_digest.archive import ArchiveRepository  # noqa: E402
from agent_paper_digest.arxiv import ArxivSource  # noqa: E402
from agent_paper_digest.candidates import CandidateRepository  # noqa: E402
from agent_paper_digest.highlight import classify_highlights  # noqa: E402
from agent_paper_digest.models import Paper  # noqa: E402
from agent_paper_digest.scholar import SemanticScholarEnricher  # noqa: E402
from agent_paper_digest.topics import (  # noqa: E402
    SELF_EVOLUTION_TOPIC,
    infer_topics_from_text,
)

CUTOFF = date.today()
VERIFY_DATE = CUTOFF.isoformat()
HISTORICAL_DISCOVERY_DAYS = 730

DISCOVERY_SOURCES = {
    "self-improving": (
        "https://raw.githubusercontent.com/selfimproving-agent/"
        "Awesome-Self-Improving-Agents/main/README.md"
    ),
    "agent-memory": (
        "https://raw.githubusercontent.com/AgentMemoryWorld/"
        "Awesome-Agent-Memory/main/papers/2026.md"
    ),
    "agent-memory-taxonomy": (
        "https://raw.githubusercontent.com/TeleAI-UAGI/Awesome-Agent-Memory/main/README.md"
    ),
}

EXTRA_ARXIV_TOPICS = {
    "2601.03570": ("llm-continual-training",),
    "2601.05874": ("llm-continual-training",),
    "2601.11658": (SELF_EVOLUTION_TOPIC,),
    "2602.18055": ("llm-continual-training",),
    "2602.11075": (SELF_EVOLUTION_TOPIC,),
    "2603.05872": (SELF_EVOLUTION_TOPIC,),
    "2603.12658": ("llm-continual-training",),
    "2603.15421": ("agent-memory",),
    "2603.19461": (SELF_EVOLUTION_TOPIC,),
    "2604.10923": (SELF_EVOLUTION_TOPIC, "agent-memory"),
    "2604.15082": (SELF_EVOLUTION_TOPIC,),
    "2604.18292": (SELF_EVOLUTION_TOPIC,),
    "2604.20714": (SELF_EVOLUTION_TOPIC,),
    "2605.17721": (SELF_EVOLUTION_TOPIC, "agent-memory"),
    "2605.23986": ("agent-memory",),
    "2606.04703": (SELF_EVOLUTION_TOPIC, "llm-continual-training"),
    "2606.06114": (SELF_EVOLUTION_TOPIC,),
    "2606.06448": ("agent-memory",),
    "2606.07367": (SELF_EVOLUTION_TOPIC,),
    "2606.10722": ("llm-continual-training",),
    "2606.24775": ("agent-memory",),
    "2607.12227": (SELF_EVOLUTION_TOPIC,),
    "2607.22529": (SELF_EVOLUTION_TOPIC,),
    "2608.02276": (SELF_EVOLUTION_TOPIC,),
    "2608.03392": (SELF_EVOLUTION_TOPIC,),
    "2608.03463": ("agent-memory",),
}


@dataclass(frozen=True, slots=True)
class ExternalCandidate:
    identifier: str
    url: str
    topics: tuple[str, ...]
    venue: str
    venue_tier: str
    doi: str = ""
    github_url: str = ""


EXTERNAL_CANDIDATES = (
    ExternalCandidate(
        "2026.acl-long.247",
        "https://aclanthology.org/2026.acl-long.247/",
        ("llm-continual-training",),
        "ACL 2026 (Main)",
        "ccf-a",
        "10.18653/v1/2026.acl-long.247",
        "https://github.com/alina1031/SLoRA",
    ),
    ExternalCandidate(
        "2026.findings-acl.483",
        "https://aclanthology.org/2026.findings-acl.483/",
        (SELF_EVOLUTION_TOPIC,),
        "ACL 2026 Findings",
        "",
        "10.18653/v1/2026.findings-acl.483",
    ),
    ExternalCandidate(
        "2026.findings-acl.1522",
        "https://aclanthology.org/2026.findings-acl.1522/",
        (SELF_EVOLUTION_TOPIC, "agent-memory"),
        "ACL 2026 Findings",
        "",
        "10.18653/v1/2026.findings-acl.1522",
    ),
    ExternalCandidate(
        "2026.findings-acl.250",
        "https://aclanthology.org/2026.findings-acl.250/",
        ("agent-memory",),
        "ACL 2026 Findings",
        "",
        "10.18653/v1/2026.findings-acl.250",
        "https://github.com/Hongyi4221/EMA",
    ),
)

KNOWN_ENRICHMENTS: dict[str, dict[str, object]] = {
    "2601.01885": {
        "venue": "ACL 2026 (Main)",
        "venue_tier": "top",
        "doi": "10.18653/v1/2026.acl-long.981",
        "industry_affiliations": ("Alibaba Group",),
    },
    "2601.05874": {
        "venue": "EACL 2026 (Main)",
        "venue_tier": "top",
        "doi": "10.18653/v1/2026.eacl-long.293",
    },
    "2602.11075": {
        "venue": "RSS 2026",
        "venue_tier": "top",
        "github_url": "https://github.com/OpenDriveLab/RISE",
    },
    "2603.15421": {
        "venue": "ACL 2026 Findings",
        "venue_tier": "notable",
    },
    "2603.19461": {
        "industry_affiliations": ("Meta",),
        "github_url": "https://github.com/facebookresearch/HyperAgents",
    },
    "2604.10923": {
        "venue": "ACL 2026 (Main)",
        "venue_tier": "top",
        "doi": "10.18653/v1/2026.acl-long.952",
        "github_url": "https://github.com/BUAA-IRIP-LLM/Mem2Evolve",
    },
    "2604.15082": {"venue": "DAC 2026", "venue_tier": "top"},
    "2604.18292": {
        "affiliations": (
            "Gaoling School of Artificial Intelligence, Renmin University of China",
            "ByteDance Seed",
        ),
        "first_author_affiliations": (
            "Gaoling School of Artificial Intelligence, Renmin University of China",
        ),
        "affiliation_source": "Official arXiv HTML and project page",
        "github_url": "https://github.com/RUC-NLPIR/Agent-World",
    },
    "2604.20714": {
        "venue": "ACL 2026 Findings",
        "venue_tier": "notable",
    },
    "2605.23904": {
        "industry_affiliations": ("Microsoft Research",),
        "github_url": "https://github.com/microsoft/SkillOpt",
    },
    "2606.07367": {"venue": "ICML 2026", "venue_tier": "top"},
    "2607.22529": {
        "industry_affiliations": ("Alibaba / Qwen",),
        "github_url": "https://github.com/Qwen-Applications/skill-self-play",
    },
}

CITATION_PRIORITY_IDS = {
    "2601.01885",
    "2601.02553",
    "2601.03192",
    "2601.03236",
    "2602.02007",
    "2602.02474",
    "2602.05665",
    "2602.06052",
    "2602.19320",
    "2603.03296",
    "2603.12658",
    "2603.19461",
    "2604.10923",
    "2605.13941",
    "2605.23904",
    "2606.03841",
    "2606.07367",
    "2607.13104",
    "2608.03392",
}

ARXIV_LINK = re.compile(
    r"\[([^\]\n]{8,220})\]\(https?://arxiv\.org/(?:abs|pdf)/"
    r"(26(?:0[1-9]|1[0-2])\.\d{4,5})(?:v\d+)?(?:\.pdf)?\)",
    re.IGNORECASE,
)
GITHUB_REPO = re.compile(r"https?://github\.com/([\w.-]+)/([\w.-]+)", re.IGNORECASE)


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def _topics_for_title(title: str) -> tuple[str, ...]:
    return infer_topics_from_text(title, "")


def _meta_values(page: str, name: str) -> list[str]:
    values: list[str] = []
    for tag in re.findall(r"<meta\b[^>]*>", page, re.IGNORECASE | re.DOTALL):
        attributes: dict[str, str] = {}
        for match in re.finditer(
            r"([:\w-]+)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
            tag,
            re.DOTALL,
        ):
            value = next(group for group in match.groups()[1:] if group is not None)
            attributes[match.group(1).lower()] = _normalize(value)
        if attributes.get("name", "").lower() == name.lower() and "content" in attributes:
            values.append(attributes["content"])
    return values


def _github_url(page: str) -> str:
    matches = GITHUB_REPO.findall(html.unescape(page))
    for owner, repository in matches:
        repository = repository.rstrip(".,;:)'\"")
        if repository.lower() not in {"topics", "features", "settings"}:
            return f"https://github.com/{owner}/{repository}"
    return ""


def _parse_date(raw: str, *, default: date | None = None) -> datetime:
    cleaned = raw.strip().replace("/", "-")
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            parsed = datetime.strptime(cleaned[: len(datetime.now().strftime(fmt))], fmt)
            month = parsed.month or 1
            day = parsed.day or 1
            return datetime(parsed.year, month, day, tzinfo=UTC)
        except ValueError:
            continue
    fallback = default or CUTOFF
    return datetime(fallback.year, fallback.month, fallback.day, tzinfo=UTC)


def _arxiv_v1_date(page: str, identifier: str) -> datetime:
    plain = _normalize(re.sub(r"<[^>]+>", " ", page))
    match = re.search(r"Submitted on\s+(\d{1,2}\s+[A-Z][a-z]{2}\s+\d{4})", plain)
    if match:
        return datetime.strptime(match.group(1), "%d %b %Y").replace(tzinfo=UTC)
    year = 2000 + int(identifier[:2])
    month = int(identifier[2:4])
    return datetime(year, month, 1, tzinfo=UTC)


def _paper_from_arxiv(identifier: str, topics: tuple[str, ...], page: str) -> Paper:
    title = (_meta_values(page, "citation_title") or [identifier])[0]
    abstract = (_meta_values(page, "citation_abstract") or [""])[0]
    authors = tuple(_meta_values(page, "citation_author"))
    raw_date = (
        _meta_values(page, "citation_online_date")
        or _meta_values(page, "citation_date")
        or [f"20{identifier[:2]}-{identifier[2:4]}-01"]
    )[0]
    published = _arxiv_v1_date(page, identifier)
    updated = _parse_date(raw_date, default=published.date())
    category_match = re.search(
        r'<span class="primary-subject">(.*?)</span>', page, re.IGNORECASE | re.DOTALL
    )
    category = _normalize(re.sub(r"<[^>]+>", "", category_match.group(1))) if category_match else ""
    category_code = ""
    code_match = re.search(r"\(([-\w.]+)\)\s*</span>", page, re.IGNORECASE)
    if code_match:
        category_code = code_match.group(1)
    return Paper(
        arxiv_id=identifier,
        title=title,
        abstract=abstract,
        authors=authors,
        published=published,
        updated=updated,
        url=f"https://arxiv.org/abs/{identifier}",
        pdf_url=f"https://arxiv.org/pdf/{identifier}",
        primary_category=category_code or category,
        categories=(category_code or category,) if (category_code or category) else (),
        topics=topics,
        github_url=_github_url(page),
        verified_at=VERIFY_DATE,
    )


def _paper_from_external(candidate: ExternalCandidate, page: str) -> Paper:
    title = (_meta_values(page, "citation_title") or [candidate.identifier])[0]
    abstracts = _meta_values(page, "citation_abstract")
    if abstracts:
        abstract = abstracts[0]
    else:
        match = re.search(
            r'class="card-body acl-abstract".*?<span>(.*?)</span>',
            page,
            re.IGNORECASE | re.DOTALL,
        )
        abstract = _normalize(re.sub(r"<[^>]+>", " ", match.group(1))) if match else ""
    authors = tuple(_meta_values(page, "citation_author"))
    raw_date = (
        _meta_values(page, "citation_publication_date")
        or _meta_values(page, "citation_date")
        or ["2026-07-02"]
    )[0]
    pdf_url = (
        _meta_values(page, "citation_pdf_url")
        or [candidate.url.rstrip("/") + ".pdf"]
    )[0]
    return Paper(
        arxiv_id=candidate.identifier,
        title=title,
        abstract=abstract,
        authors=authors,
        published=_parse_date(raw_date, default=date(2026, 7, 2)),
        updated=_parse_date(raw_date, default=date(2026, 7, 2)),
        url=candidate.url,
        pdf_url=pdf_url,
        primary_category="cs.CL",
        categories=("cs.CL",),
        topics=candidate.topics,
        doi=candidate.doi,
        venue=candidate.venue,
        venue_tier=candidate.venue_tier,
        github_url=candidate.github_url,
        verified_at=VERIFY_DATE,
    )


async def _get(client: httpx.AsyncClient, url: str) -> str:
    for attempt in range(4):
        try:
            response = await client.get(url)
        except httpx.HTTPError:
            if attempt == 3:
                raise
            await asyncio.sleep(1.5 * (attempt + 1))
            continue
        if response.status_code == 200:
            return response.text
        if response.status_code not in {429, 500, 502, 503, 504}:
            response.raise_for_status()
        await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Unable to retrieve {url} after retries")


async def discover_candidates(
    client: httpx.AsyncClient,
    *,
    official_source: ArxivSource | None = None,
) -> dict[str, tuple[str, ...]]:
    pages = await asyncio.gather(*(_get(client, url) for url in DISCOVERY_SOURCES.values()))
    candidates: dict[str, set[str]] = {}
    for page in pages:
        for title, identifier in ARXIV_LINK.findall(page):
            topics = _topics_for_title(_normalize(title).strip("*"))
            if topics:
                candidates.setdefault(identifier, set()).update(topics)
    for identifier, topics in EXTRA_ARXIV_TOPICS.items():
        candidates.setdefault(identifier, set()).update(topics)
    source = official_source or ArxivSource(client=client)
    history_start = datetime.combine(
        CUTOFF - timedelta(days=HISTORICAL_DISCOVERY_DAYS),
        datetime.min.time(),
        tzinfo=UTC,
    )
    try:
        official_papers = await source.fetch(
            since=history_start,
            max_results_per_topic=100,
        )
    except (httpx.HTTPError, RuntimeError, ValueError) as error:
        print(f"WARN official arXiv historical discovery: {error}")
        official_papers = []
    for paper in official_papers:
        candidates.setdefault(paper.arxiv_id, set()).update(paper.topics)
    return {identifier: tuple(sorted(topics)) for identifier, topics in candidates.items()}


async def fetch_papers(
    client: httpx.AsyncClient, candidates: dict[str, tuple[str, ...]]
) -> list[Paper]:
    semaphore = asyncio.Semaphore(5)

    async def fetch_one(identifier: str, topics: tuple[str, ...]) -> Paper | None:
        async with semaphore:
            try:
                page = await _get(client, f"https://arxiv.org/abs/{identifier}")
                paper = _paper_from_arxiv(identifier, topics, page)
                return paper if paper.published.date() <= CUTOFF else None
            except (httpx.HTTPError, RuntimeError, ValueError) as error:
                print(f"WARN metadata {identifier}: {error}")
                return None

    papers = await asyncio.gather(
        *(fetch_one(identifier, topics) for identifier, topics in sorted(candidates.items()))
    )
    output = [paper for paper in papers if paper is not None]

    async def fetch_external(candidate: ExternalCandidate) -> Paper | None:
        try:
            page = await _get(client, candidate.url)
            return _paper_from_external(candidate, page)
        except (httpx.HTTPError, RuntimeError, ValueError) as error:
            print(f"WARN metadata {candidate.identifier}: {error}")
            return None

    external_papers = await asyncio.gather(
        *(fetch_external(candidate) for candidate in EXTERNAL_CANDIDATES)
    )
    output.extend(paper for paper in external_papers if paper is not None)
    return output


def _github_token() -> str:
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return ""


async def enrich_github_stars(client: httpx.AsyncClient, papers: list[Paper]) -> list[Paper]:
    token = _github_token()
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    semaphore = asyncio.Semaphore(8)
    cache: dict[str, int | None] = {}

    async def stars(url: str) -> int | None:
        match = GITHUB_REPO.match(url)
        if not match:
            return None
        slug = f"{match.group(1)}/{match.group(2).rstrip('.')}"
        if slug in cache:
            return cache[slug]
        response: httpx.Response | None = None
        for attempt in range(3):
            try:
                async with semaphore:
                    response = await client.get(
                        f"https://api.github.com/repos/{slug}", headers=headers
                    )
                break
            except httpx.HTTPError:
                if attempt < 2:
                    await asyncio.sleep(attempt + 1)
        if response is not None and response.status_code == 200:
            value = int(response.json()["stargazers_count"])
        else:
            value = None
        cache[slug] = value
        return value

    values = await asyncio.gather(*(stars(paper.github_url) for paper in papers))
    return [replace(paper, github_stars=value) for paper, value in zip(papers, values, strict=True)]


async def enrich_citations(client: httpx.AsyncClient, papers: list[Paper]) -> list[Paper]:
    enriched: list[Paper] = []
    for paper in papers:
        priority = (
            paper.arxiv_id in CITATION_PRIORITY_IDS
            or paper.venue_tier == "ccf-a"
            or (paper.github_stars or 0) >= 100
        )
        if not priority:
            enriched.append(paper)
            continue
        query = quote_plus(f'"{paper.title}"')
        try:
            response = await client.get(
                f"https://scholar.google.com/scholar?q={query}",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            match = re.search(r"Cited by ([0-9,]+)", response.text)
            count = int(match.group(1).replace(",", "")) if match else None
        except httpx.HTTPError:
            count = None
        enriched.append(
            replace(
                paper,
                citation_count=count if count is not None else paper.citation_count,
                citation_source=(
                    "Google Scholar" if count is not None else paper.citation_source
                ),
            )
        )
        await asyncio.sleep(1.5)
    return enriched


def apply_known_enrichments(papers: list[Paper]) -> list[Paper]:
    output: list[Paper] = []
    for paper in papers:
        values = KNOWN_ENRICHMENTS.get(paper.arxiv_id)
        output.append(replace(paper, **values) if values else paper)
    return output


async def run(root: Path, *, skip_citations: bool) -> tuple[Paper, ...]:
    previous_path = root / "data" / "papers.json"
    previous: dict[str, Paper] = {}
    if previous_path.exists():
        previous = {
            paper.arxiv_id: paper
            for paper in (
                Paper.from_dict(value)
                for value in json.loads(previous_path.read_text(encoding="utf-8"))
            )
        }
    timeout = httpx.Timeout(60)
    headers = {"User-Agent": "Awesome-Agent-Evolution-Papers/1.0"}
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, headers=headers) as client:
        candidates = await discover_candidates(client)
        print(f"Discovered {len(candidates)} arXiv candidates")
        papers = await fetch_papers(client, candidates)
        print(f"Verified {len(papers)} papers at or before {CUTOFF}")
        papers = apply_known_enrichments(papers)
        papers = await enrich_github_stars(client, papers)
        papers = [
            replace(
                paper,
                citation_count=previous[paper.arxiv_id].citation_count,
                citation_source=previous[paper.arxiv_id].citation_source,
            )
            if paper.arxiv_id in previous
            else paper
            for paper in papers
        ]
        papers = await SemanticScholarEnricher(client=client).enrich(papers)
        if not skip_citations:
            papers = await enrich_citations(client, papers)
    papers = [classify_highlights(paper) for paper in papers]
    CandidateRepository(root).save(papers)
    result = ArchiveRepository(root).replace_dataset(papers)
    audit = {
        "cutoff": CUTOFF.isoformat(),
        "generated_at": datetime.now(UTC).isoformat(),
        "paper_count": len(result),
        "topic_counts": {
            topic: sum(topic in paper.topics for paper in result)
            for topic in (
                SELF_EVOLUTION_TOPIC,
                "agent-memory",
                "llm-continual-training",
            )
        },
        "month_counts": {
            f"2026-{month:02d}": sum(
                paper.published.year == 2026 and paper.published.month == month
                for paper in result
            )
            for month in range(1, 9)
        },
        "github_metrics": sum(paper.github_stars is not None for paper in result),
        "citation_metrics": sum(paper.citation_count is not None for paper in result),
        "industry_flags": sum(bool(paper.industry_affiliations) for paper in result),
        "ccf_a_flags": sum(paper.venue_tier == "ccf-a" for paper in result),
        "eccv_emnlp_flags": sum(
            paper.venue_tier == "selected-extra" for paper in result
        ),
        "discovery_sources": list(DISCOVERY_SOURCES.values()),
        "notes": [
            "Discovery lists provide recall only; metadata is rechecked on paper pages.",
            "Missing star and citation metrics are represented as null, never estimated.",
            "Only strict public-policy qualifiers are written to data/papers.json.",
            "Counts are snapshots as of the cutoff date and will change over time.",
        ],
    }
    audit_path = root / "data" / "candidate_backfill_audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill the verified 2026 paper corpus")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root",
    )
    parser.add_argument(
        "--skip-citations",
        action="store_true",
        help="Skip the small Google Scholar verification pass",
    )
    args = parser.parse_args()
    papers = asyncio.run(run(args.root.resolve(), skip_citations=args.skip_citations))
    print(f"Wrote {len(papers)} papers to {args.root.resolve()}")


if __name__ == "__main__":
    main()
