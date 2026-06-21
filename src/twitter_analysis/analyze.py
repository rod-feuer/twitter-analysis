"""Extract recurring frameworks from an author's corpus using Claude.

Stitches the author's tweets into threads (threads.py), feeds the highest-signal
content — multi-tweet threads and standalone original posts, NOT one-line replies
to other people — to Claude, and asks it to surface the recurring mental models
and frameworks that author returns to. The output (authors/<handle>/_frameworks.json
plus a readable _analysis.md) is designed to be the input to the skill-creator
skill: one framework → one candidate thinking-skill.

Cost scales with corpus size. To bound it we cap input at MAX_INPUT_CHARS and
report loudly when content is dropped — a silent cap would read as full coverage.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from rich.console import Console

from .threads import AUTHORS_DIR, stitch_author

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"

# Framework extraction is the high-value judgment step, run once per author and
# infrequently — use a stronger model than the bookmark classifier (Haiku).
MODEL = "claude-sonnet-4-6"
MAX_INPUT_CHARS = 400_000  # ~100k tokens; guards cost on full ~3,200-tweet pulls

console = Console()

SYSTEM_PROMPT = (
    "You analyze the public writing of one person on X/Twitter to extract the "
    "recurring FRAMEWORKS and mental models they return to — the reusable ways of "
    "thinking that could be turned into a skill, not their stylistic voice.\n\n"
    "You will receive that person's threads and standalone posts. Identify the "
    "distinct frameworks they apply repeatedly. For each, capture what it is, how "
    "to apply it step by step, and the tweet IDs that evidence it.\n\n"
    "## Rules\n"
    "- A framework must recur or be developed in depth — ignore one-off quips.\n"
    "- 'how_to_apply' must be concrete enough that someone could follow it without "
    "the original author present.\n"
    "- 'evidence_tweet_ids' must be IDs that actually appear in the input.\n"
    "- 'confidence' is high if the framework is explicit and repeated, medium if "
    "inferred from a few posts, low if it is a stretch.\n"
    "- Prefer 4-10 strong frameworks over an exhaustive shallow list."
)

SCHEMA = {
    "type": "object",
    "properties": {
        "frameworks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "how_to_apply": {"type": "string"},
                    "evidence_tweet_ids": {"type": "array", "items": {"type": "string"}},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                },
                "required": [
                    "name",
                    "description",
                    "how_to_apply",
                    "evidence_tweet_ids",
                    "confidence",
                ],
                "additionalProperties": False,
            },
        },
        "overview": {"type": "string"},
    },
    "required": ["frameworks", "overview"],
    "additionalProperties": False,
}


def _is_reply_to_other(thread: list[dict[str, Any]]) -> bool:
    """A singleton that replies to someone outside the corpus — low signal."""
    if len(thread) > 1:
        return False
    rec = thread[0]
    return any(r.get("type") == "replied_to" for r in rec.get("referenced_tweets") or [])


def _build_input(handle: str) -> tuple[str, int, int]:
    """Return (corpus_text, included_unit_count, dropped_unit_count).

    A "unit" is a thread or standalone post. Threads come first (highest signal);
    we stop adding once MAX_INPUT_CHARS is reached and count the rest as dropped.
    """
    threads = [t for t in stitch_author(handle) if not _is_reply_to_other(t)]
    blocks: list[str] = []
    used = 0
    included = 0
    for thread in threads:
        lines: list[str] = []
        for rec in thread:
            text = (rec.get("note_tweet") or {}).get("text") or rec.get("text") or ""
            lines.append(f"[{rec['id']}] {text.strip()}")
        block = ("THREAD:\n" if len(thread) > 1 else "POST:\n") + "\n".join(lines)
        if used + len(block) > MAX_INPUT_CHARS and blocks:
            break
        blocks.append(block)
        used += len(block)
        included += 1
    return "\n\n".join(blocks), included, len(threads) - included


def _analysis_markdown(handle: str, result: dict[str, Any]) -> str:
    parts = [f"# Frameworks: @{handle}", "", result.get("overview", ""), ""]
    for fw in result.get("frameworks", []):
        ids = ", ".join(fw.get("evidence_tweet_ids", []))
        parts += [
            f"## {fw['name']} ({fw.get('confidence', '?')})",
            "",
            fw.get("description", ""),
            "",
            f"**How to apply:** {fw.get('how_to_apply', '')}",
            "",
            f"_Evidence: {ids}_",
            "",
        ]
    return "\n".join(parts)


def analyze_author(handle: str) -> dict[str, Any] | None:
    """Extract frameworks for one handle. Returns the result, or None if skipped."""
    try:
        import anthropic
    except ImportError:
        console.print(
            "[yellow]Skipping analysis:[/yellow] anthropic package not installed. "
            "Run `pip install -e .`."
        )
        return None
    load_dotenv(ENV_PATH, override=False)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print(
            "[yellow]Skipping analysis:[/yellow] ANTHROPIC_API_KEY not set in env or .env."
        )
        return None

    handle = handle.lstrip("@").lower()
    corpus, included, dropped = _build_input(handle)
    if not corpus.strip():
        console.print(f"[yellow]@{handle}:[/yellow] no substantive content to analyze.")
        return None
    if dropped:
        console.print(
            f"[yellow]@{handle}: input capped[/yellow] — analyzing {included} unit(s), "
            f"dropped {dropped} (raise MAX_INPUT_CHARS to include them)."
        )

    console.print(f"[bold]Analyzing[/bold] @{handle} ({included} thread(s)/post(s))...")
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": corpus}],
    )
    result = json.loads(next(b.text for b in response.content if b.type == "text"))

    out_dir = AUTHORS_DIR / handle
    (out_dir / "_frameworks.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    (out_dir / "_analysis.md").write_text(_analysis_markdown(handle, result))
    console.print(
        f"  [green]✓[/green] {len(result.get('frameworks', []))} framework(s) "
        f"→ {handle}/_analysis.md"
    )
    return result
