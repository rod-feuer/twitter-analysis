"""Render fetched bookmarks to per-tweet Markdown + JSON files.

The JSON sidecar is always the full raw record — it's the source of truth so
we can re-render later if the renderer improves. The Markdown is a best-effort
human-readable form with Article and note_tweet content prioritized over the
truncated `text` field.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "bookmarks"


def _author_line(record: dict[str, Any]) -> str:
    author = record.get("_author") or {}
    handle = author.get("username", "unknown")
    name = author.get("name", "")
    return f'"@{handle} ({name})"' if name else f'"@{handle}"'


def _url(record: dict[str, Any]) -> str:
    author = record.get("_author") or {}
    handle = author.get("username", "i")
    return f"https://x.com/{handle}/status/{record['id']}"


def _expand_urls(text: str, entities: dict[str, Any] | None) -> str:
    """Replace t.co shorturls with expanded URLs from the entities block."""
    if not entities:
        return text
    for u in entities.get("urls") or []:
        short = u.get("url")
        full = u.get("expanded_url")
        if short and full:
            text = text.replace(short, full)
    return text


def _render_article(article: dict[str, Any]) -> tuple[str, str]:
    """Return (title, body_markdown) for an Article-typed tweet.

    The article schema is sparsely documented and may evolve, so we try a few
    common shapes and fall back to dumping the raw structure. The JSON sidecar
    preserves the original so we can re-render if needed.
    """
    title = article.get("title") or "Untitled Article"

    content = article.get("content")
    if isinstance(content, str) and content.strip():
        return title, content

    if isinstance(content, dict):
        for key in ("markdown", "text", "body", "plain_text"):
            val = content.get(key)
            if isinstance(val, str) and val.strip():
                return title, val
        blocks = content.get("blocks") or content.get("entity_annotations")
        if isinstance(blocks, list):
            parts: list[str] = []
            for block in blocks:
                if isinstance(block, dict):
                    text = block.get("text") or block.get("plain_text")
                    if text:
                        parts.append(text)
            if parts:
                return title, "\n\n".join(parts)

    raw = json.dumps(article, indent=2, ensure_ascii=False)
    return title, f"_Article rendering fell back to raw payload._\n\n```json\n{raw}\n```"


def _body(record: dict[str, Any]) -> tuple[str, str, str]:
    """Pick the richest available body for this tweet.

    Returns (kind, title, body_markdown).
      kind: "article" | "note_tweet" | "tweet"
      title: heading text for the .md file
      body: expanded markdown body
    """
    article = record.get("article")
    if isinstance(article, dict) and article:
        title, body = _render_article(article)
        return "article", title, body

    note = record.get("note_tweet")
    if isinstance(note, dict) and note.get("text"):
        body = _expand_urls(note["text"], note.get("entities"))
        title = body.strip().split("\n", 1)[0][:80]
        return "note_tweet", title, body

    text = record.get("text") or ""
    body = _expand_urls(text, record.get("entities"))
    title = body.strip().split("\n", 1)[0][:80] or f"Bookmark {record['id']}"
    return "tweet", title, body


def _media_section(record: dict[str, Any]) -> str:
    media = record.get("_media") or []
    if not media:
        return ""
    lines = ["## Media"]
    for m in media:
        url = m.get("url") or m.get("preview_image_url") or ""
        alt = m.get("alt_text") or m.get("type", "media")
        if url:
            lines.append(f"- ![{alt}]({url})")
        else:
            lines.append(f"- _{alt} (no URL)_")
    return "\n".join(lines)


def _links_section(record: dict[str, Any]) -> str:
    sources = []
    entities = record.get("entities") or {}
    note = record.get("note_tweet") or {}
    note_entities = note.get("entities") or {}
    seen: set[str] = set()
    out: list[str] = []
    for ent in (entities, note_entities):
        for u in ent.get("urls") or []:
            full = u.get("expanded_url")
            if full and full not in seen and "x.com/" not in full and "twitter.com/" not in full:
                seen.add(full)
                out.append(f"- {full}")
                sources.append(full)
    if not out:
        return ""
    return "## Links\n" + "\n".join(out)


def _referenced_section(record: dict[str, Any]) -> str:
    refs = record.get("_referenced") or []
    if not refs:
        return ""
    lines = ["## Referenced"]
    for ref in refs:
        kind = ref.get("type", "ref")
        rt = ref.get("tweet") or {}
        text = rt.get("text", "(not expanded)")
        lines.append(f"- **{kind}**: {text[:200]}")
    return "\n".join(lines)


def write_bookmark(record: dict[str, Any], output_dir: Path = OUTPUT_DIR) -> Path:
    """Write {id}.json and {id}.md, return the path to the markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    tid = record["id"]

    json_path = output_dir / f"{tid}.json"
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False))

    kind, title, body = _body(record)
    parts = [
        "---",
        f"id: {tid}",
        f"author: {_author_line(record)}",
        f"created_at: {record.get('created_at', '')}",
        f"url: {_url(record)}",
        f"type: {kind}",
        "---",
        "",
        f"# {title}",
        "",
        body,
    ]
    for section in (_media_section(record), _links_section(record), _referenced_section(record)):
        if section:
            parts.extend(["", section])
    md_path = output_dir / f"{tid}.md"
    md_path.write_text("\n".join(parts) + "\n")
    return md_path
