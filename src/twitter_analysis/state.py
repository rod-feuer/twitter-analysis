"""Persist incremental-sync cursors across runs.

Two independent cursors share state.json:
  - "last_seen_id": highest bookmark ID seen (bookmarks sync)
  - "authors": {user_id: highest tweet ID seen} (per-author timeline sync)
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
