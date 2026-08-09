# Weekly Research and Decision Review — 2026-08-09
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode: GPT-5.6 / continuity-first evidence-gated hybrid
- Input snapshot / SHA-256: `data/research_snapshot.csv` / `dfd34b091f74d19c7e71ebf0832006e3c765f5a4800f1c394fe37c7ba7783202`
- Prior reports reviewed: `research/candidates-2026-08-02.md` and matching manifest; six-week continuity context checked through repository history
- Active recommendations reviewed: none were present before this run
- Open positions reviewed: CELC trade `2026-0004`
- Preliminary pool: 7 discussed leads (5 snapshot/scanner names plus BC8.DE continuity and CELC management); 4 European names were explicitly checked. The configured count of 12 was not padded because the current canonical snapshot has only five rows and unsupported calendar names are not evidence.
- New leads / Actionable / Early Watch / Reject counts: 5 / 0 / 0 / 7
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

`data/recommendations.csv` was empty before this run, so there were no durable prior recommendation IDs to carry. The previous BC8.DE research object was re-opened because its verified August 12 event is now three days away. It still does not qualify for a trigger-ready setup. CELC remains relevant only because `trades.csv` still records trade `2026-0004` as open.

## Existing positions

### CELC — MANAGE
- Linked trade: `2026-0004`
- Original thesis / current thesis: the original July 17 FDA-decision thesis is complete; Celcuity announced FDA approval on July 14. The issuer now describes commercial launch in late Q3 and an sNDA submission in Q3, but neither is an exact binding date.
- Original invalidation: 85.37, preserved from the journal. This review does not infer a stop change, sale, add, or other execution.
- Event/time risk: Celcuity's current IR events page lists no upcoming event. The position is therefore no longer supported by the original binary-event thesis and needs human reconciliation against the broker and maximum-holding discipline.
- This week's management review: **manage only**. Reconcile whether the trade is actually still open; do not add exposure based on the completed approval catalyst.

## Coming-week decision sheet

No candidate has a complete, evidence-based trigger, structure-derived invalidation and target with at least 1.5R. **NO NEW TRADE.**

## New research

### TUI1.DE — TUI AG
- Discovery origin: EU-XETRA canonical snapshot / scanner seed.
- Broker/universe: eToro Germany page presents TUI1.DE as a purchasable XETRA stock; eToro market cap is about €3.6B, inside the core universe. EUR listing avoids direct FX conversion for the EUR account.
- Verified catalyst: TUI's official financial calendar schedules the FY2026 Q3 quarterly statement for **2026-08-12** (3 calendar days away).
- Market data: canonical snapshot dated 2026-08-03 records €7.754, approximately €24.65M average daily value, +3.22% daily change, 2.18x relative volume, a 20-day breakout, RSI 70.36 and 2.40% five-day extension. Preferred non-US liquidity is satisfied.
- Expectations / priced-in: TUI's May H1 release confirmed revised FY2026 underlying EBIT guidance of €1.1B–€1.4B after April's geopolitical guidance reset. The stock had already broken out on elevated volume in the snapshot, so a favorable summer-trading outcome may be partly reflected.
- Classification: `REJECT` for this run. The catalyst is inside the 21-day Actionable horizon, but the committed snapshot does not provide enough price structure to define a non-arbitrary trigger, invalidation and first target with >=1.5R. An arbitrary current-price entry or day-low stop would violate the method.
- Red-team verdict: `REJECT`. Strongest objection: the event is imminent and the stock is already extended; entering without a structure-based setup would be event anticipation rather than confirmation.
- Pre-mortem: the trade would fail because the market already priced a strong summer season, while guidance uncertainty around geopolitics/fuel or Markets + Airline margins dominates the Q3 release.

### BC8.DE — Bechtle AG
- Discovery origin: prior report continuity plus issuer calendar.
- Broker/universe: eToro presents BC8.DE as a purchasable XETRA stock; market cap is around €4B, core universe.
- Verified catalyst: Bechtle's financial calendar confirms the interim report and conference call on **2026-08-12**.
- What changed: Bechtle's July 28 primary-source ad-hoc announcement already disclosed strong preliminary Q2 figures, said EBT significantly exceeded market expectations, and raised 2026 guidance. The August 12 report therefore follows a substantial pre-announcement rather than being a clean undisclosed earnings catalyst.
- Expectations / priced-in: the positive surprise and guidance raise are already public. This sharply increases the risk that the remaining event is detail/confirmation rather than a fresh positive catalyst.
- Classification: `REJECT`. BC8.DE is absent from the current canonical snapshot, so this run lacks current normalized structure for a defensible trigger/stop/target; more importantly, the key positive information was pre-announced on July 28.
- Red-team verdict: `REJECT`. A fresh long would risk chasing a move whose fundamental surprise has already been disclosed.

### HAG.DE — HENSOLDT AG
- Discovery origin: EU-XETRA canonical snapshot / scanner seed.
- Broker/universe: eToro lists HAG.DE as a purchasable XETRA share. Snapshot ADV is about €29.42M, comfortably above the preferred non-US floor.
- Verification: HENSOLDT's official calendar shows the H1 report occurred on July 31. The next listed financial report is November 5, outside the 42-day discovery horizon. Investor conferences begin September 2, but they are not treated as sufficiently material binding catalysts for this process.
- Snapshot context: €94.80 on August 7, +4.98%, 3.56x relative volume, breakout above the 20-day high, RSI 74.17 and 14.26% above EMA20.
- Classification / red team: `REJECT`. The move is scanner momentum after the reporting event, without a verified material forward catalyst inside the discovery horizon; the technical state is also extended.

### R3NK.DE — RENK Group AG
- Discovery origin: EU-XETRA canonical snapshot / scanner seed.
- Broker/universe: eToro lists R3NK.DE as a purchasable XETRA stock with core-universe market cap around €4.3B. Snapshot average daily value is about €21.95M.
- Verification: RENK's official IR calendar states H1 2026 results and conference call occurred on **2026-08-06**, before this run. The next 9M statement is November 5, outside 42 days.
- Snapshot context: €52.26 on August 6, +7.75%, 2.68x relative volume and a 20-day breakout. That observation is event-day reaction, not a future catalyst.
- Classification / red team: `REJECT`. The relevant event has already occurred and no new primary-source-verified material event is inside the discovery horizon.

### PATH — UiPath Inc.
- Discovery origin: US canonical snapshot / scanner seed.
- Broker/universe: eToro presents PATH as a purchasable stock; eToro market cap observations place it in the core universe. Canonical snapshot ADV is about $31.74M, above the preferred US floor.
- Verification: UiPath's official IR FAQ says quarterly earnings dates are announced by press release and posted to Events & Presentations when determined. The current opened IR events page does not provide a new Q2 FY2027 earnings date. A historical September cadence is not verification.
- Snapshot context: $14.94 on August 7, +6.75%, 2.56x relative volume, 20-day breakout, RSI 73.69 and 18.13% above EMA20.
- Classification / red team: `REJECT`. Strong momentum and tradeability survive, but no primary-source-verified future catalyst date exists and the move is extended. Scanner momentum alone is not a setup.

### PLTR — Palantir Technologies
- Discovery origin: US canonical snapshot / scanner seed.
- Snapshot context: $170.14 on August 7, +9.10%, 5.10x relative volume, 20-day breakout and RSI 72.23.
- Classification / red team: `REJECT` at discovery. PLTR is an obvious crowded headline AI mega-cap and therefore excluded by the broker/universe overlay by default. Its scanner score cannot override the >$50B / crowded-AI exclusion.

## Removed or expired
- CELC — `REJECT` for any new or add-on research entry. The July FDA catalyst is complete and no exact new issuer event is scheduled. Existing trade `2026-0004` is separately carried as `manage` pending human reconciliation.
- BC8.DE — prior research object remains rejected; the positive Q2 surprise and guidance raise were pre-announced July 28, and no current canonical structure supports a trigger-ready setup.

## Sources used
- TUI official financial calendar and FY2026 H1 release.
- Bechtle official financial calendar, July 28 ad-hoc preliminary Q2/guidance announcement, and investor consensus page.
- HENSOLDT official financial calendar.
- RENK official IR calendar.
- UiPath official IR FAQ and Events & Presentations.
- Celcuity official investor-relations and events pages.
- Public eToro instrument pages for broker availability and market-cap context.
- Canonical repository snapshot, scanner summary, trade journal, prior report and manifest.
