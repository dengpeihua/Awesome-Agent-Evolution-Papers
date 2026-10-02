from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path


class GitCommandError(RuntimeError):
    """Raised when an automated Git command fails."""


class GitSync:
    """Commit generated archive artifacts and optionally push them to a remote."""

    def __init__(
        self,
        repo: Path | str,
        *,
        remote: str = "origin",
        branch: str = "main",
        auto_push: bool = True,
        author_name: str = "Agent Paper Digest Bot",
        author_email: str = "agent-paper-digest@users.noreply.github.com",
    ) -> None:
        self.repo = Path(repo).resolve()
        self.remote = remote
        self.branch = branch
        self.auto_push = auto_push
        self.author_name = author_name
        self.author_email = author_email

    async def _run(self, *args: str, allowed_codes: tuple[int, ...] = (0,)) -> tuple[int, str]:
        process = await asyncio.create_subprocess_exec(
            "git",
            *args,
            cwd=self.repo,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode(errors="replace").strip()
        if process.returncode not in allowed_codes:
            detail = stderr.decode(errors="replace").strip() or output
            raise GitCommandError(f"git {' '.join(args)} failed: {detail}")
        return process.returncode or 0, output

    async def sync(self, discovery_date: date) -> bool:
        """Stage generated outputs, commit when changed, and push.

        Args:
            discovery_date: Date inserted into the deterministic commit subject.

        Returns:
            ``True`` when a commit was created, otherwise ``False``.

        Raises:
            GitCommandError: If the directory is not a repository or Git fails.
        """
        await self._run("rev-parse", "--is-inside-work-tree")
        targets = [name for name in ("README.md", "data", "papers") if (self.repo / name).exists()]
        if not targets:
            return False
        await self._run("add", "-A", "--", *targets)
        return_code, _ = await self._run("diff", "--cached", "--quiet", allowed_codes=(0, 1))
        if return_code == 0:
            # A previous run may have committed successfully but failed to push.
            if self.auto_push:
                await self._run("push", "-u", self.remote, f"HEAD:{self.branch}")
            return False
        await self._run(
            "-c",
            f"user.name={self.author_name}",
            "-c",
            f"user.email={self.author_email}",
            "commit",
            "-m",
            f"docs: add paper digest for {discovery_date.isoformat()}",
        )
        if self.auto_push:
            await self._run("push", "-u", self.remote, f"HEAD:{self.branch}")
        return True

