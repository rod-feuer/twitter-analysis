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
    clear_author_progress,
    load_author_cursor,
    load_author_progress,
    load_last_seen_id,
    save_author_cursor,
    save_author_progress,
    save_last_seen_id,
)

console = Console()

AUTHORS_DIR = Path(__file__).resolve().parents[2] / "authors"

# Rough only — X bills per request/usage in ways this doesn't model, and observed
# spend ran ~4x a naive $0.001/tweet. Treat as a ballpark; the X developer
# dashboard is the source of truth for actual cost.
COST_PER_TWEET_EST = 0.004


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

    console.print(
        f"\n[bold]Done.[/bold] Fetched {count} new bookmark(s). "
        f"Rough cost: ~${count * COST_PER_TWEET_EST:.2f} "
        f"(estimate only — see your X developer dashboard for actual spend)."
    )

    if categorize:
        categorize_run()
    return 0


def _cmd_fetch_authors(
    handles: list[str],
    full: bool,
    max_tweets: int | None,
    analyze: bool = False,
    yes: bool = False,
) -> int:
    access_token, _ = get_access_token()

    resolved = resolve_usernames(access_token, handles)
    missing = [h for h in handles if h.lstrip("@").lower() not in resolved]
    if missing:
        console.print(f"[yellow]Skipping unresolved handle(s):[/yellow] {', '.join(missing)}")
    if not resolved:
        console.print("[red]No handles resolved — nothing to fetch.[/red]")
        return 1

    # Guardrail: an uncapped pull can fetch thousands of tweets per author and cost
    # real money. Warn (and confirm if interactive) before spending.
    if max_tweets is None and not yes:
        warning = (
            f"[yellow]No --max set:[/yellow] this pulls each author's full reachable "
            f"history — up to ~3,000+ tweets each at ~${COST_PER_TWEET_EST:.3f}/tweet "
            f"(rough; check your X dashboard). {len(resolved)} author(s) queued."
        )
        if sys.stdin.isatty():
            console.print(warning)
            if input("Continue? [y/N] ").strip().lower() not in ("y", "yes"):
                console.print("Aborted.")
                return 1
        else:
            console.print(warning + " Proceeding (non-interactive; use --max or --yes).")

    grand_total = 0
    for handle, user in resolved.items():
        user_id = user["id"]
        since_id = None if full else load_author_cursor(user_id)
        progress = None if full else load_author_progress(user_id)
        resume_token = progress["token"] if progress else None
        # newest_id lives in a mutable holder so the on_progress closure sees the
        # latest value; on resume we keep the interrupted run's newest as the cursor.
        prog = {"newest_id": progress["newest_id"] if progress else None}
        out_dir = AUTHORS_DIR / handle
        mode = (
            "full" if full
            else "resuming" if progress
            else f"since {since_id}" if since_id
            else "first run"
        )
        console.print(f"\n[bold]@{handle}[/bold] ({user_id}) ({mode})")

        def _on_progress(token, _uid=user_id, _prog=prog):
            if token:
                save_author_progress(_uid, token, _prog["newest_id"])
            else:
                clear_author_progress(_uid)

        count = 0
        for record in fetch_user_tweets(
            access_token, user_id, since_id=since_id, max_tweets=max_tweets,
            resume_token=resume_token, on_progress=_on_progress,
        ):
            path = write_bookmark(record, output_dir=out_dir)
            if prog["newest_id"] is None:
                prog["newest_id"] = record["id"]
            count += 1
            console.print(f"  [green]✓[/green] {record['id']} → {handle}/{path.name}")

        if prog["newest_id"]:
            save_author_cursor(user_id, prog["newest_id"])
        clear_author_progress(user_id)  # belt-and-suspenders on clean completion
        grand_total += count
        console.print(f"  [dim]{count} new tweet(s)[/dim]")

    console.print(
        f"\n[bold]Done.[/bold] Fetched {grand_total} tweet(s) across "
        f"{len(resolved)} author(s). Rough cost: ~${grand_total * COST_PER_TWEET_EST:.2f} "
        f"(estimate only — see your X developer dashboard for actual spend)."
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
        help="Cap tweets pulled per author (default: all reachable history; varies by author, up to X's ~3,200 archive limit)",
    )
    authors.add_argument(
        "--analyze", action="store_true",
        help="After fetching, run analyze-authors (stitch threads, extract frameworks, write skill briefs)",
    )
    authors.add_argument(
        "--yes", "-y", action="store_true",
        help="Skip the uncapped-pull cost confirmation",
    )

    study = sub.add_parser(
        "study",
        help="Full pipeline for given handles: fetch tweets → extract frameworks → write skill briefs",
    )
    study.add_argument("handles", nargs="+", help="X handles, e.g. @hnshah @pmarca")
    study.add_argument("--full", action="store_true", help="Ignore saved cursors and refetch all")
    study.add_argument(
        "--max", type=int, default=None, dest="max_tweets",
        help="Cap tweets pulled per author (default: all reachable history; varies by author, up to X's ~3,200 archive limit)",
    )
    study.add_argument(
        "--yes", "-y", action="store_true",
        help="Skip the uncapped-pull cost confirmation",
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
    if args.cmd in ("fetch-authors", "study"):
        try:
            return _cmd_fetch_authors(
                handles=args.handles, full=args.full, max_tweets=args.max_tweets,
                analyze=args.cmd == "study" or getattr(args, "analyze", False),
                yes=args.yes,
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
