# Weekly Research and Decision Review — 2026-10-18

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: Claude Opus 5 (`claude-opus-5`) / continuity-first, catalyst-first discovery, evidence-gated
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`
- Snapshot generated: 2026-10-18 21:38 UTC; **0 rows**; archived to `research/snapshots/research_snapshot-2026-10-18.csv`
- Supplementary repository market data: `data/eu_quote_history.csv` — 46 XETRA tickers, daily bars 2026-01-05 → 2026-10-16
- Prior reports reviewed: `candidates-2026-09-20.md`, `-09-13.md`, `-09-06.md` and matching manifests (the previous six calendar weeks contain no other report — the routine last produced a report four weeks ago)
- Active recommendations reviewed: **0** (all three registry objects are terminal)
- Open positions reviewed: **0** (`trades.csv` has no open rows)
- Preliminary pool: **12 names — 7 Europe/XETRA, 5 US** (configured minimum of 4 European met)
- Final classifications: **0 ACTIONABLE / 0 EARLY_WATCH / 12 REJECT**
- Scanner input: reviewed; no signal falls inside the 7-day lookback. Newest recorded signals are RXRX (2026-10-06) and MRVL (2026-10-07). Both the 2026-10-17 US and 2026-10-16 EU scanner runs recorded zero candidates at the alert threshold.
- Market regime: **defensive** (SPY 763.34 vs 50-day MA 768.48; 11.3% of universe above its 20-day MA; cross-asset score −2 of −3)
- Weekly decision: **NO NEW TRADE**

### Run-blocking constraint — primary-source verification was impossible

This run executed from an environment whose network policy permits outbound HTTPS to GitHub only.
Every tier-1 and tier-2 source in the brief's source policy was unreachable: issuer IR sites
(`about.puma.com`, `corporate.zalando.com`, `nordex-online.com`), the Deutsche Börse EQS news
host, `sec.gov`, market-data providers (`finance.yahoo.com`, `stockanalysis.com`) and
`etoro.com` all refused at the egress proxy. Web *search* worked and returned current,
correctly-dated 2026 material; opening any page it pointed at did not.

Two hard gates in the method therefore failed for every candidate:

1. `research_method/verification.md` — "Open the primary source personally in the synthesizing
   pass"; only `date_status: verified` may enter the Actionable or Early Watch lists. The best
   status reachable this run is `secondary_only`.
2. `ETORO_TRADEABILITY.md` — "A candidate can only enter the final shortlist if eToro
   tradeability is verified… Reject candidates when eToro availability cannot be verified."

The honest output is a full discovery pass with every lead rejected at the evidence gate, which
is what follows. **This is an infrastructure finding, not a market finding**, and it is distinct
from the empty-snapshot problem that drove the previous three no-trade weeks. Both now apply at
once. Note separately that the single strongest lead, NDX1.DE, also fails on setup math alone —
so this week's `NO NEW TRADE` does not rest only on the blocked network.

## Prior recommendation audit

| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|
| FTK.DE | 2026-09-06 at €37.74 | remove | removed 2026-09-20 at €30.18 | no trigger ever existed | `invalidated` (unchanged) | no action — terminal |
| LW | 2026-09-13 at $47.37 | remove | removed 2026-09-20 at $42.01 | no trigger ever existed | `expired` (unchanged) | no action — terminal |
| CELC | 2026-08-09 | remove | trade 2026-0004 closed 2026-07-09 at 108.00, +4.04R | n/a | `archived` (unchanged) | no action — terminal |

All three registry objects reached terminal status on or before 2026-09-20 and carry satisfied
removal conditions. Nothing re-enters the book: no post-removal evidence appeared for FTK.DE or
LW, and both of their catalysts (the 2026-10-05 flatexDEGIRO KPI release and the 2026-10-06 Lamb
Weston Q1 report) have now passed unexamined, which is the correct consequence of their removal
rather than a gap. **No review rows were appended this run** — there was no active object to
review, so `data/recommendations.csv` and `data/recommendation_reviews.csv` are unchanged and
this week's decision archive is empty by construction.

## Existing positions

None. `trades.csv` contains 18 closed trades and no open rows, so no `manage` recommendation is
owed. `data/proposals.csv` remains empty, so the control group for the picker test still cannot
begin to work — a standing gap worth noting, not a decision for this run.

## Coming-week decision sheet

No candidate has a complete trigger-ready setup, and no candidate cleared verification.
**NO NEW TRADE.**

Nothing is promoted to `enter_if_triggered`, `wait_pullback`, `monitor` or `manage`, because a
`REJECT` classification cannot carry a weekly action and no object remains in the active book.
The decision sheet is empty for the fourth consecutive report.

## New research

Seven European and five US leads were taken through discovery. Levels and structure for the
European names are computed this run from `data/eu_quote_history.csv` (last bar 2026-10-16);
**no price, liquidity or market-cap data of any kind was obtainable for the US names**, which is
itself part of their rejection.

### NDX1.DE — Nordex SE — REJECT (strongest lead; carry forward)

- Discovery origin: Europe/XETRA repository price history, cross-checked against a catalyst-first
  web-search sweep that surfaced the 2026-10-15 ad-hoc.
- Reported event: Nordex published **preliminary Q3/2026 results on 2026-10-15** and **raised
  full-year 2026 EBITDA-margin guidance to 11.5–12.5% from 8.0–11.0%** (preliminary Q3 EBITDA
  ≈ €278M on revenue ≈ €2,187M), stating the full Q3 report for **2026-11-05** (18 days out).
  `date_status: secondary_only` — the EQS release and the issuer calendar could not be opened.
- Structure, from repository bars: closed **€39.14** on 2026-10-16 after opening **38.78**
  against a prior close of **34.86** — a **+11.2% gap** — with session high **40.02**, low
  **38.48**, and volume **1,382,285** against a ~600k 20-session average. The gap held far above
  its own midpoint (36.82) and closed above the open. Price sits 7.56% below the 20-session high
  of **42.10** (set 2026-09-23), 4.87% above a 20-period EMA, RSI(14) 50.8, ATR(14) 4.17% of
  price, ~€23.9M average daily traded value (clears the non-US €/$5M preferred floor).
- Why it matters now: this is the one name in the pool whose thesis rests on **information that
  is already public** rather than on an event to be anticipated. The binary risk is spent; the
  2026-11-05 report is confirmation, not a coin flip. That is exactly the shape `post-earnings-drift`
  is written for.
- Why it is still rejected — three independent reasons:
  1. **Evidence**: no primary source opened, so the date and the guidance raise are
     `secondary_only`. Verification is a hard gate, not a confidence adjustment.
  2. **Broker**: eToro tradeability unverifiable this run.
  3. **Setup math, which fails on its own**: `post-earnings-drift` requires entry above a
     *consolidation* high with the stop below the gap-day low, and only **one** post-gap session
     exists — no consolidation has formed. Using the gap-day high as trigger (40.10), the gap-day
     low as invalidation (38.20) and the 2026-09-23 swing high as a conservative first target
     (42.00) gives **exactly 1.00R**, below the 1.5R minimum. Reaching 1.5R needs either a target
     near 42.95 — above the 20-session high, so not conservative — or a stop placed *inside* the
     gap-day range, which is a manufactured level. Neither is acceptable.
- Next-run priority: re-examine first, with a primary source, once one is reachable. If a
  consolidation forms in the 38.48–40.02 band over the coming sessions, a defensible trigger may
  exist with a tighter structural stop; if price instead fills the gap back below 38.48 the
  post-guidance strength has been rejected and the object lapses.
- Red-team verdict: `REJECT` (on evidence and on R, not on thesis).

### PUM.DE — PUMA SE — REJECT

- Discovery origin: Europe/XETRA repository price history; catalyst lead from search.
- Reported event: Q3 2026 results **2026-10-30** (12 days out) per calendar sources, with one
  aggregator dissenting at 2026-10-29. `secondary_only`, and the sources disagree.
- Structure: closed **€24.24**, only **1.07%** below the 20-session high of 24.50, RSI(14) 63.3,
  +5.48% over five sessions, +10.23% over twenty, 20.0% below the 52-week high, ~€13.6M daily value.
- Rejection reason: the quietest kind of near-high drift — 2026-10-16 volume was **536k against a
  ~570k average**, so the SETUPS.md breakout condition of ≥2x relative volume is not merely
  missed but contradicted. Add a binary earnings event eight sessions out, which forces
  `exit_before_catalyst = yes` and a holding window shorter than the setup's own 5–10 session
  horizon. Unverified date and unverified broker availability on top.
- Red-team verdict: `REJECT`.

### ZAL.DE — Zalando SE — REJECT

- Discovery origin: Europe/XETRA repository price history; catalyst lead from search.
- Reported event: Q3 2026 results **2026-11-03** (16 days out) per several calendar aggregators,
  none of them the issuer. `secondary_only`.
- Structure: closed **€25.25**, 0.91% below the 20-session high, but **RSI(14) 85.4**, 8.17% above
  its 20-period EMA, **+17.33% over twenty sessions**, ~€23.1M daily value.
- Rejection reason: a chase into a binary event. Even with a verified date the honest action would
  be `wait_pullback`, never an entry — and `wait_pullback` requires an active research object,
  which verification denies it this week.
- Red-team verdict: `REJECT`.

### HAG.DE — HENSOLDT AG — REJECT

- Discovery origin: Europe/XETRA repository price history.
- Reported event: **none established at any source quality.** Search produced only a stated
  2026-07-31 H1 release and a 2024-11-07 Q3 precedent. `date_status: unverified` — and an
  inference from last year's pattern is explicitly not a date under `verification.md`.
- Structure: closed **€87.86** on a session that opened 83.82 and printed a new 20-session high at
  **89.02** on 419k shares against a ~200k average; **+15.27% over five sessions**, 9.72% above
  its 20-period EMA, RSI(14) 71.9, ~€20.2M daily value.
- Rejection reason: undated thesis plus a textbook chase. The five-session extension alone would
  disqualify a breakout entry under SETUPS.md's "not excessively extended" condition.
- Red-team verdict: `REJECT`.

### NEM.DE — Nemetschek SE — REJECT

- Discovery origin: Europe/XETRA repository price history.
- Reported event: none established (`unverified`).
- Structure: closed **€73.55**, **RSI(14) 88.5**, 10.79% above its 20-period EMA and 15.14% above
  its 50-period EMA after **+21.47% in twenty sessions**, ~€16.5M daily value.
- Rejection reason: the most extended name in the pool, with no dated catalyst to justify
  attention. Nothing in SETUPS.md entertains an entry here.
- Red-team verdict: `REJECT`.

### R3NK.DE — RENK Group AG — REJECT

- Discovery origin: Europe/XETRA repository price history.
- Reported event: none established (`unverified`).
- Structure: closed **€38.33** after two strong sessions (+12.59% over five) yet still **11.51%
  below** the 20-session high of 42.73 and **42.2% below** the 52-week high; RSI(14) 44.2;
  ~€20.3M daily value.
- Rejection reason: a two-day bounce inside a decline. Not a breakout — no 20-day-high clearance.
  Not a pullback — there is no prior uptrend to retrace into. The only available thesis is that
  price moved, which SETUPS.md lists under "deliberately not a setup".
- Red-team verdict: `REJECT`.

### SZG.DE — Salzgitter AG — REJECT

- Discovery origin: Europe/XETRA repository price history.
- Reported event: none established (`unverified`).
- Structure: closed **€48.24**, 11.94% below the 20-session high, 2.55% below its 20-period EMA,
  28.6% below the 52-week high, RSI(14) 40.7, −3.40% over five sessions, ~€7.8M daily value
  (clears the non-US floor).
- Rejection reason: a downtrend with no event and no setup. Liquidity that clears a floor is not
  a reason to hold a research object open.
- Red-team verdict: `REJECT`.

### US leads — AGIO, CAPR, SVRA, NUVL, MEOH — all REJECT

All five were sourced catalyst-first from web search and all five fail identically, for reasons
worth stating once rather than five times:

| Ticker | Company | Reported catalyst | Days out | Horizon band | Date status |
|---|---|---|---|---|---|
| AGIO | Agios Pharmaceuticals | PDUFA, mitapivat (sickle cell disease) | 14 | Actionable | `secondary_only` (aggregator) |
| MEOH | Methanex Corporation | Q3 2026 results call, 11:00 ET | 12 | Actionable | `secondary_only` |
| CAPR | Capricor Therapeutics | PDUFA, deramiocel (DMD) — extended from 2026-08-22 | 35 | Early Watch | `secondary_only` (8-K unopened) |
| SVRA | Savara Inc. | PDUFA, molgramostim BLA | 35 | Early Watch | `secondary_only` (aggregator) |
| NUVL | Nuvalent, Inc. | PDUFA, neladalkib (ALK+ NSCLC) | 40 | Early Watch | `secondary_only` (aggregator) |

1. **No primary source opened.** `sec.gov`, FDA and every issuer IR host are unreachable. For the
   three PDUFA names the only sources are aggregator calendars — explicitly lead-only under the
   brief's source policy — and they disagree with each other on several late-November entries,
   with one page self-reporting as ~347 days stale. CAPR's date has already been moved once by
   the FDA, which is weak ground for anticipation even if it were verified.
2. **No market data at all.** `research_snapshot.csv` has zero rows, no scanner signal falls
   inside the 7-day lookback, and no external provider is reachable, so for these five names there
   is no current price, no liquidity figure, no market-cap bucket and no structure. A candidate
   with no verifiable price cannot be sized, stopped or classified.
3. **eToro availability unverified** for all five.
4. Three of the five are single binary FDA decisions with no intermediate trigger inside 21 days.
   Under `RISK_RULES.md` those are monitoring material at most, and holding through one would
   require the explicit half-size (€75) binary-event rule — the exact rule trades 2026-0018 and
   2026-0019 already breached once each.

Red-team verdict for all five: `REJECT`.

## Removed or expired

Nothing was removed this run — the active book was already empty when the run started. The three
terminal objects (FTK.DE `invalidated`, LW `expired`, CELC `archived`) stay in the registry for
outcome analysis, as the method requires.

## Data-quality findings for the human

Two defects found while working, both affecting the routine's own inputs:

1. **`data/eu_quote_history.csv` contains systematically duplicated bars.** For every ticker
   checked, consecutive calendar dates carry identical high/low/close: 2026-07-03 & 07-04,
   2026-08-27 & 08-28, 2026-10-05 & 10-06, and 2026-10-12 & 10-13. The accumulator appears to
   re-record a stale quote rather than skipping a non-session or failed fetch. Consequence: the
   claimed "204 distinct days" overstates true sessions, and every 20-day high, relative-volume
   average and extension figure derived from this file — including the EU scanner's own scores —
   is computed over a window that is shorter in real sessions than it looks. The NDX1.DE levels
   used above were taken from distinct, non-duplicated bars, but the defect should be fixed at the
   collector before these numbers back any entry.
2. **The canonical snapshot has been empty for at least five consecutive weekly cycles.**
   `build_research_snapshot.py` emitted 0 rows again, because it sources only from
   `scanner_signals.csv` within a 7-day lookback plus an empty `finviz_watchlist.csv`, and the
   scanners have produced no alert-threshold candidate since 2026-10-07. Meanwhile
   `eu_quote_history.csv` holds 9,377 usable daily bars that the snapshot builder never reads.
   The research routine is structurally starved of the market data the repository already has.

Neither is a decision for this run; both are repository changes for the human to approve.

## Sources used

### Primary / issuer sources

**None could be opened.** Every attempt against issuer IR, exchange, regulator and market-data
hosts was refused by this environment's egress policy (403 at the proxy / DNS refusal). This is
recorded in the manifest as `source_counts.opened: 0` and `source_counts.primary: 0` rather than
disguised by citing pages that were never read.

### Repository sources (read directly)

- `data/research_snapshot.csv` + `.meta.json` (0 rows; sha256 `564467de…`), archived as
  `research/snapshots/research_snapshot-2026-10-18.csv`
- `data/eu_quote_history.csv` — 9,377 daily bars, 46 XETRA tickers, through 2026-10-16
- `data/market_regime.csv` (latest row 2026-10-17), `data/scanner_signals.csv`,
  `research/scanner-summary.md`, `research/scans/scan-2026-10-17-0002.md`,
  `research/scans/scan-eu-2026-10-16-2056.md`
- `data/recommendations.csv`, `data/recommendation_reviews.csv`, `trades.csv`,
  `data/proposals.csv`, `research/recommendation-book.md`, `research/digest-2026-10-12.md`
- `research/candidates-2026-09-20.md`, `-09-13.md`, `-09-06.md` and matching manifests
- `RESEARCH_BRIEF.md`, `RISK_RULES.md`, `config/risk.toml`, `SETUPS.md`,
  `ETORO_TRADEABILITY.md`, `research_method/*`

### Context sources (surfaced by web search; pages not opened)

Listed with their URLs in the JSON manifest's `evidence` entries, each marked `UNVERIFIED` with
the reason. Search-level coverage: the Nordex 2026-10-15 ad-hoc (via TradingView/MarketScreener/
Deutsche Börse EQS summaries), PUMA and Zalando Q3 calendar entries, HENSOLDT's absent Q3 date,
Methanex's Q3 call, and November 2026 PDUFA aggregator calendars.
