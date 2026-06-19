"""Categorize bookmarks against a fixed 10-category taxonomy using Claude.

Reads bookmarks/*.json, classifies each bookmark not already in the index against
the taxonomy derived from the May 2026 corpus analysis (see
analysis/bookmarks-report.md), and writes labels to bookmarks/_categories.json.
Idempotent: re-running skips bookmarks already in the index. Persists after each
successful classification so a crash mid-batch loses at most one in-flight item.

Cost: ~$0.0008/bookmark on Claude Haiku 4.5. The 99-bookmark backfill is ~$0.08.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from rich.console import Console

BOOKMARKS_DIR = Path(__file__).resolve().parents[2] / "bookmarks"
INDEX_PATH = BOOKMARKS_DIR / "_categories.json"

MODEL = "claude-haiku-4-5"

CATEGORIES: dict[str, str] = {
    "A": "Claude Code Configuration & Productivity — daily-driver tips on CLAUDE.md, hooks, skills, settings, plugins, prompts.",
    "B": "Agent Orchestration & 'Solo Company' Patterns — multi-agent swarms, software factories, agent fleets, folder-as-company memes.",
    "C": "Agent Engineering: Harnesses, Tools, Evals — architectural patterns, eval design, harness theory, sub-agent design, self-improvement loops.",
    "D": "AI Memory & Knowledge Systems — personal/company brain, second brain, long-term memory, knowledge bases.",
    "E": "AI-Native Workflows by Function — design, PM, research, GTM, enterprise engineering practices powered by AI.",
    "F": "Curated AI Resources & Tutorials — lists of skills/repos, courses, cheatsheets, individual tool callouts, learning material.",
    "G": "AI Industry & Strategic Commentary — macro takes on convergence, moats, enterprise adoption, predictions.",
    "H": "Investing & Economics — non-AI: macro analysis, trading, economic theory.",
    "I": "Thinking & Personal Development — non-AI: philosophy, learning, leadership, mental models.",
    "J": "Humor & Off-Topic — non-AI: jokes, memes, one-off tweets without substantive content.",
}

CONFIDENCE_LEVELS = ["high", "medium", "low"]

SYSTEM_PROMPT = (
    "You are a classifier for X/Twitter bookmarks in a personal corpus.\n\n"
    "Your job: read one bookmark (title, author, content snippet) and assign exactly "
    "one of the following category codes (A-J). The taxonomy was derived from a corpus "
    "analysis in May 2026 and is intentionally fixed.\n\n"
    "## Categories\n\n"
    + "\n".join(f"- **{code}**: {desc}" for code, desc in CATEGORIES.items())
    + "\n\n## Rules\n\n"
    "- Assign exactly one category code.\n"
    "- If a bookmark spans two AI topics, pick the more specific one (e.g. a specific "
    "Claude Code hook tip is A, not C, even if it touches harness design).\n"
    "- Categories H-J are explicitly non-AI; do not stretch them to fit AI content.\n"
    "- 'confidence' is high if the category is obvious, medium if the bookmark spans "
    "multiple categories or is short on signal, low if you are essentially guessing.\n"
    "- 'reasoning' is one short sentence explaining the choice."
)

SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": list(CATEGORIES.keys())},
        "confidence": {"type": "string", "enum": CONFIDENCE_LEVELS},
        "reasoning": {"type": "string"},
    },
    "required": ["category", "confidence", "reasoning"],
    "additionalProperties": False,
}

console = Console()


def _load_index() -> dict[str, dict[str, Any]]:
    if not INDEX_PATH.exists():
        return {}
    try:
        return json.loads(INDEX_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _save_index(index: dict[str, dict[str, Any]]) -> None:
    tmp = INDEX_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(index, indent=2, sort_keys=True))
    tmp.replace(INDEX_PATH)


def _bookmark_input(record: dict[str, Any]) -> str:
    author = record.get("_author") or {}
    author_str = f"@{author.get('username', '?')} ({author.get('name', '?')})"
    ttype = record.get("type", "tweet")

    article = record.get("article") or {}
    title = (article.get("title") or "").strip()
    body = article.get("plain_text") or article.get("preview_text") or ""
    text = record.get("text") or ""
    snippet = (body or text)[:1500]

    parts = [f"Author: {author_str}", f"Type: {ttype}"]
    if title:
        parts.append(f"Title: {title}")
    parts.append(f"Content: {snippet}")
    return "\n".join(parts)


def _classify_one(client: Any, bookmark_input: str) -> dict[str, Any]:
    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": bookmark_input}],
    )
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


def run() -> int:
    """Categorize any bookmarks not yet in the index. Returns count newly classified."""
    try:
        import anthropic
    except ImportError:
        console.print(
            "[yellow]Skipping categorization:[/yellow] anthropic package not installed. "
            "Run `pip install -e .` to pick up the new dependency."
        )
        return 0

    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print(
            "[yellow]Skipping categorization:[/yellow] ANTHROPIC_API_KEY not set in env."
        )
        return 0

    index = _load_index()
    all_paths = sorted(BOOKMARKS_DIR.glob("*.json"))
    new_paths = [p for p in all_paths if p.stem not in index and not p.stem.startswith("_")]

    if not new_paths:
        console.print("[dim]Categorize: no new bookmarks.[/dim]")
        return 0

    console.print(f"[bold]Categorizing[/bold] {len(new_paths)} new bookmark(s)...")
    client = anthropic.Anthropic()
    classified = 0

    for path in new_paths:
        try:
            record = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"  [red]✗[/red] {path.stem}: failed to read ({exc})")
            continue

        try:
            result = _classify_one(client, _bookmark_input(record))
        except Exception as exc:  # noqa: BLE001
            console.print(f"  [red]✗[/red] {path.stem}: classify error: {exc}")
            raise

        index[path.stem] = result
        _save_index(index)
        classified += 1
        console.print(
            f"  [green]✓[/green] {path.stem} → {result['category']} "
            f"({result['confidence']})"
        )

    by_cat: dict[str, int] = {}
    for entry in index.values():
        c = entry.get("category", "?")
        by_cat[c] = by_cat.get(c, 0) + 1
    dist = " ".join(f"{k}={by_cat.get(k, 0)}" for k in CATEGORIES)
    console.print(f"\n[bold]Done.[/bold] Categorized {classified} new. Totals: {dist}")
    return classified
