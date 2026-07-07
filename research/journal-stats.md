# Journal Stats

Auto-generated from `trades.csv` on 2026-07-07 12:29 UTC. Do not edit by hand.
Arithmetic only — the behavioral review in AGENTS.md is still the real review.

## Closed trades

- Trades closed: 10 (of 15 total; 5 open)
- With computable R: 8 — **every closed trade without a stop is invisible to R stats**
- Win rate (R-trades): 50%
- Avg win: +1.56R | Avg loss: -0.83R | Worst: -1.00R
- **Expectancy per trade: +0.37R**
- Total P&L: +16.32 € | Profit factor: 1.29

### By source

| source | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| own | 3 | 2 | 50% | +1.36 | -20.68 |
| routine | 7 | 6 | 50% | +0.04 | +37.00 |

### By setup_type

| setup_type | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 7 | 6 | 50% | +0.36 | -16.93 |
| base | 1 | 0 | — | — | +27.33 |
| breakout | 1 | 1 | 0% | -0.31 | -2.36 |
| special-situation | 1 | 1 | 100% | +1.10 | +8.28 |

### By risk_rating

| risk_rating | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 7 | 6 | 50% | +0.36 | -16.93 |
| Med | 3 | 2 | 50% | +0.40 | +33.25 |

### Realized R by week

| Week | Trades closed | Realized R | Weekly limit (-4.0R) |
|---|---:|---:|---|
| 2026-W26 | 1 | — | ok |
| 2026-W27 | 9 | +2.93 | ok |

## Open positions

| Trade | Ticker | Sector | Entry | Stop | Size (€) | Catalyst date |
|---|---|---|---:|---:|---:|---|
| 2026-0004 | CELC | — | 89.86 | 85.37 | — | 2026-07-17 |
| 2026-0011 | RHM | — | 956.6 | 922.6 | 131.62 | 2026-08-06 |
| 2026-0014 | OPFI | — | 9.93 | 9.00 | 85 | — |
| 2026-0016 | CELH | — | 33.16 | 31.06 | 150 | — |
| 2026-0017 | KGX.DE | — | 45.43 | 41.22 | 127 | — |

## Rule checks (RISK_RULES.md)

- ⚠️ 2026-0007 (ALI1.DE): size €174.19 > €150 cap.

## Data gaps (fill these for the review to work)

- 2026-0003 (AYI): missing followed_plan, lesson, stop_price
- 2026-0006 (FCEL): missing followed_plan, lesson, setup_type
- 2026-0007 (ALI1.DE): missing followed_plan, lesson, stop_price, setup_type
- 2026-0008 (AMD): missing followed_plan, lesson, setup_type
- 2026-0009 (DAL): missing lesson, setup_type
- 2026-0010 (ENR.DE): missing followed_plan, lesson, setup_type
- 2026-0012 (ELF): missing followed_plan, lesson, setup_type
- 2026-0013 (MSM): missing followed_plan, lesson
- 2026-0015 (NBIS): missing followed_plan, lesson, setup_type
- 2026-0004 (CELC): missing sector, setup_type
- 2026-0011 (RHM): missing sector, setup_type
- 2026-0014 (OPFI): missing sector, setup_type, catalyst
- 2026-0016 (CELH): missing sector, catalyst
- 2026-0017 (KGX.DE): missing sector, setup_type, catalyst

