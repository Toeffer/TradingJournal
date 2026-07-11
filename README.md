# TradingJournal

A private trading journal for recording trades, reviewing decisions, and measuring
whether process quality improves over time.

This repository measures and prepares; it never places orders and is not financial
advice.

## Core boundaries

- `trades.csv` is the source of truth for real trades.
- `data/proposals.csv` contains fully specified ideas, traded or not.
- `data/scanner_signals.csv` contains scanner observations, never trades.
- `config/risk.toml` contains executable risk and horizon values.
- `RISK_RULES.md` explains those values for the human.
- `research/*.md` contains research or generated reports and is not edited by hand.

## Repository structure

```text
.
├── AGENTS.md
├── RESEARCH_BRIEF.md
├── RISK_RULES.md
├── SETUPS.md
├── MASTERPLAN.md
├── trades.csv
├── config/
│   └── risk.toml
├── data/
│   ├── proposals.csv
│   ├── scanner_signals.csv
│   ├── market_regime.csv
│   ├── eu_quote_history.csv
│   ├── finviz_watchlist.csv
│   └── finviz_watchlist_archive.csv   # created when seeds expire
├── scanner/
│   ├── run_scan.py
│   ├── run_scan_eu.py
│   ├── backfill_returns.py
│   ├── summarize_signals.py
│   ├── simulate_proposals.py
│   ├── expire_finviz_seeds.py
│   └── io_utils.py
├── scripts/
│   ├── journal_stats.py
│   ├── weekly_digest.py
│   └── validate_data.py
├── tests/
└── .github/workflows/
    ├── ci.yml
    ├── scanner.yml
    ├── scanner-eu.yml
    ├── journal.yml
    └── digest.yml
```

## Quick start

1. Log every real trade in `trades.csv`.
2. Log every fully specified surviving idea in `data/proposals.csv`, including
   ideas you pass on.
3. Put longer narratives in `notes/<trade_id>.md`.
4. Run validation after editing source data:

   ```bash
   python scripts/validate_data.py
   ```

5. Regenerate stats locally when needed:

   ```bash
   python scripts/journal_stats.py
   python scanner/summarize_signals.py
   python scanner/simulate_proposals.py
   ```

6. Run the test suite before merging code changes:

   ```bash
   python -m pip install -e '.[dev]'
   ruff check scanner scripts tests
   pytest
   ```

CI runs compilation, linting, tests, and source-data validation on pull requests.

## Catalyst and holding horizons

The weekly research process separates discovery from action:

- **0–21 calendar days:** eligible for the actionable shortlist.
- **22–42 calendar days:** Early Watch only, unless a separately verified trigger
  inside 21 days creates the current setup.

Proposals use a separate trading horizon:

- Default `max_holding_days`: **10 trading sessions**.
- Catalyst-driven proposals default to `exit_before_catalyst = yes`.
- The 21-trading-day scanner return is retained only as slow research context; the
  primary scanner evaluation windows are 1, 3, 5, and 10 sessions.

## Scanner workflow

The US scanner uses Alpaca IEX data and optional manual Finviz discovery seeds.
The EU scanner uses the configured FMP / Twelve Data / Stooq / Yahoo fallback chain
and stores local daily history.

Manual Finviz rows now require `added_at` and may specify `expires_at`. The scheduled
US workflow archives expired rows before scanning so an old screenshot cannot add
score indefinitely.

Repository secrets:

```text
APCA_API_KEY_ID
APCA_API_SECRET_KEY
FMP_API_KEY             # optional
TWELVE_DATA_API_KEY     # optional
```

Scanner workflows preserve diagnostic reports when a provider fails, but the
workflow run is marked failed instead of silently appearing healthy.

## Proposal schema

```csv
proposal_id,date,ticker,direction,source,setup_type,regime,entry_price,stop_price,target_price,planned_r,catalyst,catalyst_date,thesis,risk_rating,max_holding_days,exit_before_catalyst,status,triggered_date,resolved_date,exit_price,sim_r,traded,trade_id,notes
```

The simulator uses adjusted US daily bars, conservative same-bar handling, explicit
holding periods, and pre-catalyst exits.

## Security and privacy

Never commit broker/API credentials, account numbers, full brokerage exports,
balance screenshots, `.env` files, or proprietary material that should stay local.
Use `.env.example` only for placeholders and GitHub Actions secrets for credentials.

## Current phase

Foundation/learning phase. The system is intentionally small-sized and process-first.
The immediate goal is complete records, an actively used proposal ledger, and enough
clean observations to prove or kill each pipeline before adding complexity.
