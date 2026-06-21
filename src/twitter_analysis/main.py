"""CLI entry point: `twitter-analysis sync | authorize`."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from rich.console import Console

from .analyze import analyze_author
from .auth import get_access_token
from .categorize import run as categorize_run
from .fetch import fetch_bookmarks, fetch_user_tweets, resolve_usernames
from .render import write_bookmark
from .threads import write_threads
from .state import (
    load_author_cursor,
    load_last_seen_id,
    save_author_cursor,
    save_last_seen_id,
)

console = Console()

AUTHORS_DIR = Path(__file__).resolve().parents[2] / "authors"


def _cmd_authorize() -> int:
    script = Path(__file__).resolve().parents[2] / "scripts" / "authorize.py"
    return subprocess.call([sys.executable, str(script)])


def _cmd_sync(full: bool, categorize: bool) -> int:
    access_token, user_id = get_access_token()
    since_id = None if full else load_last_seen_id()

    console.print(
        f"[bold]Syncing bookmarks[/bold] for user {user_id} "
        f"({'full refetch' if full else f'since {since_id}' if since_id else 'first run'})"
    )

    count = 0
    newest_id: str | None = None
    for record in fetch_bookmarks(access_token, user_id, since_id=since_id):
        path = write_bookmark(record)
        if newest_id is None:
            newest_id = record["id"]
        count += 1
        console.print(f"  [green]✓[/green] {record['id']} → {path.name}")

    if newest_id:
        save_last_seen_id(newest_id)

    cost = count * 0.001
    console.print(
        f"\n[bold]Done.[/bold] Fetched {count} new bookmark(s). "
        f"Estimated cost: ${cost:.3f}"
    )

    if categorize:
        categorize_run()
    return 0


def _cmd_fetch_authors(
    handles: list[str], full: bool, max_tweets: int | None, analyze: bool = False
) -> int:
    access_token, _ = get_access_token()

    resolved = resolve_usernames(access_token, handles)
    missing = [h for h in handles if h.lstrip("@").lower() not in resolved]
    if missing:
        console.print(f"[yellow]Skipping unresolved handle(s):[/yellow] {', '.join(missing)}")
    if not resolved:
        console.print("[red]No handles resolved — nothing to fetch.[/red]")
        return 1

    grand_total = 0
    for handle, user in resolved.items():
        user_id = user["id"]
        since_id = None if full else load_author_cursor(user_id)
        out_dir = AUTHORS_DIR / handle
        console.print(
            f"\n[bold]@{handle}[/bold] ({user_id}) "
            f"({'full' if full else f'since {since_id}' if since_id else 'first run'})"
        )

        count = 0
        newest_id: str | None = None
        for record in fetch_user_tweets(
            access_token, user_id, since_id=since_id, max_tweets=max_tweets
        ):
            path = write_bookmark(record, output_dir=out_dir)
            if newest_id is None:
                newest_id = record["id"]
            count += 1
            console.print(f"  [green]✓[/green] {record['id']} → {handle}/{path.name}")

        if newest_id:
            save_author_cursor(user_id, newest_id)
        grand_total += count
        console.print(f"  [dim]{count} new tweet(s)[/dim]")

    console.print(
        f"\n[bold]Done.[/bold] Fetched {grand_total} tweet(s) across "
        f"{len(resolved)} author(s). Estimated cost: ${grand_total * 0.001:.3f}"
    )

    if analyze:
        console.print("\n[bold]Analyzing[/bold] fetched author(s)...")
        return _cmd_analyze_authors(handles=list(resolved.keys()), stitch_only=False)
    return 0


def _cmd_analyze_authors(handles: list[str], stitch_only: bool) -> int:
    for handle in handles:
        multi, total = write_threads(handle)
        console.print(
            f"[bold]@{handle.lstrip('@').lower()}[/bold]: stitched "
            f"{multi} multi-tweet thread(s) of {total} group(s)"
        )
        if not stitch_only:
            analyze_author(handle)
    return 0


def cli() -> int:
    parser = argparse.ArgumentParser(prog="twitter-analysis")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("authorize", help="Run one-time OAuth 2.0 PKCE flow")

    sync = sub.add_parser("sync", help="Fetch new bookmarks and render to disk")
    sync.add_argument("--full", action="store_true", help="Ignore state.json and refetch all")
    sync.add_argument(
        "--no-categorize",
        action="store_true",
        help="Skip auto-categorization (otherwise runs after fetch if ANTHROPIC_API_KEY is set)",
    )

    sub.add_parser(
        "categorize",
        help="Classify bookmarks against the 10-category taxonomy; idempotent",
    )

    authors = sub.add_parser(
        "fetch-authors",
        help="Fetch authored tweets (RTs excluded, replies kept) for given handles",
    )
    authors.add_argument("handles", nargs="+", help="X handles, e.g. @hnshah @pmarca")
    authors.add_argument(
        "--full", action="store_true", help="Ignore saved cursors and refetch all"
    )
    authors.add_argument(
        "--max", type=int, default=None, dest="max_tweets",
        help="Cap tweets pulled per author (default: up to the X depth wall, ~800 on this tier)",
    )
    authors.add_argument(
        "--analyze", action="store_true",
        help="After fetching, run analyze-authors (stitch threads, extract frameworks, write skill briefs)",
    )

    analyze = sub.add_parser(
        "analyze-authors",
        help="Stitch threads and extract recurring frameworks for given handles",
    )
    analyze.add_argument("handles", nargs="+", help="X handles already fetched")
    analyze.add_argument(
        "--stitch-only", action="store_true",
        help="Only stitch threads to disk; skip the Claude framework extraction",
    )

    args = parser.parse_args()
    if args.cmd == "authorize":
        return _cmd_authorize()
    if args.cmd == "sync":
        try:
            return _cmd_sync(full=args.full, categorize=not args.no_categorize)
        except Exception as exc:  # noqa: BLE001 (surface clearly to the user)
            console.print(f"[red]Error:[/red] {exc}")
            return 1
    if args.cmd == "categorize":
        try:
            categorize_run()
            return 0
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]Error:[/red] {exc}")
            return 1
    if args.cmd == "fetch-authors":
        try:
            return _cmd_fetch_authors(
                handles=args.handles, full=args.full, max_tweets=args.max_tweets,
                analyze=args.analyze,
            )
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]Error:[/red] {exc}")
            return 1
    if args.cmd == "analyze-authors":
        try:
            return _cmd_analyze_authors(handles=args.handles, stitch_only=args.stitch_only)
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]Error:[/red] {exc}")
            return 1
    return 1


if __name__ == "__main__":
    sys.exit(cli())
