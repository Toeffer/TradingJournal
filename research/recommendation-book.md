# Rolling Recommendation Book

Auto-generated from `data/recommendations.csv`. Research decisions are not trade executions.

## Current decision load

- Active recommendations: 2
- Archived/removed recommendations: 3
- Actions: monitor: 1 | wait_pullback: 1

## Active recommendations

| Ticker | Status | This week | Setup | Trigger | Expiry | Stop | Target | Next review |
|---|---|---|---|---:|---|---:|---:|---|
| PATH | carry | monitor | — | — | — | — | — | 2026-11-15 |
| TUI1.DE | upgraded | wait_pullback | — | — | — | — | — | 2026-11-15 |

### Decision reasons

- **PATH** — monitor: Carry at monitor; no setup exists and none can be computed. This repository holds no PATH price history (snapshot carries only ARRY and GRAB) and all quote hosts are unreachable, so entry, stop, target and R are unavailable rather than merely unattractive. The expectations work added this run argues actively against pre-event entry: Q3 FY27 guidance is revenue USD440-445m and ARR USD1.992-1.997bn, consensus revenue is ~USD441.1m - essentially the guidance midpoint, so no cushion - and last quarter PATH beat on revenue (USD410.26m vs USD397.77m expected) yet fell ~9.77% after hours. Event is 25 days out with no nearer verified trigger; USD13.00 reference sits below the ~USD14.04 50-day average.
- **TUI1.DE** — wait_pullback: Upgraded on repository-verified price structure, not on news. The 2026-11-03 XETRA session closed EUR7.384 above the prior 20-session high of EUR6.986 on 3.28x average volume (+5.94%), ending a base that had held since 2026-08-11 - the only breakout with >=2x volume among all 46 tickers in the repository EU universe. The 18:07Z run recorded no such breakout existed. It is still not an entry: a structural stop below the EUR6.990 breakout-day low gives EUR0.45 risk against a EUR7.40 retest, and the nearest supply (EUR7.75-7.908 August swing cluster) yields only 0.78-1.13R; 1.5R would need EUR8.075, above the August high. A ~EUR7.20 stop would manufacture 1.8R but is ~1x the EUR0.194 ATR14 and is not invalidation. Secondary EUR7.57 Nov 6 close is already 2.5% above the breakout level, so do not chase. Wait for a retest holding EUR7.384 or a tight consolidation above it that permits >=1.5R.

## Recently removed

- **FTK.DE** — invalidated: Monitoring phase ended without a valid Actionable setup as the catalyst entered the 0-21 day window; archive unless a genuinely new thesis/event creates a new research object.
- **LW** — expired: Early-Watch phase expired without a valid Actionable setup as earnings entered the 0-21 day window; archive after this review.
- **CELC** — archived: Archive management recommendation after the human confirms trade closure or journal reconciliation. SATISFIED 2026-08-10.
