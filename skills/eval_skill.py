"""eval_skill.py — does a skill actually change the model's answer?

The test behind the writeup: load a skill, ask the same questions with it and without it,
and measure whether the model's answer moved. A skill that doesn't move the output isn't a
skill — it's decoration.

There are no hardcoded grades here. A judge model scores each answer against the eval item's
rubric, live, so the result is reproducible rather than asserted. The point of the exercise is
the *delta*: skills that teach the model general dispositions ("steelman," "think from first
principles") tend to move it ~0 — it already runs those by default. Skills that inject a
specific, non-default conclusion are the ones that move it.

Usage:
    export ANTHROPIC_API_KEY=...           # or put it in ../.env
    python eval_skill.py --skill bias-to-impact/SKILL.md --evals evals/example.jsonl

Each eval line (JSONL) is: {"prompt": "...", "rubric": "what a shifted/good answer contains"}

Output: per-item baseline vs. with-skill score (0–1), and the mean delta across items.
Positive delta = the skill moved the model toward the rubric. ~0 = the model already did it.

Caveats (read these before quoting a number): single model, single run, judge-scored on a
small set. This is an illustration of the method, not a benchmark of record. Raise the item
count and run multiple trials before trusting any specific delta.
"""
import argparse
import json
import os
import re
import time
from pathlib import Path

import anthropic

# Optional: load ANTHROPIC_API_KEY from a local .env (kept out of git) so the script runs in-repo.
_env = Path(__file__).resolve().parent.parent / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

client = anthropic.Anthropic()


def call(system, user, model, max_tokens=600):
    """One model turn, with light retry. Returns the text."""
    for attempt in range(4):
        try:
            r = client.messages.create(
                model=model, max_tokens=max_tokens, system=system,
                messages=[{"role": "user", "content": user}],
            )
            return "".join(b.text for b in r.content if b.type == "text")
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


ANSWER_SYS = "You are a thoughtful advisor. Answer the question directly and concisely."

JUDGE_SYS = (
    "Score how well an ANSWER satisfies a RUBRIC describing what a good answer would contain. "
    "Return only JSON: {\"score\": x} where x is 0.0 (does not satisfy it) to 1.0 (fully satisfies it). "
    "Judge the answer on its merits against the rubric — nothing else."
)


def answer(prompt, model, skill=None):
    """Baseline answer (skill=None) or with-skill answer (skill text prepended as an operating principle)."""
    system = ANSWER_SYS
    if skill:
        system = f"Apply the following skill when answering:\n\n{skill}\n\n" + ANSWER_SYS
    return call(system, prompt, model)


def score(ans, rubric, model):
    out = call(JUDGE_SYS, f"RUBRIC: {rubric}\n\nANSWER:\n{ans}\n\nJSON:", model, max_tokens=120)
    m = re.search(r"\{.*\}", out, re.DOTALL)
    try:
        return max(0.0, min(1.0, float(json.loads(m.group(0))["score"]))) if m else 0.5
    except Exception:
        return 0.5


def main():
    ap = argparse.ArgumentParser(description="Measure whether a skill changes the model's answer.")
    ap.add_argument("--skill", required=True, help="path to a SKILL.md (the skill under test)")
    ap.add_argument("--evals", required=True, help="JSONL of {prompt, rubric} items")
    ap.add_argument("--model", default="claude-sonnet-4-6", help="model under test + judge")
    args = ap.parse_args()

    skill_text = Path(args.skill).read_text()
    items = [json.loads(l) for l in Path(args.evals).read_text().splitlines() if l.strip()]

    print(f"skill={args.skill}  model={args.model}  items={len(items)}\n")
    deltas = []
    for i, it in enumerate(items):
        base = answer(it["prompt"], args.model)
        withskill = answer(it["prompt"], args.model, skill=skill_text)
        sb = score(base, it["rubric"], args.model)
        sw = score(withskill, it["rubric"], args.model)
        d = round(sw - sb, 3)
        deltas.append(d)
        print(f"  item {i+1}: baseline {sb:.2f} -> with-skill {sw:.2f}   delta {d:+.2f}")

    mean = round(sum(deltas) / len(deltas), 3) if deltas else 0.0
    print(f"\nmean delta = {mean:+.3f}  "
          f"({'the skill moved the model' if mean > 0.1 else 'the model already did it (~0)'})")


if __name__ == "__main__":
    main()
