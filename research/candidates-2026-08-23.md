# Weekly Research and Decision Review — 2026-08-23
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode: GPT-5.6 Sol / continuity-first evidence-gated hybrid
- Input snapshot / SHA-256: `data/research_snapshot.csv` / `1bbac2049352c0d225b6e1c8e2fa8ffe75e8f6d3a824795b1a47c0c48c8c52d0`
- Snapshot timestamp: 2026-08-21 19:33 UTC; 1 canonical row (HOOD).
- Prior reports reviewed: `research/candidates-2026-08-16.md` and matching manifest, plus rolling recommendation state and review history.
- Active recommendations reviewed: 0. `REC-CELC-2026-0004` remains archived.
- Open positions reviewed: 0. `trades.csv` contains no open rows.
- Preliminary pool: 5 leads; 4 European/XETRA names (AT1.DE, DHER.DE, EVD.DE, NCH2.DE) and 1 US scanner name (HOOD). Discovery was hybrid and deliberately not padded because current canonical breadth is only one row and additional web leads did not clear the evidence/materiality gate.
- New leads / Actionable / Early Watch / Reject counts: 5 / 0 / 0 / 5
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

There are no non-terminal recommendation objects to carry. The only durable recommendation, CELC, is archived after trade reconciliation, so no lifecycle row changes this week.

## Existing positions

No open positions are recorded in `trades.csv`; no `manage` review is required.

## Coming-week decision sheet

No candidate has both qualifying evidence and a complete, structure-based setup for the next five trading sessions. **NO NEW TRADE.**

AT1.DE and DHER.DE have verified reports on August 26 and August 27 respectively, but both are absent from the canonical snapshot. Supplementary broker data can confirm tradeability, price, market cap and rough liquidity, but it cannot create the multi-session structure needed for a legitimate trigger, stop, target and planned R. The method therefore rejects them for this run rather than manufacturing pre-event entries.

## New research

### AT1.DE — Aroundtown SA
- Discovery origin: prior report continuity plus catalyst-first European pass.
- Broker/universe: `ETORO_TRADEABLE: YES`. Public eToro presents AT1.DE as a purchasable XETRA share. Current public broker data shows roughly €2.05 price, €2.25B market cap and 2.42M three-month average volume, comfortably inside the core market-cap universe and around the preferred non-US liquidity floor.
- Verified catalyst: Aroundtown's official IR calendar lists the **H1 2026 Financial Report on 2026-08-26** (3 calendar days away).
- Financing/event review: the July €850M bond issuance and tender offer remain important capital-structure context going into H1 results.
- Expectations / priced-in: public broker data shows the stock near the bottom of its 52-week range, but the canonical research snapshot has no AT1.DE row and therefore no current normalized multi-session structure from which to establish a setup.
- Classification / red team: `REJECT`. The date and broker gate pass, but a 3-day-away event with no evidence-based trigger, invalidation, target and >=1.5R is event anticipation, not an allowed proposal.
- Pre-mortem: the process buys simply because the H1 report is near, while financing/valuation expectations dominate and the nominal stop was never grounded in structure.

### DHER.DE — Delivery Hero SE
- Discovery origin: prior report continuity plus catalyst-first European pass.
- Broker/universe: `ETORO_TRADEABLE: YES`. Public eToro presents DHER.DE as a purchasable XETRA share around €37.00, with roughly €11.34B market cap and 1.09M three-month average volume. Liquidity is strong, but market cap places the name in the larger-cap exception bucket.
- Verified catalyst: Delivery Hero's official IR materials list the **Half-Year Financial Report 2026 & Q2 2026 Trading Update on 2026-08-27** (4 calendar days away).
- Intervening-event review: the July Uber business-combination/takeover process remains material. That special-situation path can overwhelm normal Q2/H1 expectations and make stop-based event risk non-linear.
- Expectations / priced-in: eToro shows the share close to its 52-week high, while M&A probability and terms remain central expectations variables. The canonical snapshot contains no current DHER.DE structure.
- Classification / red team: `REJECT`. A larger-cap exception needs a clearly superior, complete setup; this run has neither defensible technical levels nor a clean ordinary earnings thesis separate from the takeover process.
- Pre-mortem: a conventional earnings setup is overwhelmed by takeover terms, negotiation headlines or deal-risk repricing, invalidating nominal R arithmetic.

### EVD.DE — CTS Eventim AG & Co. KGaA
- Discovery origin: prior report continuity / European pass.
- Broker/universe: `ETORO_TRADEABLE: YES`. Public eToro presents EVD.DE as a purchasable XETRA share around €58.40, with about €5.57B market cap and roughly 244k three-month average volume.
- Verification: CTS EVENTIM's official financial calendar and issuer/exchange publication confirm the **H1/Q2 report was published on 2026-08-20**. The report is no longer a future catalyst; the next scheduled quarterly publication is in November, outside the 42-day horizon.
- Classification / red team: `REJECT`. The prior catalyst has already occurred, so the old event cannot be recycled into a new research object merely because the post-report price may still move.
- Pre-mortem: the routine mistakes post-event drift for unpriced catalyst anticipation and enters after the information edge is gone.

### NCH2.DE — thyssenkrupp nucera AG & Co. KGaA
- Discovery origin: catalyst-first European pass.
- Broker/universe: `ETORO_TRADEABLE: YES`. Public eToro presents NCH2.DE as a purchasable XETRA share around €7.56 with roughly €0.95B market cap. Three-month average volume around 90k shares implies only about €0.68M daily value at current price, below even the €3M conditional non-US floor.
- Verification: the official investor calendar shows **Q3/9M results were published on 2026-08-12**. September dates are routine investor conferences rather than a new material reporting or structural catalyst.
- Classification / red team: `REJECT`. The principal financial event is past, the remaining September appearances are not sufficient material catalysts for this method, and liquidity independently fails the broker overlay.
- Pre-mortem: a low-liquidity conference-theme trade is mistaken for a catalyst setup and slippage overwhelms the small learning-phase position.

### HOOD — Robinhood Markets, Inc.
- Discovery origin: current US canonical snapshot / scanner seed.
- Snapshot context: $106.23 on 2026-08-21, +11.70% on the day, 7.35x relative volume, above the 20-day high, RSI 60.98 and about $64.4M canonical average daily dollar volume.
- Broker/universe: `ETORO_TRADEABLE: YES`, but current public eToro data reports market capitalization around **$86.1B**, above the overlay's default $50B exclusion threshold.
- Verification: Robinhood's official IR site confirms Q2 2026 results were released on **2026-07-29**. No new primary-source-verified material event inside the 42-day horizon was identified during this run.
- Classification / red team: `REJECT`. The only fresh canonical anomaly is a strong scanner move, but the name is excluded by market cap and has no qualifying forward catalyst. Scanner momentum cannot override either rule.
- Pre-mortem: the process chases a liquid, high-beta momentum spike in an excluded mega-cap-like name after the principal earnings catalyst has already passed.

## Removed or expired

No active rolling recommendation was removed this week. CELC remains archived and there are no open trades.

## Sources used
- Aroundtown official Investor Relations financial calendar and current public eToro AT1.DE page.
- Delivery Hero official financial reports/calendar and July transaction disclosures, plus current public eToro DHER.DE page.
- CTS EVENTIM official financial calendar / issuer publication and current public eToro EVD.DE page.
- thyssenkrupp nucera official financial calendar and current public eToro NCH2.DE page.
- Robinhood official Investor Relations Q2 2026 release, current public eToro HOOD page, canonical repository snapshot and scanner summary.
- Repository recommendation registry/reviews, trade journal, prior weekly report and prior manifest.

The rolling recommendation registry, append-only review ledger and recommendation book require no state change because there are no active recommendations, no open positions and no surviving new research object. The dated weekly decision archive therefore contains zero review rows.
