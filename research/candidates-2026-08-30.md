# Weekly Research and Decision Review — 2026-08-30
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode: GPT-5.6 Sol / continuity-first evidence-gated hybrid
- Input snapshot / SHA-256: `data/research_snapshot.csv` / `fe776d6dd03470275e96ebf3a7c5de3f96a6608b7548ea6df676d5249b1ff619`
- Snapshot metadata generated: 2026-08-29 02:07:52 UTC; 1 canonical row (DBK.DE), signal timestamp 2026-08-26 11:55:02 +0200.
- Repository base commit: `5983b901689a67ec8879e2bd632e25153b898228`.
- Prior report reviewed: `research/candidates-2026-08-23.md` and matching manifest, plus rolling recommendation state and trade journal.
- Active recommendations reviewed: 0. `REC-CELC-2026-0004` remains archived.
- Open positions reviewed: 0. `trades.csv` contains no open rows.
- Preliminary pool: 5 leads; 4 European/XETRA names (DBK.DE, AT1.DE, DHER.DE, TUI1.DE) and 1 US name (PATH). Discovery was hybrid and deliberately not padded beyond traceable current leads.
- New leads / Actionable / Early Watch / Reject counts: 5 / 0 / 0 / 5.
- Weekly decision: **NO NEW TRADE**.

## Prior recommendation audit
There are no non-terminal recommendation objects. CELC remains archived after trade reconciliation, so no registry or append-only review change is required.

## Existing positions
No open positions are recorded in `trades.csv`; no `manage` review is required.

## Coming-week decision sheet
No candidate has both qualifying evidence and a complete structure-based setup for the next five trading sessions. **NO NEW TRADE.**

PATH has a verified September 3 earnings event and passes eToro tradeability, market-cap and liquidity gates, but it is absent from the canonical snapshot and has already risen about 11% over the prior week on the public broker page. Without current normalized multi-session structure, a pre-earnings trigger, stop and target would be manufactured rather than evidence-based. The event is only four days away, so the routine rejects it instead of anticipating the binary report.

## New research

### PATH — UiPath Inc.
- Discovery origin: catalyst-first US pass; previously appeared as an older scanner lead but is not a current scanner row.
- Broker/universe: `ETORO_TRADEABLE: YES`. Public eToro presents PATH as a purchasable stock. Current public broker data shows about $18.15 price, $9.4B market cap and 67.36M three-month average volume, placing it in the core market-cap universe with very strong liquidity.
- Verified catalyst: UiPath's official IR release dated August 6 states that it will report fiscal Q2 2027 results after market close on **September 3, 2026** and host a 5:00 p.m. ET call the same day.
- Expectations / priced-in: eToro shows PATH up about 11.01% over the prior week, near the upper part of its $9.20-$19.80 52-week range. The broker's displayed analyst consensus is Hold with a $13.86 target. That makes pre-event expectations/crowding a material concern rather than a clean unpriced catalyst.
- Setup: no valid current setup. PATH is not in the canonical snapshot, so the routine cannot derive a normalized breakout/retest or pullback structure. A broker day low is not a valid stop basis.
- Classification / red team: `REJECT`. The primary date and broker/liquidity gates pass, but a four-day-away binary event without defensible structure and >=1.5R is event anticipation. Preferred policy is post-information or exit-before-event, not buying merely because earnings are near.
- Pre-mortem: the process chases an 11% weekly run into earnings, uses an arbitrary nearby stop, and an overnight gap makes the planned R meaningless.

### DBK.DE — Deutsche Bank AG
- Discovery origin: current canonical snapshot / EU scanner seed.
- Snapshot context: €34.485 on August 26, +3.87% on the day, 2.36x relative volume, 20-day breakout, RSI 70.76 and about €140.2M average daily value.
- Broker/universe: `ETORO_TRADEABLE: YES`; public eToro shows a purchasable XETRA share around €34.635. However, eToro reports market capitalization around **€75.29B**, above the overlay's default €/$50B exclusion threshold.
- Event verification: Deutsche Bank's official 2026 financial calendar lists its next earnings report for **October 28, 2026**, 59 days away and outside the 42-day discovery horizon.
- Classification / red team: `REJECT`. The current scanner breakout is not a catalyst, the next verified financial event is outside the horizon, and market cap independently fails the default universe gate.
- Pre-mortem: the routine mistakes a liquid bank momentum breakout for a qualifying catalyst setup and ignores the explicit mega-cap exclusion.

### AT1.DE — Aroundtown SA
- Discovery origin: prior-report continuity / European pass.
- Broker/universe: `ETORO_TRADEABLE: YES`; public eToro shows AT1.DE around €2.02 with €2.24B market cap and 2.41M three-month average volume.
- Verification: Aroundtown's official IR page confirms that H1 2026 results were published on **August 26, 2026**. Its next scheduled Q3 report is **November 25, 2026**, outside the 42-day horizon.
- What changed: last week's forward H1 catalyst has completed. The company says H1 results were in line with guidance, so the old event cannot be recycled as a new anticipation trade.
- Classification / red team: `REJECT`. No qualifying future catalyst inside 42 days remains.
- Pre-mortem: the routine retains a stale research object after the information event has already occurred.

### DHER.DE — Delivery Hero SE
- Discovery origin: prior-report continuity / European pass.
- Broker/universe: `ETORO_TRADEABLE: YES`; the public eToro instrument remains available. Market cap remains in the larger-cap exception bucket rather than the preferred core universe.
- Verification: Delivery Hero's official IR release confirms that Q2/H1 results were published on **August 27, 2026**. The company raised full-year guidance, while the voluntary Uber takeover offer at €41.50 per share remains material special-situation context. The official financial calendar currently shows no upcoming scheduled dates.
- What changed: last week's forward earnings catalyst has completed and the takeover process dominates ordinary swing-trade expectations.
- Classification / red team: `REJECT`. No new primary-source-verified dated event inside 42 days was identified, and takeover headlines make ordinary stop-based R non-linear.
- Pre-mortem: the routine treats a takeover-driven stock as a normal post-results swing and underestimates headline/gap risk.

### TUI1.DE — TUI AG
- Discovery origin: prior European scanner/research context.
- Broker/universe: `ETORO_TRADEABLE: YES`; public eToro presents TUI1.DE as a purchasable XETRA share.
- Verification: the previously researched Q3 event occurred on August 12, 2026. No new primary-source-verified material event inside the current 42-day horizon was established in this run.
- Classification / red team: `REJECT`. The prior catalyst is complete and no replacement dated catalyst passed verification.
- Pre-mortem: the routine carries forward a familiar ticker without genuinely new evidence.

## Removed or expired
No active rolling recommendation was removed this week. CELC remains archived and there are no open trades.

## Sources used
- UiPath official Investor Relations August 6 earnings-call announcement and current public eToro PATH page.
- Deutsche Bank official 2026 financial calendar, canonical repository snapshot, scanner summary and current public eToro DBK.DE page.
- Aroundtown official Investor Relations results/news and financial calendar, plus current public eToro AT1.DE page.
- Delivery Hero official August 27 Q2/H1 release and financial calendar, plus public eToro DHER.DE page.
- Public eToro TUI1.DE page and prior verified repository research for the completed August event.
- Repository recommendation registry, trade journal, prior weekly report/manifest and scanner outputs.

The rolling recommendation registry, append-only review ledger and recommendation book require no state change because there are no active recommendations, no open positions and no surviving new research object. The dated weekly decision archive therefore contains zero review rows.
