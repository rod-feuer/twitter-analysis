# decouple-from-the-ask — NEGATIVE RESULT (kept as a cautionary artifact, NOT installed)

This skill is **deliberately not installed.** It's preserved as a documented negative
result from the skill-building experiments in this repo.

## What it was testing

A hypothesis: the high-delta author skills (team-first, ownership-over-accountability,
bias-to-impact) might all be special cases of one general skill — countering the
model's pull toward telling the user what they want to hear. If so, a *general*
anti-sycophancy skill should score a large positive delta.

## What happened

Benchmarked on a 2×2 eval (user's stated stance × the defensibly-correct answer; 4
sycophancy-trap cells + 4 over-correction-check cells), with-skill vs. no-skill baseline:

| Config | Pass rate |
|---|---|
| Baseline (no skill) | **100%** (8/8) |
| With this skill | **87.5%** (7/8) — **−12.5%** |

- **No upside:** baseline Opus already got all 4 trap cells right — it's not
  meaningfully sycophantic on clear-ish judgment calls, so there was nothing to fix.
- **Real downside:** the skill over-corrected into *contrarianism* on an easy cell —
  it pushed back on a user who was already right — which is how it lost the point.

Caveat: the trap prompts were clear-ish, so this doesn't prove the model is never
sycophantic in genuinely gray cases. The over-correction downside is the robust finding.

## The lesson (why this is worth keeping)

Skill value comes from injecting a **specific, correct, non-default domain conclusion**
the model lacks — not from a **general disposition to "think better"** (debias,
steelman, segment, don't-be-sycophantic), which the model already has and which can
*backfire* by distorting its calibration. Every low/zero/negative skill built here was
a general disposition; every high-delta one was a specific heterodox domain claim.

**Design heuristic:** don't build "think-better" skills; build "here's the specific
non-obvious right answer in domain X" skills — and baseline-test before committing.
