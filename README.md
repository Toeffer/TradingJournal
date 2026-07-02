# TradingJournal

A private trading journal for recording trades, reviewing decisions, and measuring whether process quality is improving over time.

This repository is intended to be the system of record for trades, research notes, risk rules, scanner observations, and periodic self-reviews. It is not financial advice and should not be used as a signal-generation system by itself.

## Goals

- Log trades quickly and consistently.
- Track plan versus execution.
- Measure performance by setup, source, conviction, risk rating, and time period.
- Keep personal risk rules explicit and reviewable.
- Preserve lessons learned without mixing them into raw trade data.
- Collect scanner/research observations separately from actual trades, so the process can be measured before scaling.

## Repository structure

```text
.
├── CLAUDE.md                  # Claude Code session startup guide
├── AGENTS.md                  # Operating instructions for AI-assisted journaling
├── LLM_RESEARCH_PLAYBOOK.md   # Research routine / discovery workflow
├── RESEARCH_BRIEF.md          # Automated weekly research routine spec
├── SCANNER_RESEARCH_PROMPT.md # Claude/GPT review prompt for scanner reports
├── MONTHLY_SELF_GRADE.md      # Monthly review template for the research process
├── RISK_RULES.md              # Personal risk rules (position sizing, loss limits)
├── ETORO_TRADEABILITY.md      # Broker overlay for eToro Germany/EU
├── SECOND_OPINION.md          # Red-team prompt for a second model
├── trades.csv                 # Structured trade log; source of truth for real trades
├── data/
│   ├── scanner_signals.csv    # Append-only scanner signal dataset
│   ├── finviz_watchlist.csv   # Manual Finviz free-tier/Elite seed list
│   └── TradingJournalCandidatesTry_updated.xlsx  # Legacy Excel journal (used to backfill trades.csv; CSV is source of truth)
├── scanner/                   # Optional Python scanner for unusual volume/breakouts
├── notes/                     # Optional longer notes per trade
├── research/
│   └── scans/                 # Scanner reports used as input for Claude/GPT review
└── docs/                      # Architecture, setup, and project notes
```

## Quick start

1. `RISK_RULES.md` is filled in with learning-phase rules (€150/trade fixed sizing).
2. Use `trades.csv` as the structured source of truth — log every real trade.
3. Put longer narratives in `notes/<trade_id>.md` instead of overloading the CSV.
4. Store weekly research outputs in `research/` so reviews can compare ideas against actual trades.
5. Store scanner outputs in `research/scans/` and raw scanner rows in `data/scanner_signals.csv` — these are observations, not trades.
6. Save second-opinion output to `research/second-opinion-YYYY-MM-DD.md` alongside candidates.
7. For scanner reports, use `SCANNER_RESEARCH_PROMPT.md` in both Claude and GPT, then compare overlap/disagreement.
8. Review the journal regularly using `MONTHLY_SELF_GRADE.md` and the review guidance in `AGENTS.md`.

## Scanner workflow

The optional scanner workflow is documented in `docs/SCANNER_WORKFLOW.md`.

It can run through GitHub Actions using Alpaca market-data secrets and a manual Finviz seed list. The scanner never writes to `trades.csv`; it writes candidate observations to `data/scanner_signals.csv` and Markdown reports to `research/scans/`.

Required repository secrets for Alpaca data:

```text
APCA_API_KEY_ID
APCA_API_SECRET_KEY
```

The scheduled workflow lives at `.github/workflows/scanner.yml`. Scheduled runs only become active when that workflow exists on the default branch. While testing on a feature branch, run it manually or open a PR first.

## Trade log schema

`trades.csv` uses this header:

```csv
trade_id,date_opened,ticker,direction,sector,catalyst,catalyst_date,setup_type,thesis,entry_price,stop_price,target_price,position_size,conviction,source,candidate_ref,risk_rating,planned_r,status,date_closed,exit_price,pnl,r_multiple,followed_plan,lesson
```

See `AGENTS.md` for field definitions and logging rules.

## Security and privacy

Do not commit:

- Broker API keys or tokens
- Alpaca, Finviz, or other data-provider credentials
- Account numbers
- Full brokerage exports with personal identifiers
- Screenshots showing balances or account details
- `.env` files
- Proprietary strategy data that should stay local

Use `.env.example` for placeholders only. Use GitHub Actions secrets for API keys.

## Status

Learning phase. Risk rules are set (€150/trade fixed sizing, R-based loss limits), the trade log is live in `trades.csv` (backfilled from the legacy Excel journal), the weekly research routine is active, and the scanner workflow runs on a schedule from `main` via GitHub Actions.
