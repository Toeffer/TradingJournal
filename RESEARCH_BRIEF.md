# RESEARCH_BRIEF.md — Autonomous Weekly Candidate Research

This file is the instruction set for an unattended, scheduled research run (a Claude
Code on the web *Routine*). It runs in the cloud on a weekly cadence and writes a
candidate shortlist — now with a per-candidate **risk rating**, **risk-per-share** (and
optional position sizing from your own fixed rule), plus a **deep-dive workup on the top
few front-runners** — into this repo. So the recurring research happens without you.

**Not financial advice.** This produces a *draft for a human to verify and judge*. It
does not decide trades. Every date and number must be checked before any decision. Any
position size it shows is **your own fixed rule applied as arithmetic — not a
recommendation**, and the routine must never invent or change that rule.

---

## Recommended routine settings

- **Model: Opus, high effort.** This is judgment work (filtering, bull/bear reasoning,
  risk rating) that runs only once a week — use the strongest model at full effort.
- Schedule: weekly (e.g. Sunday evening). Web search on. Include your finance connector
  if you've connected one.
- Repository branch/ref: use the `main` branch unless you intentionally test a different
  branch. Do not silently use another branch.

## How to set this up (once)

1. Keep this file in your repo.
2. claude.ai/code/routines -> New routine -> point it at this repo -> web search on.
3. Routine prompt (one line): "Follow the instructions in RESEARCH_BRIEF.md from the main branch of Toeffer/TradingJournal and produce this week's shortlist and deep dives, writing the output file exactly as specified."
4. Run Now once to verify the output, fix the CONFIG below if needed, then activate.

---

## CONFIG — edit these to tune

```
REGION:                   US-listed common shares
MARKET_CAP_MIN:           500000000        # $500M
MARKET_CAP_MAX:           10000000000      # $10B
MIN_AVG_DOLLAR_VOLUME:    25000000         # $25M average daily $ volume (liquidity floor)
PRELIMINARY_SCAN_COUNT:   12               # first pass breadth before filtering down
NUM_CANDIDATES:           5                # max shortlist size; fewer is fine
NUM_DEEP_DIVES:           3                # how many front-runners to deep-dive
CATALYST_WINDOW_DAYS:     28               # catalyst must fall within the next N days
EXCLUDE:                  mega-caps, the "Magnificent 7", obvious headline AI names
SECTOR_FOCUS:             none

# Position sizing (OPTIONAL — your fixed rule). Leave blank to skip suggested sizing.
# If set, the routine computes suggested shares as pure arithmetic from these values.
# NOTE: filling ACCOUNT_SIZE puts that number in your repo — use a PRIVATE repo, or
# leave it blank and just do the one division yourself.
ACCOUNT_SIZE:             <blank>          # e.g. 25000
RISK_PER_TRADE_PCT:       <blank>          # e.g. 1   (risk 1% of the account per trade)
```

If `RISK_RULES.md` exists, read it before interpreting risk, sizing, or portfolio context.
If a relevant rule in `RISK_RULES.md` is blank, do not infer it. Write "risk rule not set."

---

## Source quality and bias controls

Use web search (and the finance connector if available). Determine today's date at run
time. Prefer recent sources and flag anything older than 2 weeks.

Source priority:
1. Company investor relations, SEC filings, exchange notices, official index/event
   calendars, and other primary sources.
2. Reputable financial news and data providers.
3. Analyst notes, blogs, newsletters, forums, and social sources only as secondary context.

Every catalyst must have at least one primary or high-quality source. If the catalyst is
not verifiable from a primary or high-quality source, reject the candidate.

Bias-control pass:
- First build a broad preliminary list of up to `PRELIMINARY_SCAN_COUNT` candidates.
- Then run a skeptical pass that tries to disqualify each candidate.
- For every surviving candidate, explicitly ask: "What would make this already priced in?"
- Reject candidates mainly driven by social/news hype rather than a dated catalyst.
- Remove any candidate where the bear case is stronger than the bull case.
- Do not select exciting/high-upside names over cleaner reward-to-risk names.

A sparse report is better than a stretched report. If fewer than 3 high-quality candidates
qualify, say so. A "no strong candidates this week" output is a successful output.

---

## STAGE 1 — Weekly scan + risk rating

You are an experienced swing-trading research analyst running an automated weekly scan.

**Methodology skills:** Apply the screening methodology from the `idea-generation` skill
(`.claude/skills/idea-generation/SKILL.md`) to structure the quantitative and thematic
sweep. Use the `catalyst-calendar` skill (`.claude/skills/catalyst-calendar/SKILL.md`)
to find, categorize, and validate catalyst dates across the coverage universe. These
skills define the workflow — adapt their frameworks to the CONFIG constraints below.

GOAL: up to `NUM_CANDIDATES` swing-trade **candidates** with a specific, dated catalyst
within the next `CATALYST_WINDOW_DAYS` days, for a human to research further.

HARD CONSTRAINTS (from CONFIG): `REGION` only; market cap within range; average daily
dollar volume above `MIN_AVG_DOLLAR_VOLUME`; `EXCLUDE` the named groups; the catalyst
must be SPECIFIC and DATED. "General momentum" is not a catalyst. Do NOT pad — fewer
good names beats a padded list; if you find only 2, return 2 and say so.

FOR EACH CANDIDATE, produce:
1. Ticker + one-line company description.
2. Catalyst + exact date/window.   | DATE_VERIFIED: NO
3. Why now — the current setup in plain language (basing, breakout, pullback).
4. Bull case (brief) and bear case (brief, including downside-gap risk).
5. Priced-in check — why the catalyst may already be reflected in the price.
6. Invalidation — the level or event that means the idea is wrong.
7. Liquidity note (approx. average daily dollar volume).
8. **Risk rating — Low / Medium / High**, with one short reason per factor. Push toward
   HIGHER risk when these apply, LOWER when they don't:
   - Liquidity: dollar volume near/below the floor; wide spread.
   - Event type: a binary event held *through* (earnings, FDA, ruling) vs a drift or
     structural catalyst (index inclusion, already-reported drift). Binary = higher.
   - Volatility: large historical moves on past catalysts (e.g. frequent +/-15% gaps).
   - Float / short: very low float or high short interest (violent moves either way).
   - Setup: weak reward-to-risk, or no clear invalidation level.
   - Data: thin coverage or unverified / low-confidence catalyst info.
   State plainly that this is a caution gauge from imperfect data, not a precise score.
   Higher risk means size smaller or skip — NEVER size up.
9. **Risk per share** = entry - stop (absolute, per share). Always show this.
10. **Suggested size** — ONLY if `ACCOUNT_SIZE` and `RISK_PER_TRADE_PCT` are both set:
    suggested_shares = floor( (ACCOUNT_SIZE * RISK_PER_TRADE_PCT / 100) / risk_per_share )
    Show the arithmetic. If either is blank, write the formula and "set your rule in
    CONFIG to get a suggested size." Use ONLY the CONFIG values — never invent or adjust
    the risk %, the account size, or the suggested size. This is arithmetic, not judgment.
11. Confidence (low/med/high) + one line on what would raise it. Cite a recent source.

Also include a short **Rejected Candidates** section with 3-5 names that looked promising
but were rejected, plus the exact reason: no dated catalyst, too illiquid, catalyst already
priced in, binary gap risk too high, unclear invalidation, weak source quality, or another
specific failure.

---

## STAGE 2 — Deep-dive the front-runners

SELECT the top `NUM_DEEP_DIVES` candidates by **setup quality, confidence, and
reward-to-risk — NOT by raw upside or excitement**. When two are close, prefer the
LOWER risk rating. (Deepen the most tradeable names, not the most dangerous.)

**Methodology skills:** Run each front-runner through the `earnings-preview` skill
(`.claude/skills/earnings-preview/SKILL.md`) to build consensus estimates, key-metrics
frameworks, and bull/base/bear scenarios. If the candidate's catalyst is a *past* earnings
report and the trade is a post-earnings drift, also apply the `earnings-analysis` skill
(`.claude/skills/earnings-analysis/SKILL.md`) to assess the reported results. These skills
provide the analytical structure — feed their output into the workup format below.

For EACH selected front-runner, write a fuller workup:
- **Catalyst mechanics:** what happens, when, and crucially **what the market already
  expects** (consensus / what is priced in) — so we don't chase something already in the
  price.
- **Bull case** — 3-4 specific points.
- **Bear case** — 3-4 specific points, including downside-gap risk.
- **Key levels:** support, resistance, and the invalidation level.
- **Main risk** specific to this name.
- **Pre-mortem:** assume this trade lost money a month from now — the single most likely
  reason, and what I would have ignored.
- Carry over the **risk rating, risk-per-share, and suggested size** from Stage 1.
- Cite recent sources. DATE_VERIFIED: NO.

---

## OUTPUT — write exactly this file

Create `research/candidates-<YYYY-MM-DD>.md` (today's date), structured as:

```
# Candidate Shortlist — <YYYY-MM-DD>
DRAFT for human review. Verify all dates/numbers before trading.
Any size shown is YOUR fixed rule as arithmetic, not a recommendation.

## Summary
- <N> candidates, <M> deep-dived. <one line on overall quality / data gaps this week>

## Shortlist
### 1. <TICKER> — <company>
- Catalyst: <what> on <date>   | DATE_VERIFIED: NO
- Why now: <setup>
- Bull / Bear: <brief> / <brief, incl. gap risk>
- Priced-in check: <why this may already be reflected in price>
- Invalidation: <level/event>
- Liquidity: ~$<X>M ADV
- Risk: <Low/Med/High> — <factor reasons>
- Risk/share: <entry - stop>   | Suggested size: <shares, or "set rule in CONFIG">
- Confidence: <low/med/high> — <what would raise it>
- Source: <recent citation>
### 2. ...

## Rejected Candidates
- <TICKER> — rejected because <specific reason>

## Deep Dives (top <M> front-runners)
### <TICKER> — <company>
- Catalyst mechanics & what's priced in: ...
- Bull: ...
- Bear (incl. gap risk): ...
- Key levels (support / resistance / invalidation): ...
- Main risk: ...
- Pre-mortem: ...
- Risk: <...>  | Risk/share: <...>  | Suggested size: <...>
- Sources: <...>   | DATE_VERIFIED: NO
```

SUCCESS = the file exists at `research/candidates-<YYYY-MM-DD>.md`; every candidate meets
CONFIG; every catalyst has a cited recent source and DATE_VERIFIED: NO; risk rating and
risk-per-share are present for all; suggested size appears only if the CONFIG rule is set;
the top `NUM_DEEP_DIVES` names are deep-dived; rejected candidates are included; counts are
honest (no padding). If nothing qualifies this week, still create the file and say so.

---

## Reminders to my future self (the human)

- This is a **draft**. Before acting: verify the catalyst date against a real calendar,
  verify numbers against a primary source, and re-read the deep-dive bear case and
  pre-mortem.
- The **risk rating** is a caution gauge from imperfect data — use it to size down or
  skip, not as a precise measurement.
- Any **suggested size** is your own fixed rule done as arithmetic. The size decision
  belongs to you and your rule — never the model.
- The **deep dive teaches the bear case** you might not think of — that's its main value
  while you're still building expertise. Read it before you look at the upside.
- For higher reliability later, feed Stage 1 the data-driven screener (see the screener
  AGENTS.md) and have this routine rank *its* output. And log what you trade in the
  journal, so you can check whether the risk rating and the routine's picks actually
  predict anything.
