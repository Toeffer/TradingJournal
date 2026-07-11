# AGENTS.md — Trading Journal Operating Instructions

This repository is the trading journal. Natural-language requests are translated into
structured records, calculations, research artifacts, and reviews.

**Not financial advice. Never tell the user what to buy. Record, measure, verify, and
expose process violations.**

## Sources of truth

- `trades.csv`: real trades only.
- `data/proposals.csv`: fully specified ideas, traded or not.
- `data/scanner_signals.csv`: scanner observations, never trades.
- `data/research_snapshot.csv`: normalized market input shared by every research model.
- `research/manifests/*.json`: evidence contract for candidate reports.
- `config/risk.toml`: executable limits and holding horizons.
- `RISK_RULES.md`: human-readable rationale.
- `SETUPS.md`: allowed proposal definitions.
- `research/*.md`: human-facing research and derived reports.

Generated reports are never edited by hand. Scanner/research output can never add a
trade without an explicit statement that a real position was opened.

After changing a source CSV, run:

```bash
python scripts/validate_data.py
```

Before a weekly research run, generate:

```bash
python scripts/build_research_snapshot.py
```

Before committing a candidate report, validate its paired manifest:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
```

Structural validation errors must be corrected before committing. Historical
completeness warnings should be surfaced, not hidden.

## Natural-language intents

Recognize:

- Log/open a trade.
- Close a trade.
- Correct a field.
- Log/cancel a proposal.
- Run or review weekly candidate research.
- Review scanner output.
- Show stats or review behavior.
- Review open positions.
- Compare model research outputs.

Ask at most one short question for a critical missing value. Never invent a price, date,
stop, fill, source, or risk rule.

## Trade schema

```csv
trade_id,date_opened,ticker,direction,sector,catalyst,catalyst_date,setup_type,thesis,entry_price,stop_price,target_price,position_size,conviction,source,candidate_ref,risk_rating,planned_r,status,date_closed,exit_price,pnl,r_multiple,followed_plan,lesson
```

During the current learning phase, `position_size` is EUR capital deployed—not shares
and not risk-to-stop. Keep that interpretation consistent until a deliberate schema
migration introduces quantity and FX fields.

Allowed conventions:

- `direction`: `long` or `short`.
- `status`: `open` or `closed`.
- `source`: `routine`, `scanner`, `scanner+routine`, or `own`.
- `followed_plan`: `yes`, `no`, or `partial`.
- `candidate_ref`: path/anchor to the research or proposal that produced the idea.

## Log a real trade

Required before appending:

- ticker
- direction
- entry price
- stop price
- setup type
- catalyst or explicit non-catalyst rationale
- position size in EUR

Also capture sector, target, thesis, source, candidate reference, catalyst date,
conviction, and risk rating when available.

Before appending, check `config/risk.toml`, `RISK_RULES.md`, and current open trades:

1. Maximum open positions.
2. Maximum positions per sector/theme.
3. Maximum total open position value.
4. Per-position size cap.
5. Daily and weekly realized-R circuit breakers.
6. Three-consecutive-loss pause.
7. Stop exists and is on the correct side of entry.
8. Binary-event half-size rule when the plan is to hold through the event.
9. Planned R when target is known; flag planned R below the proposal minimum.

Flag violations briefly. The journal records reality, so if the user explicitly says the
trade occurred, log it even when it broke a rule.

Generate the next sequential `trade_id`, set `status=open`, and calculate:

- Long planned R: `(target - entry) / (entry - stop)`.
- Short planned R: `(entry - target) / (stop - entry)`.

Confirm the saved id, entry, stop, target, planned R, and any rule flags.

## Close a real trade

Find the open row. When more than one position in the ticker is open, identify the
correct trade before editing.

Set date closed, exit price, status, P&L from the broker-confirmed figure when available,
and R multiple:

- Long: `(exit - entry) / (entry - stop)`.
- Short: `(entry - exit) / (stop - entry)`.

Ask for `followed_plan` and a one-line `lesson`. These are required raw material, not
optional decoration.

For cross-currency instruments, do not invent FX reconciliation. Use the verified broker
P&L and price-level R, and explain the convention in the lesson or note.

## Proposals

Proposal schema:

```csv
proposal_id,date,ticker,direction,source,setup_type,regime,entry_price,stop_price,target_price,planned_r,catalyst,catalyst_date,thesis,risk_rating,max_holding_days,exit_before_catalyst,status,triggered_date,resolved_date,exit_price,sim_r,traded,trade_id,notes
```

Required:

- ticker and direction
- a setup defined in `SETUPS.md`
- entry, stop, and target
- planned R of at least the configured minimum
- thesis
- catalyst/date when catalyst-driven
- `max_holding_days` (default from `config/risk.toml`, currently 10)
- `exit_before_catalyst` (`yes` by default)

A catalyst 22–42 days away remains `EARLY_WATCH` research and is not logged as a proposal
unless a separate verified trigger inside 21 days creates the setup.

When logging:

1. Copy the newest market regime when available.
2. Generate the next `proposal_id`.
3. Set `status=pending`.
4. Default `max_holding_days` from the risk config.
5. Default `exit_before_catalyst=yes` when a catalyst date exists.
6. Append whether or not the user expects to trade it.

When a proposal becomes a real trade, set `traded=yes`, attach `trade_id`, and set the
trade's `candidate_ref` to the proposal id. Cancellation sets `status=cancelled`; never
delete historical rows.

`scanner/simulate_proposals.py` owns simulated terminal fields. Do not manually rewrite
`triggered_date`, `resolved_date`, `exit_price`, or `sim_r` after resolution.

## Weekly research

All models follow `RESEARCH_BRIEF.md` and `research_method/`. Claude-native skills are
optional references only; they do not define a different standard from ChatGPT.

Required paired outputs:

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
```

The model must:

1. use the normalized snapshot and record its SHA-256;
2. separate discovery, verification, analysis, red-team, and synthesis;
3. open the primary source itself for every non-rejected catalyst date;
4. classify unverified/secondary-only/derived dates as Reject;
5. use evidence-based levels rather than broker-page day-low proxies;
6. keep compliance metadata in the manifest, not repetitive Markdown;
7. pass `scripts/validate_candidate_manifest.py` before commit.

Horizons:

- 0–21 calendar days: Actionable only when a current setup also exists.
- 22–42 days: Early Watch.

A distant event is not a current setup. Price and expectations can change before the
catalyst, so promotion requires current structure or a separate verified near-term trigger.

For ChatGPT use `CHATGPT_RESEARCH_PROMPT.md`. Research through connected apps is read-only
during the Deep Research pass; repository persistence is a separate explicit write step.

For matched model comparisons use `research_method/evaluation_rubric.md` and hold the
repository commit, snapshot hash, source access, time window, and output schema constant.

## Scanner review

When reviewing scanner output:

1. Open the newest relevant US/EU scan report.
2. Use `SCANNER_RESEARCH_PROMPT.md`.
3. Classify each ticker as Deep dive, Watch, or Reject.
4. Verify news/catalyst, dilution, liquidity/spread, event risk, and invalidation.
5. Treat score as a reason to investigate, never as a setup.
6. Never write to `trades.csv` from scanner review alone.

Manual Finviz seeds expire and are archived by `scanner/expire_finviz_seeds.py`; a stale
screenshot must not keep adding score.

## Open-position review

Review each open position against the recorded thesis and invalidation:

- `HOLD`: thesis intact, structure intact, catalyst policy unchanged.
- `EXIT/REDUCE`: recorded invalidation hit, thesis broken, or pre-planned event exit due.
- `EXHAUSTION REVIEW`: multiple momentum-exhaustion signs agree; one indicator alone is
  not enough.

Never move a stop farther away, average down as a strategy, or silently change an event-
hold decision after entry.

## Statistics and interpretation

- Use R for decision quality and broker P&L for account impact.
- Small samples prove nothing.
- Scanner 1/3/5/10-day outcomes are primary; 21-day results are slow context.
- Separate score versions, markets, and providers before drawing conclusions.
- Proposal `passed` versus `traded` is the picker test.
- Missing fields must remain visible in generated reports.
- Research-quality grades and later price outcomes are separate measurements.

## Corrections and audit trail

Correct factual errors when evidence is available. Never delete a real trade, proposal,
research manifest, or resolved outcome to improve statistics. Explain non-obvious
corrections in the commit message or a note.
