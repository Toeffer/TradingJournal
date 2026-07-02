# Pump Scanner Workflow

This branch adds a lightweight scanner for unusual-volume / breakout candidates.

It is a **measurement and candidate-discovery tool**, not an auto-trader and not a buy/sell signal. Actual trades still belong in `trades.csv` only after you decide to trade.

## Why this exists

The scanner gives Claude/GPT a cleaner input set:

1. Python collects objective price/volume anomalies.
2. Finviz free screener can be used as a manual discovery surface.
3. Claude and GPT review the same candidates independently.
4. Only actual trades are logged in `trades.csv`.
5. After 30+ days, the journal can test whether scanner scores had any predictive value.

## Files added

```text
scanner/config.toml              # thresholds and data-source config
scanner/universe.txt             # starter U.S. ticker universe
scanner/run_scan.py              # scanner script
scanner/backfill_returns.py      # fills in 1/3/5-trading-day returns once elapsed
data/scanner_signals.csv         # signal dataset, deduped to one row per ticker/day
data/finviz_watchlist.csv        # optional manual Finviz seed tickers
research/scans/                  # Markdown reports per run
.github/workflows/scanner.yml    # scheduled/manual GitHub Actions workflow
```

## Data sources

### Alpaca

The script uses Alpaca Market Data when these repository secrets are present:

```text
APCA_API_KEY_ID
APCA_API_SECRET_KEY
```

Start with the free tier/IEX feed. Upgrade only if the scanner proves useful in the journal.

**IEX caveat:** the IEX feed only reports IEX-exchange volume, a minority of
consolidated U.S. tape. `volume`, `avg_volume_20d`, and `min_avg_volume_20d` are all
in IEX-only terms, not real total liquidity — read them as relative/internal signals,
not absolute share counts.

### Finviz free tier

The script deliberately does **not** scrape Finviz. Free Finviz is best used manually:

1. Open the Finviz screener.
2. Filter for unusual movers, for example:
   - Price above $2
   - Average volume above 500k
   - Relative volume above 2
   - Current change roughly +3% to +15%
   - Strong technical setup / new high / above moving averages
3. Copy interesting tickers into `data/finviz_watchlist.csv`.
4. The scanner gives those names a small score boost but still validates price/volume via Alpaca.

Example row:

```csv
ticker,added_at,finviz_screen,notes
SOUN,2026-06-29,unusual-volume,"AI/voice name from Finviz rel-volume screen"
```

## How scoring works

The scanner scores each ticker using:

- relative volume, normalized against the elapsed fraction of the US regular
  session (9:30-16:00 America/New_York) rather than the full-day average — a
  mid-session snapshot only has a partial day's volume, so comparing it to a
  full-day average made the trigger nearly unreachable except right at the close
- daily price move
- breakout above 20-day high
- breakout above 50-day high as context
- price above the current daily open
- not being too extended versus the 5-day high
- liquidity above the minimum volume floor
- optional Finviz manual seed boost

Default thresholds live in `scanner/config.toml`.

Interpretation:

| Score | Meaning |
|---:|---|
| 80+ | urgent watch, but still needs human review |
| 70-79 | strong watch |
| 60-69 | interesting / log for measurement |
| <60 | ignored |

Note: `min_score_to_record` was temporarily lowered to 40 (2026-06-30 to 2026-07-01)
while relative-volume normalization was being fixed, so `data/scanner_signals.csv`
contains rows scoring 40-59 from that window. Treat them as their own bucket in any
score-vs-return analysis; don't mix them into the 60+ buckets or drop them.

## Running manually

From the repo root:

```bash
python scanner/run_scan.py
```

Without Alpaca secrets, the script still writes a report explaining that market data is not configured. It will not fail destructively.

## Running online through GitHub Actions

The workflow is at `.github/workflows/scanner.yml`.

Scheduled GitHub Actions workflows run from the repository's default branch. The scanner workflow is now on `main`, so scheduled runs are active when Actions are enabled.

The schedule is aligned to the U.S. regular-market open. During Berlin summer time, U.S. regular trading starts at 15:30 Europe/Berlin, so the main useful scans are shortly after the open:

```text
15:50 Berlin — first useful early-momentum scan after the initial volatility burst
16:10 Berlin — early confirmation scan
16:45 Berlin — cleaner VWAP / continuation check
17:30 Berlin — mid-session continuation scan
21:15 Berlin — late-day / next-day setup scan
```

GitHub cron doesn't follow DST, so `scanner.yml` lists both a CEST-offset and a
CET-offset cron for each of the five times above, targeting the same Berlin
wall-clock time year-round. Whichever set doesn't match the season's actual Berlin
offset fires an hour off from the intended local time instead of silently drifting;
runs are non-destructive and same-day duplicates are deduped, so the extra/off-target
runs are harmless.

Finviz free-tier data is manual. For best results, update `data/finviz_watchlist.csv` around 15:40-15:45 Berlin so the 15:50 and 16:10 runs can validate fresh Finviz names through Alpaca.

## Human review prompt

Use the canonical prompt in `SCANNER_RESEARCH_PROMPT.md` after each scanner report —
it is the single source of truth for the review layer (an earlier, slightly different
copy embedded here caused drift).

Run the same prompt in Claude and GPT. Overlap is higher priority; disagreement is a reason to dig harder, not automatically reject.

## Guardrails

- The scanner never writes to `trades.csv`.
- A high score is not a trade signal.
- Do not size up because the scanner found a name.
- Do not hold through binary events unless it fits `RISK_RULES.md`.
- Keep all API keys in GitHub Actions secrets, never in the repo.
- Review results after 30 days before paying for better data.
- `data/scanner_signals.csv` is deduped to one row per (date, ticker), keeping the
  highest-scoring run of the day, so a name that stays elevated all session doesn't
  overweight later score-bucket stats.

## Return backfill

`scanner/backfill_returns.py` runs after each scan (wired into `scanner.yml`). For
any recorded signal where 1/3/5 trading days have now elapsed, it fetches daily bars
from Alpaca and fills `one_day_return` / `three_day_return` / `five_day_return`
relative to the price recorded at scan time. It only fills blank cells and is safe
to re-run. Without this, the 30-day evaluation below has no data to work from.

## 30-day evaluation

After 30 days, check:

- Did scores above 70 actually follow through better than scores 60-69?
- Did Finviz-seeded names perform better than scanner-universe-only names?
- Did Claude/GPT agreement improve candidate quality?
- Did the scanner reduce time spent or only create more noise?
- Did any actual trades come from scanner candidates, and how did they compare to your own ideas?
