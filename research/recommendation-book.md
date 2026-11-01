# Rolling Recommendation Book

Auto-generated from `data/recommendations.csv`. Research decisions are not trade executions.

## Current decision load

- Active recommendations: 1
- Archived/removed recommendations: 3
- Actions: monitor: 1

## Active recommendations

| Ticker | Status | This week | Setup | Trigger | Expiry | Stop | Target | Next review |
|---|---|---|---|---:|---|---:|---:|---|
| TUI1.DE | carry | monitor | — | — | — | — | — | 2026-11-08 |

### Decision reasons

- **TUI1.DE** — monitor: Second same-day run (Claude Opus 5, 21:45 UTC): no material change since the 18:00Z review. No trading session has opened in between, the FY2026 results date 2026-12-09 (38 days) is unchanged, and search surfaced no new issuer disclosure. This run could NOT independently re-open the issuer page or the broker page - the session network policy blocks every outbound host except GitHub/Anthropic - so the earlier primary-source verification stands and is not re-asserted here. Still Early Watch distance with no nearer verified trigger and no multi-session XETRA structure in the one-row canonical snapshot; regime is defensive (Oct 31 scan: SPY 755.72 vs 50d 767.48, breadth 22.6%). Monitor only, no trade levels.

## Recently removed

- **FTK.DE** — invalidated: Monitoring phase ended without a valid Actionable setup as the catalyst entered the 0-21 day window; archive unless a genuinely new thesis/event creates a new research object.
- **LW** — expired: Early-Watch phase expired without a valid Actionable setup as earnings entered the 0-21 day window; archive after this review.
- **CELC** — archived: Archive management recommendation after the human confirms trade closure or journal reconciliation. SATISFIED 2026-08-10.
