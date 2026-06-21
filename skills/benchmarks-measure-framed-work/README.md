# benchmarks-measure-framed-work — NEGATIVE RESULT (kept as a cautionary artifact, NOT installed)

This skill is **deliberately not installed.** It's preserved as a documented negative
result from the skill-building experiments in this repo.

Source of the idea: Dan Shipper (CEO, Every) on Lenny's Podcast, 2026 — "benchmarks
only rise on problems already framed; framing the higher frame is the unmeasured human
move; models make yesterday's competence cheap." The SKILL.md captures that mechanism
faithfully, with the verbatim quotes (senior-engineer rewrite story, "yesterday's
competence is cheap," "AI doesn't use itself," "always a higher frame").

## What it was testing

The hypothesis: when someone extrapolates a benchmark/agent-autonomy number to "this
role is automated," baseline Claude gives *generic "AI won't take your job" reassurance*
and misses the differentiated **mechanism** (benchmarks only score already-framed
problems; the framing move is unmeasurable). If true, a skill injecting that mechanism
should score a large positive delta over baseline.

## What happened

Benchmarked on 3 trigger prompts (CTO citing SWE-bench to freeze junior hiring; an
agent-task-length chart used to pause a PM req; a friend extrapolating saturating
benchmarks to AGI-in-3-years), 4 substantive assertions each, with-skill vs. no-skill
baseline. Plus 2 non-trigger prompts (over-triggering check).

| Config | Pass rate (3 trigger evals) |
|---|---|
| Baseline (no skill) | **100%** (12/12) |
| With this skill | **100%** (12/12) — **delta +0.00** |

- **No upside.** Baseline Opus, with no skill, independently produces the *exact*
  load-bearing argument — not vague optimism. Verbatim from the no-skill runs:
  - *"someone has already decided this is a real bug, written it up... the hard part is upstream of where the benchmark starts"* (SWE-bench run)
  - *"the benchmark tasks are chosen because they have a clear spec and verifiable answer... the opposite of the core PM job: deciding what to build and why"* (PM run)
  - *"a benchmark measures performance on work already framed into a benchmark-shaped task... that framing is the job"* (AGI run)
  - All three baselines also landed the honest "role moves up the value chain, not erasure" conclusion and the seedcorn/pipeline point on their own.
- **The baseline was sometimes *richer*.** On the AGI eval the no-skill answer added
  arguments the skill doesn't even contain — the benchmark treadmill / Goodhart, the
  logistic-vs-exponential point, reliability compounding over long tasks, and the
  capability-to-deployment gap. The skill would have *narrowed* the answer, not improved it.
- **Over-triggering check: clean.** On both non-trigger prompts (designing a real
  support-agent eval; a paralegal's UX-vs-nursing career question with "no AI-hype
  angle") the model correctly declined to invoke the skill and answered on the merits.
  So the description is well-scoped — but a well-scoped description on a zero-delta skill
  is still a zero-delta skill.

## The lesson (why this is worth keeping)

This is the same finding as `decouple-from-the-ask` and the Shreyas skills, on a new
topic. The Shipper reframe is genuinely good *thinking*, but it's **conventional wisdom
inside the frontier-AI discourse the model is steeped in** — "benchmarks measure narrow
framed tasks, the human framing layer is what's unmeasured" is the model's *default*
response to a naive automation extrapolation, not a heterodox domain claim it lacks.

Skill ROI comes from injecting a **specific, correct, non-default domain conclusion** the
model wouldn't reach on its own — not from a **well-articulated version of a take the
model already holds**, however true. The high-delta author skills in this repo
(team-first, bias-to-impact, ownership-over-accountability) win because their reframe
*contradicts the model's default* (action is good → impact; accountability → obligation;
exec-first → team-first). This skill's reframe *is* the model's default, so there's
nothing to inject.

**Design heuristic (reinforced):** before building a contrarian-reframe skill, baseline-
test whether the model is actually on the *other* side of the reframe. If the no-skill
baseline already argues your thesis, the skill is a no-op no matter how well-written —
document it and move on.
