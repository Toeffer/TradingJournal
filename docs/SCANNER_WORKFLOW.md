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

### Indicator columns (measurement-only)

Since 2026-07, every recorded signal also carries five classic technical
indicators, computed deterministically by `scanner/indicators.py` (stdlib-only,
TradingView conventions; idea adapted from oft3r/agentic-trading-desk):

| Column | Meaning |
|---|---|
| `rsi14` | Wilder's RSI, 14 periods |
| `ema20_dist_pct` | price vs EMA20, in % |
| `ema50_dist_pct` | price vs EMA50, in % |
| `macd_hist_pct` | MACD(12,26,9) histogram as % of price |
| `bb_percent_b` | Bollinger(20,2) %B — 0 = lower band, 1 = upper band |

These columns **do not contribute to the score**. They exist so the return
backfill can later answer questions like "did signals above their EMA50
follow through better?" — if a column separates forward returns once enough
rows are filled, promoting it into the score is a phase-transition decision
(MASTERPLAN), never a quiet tweak. US signals compute them from Alpaca bars
(`lookback_days = 150` for warm-up); EU signals from the accumulated history,
so they stay blank until enough sessions exist.

### Market regime columns (cross-asset context)

`data/market_regime.csv` additionally records three cross-asset ratios as
20-trading-day % changes plus a `cross_asset_score` (-3..+3, one vote per
ratio beyond ±1%):

- `credit_hyg_lqd_20d_pct` — HYG vs LQD (credit risk appetite)
- `size_iwm_spy_20d_pct` — IWM vs SPY (small-cap risk appetite)
- `risk_xly_xlp_20d_pct` — XLY vs XLP (consumer discretionary vs staples)

The `regime` label formula (SPY vs 50d MA + universe breadth) is **unchanged**
so existing regime history stays comparable; the new columns are context for
the Phase 2 regime-scaled-exposure decision.

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

### Scheduling reality and the timing policy

GitHub Actions cron is **best-effort**: on this repo, scheduled starts have been
observed 1.5-2.5 hours late (e.g. all of 2026-07-01 ran ~2h behind). No cron
syntax fixes that — it's queueing on GitHub's side. `workflow_dispatch` runs, by
contrast, start within seconds.

The timing step in `scanner.yml` therefore works like this:

- Each target time has a CEST cron and a CET cron; the step detects Berlin's
  current UTC offset and **skips only the wrong-season duplicate**.
- Crons fire ~5 minutes early; if the runner starts before the target, it waits.
- **Late runs still scan** (up to 3.5h late). A late scan is a valid observation:
  relative volume is normalized by elapsed session time, and same-day dedup in
  `scanner_signals.csv` keeps one row per ticker/day. Late data beats no data —
  the old policy of skipping runs more than 30 minutes late silently produced
  zero scheduled scans on delayed days.
- Runs later than 3.5h after their slot are skipped as stale.

### Exact timing (optional upgrade): external scheduler -> workflow_dispatch

If scan timing needs to be tight (e.g. the 15:50 open-momentum scan), trigger the
workflow from an external scheduler instead of relying on GitHub cron:

1. Create a fine-grained GitHub personal access token scoped to this repo with
   **Actions: read and write** permission only.
2. On any reliable scheduler (cron-job.org free tier, a home server/Raspberry Pi
   cron, or a cloud scheduler), create one job per scan time that POSTs:

   ```text
   POST https://api.github.com/repos/<owner>/TradingJournal/actions/workflows/scanner.yml/dispatches
   Authorization: Bearer <token>
   Accept: application/vnd.github+json
   Body: {"ref": "main"}
   ```

3. Keep the GitHub crons as a fallback; duplicate runs are harmless (same-day
   dedup) and the digest/summary files regenerate idempotently.

The token stays in the external scheduler's secret store — never in this repo.

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

## EU scanner (XETRA/LSE)

`scanner/run_scan_eu.py` (workflow: `.github/workflows/scanner-eu.yml`) scans the
`scanner/universe_eu.txt` universe — XETRA-first, because XETRA trades in EUR
(no FX on a EUR account) and has no UK stamp duty; LSE `.L` symbols are
supported but each buy costs 0.5% stamp duty plus GBP exposure.

Data sources — a free-by-default chain, because the Phase 1 rule says no paid
data before the pipeline proves itself. **Yahoo is primary** (since
2026-07-12): it is the only source that has actually delivered data from
GitHub-hosted runners, and trying the dead sources first stamped 2-3 failure
warnings into every report.

1. **Yahoo Finance** chart API (`scanner/yahoo_eu.py`) — keyless, one request
   per ticker, same symbol format as the repo. Each response also carries ~6
   months of daily bars, which the scanner merges into
   `data/eu_quote_history.csv` (fill-missing only), so the history warm-up
   disappears without any seeding step.
2. **FMP** — only if the optional `FMP_API_KEY` secret is set (richest
   fields). Not required; don't buy a plan for this.
3. **Twelve Data** (`scanner/twelvedata_eu.py`) — only if the
   `TWELVE_DATA_API_KEY` secret is set. **The free Basic plan does NOT
   include XETRA/LSE market data** (diagnosed 2026-07-04, reconfirmed
   2026-07-09: `/quote` returns 404/symbol-not-found for XETRA and LSE
   symbols that the free `/stocks` directory itself lists; `plan_category:
   basic`). The integration stays wired for a possible future plan upgrade —
   with a paid plan it is the best source here because the quote payload
   includes `previous_close` and `average_volume`. It is paced to the plan's
   per-minute credit limit (config `[eu.twelvedata] credits_per_minute`),
   and fails fast when the entire first batch is rejected so a gated plan
   costs seconds, not minutes.
4. **Stooq** keyless CSV — works from residential IPs, but is unusable from
   GitHub-hosted runners: Stooq rate-limits/blocks the shared runner egress
   IPs (observed 2026-07-03 — every scan got HTTP 404 on batch quotes and the
   seeder got empty 200 responses for all 46 tickers). Note Stooq uses `.UK`
   where eToro/FMP use `.L` — the tooling maps this automatically.

Each scan report names the source actually used in its `Data:` line. As long
as Yahoo keeps answering, the fallbacks are never attempted and reports carry
no source warnings.

The scanner self-accumulates history into `data/eu_quote_history.csv` — every
run upserts today's bar, and the 17:40 post-close run finalizes it.

**Seeding is now optional**: Yahoo (the primary source) backfills ~6 months of daily
bars automatically on every successful scheduled run, so the 20d/50d breakout
components are fully active from the first scan that reaches Yahoo. The Stooq
seeder (`python scanner/seed_eu_history.py`) still works **locally from a
residential IP** (commit `data/eu_quote_history.csv` afterwards) — but do not
run it via the workflow's `seed_history` input: GitHub runners hit the Stooq
block (the 2026-07-03 attempt seeded 0 bars; the seeder now exits nonzero in
that case instead of looking green). If neither Yahoo nor seeding has filled
the history yet:

- Day-move and price-vs-open work from day one; relative volume and change-%
  derive from the accumulated history as it grows.
- Breakout components (20d/50d highs) activate after
  `min_history_days_for_breakout` sessions (default 15); until then candidates
  carry a "history N/15 days" warning and score lower. This is expected — do not
  raise thresholds to compensate.
- EU return backfill and proposal simulation read the same accumulated history
  instead of Alpaca, so all downstream loops work identically. EU signals land in
  `data/scanner_signals.csv` with `market = EU-XETRA` / `EU-LSE`, and
  `research/scanner-summary.md` breaks outcomes down by market.

Schedule (Berlin): 09:20 early momentum after the XETRA open, 11:20 mid-morning,
15:10 afternoon (before US-open noise), 17:40 post-close bar finalization. The
timing step uses the same late-run policy as the US scanner. Both scanner
workflows share one concurrency group so they never write the signals CSV
simultaneously.

## Return backfill

`scanner/backfill_returns.py` runs after each scan (wired into `scanner.yml`). For
any recorded signal where 1/3/5/10/21 trading days have now elapsed, it fetches
daily bars from Alpaca and fills `one_day_return` / `three_day_return` /
`five_day_return` / `ten_day_return` / `twenty_one_day_return` relative to the
price recorded at scan time (roughly next day / week / two weeks / month). It only
fills blank cells and is safe to re-run. Without this, the 30-day evaluation below
has no data to work from.

## Signal summary

`scanner/summarize_signals.py` runs after the backfill and regenerates
`research/scanner-summary.md`: outcome stats by score bucket and source (average,
median, hit rate, best/worst per horizon) plus a runner board listing every
recorded signal with its 1d/5d/10d/21d outcomes. It is a derived artifact —
regenerated on every run, never edited by hand, and never a trade signal.

## Proposal draft cards

`scanner/draft_proposals.py` (wired into both scanner workflows, after the
signal summary) regenerates `research/proposal-drafts.md`: for each of the
latest scan day's alerts (score ≥ `min_score_to_alert`, excluding tickers that
are already an open trade or a live proposal) it emits a **pre-filled draft
proposal card** — mechanical fields filled, judgment fields (`entry_price`,
`stop_price`, `target_price`, `thesis`, `planned_r`) left as blank TODOs. It is
a research aid to make logging a real proposal fast; it **never** writes to
`data/proposals.csv` or `trades.csv`, and it is not a trade signal. The file
also carries a "Proposal hygiene" check that flags any open proposal breaking
the `SETUPS.md` card standard (bad `setup_type`, `planned_r` < 1.5, blank
required fields). Derived artifact — regenerated every run, never hand-edited.

## 30-day evaluation

After 30 days, check:

- Did scores above 70 actually follow through better than scores 60-69?
- Did Finviz-seeded names perform better than scanner-universe-only names?
- Did Claude/GPT agreement improve candidate quality?
- Did the scanner reduce time spent or only create more noise?
- Did any actual trades come from scanner candidates, and how did they compare to your own ideas?
