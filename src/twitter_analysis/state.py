"""Persist the highest bookmark ID seen across runs for incremental sync."""

from __future__ import annotations

import json
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parents[2] / "state.json"


def load_last_seen_id() -> str | None:
    if not STATE_PATH.exists():
        return None
    try:
        return json.loads(STATE_PATH.read_text()).get("last_seen_id")
    except (json.JSONDecodeError, OSError):
        return None


def save_last_seen_id(tweet_id: str) -> None:
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"last_seen_id": tweet_id}, indent=2))
    tmp.replace(STATE_PATH)
