# Rolling Recommendation Book

Auto-generated from `data/recommendations.csv`. Research decisions are not trade executions.

## Current decision load

- Active recommendations: 2
- Archived/removed recommendations: 1
- Actions: monitor: 2

## Active recommendations

| Ticker | Status | This week | Setup | Trigger | Expiry | Stop | Target | Next review |
|---|---|---|---|---:|---|---:|---:|---|
| FTK.DE | downgraded | monitor | — | — | — | — | — | 2026-09-20 |
| LW | carry | monitor | — | — | — | — | — | 2026-09-20 |

### Decision reasons

- **FTK.DE** — monitor: Second same-day review (21:39 UTC). No evidence changed since the 17:00 UTC run: no reachable source produced new price, governance or calendar data on flatexDEGIRO, and FTK.DE is absent from data/eu_quote_history.csv so this pass has no structure for it. Status held at downgraded rather than relaxed - the governance concern is unresolved - and not lowered further, because a blocked network is not evidence against a thesis. This pass did not re-open the October 5 primary source; that verification belongs to the 17:00 run.
- **LW** — monitor: Second same-day review (21:39 UTC). Thesis unchanged, so status moves new -> carry. Independent structured market data re-confirms the universe and liquidity gates - market cap USD6.58B (core bucket) and 1.56M average shares, roughly USD75M average daily value - without relying on the 17:00 run's broker-page figures. Still monitor: the October 6 release is 23 days out (Early Watch, not Actionable) and no US price history was reachable this pass, so no trigger, stop, target or planned R >= 1.5 can be constructed.

## Recently removed

- **CELC** — archived: Archive management recommendation after the human confirms trade closure or journal reconciliation. SATISFIED 2026-08-10.
