---
name: correction-to-skill
description: >-
  Turn repeated AI corrections into reusable skills. Use this whenever the user
  notices they keep fixing, rewriting, or re-explaining the same thing to an AI —
  e.g. "I always have to tell it to...", "every time it does X I fix it to Y", "I
  keep correcting the same mistake", or when they want to figure out which of
  their workflows are worth turning into a skill. Also use it to mine a corpus
  (chat history, docs, Slack threads, support tickets) for skill-worthy patterns.
  The core insight: the mistake you keep fixing is your next skill. Trigger this
  even when the user never says the word "skill" — if they describe a recurring
  correction or a fix they make over and over to AI output, this skill extracts
  the hidden process and codifies it into something reusable.
---

# Correction → Skill

## The idea behind this skill

The most valuable moment in an AI interaction is usually not the output — it's the
**correction**. When the model gets close enough to be useful but wrong enough that
you have to step in, your fix carries information the model didn't have: your taste,
your context, the way the work actually gets done. Most people treat that fix as
cleanup, apply it, and move on. The information evaporates.

But a correction you make *repeatedly* is a different animal. It's a signal that a
**reusable process is hiding inside the work** — judgment you're re-supplying by hand
every single time. The whole job of this skill is to catch that signal and turn it
into a skill so the judgment stops disappearing after every chat.

The litmus test, in one line: **the mistake you keep fixing is probably your next skill.**

## When you're invoked

You'll land in one of two situations. Figure out which, then follow that path.

- **Path A — one correction in hand.** The user already knows the thing they keep
  fixing ("every time it writes my standup it buries the blocker — I always move it to
  the top"). Go to *Extracting a skill from a correction*.
- **Path B — go find them.** The user wants to discover what's worth codifying and
  points you at a corpus — past chats, a doc folder, Slack export, ticket history.
  Go to *Mining a corpus for candidates*, then run each candidate through Path A.

If it's ambiguous, ask one question: *"Do you already have a specific thing you keep
correcting, or do you want to dig through your past AI work to find the patterns?"*

## Extracting a skill from a correction (Path A)

The goal is to recover the *process* hiding inside the fix — not just the fix itself.
A skill that only encodes "the answer to this one case" is worthless; a skill that
encodes "here's how to get this kind of thing right" is leverage.

Work through these with the user. Don't interrogate — infer what you can from what
they've already said and only ask about real gaps.

1. **Pin the recurring correction.** What does the AI produce, and what do you change
   it to? Get a concrete before → after. Vague dissatisfaction ("it's just off") isn't
   a skill yet — push for the specific edit they make.

2. **Confirm it actually recurs.** A one-off fix is just a one-off fix. Ask: does this
   come up across many tasks, or was it a single weird case? If it doesn't repeat,
   say so honestly — not everything should become a skill, and a library full of
   single-use skills is noise. (See *When NOT to make a skill* below.)

3. **Name the hidden judgment.** This is the crux. Ask *why* the AI's version is wrong
   and theirs is right. The answer is the transferable rule. "Blocker goes first
   because whoever reads a standup is scanning for what's stuck" — that *why* is what
   makes the skill generalize beyond today's standup.

4. **Generalize the trigger.** When should this skill fire? Describe the *class* of
   situations, not the one instance. "Writing any status update for a team," not "my
   Tuesday standup." Be generous with phrasings the user might actually use, because
   under-triggering is the most common way a skill dies unused.

5. **Write down the process.** Turn the judgment into 3–7 concrete steps someone could
   follow without the user present. If a step is "use good taste," that's a sign the
   judgment isn't fully extracted yet — dig until it's explicit.

6. **Draft the skill** using the template below, then hand off. If a dedicated
   skill-creation tool/skill is available (e.g. skill-creator), pass this draft to it
   to formalize, test, and package — that's its job, not yours. Your job is to nail the
   *content*: the trigger, the judgment, and the steps.

### Output template

Produce the draft in this shape so it drops cleanly into a skill file:

```markdown
---
name: <kebab-case-name>
description: <what it does + when to trigger, in the user's own vocabulary;
  lead with the recurring situation that should fire it>
---

# <Title>

## When to use this
<The class of situations. Include the phrasings the user actually says.>

## The judgment this encodes
<The "why" from step 3 — the rule that makes the output right. State it plainly;
explain the reasoning so the model can apply it to cases you didn't foresee.>

## How to do it
1. <step>
2. <step>
...

## Example
Before (typical AI output): <...>
After (corrected): <...>
Why: <the rule, applied>
```

The single most important part is the **judgment** section. Anyone can list steps;
the reason the steps are right is what lets the skill handle novel cases instead of
breaking on anything that isn't the original example.

## Mining a corpus for candidates (Path B)

When the user points you at a body of past work, you're hunting for **repeated
corrections** — the same kind of fix showing up again and again. Hiten Shah's framing:
your skills are already sitting in old docs, Slack threads, customer calls, review
rituals, and onboarding notes. The method is hidden in the work; you're surfacing it.

What to look for:

- **Edits that repeat.** The same rewrite applied to many AI drafts ("always makes the
  intro too long, I always cut it").
- **Re-explanations.** Context the user pastes or restates in chat after chat — that
  standing context is itself a skill.
- **Review rituals.** Checklists people run by hand every time ("did we cite the
  ticket? did we flag the renewal risk?").
- **"Whenever X, do Y" lore.** Tribal knowledge stated in passing in threads.

For each candidate, capture: the recurring correction, how often it shows up (your
evidence), and a one-line guess at the hidden process. Then **rank by frequency ×
leverage** — how often it recurs times how much pain each instance causes — and walk
the top few through Path A. Don't dump fifty half-formed ideas; surface the handful
that are clearly worth it and say why.

If you have tool access to where the work lives (a repo, a notes folder, a connected
Slack/docs MCP), offer to scan it directly and propose candidates rather than making
the user recall them from memory. Put the AI where the work happens.

## What makes a good skill (keep these in mind)

Good skills tend to share three traits — use them as a quality bar for anything you draft:

- **Loaded only when needed.** A sharp, specific trigger so it surfaces in the right
  moment and stays out of the way otherwise. This is why the *when to use* section
  matters as much as the steps.
- **Portable.** Written so it works for anyone/any agent doing this class of work, not
  wired to one person's one example. If it only works on the exact case it was born
  from, you've captured a fix, not a skill.
- **Easy to make and to revise.** Skills are a living system. Ship a tight first
  version, then refine it as new corrections reveal where it's still thin. Don't try to
  make it perfect before it has met a second example.

## When NOT to make a skill

Be honest about this — it's what keeps a skill library valuable instead of cluttered:

- **It didn't actually repeat.** One correction is a fix. Tell the user to wait until
  they've made it a few times; the repetition is the whole signal.
- **The "process" is a single fact.** "It used the wrong company address" is a memory
  item or a config value, not a skill. Skills encode *how to do something*, not a
  static lookup.
- **The model already does it reliably.** If the correction was a one-time model miss
  and it gets it right otherwise, there's nothing to codify.

Surfacing a non-candidate as a non-candidate is a real result, not a failure. The user
asked you to find leverage; telling them where it *isn't* protects their attention.
