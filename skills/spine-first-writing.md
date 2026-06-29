# Skill brief: Spine-First Writing (kernel → spine → prose → flourish)

_Hand-authored from a real editing session (a LinkedIn draft + the prompts that
improved it), not auto-generated from an author corpus. Hand this file to the
**skill-creator** skill to build the skill. Review first — confirm it clears the
install bar (does it inject a move the model doesn't already default to?)._

## Core idea
Don't edit a draft — find its spine first, then rebuild on it. Most writing help
fails because it polishes prose that sits on the wrong central concept. The fix is a
strict order that never folds the stages together:

1. **Kernel** — the basic *lived-experience* thing underneath the draft (a feeling or
   moment, not a thesis). "I just spent a weekend bottling expertise and I'm afraid the
   machine already knows all of it" is a kernel; "AI commoditizes knowledge" is not.
2. **Spine** — the single central concept the piece will carry. Reached by laddering the
   kernel down with **5 Whys** until it lands on *why it matters to this author
   specifically* — that's what makes a piece only-they-could-write-it instead of generic.
3. **Prose** — rebuild the whole piece on the chosen spine. Don't patch the old draft.
4. **Flourish pass** — only last, and only after the spine is locked, hunt and cut
   showy language by *category*, leaving close calls flagged for the author.

**The load-bearing move — the one that clears the "non-default" bar:**
- **5 Whys to excavate the lived kernel** — the engine for non-commoditized writing. It
  converts an interesting *topic* into the author's actual nerve, then a spine to rebuild
  on. Stop at the place that lands on *them*. A 4-item eval probe (n=4, single run —
  illustrative, not a benchmark) put this move at the top: on a generic listicle the model
  scored 0.10 baseline → 0.85 with the skill (+0.75), and the copywriting panel didn't move
  it at all (0.10 → 0.10). This is where the alpha is. An **ablation** then isolated it: a
  *kernel-only* instruction reproduced the lift (+0.85), a length-matched *generic editing
  framework* did nothing (0.10 → 0.10, = baseline), and the lift survived a *blind* rubric
  written by an editor who never saw the skill (+0.67). So it's the kernel content
  specifically — not generic-framework priming and not a self-authored rubric.
  **Generalized:** rerun on 5 fresh kernel-type drafts (founder lessons, gratitude,
  failure, sales career, burnout) with a *cross-model* judge — Sonnet answers, Opus scores —
  held up 5/5 positive, mean +0.39. So it's not a single-item or shared-judge fluke.
  Remaining caveats: single run per item, drafts authored by me (rubrics were blind),
  judge still Claude-family (not cross-vendor).

**A useful move, but NOT load-bearing — the model mostly does it already:**
- **Make the piece obey its own logic** — catch the spot where the writing violates the
  thing it argues (e.g. a draft that preaches plain writing while leaning on vague
  absolutes). Worth doing, but in the same probe a capable baseline already caught the
  self-contradiction (~0.90) and the skill didn't improve it. Keep it as an edit step;
  don't sell it as the skill's edge. Its real value is *direction*: demote the absolute
  toward the quieter **true** claim the argument supports — not (as a conversion-optimized
  editor would) toward the punchiest *sellable* claim.

## How to apply
1. **Name the kernel in one sentence.** What's the felt thing under this draft? If you
   can't state it, the author isn't ready to write the piece — say so.
2. **Run 5 Whys, downward not outward.** Each "why" should drive toward why it lands on
   *this person*, not explain the subject. Why #5 is usually where the spine lives.
3. **Offer three competing spines, not edits.** Three different *central concepts*, each
   a different post. Let the author pick the one truest to what they actually went
   through, then commit to it. (Give a short rationale per spine: most-narrative,
   most-zoomed-out, most-about-character, etc.)
4. **Rebuild on the chosen spine.** Keep the raw material, re-spine it so the kernel
   carries the piece instead of the structure/taxonomy doing the work. Crest the piece on
   the kernel — give the single most-alive beat its own line.
5. **Self-consistency check (do this before line-editing).** Find any sentence that
   violates the piece's own thesis and fix it first. Demote every overconfident headline
   ("only," "always," "the single most powerful") to the quieter claim hiding underneath
   that actually survives scrutiny — the softer version is usually truer *and* stronger.
6. **Flourish pass, last.** Cut by category, not one-offs: warm-up tics that announce a
   surprise instead of delivering it ("Here's the thing:", "Here's the part that threw
   me"); metaphors that stage a scene for effect ("from where the machine is standing");
   structural punctuation overused (em-dashes around a name list → parentheses). Keep
   punch, cut decoration, and flag the genuine close calls for the author to call rather
   than deciding for them.

## Grounding — the session this was extracted from
A friend improved "LinkedIn Post #1" with a sequence of prompts. The moves that worked,
in order:
- **Kernel before structure:** _"try to get at the basic lived-experience kernel
  underneath this to arrive at the central concept a la Steven Pressfield."_ The answer
  was an emotion (the fear the machine already knows everything), not a thesis.
- **5 Whys to the nerve:** the whys laddered from "why build the test" down to "the nerve
  to hold a sound-but-uncited call is the one move the machine structurally can't make" —
  which is also exactly why the experts were worth bottling. That became the spine.
- **Three spines to choose from:** "early looks like wrong" / "it commoditized knowing,
  not judgment" / "conviction without citation" — same raw material, three central
  concepts, author picks.
- **Obey-your-own-logic edit:** the author's own one-line summary of the work — "real
  alpha can *only* come from humans" — was, *by the post's own taxonomy*, an overconfident
  "Pile 2" headline. The edit demoted it to the quieter surviving claim ("the alpha that's left
  comes from people, at least for now") so the post practiced what it preached. (Note:
  the eval probe found this catch is *not* a non-default move — a capable model already
  does it. The value is the demote-toward-true direction, not the catch itself.)
- **Flourish pass by category:** cut "Here's the part that threw me" (warm-up tic),
  "from where the machine is standing" (showy spatial framing → "identical to the
  machine"), and flagged em-dashes-around-a-name-list as the author's call.

## Relationship to `copywriting-panel-eval` (tested, with one corrected claim)
The two are **complementary, not rival** — different layer, different objective:
- **Layer:** the copywriting panel sharpens the *words* given the concept; spine-first
  works the *concept* upstream of the words.
- **Objective:** the panel optimizes *conversion* (make them act); spine-first optimizes
  *truth + author-specific resonance* (make it the realest thing only this person could say).
- **Chain:** spine-first → copywriting panel (get the concept right, then make the words
  convert) — one layer further upstream than `pmm-panel-eval → copywriting-panel-eval`.

A claim I made and the probe **falsified, recorded so it isn't repeated:** I predicted the
conversion-optimized panel would push an overconfident headline *more* absolute and *miss*
the self-contradiction. Both wrong — Hopkins bans vague superlatives, so the panel
*softened* the absolute and *caught* the contradiction. The distinction that survives is
**destination, not direction**: both demote the absolute, but the panel rewrites toward a
*sellable, concrete* claim while spine-first rewrites toward the quieter *true* claim the
argument supports. On the probe's spine-first-objective rubrics the panel scored net
negative (mean −0.225) and over-triggered on the release-note guard — expected, since it's
optimizing a different thing, not failing.

_Eval caveat: all numbers above are from a 4-item, single-run, judge-scored probe
(`spine-first-writing.evals.jsonl`). Same-condition baselines varied ~0.30 run to run, so
treat single-item deltas as directional and don't quote any figure as a benchmark of record._

## When NOT to use / limits
- **Not for utilitarian text.** Docs, specs, release notes, transactional email — there's
  no lived kernel to find; spine-hunting is overhead. This is for persuasive/personal
  writing (posts, essays, narrative copy, talks).
- **Don't manufacture a kernel.** If the draft genuinely has no felt center, the honest
  output is "this is a topic, not a piece yet" — not a forced Pressfield spine. **This
  guard is load-bearing, not decorative:** in the ablation, the kernel instruction
  *stripped of this limit* over-triggered on a release note and cratered it (−0.60), while
  the full skill (limit intact) improved it (+0.30). Ship the kernel move only with its
  guardrail.
- **The author owns the call.** Offer spines and flag close calls; don't decide voice or
  the final "only vs. the softer claim" punch for them.

## Suggested skill name
`spine-first-writing` (alt: `kernel-before-prose`, `find-the-spine`)
