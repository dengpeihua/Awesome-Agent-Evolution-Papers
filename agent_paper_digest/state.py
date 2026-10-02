from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DigestState:
    last_successful_run_at: datetime | None = None
    last_attempt_at: datetime | None = None
    pending_paper_ids: tuple[str, ...] = ()
    discovery_revision: str = ""


class DigestStateStore:
    """Persist catch-up cursor and undelivered paper identifiers."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / "data" / "digest_state.json"

    @staticmethod
    def _parse_datetime(value: object) -> datetime | None:
        if not value:
            return None
        parsed = datetime.fromisoformat(str(value))
        return parsed

    def load(self) -> DigestState:
        if not self.path.exists():
            return DigestState()
        value = json.loads(self.path.read_text(encoding="utf-8"))
        return DigestState(
            last_successful_run_at=self._parse_datetime(value.get("last_successful_run_at")),
            last_attempt_at=self._parse_datetime(value.get("last_attempt_at")),
            pending_paper_ids=tuple(value.get("pending_paper_ids", [])),
            discovery_revision=str(value.get("discovery_revision", "")),
        )

    def coverage_start(
        self,
        now: datetime,
        *,
        fallback_days: int,
        discovery_revision: str = "",
        historical_backfill_days: int = 730,
    ) -> datetime:
        state = self.load()
        if discovery_revision and state.discovery_revision != discovery_revision:
            historical_start = now - timedelta(days=historical_backfill_days)
            if state.last_successful_run_at is None:
                return historical_start
            successful = state.last_successful_run_at
            successful = successful if successful.tzinfo else successful.replace(tzinfo=now.tzinfo)
            return min(successful, historical_start)
        if state.last_successful_run_at is not None:
            value = state.last_successful_run_at
            return value if value.tzinfo else value.replace(tzinfo=now.tzinfo)
        discovery_path = self.root / "data" / "discoveries.json"
        if discovery_path.exists():
            discoveries = json.loads(discovery_path.read_text(encoding="utf-8"))
            if discoveries:
                latest = max(datetime.fromisoformat(str(day)).date() for day in discoveries)
                return datetime.combine(latest, time.min, tzinfo=now.tzinfo)
        return now - timedelta(days=fallback_days)

    def _write(self, state: DigestState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(
                {
                    "last_successful_run_at": (
                        state.last_successful_run_at.isoformat()
                        if state.last_successful_run_at
                        else None
                    ),
                    "last_attempt_at": (
                        state.last_attempt_at.isoformat() if state.last_attempt_at else None
                    ),
                    "pending_paper_ids": list(state.pending_paper_ids),
                    "discovery_revision": state.discovery_revision,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)

    def restore(self, state: DigestState) -> None:
        """Roll back local completion when publishing the success ledger fails."""
        self._write(state)

    def stage(self, now: datetime, paper_ids: tuple[str, ...]) -> DigestState:
        current = self.load()
        state = DigestState(
            last_successful_run_at=current.last_successful_run_at,
            last_attempt_at=now,
            pending_paper_ids=tuple(dict.fromkeys((*current.pending_paper_ids, *paper_ids))),
            discovery_revision=current.discovery_revision,
        )
        self._write(state)
        return state

    def complete(self, now: datetime, *, discovery_revision: str = "") -> DigestState:
        state = DigestState(
            last_successful_run_at=now,
            last_attempt_at=now,
            pending_paper_ids=(),
            discovery_revision=discovery_revision,
        )
        self._write(state)
        return state
