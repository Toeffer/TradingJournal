# Journal Stats

Auto-generated from `trades.csv` on 2026-07-13 13:45 UTC. Do not edit by hand.
Arithmetic and executable rule checks only; the behavioral review remains human work.

## Closed trades

- Trades closed: 17 (of 18 total; 1 open)
- With computable R: 14 — **every closed trade without a stop is invisible to R stats**
- Win rate (R-trades): 43%
- Avg win: +2.22R | Avg loss: -0.92R | Worst: -1.04R
- **Expectancy per trade: +0.43R**
- Total P&L: +38.08 € | Profit factor: 1.40

### By source

| source | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| own | 8 | 6 | 33% | +0.47 | -9.28 |
| routine | 8 | 7 | 57% | +0.60 | +67.08 |
| scanner+routine | 1 | 1 | 0% | -1.04 | -19.72 |

### By setup_type

| setup_type | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 11 | 9 | 44% | +0.35 | -2.73 |
| base | 1 | 0 | — | — | +27.33 |
| breakout | 1 | 1 | 0% | -0.31 | -2.36 |
| post-earnings-drift | 1 | 1 | 100% | +4.07 | +30.54 |
| scanner-breakout | 1 | 1 | 0% | -1.04 | -19.72 |
| special-situation | 2 | 2 | 50% | +0.05 | +5.02 |

### By risk_rating

| risk_rating | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |
|---|---:|---:|---:|---:|---:|
| (blank) | 13 | 11 | 36% | +0.10 | -25.71 |
| High | 1 | 1 | 100% | +4.07 | +30.54 |
| Med | 3 | 2 | 50% | +0.40 | +33.25 |

### Realized R by week

| Week | Trades closed | Realized R | Weekly limit (-4.0R) |
|---|---:|---:|---|
| 2026-W26 | 1 | — | ok |
| 2026-W27 | 10 | +2.83 | ok |
| 2026-W28 | 6 | +3.15 | ok |

### Realized R by day

| Date | Trades closed | Realized R | Daily limit (-2.0R) |
|---|---:|---:|---|
| 2026-06-25 | 1 | — | ok |
| 2026-06-29 | 2 | -1.00 | ok |
| 2026-06-30 | 3 | +5.81 | ok |
| 2026-07-01 | 2 | -0.31 | ok |
| 2026-07-02 | 3 | -1.67 | ok |
| 2026-07-07 | 2 | -2.00 | **BREACHED** |
| 2026-07-08 | 4 | +5.15 | ok |

## Open positions

| Trade | Ticker | Sector | Entry | Stop | Size (€) | Catalyst date |
|---|---|---|---:|---:|---:|---|
| 2026-0004 | CELC | — | 89.86 | 85.37 | — | 2026-07-17 |

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
- 2026-0011 (RHM): missing followed_plan, setup_type
- 2026-0012 (ELF): missing followed_plan, setup_type
- 2026-0013 (MSM): missing followed_plan, lesson
- 2026-0014 (OPFI): missing followed_plan, lesson, setup_type
- 2026-0015 (NBIS): missing followed_plan, lesson, setup_type
- 2026-0016 (CELH): missing followed_plan, lesson
- 2026-0017 (KGX.DE): missing followed_plan, lesson, setup_type
- 2026-0018 (VERA): missing followed_plan, lesson
- 2026-0019 (PENG): missing followed_plan, lesson
- 2026-0020 (HOOD): missing followed_plan, lesson, stop_price, setup_type
- 2026-0004 (CELC): missing sector, setup_type

