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
        return replace(newest, topics=tuple(sorted(set(self.topics) | set(other.topics))))

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
        )

