# Weekly Research and Decision Review — 2026-09-27

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: GPT-5.6 Sol / continuity-first, evidence-gated catalyst-first
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`
- Snapshot generated: 2026-09-25 22:15 UTC; 0 rows. Public dated broker data supplements this empty snapshot but does not replace it.
- Prior report reviewed: `research/candidates-2026-09-20.md` and matching manifest
- Active recommendations reviewed: none
- Open positions reviewed: none
- Preliminary pool: 8 names — 4 Europe/XETRA and 4 US
- Final classifications: 0 `ACTIONABLE` / 0 `EARLY_WATCH` / 8 `REJECT`
- Scanner input: reviewed; no signal falls inside the configured seven-day lookback. Latest recorded scanner signal remains VOW3.DE on 2026-09-04.
- Weekly decision: **NO NEW TRADE**

## Prior recommendation audit

There are no non-terminal recommendations. FTK.DE and LW were removed on 2026-09-20 after their Early-Watch phases entered the Actionable horizon without a defensible setup. This run rechecks their still-future events only to avoid accidental resurrection; neither becomes a new recommendation.

## Existing positions

None. `trades.csv` contains no open positions.

## Coming-week decision sheet

No candidate has a complete trigger-ready setup. **NO NEW TRADE.**

## New research

### CAG — Conagra Brands, Inc. — REJECT
- Primary event: issuer release schedules fiscal Q1 2027 results for **2026-09-30**, three calendar days away.
- Broker / universe: eToro presents CAG as a purchasable stock; delayed data show a core-universe market cap and ample liquidity.
- Rejection reason: binary event inside ACT-NOW territory and the canonical snapshot has no current row. No defensible multi-session trigger, structure-based invalidation, first target or >=1.5R exists.
- Red-team verdict: `REJECT`.

### JBL — Jabil Inc. — REJECT
- Primary event: issuer release schedules Q4/FY2026 results for **2026-09-30 before market**, three calendar days away.
- Broker / universe: eToro offers JBL shares, but current broker evidence places it in the larger-cap exception bucket.
- Rejection reason: imminent binary earnings, no justified larger-cap exception, and no canonical structure for valid setup math.
- Red-team verdict: `REJECT`.

### AYI — Acuity Inc. — REJECT
- Primary event: issuer release schedules fiscal Q4/FY2026 results for **2026-10-01 at 06:00 ET**, followed by the 08:00 ET call, four calendar days away.
- Intervening event check: Acuity declared its ordinary quarterly dividend on September 24; that release does not move the October 1 earnings date.
- Broker / universe: eToro offers AYI shares; delayed evidence places market cap in the core universe.
- Rejection reason: event is inside ACT-NOW territory but there is no canonical multi-session structure. A broker day range is not acceptable stop evidence.
- Red-team verdict: `REJECT`.

### LW — Lamb Weston Holdings, Inc. — REJECT / NO RESURRECTION
- Primary event: issuer release still schedules fiscal Q1 2027 results for **2026-10-06**, nine calendar days away.
- Broker / universe: eToro continues to present LW as a purchasable stock with core-universe market cap and preferred liquidity.
- Continuity: recommendation `REC-LW-2026-0913` is already terminal (`expired`) after the 2026-09-20 review.
- Rejection reason: no new thesis or structure appears in the canonical input; the same binary date cannot recreate a recommendation that expired for lack of setup.
- Red-team verdict: `REJECT`.

### FTK.DE — flatexDEGIRO SE — REJECT / NO RESURRECTION
- Primary event: official calendar schedules September monthly KPIs for **2026-10-05 at 08:30 CEST**, eight calendar days away; Q3 publication remains October 21.
- Broker / universe: eToro presents FTK.DE as a purchasable XETRA share with core-universe market cap and preferred non-US liquidity.
- Continuity: recommendation `REC-FTK-2026-0906` is already terminal (`invalidated`) after the 2026-09-20 review.
- Rejection reason: canonical snapshot remains empty, no new structure has appeared, and the prior recommendation was removed when the KPI event entered the Actionable horizon without a setup.
- Red-team verdict: `REJECT`.

### DB1.DE — Deutsche Börse AG — REJECT
- Primary event: issuer calendar and September 17 regulatory announcement verify Q3 publication for **2026-10-20**, 23 calendar days away.
- Intervening financing: issuer's September 9 €600m convertible-bond offering remains material setup context.
- Broker / universe: eToro presents DB1.DE as a purchasable XETRA share, but market cap is near the top of the larger-cap exception bucket.
- Rejection reason: no clearly superior swing setup exists to justify the larger-cap exception, and the canonical snapshot has no structure row.
- Red-team verdict: `REJECT`.

### SAP.DE — SAP SE — REJECT
- Primary event: official investor calendar schedules Q3 2026 results for **2026-10-21**, 24 calendar days away.
- Broker: eToro offers SAP.DE as a XETRA share.
- Rejection reason: eToro market-cap evidence remains far above the default €/$50B exclusion threshold.
- Red-team verdict: `REJECT`.

### DBK.DE — Deutsche Bank AG — REJECT
- Primary event: official financial calendar schedules Q3 earnings for **2026-10-28**, 31 calendar days away.
- Broker: eToro presents DBK.DE as a purchasable XETRA share with ample liquidity.
- Rejection reason: eToro reports market capitalization around €75.8B, above the default €/$50B exclusion threshold; no exception applies.
- Red-team verdict: `REJECT`.

## Red-team synthesis

The skeptical pass rejected every name. CAG, JBL and AYI are too close to binary earnings to justify anticipation without current structured setup evidence. FTK.DE and LW already failed promotion and are terminal recommendation objects. DB1.DE lacks a justified larger-cap exception and carries convertible-financing complexity. SAP.DE and DBK.DE fail the default mega-cap/universe gate. The empty canonical snapshot means no candidate can support structure-derived levels, so no broker day low or arbitrary percentage stop was substituted.

## Sources used

Primary sources opened: Conagra Brands August 31 release; Jabil September 9 release; Acuity August 28 release, October 1 event page and September 24 dividend release; Lamb Weston September 8 release; flatexDEGIRO financial calendar; Deutsche Börse Q3 calendar/regulatory announcement; SAP investor calendar; Deutsche Bank financial calendar.

Market/broker/repository sources: `data/research_snapshot.csv`, `data/research_snapshot.meta.json`, `research/scanner-summary.md`, `data/scanner_signals.csv`, public eToro instrument pages, prior `research/candidates-2026-09-20.md` and matching manifest, `data/recommendations.csv`, `data/recommendation_reviews.csv`, `trades.csv`, `RISK_RULES.md`, `SETUPS.md`, and current research-method files.
