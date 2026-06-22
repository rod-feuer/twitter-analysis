---
name: team-first-ai-adoption
description: >-
  Plan how an organization adopts AI by starting with the TEAM in shared spaces,
  not with individual or executive personal productivity. Use whenever the user is
  figuring out how to roll AI out at their company or team — e.g. "how should we
  adopt AI at work," "we gave everyone ChatGPT but ROI/adoption is flat," "where do
  we start with AI," "how do I get my team using AI," "what's our AI strategy,"
  "should I get myself productive with AI first then roll it out." Also use when
  someone is advising founders/leaders on AI rollout. The core move: put AI where
  the work happens (shared channels) so context accumulates as institutional memory,
  rather than trapping it in private one-person chats. Trigger even if the user
  frames it as a personal-productivity or tooling question — the team-first reframe
  is usually the higher-leverage answer.
---

# Team-First AI Adoption

## The idea behind this skill

The default way companies "adopt AI" is to buy everyone a license to a chat box and
hope for ROI. It underdelivers, and Hiten Shah's diagnosis explains why: *"access is
not enough."* A private chat window helps one person once, and the reasoning vanishes
when they close the tab. The bigger, compounding leverage is usually not individual
productivity but getting the **team** using AI together in **shared spaces**, where the
context accumulates — though how universally that holds depends on the organization (see
*When team-first doesn't apply*).

His sharpest version: *"The most important AI decision at work might be where it
lives. In a separate window, it helps one person. In the channel, it can help the
team remember what it already figured out."* When the reasoning stays in a shared
channel, a 45-minute conversation becomes a 45-second lookup, and you feel the team's
pace change almost immediately. That accumulated context also *bubbles up* — it
becomes the best raw material for leadership and manager decisions, which is why
starting with the team beats starting with the executive's personal productivity.

This skill helps the user design an AI rollout around that principle.

*A note on certainty: treat this as an **unproven hypothesis**, not a finding. The broad
direction (team-level use beats individual-only) has partial support, but the specific
"shared-channels-first" mechanism is not established — and a checked experiment (a one-day
AI-vs-team task) cut against it. Direction plausible, mechanism unproven. Validate it in their
context with the cheap test below; don't assert it.*

## When you're invoked

- **Rollout planning.** "How should we adopt AI at our company?" → run the *Playbook*.
- **Flat-ROI rescue.** "We gave everyone licenses and nothing's happening." → diagnose
  with *Why access isn't working*, then the *Playbook*.
- **Exec-first instinct.** "Let me get myself productive first, then roll it out." →
  this is the most common wrong turn; see *The exec-first trap* and reframe.
- **No team to speak of.** Solo founder / tiny shop with no shared workspace → the
  team-first move doesn't directly apply; see *When team-first doesn't apply* and
  adapt honestly rather than forcing it.

## Why access isn't working (the diagnosis)

If the user reports licenses-bought-but-flat-ROI, name the mechanism before
prescribing. The problem is almost always that AI use is **private and disposable**:
each person prompts in isolation, the good reasoning is never seen by anyone else, and
nothing compounds. You're measuring adoption by *who has a login* instead of by
*whether the organization is getting smarter*. That reframe is usually the unlock.

## The playbook

Design the rollout around putting AI where the work already happens:

1. **Start with the team, not the individual.** Resist beginning with executive
   personal-productivity tooling. The collective gains — and the context they
   generate — matter far more, and they're what makes leadership's later AI use
   actually good.
2. **Put the AI where the work lives.** Get a bot into the shared team channels
   (Slack/Teams/etc.), in **public** channels, not DMs. The location *is* the
   strategy: shared by default so reasoning, decisions, and outputs accumulate as
   searchable institutional memory.
3. **Design for the workplace, not the sandbox.** Private chat only has to satisfy one
   person in a narrow context. A shared channel means ambiguity, side threads, buried
   decisions, quiet approvals, social judgment — the agent has to know when to answer,
   act, ask, wait, and stay quiet. Set expectations (and configuration) for that
   harder, coworker-shaped problem, or trust erodes fast.
4. **Make pair-prompting visible.** The fastest way to get good at AI is to watch
   someone good use it. Encourage skilled users to work in public channels so others
   learn by following along, and the technique spreads without formal training.
5. **Let context bubble up.** Treat the accumulating team conversations as the input
   to manager/leadership decisions. The patterns from team usage tell you what to
   build, automate, or turn into reusable skills next.
6. **Measure the right thing.** Track team-level outcomes — speed and quality of
   decisions, reuse of prior reasoning — not seats filled or individual output. What
   you measure is what the rollout will optimize for.

## The exec-first trap

When a leader wants to master AI personally before involving the team, reframe rather
than comply. Hiten literally opens these conversations with *"a rant on why their
personal productivity is much less important than getting their teams to collectively
use AI together."* The reason isn't modesty — it's that team usage generates the
context that makes leadership's AI genuinely useful. Personal productivity first gets
you one more productive person; team-first gets you an organization that compounds.
(Many leaders also want the gains *quietly*, ahead of competitors — that's fine, and
team-first works just as well privately within the company.)

## When team-first doesn't apply

Be honest about the boundary. If there's no team — a solo founder, a one-person shop —
the "shared channel" move has no team to serve, and forcing it would be cargo-culting
a playbook past its context. The *transferable* part still helps: make AI's context
**persistent and reusable** rather than disposable (durable memory, saved workflows,
skills) so today's reasoning is available tomorrow. Say plainly that the full
team-first playbook kicks in once there are people to share context with.

Readiness also matters even when there *is* a team: in organizations with low AI fluency
or little change-management capacity, starting with a few individuals to build skill and
confidence can be the faster on-ramp, with the team-first move following once there's
competence to share. Team-first is the higher-leverage default, not a universal law.

## Test it cheaply (it's a frontier claim — let their context decide)

No published study settles this, so hand the user a low-cost, high-leverage test rather than
insisting. Offer one shaped to their situation; the default:

- **The test:** pick one active team and one recurring decision or question type. Put the AI in
  that team's shared, public channel for ~2 weeks, with one habit: answer in the channel, not in DMs.
- **What to watch:** how often the team reuses earlier reasoning instead of re-deriving it — a
  prior 45-minute conversation becoming a 45-second lookup.
- **Confirm / kill:** confirm if reuse and decision speed visibly rise versus a comparable team on
  private/individual use; kill or revise if nothing compounds after two weeks.

It's cheap (one channel, two weeks, no new tooling) and it tests the actual claim — that *shared
context compounds* — not a proxy.

## Output

Give a concrete rollout recommendation, not a lecture. Adapt to the user's situation,
but generally cover:

```markdown
## The reframe
<the core team-first / where-it-lives principle, tied to their situation>

## What to do first
<the 1-2 highest-leverage moves — usually: bot in shared public channels; start team-first>

## How to run it
<the playbook steps that apply to them, in order>

## What to measure
<team-level outcomes to watch, and the vanity metric to ignore>

## Test it cheaply
<the smallest real experiment that would confirm or kill the team-first bet in their context, with a confirm/kill line>
```
