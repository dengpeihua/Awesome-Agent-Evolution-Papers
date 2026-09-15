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
        )

    def coverage_start(self, now: datetime, *, fallback_days: int) -> datetime:
        state = self.load()
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
        self.path.write_text(
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
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def stage(self, now: datetime, paper_ids: tuple[str, ...]) -> DigestState:
        current = self.load()
        state = DigestState(
            last_successful_run_at=current.last_successful_run_at,
            last_attempt_at=now,
            pending_paper_ids=tuple(
                dict.fromkeys((*current.pending_paper_ids, *paper_ids))
            ),
        )
        self._write(state)
        return state

    def complete(self, now: datetime) -> DigestState:
        state = DigestState(
            last_successful_run_at=now,
            last_attempt_at=now,
            pending_paper_ids=(),
        )
        self._write(state)
        return state
