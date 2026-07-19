# Weekly Research and Decision Review — 2026-07-19
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode: GPT-5.6 Thinking / hybrid, evidence-gated
- Input snapshot / SHA-256: `data/research_snapshot.csv` / `7346ed76fa81090f28c17b1b3ef440e13269f80b85798a797678473500a71f60`
- Snapshot generated: 2026-07-17 20:13:14 UTC; 2 rows
- Prior reports reviewed: `research/candidates-2026-07-12.md` and its manifest
- Active recommendations reviewed: 0 (`data/recommendations.csv` contains only its header)
- Open positions reviewed: 1 (`CELC`, trade `2026-0004`)
- New leads / Actionable / Early Watch / Reject: 2 / 0 / 0 / 3
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

No durable recommendations are currently recorded in `data/recommendations.csv`. The 2026-07-12 run also produced no Actionable or Early Watch candidates, so there is no recommendation ID to carry or remove.

## Existing positions

### CELC — MANAGE
- Linked trade: `2026-0004`, opened 2026-06-23 at 89.86; recorded stop 85.37.
- Original thesis / current thesis: the trade was tied to the FDA decision for gedatolisib. Celcuity's primary-source release originally stated a July 17, 2026 PDUFA goal date, but the FDA approval was announced early on July 14, 2026. The binary catalyst has therefore occurred and the original pre-decision thesis is complete.
- Intervening material events: Celcuity announced an upsized convertible-note offering in June, and on July 14 announced FDA approval of REVTORPYK (gedatolisib). Financing/dilution and commercialization execution now replace PDUFA timing as the main risks.
- Original invalidation: preserve the recorded 85.37 level for audit purposes; this review does not infer that the stop, size, or position changed.
- Event/time risk: the recorded catalyst date is stale because approval occurred three days earlier. The repository has no current CELC row in the canonical snapshot, so this run cannot evidence a fresh technical management level.
- This week's management review: reconcile the still-open journal status against the broker and decide the post-approval thesis explicitly. Do not treat the completed approval event as a reason to add. A separate post-event setup would require fresh dated market data, structure-based levels, and a new recommendation/proposal.

## Coming-week decision sheet

**NO NEW TRADE.** Neither current snapshot lead has a primary-source-verified future catalyst and complete setup for the next five trading sessions.

### DHER.DE — REMOVE / REJECT
- Continuity: new scanner lead from the canonical snapshot.
- What changed: the July 14 snapshot recorded a 5.76% move, 2.38 relative volume, a 20-day breakout and defensive market regime. Public eToro evidence supports stock/share availability under ticker `DHER.DE`; the snapshot's approximately €20.7M average daily value passes the preferred non-US liquidity floor.
- Why this action: price/volume behavior is discovery context only. No opened Delivery Hero primary source explicitly stated a binding catalyst inside the 42-day discovery horizon during this run. Snapshot market cap is blank, and no structure-based entry, stop and target with at least 1.5R was established.
- Red-team verdict: `REJECT`. Removing the scanner move leaves no verified event or independent setup.

### S — REMOVE / REJECT
- Continuity: new scanner lead; eToro uses ticker `S.US`.
- What changed: the July 14 snapshot recorded a 7.49% move, 3.00 relative volume and a 20-day breakout. Public eToro evidence supports stock/share availability and indicates a core-universe market cap, but the canonical snapshot records only about $8.70M average daily dollar volume.
- Why this action: the snapshot liquidity is below even the $10M conditional US floor. No opened SentinelOne primary source explicitly stated a future catalyst inside 42 days. The scanner breakout alone is not a setup.
- Red-team verdict: `REJECT` on liquidity and evidence before level construction.

## New research

### CELC — Celcuity
- Discovery origin: open-position continuity review.
- Evidence and classification: `REJECT` as a new candidate because the July 17 PDUFA event already occurred early on July 14. The approval is material to management of the existing position, but it is not a future catalyst supporting a new entry.
- Why it did not displace a carry-over name: no active research recommendation exists, current structured price/liquidity data are absent from the snapshot, and a post-approval setup was not established.

## European preliminary sourcing

The canonical snapshot contains only one current EU/XETRA row (`DHER.DE`). Recent prior-report EU names were reviewed for continuity, but QIA.DE, HAG.DE and AIXA.DE were not promoted because this run had no current snapshot rows plus opened primary-source dates inside 42 days for them. The required four-name EU preliminary target could not be met without padding with stale or unverified objects.

## Removed or expired
- CELC new-entry catalyst thesis — expired/completed when FDA approval was announced on 2026-07-14, ahead of the recorded 2026-07-17 goal date.
- DHER.DE — rejected: no verified future catalyst or complete setup.
- S / S.US — rejected: snapshot liquidity below conditional US floor and no verified future catalyst.

## Sources used
- Repository instructions and method files on `main`.
- Canonical structured data: `data/research_snapshot.csv`, generated 2026-07-17; SHA-256 `7346ed76fa81090f28c17b1b3ef440e13269f80b85798a797678473500a71f60`.
- Repository continuity: `data/recommendations.csv`, `trades.csv`, and `research/candidates-2026-07-12.md` plus manifest.
- Celcuity primary sources: https://ir.celcuity.com/news-releases/news-release-details/celcuity-announces-fda-acceptance-new-drug-application and https://ir.celcuity.com/news-releases/news-release-details/celcuity-announces-fda-approval-revtorpyktm-gedatolisib
- Broker evidence: https://www.etoro.com/markets/dher.de/ and https://www.etoro.com/markets/s.us/
