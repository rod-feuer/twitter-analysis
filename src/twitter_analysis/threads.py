"""Stitch an author's individual tweets into whole threads.

A "thread" is a chain of the author replying to their own earlier tweet — that's
where a framework usually unfolds, so we group those tweets before any analysis.
This is a pure local transform over the saved JSON (no API): we link each tweet
to its `replied_to` parent *only when that parent is also in our set*, which —
because the corpus is author-only — means a self-reply. Replies to other people
(whose parent isn't in the set) stay as singletons.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

AUTHORS_DIR = Path(__file__).resolve().parents[2] / "authors"


def _replied_to_parent(record: dict[str, Any]) -> str | None:
    for ref in record.get("referenced_tweets") or []:
        if ref.get("type") == "replied_to":
            return ref.get("id")
    return None


def stitch_author(handle: str) -> list[list[dict[str, Any]]]:
    """Group an author's tweets into threads, each ordered oldest→newest.

    Returns a list of threads (a thread is a chronological list of records).
    Multi-tweet threads come first, longest first; singletons follow. A tweet
    whose `replied_to` parent isn't in the corpus starts its own thread.
    """
    author_dir = AUTHORS_DIR / handle.lstrip("@").lower()
    records: dict[str, dict[str, Any]] = {}
    for path in sorted(author_dir.glob("*.json")):
        if path.stem.startswith("_"):  # skip sidecars like _frameworks.json
            continue
        try:
            rec = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        records[rec["id"]] = rec

    # Union the corpus into connected components via in-set replied_to edges.
    parent_of: dict[str, str] = {}

    def find(x: str) -> str:
        root = x
        while parent_of.get(root, root) != root:
            root = parent_of.get(root, root)
        while parent_of.get(x, x) != root:  # path compression
            parent_of[x], x = root, parent_of.get(x, x)
        return root

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent_of[ra] = rb

    for tid in records:
        parent_of.setdefault(tid, tid)
    for tid, rec in records.items():
        p = _replied_to_parent(rec)
        if p and p in records:
            union(tid, p)

    groups: dict[str, list[dict[str, Any]]] = {}
    for tid, rec in records.items():
        groups.setdefault(find(tid), []).append(rec)

    threads = [sorted(g, key=lambda r: r.get("created_at", "")) for g in groups.values()]
    threads.sort(key=lambda t: (len(t) == 1, -len(t), t[0].get("created_at", "")))
    return threads


def write_threads(handle: str) -> tuple[int, int]:
    """Write multi-tweet threads to authors/<handle>/threads/<root_id>.md.

    Singletons are skipped — they already exist as individual files. Returns
    (multi_tweet_thread_count, total_threads_including_singletons).
    """
    handle = handle.lstrip("@").lower()
    threads = stitch_author(handle)
    out_dir = AUTHORS_DIR / handle / "threads"
    multi = [t for t in threads if len(t) > 1]
    if multi:
        out_dir.mkdir(parents=True, exist_ok=True)
    for thread in multi:
        root = thread[0]
        author = (root.get("_author") or {}).get("username", handle)
        parts = [
            "---",
            f"thread_root: {root['id']}",
            f"author: @{author}",
            f"tweet_count: {len(thread)}",
            f"created_at: {root.get('created_at', '')}",
            f"url: https://x.com/{author}/status/{root['id']}",
            "---",
            "",
            f"# Thread by @{author} ({len(thread)} tweets)",
        ]
        for i, rec in enumerate(thread, 1):
            text = (rec.get("note_tweet") or {}).get("text") or rec.get("text") or ""
            parts += ["", f"## {i}/{len(thread)}", "", text.strip()]
        (out_dir / f"{root['id']}.md").write_text("\n".join(parts) + "\n")
    return len(multi), len(threads)
