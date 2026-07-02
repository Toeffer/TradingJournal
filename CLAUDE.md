# CLAUDE.md — TradingJournal

Personal swing-trade journal and research system. No application code — the repo
is structured data (CSV), documentation (Markdown), and Claude Code integration.

## Reading order

1. `AGENTS.md` — how the journal works (intents, CSV schema, logging/closing/stats/review rules)
2. `RISK_RULES.md` — personal risk framework (position sizing, loss limits, earnings policy)
3. `SETUPS.md` — setup definitions and the proposal card standard (feeds `data/proposals.csv`)
4. `RESEARCH_BRIEF.md` — automated weekly research routine spec
5. `ETORO_TRADEABILITY.md` — broker overlay (eToro Germany/EU account)
6. `LLM_RESEARCH_PLAYBOOK.md` — manual research workflow and prompts
7. `MONTHLY_SELF_GRADE.md` — monthly grading of the discovery engine
8. `SECOND_OPINION.md` — red-team prompt for a second model

## Key data

- `trades.csv` — source of truth for all trades. Append only; never silently rewrite.
- `research/candidates-YYYY-MM-DD.md` — weekly candidate shortlists from the routine.
- `notes/<trade_id>.md` — optional longer narratives per trade.

## Rules

- Never fabricate stats — compute everything from `trades.csv`.
- Never give financial advice — record, measure, and reflect only.
- Keep interactions fast — one short question max when logging.
- Check `RISK_RULES.md` before interpreting sizing, risk, or portfolio context.
- All catalyst dates must be flagged for human verification.

## Broker

eToro, Germany/EU account. Only surface stocks tradeable on eToro.

## Skills

The repo includes equity-research skills in `.claude/skills/` (earnings-analysis,
earnings-preview, idea-generation, catalyst-calendar, thesis-tracker) with
matching commands in `.claude/commands/`.
