# Journal Stats

Auto-generated from `trades.csv` on 2026-07-02 16:29 UTC. Do not edit by hand.
Arithmetic only — the behavioral review in AGENTS.md is still the real review.

## Closed trades

- Trades closed: 9 (of 13 total; 4 open)
- With computable R: 7 — **every closed trade without a stop is invisible to R stats**
- Win rate (R-trades): 57%
- Avg win: +1.56R | Avg loss: -0.77R | Worst: -1.00R
- **Expectancy per trade: +0.56R**
- Total P&L: +18.50 € | Profit factor: 1.34

### By source

| source | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| own | 3 | 2 | 50% | +1.36 | -20.68 |
| routine | 6 | 5 | 60% | +0.24 | +39.18 |

### By setup_type

| setup_type | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 6 | 5 | 60% | +0.63 | -14.75 |
| base | 1 | 0 | — | — | +27.33 |
| breakout | 1 | 1 | 0% | -0.31 | -2.36 |
| special-situation | 1 | 1 | 100% | +1.10 | +8.28 |

### By risk_rating

| risk_rating | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 6 | 5 | 60% | +0.63 | -14.75 |
| Med | 3 | 2 | 50% | +0.40 | +33.25 |

### Realized R by week

| Week | Trades closed | Realized R | Weekly limit (-4.0R) |
|---|---:|---:|---|
| 2026-W26 | 1 | — | ok |
| 2026-W27 | 8 | +3.93 | ok |

## Open positions

| Trade | Ticker | Sector | Entry | Stop | Size (€) | Catalyst date |
|---|---|---|---:|---:|---:|---|
| 2026-0004 | CELC | — | 89.86 | 85.37 | — | 2026-07-17 |
| 2026-0009 | DAL | — | 92.75 | 88.57 | 90 | — |
| 2026-0011 | RHM | — | 956.6 | 922.6 | 131.62 | 2026-08-06 |
| 2026-0014 | OPFI | — | 9.93 | 9.00 | 85 | — |

## Rule checks (RISK_RULES.md)

- ⚠️ 2026-0007 (ALI1.DE): size €174.19 > €150 cap.

## Data gaps (fill these for the review to work)

- 2026-0003 (AYI): missing followed_plan, lesson, stop_price
- 2026-0006 (FCEL): missing followed_plan, lesson, setup_type
- 2026-0007 (ALI1.DE): missing followed_plan, lesson, stop_price, setup_type
- 2026-0008 (AMD): missing followed_plan, lesson, setup_type
- 2026-0010 (ENR.DE): missing followed_plan, lesson, setup_type
- 2026-0012 (ELF): missing followed_plan, lesson, setup_type
- 2026-0013 (MSM): missing followed_plan, lesson
- 2026-0015 (NBIS): missing followed_plan, lesson, setup_type
- 2026-0004 (CELC): missing sector, setup_type
- 2026-0009 (DAL): missing sector, setup_type, catalyst
- 2026-0011 (RHM): missing sector, setup_type
- 2026-0014 (OPFI): missing sector, setup_type, catalyst

