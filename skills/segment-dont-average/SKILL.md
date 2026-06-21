---
name: segment-dont-average
description: >-
  Replace averages and blanket claims with segmented statements, because most
  real-world data is bimodal/multi-modal and an average describes nobody. Use whenever
  someone reasons from an average or a single aggregate stat ("our conversion rate is
  X," "average order value," "NPS is Y"), makes a one-size-fits-all claim about
  "users / customers / the team / people," designs strategy for "the customer," or
  draws a conclusion from a mean before looking at the distribution. Trigger even when
  the average looks like a reasonable summary — the move (ask "which group, under what
  conditions?" and check for bimodality) routinely flips the decision.
---

# Segment, Don't Average

## The idea behind this skill

An average is usually a smoothie: pour in distinct segments, blend, and you get a
number that *"accurately describes nobody and nothing."* Evan Lapointe's claim is
strong on purpose: *"Your average conversion rates, average cart sizes, average
anything are all garbage data points. You should literally never use the word 'average'
in your business."* The reason is statistical, not stylistic — most real data is
**bimodal or multi-modal**, and for such data *"the average is, in fact, a complete
inaccuracy."* Your business doesn't have an average customer; it has **segments and
clusters.**

The upgrade is segmentation, and it applies far beyond data — to advice, strategy,
hiring, culture, and feedback. Evan's shortcut for sounding (and being) smarter than
almost everyone: *"Segment everything you say. 'For this group, X happens. For this
other group, Y happens.' Never again: 'For people, this happens.'"* Compare *"US
employee engagement is 67%"* to *"for companies with great culture it's >90%, for the
rest it dips below 60%"* — the second is a smarter, more actionable statement. And
there's *always* a small group doing better than the majority; **that** is what to
surface.

## When you're invoked

Someone is reasoning from a blended number or a homogeneous claim — an average metric,
"our users do X," "the team is too slow," a strategy for "the customer." Your job is to
break the blend back into its real segments before any conclusion or decision is drawn.

## The method

1. **Replace the average with quartiles/segments.** Swap *"the average is X"* for
   *"the top quartile does X, the bottom quartile does Y."* Same data, a statement that
   actually describes real groups.

2. **For any claim about people/outcomes, ask "which ones, under what conditions?"**
   *"Customers don't use this"* → *which* customers? *"The team isn't fast enough"* →
   which people, on which work, under which conditions? The qualifier is where the real
   insight (and the right action) lives.

3. **Look at the distribution before the central tendency.** Plot it; check for
   bimodality/multimodality. If there are two or more clusters, the mean is between
   them describing no one — and any decision based on it is aimed at a fiction.

4. **Find and highlight the high-performing cluster.** There's almost always a segment
   doing markedly better. *That's the signal* — what are they doing, and can it spread?
   The average buries exactly the thing worth learning from.

5. **Design and advise for a specific segment, not "the customer."** Strategy aimed at
   the blended average fits nobody. Name the segment whose behavior you're designing
   for. When consuming advice, ask *"which type of person/company/condition does this
   apply to?"* — unsegmented advice is a smoothie too.

## Output

De-average, then re-segment toward the decision. Use this shape:

```markdown
## The average is hiding something
[why the blended number/claim likely masks distinct segments here — name the suspected
clusters]

## Segment it
[the claim restated by segment: "for group A… for group B…"; what to actually plot/pull]

## Where the signal is
[the high/low-performing cluster that matters, and the decision it changes]
```

## Limits — don't turn this into a tic

The goal is accuracy, not banning a word reflexively:

- **Sometimes a single number is genuinely fine.** For truly unimodal, low-variance
  data, the mean is a fair summary — and some contexts (a board headline, a tracked
  KPI, a quick gut-check) legitimately need one number. The discipline is to *check the
  distribution first* and pair the number with its segments, not to refuse to ever
  summarize.
- **Don't over-segment into noise.** Slice far enough and every segment has an n of 3
  and no signal. Segment to the point where the clusters are real and decision-relevant,
  then stop. More cuts past that is false precision.
- **Segment toward a decision.** Segmentation that doesn't change what you'd do is
  trivia. Always tie it back to the action the segments imply.
