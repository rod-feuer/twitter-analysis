"""tally.py — turn the pile ledger into numbers.

Reads piles/ledger.jsonl (append-only, one graded claim per line) and reports how
the claims sort across the three piles — overall and BY POOL — so "Pile 3 is rare"
becomes a measured rate instead of a vibe. The point is the denominator: log every
claim you grade (the Pile 1 documented-truths and Pile 2 duds too), not just the
Pile 3 wins, or the rate is meaningless.

Ledger record schema (one JSON object per line in ledger.jsonl):
  id         short slug
  date       YYYY-MM-DD the grade was made
  claim      the claim, in one sentence
  source     who/where it came from ("@handle", "documented", ...)
  pool       sampling pool — THE key field for rarity:
             documented | trusted-expert | feedback | own-writing | random | ...
  pile       1 (documented truth) | 2 (overconfident headline) | 3 (frontier call)
  graded_by  how the grade was assigned — honesty about rigor:
             eyeballed | model-check | stress-test | panel | eval
  eval_delta optional float (baseline-vs-skill delta if formally eval'd), else null
  notes      free text

Pile 3 rate is reported per pool because rarity depends on where you look: a rate
from 'random' and a rate from 'trusted-expert' mean very different things. The
grading-rigor breakdown shows how many Pile 3 calls are *identified* (eval) vs only
*consistent-with* (eyeballed/stress-test) — don't let a hopeful call pose as a proven one.

Usage:
    python piles/tally.py                 # reads piles/ledger.jsonl
    python piles/tally.py --ledger PATH
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load(path):
    rows = []
    for i, line in enumerate(Path(path).read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"  ! skipping malformed line {i}: {e}")
    return rows


def pct(n, d):
    return f"{(100 * n / d):.0f}%" if d else "—"


def main():
    ap = argparse.ArgumentParser(description="Tally pile grades from the ledger.")
    ap.add_argument("--ledger", default="piles/ledger.jsonl", help="path to ledger.jsonl")
    args = ap.parse_args()

    if not Path(args.ledger).exists():
        print(f"no ledger at {args.ledger} — log some grades first")
        return
    rows = load(args.ledger)
    if not rows:
        print(f"no records in {args.ledger}")
        return

    total = len(rows)
    piles = Counter(r.get("pile") for r in rows)

    print(f"ledger: {args.ledger}   claims: {total}\n")
    print("by pile:")
    for p in (1, 2, 3):
        print(f"  Pile {p}: {piles.get(p, 0):2d}  ({pct(piles.get(p, 0), total)})")
    print(f"\noverall Pile 3 rate: {pct(piles.get(3, 0), total)}\n")

    by_pool = defaultdict(lambda: [0, 0])  # pool -> [pile3_count, total]
    for r in rows:
        pool = r.get("pool", "(unspecified)")
        by_pool[pool][1] += 1
        if r.get("pile") == 3:
            by_pool[pool][0] += 1
    print("Pile 3 rate by pool (rarity depends on where you look):")
    for pool, (p3, n) in sorted(by_pool.items(), key=lambda kv: -kv[1][1]):
        print(f"  {pool:16s} {p3}/{n}  ({pct(p3, n)})")

    p3_methods = Counter(r.get("graded_by", "?") for r in rows if r.get("pile") == 3)
    if p3_methods:
        print("\nPile 3 calls by grading rigor (identified vs hopeful):")
        for m, c in p3_methods.most_common():
            print(f"  {m:12s} {c}")


if __name__ == "__main__":
    main()
