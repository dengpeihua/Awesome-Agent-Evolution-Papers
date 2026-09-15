from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class Paper:
    """Normalized paper metadata used by every integration."""

    arxiv_id: str
    title: str
    abstract: str
    authors: tuple[str, ...]
    published: datetime
    updated: datetime
    url: str
    pdf_url: str
    primary_category: str
    categories: tuple[str, ...]
    topics: tuple[str, ...]
    doi: str = ""
    comment: str = ""
    journal_ref: str = ""
    venue: str = ""
    venue_tier: str = ""
    venue_source: str = ""
    acceptance_evidence: str = ""
    github_url: str = ""
    github_stars: int | None = None
    citation_count: int | None = None
    citation_source: str = ""
    affiliations: tuple[str, ...] = ()
    first_author_affiliations: tuple[str, ...] = ()
    industry_affiliations: tuple[str, ...] = ()
    industry_first_author_affiliations: tuple[str, ...] = ()
    affiliation_source: str = ""
    highlight_reasons: tuple[str, ...] = ()
    verified_at: str = ""

    def merge(self, other: Paper) -> Paper:
        """Merge topic labels and prefer the most recently updated metadata.

        Args:
            other: Paper with the same stable arXiv identifier.

        Returns:
            A single paper with the union of both topic sets.

        Raises:
            ValueError: If the paper identifiers differ.
        """
        if self.arxiv_id != other.arxiv_id:
            raise ValueError("Cannot merge papers with different arXiv identifiers")
        newest = other if other.updated >= self.updated else self
        older = self if newest is other else other
        return replace(
            newest,
            topics=tuple(sorted(set(self.topics) | set(other.topics))),
            doi=newest.doi or older.doi,
            comment=newest.comment or older.comment,
            journal_ref=newest.journal_ref or older.journal_ref,
            venue=newest.venue or older.venue,
            venue_tier=newest.venue_tier or older.venue_tier,
            venue_source=newest.venue_source or older.venue_source,
            acceptance_evidence=newest.acceptance_evidence or older.acceptance_evidence,
            github_url=newest.github_url or older.github_url,
            github_stars=(
                newest.github_stars
                if newest.github_stars is not None
                else older.github_stars
            ),
            citation_count=(
                newest.citation_count
                if newest.citation_count is not None
                else older.citation_count
            ),
            citation_source=newest.citation_source or older.citation_source,
            affiliations=tuple(sorted(set(self.affiliations) | set(other.affiliations))),
            first_author_affiliations=(
                newest.first_author_affiliations or older.first_author_affiliations
            ),
            industry_affiliations=tuple(
                sorted(set(self.industry_affiliations) | set(other.industry_affiliations))
            ),
            industry_first_author_affiliations=tuple(
                sorted(
                    set(self.industry_first_author_affiliations)
                    | set(other.industry_first_author_affiliations)
                )
            ),
            affiliation_source=newest.affiliation_source or older.affiliation_source,
            highlight_reasons=tuple(
                sorted(set(self.highlight_reasons) | set(other.highlight_reasons))
            ),
            verified_at=newest.verified_at or older.verified_at,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize this paper to a stable JSON-compatible dictionary."""
        return {
            "arxiv_id": self.arxiv_id,
            "title": self.title,
            "abstract": self.abstract,
            "authors": list(self.authors),
            "published": self.published.isoformat(),
            "updated": self.updated.isoformat(),
            "url": self.url,
            "pdf_url": self.pdf_url,
            "primary_category": self.primary_category,
            "categories": list(self.categories),
            "topics": list(self.topics),
            "doi": self.doi,
            "comment": self.comment,
            "journal_ref": self.journal_ref,
            "venue": self.venue,
            "venue_tier": self.venue_tier,
            "venue_source": self.venue_source,
            "acceptance_evidence": self.acceptance_evidence,
            "github_url": self.github_url,
            "github_stars": self.github_stars,
            "citation_count": self.citation_count,
            "citation_source": self.citation_source,
            "affiliations": list(self.affiliations),
            "first_author_affiliations": list(self.first_author_affiliations),
            "industry_affiliations": list(self.industry_affiliations),
            "industry_first_author_affiliations": list(
                self.industry_first_author_affiliations
            ),
            "affiliation_source": self.affiliation_source,
            "highlight_reasons": list(self.highlight_reasons),
            "verified_at": self.verified_at,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Paper:
        """Restore a paper from a serialized dictionary.

        Args:
            value: Dictionary produced by :meth:`to_dict`.

        Returns:
            Restored immutable paper.
        """
        return cls(
            arxiv_id=str(value["arxiv_id"]),
            title=str(value["title"]),
            abstract=str(value["abstract"]),
            authors=tuple(value.get("authors", [])),
            published=datetime.fromisoformat(str(value["published"])),
            updated=datetime.fromisoformat(str(value["updated"])),
            url=str(value["url"]),
            pdf_url=str(value["pdf_url"]),
            primary_category=str(value.get("primary_category", "")),
            categories=tuple(value.get("categories", [])),
            topics=tuple(value.get("topics", [])),
            doi=str(value.get("doi", "")),
            comment=str(value.get("comment", "")),
            journal_ref=str(value.get("journal_ref", "")),
            venue=str(value.get("venue", "")),
            venue_tier=str(value.get("venue_tier", "")),
            venue_source=str(value.get("venue_source", "")),
            acceptance_evidence=str(value.get("acceptance_evidence", "")),
            github_url=str(value.get("github_url", "")),
            github_stars=(
                int(value["github_stars"])
                if value.get("github_stars") is not None
                else None
            ),
            citation_count=(
                int(value["citation_count"])
                if value.get("citation_count") is not None
                else None
            ),
            citation_source=str(value.get("citation_source", "")),
            affiliations=tuple(value.get("affiliations", [])),
            first_author_affiliations=tuple(value.get("first_author_affiliations", [])),
            industry_affiliations=tuple(value.get("industry_affiliations", [])),
            industry_first_author_affiliations=tuple(
                value.get("industry_first_author_affiliations", [])
            ),
            affiliation_source=str(value.get("affiliation_source", "")),
            highlight_reasons=tuple(value.get("highlight_reasons", [])),
            verified_at=str(value.get("verified_at", "")),
        )
