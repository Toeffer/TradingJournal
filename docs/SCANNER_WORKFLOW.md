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
data/scanner_signals.csv         # append-only signal dataset
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

- relative volume
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

## Running manually

From the repo root:

```bash
python scanner/run_scan.py
```

Without Alpaca secrets, the script still writes a report explaining that market data is not configured. It will not fail destructively.

## Running online through GitHub Actions

The workflow is at `.github/workflows/scanner.yml`.

Important: scheduled GitHub Actions workflows only run from the repository's default branch. Because this implementation is intentionally on `feature/scanner-workflow` and not merged to `main`, the schedule will not become active yet.

Once you are ready, either:

1. run it manually if GitHub exposes the workflow for the branch, or
2. open a pull request and test, or
3. merge after review so the schedule starts running from `main`.

The planned schedule is four U.S.-session checks during Berlin summer time:

```text
15:05 Berlin — pre-market / setup scan
16:00 Berlin — first U.S. open confirmation
17:30 Berlin — continuation scan
21:15 Berlin — late-day / next-day setup scan
```

## Human review prompt

Use this after each scanner report:

```text
Review this scanner report as a trading research analyst. Do not tell me what to buy.
For each top candidate, check: current news, catalyst within 1-14 days, dilution/offering risk,
short interest if available, options activity if available, sector sympathy, chart invalidation,
and whether the move is probably already too late. Mark each: Deep dive / Watch / Reject.
```

Run the same prompt in Claude and GPT. Overlap is higher priority; disagreement is a reason to dig harder, not automatically reject.

## Guardrails

- The scanner never writes to `trades.csv`.
- A high score is not a trade signal.
- Do not size up because the scanner found a name.
- Do not hold through binary events unless it fits `RISK_RULES.md`.
- Keep all API keys in GitHub Actions secrets, never in the repo.
- Review results after 30 days before paying for better data.

## 30-day evaluation

After 30 days, answer:

- Did 70+ score candidates outperform 60-69 score candidates?
- Did Finviz-seeded names perform better than base-universe names?
- Were alerts early enough to enter calmly, or already too late?
- Which signals mattered most: relative volume, breakout, Finviz seed, or liquidity?
- Did the scanner reduce randomness or increase overtrading?

If the answer is unclear, keep the free tier and collect more data before spending money.
