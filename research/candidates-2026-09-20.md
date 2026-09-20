# Weekly Research and Decision Review — 2026-09-20

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: GPT-5.6 Sol / continuity-first, evidence-gated catalyst-first
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`
- Snapshot generated: 2026-09-18 21:37 UTC; 0 rows. Public dated broker data supplements this empty snapshot but does not replace it.
- Prior report reviewed: `research/candidates-2026-09-13.md` and matching manifest
- Active recommendations reviewed: 2 (`FTK.DE`, `LW`)
- Open positions reviewed: none
- Preliminary pool: 8 names — 4 Europe/XETRA and 4 US
- Final classifications: 0 `ACTIONABLE` / 0 `EARLY_WATCH` / 8 `REJECT`
- Scanner input: reviewed; no signal fell inside the configured seven-day lookback. Latest recorded scanner signal remains VOW3.DE on 2026-09-04.
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|
| FTK.DE | 2026-09-06 at €37.74 | monitor | €30.18 eToro delayed reference; about -20% from mention | no trigger existed | invalidated | remove |
| LW | 2026-09-13 at $47.37 | monitor | $42.01 eToro delayed reference; about -11% from mention | no trigger existed | expired | remove |

Both watches have crossed from the 22–42 day Early Watch window into the 0–21 day Actionable horizon without developing a defensible setup. The canonical snapshot still has zero rows, so there is no normalized multi-session structure from which to derive a non-arbitrary trigger, stop, target and planned R. They leave the active book rather than being converted into event-anticipation trades.

## Existing positions

None. `trades.csv` contains no open positions.

## Coming-week decision sheet

No candidate has a complete trigger-ready setup. **NO NEW TRADE.**

### FTK.DE — REMOVE

- Recommendation ID / continuity: `REC-FTK-2026-0906`; carry-over from 2026-09-06.
- Verified reason: flatexDEGIRO's official calendar still schedules September 2026 monthly KPIs for **2026-10-05 at 08:30 CEST**, 15 calendar days away.
- What changed: eToro's delayed Germany/EU page shows €30.18 versus €37.74 at first mention. The September 11 supervisory-board-chairman resignation remains an unresolved governance risk.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro presents FTK.DE as a purchasable XETRA share. Core market cap about €3.28B and roughly €11.6M average daily value from €30.18 × 383k three-month average volume, above the preferred non-US floor.
- Why remove: the catalyst is now inside the Actionable horizon, but no allowed setup exists and the monitoring thesis weakened rather than improved. No entry/stop/target is invented.
- Final status: `invalidated` for this recommendation object. A genuinely new thesis or later event would require fresh research.
- Red-team verdict: `REJECT`.

### LW — REMOVE

- Recommendation ID / continuity: `REC-LW-2026-0913`; carry-over from 2026-09-13.
- Verified reason: Lamb Weston's official release still schedules fiscal Q1 2027 results for **2026-10-06**, 16 calendar days away.
- What changed: eToro's delayed Germany/EU page shows $42.01 versus $47.37 at first mention, roughly -11%. Market cap remains core at about $5.8B and average volume about 2.77M shares.
- Why remove: the binary earnings date is now inside the Actionable horizon but the zero-row canonical snapshot still cannot support structure-based levels or ≥1.5R. The falling pre-event tape is not itself a pullback setup.
- Final status: `expired` as an Early-Watch recommendation without promotion.
- Red-team verdict: `REJECT`.

## New research

### DB1.DE — Deutsche Börse AG — REJECT

- Discovery origin: Europe/XETRA catalyst-first sourcing.
- Primary event: issuer page states Q3 2026 financial results will be published **2026-10-20**, 30 days away.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro shows a purchasable XETRA share, about €48.15B market cap and strong liquidity, placing it near the top of the larger-cap exception bucket.
- Rejection reason: the larger-cap exception remains unjustified, the September €600M convertible financing complicates the setup, and the canonical snapshot has no structure row.
- Red-team verdict: `REJECT`.

### SAP.DE — SAP SE — REJECT

- Discovery origin: Europe/XETRA catalyst-first sourcing.
- Primary event: SAP's official IR calendar schedules Q3 2026 results for **2026-10-21**, 31 days away.
- Broker: `ETORO_TRADEABLE: YES` on XETRA in EUR.
- Rejection reason: eToro market-cap evidence remains far above the default €/$50B exclusion threshold. A verified date does not override the universe rule.
- Red-team verdict: `REJECT`.

### DBK.DE — Deutsche Bank AG — REJECT

- Discovery origin: Europe/XETRA catalyst-first sourcing.
- Primary event: Deutsche Bank's official calendar schedules Q3 earnings for **2026-10-28**, 38 days away.
- Broker: `ETORO_TRADEABLE: YES`; eToro shows a purchasable XETRA share with roughly €75.8B market cap and ample liquidity.
- Rejection reason: market cap is above the default €/$50B exclusion threshold; no exception applies.
- Red-team verdict: `REJECT`.

### CAG — Conagra Brands, Inc. — REJECT

- Discovery origin: US catalyst-first sourcing.
- Primary event: Conagra's official release schedules fiscal Q1 2027 results for **2026-09-30**, 10 days away.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro shows about $7.24B market cap, $15.13 delayed price and 15.56M three-month average volume.
- Expectations / priced in: eToro's analyst surface is cautious while the share has recently stabilized, but that is context, not a setup.
- Rejection reason: the binary event is inside the Actionable horizon and the canonical snapshot has no structure row; no defensible trigger, stop, target and ≥1.5R can be established.
- Red-team verdict: `REJECT`.

### JBL — Jabil Inc. — REJECT

- Discovery origin: US catalyst-first sourcing.
- Primary event: Jabil's official release schedules Q4/FY2026 results for **2026-09-30 before market**, 10 days away.
- Broker: `ETORO_TRADEABLE: YES`; eToro offers JBL shares with deep liquidity, but market cap is in the larger-cap exception bucket.
- Rejection reason: binary earnings plus larger-cap exception and no canonical setup structure. The event date alone is not an entry.
- Red-team verdict: `REJECT`.

### AYI — Acuity Inc. — REJECT

- Discovery origin: US catalyst-first sourcing.
- Primary event: Acuity's official IR release schedules fiscal Q4/FY2026 results for **2026-10-01**, 11 days away.
- Broker: `ETORO_TRADEABLE: YES`; eToro offers AYI shares. Recent eToro surfaces place market cap around the core/low exception boundary with preferred liquidity.
- Expectations: Q3 showed 1.6% sales growth and 3.7% adjusted EPS growth, while tariff refunds affected comparability.
- Rejection reason: no canonical multi-session structure exists for a valid pre-earnings setup; do not manufacture levels from a broker day range.
- Red-team verdict: `REJECT`.

## Removed / expired

- FTK.DE — `invalidated`; monitoring phase ended without a valid setup as the October 5 catalyst entered the Actionable horizon, with governance risk still elevated.
- LW — `expired`; Early-Watch phase ended without a valid setup as October 6 earnings entered the Actionable horizon.

## Sources used

### Primary / issuer sources

- flatexDEGIRO financial calendar — October 5 monthly KPIs and October 21 Q3 update.
- Lamb Weston September 8 earnings-date release — October 6 Q1 results.
- Deutsche Börse Q3 conference page — October 20 Q3 publication; September convertible-financing announcement retained as intervening-risk context.
- SAP investor events calendar — October 21 Q3 results.
- Deutsche Bank financial calendar — October 28 Q3 earnings report.
- Conagra August 31 earnings-date release — September 30 Q1 results.
- Jabil September 9 earnings-date release — September 30 Q4/FY results.
- Acuity August 28 earnings-date release — October 1 Q4/FY results.

### Market / broker / repository sources

- `data/research_snapshot.csv` and `data/research_snapshot.meta.json`
- `research/scanner-summary.md` and `data/scanner_signals.csv`
- Public eToro Germany/EU instrument pages for stock/share availability, market cap, price and liquidity context
- Prior `research/candidates-2026-09-13.md` and matching manifest
- `data/recommendations.csv`, `data/recommendation_reviews.csv`, `trades.csv`, `RISK_RULES.md`, `SETUPS.md`, and current research-method files
