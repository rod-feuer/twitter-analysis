#!/usr/bin/env bash
# Causal second-pass Stop hook (project-level).
# If the final assistant turn contains causal-attribution language, re-inject a
# forced self-refutation pass. Loop-guarded; silent when nothing matches.
# Disable: remove the Stop hook from .claude/settings.json, or run /hooks.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

# Loop guard — never re-block our own re-block.
active=$(printf '%s' "$input" | jq -r '.stop_hook_active // false' 2>/dev/null)
[ "$active" = "true" ] && exit 0

transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null)
[ -z "$transcript" ] && exit 0
[ ! -f "$transcript" ] && exit 0

# Text of the final assistant turn (concatenate its text blocks).
last=$(jq -rs '
  [ .[] | select((.type? == "assistant") or (.message.role? == "assistant")) ] | last
  | ((.message.content // .content // [])
     | if type == "array" then ([ .[] | select(.type? == "text") | .text ] | join("\n"))
       elif type == "string" then .
       else "" end)
' "$transcript" 2>/dev/null)
[ -z "$last" ] && exit 0

# Causal-attribution markers (case-insensitive). Tightened to skip bare "because".
pattern='caused|\bdrove\b|driven by|\bled to\b|\bdue to\b|because of|resulted in|results? in|thanks to|attribut|\bcausal\b|gave rise to|brought about'
printf '%s' "$last" | grep -iqE "$pattern" || exit 0

reason='Causal-claim check (automatic second pass). Your last response asserts at least one cause->effect relationship. Before finishing, audit ONLY the load-bearing causal claim(s):
1. Counterfactual - what happens to the outcome WITHOUT the asserted cause?
2. Confounder - the single most plausible alternative explanation you have not ruled out.
3. Verdict - IDENTIFIED, or only CONSISTENT-WITH the evidence?
Then: if the audit changes the claim, correct it; if it survives, say so in one line. If the causal language was incidental and nothing rides on it, reply exactly: "Causal check: clean." Returning clean is a valid, expected outcome - do NOT manufacture doubt to perform rigor.
Finally, if you audited a real claim, end the reply with a clean, self-contained "Bottom line:" - 2 to 4 sentences (or tight bullets) giving the corrected takeaway a reader could act on WITHOUT reading the audit mechanics. Skip the summary only if you returned "clean."'

jq -n --arg r "$reason" '{decision:"block", reason:$r}'
exit 0
