# Weekly Research and Decision Review — 2026-09-06

DRAFT for human review. Not financial advice.

## Run metadata

- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `948577333eea2dfcb5dcb6eb808805354545bef631c3b5f21f83f3001a3208e3`
- Snapshot row count: 1 (`VOW3.DE`, as of 2026-09-04 20:32 CEST)
- Prior report reviewed: `research/candidates-2026-08-30.md` and matching manifest
- Active recommendations reviewed: none
- Open positions reviewed: none
- Preliminary pool: 8 names — 4 Europe/XETRA and 4 US
- Final classifications: 0 `ACTIONABLE` / 1 `EARLY_WATCH` / 7 `REJECT`
- Scanner input: used. The only current canonical/scanner lead was VOW3.DE (score 65), below the scanner-priority score of 70.
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

There were no non-terminal recommendations to carry, upgrade, downgrade, invalidate, or expire. `REC-CELC-2026-0004` remains archived after the trade-close reconciliation, and `trades.csv` contains no open positions.

The 2026-08-30 report also had no Actionable or Early Watch names. Its previously imminent US earnings leads have now resolved or moved into post-event territory, so none was recycled without a new verified catalyst and present setup.

## Existing positions

None.

## Coming-week decision sheet

### FTK.DE — MONITOR

- Classification / status: `EARLY_WATCH` / new
- Action this week: `monitor`
- Catalyst: Monthly KPIs September 2026 on **2026-10-05 at 08:30 CEST** — primary-source verified, **29 calendar days** away.
- `ETORO_TRADEABLE: YES` — eToro presents FTK.DE as a purchasable XETRA stock/share.
- Exchange / currency / instrument: XETRA / EUR / local ordinary share. No direct EUR-account FX conversion; XETRA hours, settlement and holiday-calendar risk still apply.
- Market-cap bucket: core. Public eToro data shows about **€4.09B**.
- Liquidity: preferred tier. Delayed eToro data showed €37.74 and 339,742.58 three-month average volume, about **€12.82M average daily value**.
- Why monitor: the exact October KPI release is inside the 42-day discovery horizon but outside the 21-day Actionable horizon. Management publicly targets about €650M of 2026 revenue and €200M–€230M net income, so the market's bar is already high.
- Priced-in check: the accelerated 2026 targets are known. FTK.DE is not in the committed canonical snapshot, so this run cannot establish a defensible breakout/retest/pullback structure from normalized multi-session data.
- Entry / stop / target: **none**. No broker day-low or arbitrary percentage level is substituted for structure.
- Risk / confidence: **Medium / Medium**
- Red-team verdict: `DOWNGRADE_EARLY_WATCH` — evidence and broker/liquidity gates survive, but the current setup does not support an entry.
- Promotion condition: updated structured market data forms a valid setup with evidence-based trigger, invalidation, first target and planned R ≥ 1.5, while the October 5 event remains verified and uncompleted.
- Removal condition: eToro availability changes, liquidity falls below the allowed tier, the October 5 release moves/completes without a valid setup, or new evidence weakens the KPI thesis.
- Next review: **2026-09-13**
- Flags: none.

**NO NEW TRADE.** There is no `enter_if_triggered` recommendation this week.

## New research

### VOW3.DE — Volkswagen AG — REJECT

- Discovery origin: canonical snapshot / scanner seed.
- Broker: eToro publicly presents VOW3.DE as a purchasable XETRA share in EUR.
- What happened: Volkswagen's Supervisory Board approved the comprehensive Future Plan on **September 3, 2026**. The canonical September 4 snapshot then recorded €81.30, +6.47%, 3.94× relative volume, a 20-day breakout, RSI 64.86 and about €67.72M average daily value.
- Forward-catalyst check: Volkswagen's official 2026 schedule lists the next January–September interim report for **October 29**, **53 days** away and outside the 42-day discovery horizon.
- Priced-in / risk: the Future Plan is already public and is the obvious explanation for the price/volume anomaly. Treating the move itself as a fresh catalyst would violate the scanner-evidence rule.
- Red-team verdict: `REJECT`.
- Rejection reason: completed/current-news catalyst plus no qualifying verified forward event inside 42 days.

### AAG.DE — Aumann AG — REJECT

- Discovery origin: Europe/XETRA routine sourcing.
- Broker: eToro presents AAG.DE as a purchasable XETRA share.
- Primary calendar: September 23 Berenberg & Goldman Sachs German Corporate Conference; next interim statement November 12.
- Universe check: eToro reports about **€193.76M market cap**, below the €/$500M minimum. Average three-month volume is also only about 46,187 shares.
- Red-team verdict: `REJECT`.
- Rejection reason: fails the market-cap gate before expensive research; the September conference is not a sufficiently material binding catalyst anyway.

### DUE.DE — Dürr AG — REJECT

- Discovery origin: Europe/XETRA routine sourcing.
- Broker: eToro presents DUE.DE as a purchasable XETRA share.
- Primary calendar: investor conferences September 22–23, an October 15 company event, and the next nine-month interim statement November 12.
- Liquidity: eToro showed €18.06 and 101,108.3 average three-month volume, about **€1.83M daily value** — below even the non-US conditional floor.
- Red-team verdict: `REJECT`.
- Rejection reason: fails liquidity; nearby calendar items are also weaker than the method's required material catalyst standard.

### RH — RH — REJECT

- Primary catalyst: fiscal Q2 2026 results **September 10 after market**, **4 days** away.
- Broker/universe: eToro confirms RH as a stock/share; recent delayed data showed about $148.57, $2.81B market cap and strong liquidity.
- Intervening-event check: RH's IR news records a July 8 disclosure that Chairman & CEO Gary Friedman sold a small portion of his RH common-stock ownership.
- Setup / priced-in: RH is absent from the canonical snapshot, eToro showed beta 2.54 and a sharp weekly decline, and no evidence-based multi-session trigger, stop and target can be constructed.
- Red-team verdict: `REJECT`.
- Rejection reason: binary event is too close for this evidence set; entering without a validated ≥1.5R structure would be anticipation.

### CHWY — Chewy, Inc. — REJECT

- Primary catalyst: fiscal Q2 2026 results **September 9 before market**, **3 days** away.
- Broker/universe: eToro presents CHWY as a purchasable stock; recent delayed data showed about $24.02 and a market cap near the $10B core-universe ceiling.
- Intervening-event check: Chewy's April 8 Modern Animal transaction was expected to close in fiscal Q2 2026; the same release increased the share-repurchase authorization by $500M.
- Setup / expectations: the acquisition and repurchase program affect the earnings context, while CHWY is absent from the committed snapshot. No defensible structure-based levels or ≥1.5R are available.
- Red-team verdict: `REJECT`.
- Rejection reason: three-day binary event plus insufficient current structured setup evidence.

### AVAV — AeroVironment, Inc. — REJECT

- Primary catalyst: fiscal Q1 2027 results **September 9 after market**, **3 days** away.
- Broker/universe: eToro Germany presents AVAV as a purchasable stock; delayed data showed about $144.80, $7.48B market cap and 1.59M average volume.
- Setup: AVAV is absent from the canonical snapshot. No committed multi-session structure supports an evidence-based entry, stop, first target and planned R ≥ 1.5.
- Risk: binary earnings gap, defense/contract timing, integration/execution and USD/EUR exposure.
- Red-team verdict: `REJECT`.
- Rejection reason: event anticipation without a trigger-ready setup.

### ASO — Academy Sports and Outdoors, Inc. — REJECT

- Primary catalyst: fiscal Q2 2026 results **September 9 before market**, **3 days** away.
- Broker/universe: eToro Germany presents ASO as a purchasable stock; delayed data showed roughly $2.91B market cap and 1.5M average volume.
- Setup: ASO is absent from the canonical snapshot, so there is no normalized structure from which to derive valid entry/invalidation/target levels.
- Risk: binary earnings gap, discretionary consumer demand, inventory/promotional pressure and USD/EUR exposure.
- Red-team verdict: `REJECT`.
- Rejection reason: no defensible ≥1.5R setup with only three days to earnings.

## Removed / expired

None this week. No active recommendation existed at the start of the review.

## Sources used

### Primary / issuer sources

- flatexDEGIRO financial calendar — October 5 Monthly KPIs September 2026.
- flatexDEGIRO investor-relations overview — accelerated 2026 revenue/net-income targets.
- Volkswagen Group September 3 Future Plan ad-hoc release and official 2026 scheduled dates.
- Aumann financial calendar.
- Dürr Group financial calendar.
- RH September 3 earnings-date release and current IR news feed.
- Chewy August 19 earnings-date release and April 8 Modern Animal / repurchase release.
- AeroVironment August 26 earnings-date release.
- Academy Sports + Outdoors August 26 earnings-date release.

### Market / broker / repository sources

- `data/research_snapshot.csv` and `data/research_snapshot.meta.json`
- `research/scanner-summary.md` and `data/scanner_signals.csv`
- Public eToro Germany/EU instrument pages for broker availability and supplemental delayed market data
- Prior `research/candidates-2026-08-30.md` and matching manifest
- `data/recommendations.csv`, `data/recommendation_reviews.csv`, `trades.csv`, `RISK_RULES.md`, `SETUPS.md`, and the current research-method files

The research snapshot used by this report is archived as `research/snapshots/research_snapshot-2026-09-06.csv`.
