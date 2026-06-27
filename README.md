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
├── CLAUDE.md                  # Claude Code session startup guide
├── AGENTS.md                  # Operating instructions for AI-assisted journaling
├── LLM_RESEARCH_PLAYBOOK.md   # Research routine / discovery workflow
├── RESEARCH_BRIEF.md          # Automated weekly research routine spec
├── MONTHLY_SELF_GRADE.md      # Monthly review template for the research process
├── RISK_RULES.md              # Personal risk rules (position sizing, loss limits)
├── ETORO_TRADEABILITY.md      # Broker overlay for eToro Germany/EU
├── SECOND_OPINION.md          # Red-team prompt for a second model
├── trades.csv                 # Structured trade log; source of truth
├── notes/                     # Optional longer notes per trade
├── research/                  # Weekly/monthly research outputs and candidates
└── docs/                      # Architecture, setup, and project notes
```

## Quick start

1. `RISK_RULES.md` is filled in with learning-phase rules (€150/trade fixed sizing).
2. Use `trades.csv` as the structured source of truth — log every trade.
3. Put longer narratives in `notes/<trade_id>.md` instead of overloading the CSV.
4. Store research outputs in `research/` so weekly reviews can compare ideas against actual trades.
5. Save second-opinion output to `research/second-opinion-YYYY-MM-DD.md` alongside candidates.
6. Review the journal regularly using `MONTHLY_SELF_GRADE.md` and the review guidance in `AGENTS.md`.

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

Learning phase. Risk rules are set (€150/trade fixed sizing), trade log is ready,
research routine is active. Application code can be added later once the preferred
stack is decided.
