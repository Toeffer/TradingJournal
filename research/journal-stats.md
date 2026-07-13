# Journal Stats

Auto-generated from `trades.csv` on 2026-07-13 13:38 UTC. Do not edit by hand.
Arithmetic and executable rule checks only; the behavioral review remains human work.

## Closed trades

- Trades closed: 13 (of 17 total; 4 open)
- With computable R: 11 — **every closed trade without a stop is invisible to R stats**
- Win rate (R-trades): 45%
- Avg win: +2.06R | Avg loss: -0.89R | Worst: -1.00R
- **Expectancy per trade: +0.45R**
- Total P&L: +31.67 € | Profit factor: 1.44

### By source

| source | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| own | 5 | 4 | 25% | +0.18 | -35.87 |
| routine | 8 | 7 | 57% | +0.61 | +67.54 |

### By setup_type

| setup_type | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 8 | 7 | 43% | +0.16 | -28.86 |
| base | 1 | 0 | — | — | +27.33 |
| breakout | 1 | 1 | 0% | -0.31 | -2.36 |
| post-earnings-drift | 1 | 1 | 100% | +4.07 | +30.54 |
| special-situation | 2 | 2 | 50% | +0.05 | +5.02 |

### By risk_rating

| risk_rating | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 9 | 8 | 38% | +0.02 | -32.12 |
| High | 1 | 1 | 100% | +4.07 | +30.54 |
| Med | 3 | 2 | 50% | +0.40 | +33.25 |

### Realized R by week

| Week | Trades closed | Realized R | Weekly limit (-4.0R) |
|---|---:|---:|---|
| 2026-W26 | 1 | — | ok |
| 2026-W27 | 9 | +2.93 | ok |
| 2026-W28 | 3 | +2.07 | ok |

### Realized R by day

| Date | Trades closed | Realized R | Daily limit (-2.0R) |
|---|---:|---:|---|
| 2026-06-25 | 1 | — | ok |
| 2026-06-29 | 2 | -1.00 | ok |
| 2026-06-30 | 3 | +5.81 | ok |
| 2026-07-01 | 1 | -0.31 | ok |
| 2026-07-02 | 3 | -1.57 | ok |
| 2026-07-07 | 1 | -1.00 | ok |
| 2026-07-08 | 2 | +3.07 | ok |

## Open positions

| Trade | Ticker | Sector | Entry | Stop | Size (€) | Catalyst date |
|---|---|---|---:|---:|---:|---|
| 2026-0004 | CELC | — | 89.86 | 85.37 | — | 2026-07-17 |
| 2026-0011 | RHM | — | 956.6 | 922.6 | 131.62 | 2026-08-06 |
| 2026-0014 | OPFI | — | 9.93 | 9.00 | 85 | — |
| 2026-0016 | CELH | — | 33.16 | 31.06 | 150 | 2026-08-06 |

## Rule checks (config/risk.toml)

- ⚠️ 2026-0003 (AYI): held through binary event at €138.00 > €75 half-size cap.
- ⚠️ 2026-0007 (ALI1.DE): size €174.19 > €150 cap.
- ⚠️ 2026-0013 (MSM): held through binary event at €150.00 > €75 half-size cap.
- ⚠️ 2026-0018 (VERA): held through binary event at €150.00 > €75 half-size cap.
- ⚠️ 2026-0019 (PENG): held through binary event at €150.00 > €75 half-size cap.

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
- 2026-0017 (KGX.DE): missing followed_plan, lesson, setup_type
- 2026-0018 (VERA): missing followed_plan, lesson
- 2026-0019 (PENG): missing followed_plan, lesson
- 2026-0004 (CELC): missing sector, setup_type
- 2026-0011 (RHM): missing sector, setup_type
- 2026-0014 (OPFI): missing sector, setup_type, catalyst
- 2026-0016 (CELH): missing sector

