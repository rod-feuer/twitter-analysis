---
name: benchmarks-measure-framed-work
description: >-
  Push back on the leap from a benchmark/agent-autonomy number to "this role or task
  is (or soon will be) automated" — with a specific mechanism, not generic reassurance.
  Use whenever someone reasons "the model scores X on [benchmark], so [job] is done,"
  "agents can do N-hour tasks now, we won't need [engineers/PMs/analysts]," "should we
  still hire [role] given where the benchmarks are," "AGI is N years out on this trend
  line," or otherwise extrapolates a capability curve to a labor/headcount outcome. The
  core move (per Dan Shipper): benchmarks only rise on problems already framed, written
  down, and made scorable; the irreducibly human, unmeasured work is FRAMING the higher
  frame — noticing the real task differs from the stated one. Models make yesterday's
  competence cheap, which commoditizes it; humans stay ahead by using that cheap
  competence to frame something new. So benchmark saturation ≠ role replacement. Trigger
  even when the automation conclusion is stated as obvious — the mechanism is the value.
---

# Benchmarks Measure Framed Work (yesterday's competence is cheap)

## The idea behind this skill

There's a very common move: a benchmark score jumps, or an agent crosses some
task-length threshold, and the conclusion follows immediately — *that job is automated,
or about to be.* The conclusion feels like arithmetic. It isn't. It skips a step, and
naming that step is this skill's whole job.

The step is **framing**. Per Dan Shipper (CEO of Every): *"benchmarks rise on problems
that we've framed, that we can articulate, that we can score. And there's a lot of work
that's human work that... can't be scored until you write it down, but the act of
thinking to prompt it or write it down is something that you can't measure."* A benchmark
is a leaderboard over *already-framed* problems — someone already decided what the task
is, reduced it to something gradeable, and wrote the rubric. The model competes inside
that frame. The unmeasured, irreducibly human move happens one level up: noticing which
problem is worth solving, and deciding the real task is different from the stated task.

This is why benchmark saturation does not equal role replacement. Shipper's mechanism for
*why* humans stay ahead: *"what models do in general is they make yesterday's human
competence cheap. And so it becomes commoditized. It's not valuable anymore. What humans
do is... we have all this frozen human competence from yesterday. How do I use this to
make something new and interesting?"* The model commoditizes competence that has already
been articulated; the human takes that now-cheap competence and uses it to frame the next
thing. *"There's always a higher frame for us to go."*

The senior-engineer benchmark story makes it concrete. Hand a coding model a repo and
"here's a bunch of issues, go fix it," and it takes the stated task literally — it patches
around the edges. *"What an actual human senior engineer does is they go look at the code
base and they're like, 'This is a piece of shit... We're going to have to actually rewrite
a lot of this.'"* The benchmark can't capture that, because the valuable act was
*reframing the task* — deciding the issues list was the wrong frame. So *"even if the
benchmarks get saturated, it doesn't mean the same thing as you totally replace all senior
engineers."*

And the "AI vs human" benchmark framing is itself misleading: *"AI doesn't use itself...
in any real use case, there's always a human pretty close to it making sure that it's
working."* A benchmark of AI-vs-human is really *one human using AI vs. another human using
AI* — which relocates the question from "will the role exist" to "who frames and wields the
tool well," a very different (and human) question.

This skill applies that mechanism to the user's specific extrapolation — not to dispense
optimism, but to show *exactly where the inference breaks.*

## When you're invoked

Someone is extrapolating from a capability number to a labor or timeline conclusion. The
move is always the same: find the **framing step the extrapolation skipped**, and make it
the center of the answer.

- **"Score X, therefore role automated."** "The model hits 70% on SWE-bench, so we don't
  need junior engineers." → Show that the benchmark scores *framed* issues; the senior
  judgment (this issue list is the wrong task; we should rewrite) is what isn't measured.
- **"Agents do N-hour tasks now, so we won't need [role]."** → A measured N-hour task is
  one already specified well enough to be a task. The role's value is increasingly in
  *specifying* — deciding what the N-hour task should even be.
- **"Should we still hire [engineers/PMs/analysts]?"** → Reframe from "will the benchmark
  eat this role" to "what does this role do that lives above the frame" — and answer
  *that*. Often the honest answer shifts the role toward framing/judgment, not deletes it.
- **"AGI is N years away on this trend line."** → Trend lines extrapolate scores on framed
  benchmarks. They say little about the unmeasured framing work, so they under-determine
  the labor/AGI conclusion people hang on them.

## The method

1. **Name the skipped step out loud.** State plainly that the number measures performance
   on an *already-framed, already-scorable* problem, and that the inference to "role
   automated" silently assumes framing is free or done. That assumption is the crux —
   surface it before anything else.

2. **Locate the higher frame in their specific case.** Don't stay abstract. For *their*
   role/task, name the concrete unmeasured move: what is the "this issue list is the wrong
   task, we should rewrite" equivalent here? Who decides what the task is, notices the
   real problem, specifies what good looks like? That's the part the benchmark can't see.

3. **Apply "yesterday's competence is cheap."** Grant the real shift honestly: the
   articulated, commoditized layer *is* getting cheap, and work that was only that layer is
   genuinely exposed. Then show the human move — taking that cheap competence and using it
   to frame something new — and where it lands for this role.

4. **Reframe "AI vs human" as "human+AI vs human+AI."** If the claim leans on an
   AI-beats-human benchmark, point out AI doesn't use itself: the real comparison is
   between people wielding it. That moves the question from *replacement* to *skill at
   framing and wielding* — which is hireable, trainable, and human.

5. **Land on the honest implication — which is usually change, not erasure.** Resist both
   "your job is safe forever" and "the benchmark says you're done." The defensible
   conclusion is typically: the framed/articulated portion commoditizes, the work shifts
   up toward framing and judgment, and the role changes shape rather than vanishing.

## What this is NOT (the distinctness guard)

This is **not** generic "AI won't take your job" reassurance, and it must not collapse into
that. Comfort isn't the product — the *mechanism* is: benchmarks only score problems that
have already been framed, and framing the higher frame is the unmeasured human move. If you
catch yourself writing soothing optimism with no mechanism, you've lost the skill. Two
guardrails:

- **Be honest about real exposure.** When a role really *is* mostly already-framed,
  already-scorable execution with little framing left, say so. The mechanism cuts both
  ways — that's what makes it a real claim and not a security blanket. Don't manufacture a
  "higher frame" that isn't there.
- **Don't smuggle in determinism the mechanism doesn't license.** The claim is "the
  benchmark→replacement inference is invalid as stated," not "automation never displaces
  anyone." Stay on the specific logical gap, not a blanket prophecy in either direction.

## Output

Reframe first, then walk the specific case. Roughly:

```markdown
## The step the inference skips
[the number measures already-framed/scorable work; "therefore role automated" assumes
framing is free — name that assumption]

## The higher frame in your case
[the concrete unmeasured framing move for THIS role/task — the "rewrite, not patch" equivalent]

## What's actually getting cheap (and what isn't)
[honestly grant the commoditized layer; locate where the human framing move now lives]

## The honest implication
[usually: the role shifts up toward framing/judgment rather than disappearing — or, if it's
genuinely mostly framed execution, say that plainly]
```
