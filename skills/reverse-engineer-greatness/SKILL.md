---
name: reverse-engineer-greatness
description: >-
  Systematically learn from someone who is ahead of the curve by reconstructing
  HOW they work, not just copying what they produce. Use whenever the user admires
  an operator, builder, writer, or team and wants to learn from them — e.g. "how
  does X do it," "I want to get good at the thing so-and-so is great at," "break
  down this person's workflow," "study/emulate this expert," "what can I learn from
  how they work." Also use when the user has gathered an exemplar's public traces
  (GitHub activity, a blog, a workflow writeup, talks, threads) and wants the
  repeatable method pulled out of them. Trigger even if the user doesn't say
  "reverse engineer" — any time someone wants to turn another person's excellence
  into something they can actually apply, this skill applies.
---

# Reverse-Engineer Greatness

## The idea behind this skill

When you meet someone clearly ahead of the curve, the instinct is to copy what they
*made* — their thumbnail, their landing page, their repo structure. That's cargo
cult. The output is the visible tip; the value is the **invisible process** that
produced it — the decisions, the habits, the order of operations, the things they
chose *not* to do. Hiten Shah's framing: *"reverse engineer greatness whenever
possible — see someone ahead of the curve and try to understand how they do it."*

The goal of this skill is to reconstruct that process from whatever traces a person
leaves, extract the **transferable decisions** (not the surface artifacts), and turn
them into something the user can apply to their own work. Done well, it's one of the
fastest ways to learn — and AI makes it dramatically cheaper, because an agent can
dissect a body of someone's public work at a scale a human reading-by-hand can't.

One more principle worth holding onto, in Hiten's words: *"experience only stays
valuable when it keeps updating... the most effective operators treat experience like
a living system."* So the output isn't a monument to one person — it's a hypothesis
you test and keep revising.

## When you're invoked

Figure out which situation you're in:

- **You have traces in hand.** The user points you at an exemplar's public work — a
  GitHub profile, a blog, a recorded talk, a thread, a workflow writeup. Go straight
  to *Dissecting the process*.
- **You have a name and an admiration.** The user knows *who* and *what* they admire
  ("her launches always nail positioning") but hasn't gathered anything. Start with
  *Gathering signals*, then dissect.
- **The user just wants the output copied.** ("Make me thumbnails exactly like
  MrBeast's.") Don't just comply — that's the trap this skill exists to avoid. See
  *The copy trap* and redirect to the process level.

## Gathering signals

You're hunting for **evidence of process**, not just finished products. The richest
signals show the work *in motion*:

- **Public activity trails** — commit history, PRs, changelogs, edit history. *What
  order did they build things in? What did they fix repeatedly? What did they delete?*
- **Stated workflow** — blog posts, "how I work" threads, talks, interviews where they
  narrate their own method.
- **Decisions over time** — how their approach changed, what they stopped doing. The
  *deltas* are often more revealing than any single snapshot.
- **The negative space** — what a great operator consistently *doesn't* do is as
  instructive as what they do.

If you have tool access (web search, a repo, a connected source), offer to gather
these directly rather than making the user assemble them. Use AI to dissect at scale —
that's the leverage. If you can't access the traces, tell the user exactly what to
collect and why each one matters.

## Dissecting the process

This is the core. For the exemplar and the specific excellence the user cares about,
work to answer:

1. **Name the specific greatness.** "Great at product" is too vague to learn from.
   Pin it: *what exactly* are they better at, observable in *what specific outputs*?
2. **Trace the process behind it.** From the signals, reconstruct the sequence of
   moves that produces that result. What do they do first? What do they refuse to do?
   Where do they spend disproportionate effort?
3. **Extract the transferable decisions.** This is the crux — separate the
   *principle* from the *person*. "He uses a black background" is surface. "He removes
   everything that isn't the one thing the viewer must notice" is transferable. The
   test: would this still be true if they worked in a totally different medium?
4. **Find the why.** A decision you can't explain is a decision you can't reapply.
   Push until you understand *why* the move works, so it survives contact with the
   user's different situation.
5. **Separate the imitable from the idiosyncratic.** Some of their edge is
   transferable method; some is raw talent, timing, or audience you can't copy. Be
   honest about which is which — false hope wastes the user's effort.

## Cross-referencing (when there's more than one exemplar)

If the user admires several people in the same domain, don't analyze them in
isolation. The highest-value output is the **convergent pattern** — the move that
shows up across all of them is far more likely to be a real principle than any single
person's quirk. Where they diverge, that's a genuine choice the user gets to make,
and worth surfacing as such.

## Output

Produce something the user can act on, not a biography. Use this shape:

```markdown
# Reverse-engineering: <person> — <the specific greatness>

## What they're actually great at
<the pinned, observable skill>

## The process behind it
<the reconstructed sequence of moves, from the signals>

## Transferable decisions (the part you can use)
- <principle, stated so it works in the user's context> — *why it works*
- ...

## Idiosyncratic / not transferable
<the talent/timing/audience parts to be honest about>

## Your first experiment
<one concrete thing the user can try on their own work this week to test the method>
```

The **first experiment** matters most. Reverse-engineering that never gets tested is
just admiration with extra steps. End with the smallest real test of the method on
the user's own work, because the method only becomes theirs once it survives that.

## The copy trap

When the user asks to clone the *surface* ("same exact style/titles/layout"), gently
redirect — not to refuse, but because copying outputs is the slow, brittle path and
they came here to actually get good. Cloning the artifact gets you one artifact;
extracting the process gets you the ability to produce many, in your own context.
Name the underlying decisions and offer to apply *those* to their specific case.
Copying identity, as Hiten warns, is also where stale judgment hardens into a cage —
the point is to learn the method and then make it your own, not to wear someone
else's choices.
