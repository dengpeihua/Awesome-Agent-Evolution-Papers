# Deployment Guide

This repository is both the paper archive and an AstrBot plugin. The local
deployment uses Python 3.12 in an isolated `uv` environment; Docker is optional.

## 1. Install and start AstrBot

```powershell
git clone https://github.com/AstrBotDevs/AstrBot.git C:\Users\you\Projects\AstrBot
cd C:\Users\you\Projects\AstrBot
py -m pip install --user uv
py -m uv sync --no-dev --python 3.12
\.venv\Scripts\python.exe main.py
```

Open `http://localhost:6185`, sign in with the one-time password printed in the
startup log, and change the dashboard password immediately.

## 2. Install this repository as the plugin

Run from this repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_astrbot_plugin.ps1 `
  -AstrBotPath C:\Users\you\Projects\AstrBot
```

Restart AstrBot or reload **Agent Paper Digest** in the WebUI plugin page.

## 3. Create the enterprise WeChat webhook

In an enterprise WeChat internal group, open **Group settings → Message Push →
Create bot** and copy its URL. It starts with
`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=`.

In AstrBot WebUI, open **Plugins → Agent Paper Digest → Configuration** and set:

- `wecom_webhook_url`: the group bot URL (never commit it to Git)
- `schedule_hour` / `schedule_minute`: daily local push time
- `timezone`: `Asia/Shanghai`
- `archive_dir`: the absolute path of this repository
- `run_on_startup`: `true`, so a late restart immediately performs a catch-up run

The plugin stores its successful cursor in `data/digest_state.json`. Each run starts
at the last successful notification-and-Git publication time and follows arXiv
pagination until it crosses that boundary. If delivery fails, the undelivered paper
IDs remain pending and are retried after the next startup instead of being lost.

The push-only webhook needs no public IP, callback URL, or enterprise application
credentials. Configure AstrBot's full WeCom adapter separately only if you also
want interactive conversations.

## 4. Publish to GitHub

Create an empty GitHub repository named `Awesome-Agent-Evolution-Papers`, then:

```powershell
git remote add origin https://github.com/YOUR_NAME/Awesome-Agent-Evolution-Papers.git
git push -u origin main
```

Authenticate with Git Credential Manager or SSH. Then configure:

- `repository_url`: the public GitHub URL
- `git_remote`: `origin`
- `git_branch`: `main`
- `git_auto_push`: `true`

The publication state machine can create two small commits in one run: the first
publishes papers plus the pending-delivery ledger; after notification succeeds, the
second advances and publishes the success cursor. This is intentional and makes
crash recovery auditable.

No token is stored in this repository; Git uses the operating system credential
manager or your SSH agent.

## 5. Metadata enrichment and priority markers

Keep `semantic_scholar_enrichment` enabled to batch-fill missing venue and author
profile metadata. Most Semantic Scholar endpoints work without a key but may be
throttled. An optional key can be placed in `semantic_scholar_api_key` in AstrBot's
local plugin configuration; never add it to this repository.

Public inclusion and priority markers are conservative:

- every public paper must be in one of the three research tracks and independently
  qualify through CCF-A (AI), ECCV/EMNLP, big-tech authorship, or at least 10
  citations;
- a team industry marker requires paper-specific evidence; Semantic Scholar author
  profiles qualify only when the first author's profile names a big-tech company;
- a venue marker requires an arXiv acceptance comment, journal reference,
  DOI-backed publisher record, or publication-venue metadata;
- workshop, Findings, demo, short-paper, submitted, and under-review text is not
  promoted by venue status, and `arXiv.org` is never treated as a venue;
- GitHub stars are displayed for context but do not qualify a paper by themselves.

## 6. Verify before unattended operation

Copy `config.example.json` to ignored `config.json`, fill non-secret values, and run:

```powershell
py -m uv sync --dev --python 3.12
py -m uv run python scripts/run_once.py --no-notify --no-push
```

When either flag suppresses a normally configured delivery channel, the run keeps
the discovered IDs pending and deliberately does not advance the success cursor.
The next normal run will still deliver them.

After the dry run, use `/paper_digest_status` and `/paper_digest` in a connected
AstrBot chat, or reload the plugin with `run_on_startup` enabled for one run.

## Operations

- Dashboard: `http://localhost:6185`
- Manual command: `/paper_digest`
- Safe status command: `/paper_digest_status`
- Daily pages: `papers/YYYY/MM/YYYY-MM-DD.md`
- Machine-readable dataset: `data/papers.json`
- AstrBot logs: `C:\Users\you\Projects\AstrBot\data\logs`
