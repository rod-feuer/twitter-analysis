# twitter-analysis

Pulls your X/Twitter bookmarks (including **Twitter Articles**, the rich long-form post type) into a local corpus of Markdown + JSON files for re-reading and LLM analysis.

Uses the official X API on the pay-as-you-go tier (~$0.001 per bookmark fetched, no subscription). Returns the 800 most recent bookmarks — that's the API ceiling.

## One-time setup

### 1. Create an X developer app

1. Go to [console.x.com](https://console.x.com), sign in, accept developer terms.
2. Create a project + app. Copy the **Client ID** and **Client Secret**.
3. In **User authentication settings**:
   - App permissions: **Read**
   - Type of App: **Confidential client** (Web App)
   - Callback URL: `http://127.0.0.1:8765/callback`
   - Website URL: anything (e.g. `https://example.com`)
4. In the developer console, **load credits** (start with $5).

### 2. Configure the project

```bash
cd /Users/rodfeuer/claude-projects/twitter-analysis
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Edit `.env` and fill in `X_CLIENT_ID` and `X_CLIENT_SECRET` from step 1. Leave `X_USER_ID` and `X_REFRESH_TOKEN` empty — the authorize step fills them in.

### 3. Authorize

```bash
twitter-analysis authorize
```

Opens a browser to X. After you click Authorize, the script captures the redirect, exchanges the code for tokens, and writes `X_REFRESH_TOKEN` (and `X_USER_ID`) to `.env`.

## Usage

```bash
twitter-analysis sync             # fetch new bookmarks, then auto-categorize
twitter-analysis sync --full      # ignore state.json, refetch all 800
twitter-analysis sync --no-categorize  # skip the auto-categorize step
twitter-analysis categorize       # classify any unlabeled bookmarks (idempotent)
```

Output lands in `bookmarks/`:
- `<tweet_id>.json` — full raw record (source of truth)
- `<tweet_id>.md` — rendered for reading / LLM consumption
- `_categories.json` — index of `tweet_id → {category, confidence, reasoning}` from the categorize step

State (highest bookmark ID seen) is persisted to `state.json` so incremental runs only fetch new ones.

## Auto-categorization

After each sync, new bookmarks are classified against a fixed 10-category taxonomy (A–J, defined in [`src/twitter_analysis/categorize.py`](src/twitter_analysis/categorize.py) and derived from [`analysis/bookmarks-report.md`](analysis/bookmarks-report.md)) using Claude Haiku 4.5. Labels go to `bookmarks/_categories.json`.

Requires `ANTHROPIC_API_KEY` in the environment. If it's missing, sync still succeeds and categorization is skipped with a warning. Cost: ~$0.0008 per bookmark (~$0.08 for a full 99-item backfill, cents/day after that).

Run `twitter-analysis categorize` standalone to backfill or pick up after a missed sync — it skips bookmarks already in the index.

## Evaluating skills (does a skill actually work?)

A "skill" is a short, reusable instruction that tells a model how to handle a class of
problem. The question that matters is whether loading it actually *changes the model's answer* —
a skill that doesn't move the output isn't a skill, it's decoration.

[`skills/eval_skill.py`](skills/eval_skill.py) measures that directly. For each eval prompt it
answers the question twice — once with the skill loaded, once without — and a judge model
scores each answer against a rubric. The result is the **delta**: how far the skill moved the
model. No grades are hardcoded; the scoring runs live.

```bash
export ANTHROPIC_API_KEY=...        # or put it in .env
python skills/eval_skill.py --skill skills/bias-to-impact/SKILL.md --evals skills/evals/example.jsonl
```

Each eval line is `{"prompt": "...", "rubric": "what a shifted/good answer contains"}`
(see [`skills/evals/example.jsonl`](skills/evals/example.jsonl)).

The pattern worth knowing: skills that teach the model a general *disposition* ("steelman the
other side," "reason from first principles") tend to move it ~0 — it already runs those by
default. Skills that inject a specific, non-default *conclusion* are the ones that move it.
Caveat: a small, single-model, single-run, judge-scored test is an illustration of the method,
not a benchmark of record — raise the item count and run multiple trials before trusting a
specific number.

## Scheduling daily sync via launchd

Create `~/Library/LaunchAgents/com.rodfeuer.twitter-analysis.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rodfeuer.twitter-analysis</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/rodfeuer/claude-projects/twitter-analysis/.venv/bin/twitter-analysis</string>
        <string>sync</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/rodfeuer/claude-projects/twitter-analysis</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>8</integer>
        <key>Minute</key><integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/rodfeuer/claude-projects/twitter-analysis/sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/rodfeuer/claude-projects/twitter-analysis/sync.log</string>
</dict>
</plist>
```

Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.rodfeuer.twitter-analysis.plist
launchctl kickstart -k gui/$(id -u)/com.rodfeuer.twitter-analysis  # force a run now
```

## Limits & gotchas

- **800-bookmark cap** is X-side. Older bookmarks aren't reachable via the API.
- **Refresh token rotation**: each token exchange issues a new refresh token; the script writes it back to `.env` before doing anything else.
- **Article schema**: the `article` field shape isn't well-documented. The renderer tries common shapes and falls back to dumping the raw payload in a code block — the JSON sidecar always preserves the full record so you can re-render later.
- **Cost**: ~$0.001 per bookmark fetched. First full sync of 800 bookmarks ≈ $0.80. Subsequent incremental runs are cents.
