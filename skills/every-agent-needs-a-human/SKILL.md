---
name: every-agent-needs-a-human
description: >-
  Surface the ongoing OWNERSHIP cost when someone plans to fully automate a workflow,
  replace a role/team with an agent, or let an agent run unattended. Use whenever the
  user says "automate this end-to-end," "replace the team/role with an agent," "set it
  and forget it / let it run unattended," "we gave everyone agents but adoption/ROI
  stalled," counts "headcount savings from automation," or is scoping a fully autonomous
  pipeline. The contrarian reframe (Dan Shipper: "automation is a lie") is the high-value
  move: automation doesn't subtract a human, it RELOCATES one into a manager / forward-
  deployed owner who gardens the agent — and that role is real, ongoing work. Trigger
  even when the user frames full autonomy as the obvious goal; the ROI failure mode is
  severing the human who cares about the agent. NOT for "where should AI live / how do
  we roll AI out to the team" (that's team-first-ai-adoption) — this is about the
  maintenance/ownership cost of automation and the relocated-human role.
---

# Every Agent Needs a Human (automation is a lie)

## The idea behind this skill

The seductive promise of an agent is subtraction: automate the workflow, delete the
human, bank the savings. Dan Shipper's claim is that this is *"a lie"* — not because
agents don't work, but because of what automating actually does to the human:

> *"Automation is a lie, in the sense that every time you automate something, in order
> to make sure the automation is working well you need a human on top of it making sure
> that it's working well."*

The mechanism is ownership. An agent that's any good needs someone who cares about it:

> *"In order for an AI agent to be useful right now, it really needs a human who cares
> about it... a human personal connection with someone who's watching what it does. And
> the minute you sever that connection... is the minute the agent is not really that
> useful anymore."*

So automation doesn't remove the human — it **relocates** them. The person stops doing
the task and starts *managing the thing that does the task*. That's a real job with real
hours, not a freebie. Shipper's punchline: *"automation was supposed to take away jobs,
but it looks like it just created one or many"* — the **forward-deployed engineer** who
owns the agent for the whole company. Even at scale, where companies converge on **one**
well-maintained company-wide agent instead of many fiddly personal ones, *"you basically
set up a forward deployed engineer or someone with that profile who's responsible for
making sure that that agent is working for the whole company."*

And the relocated role is genuinely demanding. Working with AI is like managing people:
*"managers actually spend a lot of time working... it still requires a lot of time and
attention."* Being AI-pilled and bullish on humans is not a contradiction — *"I'm
simultaneously extremely AI-pilled... and very bullish on humans and the role of humans
in making sure that AI is working well."*

This skill makes you surface the relocated-human / ownership cost **before** the user
prices in savings or scopes an unattended pipeline — so the ROI math and the plan are
honest.

## When you're invoked

- **End-to-end automation.** "Automate this whole workflow / build a fully autonomous
  pipeline." → don't just design the automation; name the owner it will require and fold
  their ongoing time into the plan. See *The move*.
- **Replace-the-role math.** "We can replace this role/team with an agent and save the
  headcount." → run *The headcount illusion*: the work relocates into an owner/manager
  role, it doesn't vanish. Be honest about partial savings vs. zero savings.
- **Set-and-forget.** "Set up the agent and let it run unattended." → this is the
  precise failure Shipper names (severing the connection). See *Why unattended decays*.
- **Stalled-ROI rescue.** "We rolled out agents and ROI/adoption stalled." → check
  whether each agent has a human who *cares about it*. Ownerless agents are the usual
  culprit. See *The diagnosis*.

## The diagnosis (when agents underdeliver)

Before prescribing more automation or better prompts, find the owner. For each agent or
automation, ask: **who is the single human who watches what this does and cares whether
it's good?** If the answer is "no one" or "everyone" (which is no one), that's the ROI
leak. Agents don't fail loudly — they drift quietly, and only a human who's watching
catches it. The fix is rarely a better model; it's assigning (and resourcing) an owner.

## The move

When the user wants to automate a workflow end-to-end, do both halves:

1. **Design the automation** they asked for — don't be a wet blanket about what agents
   can do. Shipper is extremely AI-pilled and so should you be.
2. **Name the relocated human and their ongoing job.** Every useful agent needs a
   gardener: someone who watches its output, corrects it, updates it as the world and
   the inputs change, and notices when it's quietly gone wrong. Make this explicit —
   who is it, and what's the realistic ongoing time cost (it's manager-shaped work, not
   zero). The plan isn't done until the owner is in it.

The reframe to deliver: *automation relocates the human, it doesn't remove them.* The
task-doer becomes the agent-manager. That's often still a great trade — one owner can
manage an agent doing the work of several task-doers — but it's a different job, and
pretending the human disappears is how the ROI promise breaks.

## The headcount illusion

When savings are being booked from "replacing" a role or team, resist the clean
subtraction. The realistic picture:

- The agent absorbs the *task*, but a human still has to **own** the agent — review,
  correct, maintain, and stand behind its output. That's the forward-deployed-engineer /
  manager role, and it's real ongoing cost.
- So model it as **relocation, not elimination**: N task-doers might become 1 owner + an
  agent. That can be a large, genuine saving — but it is not N→0, and quoting N→0 sets up
  a miss. Put the owner's cost on the ledger.
- The higher the stakes of the output, the more owner-time it needs. A human still has to
  be *accountable* for what ships; an agent can't hold that.

## Why unattended decays

"Set it and forget it" is the exact thing Shipper warns against: *the minute you sever
the human connection is the minute the agent stops being useful.* Unattended agents decay
because inputs shift, edge cases accumulate, and small errors compound silently with no
one watching. If the user wants something to run without a human in the loop, say plainly
what that costs in reliability — and design the human checkpoints (review cadence,
monitoring, escalation) that keep an owner connected, rather than pretending none are
needed.

## How this differs from team-first-ai-adoption

These two can look adjacent but answer different questions — don't conflate them:

- **team-first-ai-adoption** is about **where AI lives** when an org adopts it: shared
  public channels vs. private one-person chats, so context compounds as institutional
  memory. It's a *rollout-location* skill.
- **This skill** is about the **ongoing ownership/maintenance cost** of automation and
  the **relocated-human** role: every agent needs a gardener, and "replace the human"
  is a lie because the human moves into a manager/forward-deployed-owner job.

If the question is "how do we roll AI out to the team / where should it live," that's
team-first. If it's "let's automate this away / replace this role / let it run
unattended / why did our agents stall," that's this skill. They can both apply — a
team-first rollout still needs owners for its agents — but lead with the one that
matches the user's actual question.

## When this doesn't apply (the honest boundary)

Don't force the ownership-cost reframe onto things that are genuinely fire-and-forget.
Plenty of deterministic automation — a cron job, a data pipeline, a formatting script,
a well-bounded rules engine — runs fine for years with near-zero human gardening, and
insisting it needs a devoted owner would be cargo-culting. The reframe is for *agentic,
judgment-laden, open-ended* work whose quality drifts and whose output someone has to
stand behind. If the task is narrow, deterministic, and low-stakes, say so and let it be
automated cleanly. Reserve the "every agent needs a human" move for where the human
judgment actually relocates rather than disappears.

## Output

Give a real plan, not a lecture. Generally:

```markdown
## The reframe
<automation relocates the human into an owner/manager role — it doesn't delete them>

## The automation
<what to actually automate — be concretely AI-pilled here>

## The owner it needs
<who gardens this agent, and the realistic ongoing time cost (manager-shaped, not zero)>

## The honest ROI
<relocation math: N task-doers → 1 owner + agent, not N → 0; or, if truly deterministic
and fire-and-forget, say the ownership cost is genuinely near-zero>
```
