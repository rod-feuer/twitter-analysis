---
name: spine-first-writing
description: >-
  Improve a piece of persuasive or personal writing — a post, essay, narrative, talk,
  bio, or story-driven copy — by finding the lived-experience KERNEL underneath the draft
  and rebuilding on a spine BEFORE editing prose. Use whenever asked to "improve / sharpen /
  punch up / make better" a draft post or essay, when a draft reads generic, listicle-y,
  or like platitudes ("3 lessons I learned", "gratitude changed my life"), or when someone
  wants their writing to feel personal, specific, or "only-I-could-have-written-this".
  The high-value move is to go underneath the topic to the real felt moment and rebuild
  around it — not to tighten sentences. Do NOT use for utilitarian text (docs, specs,
  release notes, transactional email): there's no kernel to find and forcing one harms it.
---

# Spine-First Writing

## The idea behind this skill

The reflexive way to "improve" a draft is to polish its prose — tighten sentences, add a
hook, cut adverbs. That optimizes the wrong layer. Most weak persuasive/personal writing
fails one level up: it sits on a generic *topic* ("failure is the best teacher") instead of
a specific *lived kernel* ("the moment my co-founder quit and I refreshed the bank balance
twice"). No amount of line-editing fixes that — you have to find the kernel and rebuild on it.

The one move that does the work is **excavating the lived kernel**: the basic felt thing
underneath the draft (a moment or feeling, not a thesis), laddered down until it lands on why
this matters to *this* author specifically — the thing that makes it only-they-could-write-it.
Then you choose a central concept (the "spine") and rebuild around it, instead of polishing
the structure the draft already has.

*Why this move and not the others: it's the part a capable model doesn't already do. In a
baseline-vs-skill eval, a generic listicle scored 0.10 without the skill and 0.85 with it; an
ablation showed the kernel instruction alone reproduced the lift while a length-matched generic
editing framework did nothing, and it held 5/5 on fresh drafts under a cross-model judge. The
other moves below (catching self-contradiction, sharpening prose) are worth doing but a good
model — or plain editing — already does them; don't treat them as the edge.*

## When you're invoked

Someone hands you a draft (or a topic) and wants it stronger, sharper, more personal, or
"better." The job is **not** to start editing sentences. It's to find the kernel first, then
rebuild — and, if the text has no kernel, to say so rather than manufacture one.

## The method

1. **Name the kernel in one sentence.** What's the felt thing under this draft — the specific
   moment or emotion? If you genuinely can't state one, stop: this is a topic, not a piece yet,
   or it's utilitarian text (see limits). Say that instead of forcing it.

2. **Run 5 Whys — downward, not outward.** Each "why" drives toward *why it lands on this
   person*, not toward explaining the subject. Stop at the nerve — usually around why #5. That's
   where the spine lives.

3. **Offer two or three competing spines, not edits.** Each is a different *central concept* —
   a different piece — with a one-line rationale (most-narrative / most-zoomed-out /
   most-about-character). Let the author pick the one truest to what they actually went through.
   Don't decide it for them.

4. **Rebuild on the chosen spine.** Keep the raw material; re-spine it so the kernel carries the
   piece instead of the structure doing the work. Give the single most-alive beat its own line.

5. **Then, and only then, two light edit passes** (useful, not the edge):
   - **Self-consistency:** fix any sentence that violates the piece's own thesis; demote
     overconfident absolutes ("only", "always", "the single most powerful") to the quieter claim
     that actually survives — the truer version is usually stronger too.
   - **Flourish:** cut by category — warm-up tics that announce a surprise instead of delivering
     it ("Here's the thing:"), metaphors that stage a scene for effect, punctuation overused.
     Keep punch, flag genuine close calls for the author.

## When NOT to use / limits

- **Not for utilitarian text** — docs, specs, release notes, transactional email. There's no
  lived kernel; spine-hunting is overhead.
- **Don't manufacture a kernel. This guard is load-bearing, not decorative.** In the ablation,
  the kernel move *stripped of this limit* over-triggered on a release note and made it worse
  (−0.60) where the full skill, limit intact, improved it (+0.30). If the draft has no felt
  center, the honest output is "this is a topic, not a piece yet" — not a forced Pressfield spine.
- **The author owns the call.** Offer spines, flag close calls; don't decide voice or the final
  "loud vs. quiet claim" punch for them.

## Output format

```markdown
## The kernel
[one sentence — the felt thing under the draft; or: "no kernel here, this is a topic/utilitarian — say why"]

## 5 Whys → the nerve
[the ladder, ending where it lands on this author specifically]

## Three spines (pick one)
[2–3 competing central concepts, each with a one-line rationale]

## Rebuild
[the piece rebuilt on the chosen spine — or, if no spine was chosen yet, a draft on the strongest one, marked as such]

## Edit passes
[self-consistency fixes + flourish cuts, with close calls flagged for the author]
```

## How we know (provenance)

Extracted from a real editing session (a LinkedIn draft + the prompts that improved it) and
pressure-tested with `eval_skill.py`: see [`../spine-first-writing.md`](../spine-first-writing.md)
for the full brief and the eval/ablation record. Headline result: the kernel move is the
load-bearing, non-default edge; the rest is good craft a capable model already runs.
