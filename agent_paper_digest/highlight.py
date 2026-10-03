from __future__ import annotations

import re
from dataclasses import replace
from typing import Final

from .models import Paper
from .topics import MIN_PUBLICATION_DATE, REQUIRED_TOPICS, infer_topics

HIGH_CITATION_COUNT: Final = 10

INDUSTRY_PATTERNS: Final[tuple[tuple[str, re.Pattern[str]], ...]] = tuple(
    (name, re.compile(pattern, re.IGNORECASE))
    for name, pattern in (
        ("OpenAI", r"\bopenai\b"),
        ("Google / DeepMind", r"\bgoogle(?: research| deepmind)?\b|\bdeepmind\b"),
        ("Microsoft", r"\bmicrosoft\b"),
        ("Meta", r"\bmeta(?: ai)?\b|facebook ai research"),
        ("Anthropic", r"\banthropic\b"),
        ("Amazon", r"\bamazon\b|\baws\b"),
        ("Apple", r"\bapple\b"),
        ("NVIDIA", r"\bnvidia\b"),
        ("IBM", r"\bibm\b"),
        ("Adobe", r"\badobe\b"),
        ("Intel", r"\bintel\b"),
        ("Salesforce", r"\bsalesforce\b"),
        ("Oracle", r"\boracle\b"),
        ("NAVER", r"\bnaver\b"),
        ("Samsung", r"\bsamsung\b"),
        ("ByteDance", r"\bbytedance\b|\btik ?tok\b"),
        ("Alibaba", r"\balibaba\b|\bdamo academy\b|\bqwen\b|阿里(?:巴巴)?"),
        ("Tencent", r"\btencent\b|腾讯"),
        ("Baidu", r"\bbaidu\b|百度"),
        ("Huawei", r"\bhuawei\b|华为"),
        ("Ant Group", r"\bant group\b|蚂蚁集团"),
        ("JD.com", r"\bjd\.?(?:com)?\b|京东"),
        ("Xiaomi", r"\bxiaomi\b|小米"),
        ("Meituan", r"\bmeituan\b|美团"),
        ("Kuaishou", r"\bkuaishou\b|快手"),
        ("SenseTime", r"\bsensetime\b|商汤"),
        ("iFLYTEK", r"\biflytek\b|科大讯飞"),
        ("DeepSeek", r"\bdeepseek\b|深度求索"),
        ("Mistral AI", r"\bmistral ai\b"),
        ("xAI", r"\bxai\b"),
        ("Zhipu AI", r"\bzhipu\b|智谱"),
        ("Moonshot AI", r"\bmoonshot ai\b|月之暗面"),
        ("MiniMax", r"\bminimax\b"),
        ("Baichuan", r"\bbaichuan\b|百川智能"),
        ("01.AI", r"\b01\.ai\b|零一万物"),
    )
)

# AI venue watchlist plus selected ML conferences and journals.
# Main-conference labels exclude workshop and non-main-track evidence.
SELECTED_VENUE_PATTERNS: Final[tuple[tuple[str, str, re.Pattern[str]], ...]] = tuple(
    (name, tier, re.compile(pattern, re.IGNORECASE))
    for name, tier, pattern in (
        ("AAAI", "ccf-a", r"\baaai\b|aaai conference on artificial intelligence"),
        (
            "NeurIPS",
            "ccf-a",
            r"\b(?:neurips|nips)\b|(?:conference|advances) in neural information "
            r"processing systems",
        ),
        (
            "ACL",
            "ccf-a",
            r"\bacl\b|annual meeting of the association for computational linguistics",
        ),
        (
            "CVPR",
            "ccf-a",
            r"\bcvpr\b|conference on computer vision and pattern recognition",
        ),
        ("ICCV", "ccf-a", r"\biccv\b|international conference on computer vision"),
        ("ICML", "ccf-a", r"\bicml\b|international conference on machine learning"),
        (
            "IJCAI",
            "ccf-a",
            r"\bijcai\b|international joint conference on artificial intelligence",
        ),
        ("AI", "ccf-a", r"^\s*(?:AI|Artificial Intelligence(?: Journal)?)\s*(?:20\d{2})?\s*$"),
        (
            "TPAMI",
            "ccf-a",
            r"\b(?:tpami|pami)\b|transactions on pattern analysis and machine intelligence",
        ),
        ("IJCV", "ccf-a", r"\bijcv\b|international journal of computer vision"),
        ("JMLR", "ccf-a", r"\bjmlr\b|journal of machine learning research"),
        (
            "EMNLP",
            "selected-extra",
            r"\bemnlp\b|(?:conference on )?empirical methods in natural language processing",
        ),
        ("ECCV", "selected-extra", r"\beccv\b|european conference on computer vision"),
        (
            "ICLR",
            "selected-extra",
            r"\biclr\b|international conference on learning representations",
        ),
        (
            "Nature",
            "selected-extra",
            r"^\s*nature(?:\s+20\d{2})?\s*$|"
            r"\b(?:accepted (?:to|in)|published in|to appear in) nature"
            r"(?=\s*(?:20\d{2}\b|[.,;:]|$))",
        ),
        (
            "Science",
            "selected-extra",
            r"^\s*science(?:\s+20\d{2})?\s*$|"
            r"\b(?:accepted (?:to|in)|published in|to appear in) science"
            r"(?=\s*(?:20\d{2}\b|[.,;:]|$))",
        ),
        ("Nature Machine Intelligence", "selected-extra", r"\bnature machine intelligence\b"),
    )
)

ACCEPTANCE_PATTERN: Final = re.compile(
    r"\b(?:accepted|to appear|forthcoming|published|main conference|full paper|"
    r"regular paper|oral|spotlight)\b",
    re.IGNORECASE,
)
NON_MAIN_PATTERN: Final = re.compile(
    r"\b(?:workshop|findings|demo(?:nstration)?|short paper|industry track|"
    r"technical brief|summary|submitted|under review)\b",
    re.IGNORECASE,
)
PREPRINT_PATTERN: Final = re.compile(r"^\s*(?:arxiv(?:\.org)?|corr|preprint)\s*$", re.IGNORECASE)


def _industry_names(affiliations: tuple[str, ...]) -> tuple[str, ...]:
    text = " | ".join(affiliations)
    return tuple(name for name, pattern in INDUSTRY_PATTERNS if pattern.search(text))


def _venue_match(text: str) -> tuple[str, str, str] | None:
    for name, tier, pattern in SELECTED_VENUE_PATTERNS:
        match = pattern.search(text)
        if match:
            nearby = text[max(0, match.start() - 24) : match.end() + 32]
            year = re.search(r"20\d{2}", nearby)
            return name, f"{name} {year.group(0)}" if year else name, tier
    return None


def _publisher_record(paper: Paper) -> bool:
    return bool(
        paper.doi
        or re.search(
            r"(?:aclanthology\.org|proceedings\.mlr\.press|openaccess\.thecvf\.com|"
            r"aaai\.org|dl\.acm\.org|ieeexplore\.ieee\.org|jmlr\.org)",
            paper.url,
            re.IGNORECASE,
        )
    )


def _venue_evidence(paper: Paper) -> tuple[str, str, str, str] | None:
    for prefix, value in (
        ("arXiv comment", paper.comment),
        ("verified evidence", paper.acceptance_evidence),
    ):
        matched = _venue_match(value)
        if matched and ACCEPTANCE_PATTERN.search(value) and not NON_MAIN_PATTERN.search(value):
            name, label, tier = matched
            return name, label, tier, f"{prefix}: {value}"[:500]

    if paper.journal_ref:
        matched = _venue_match(paper.journal_ref)
        if matched and not NON_MAIN_PATTERN.search(paper.journal_ref):
            name, label, tier = matched
            return name, label, tier, f"arXiv journal reference: {paper.journal_ref}"[:500]

    matched = _venue_match(paper.venue)
    trusted_venue = (
        paper.venue_source
        and "arxiv" not in paper.venue_source.lower()
        and "manual" not in paper.venue_source.lower()
        and not PREPRINT_PATTERN.match(paper.venue)
    )
    if (
        matched
        and not NON_MAIN_PATTERN.search(paper.venue)
        and (trusted_venue or _publisher_record(paper))
    ):
        name, label, tier = matched
        source = paper.venue_source or "publisher record"
        return name, label, tier, f"{source}: {paper.venue}"[:500]
    return None


def has_industry_qualification(paper: Paper) -> bool:
    """Return whether affiliation evidence proves a qualifying big-tech work."""
    if paper.industry_first_author_affiliations:
        return True
    return bool(
        paper.industry_affiliations
        and paper.affiliation_source != "Semantic Scholar author profiles"
    )


def is_highly_cited(paper: Paper) -> bool:
    return paper.citation_count is not None and paper.citation_count >= HIGH_CITATION_COUNT


def qualification_reasons(paper: Paper) -> tuple[str, ...]:
    reasons: list[str] = []
    if paper.venue_tier == "ccf-a":
        reasons.append("CCF-A")
    elif paper.venue_tier == "selected-extra":
        reasons.append("Selected venue")
    if has_industry_qualification(paper):
        reasons.append("Industry")
    if is_highly_cited(paper):
        reasons.append("Highly cited")
    return tuple(reasons)


def is_eligible(paper: Paper) -> bool:
    """Include topical papers; priority evidence is a label, not an entry barrier."""
    return bool(
        paper.published >= MIN_PUBLICATION_DATE
        and REQUIRED_TOPICS.intersection(infer_topics(paper))
    )


def classify_highlights(paper: Paper) -> Paper:
    """Normalize affiliation and venue signals without trusting arXiv as a venue."""
    industry = _industry_names(paper.affiliations)
    first_author_industry = _industry_names(paper.first_author_affiliations)
    venue = _venue_evidence(paper)
    updates: dict[str, object] = {
        "topics": infer_topics(paper),
        "industry_affiliations": tuple(sorted(set(paper.industry_affiliations) | set(industry))),
        "industry_first_author_affiliations": tuple(
            sorted(set(paper.industry_first_author_affiliations) | set(first_author_industry))
        ),
        # Clear legacy generic "top" values. Only the explicit whitelist can restore a tier.
        "venue_tier": "",
    }
    if venue:
        _, label, tier, evidence = venue
        updates.update(
            venue=(label if PREPRINT_PATTERN.match(paper.venue) else paper.venue or label),
            venue_tier=tier,
            venue_source=paper.venue_source or "verified publication metadata",
            acceptance_evidence=evidence,
        )
    return replace(paper, **updates)


def highlight_priority(paper: Paper) -> tuple[int, int, int, int, int, object, str]:
    """Sort first-author industry and selected venues before other qualifying papers."""
    return (
        int(bool(paper.industry_first_author_affiliations)),
        int(paper.venue_tier == "ccf-a"),
        int(paper.venue_tier == "selected-extra"),
        int(has_industry_qualification(paper)),
        int(is_highly_cited(paper)),
        paper.updated,
        paper.arxiv_id,
    )


def promotion_signature(paper: Paper) -> tuple[object, ...]:
    """Return qualification signals whose first appearance merits notification."""
    return (
        paper.venue_tier,
        paper.venue if paper.venue_tier else "",
        paper.industry_first_author_affiliations,
        paper.industry_affiliations if has_industry_qualification(paper) else (),
        is_highly_cited(paper),
    )
