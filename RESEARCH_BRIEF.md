# RESEARCH_BRIEF.md — Autonomous Weekly Candidate Research

This is the instruction set for the weekly research routine. It creates a draft
shortlist for human review; it never creates a trade and never changes risk rules.

**Not financial advice. Verify every date, price, and claim before acting.**

## Operating principle

A distant catalyst is useful for discovery but is not automatically actionable.
Too much can change between today and the event: price, expectations, financing,
market regime, and the company itself. The routine therefore uses two horizons:

- **Actionable horizon: 21 calendar days.** A candidate may enter the final
  shortlist only when its verified catalyst is inside this window.
- **Early-watch horizon: days 22–42.** These names are recorded separately for
  follow-up, not presented as current swing-trade candidates.

Exception: a catalyst 22–42 days away may enter the actionable shortlist only if
there is a separate, dated, verified intermediate trigger inside 21 days and the
setup/invalidation are based on that nearer trigger. State the exception plainly.

For logged proposals, `data/proposals.csv` separately controls the trade horizon:
10 trading sessions by default, with an explicit `max_holding_days`, and
`exit_before_catalyst = yes` unless the human deliberately chooses otherwise.

## Recommended routine settings

- Run weekly, preferably Sunday evening, using the strongest available model.
- Web search on; use connected financial data only as a supplement.
- Work from `main` unless intentionally testing another branch.
- Read `RISK_RULES.md`, `SETUPS.md`, `ETORO_TRADEABILITY.md`, the latest US/EU
  scanner reports, and `data/scanner_signals.csv` before research.
- Scanner names are leads, never evidence or pre-approved ideas.

## CONFIG

```text
REGION:                         US common shares + XETRA shares
MARKET_CAP_MIN:                 500000000
MARKET_CAP_MAX:                 10000000000
MIN_AVG_DOLLAR_VOLUME:          25000000
PRELIMINARY_SCAN_COUNT:         12
NUM_ACTIONABLE_CANDIDATES:       5
NUM_EARLY_WATCH:                 5
NUM_DEEP_DIVES:                  3
MIN_EU_PRELIMINARY:              4
ASIA_POLICY:                     exceptional-only
ACTIONABLE_CATALYST_DAYS:       21
DISCOVERY_CATALYST_DAYS:        42
ACT_NOW_DAYS:                    7
MAX_EARNINGS_CANDIDATES:         2
SCANNER_LOOKBACK_DAYS:           7
SCANNER_MIN_SCORE:              70
MAX_SCANNER_CANDIDATES:          5
FIXED_POSITION_SIZE_EUR:       150
```

The values in `config/risk.toml` and `RISK_RULES.md` are authoritative for risk
and holding periods. Do not invent missing values.

## Source quality

Use sources in this order:

1. Company investor relations, filings, exchange notices, official calendars.
2. Reputable financial news and market-data providers.
3. Scanner output as discovery context only.
4. Analyst notes, blogs, forums, and social media as secondary context only.

For European candidates, prefer company Finanzkalender pages, EQS/DGAP, Deutsche
Börse, RNS, Euronext/SIX notices, and issuer IR pages. Reject an event date that
cannot be verified from a primary or high-quality source.

For lockup expiries, do not rely on “IPO date + N days.” Verify the prospectus,
underwriting terms, early-release provisions, waivers, and later offerings.

For every non-US candidate state exchange, currency, local share versus ADR, FX
exposure, and market hours. Name UK stamp duty for LSE shares.

## Stage 1 — Broad discovery

Build up to `PRELIMINARY_SCAN_COUNT` names with a specific dated catalyst inside
`DISCOVERY_CATALYST_DAYS`.

- Source at least `MIN_EU_PRELIMINARY` European names before quality filtering,
  or explain exactly what EU search came up empty.
- Include up to `MAX_SCANNER_CANDIDATES` recent scanner names meeting the score
  threshold, then verify them independently.
- No more than `MAX_EARNINGS_CANDIDATES` final actionable names may use earnings
  as the primary catalyst.
- Prefer structural or already-public catalysts over binary event gambling.
- Reject names with no clean invalidation, weak liquidity, unverifiable events,
  overwhelming dilution/gap risk, or a move whose only explanation is “it rose.”
- Ask for every survivor: “What would make this already priced in?”

Classify each surviving name immediately:

- `ACTIONABLE`: catalyst in 0–21 days, or a verified intermediate trigger in
  that range.
- `EARLY_WATCH`: catalyst in 22–42 days with no nearer verified trigger.
- `REJECT`: fails evidence, liquidity, tradeability, setup, or risk requirements.

A sparse output is success. Do not pad.

## Stage 2 — Actionable shortlist

For each `ACTIONABLE` candidate provide:

1. Ticker, company, exchange, currency, and one-line description.
2. Source tag: `routine`, `scanner_seed`, or `routine+scanner_seed`.
3. Catalyst and exact verified date; days until catalyst.
4. Why now: the current setup, not merely the future event.
5. Entry zone, stop/invalidation, realistic first target, and planned R.
6. Bull case and bear case, including gap/dilution risk.
7. Priced-in check.
8. Liquidity and spread note.
9. Risk rating: Low / Medium / High, with reasons.
10. Risk per share and fixed-size arithmetic using €150 only.
11. Confidence and what would raise it.
12. Flags: `ACT-NOW` when inside 7 days; `REPEAT` when carried from last week.
13. Recent primary/high-quality citations.

A candidate without entry, stop, target, and planned R is research context, not a
proposal. Do not silently promote it to `data/proposals.csv`.

## Stage 3 — Early-watch list

For each `EARLY_WATCH` name provide only:

- Catalyst and verified date.
- Days until catalyst.
- Why it may matter.
- What must happen before promotion to `ACTIONABLE`.
- Next review date, normally the following weekly run.
- Main invalidation or reason to remove it.

Do not calculate a trade size or call an early-watch name a current setup.

## Stage 4 — Deep dives

Deep-dive up to `NUM_DEEP_DIVES` actionable front-runners by setup quality,
confidence, and reward-to-risk—not by excitement or theoretical upside.

For each, cover:

- Catalyst mechanics and what the market expects.
- Bull/base/bear scenarios.
- Support, resistance, entry, target, and invalidation.
- Financing, dilution, insider, short-interest, and event-gap risks where relevant.
- Pre-mortem: assume the idea lost; identify the most likely ignored fact.
- Explicit plan: exit before catalyst or deliberately hold through it.
- Suggested `max_holding_days` (normally 5–10 trading sessions).

## Multi-agent discipline

Subagent findings are leads, not evidence. The synthesizing agent must open and
verify the primary source used for every final catalyst date. State whether the
run was screener-first, catalyst-first, or hybrid and whether parallel agents
were used.

## Output and collision rule

Before writing, check whether `research/candidates-YYYY-MM-DD.md` exists.
Never overwrite it. A second same-day run writes
`research/candidates-YYYY-MM-DD-HHMM.md` and references the earlier file.

Use this structure:

```markdown
# Candidate Research — YYYY-MM-DD
DRAFT for human review. Verify all dates and numbers.

## Summary
- Method and region mix
- Scanner inputs used
- Actionable count / early-watch count / rejected count

## Actionable Shortlist — catalyst inside 21 days
### 1. TICKER — Company
- Catalyst / date / days remaining:
- Source tag / scanner context:
- Why now:
- Entry / stop / target / planned R:
- Bull / bear / priced-in:
- Liquidity / risk rating:
- Risk per share / €150 arithmetic:
- Exit before catalyst?: yes/no
- Max holding days:
- Flags:
- Sources:

## Early Watch — catalyst 22–42 days away
### TICKER — Company
- Catalyst / date / days remaining:
- Promotion condition:
- Next review date:
- Removal condition:
- Sources:

## Rejected Candidates
- TICKER — exact rejection reason

## Deep Dives
...
```

## Success criteria

- Every actionable catalyst is within 21 days unless a nearer intermediate
  trigger is explicitly verified.
- Every 22–42-day name is in Early Watch, not the actionable shortlist.
- Every final date has a primary or high-quality source.
- Entry, stop, target, planned R, exit-before-event policy, and holding horizon
  are explicit for actionable names.
- A no-candidate week is allowed and recorded honestly.
- Nothing writes to `trades.csv`; only an explicit human statement that a trade
  occurred can do that.
