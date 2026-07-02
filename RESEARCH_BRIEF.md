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
- If the scanner workflow is active, read the latest `research/scans/scan-*.md` and
  `data/scanner_signals.csv` before Stage 1. Treat scanner names as candidates to verify,
  not as pre-approved ideas.

## How to set this up (once)

1. Keep this file in your repo.
2. claude.ai/code/routines -> New routine -> point it at this repo -> web search on.
3. Routine prompt (one line): "Follow the instructions in RESEARCH_BRIEF.md from the main branch of Toeffer/TradingJournal and produce this week's shortlist and deep dives, writing the output file exactly as specified. If scanner output exists, use the newest research/scans/scan-*.md as one input source, but still verify every candidate independently."
4. Run Now once to verify the output, fix the CONFIG below if needed, then activate.

---

## CONFIG — edit these to tune

```
REGION:                   US-listed common shares + XETRA (Frankfurt) listed shares.
                          # XETRA names trade in EUR (no FX for the EUR account).
                          # LSE only case-by-case: +0.5% UK stamp duty per buy and GBP
                          # exposure must be named in the candidate's risk factors.
MARKET_CAP_MIN:           500000000        # $500M
MARKET_CAP_MAX:           10000000000      # $10B
MIN_AVG_DOLLAR_VOLUME:    25000000         # $25M average daily $ volume (liquidity floor)
PRELIMINARY_SCAN_COUNT:   12               # first pass breadth before filtering down
NUM_CANDIDATES:           5                # max shortlist size; fewer is fine
NUM_DEEP_DIVES:           3                # how many front-runners to deep-dive
CATALYST_WINDOW_DAYS:     42               # catalyst must fall within the next N days
EXCLUDE:                  mega-caps, the "Magnificent 7", obvious headline AI names
SECTOR_FOCUS:             none
MAX_EARNINGS_CANDIDATES:  2                # max candidates with earnings as primary catalyst

# Optional scanner input — data-driven anomaly detector, not a signal engine.
USE_SCANNER_OUTPUT:        yes              # read latest research/scans/scan-*.md if present
SCANNER_MIN_SCORE:         70               # prioritize scanner candidates at/above this score
SCANNER_LOOKBACK_DAYS:     7                # only consider recent scanner reports
MAX_SCANNER_CANDIDATES:    5                # max names from scanner to carry into verification

# Position sizing — FIXED €150 per trade (learning phase).
# The routine should note this as context but cannot change the rule.
# When graduating to %-based sizing, replace with ACCOUNT_SIZE and RISK_PER_TRADE_PCT.
FIXED_POSITION_SIZE:      150              # €150 per trade
ACCOUNT_SIZE:             <blank>          # not used during learning phase
RISK_PER_TRADE_PCT:       <blank>          # not used during learning phase
```

If `RISK_RULES.md` exists, read it before interpreting risk, sizing, or portfolio context.
If a relevant rule in `RISK_RULES.md` is blank, do not infer it. Write "risk rule not set."

`ETORO_TRADEABILITY.md` is the broker/universe authority: where it conflicts with the
CONFIG above (tradeability, market-cap exceptions, liquidity tiers), the overlay wins.

---

## Source quality and bias controls

Use web search (and the finance connector if available). Determine today's date at run
time. Prefer recent sources and flag anything older than 2 weeks.

Source priority:
1. Company investor relations, SEC filings, exchange notices, official index/event
   calendars, and other primary sources.
2. Reputable financial news and data providers.
3. Data-driven scanner output (`research/scans/` and `data/scanner_signals.csv`) as a
   discovery input only, never as proof.
4. Analyst notes, blogs, newsletters, forums, and social sources only as secondary context.

Every catalyst must have at least one primary or high-quality source. If the catalyst is
not verifiable from a primary or high-quality source, reject the candidate.

Bias-control pass:
- First build a broad preliminary list of up to `PRELIMINARY_SCAN_COUNT` candidates.
- If `USE_SCANNER_OUTPUT` is yes and scanner files exist, include the strongest recent
  scanner candidates in the preliminary list, but still verify them from scratch.
- Then run a skeptical pass that tries to disqualify each candidate.
- For every surviving candidate, explicitly ask: "What would make this already priced in?"
- Reject candidates mainly driven by social/news hype rather than a dated catalyst.
- Reject scanner names where the only reason is "it moved" and no current catalyst,
  sector sympathy, or clean invalidation can be found.
- Remove any candidate where the bear case is stronger than the bull case.
- Do not select exciting/high-upside names over cleaner reward-to-risk names.

A sparse report is better than a stretched report. If fewer than 3 high-quality candidates
qualify, say so. A "no strong candidates this week" output is a successful output.

---

## Optional scanner input pass

Before Stage 1, do this if scanner output exists:

1. Open the newest `research/scans/scan-*.md` files from the last `SCANNER_LOOKBACK_DAYS`.
2. Read `data/scanner_signals.csv` for context if available.
3. Extract up to `MAX_SCANNER_CANDIDATES` names with score >= `SCANNER_MIN_SCORE`.
4. Mark each extracted name as `SCANNER_SEED`, carrying over:
   - score
   - relative volume
   - breakout reason
   - source (`alpaca`, `alpaca+finviz_manual`, future Finviz Elite source)
   - warnings from the scanner report
5. Do not assume scanner candidates have a catalyst. The whole point of Stage 1 is to find
   out whether the price/volume anomaly has a real reason or should be rejected.

If no scanner output exists, proceed with ordinary web/catalyst discovery.

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

CATALYST DIVERSITY: no more than `MAX_EARNINGS_CANDIDATES` candidates may have earnings
as their primary catalyst. Prioritize structural and non-binary catalysts — index
inclusion, lockup expiry, regulatory decisions, product launches, investor days,
conference presentations, insider-buying clusters — over binary earnings events. The
wider `CATALYST_WINDOW_DAYS` window exists to make non-earnings catalysts easier to find.

FOR EACH CANDIDATE, produce:
1. Ticker + one-line company description.
2. Source tag: `routine`, `scanner_seed`, or `routine+scanner_seed`.
3. If scanner-seeded: carry over scanner score and the price/volume reason, then state
   whether independent research confirmed a real catalyst or reason for the move.
4. Catalyst + exact date/window.   | DATE_VERIFIED: NO
5. Why now — the current setup in plain language (basing, breakout, pullback).
6. Bull case (brief) and bear case (brief, including downside-gap risk).
7. Priced-in check — why the catalyst may already be reflected in the price.
8. Invalidation — the level or event that means the idea is wrong.
9. Liquidity note (approx. average daily dollar volume).
10. **Risk rating — Low / Medium / High**, with one short reason per factor. Push toward
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
11. **Risk per share** = entry - stop (absolute, per share). Always show this.
12. **Suggested size** — If `FIXED_POSITION_SIZE` is set, compute:
    suggested_shares = floor( FIXED_POSITION_SIZE / entry_price )
    Show the arithmetic. This is the learning-phase rule: €150 per trade, regardless of
    stop distance. If `FIXED_POSITION_SIZE` is blank but `ACCOUNT_SIZE` and
    `RISK_PER_TRADE_PCT` are both set, use the risk-based formula instead:
    suggested_shares = floor( (ACCOUNT_SIZE * RISK_PER_TRADE_PCT / 100) / risk_per_share )
    Use ONLY the CONFIG values — never invent or adjust the size, risk %, or account
    size. This is arithmetic, not judgment.
13. Confidence (low/med/high) + one line on what would raise it. Cite a recent source.
14. **REPEAT flag** — if the name appeared in last week's `research/candidates-*.md`
    and still qualifies, mark it `REPEAT` and say what changed (price moved, catalyst
    closer, new info).
15. **ACT-NOW flag** — if the catalyst is within 7 calendar days, mark it `ACT-NOW`.
    (The monthly self-grade tracks REPEAT quality and ACT-NOW accuracy separately —
    these flags must be present for that grading to work.)

Also include a short **Rejected Candidates** section with 3-5 names that looked promising
but were rejected, plus the exact reason: no dated catalyst, too illiquid, catalyst already
priced in, binary gap risk too high, unclear invalidation, weak source quality, scanner move
had no confirmable reason, or another specific failure.

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
- Carry over the **source tag, risk rating, risk-per-share, and suggested size** from Stage 1.
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
- Scanner input: <used/not used>. If used, state newest scanner file and how many names were considered.

## Shortlist
### 1. <TICKER> — <company>
- Source tag: <routine/scanner_seed/routine+scanner_seed>
- Scanner context, if any: score <X>; <price/volume reason>; <warning if any>
- Catalyst: <what> on <date>   | DATE_VERIFIED: NO
- Why now: <setup>
- Bull / Bear: <brief> / <brief, incl. gap risk>
- Priced-in check: <why this may already be reflected in price>
- Invalidation: <level/event>
- Liquidity: ~$<X>M ADV
- Risk: <Low/Med/High> — <factor reasons>
- Risk/share: <entry - stop>   | Suggested size: <shares> (€150 ÷ entry = floor)
- Confidence: <low/med/high> — <what would raise it>
- Flags: <REPEAT and/or ACT-NOW, or none>
- Source: <recent citation>
### 2. ...

## Rejected Candidates
- <TICKER> — rejected because <specific reason>

## Deep Dives (top <M> front-runners)
### <TICKER> — <company>
- Source tag / scanner context: ...
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
- The **scanner** is a data-collection and anomaly-detection layer, not a trading system.
  A high scanner score can only promote a name into research; it cannot create a trade.
- The **risk rating** is a caution gauge from imperfect data — use it to size down or
  skip, not as a precise measurement.
- Any **suggested size** is your own fixed rule (€150/trade, learning phase) done as
  arithmetic. The size decision belongs to you and your rule — never the model.
- The **deep dive teaches the bear case** you might not think of — that's its main value
  while you're still building expertise. Read it before you look at the upside.
- Log what you trade in the journal, so you can check whether the risk rating, scanner
  score, and routine picks actually predict anything.
