"""Persist incremental-sync cursors across runs.

state.json holds:
  - "last_seen_id": highest bookmark ID seen (bookmarks sync)
  - "authors": {user_id: highest tweet ID seen} (per-author timeline sync)
  - "author_progress": {user_id: {token, newest_id}} — an in-flight pagination
    checkpoint so a fetch interrupted mid-pull (transient error, Ctrl-C) resumes
    from where it stopped instead of re-fetching (and re-paying for) the whole
    timeline. Cleared once a pull completes and its cursor is committed.
"""

from __future__ import annotations

import json
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parents[2] / "state.json"


def _read() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _write(state: dict) -> None:
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(STATE_PATH)


def load_last_seen_id() -> str | None:
    return _read().get("last_seen_id")


def save_last_seen_id(tweet_id: str) -> None:
    state = _read()
    state["last_seen_id"] = tweet_id
    _write(state)


def load_author_cursor(user_id: str) -> str | None:
    return (_read().get("authors") or {}).get(user_id)


def save_author_cursor(user_id: str, tweet_id: str) -> None:
    state = _read()
    state.setdefault("authors", {})[user_id] = tweet_id
    _write(state)


def load_author_progress(user_id: str) -> dict | None:
    """Return the in-flight pagination checkpoint {token, newest_id}, or None."""
    return (_read().get("author_progress") or {}).get(user_id)


def save_author_progress(user_id: str, token: str, newest_id: str | None) -> None:
    state = _read()
    state.setdefault("author_progress", {})[user_id] = {
        "token": token,
        "newest_id": newest_id,
    }
    _write(state)


def clear_author_progress(user_id: str) -> None:
    state = _read()
    progress = state.get("author_progress") or {}
    if user_id in progress:
        del progress[user_id]
        _write(state)
