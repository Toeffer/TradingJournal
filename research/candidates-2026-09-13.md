# Weekly Research and Decision Review — 2026-09-13

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: GPT-5.6 Sol / continuity-first, evidence-gated catalyst-first
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`
- Snapshot generated: 2026-09-11 21:41 UTC; 0 rows. Public dated market data supplements this empty snapshot but does not replace it.
- Prior report reviewed: `research/candidates-2026-09-06.md` and matching manifest
- Active recommendations reviewed: 1 (`FTK.DE`)
- Open positions reviewed: none
- Preliminary pool: 8 names — 4 Europe/XETRA and 4 US
- Final classifications: 0 `ACTIONABLE` / 2 `EARLY_WATCH` / 6 `REJECT`
- Scanner input: reviewed, but no scanner signal fell inside the configured seven-day lookback; latest signal was VOW3.DE on 2026-09-04.
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|
| FTK.DE | 2026-09-06 at €37.74 | monitor | €31.60 Sep 11 close, about -16% from mention; Sep 11 governance shock | no trigger existed | downgraded | monitor |

FTK.DE's October 5 KPI date remains primary-source verified, but the thesis weakened materially. Reuters reported the shares fell 7.9% on September 11 after the company said Supervisory Board chairman Hans-Hermann Lotter resigned with immediate effect. The issuer's public supervisory-board page was still showing Lotter as chairman when accessed, so governance information is not yet clean enough to increase conviction. No stop or target is invented from that uncertainty.

## Existing positions

None. `trades.csv` contains no open positions.

## Coming-week decision sheet

### FTK.DE — MONITOR

- Recommendation ID / continuity: `REC-FTK-2026-0906`; carry-over from 2026-09-06.
- Classification / status: `EARLY_WATCH` / `downgraded`.
- Verified reason: flatexDEGIRO's official calendar schedules **Monthly KPIs September 2026 for 2026-10-05 at 08:30 CEST**, exactly 22 calendar days away.
- What changed: Trading 212 records a €31.60 close on September 11 versus the €37.74 first-mention reference. Reuters reported a 7.9% September 11 drop after the supervisory-board chairman resigned with immediate effect.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro presents FTK.DE as a purchasable XETRA share. Core market-cap bucket (about €3.74B on eToro) and preferred non-US liquidity (roughly €8.7M daily value using the dated €31.60 price and eToro's 276k three-month average volume).
- Expectations / priced in: management still publicly targets about €650M 2026 revenue and €200M–€230M net income. Those accelerated targets create a high bar, while the governance shock adds a new risk not present at first mention.
- Why monitor: the catalyst remains inside the 22–42 day Early Watch window, but the canonical snapshot is empty and the recent price break is downward, not a validated pullback/breakout structure.
- Entry / stop / target: **none**.
- Risk / confidence: **High / Low**.
- Promotion condition: updated structured market data must establish a defensible allowed setup with trigger, invalidation, first target and planned R ≥1.5, while governance is clarified and the October 5 event remains verified.
- Removal condition: the October 5 release moves or completes without a valid setup, eToro availability/liquidity fails, or governance/new evidence materially weakens the KPI thesis.
- Next review: **2026-09-20**.
- Red-team verdict: `DOWNGRADE_EARLY_WATCH`.
- Pre-mortem: the watch fails because the management transition becomes a larger governance problem while September activity merely meets already-high 2026 targets and the share never rebuilds constructive structure.

### LW — MONITOR

- Recommendation ID / continuity: `REC-LW-2026-0913`; new.
- Classification / status: `EARLY_WATCH` / `new`.
- Verified reason: Lamb Weston's official IR release schedules fiscal Q1 2027 results for **2026-10-06**, 23 calendar days away.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro's Germany page offers LW shares. Core market-cap bucket (about $5.8B–$6.4B across recent eToro surfaces) and preferred US liquidity; even 2.77M average shares at the dated $47.37 reference implies more than $130M average daily value.
- Current reference: Trading 212 showed $47.37 with September 10 close $47.44; its recent history shows a roughly 6% weekly decline.
- Expectations / priced in: Lamb Weston's July 24 issuer materials say FY2026 sales and adjusted EBITDA exceeded the high end of guidance. The company is executing its Focus to Win restructuring while international demand and price/mix remain pressure points. That prior beat raises the Q1 bar rather than creating a free catalyst.
- Intervening event: the issuer lists its annual shareholder meeting for September 16. It is not treated as a material trading catalyst.
- Why monitor: the earnings date is verified and sits in the Early Watch window, but LW is absent from the canonical snapshot. There is no normalized multi-session structure from which to derive a non-arbitrary trigger, stop, first target and ≥1.5R.
- Entry / stop / target: **none**.
- Risk / confidence: **Medium / Medium**.
- Promotion condition: updated canonical/dated structure must form a valid breakout, pullback or post-event setup with complete levels and ≥1.5R; otherwise remain monitor.
- Removal condition: October 6 occurs or moves without a valid setup, eToro availability/liquidity fails, or new results/operational evidence materially weakens the thesis.
- Next review: **2026-09-20**.
- Red-team verdict: `DOWNGRADE_EARLY_WATCH`.
- Pre-mortem: the watch fails because Q1 reveals that international weakness, price/mix pressure and plant-restructuring costs outweigh North American execution, while the pre-event decline never forms reliable support.

**NO NEW TRADE.** Neither watch has a complete, validator-compatible trigger-ready setup.

## New research

### SAP.DE — SAP SE — REJECT

- Discovery origin: Europe/XETRA catalyst-first sourcing.
- Primary event: SAP's official calendar schedules Q3 2026 financial results for **October 21**, 38 days away.
- Broker: `ETORO_TRADEABLE: YES` on XETRA in EUR.
- Rejection reason: eToro reports roughly **€205B** market cap, far above the overlay's default €/$50B exclusion threshold. The verified date does not override the universe rule.
- Red-team verdict: `REJECT`.

### DB1.DE — Deutsche Börse AG — REJECT

- Discovery origin: Europe/XETRA catalyst-first sourcing.
- Primary event: Deutsche Börse will publish Q3 2026 results on **October 20**, 37 days away.
- Broker / universe: eToro tradeable; roughly **€48.7B** market cap, placing it at the top of the larger-cap exception bucket with ample liquidity.
- Financing check: on September 9 Deutsche Börse launched a **€600M convertible-bond offering** due 2031, with conversion into new and/or existing shares possible and shareholder pre-emption rights excluded.
- Rejection reason: the larger-cap exception is not justified against available core-universe watches, the recent financing complicates expectations, and the empty canonical snapshot provides no setup edge.
- Red-team verdict: `REJECT`.

### MTX.DE — MTU Aero Engines AG — REJECT

- Discovery origin: Europe/XETRA catalyst-first sourcing.
- Primary calendar: Q3 2026 results conference call is **October 29**, 46 days away.
- Broker: `ETORO_TRADEABLE: YES`; eToro places the stock in the larger-cap exception range.
- Rejection reason: the next financial event is outside the 42-day discovery horizon; no nearer material primary-source trigger was verified.
- Red-team verdict: `REJECT`.

### KBH — KB Home — REJECT

- Discovery origin: US catalyst-first sourcing.
- Primary event: fiscal Q3 2026 earnings **September 22 after market**, 9 days away.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro data places KBH in the core bucket with preferred liquidity.
- Rejection reason: the binary event is inside the Actionable horizon but KBH is absent from the canonical snapshot, so no structure-based entry, invalidation, target and ≥1.5R can be established. Pre-event anticipation is not a setup.
- Red-team verdict: `REJECT`.

### JBL — Jabil Inc. — REJECT

- Discovery origin: US catalyst-first sourcing.
- Primary event: fiscal Q4/FY2026 results **September 30 before market**, 17 days away.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro reports about $32.6B market cap and very strong liquidity, so JBL requires the larger-cap exception.
- Rejection reason: no canonical structure supports a complete setup, and the exception is not clearly superior to core-universe alternatives. A binary earnings date alone is insufficient.
- Red-team verdict: `REJECT`.

### CAG — Conagra Brands, Inc. — REJECT

- Discovery origin: US catalyst-first sourcing.
- Primary event: fiscal Q1 2027 results **September 30**, 17 days away.
- Broker / universe: `ETORO_TRADEABLE: YES`; core bucket around $7.0B with very strong liquidity.
- Expectations: current eToro analyst surface is cautious and the stock has been falling, but that is context rather than a setup.
- Rejection reason: with an empty canonical snapshot there is no defensible trigger, stop, target or ≥1.5R for the pre-earnings window. Do not turn weakness plus a date into a trade.
- Red-team verdict: `REJECT`.

## Removed / expired

None. FTK.DE remains active but is downgraded; LW is added as a new monitor.

## Sources used

### Primary / issuer sources

- flatexDEGIRO financial calendar — October 5 Monthly KPIs September 2026.
- flatexDEGIRO IR overview — 2026 revenue/net-income and customer-growth targets.
- Lamb Weston September 8 earnings-date release and current IR page / latest earnings context.
- SAP investor events calendar.
- Deutsche Börse Q3 conference page and September 9 convertible-bond ad-hoc announcement.
- MTU financial-reporting calendar.
- KB Home September 8 earnings-date release.
- Jabil September 9 earnings-date release.
- Conagra August 31 earnings-date release.

### Market / broker / context sources

- `data/research_snapshot.csv` and `data/research_snapshot.meta.json`
- `research/scanner-summary.md` and `data/scanner_signals.csv`
- Trading 212 dated FTK.DE and LW price histories as supplemental structured market data
- Public eToro Germany/EU instrument pages for stock/share availability, market cap and liquidity
- Reuters September 11 European-market report for the flatexDEGIRO chairman-resignation context
- Prior `research/candidates-2026-09-06.md` and matching manifest
- `data/recommendations.csv`, `data/recommendation_reviews.csv`, `trades.csv`, `RISK_RULES.md`, `SETUPS.md`, and current research-method files
