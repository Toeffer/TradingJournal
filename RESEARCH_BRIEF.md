# RESEARCH_BRIEF.md — Autonomous Weekly Candidate Research

This file is the instruction set for an **unattended, scheduled research run** (a Claude
Code on the web *Routine*). It turns the manual "Prompt 1" discovery step into something
that runs in the cloud on a cadence and writes a candidate shortlist into this repo —
so the recurring research happens without you.

**Not financial advice.** This produces a *draft shortlist for a human to verify and
judge*. It does not decide trades. Every date and number it outputs must be checked by
you before any decision.

---

## How to set this up (once)

1. Keep this file in your repo (the same one as your journal is fine, or a dedicated
   `trading-research` repo).
2. Go to **claude.ai/code/routines** → New routine. Point it at this repo. Turn on
   **web search**. Set the schedule to **weekly** (e.g. Sunday evening or early Monday,
   your local time).
3. As the routine's prompt, you can simply write:
   > Follow the instructions in RESEARCH_BRIEF.md and produce this week's candidate
   > shortlist, writing the output file exactly as specified.
4. Click **Run now** once to check the output. Fix the CONFIG below if needed. Then
   activate the schedule and leave it.

Each run clones the repo, does the research, and writes the output file on a new branch
(reviewable from the Code tab). You read it; you decide.

---

## CONFIG — edit these to tune the search

```
REGION:                 US-listed common shares
MARKET_CAP_MIN:         500000000        # $500M
MARKET_CAP_MAX:         10000000000      # $10B
MIN_AVG_DOLLAR_VOLUME:  10000000         # $10M average daily $ volume (liquidity floor)
NUM_CANDIDATES:         5                # max to return; fewer is fine (see rules)
CATALYST_WINDOW_DAYS:   28               # catalyst must fall within the next N days
EXCLUDE:                mega-caps, the "Magnificent 7", and obvious headline AI names
SECTOR_FOCUS:           none             # or list sectors to favor / avoid
```

---

## THE TASK (what the routine executes)

You are an experienced swing-trading research analyst running an automated weekly scan.
Use web search and cite recent sources; flag anything older than 2 weeks. Determine
today's date at run time.

GOAL: Produce up to `NUM_CANDIDATES` swing-trade **candidates** — names with a specific,
dated catalyst falling within the next `CATALYST_WINDOW_DAYS` days — for a human to
research further. These are candidates to investigate, not recommendations.

HARD CONSTRAINTS (from CONFIG):
- `REGION` only.
- Market cap between `MARKET_CAP_MIN` and `MARKET_CAP_MAX`.
- Average daily dollar volume above `MIN_AVG_DOLLAR_VOLUME`. Skip illiquid names.
- `EXCLUDE` these. If a name is the first thing a generic list would mention, drop it.
- The catalyst must be SPECIFIC and DATED (earnings on a known date, product launch,
  FDA/regulatory decision, investor day, index rebalance, lockup expiry). "General
  momentum" is not a catalyst.

FOR EACH CANDIDATE, produce:
1. Ticker + one-line company description.
2. Catalyst and its exact date (or date window).
3. Why now — the current price setup in plain language (basing, breakout, pullback).
4. Bull case (3–4 points).
5. Bear case (3–4 points), including downside-gap risk.
6. Invalidation — the level or event that means the idea is wrong.
7. Liquidity note (approx. avg daily dollar volume).
8. Confidence (low/med/high) + one line on what would raise it.
9. `DATE_VERIFIED: NO` — always; the human must confirm the catalyst date.

RULES (important for an unattended run):
- Do NOT pad to hit the number. If you can only find 2 solid, current, specific
  catalysts, return 2 and say so. Fewer good names beats a padded list.
- Cite a recent source for every catalyst date.
- If you cannot verify something, include it but mark it clearly as unverified rather
  than guessing.
- No generic large-caps. No names that fail the constraints.

---

## OUTPUT (write exactly this file)

Create `candidates/CANDIDATES_<YYYY-MM-DD>.md` (today's date) in the repo, with:

```
# Candidate Shortlist — <YYYY-MM-DD>
Generated automatically. DRAFT for human review. Verify all dates/numbers before trading.

## Summary
- <N> candidates found. <one line on overall quality / any data gaps this week>

## Candidates
### 1. <TICKER> — <company>
- Catalyst: <what> on <date>   | DATE_VERIFIED: NO
- Why now: <setup>
- Bull: <...>
- Bear (incl. gap risk): <...>
- Invalidation: <...>
- Liquidity: ~$<X>M ADV
- Confidence: <low/med/high> — <what would raise it>
- Source: <recent citation>

### 2. ...
```

SUCCESS = the output file exists, every candidate meets the CONFIG constraints, every
catalyst has a cited recent source and `DATE_VERIFIED: NO`, and the count is honest
(no padding). If no qualifying candidates exist this week, still create the file and
state that plainly.

---

## Reminders to my future self (the human)

- This is a **draft**. Before acting on any name: verify the catalyst date against a
  real calendar, verify any number against a primary source, and run your Prompt 2
  deep-dive. The routine finds; you decide.
- Quality is capped by free web data on small caps — expect some misses and the
  occasional stale date. That's why DATE_VERIFIED defaults to NO.
- When you want higher reliability, swap the web-search discovery for the data-driven
  screener (see the screener AGENTS.md) and have this routine rank *its* output instead.
