---
name: devils-advocate-against-your-own-agent
description: >-
  Before committing to a plan, idea, or output an AI agent just proposed — or that
  you arrived at while working WITH an agent — deliberately build the strongest case
  for why it's a bad idea, and kill it fast if it doesn't survive. Use whenever an
  agent has produced a plan/approach/result and the next step is to approve it, run
  it, ship it, or invest more agent hours on it ("the agent suggests X, should I let
  it proceed?", "agent finished, here's its plan/summary", "approve this and continue").
  Especially for novel/unproven directions before spending real build time or money.
---

# Devil's Advocate Against Your Own Agent

## The idea

Agents (and the humans steering them) are biased toward proceeding. An agent that
just proposed a plan will defend it; a human watching a plausible-looking plan scroll
by will rubber-stamp it. The cheapest place to kill a bad idea is *before* you spend
the build hours, tokens, or dollars executing it. So before committing, force the
opposite case: "why would this be a terrible idea?" Ideas that survive a genuine
attack are worth executing; ones that don't, you just saved the build cost on.

mvanhorn's own example: he asked an agent to build "a programming language designed
for agents." The agent argued it was a terrible idea — and a *different, better*
project (Printing Press) fell out of that argument. The devil's-advocate pass didn't
just gate the idea; it produced the real one.

## When you're invoked

An agent has produced something — a plan, an architecture, a next action, a "done"
summary — and the path of least resistance is to approve and continue. That approval
reflex is the trigger. This fires on *agent output mid-loop*, not on a human's
standalone strategic decision.

## The method

1. **Pin the proposal precisely.** What exactly is the agent about to commit you to —
   what gets built, run, spent, or shipped? Name the irreversible/expensive part.
2. **Attack it, don't audit it.** Build the strongest case that this is the *wrong*
   move: where it fails silently, what it costs that wasn't counted, the unstated
   assumption that has to hold, the cheaper thing that gets 80% of the value. Steelman
   the attack — a weak objection the agent swats away manufactures false confidence.
3. **Look for the better idea in the rubble.** Often the attack surfaces a stronger
   adjacent approach (as with Printing Press). Don't just pass/fail — see what the
   critique *proposes*.
4. **Decide fast.** If it survives, proceed — now with the failure modes known and
   instrumented. If it doesn't, kill it before the build, and state what to do instead.

## Output

```markdown
## What the agent is about to commit to
[the plan/action and its expensive or irreversible part]

## The case against (steelmanned)
[the strongest argument this is the wrong move]

## Better idea, if any
[the stronger adjacent approach the attack surfaced — or "none, the plan holds"]

## Verdict
[kill / proceed-with-guardrails / replace-with — and the why]
```

## Notes

- The reflex this fights is *approval*, not *disagreement*. Default Claude tends to
  validate an agent's plausible plan; the value is refusing to until it's been attacked.
- Weigh the cost of the build against the cost of the check. Cheap, reversible action:
  just go. Expensive or hard-to-undo (big refactor, real money, public ship): attack first.
- Sometimes the plan holds. Say so — it's now stress-tested, not just unexamined.
