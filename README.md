# TradingJournal

A private trading journal for recording trades, reviewing decisions, and measuring
whether process quality improves over time.

This repository measures and prepares; it never places orders and is not financial
advice.

## Core boundaries

- `trades.csv` is the source of truth for real trades.
- `data/proposals.csv` contains fully specified ideas, traded or not.
- `data/scanner_signals.csv` contains scanner observations, never trades.
- `data/research_snapshot.csv` is the common structured input for all research models.
- `research/manifests/*.json` records claim-level evidence for candidate reports.
- `config/risk.toml` contains executable risk and horizon values.
- `RISK_RULES.md` explains those values for the human.
- `research/*.md` contains research or generated reports and is not edited by hand.

## Repository structure

```text
.
├── AGENTS.md
├── RESEARCH_BRIEF.md
├── CHATGPT_RESEARCH_PROMPT.md
├── LLM_RESEARCH_PLAYBOOK.md
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
│   ├── research_snapshot.csv
│   ├── research_snapshot.meta.json
│   ├── eu_quote_history.csv
│   ├── finviz_watchlist.csv
│   └── finviz_watchlist_archive.csv
├── research_method/
│   ├── README.md
│   ├── discovery.md
│   ├── verification.md
│   ├── analysis.md
│   ├── red_team.md
│   ├── output_schema.md
│   ├── candidate_manifest.schema.json
│   └── evaluation_rubric.md
├── research/
│   ├── candidates-*.md
│   └── manifests/candidates-*.json
├── scanner/
├── scripts/
│   ├── build_research_snapshot.py
│   ├── validate_candidate_manifest.py
│   ├── journal_stats.py
│   ├── weekly_digest.py
│   └── validate_data.py
├── tests/
└── .github/workflows/
```

## Quick start

1. Log every real trade in `trades.csv`.
2. Log every fully specified surviving idea in `data/proposals.csv`, including ideas
   you pass on.
3. Put longer narratives in `notes/<trade_id>.md`.
4. Validate source data after edits:

   ```bash
   python scripts/validate_data.py
   ```

5. Generate the normalized research data pack before a model run:

   ```bash
   python scripts/build_research_snapshot.py --archive
   ```

6. Validate every new candidate manifest:

   ```bash
   python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
   ```

7. Run code checks before merging:

   ```bash
   python -m pip install -e '.[dev]'
   ruff check scanner scripts tests
   pytest
   ```

CI runs compilation, correctness linting, tests, source-data validation, and validation
of all committed candidate manifests.

## Model-neutral research

Claude, ChatGPT, and other models use the same process:

1. common `data/research_snapshot.csv` input;
2. separate discovery, verification, analysis, red-team, and synthesis stages;
3. opened primary source for every final catalyst date;
4. paired Markdown report and JSON evidence manifest;
5. machine validation before commit.

Model-native skills are optional references only. They cannot change the evidence gate,
horizon, or output schema. This prevents one model from appearing better merely because
its native workflow or connector supplied more structured context.

The human report stays decision-focused. Compliance and claim provenance live in the
manifest rather than a repetitive Markdown appendix.

### ChatGPT

Use `CHATGPT_RESEARCH_PROMPT.md`. The recommended flow is:

- generate the snapshot;
- run the evidence-gathering pass with ChatGPT Deep research, GitHub read access, and
  public web sources;
- prioritize company IR, filings, regulator, and exchange domains;
- review the report and manifest;
- use a separate explicit GitHub write step to commit the reviewed artifacts.

### Comparing models

Use `research_method/evaluation_rubric.md`. A fair comparison holds constant the
repository commit, snapshot hash, source permissions, research constraints, and output
schema. Grade research quality immediately; grade market outcomes later through the
proposal ledger.

## Catalyst and holding horizons

The weekly research process separates discovery from action:

- **0–21 calendar days:** eligible for the Actionable shortlist.
- **22–42 calendar days:** Early Watch only, unless a separately verified trigger inside
  21 days creates the current setup.

Proposals use a separate trading horizon:

- Default `max_holding_days`: **10 trading sessions**.
- Catalyst-driven proposals default to `exit_before_catalyst = yes`.
- The 21-trading-day scanner return is retained only as slow research context; primary
  scanner evaluation windows are 1, 3, 5, and 10 sessions.

## Scanner workflow

The US scanner uses Alpaca IEX data and optional manual Finviz discovery seeds. The EU
scanner uses the configured Yahoo / FMP / Twelve Data / Stooq fallback chain and stores
local daily history.

Manual Finviz rows require `added_at` and may specify `expires_at`. The scheduled US
workflow archives expired rows before scanning so an old screenshot cannot add score
indefinitely.

Repository secrets:

```text
APCA_API_KEY_ID
APCA_API_SECRET_KEY
FMP_API_KEY             # optional
TWELVE_DATA_API_KEY     # optional
```

Scanner workflows preserve diagnostic reports when a provider fails, but the workflow
run is marked failed instead of silently appearing healthy. A separate workflow refreshes
the normalized research snapshot when scanner or regime data changes on `main`.

## Proposal schema

```csv
proposal_id,date,ticker,direction,source,setup_type,regime,entry_price,stop_price,target_price,planned_r,catalyst,catalyst_date,thesis,risk_rating,max_holding_days,exit_before_catalyst,status,triggered_date,resolved_date,exit_price,sim_r,traded,trade_id,notes
```

The simulator uses adjusted US daily bars, conservative same-bar handling, explicit
holding periods, and pre-catalyst exits.

## Security and privacy

Never commit broker/API credentials, account numbers, full brokerage exports, balance
screenshots, `.env` files, or proprietary material that should stay local. Use
`.env.example` only for placeholders and GitHub Actions secrets for credentials.

## Current phase

Foundation/learning phase. The immediate goal is complete records, an actively used
proposal ledger, matched model comparisons, and enough clean observations to prove or
kill each pipeline before adding complexity.
