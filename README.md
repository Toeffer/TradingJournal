# TradingJournal

A private trading journal for recording trades, reviewing decisions, and measuring whether process quality is improving over time.

This repository is intended to be the system of record for trades, research notes, risk rules, and periodic self-reviews. It is not financial advice and should not be used as a signal-generation system by itself.

## Goals

- Log trades quickly and consistently.
- Track plan versus execution.
- Measure performance by setup, source, conviction, risk rating, and time period.
- Keep personal risk rules explicit and reviewable.
- Preserve lessons learned without mixing them into raw trade data.

## Repository structure

```text
.
├── AGENTS.md                  # Operating instructions for AI-assisted journaling
├── LLM_RESEARCH_PLAYBOOK.md   # Research routine / discovery workflow
├── MONTHLY_SELF_GRADE.md      # Monthly review template for the research process
├── RISK_RULES.md              # Personal risk-rule template
├── trades.csv                 # Structured trade log; source of truth
├── notes/                     # Optional longer notes per trade
├── research/                  # Weekly/monthly research outputs and candidates
└── docs/                      # Architecture, setup, and project notes
```

## Quick start

1. Fill out `RISK_RULES.md` before logging live trades.
2. Use `trades.csv` as the structured source of truth.
3. Put longer narratives in `notes/<trade_id>.md` instead of overloading the CSV.
4. Store research outputs in `research/` so weekly reviews can compare ideas against actual trades.
5. Review the journal regularly using `MONTHLY_SELF_GRADE.md` and the review guidance in `AGENTS.md`.

## Trade log schema

`trades.csv` uses this header:

```csv
trade_id,date_opened,ticker,direction,catalyst,catalyst_date,setup_type,thesis,entry_price,stop_price,target_price,position_size,conviction,source,risk_rating,planned_r,status,date_closed,exit_price,pnl,r_multiple,followed_plan,lesson
```

See `AGENTS.md` for field definitions and logging rules.

## Security and privacy

Do not commit:

- Broker API keys or tokens
- Account numbers
- Full brokerage exports with personal identifiers
- Screenshots showing balances or account details
- `.env` files
- Proprietary strategy data that should stay local

Use `.env.example` for placeholders only.

## Status

Early-stage private project. The documentation and data skeleton are in place; application code can be added later once the preferred stack is decided.
