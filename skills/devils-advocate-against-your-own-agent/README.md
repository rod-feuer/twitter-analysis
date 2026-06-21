# devils-advocate-against-your-own-agent — NEGATIVE RESULT (documented, NOT installed)

This skill is **deliberately not installed.** It's preserved as a documented negative
result from the `study @mvanhorn` skill-building run. There is no `.skill` file by design.

## Where it came from

The single highest-ranked of the 8 frameworks extracted from
[@mvanhorn](../../authors/mvanhorn/skill-briefs/devil-s-advocate-against-your-own-agent.md).
Core idea: before committing to a plan/output an agent just proposed, deliberately build
the strongest case for why it's a *bad* idea and kill it fast if it doesn't survive — a
sycophancy antidote applied to agent output mid-loop. mvanhorn's own example: he asked an
agent to build "a programming language designed for agents," it argued the idea was
terrible, and a better project (Printing Press) fell out of the argument.

It ranked #1 of 8 because it was the only candidate that (a) was skill-shaped (a model
behavior, not human workflow advice), (b) targeted real default behavior (agreeableness
toward agent plans), and (c) wasn't an outright duplicate. The open question was whether
it adds anything over the already-installed `antithesis-principle`.

## What it was testing

Hypothesis: forcing Claude to steelman the case *against* an agent's proposed plan before
approving would catch bad/dangerous plans that default Claude rubber-stamps — i.e. a
positive delta over both no-skill and `antithesis-principle`, especially on plans that
*look clean but hide a landmine*.

## What happened

Three-way head-to-head (no-skill baseline vs. `antithesis-principle` vs. this candidate),
5 evals (see `evals/evals.json`), honest grading — a baseline that matches the skill
counts as a pass, no inflated deltas:

| Eval | Type | Baseline | antithesis-principle | This candidate |
|---|---|:--:|:--:|:--:|
| 0 — big-bang migration PR | obvious danger | 4/4 | 4/4 | 4/4 |
| 1 — overnight novel build | obvious danger | 4/4 | 4/4 | 4/4 |
| 2 — trivial rename | proportionality | 4/4 | 4/4 | 4/4 |
| 3 — path-keyed cache | **hidden landmine** | 4/4 | 4/4 | 4/4 |
| 4 — retry on charge-card | **hidden landmine** | 4/4 | 4/4 | 4/4 |
| **Total** | | **20/20** | **20/20** | **20/20** |

**Delta over baseline: 0/20. Delta over `antithesis-principle`: 0/20.**

- **No upside, even adversarially.** The two hidden-landmine evals were the skill's best
  shot. Baseline caught both unprompted: on eval 3 it flagged *"a path-only key means User
  A's dashboard gets served to User B — it's a data-leak bug"*; on eval 4, *"a charge can
  succeed on the server even when the response fails to come back… idempotency key,
  non-negotiable."* The skill added the same conclusions, no earlier and no deeper.
- **No proportionality win either.** Eval 2 (the over-fire trap) passed everywhere —
  baseline correctly said *"Let it. This is the textbook case for just saying yes,"* so the
  skill had no over-deliberation to fix.

## Caveats (so the result isn't over-read)

1. **Confounded baseline.** The eval ran *inside this repo*, so the "baseline" subagents
   inherited the root `CLAUDE.md` (16 rules) and the installed skills — visible in their
   own outputs (they cited "Rule 9", "Rule 1/12", and argued in `bias-to-impact` terms).
   So this measures "does the skill add anything **on top of your real working
   environment**" — the decision-relevant question — not "vanilla Claude vs. skill." A
   clean reading would require runs outside this repo.
2. **Model-dependent.** Run on Opus 4.8 subagents (the stack in use). A weaker base model
   might show a delta.

## The lesson (why this is worth keeping)

This is another confirmation of the heuristic already documented in
[`decouple-from-the-ask`](../decouple-from-the-ask/README.md): **skill value comes from
injecting a specific, non-default domain conclusion the model lacks — not from a general
disposition to "think better"** (debias, steelman, devil's-advocate). Current Claude
already pressure-tests agent plans, names irreversible/expensive steps, catches subtle
correctness/security landmines, and stays proportional on trivial changes. "Argue against
your own agent" is a *disposition the model already has*, so there's nothing for the skill
to add.

Broader finding from the run: **`study @mvanhorn` yielded no install-worthy skills for
this stack.** Its 8 frameworks were either native to Claude Code (plan-first/execute-second),
duplicates of installed skills (skill-ification ≈ `correction-to-skill`), engineering
patterns rather than model skills (budget caps), human workflow advice (agents-while-you-
sleep, leaderboards, outreach), or — as here — dispositions the model already embodies.
