# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

Pulls your X/Twitter bookmarks (including long-form **Twitter Articles**) into a
local corpus of Markdown + JSON for re-reading and LLM analysis, then
auto-categorizes them with Claude Haiku 4.5. Uses the official X API on the
pay-as-you-go tier (~$0.001/bookmark; 800-bookmark API ceiling). Full setup,
auth flow, and launchd scheduling are in [`README.md`](README.md).

## Setup & commands

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env          # then fill X_CLIENT_ID / X_CLIENT_SECRET
twitter-analysis authorize    # OAuth; writes X_REFRESH_TOKEN + X_USER_ID to .env
```

CLI (entry point `twitter_analysis.main:cli`):

- `twitter-analysis sync` — fetch new bookmarks, render, then auto-categorize.
- `twitter-analysis sync --no-categorize` — fetch/render only.
- `twitter-analysis categorize` — classify unlabeled bookmarks (idempotent).

## Architecture

- `src/twitter_analysis/auth.py` — OAuth2 + refresh-token rotation (writes the new token back to `.env` before anything else).
- `fetch.py` — X API bookmark pull. `render.py` — JSON → Markdown (handles the under-documented `article` shape, falls back to raw dump).
- `categorize.py` — 10-category taxonomy (A–J) classification via Haiku 4.5; taxonomy derived from `analysis/bookmarks-report.md`.
- `state.py` — persists highest bookmark ID seen to `state.json` for incremental sync.
- `main.py` — CLI wiring. `scripts/authorize.py` — standalone auth helper.

## Output layout (`bookmarks/`, gitignored)

- `<tweet_id>.json` — full raw record (source of truth)
- `<tweet_id>.md` — rendered for reading / LLM use
- `_categories.json` — `tweet_id → {category, confidence, reasoning}`

## Working conventions & gotchas

- **Secrets live in `.env`** (`X_CLIENT_*`, `X_REFRESH_TOKEN`, `ANTHROPIC_API_KEY`)
  — already gitignored. Never commit it or print token values. The JSON sidecar
  in `bookmarks/` always preserves the full record, so re-rendering is safe.
- `ANTHROPIC_API_KEY` is required only for categorization; if missing, sync still
  succeeds and categorize is skipped with a warning.
- **Refresh-token rotation**: every token exchange issues a new refresh token —
  `auth.py` must persist it back to `.env` before making API calls.
- **800-bookmark cap** is X-side; older bookmarks are unreachable.
- `bookmarks/`, `.venv/`, and `state.json` are gitignored — local data, not source.
