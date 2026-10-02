import asyncio
import subprocess
from datetime import date
from pathlib import Path

from agent_paper_digest.git_sync import GitSync


def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_sync_commits_and_pushes_to_configured_remote(tmp_path) -> None:
    remote = tmp_path / "remote.git"
    repo = tmp_path / "repo"
    git("init", "--bare", str(remote))
    git("init", "-b", "main", str(repo))
    git("config", "user.name", "Test User", cwd=repo)
    git("config", "user.email", "test@example.com", cwd=repo)
    git("remote", "add", "origin", str(remote), cwd=repo)
    (repo / "README.md").write_text("# First run\n", encoding="utf-8")
    sync = GitSync(
        repo,
        remote="origin",
        branch="main",
        auto_push=True,
        author_name="Digest Bot",
        author_email="digest@example.com",
    )

    changed = asyncio.run(sync.sync(date(2026, 7, 16)))

    assert changed is True
    assert git("log", "-1", "--format=%s", cwd=repo) == "docs: add paper digest for 2026-07-16"
    assert git("log", "-1", "--format=%an <%ae>", cwd=repo) == "Digest Bot <digest@example.com>"
    assert git("--git-dir", str(remote), "rev-parse", "refs/heads/main") == git(
        "rev-parse", "HEAD", cwd=repo
    )


def test_sync_is_noop_when_repository_has_no_changes(tmp_path) -> None:
    repo = tmp_path / "repo"
    git("init", "-b", "main", str(repo))
    git("config", "user.name", "Test User", cwd=repo)
    git("config", "user.email", "test@example.com", cwd=repo)
    (repo / "README.md").write_text("# Existing\n", encoding="utf-8")
    git("add", ".", cwd=repo)
    git("commit", "-m", "initial", cwd=repo)

    changed = asyncio.run(GitSync(repo, auto_push=False).sync(date(2026, 7, 16)))

    assert changed is False
    assert git("rev-list", "--count", "HEAD", cwd=repo) == "1"


def test_sync_retries_unpushed_commit_even_with_clean_worktree(tmp_path):
    remote = tmp_path / "remote.git"
    repo = tmp_path / "repo"
    git("init", "--bare", str(remote))
    git("init", "-b", "main", str(repo))
    git("config", "user.name", "Test", cwd=repo)
    git("config", "user.email", "test@example.com", cwd=repo)
    git("remote", "add", "origin", str(remote), cwd=repo)
    (repo / "README.md").write_text("pending publication", encoding="utf-8")
    asyncio.run(GitSync(repo, auto_push=False).sync(date(2026, 10, 3)))
    assert not asyncio.run(GitSync(repo).sync(date(2026, 10, 3)))
    assert git("--git-dir", str(remote), "rev-parse", "refs/heads/main") == git(
        "rev-parse", "HEAD", cwd=repo
    )
