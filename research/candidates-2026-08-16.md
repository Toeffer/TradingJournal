# Weekly Research and Decision Review — 2026-08-16
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode: GPT-5.6 Sol / continuity-first evidence-gated hybrid
- Input snapshot / SHA-256: `data/research_snapshot.csv` / `1b250764823b4769a981e4bbc58fb00959ee97963f9d1c7a29456888314a258d`
- Snapshot timestamp: 2026-08-14 19:52:48 UTC; 5 canonical rows.
- Prior reports reviewed: `research/candidates-2026-08-09.md` and matching manifest, plus rolling recommendation state and review history.
- Active recommendations reviewed: 0. CELC is already archived after the 2026-08-10 reconciliation.
- Open positions reviewed: 0. `trades.csv` currently contains no open rows.
- Preliminary pool: 8 leads; 4 European/XETRA names (TKA.DE, AT1.DE, DHER.DE, EVD.DE) and 4 US names (IREN, JOBY, PLTR, SMCI). Discovery was hybrid and was not padded to 12 after the current snapshot and primary-source pass yielded no additional evidence-grade names.
- New leads / Actionable / Early Watch / Reject counts: 8 / 0 / 0 / 8
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

There are no non-terminal recommendation objects to carry this week. `REC-CELC-2026-0004` is archived and its linked trade is confirmed closed, so no management recommendation is required.

## Existing positions

No open positions are recorded in `trades.csv`.

## Coming-week decision sheet

No candidate has both a primary-source-verified forward catalyst and a complete, structure-based setup with a defensible trigger, invalidation, first target and planned R of at least 1.5. **NO NEW TRADE.**

The strongest event leads are AT1.DE, DHER.DE and EVD.DE. All three have verified issuer-calendar events inside the 21-day Actionable horizon, but none has sufficient current multi-session structure in the canonical data pack to manufacture a legitimate trigger/stop/target set. The method therefore rejects them for this run rather than converting event dates into pseudo-setups.

## New research

### TKA.DE — thyssenkrupp AG
- Discovery origin: EU-XETRA canonical snapshot / scanner seed.
- Broker/universe: public eToro pages present TKA.DE as a purchasable XETRA share; market-cap observations are inside the core universe. Canonical average daily value is about €23.52M, above the preferred non-US liquidity floor.
- Verification: thyssenkrupp's official investor calendar shows the 9M 2025/2026 interim report occurred on **2026-08-13**. The next scheduled annual report is in December, outside the 42-day discovery horizon.
- Snapshot context: €13.525 on August 13, +9.07%, 3.14x relative volume, above the 20-day high and RSI 69.96.
- Classification / red team: `REJECT`. The scanner observation coincides with an already-completed reporting event. No new primary-source-verified material catalyst is inside 42 days, so the price move cannot support a fresh research object by itself.
- Pre-mortem: a momentum chase fails because the event-day repricing was the catalyst and there is no verified follow-on event to support continued anticipation.

### IREN — IREN Limited
- Discovery origin: US canonical snapshot / scanner seed.
- Broker/universe: public eToro pages present IREN as a purchasable share. Recent public broker observations place market cap around $14.5B, which is the larger-cap exception bucket. Canonical ADV is about $84.42M.
- Verification: IREN's opened investor events/reports pages do not state a new future FY2026 results date. Historical cadence is not date verification.
- Snapshot context: $47.42 on August 13, +8.61%, 2.91x relative volume and a 20-day breakout.
- Classification / red team: `REJECT`. No primary-source-verified forward date exists, and a larger-cap exception would additionally need a clearly superior setup. Scanner momentum cannot fill either gap.
- Pre-mortem: the move is a thematic/high-beta repricing that fades while the research process mistakes historical reporting cadence for a verified catalyst.

### JOBY — Joby Aviation, Inc.
- Discovery origin: US canonical snapshot / scanner seed.
- Broker/universe: eToro tradeability is publicly visible and market cap is near the top of the core universe.
- Verification: Joby's official IR calendar shows Q2 2026 results were released **2026-08-05**, before this run.
- Snapshot context: $8.895 on August 10, +3.01%, 3.39x relative volume and a 20-day breakout. Canonical ADV is only about $9.50M.
- Classification / red team: `REJECT`. The relevant reporting event already occurred and liquidity is below the $10M US conditional-watchlist floor, independently disqualifying it.
- Pre-mortem: an illiquid post-event breakout reverses and slippage dominates a small position while there is no forward catalyst.

### PLTR — Palantir Technologies Inc.
- Discovery origin: US canonical snapshot / scanner seed.
- Snapshot context: $178.78 on August 10, about $240.85M ADV, 2.72x relative volume, above the 20-day high and RSI 75.03.
- Classification / red team: `REJECT` at discovery. The broker/universe overlay excludes mega-caps above $50B and obvious crowded headline-AI names by default. PLTR fits the excluded-by-default crowded headline-AI/mega-cap category, so the scanner observation cannot promote it.
- Pre-mortem: the process confuses liquid thematic momentum with an eligible small/mid-cap setup and buys after expectations are already embedded.

### SMCI — Super Micro Computer, Inc.
- Discovery origin: US canonical snapshot / scanner seed.
- Broker/universe: public eToro pages present SMCI as a purchasable share; recent public broker observations place market cap around $18B, in the larger-cap exception bucket.
- Verification: Supermicro's official IR materials scheduled fiscal Q4 2026 results for **2026-08-11**; that event has already occurred. Its July preliminary update had already flagged revenue near the low end of prior guidance while highlighting record backlog.
- Snapshot context: $41.18 on August 13, +9.58%, 3.54x relative volume, 7.97% five-day extension, RSI 72.18 and about $91.32M ADV.
- Classification / red team: `REJECT`. The principal results catalyst is past, the name is already extended, and no new verified forward event was found. It also sits in the larger-cap exception bucket.
- Pre-mortem: a post-event rebound is mistaken for a new catalyst setup and reverses after the market digests guidance quality and crowded AI-server expectations.

### AT1.DE — Aroundtown SA
- Discovery origin: catalyst-first European pass.
- Broker/universe: public eToro Germany evidence presents AT1.DE as a purchasable XETRA share. Recent public broker data showed about €2.31B market cap and approximately €6.23M average daily value, satisfying the core-universe and preferred non-US liquidity rules.
- Verified catalyst: Aroundtown's official financial calendar schedules its **H1 2026 Financial Report for 2026-08-26** (10 calendar days away).
- Intervening-event review: Aroundtown announced on July 7 a €850M bond issuance alongside a concurrent tender offer, so financing/capital-structure context is relevant to the H1 read-through.
- Expectations / priced-in: without a current canonical snapshot row, this run does not have the multi-session structure needed to judge whether the latest price already discounts the report or to derive defensible levels.
- Classification: `REJECT` for this run. The event is inside the 21-day Actionable horizon, but an event date alone is not a setup. No structure-based trigger, stop and first target with >=1.5R can be established from the canonical pack without inventing levels.
- Red-team verdict: `REJECT`. Promotion requires updated structured price history that produces an allowed setup and survives the financing/expectations review.
- Pre-mortem: the trade is entered simply because H1 results are near, while financing/valuation expectations dominate and arbitrary levels create false precision.

### DHER.DE — Delivery Hero SE
- Discovery origin: catalyst-first European pass.
- Broker/universe: public eToro Germany evidence presents DHER.DE as a purchasable XETRA share. Recent public broker data showed roughly €11.06B market cap (larger-cap exception bucket) and approximately €52.11M average daily value.
- Verified catalyst: Delivery Hero's official financial calendar schedules the **Half-Year Financial Report 2026 & Q2 Trading Update for 2026-08-27** (11 calendar days away).
- Intervening-event review: Delivery Hero disclosed on July 14 that it was in advanced negotiations with Uber regarding a potential takeover offer. That special-situation path can overwhelm a normal earnings/trading-update setup.
- Expectations / priced-in: M&A probability and terms are central expectations variables; the current canonical snapshot has no DHER.DE row from which to derive clean structure.
- Classification: `REJECT` for this run. A larger-cap exception would need a clearly superior setup, but there is no complete structure-based trigger/stop/target and the takeover process materially changes event risk.
- Red-team verdict: `REJECT`. The ordinary earnings-catalyst thesis is contaminated by takeover optionality and cannot justify a normal swing setup without current structure and explicit M&A analysis.
- Pre-mortem: a normal earnings setup is overwhelmed by takeover headlines, deal terms or negotiation failure, making stop-based R arithmetic unreliable.

### EVD.DE — CTS EVENTIM AG & Co. KGaA
- Discovery origin: catalyst-first European pass.
- Broker/universe: public eToro evidence presents EVD.DE as a purchasable XETRA share. Recent public broker observations showed about €5.37B market cap and approximately €17.82M average daily value, satisfying the core-universe and preferred non-US liquidity rules.
- Verified catalyst: CTS EVENTIM's official financial calendar schedules its **Half-Year Financial Report for 2026-08-20** (4 calendar days away).
- Expectations / priced-in: the catalyst is imminent, but EVD.DE is absent from the canonical snapshot, so this run lacks current normalized trend/structure evidence for a defensible setup and priced-in assessment.
- Classification: `REJECT` for this run. The event is verified and tradeability/liquidity appear adequate, but no evidence-based trigger, invalidation and target with >=1.5R can be produced without inventing technical levels.
- Red-team verdict: `REJECT`. An imminent report without current structure is event anticipation, not an allowed entry setup.
- Pre-mortem: strong event expectations are already reflected and an arbitrary pre-report entry suffers a gap that was never captured by the nominal stop.

## Removed or expired

No active rolling recommendation was removed this week. CELC was already archived on 2026-08-10 after the trade journal confirmed the position had closed on 2026-07-09.

## Sources used
- thyssenkrupp official investor calendar.
- Joby Aviation official investor-relations calendar.
- Super Micro Computer official IR results announcement and preliminary-results update.
- IREN official investor events/reports pages.
- Aroundtown official financial calendar and July 7 financing announcement.
- Delivery Hero official financial calendar and July 14 takeover-negotiations disclosure.
- CTS EVENTIM official investor-relations financial calendar.
- Public eToro instrument pages for broker availability, market-cap context and supplementary liquidity observations.
- Canonical repository snapshot, current scanner summary, recommendation ledger/reviews, trade journal, prior report and prior manifest.

The rolling recommendation registry, append-only review ledger and recommendation book require no state change this week because there are no active recommendations, no open positions and no surviving new object. The dated weekly decision archive therefore contains zero review rows.
