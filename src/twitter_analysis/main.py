"""CLI entry point: `twitter-analysis sync | authorize`."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from rich.console import Console

from .auth import get_access_token
from .categorize import run as categorize_run
from .fetch import fetch_bookmarks
from .render import write_bookmark
from .state import load_last_seen_id, save_last_seen_id

console = Console()


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
    return 1


if __name__ == "__main__":
    sys.exit(cli())
