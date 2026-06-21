# every-agent-needs-a-human — NEGATIVE RESULT (kept as a documented artifact, NOT installed)

This skill is **deliberately not installed.** It's preserved as a documented negative
result from the skill-building experiments in this repo, alongside `decouple-from-the-ask`
and the Shreyas skills.

## What it was testing

Dan Shipper's "automation is a lie" reframe: when someone plans to fully automate a
workflow or replace a role/team with an agent, the high-value move is to surface the
ongoing **ownership** cost. Every useful agent needs a human who gardens it; automation
doesn't subtract a human, it *relocates* one into a manager / forward-deployed-owner
role. Hypothesis: a skill carrying this reframe would change Claude's default behavior on
"automate this end-to-end / replace the role / set-and-forget" prompts.

## What happened

Benchmarked on 4 trigger evals (end-to-end automation, replace-the-role headcount math,
set-and-forget unattended agent, stalled-agent-ROI) plus 2 guards (an over-trigger
deterministic cron job, and a distinctness check vs. `team-first-ai-adoption`), with-skill
vs. no-skill baseline:

| Config | Trigger pass rate (evals 0–3) |
|---|---|
| Baseline (no skill) | **93.75%** (15/16) |
| With this skill | **100%** (16/16) — **+6.25%** |

- **Almost no upside:** baseline Opus already produced the skill's exact conclusions
  unaided on 3 of 4 trigger evals. The one differentiating assertion was a single cell in
  eval-0 (folding the owner's cost onto the *ROI ledger* specifically); on every other
  assertion the baseline got there on its own.
- **The tell:** in the stalled-ROI eval (eval-3), the **baseline** independently named
  "No ownership — unowned tools drift" as a root cause and prescribed "assign an owner per
  surviving agent... with the time to curate and correct." That is verbatim the skill's
  core diagnosis. In the unattended eval (eval-2), the baseline independently refused
  "never look at it," gated the irreversible send, and kept a human in the loop. In the
  headcount eval (eval-1), the baseline independently rejected the clean "4 of 6 vanish"
  subtraction and modeled relocation with the review cost on the ledger.

Caveat: the trigger prompts were strong, named situations. This doesn't prove the model
*never* under-weights ownership cost in subtler, more optimistic framings — but on the
clear cases that would actually trigger the skill, the base model already holds the
conclusion.

## The guards both passed (and so did the baseline)

- **Over-trigger (eval-4, deterministic cron):** with-skill correctly did *not*
  cargo-cult an owner onto fire-and-forget plumbing ("automation genuinely does subtract
  the work here... don't saddle it with a babysitter"). Good — but the baseline never
  over-triggered either, because it has no skill pulling it that way.
- **Distinctness (eval-5, "where should AI live"):** with-skill correctly self-excluded
  and led with the `team-first-ai-adoption` content, folding ownership in only as a
  one-line caveat. The boundary in the SKILL.md works. But note this means the skill's
  *correct* behavior on its nearest neighbor is to defer to a different skill — its unique
  surface area is narrow.

## The lesson (consistent with this repo's other negative results)

Per `decouple-from-the-ask`: skill value comes from injecting a **specific, correct,
non-default domain conclusion the model lacks** — not from a sensible disposition the
model already has. "Every useful agent needs a human owner / automation relocates rather
than deletes the human" is a *good* idea, but it's no longer heterodox to a 2026-era
model — it's the model's own default once the situation is concrete. The high-delta author
skills in this repo (`ownership-over-accountability`'s "-1.0 correlation,"
`bias-to-impact`'s "bias to action is one of the stupidest ideas") win because they carry
a *surprising, specific* claim the model wouldn't volunteer. This one carries a claim the
model volunteers on its own.

**Design heuristic reaffirmed:** baseline-test before installing. A reframe that feels
contrarian to a human can already be the model's default; if the baseline reaches the same
conclusion unprompted, the skill adds ceremony, not behavior. Measured delta here: **+0.06
on triggers**, below this repo's bar for installation.
