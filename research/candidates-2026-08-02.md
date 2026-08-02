# Weekly Research and Decision Review — 2026-08-02
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode: GPT-5.6 Thinking / continuity-first evidence-gated hybrid
- Input snapshot / SHA-256: `data/research_snapshot.csv` / `e62c2720bf30c2d6b8d9d960ce6a8425ba14d6d2d4435deaa8ae5021e10a7651`
- Prior reports reviewed: `research/candidates-2026-07-26.md` and matching manifest
- Active recommendations reviewed: none in `data/recommendations.csv`
- Open positions reviewed: CELC trade `2026-0004`
- New leads / Actionable / Early Watch / Reject counts: 5 / 0 / 0 / 6
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

No active rows were present in `data/recommendations.csv`. The prior CELC research object remains relevant only because `trades.csv` still records an open position; it is not a new-entry candidate.

## Existing positions

### CELC — MANAGE
- Linked trade: `2026-0004`
- Original thesis / current thesis: the original July 17 FDA-decision thesis is complete; Celcuity announced approval on July 14. The current thesis is commercial execution, financing and adoption, not the original binary catalyst.
- Original invalidation: 85.37, preserved from the journal. Research does not infer that the stop, position or execution changed.
- Event/time risk: Celcuity's IR site lists no upcoming event. The issuer describes late-Q3 launch and Q3 sNDA plans, but no exact binding date is available.
- This week's management review: reconcile the journal's still-open status with the broker and review the position against the original invalidation and maximum-holding discipline. No add-on entry is supported by this run.

## Coming-week decision sheet

No candidate has a complete, validator-compatible trigger-ready setup. **NO NEW TRADE.**

## New research

### BC8.DE — Bechtle AG
- Discovery origin: EU-XETRA canonical snapshot plus issuer financial calendar.
- Evidence and classification: `REJECT`. The August 12 interim report is primary-source verified; eToro publicly presents BC8.DE as a purchasable XETRA stock. Snapshot ADV is approximately €5.77M, above the preferred non-US floor, and eToro reports a core-universe market capitalization around €3.84B.
- Expectations / priced-in: expectations evidence is insufficiently specific. The snapshot's +9.47% move, 6.35x relative volume, RSI above 74 and breakout above the 20-day high imply substantial near-term enthusiasm may already be reflected.
- Risk: event gap, post-breakout reversal, limited expectations evidence and stale-to-current price divergence. EUR listing avoids direct currency conversion for the EUR account, but XETRA hours, settlement and holiday-calendar risk still apply.
- Red-team verdict: `REJECT`. The catalyst is only 10 days away, which is inside the Actionable horizon, but the name lacks a defensible setup, structure-based levels and sufficient planned R. Repository validation does not permit an inside-21-day name to remain Early Watch.
- Why it did not become an entry: arbitrary current-price entry or broker-page day-low stop would violate the method.

### MBG.DE — Mercedes-Benz Group AG
- Discovery origin: EU-XETRA canonical snapshot.
- Evidence and classification: `REJECT`. The issuer's Q2 report occurred on July 28, 2026, before this run. The next verified financial report is October 28, outside the 42-day discovery horizon. Roadshows on August 3–4 are not sufficiently material intermediate catalysts for this process.

### SHL.DE — Siemens Healthineers AG
- Discovery origin: EU-XETRA canonical snapshot.
- Evidence and classification: `REJECT`. The snapshot move followed the late-July reporting window; no future primary-source-verified material catalyst inside 42 days was established. It is also a larger-cap exception name and would need a clearly superior setup.

### PATH — UiPath Inc.
- Discovery origin: US canonical snapshot.
- Evidence and classification: `REJECT`. Snapshot ADV is approximately $24.53M, just below the preferred $25M US floor, and no primary-source-verified material catalyst inside 42 days was opened and confirmed. Momentum alone is not a catalyst.

### RHM.DE — Rheinmetall AG
- Discovery origin: required fourth EU preliminary lead from issuer-calendar research.
- Evidence and classification: `REJECT`. Public eToro data places the market capitalization near the upper edge of, or above depending on timestamp, the $50B-equivalent default exclusion boundary. The stock was also up strongly into the period, raising crowding/priced-in risk. It did not earn the required exceptional treatment.

## Removed or expired
- CELC — rejected for any new or add-on research entry because the original catalyst is complete and no exact verified forward catalyst currently exists. The existing position remains a separate `manage` object pending human reconciliation.

## Sources used
- Bechtle financial calendar: https://www.bechtle.com/de-en/about-bechtle/investors/financial-calendar
- Bechtle eToro page: https://www.etoro.com/de/markets/bc8.de
- Mercedes-Benz financial calendar: https://group.mercedes-benz.com/investors/events/
- Celcuity investor relations and events: https://ir.celcuity.com/ and https://ir.celcuity.com/events-presentations
- Siemens Healthineers eToro page: https://www.etoro.com/markets/shl.de
- Rheinmetall eToro page: https://www.etoro.com/markets/rhm.de
- Canonical repository snapshot and metadata, `trades.csv`, and the July 26 report/manifest.
