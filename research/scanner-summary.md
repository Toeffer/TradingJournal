# Scanner Signal Summary

Auto-generated from `data/scanner_signals.csv` on 2026-07-07 16:08 UTC. Do not edit by hand.

Not financial advice and not a trade signal. Returns are close-to-signal-price
moves on IEX data; the signal price is an intraday snapshot, so treat these as
rough process measurements, not precise performance numbers. Small sample sizes
prove nothing — look for patterns only once dozens of rows have filled in.

## Coverage

- Signals recorded: 17
- With 1-day outcome: 17
- With 21-day outcome: 0

## Outcomes by score bucket

| Group | Signals | Horizon | Filled | Avg | Median | Hit rate | Best | Worst |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| 40-59 | 8 | 1d | 8 | +0.99% | -0.26% | 38% | +5.84% | -1.68% |
|  |  | 3d | 8 | +1.17% | +1.45% | 62% | +7.98% | -4.19% |
| 60-69 | 5 | 1d | 5 | -1.52% | +1.03% | 60% | +3.38% | -13.15% |
| 70-79 | 2 | 1d | 2 | -0.28% | -0.28% | 50% | +1.66% | -2.23% |
| 80+ | 2 | 1d | 2 | -3.65% | -3.65% | 50% | +0.31% | -7.60% |

## Outcomes by source

| Group | Signals | Horizon | Filled | Avg | Median | Hit rate | Best | Worst |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| alpaca | 11 | 1d | 11 | +0.90% | -0.02% | 45% | +5.84% | -2.23% |
|  |  | 3d | 7 | +1.59% | +2.25% | 71% | +7.98% | -4.19% |
| alpaca+finviz_manual | 6 | 1d | 6 | -2.91% | -0.56% | 50% | +3.38% | -13.15% |
|  |  | 3d | 1 | -1.76% | -1.76% | 0% | -1.76% | -1.76% |

## Runner board (every recorded signal)

| Date | Ticker | Score | Signal price | Day move | 1d | 5d | 10d | 21d |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-07-06 | RIVN | 60 | 19.8100 | +6.39% | -13.15% | — | — | — |
| 2026-07-03 | SMMT | 60 | 15.4400 | +7.37% | +2.72% | — | — | — |
| 2026-07-03 | RIVN | 80 | 18.6200 | +8.51% | -7.60% | — | — | — |
| 2026-07-03 | HOOD | 70 | 112.7100 | +3.71% | +1.66% | — | — | — |
| 2026-07-03 | CELH | 60 | 33.1850 | +4.13% | -1.58% | — | — | — |
| 2026-07-02 | RIVN | 80 | 19.6000 | +14.22% | +0.31% | — | — | — |
| 2026-07-02 | PLTR | 64 | 131.9700 | +4.95% | +1.03% | — | — | — |
| 2026-07-02 | OWL | 60 | 9.1750 | +6.32% | +3.38% | — | — | — |
| 2026-07-02 | HOOD | 70 | 119.8400 | +10.27% | -2.23% | — | — | — |
| 2026-07-01 | PLTR | 49 | 125.7100 | +7.72% | +4.98% | — | — | — |
| 2026-07-01 | HIMS | 56 | 37.5400 | +8.45% | -1.68% | — | — | — |
| 2026-07-01 | GIS | 59 | 37.8050 | +8.56% | -1.43% | — | — | — |
| 2026-07-01 | SOFI | 50 | 18.7150 | +4.29% | -0.61% | — | — | — |
| 2026-07-01 | S | 40 | 17.7400 | +4.51% | +1.35% | — | — | — |
| 2026-07-01 | TOST | 50 | 29.0150 | +4.24% | -0.02% | — | — | — |
| 2026-07-01 | GRAB | 50 | 3.9050 | +3.86% | -0.51% | — | — | — |
| 2026-07-01 | CELH | 40 | 31.8500 | +8.70% | +5.84% | — | — | — |

## How to read this

- **Hit rate** = share of filled outcomes that were positive at that horizon.
- If higher score buckets don't show better outcomes than lower ones once the
  sample grows, the score has no edge and chasing alerts is unjustified.
- Compare against trades in `trades.csv` with `source = scanner` to see whether
  your selection among alerts beats the alert average.
