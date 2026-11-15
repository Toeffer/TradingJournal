# Rolling Recommendation Book

Auto-generated from `data/recommendations.csv`. Research decisions are not trade executions.

## Current decision load

- Active recommendations: 1
- Archived/removed recommendations: 4
- Actions: wait_pullback: 1

## Active recommendations

| Ticker | Status | This week | Setup | Trigger | Expiry | Stop | Target | Next review |
|---|---|---|---|---:|---|---:|---:|---|
| TUI1.DE | carry | wait_pullback | — | — | — | — | — | 2026-11-22 |

### Decision reasons

- **TUI1.DE** — wait_pullback: Second same-day run (21:45Z) using the time-suffixed report; the 18:01Z run's rows are untouched. Evidence unchanged: the 2026-12-09 FY26 results date is 24 days away, outside the 21-day actionable horizon, and no separate verified nearer trigger exists. Measurement changed: data/eu_quote_history.csv does contain 20-session structure the earlier run recorded as unavailable - the 2026-11-10 XETRA close of EUR7.698 is AT the 20-session high (EUR7.70), +15.6% over 20 sessions and +10.7% from the EUR6.956 first mention, on EUR23.1m/day turnover with ATR(14) 2.82%, including a 2026-11-02 volume-expansion session. That is the do-not-chase condition, so the action is refined from monitor to wait_pullback. No entry, stop, target or R is published: the newest bar is three sessions stale, no executable broker quote was obtainable, and price sits at its high.

## Recently removed

- **PATH** — expired: Early Watch expired as earnings entered 0-21 day window without valid setup.
- **FTK.DE** — invalidated: Monitoring phase ended without a valid Actionable setup as the catalyst entered the 0-21 day window; archive unless a genuinely new thesis/event creates a new research object.
- **LW** — expired: Early-Watch phase expired without a valid Actionable setup as earnings entered the 0-21 day window; archive after this review.
- **CELC** — archived: Archive management recommendation after the human confirms trade closure or journal reconciliation. SATISFIED 2026-08-10.
