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
- `twitter-analysis fetch-authors @a @b` — fetch authored tweets (RTs excluded,
  replies kept) per handle into `authors/<handle>/`; incremental, `--full`/`--max N`.
  Add `--analyze` to chain straight into analyze-authors (the full pull→skill-briefs flow).
- `twitter-analysis analyze-authors @a @b` — stitch self-reply threads, extract
  recurring frameworks via Claude, then write one skill-creator brief per framework
  to `authors/<handle>/skill-briefs/` (`--stitch-only` skips the LLM step).

## Architecture

- `src/twitter_analysis/auth.py` — OAuth2 + refresh-token rotation (writes the new token back to `.env` before anything else).
- `fetch.py` — X API pull: `fetch_bookmarks`, plus `fetch_user_tweets`/`resolve_usernames` for author timelines. `render.py` — JSON → Markdown (handles the under-documented `article` shape, falls back to raw dump).
- `categorize.py` — 10-category taxonomy (A–J) classification via Haiku 4.5; taxonomy derived from `analysis/bookmarks-report.md`.
- `threads.py` — deterministic (no-LLM) stitching of an author's self-reply chains into threads. `analyze.py` — extracts recurring frameworks per author via Claude (Sonnet 4.6) → `_frameworks.json` + `_analysis.md`, then deterministically writes per-framework skill-creator briefs (core idea + how-to-apply + the real evidence tweets pulled from the JSON) to `skill-briefs/`. Choosing which briefs become skills, and the eval loop, stay human/skill-creator's job.
- `state.py` — persists the highest bookmark ID (`last_seen_id`) and per-author cursors (`authors.{user_id}`) to `state.json` for incremental sync.
- `main.py` — CLI wiring. `scripts/authorize.py` — standalone auth helper.

## Output layout (`bookmarks/` and `authors/`, both gitignored)

- `bookmarks/<tweet_id>.json` — full raw record (source of truth)
- `bookmarks/<tweet_id>.md` — rendered for reading / LLM use
- `bookmarks/_categories.json` — `tweet_id → {category, confidence, reasoning}`
- `authors/<handle>/<tweet_id>.{json,md}` — that author's tweets (same record shape)
- `authors/<handle>/threads/<root_id>.md` — stitched multi-tweet threads
- `authors/<handle>/_frameworks.json` + `_analysis.md` — extracted frameworks
- `authors/<handle>/skill-briefs/<slug>.md` — per-framework skill-creator briefs

## Working conventions & gotchas

- **Secrets live in `.env`** (`X_CLIENT_*`, `X_REFRESH_TOKEN`, `ANTHROPIC_API_KEY`)
  — already gitignored. Never commit it or print token values. The JSON sidecar
  in `bookmarks/` always preserves the full record, so re-rendering is safe.
- `ANTHROPIC_API_KEY` is required only for categorization and `analyze-authors`;
  if missing, fetch still succeeds and the LLM step is skipped with a warning.
- **Refresh-token rotation**: every token exchange issues a new refresh token —
  `auth.py` must persist it back to `.env` before making API calls.
- **800-bookmark cap** is X-side; older bookmarks are unreachable. Author
  timelines hit a similar depth wall on this tier — observed **~775–800 most-recent
  tweets per user** (not the old v1.1 3,200 archive limit). For an active account
  that's only ~2–3 months back.
- `bookmarks/`, `authors/`, `.venv/`, and `state.json` are gitignored — local data, not source.
