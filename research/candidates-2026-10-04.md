# Weekly Research and Decision Review — 2026-10-04

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: GPT-5.6 Sol / continuity-first, evidence-gated catalyst-first
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`
- Snapshot generated: 2026-10-02 22:56 UTC; 0 rows. Public dated broker data supplements this empty snapshot but does not replace it.
- Prior report reviewed: `research/candidates-2026-09-20.md` and matching manifest. No 2026-09-27 artifacts exist on `main`.
- Active recommendations reviewed: 0
- Open positions reviewed: none
- Preliminary pool: 8 names — 5 Europe/XETRA and 3 US/ADR
- Final classifications: 0 `ACTIONABLE` / 0 `EARLY_WATCH` / 8 `REJECT`
- Scanner input: no signal falls inside the seven-day lookback; latest recorded signal remains VOW3.DE on 2026-09-04.
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

No non-terminal recommendation exists. FTK.DE and LW remain terminal objects from the 2026-09-20 review and are not resurrected merely because their events are imminent.

## Existing positions

None. `trades.csv` contains no open positions.

## Coming-week decision sheet

No candidate has a complete trigger-ready setup. **NO NEW TRADE.**

## New research

### SZU.DE — Südzucker AG — REJECT
- Primary event: official calendar confirms the H1 2026/27 report for **2026-10-08**, four days away. A September 28 issuer ad-hoc already disclosed a strong Q2 EBITDA increase and updated guidance.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro presents SZU.DE as a purchasable German share. Core market cap is about €2.4B, but recent three-month average volume near 268k shares at about €11.9 implies only ~€3.2M daily value, in the conditional non-US liquidity range.
- Expectations / priced in: the key positive earnings surprise was pre-announced September 28, making October 8 substantially a detail/confirmation event.
- Rejection reason: event is four days away, liquidity is conditional, and the canonical snapshot has no multi-session structure for a defensible trigger, stop, target and ≥1.5R.
- Red-team verdict: `REJECT`.

### FTK.DE — flatexDEGIRO SE — REJECT
- Continuity: prior recommendation `REC-FTK-2026-0906` is already invalidated and removed.
- Primary event: issuer calendar confirms September monthly KPIs for **2026-10-05 08:30 CEST** and Q3 interim statement for October 21.
- Broker / universe: `ETORO_TRADEABLE: YES`; core market cap around €3.7B and roughly €9.4M daily value from recent eToro data.
- Rejection reason: tomorrow's KPI event is too late for a new pre-event setup, the prior monitoring thesis was already invalidated, and no new canonical structure exists. The October 21 report alone does not justify reopening the old object.
- Red-team verdict: `REJECT`.

### DB1.DE — Deutsche Börse AG — REJECT
- Primary event: issuer/regulatory pages explicitly confirm Q3 results for **2026-10-20**.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro shows about €48.7B market cap and ~€89.7M average daily value, in the larger-cap exception bucket.
- Risk: September's €600M convertible-bond financing remains material intervening context.
- Rejection reason: no canonical setup structure exists and the larger-cap exception is not earned merely by a verified earnings date.
- Red-team verdict: `REJECT`.

### SAP.DE — SAP SE — REJECT
- Primary event: SAP's official IR calendar confirms **2026-10-21** Q3 results.
- Broker: `ETORO_TRADEABLE: YES` on XETRA in EUR.
- Rejection reason: eToro reports market cap around €215B, far above the default €50B exclusion threshold.
- Red-team verdict: `REJECT`.

### DBK.DE — Deutsche Bank AG — REJECT
- Primary event: Deutsche Bank's published financial calendar confirms Q3 earnings for **2026-10-28**.
- Broker: `ETORO_TRADEABLE: YES`; eToro reports about €75.8B market cap and deep liquidity.
- Rejection reason: market cap exceeds the default €50B exclusion threshold; no exception applies.
- Red-team verdict: `REJECT`.

### LW — Lamb Weston Holdings, Inc. — REJECT
- Continuity: prior recommendation `REC-LW-2026-0913` is already expired and removed.
- Primary event: issuer release confirms fiscal Q1 2027 results for **2026-10-06**.
- Broker / universe: `ETORO_TRADEABLE: YES`; eToro shows about $5.95B market cap and ~1.6M three-month average volume.
- Rejection reason: earnings are two days away, the prior Early Watch expired without a setup, and the zero-row canonical snapshot still provides no structure-based pre-event levels.
- Red-team verdict: `REJECT`.

### BLK — BlackRock, Inc. — REJECT
- Primary event: BlackRock's September 30 issuer release confirms Q3 earnings for **2026-10-14** before the NYSE open.
- Broker: `ETORO_TRADEABLE: YES`.
- Rejection reason: eToro reports market cap around $182B, well above the default $50B exclusion threshold.
- Red-team verdict: `REJECT`.

### TSM — Taiwan Semiconductor Manufacturing Co. ADR — REJECT
- Primary event: TSMC's official financial calendar confirms **2026-10-15** Q3 results and an October 8 monthly-sales release.
- Broker: `ETORO_TRADEABLE: YES` for the US ADR.
- Rejection reason: mega-cap/crowded headline-AI exposure is excluded by default; the ADR does not qualify for an exception merely because the dates are verified.
- Red-team verdict: `REJECT`.

## Red-team synthesis

The skeptical pass rejects every lead. The empty canonical snapshot is decisive for setup construction: no broker day range is promoted into a stop, and no candidate receives entry/stop/target math without normalized multi-session evidence. SZU.DE is additionally weakened by conditional liquidity and the September 28 pre-announcement; FTK.DE and LW are stale terminal recommendations; DB1.DE needs an unearned larger-cap exception; SAP.DE, DBK.DE, BLK and TSM fail the default market-cap/crowding universe.

## Sources used

Primary sources opened: Südzucker financial calendar and September 28 ad-hoc; flatexDEGIRO financial calendar; Deutsche Börse Q3/regulatory calendar; SAP IR calendar; Deutsche Bank financial calendar; Lamb Weston September 8 release; BlackRock September 30 release; TSMC financial calendar.

Market/broker sources: canonical repository snapshot and metadata; current scanner files; public eToro instrument pages for Germany/EU availability and dated market figures.
