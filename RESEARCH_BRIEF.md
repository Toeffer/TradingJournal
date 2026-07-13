# RESEARCH_BRIEF.md — Weekly Research and Decision Review

This is the canonical instruction set for Claude, ChatGPT, or any other research-capable
model. It maintains a rolling research book and issues conditional decisions for the next
five trading sessions. It never records a trade and never changes risk rules.

**Not financial advice. Verify every date, price, level, and claim before acting.**

## Core operating principle

Research may identify a strong company or future event without identifying a current entry.
Every run must issue a decision, but it must never force a buy recommendation.

Valid weekly actions are:

- `enter_if_triggered`: a complete setup may activate only at the stated trigger;
- `wait_pullback`: the idea remains valid but current price must not be chased;
- `monitor`: retain the research object without a current setup;
- `manage`: review an existing open position; no implicit add-on entry;
- `remove`: invalidate, expire, or archive the idea.

A week with no `enter_if_triggered` rows must state **NO NEW TRADE** plainly. That is a
successful output when no setup has earned an entry.

## Canonical method

Read and follow these files in order:

1. `research_method/README.md`
2. `research_method/discovery.md`
3. `research_method/verification.md`
4. `research_method/analysis.md`
5. `research_method/red_team.md`
6. `research_method/output_schema.md`
7. `SETUPS.md`

Model-native skills are optional methodology references only. They cannot alter the common
evidence standard, lifecycle, or output contract.

## Required data pack

Immediately before research, generate:

```bash
python scripts/build_research_snapshot.py --archive
```

Use `data/research_snapshot.csv` as the canonical structured market-data input and record
the SHA-256 from `data/research_snapshot.meta.json`.

Also read:

- `RISK_RULES.md`, `SETUPS.md`, and `ETORO_TRADEABILITY.md`;
- `trades.csv` and `data/proposals.csv`;
- `data/recommendations.csv` and `data/recommendation_reviews.csv`;
- `research/recommendation-book.md`;
- all candidate reports and manifests from the previous six calendar weeks;
- every older report referenced by an unresolved recommendation;
- newest relevant US/EU scanner reports and recent scanner outcomes.

Scanner names are leads, never evidence or pre-approved ideas.

## Continuity first

Before discovering new names, review every non-terminal recommendation and every open
position. A name does not disappear because it was omitted from the newest report.

For each existing recommendation:

1. Compare current price and evidence with the original mention and latest review.
2. State what changed since last week.
3. Preserve the original `recommendation_id`.
4. Choose one lifecycle status and one weekly action.
5. Define the next review date or a removal condition.
6. Append a new review row; never rewrite an old review to improve hindsight optics.

Lifecycle statuses:

- `new`
- `carry`
- `upgraded`
- `trigger_ready`
- `triggered`
- `manage`
- `downgraded`
- `invalidated`
- `expired`
- `archived`

Current convenience state lives in `data/recommendations.csv`. Immutable decision history
lives in append-only `data/recommendation_reviews.csv` and dated files under
`research/decisions/`.

## Open-position review

Every open trade receives a `manage` recommendation linked through `linked_trade_id`.
Review:

- original thesis versus current thesis;
- original stop/invalidation; never move it farther away merely to avoid a loss;
- event and gap risk;
- time-stop or maximum holding date;
- whether the position still matches an allowed setup;
- the coming week's management action.

Research must not infer that the user bought, sold, or changed a stop. Only an explicit
human statement may change `trades.csv`.

## Operating horizons

- **Weekly decision window:** next five trading sessions.
- **Actionable research:** verified catalyst or intermediate trigger inside 21 calendar days.
- **Early Watch:** verified catalyst 22–42 days away with no nearer verified trigger.
- **Proposal holding period:** 10 trading sessions by default.
- **Trigger expiry:** normally no more than five trading sessions.
- **Exit before catalyst:** `yes` by default unless the human explicitly accepts binary risk.

A distant catalyst may justify continued research but never an immediate entry by itself.

## Configuration

```text
REGION:                         US common shares + XETRA shares
MARKET_CAP_MIN:                 500000000
MARKET_CAP_MAX:                 10000000000
MIN_AVG_DOLLAR_VOLUME:          25000000
PRELIMINARY_SCAN_COUNT:         12
MAX_ACTIVE_RECOMMENDATIONS:      12
MAX_WEEKLY_DECISION_SHEET:        5
MAX_TRIGGER_READY:                2
MAX_SPECIAL_SITUATIONS:           1
MIN_EU_PRELIMINARY:               4
ASIA_POLICY:                     exceptional-only
ACTIONABLE_CATALYST_DAYS:       21
DISCOVERY_CATALYST_DAYS:        42
ACT_NOW_DAYS:                    7
MAX_EARNINGS_CANDIDATES:         2
SCANNER_LOOKBACK_DAYS:           7
MAX_SCANNER_CANDIDATES:          5
RECOMMENDATION_HISTORY_WEEKS:    6
TRIGGER_EXPIRY_SESSIONS:         5
FIXED_POSITION_SIZE_EUR:       150
```

`config/risk.toml` and `RISK_RULES.md` are authoritative for risk. `ETORO_TRADEABILITY.md`
is authoritative for broker availability. Never invent a blank value.

## Source policy

Use sources in this order:

1. Company investor relations, regulatory filings, exchange notices, prospectuses,
   regulator announcements, and official index/event calendars.
2. Dated structured market-data providers and the normalized repository snapshot.
3. Reputable financial news for expectations and context.
4. Scanner output as discovery context only.
5. Analyst notes, blogs, forums, newsletters, and social media as leads only.

A search snippet, third-party calendar, scanner row, subagent summary, prior report, or
model memory can create a lead but cannot verify a final date. The synthesizing pass must
open the primary source itself and record it in the JSON manifest.

Date statuses:

- `verified`: opened primary source states the date or binding window;
- `secondary_only`: reputable secondary source only;
- `derived`: calculated rather than explicitly stated;
- `unverified`: insufficient evidence.

Only `verified` may support Actionable or Early Watch classification.

## Stage 0 — Prior recommendation audit

Review all active recommendations before adding new names. Capture:

- first mention date and price;
- latest reference price;
- move and path since mention when data permits;
- whether the previous trigger fired;
- whether stop or target would have occurred first;
- whether the thesis improved, weakened, or expired;
- this week's status and action.

New names must compete with carry-over names. Novelty is not a ranking advantage.

## Stage 1 — Discovery

Build up to the configured preliminary count inside the 42-day discovery horizon.

- Source at least the configured European preliminary count or state precisely why not.
- Include up to the scanner limit from recent output.
- Use catalyst-first or hybrid discovery when scanner breadth is thin.
- Record each lead's origin and current market-data row.
- Check eToro tradeability before expensive analysis.
- Do not set levels during discovery.
- Do not pad.

## Stage 2 — Verification

For every plausible survivor:

- open and record the primary event source;
- verify date, mechanics, and whether the event already occurred;
- verify current market data;
- check financing, dilution, offerings, lockups, and intervening events;
- record expectations or state that they are unknown;
- record claim-level evidence with access timestamps.

A non-rejected catalyst candidate needs at least one primary source and one structured
market-data source.

## Stage 3 — Research classification

Classify every discussed lead:

- `ACTIONABLE`: verified trigger inside 0–21 days and a current setup may form;
- `EARLY_WATCH`: real future event or thesis, but no defensible current setup;
- `REJECT`: fails evidence, tradeability, liquidity, expectations, setup, or risk.

This classification is not itself an entry recommendation. An Actionable name still needs
a valid weekly action and setup trigger.

## Stage 4 — Weekly action construction

For each surviving recommendation choose exactly one action.

### `enter_if_triggered`

Requires:

- status `trigger_ready`;
- an allowed `setup_type` from `SETUPS.md`;
- long/short direction;
- numeric entry trigger, stop, target, and planned R of at least the configured minimum;
- a structure-based `trigger_rule`;
- trigger expiry normally within five trading sessions;
- current reference price and dated source;
- no instruction to enter at an arbitrary current price;
- red-team verdict `SURVIVE`.

A trigger-ready research recommendation may be copied into `data/proposals.csv` only after
all proposal fields are complete. The recommendation ledger itself must not pretend a
proposal triggered.

### `wait_pullback`

Use when the thesis remains valid but price is extended or the first move should not be
chased. State the desired zone/structure, removal condition, and next review date. Do not
provide a pseudo-entry that lacks defensible stop/target math.

### `monitor`

Use when research remains useful but no current price setup exists. State the promotion
condition and next review date.

### `manage`

Use only for an existing position and link the trade ID. State management facts without
inventing an execution.

### `remove`

Use with status `invalidated`, `expired`, or `archived`. State exactly why the object leaves
the active book.

## Stage 5 — Red team

Run a separate skeptical pass over every survivor and every proposed trigger. Attack:

- date accuracy and event materiality;
- expectations and crowding;
- financing and dilution;
- arbitrary levels;
- event-gap and overnight risk;
- liquidity, spread, and FX;
- whether the recommendation is early, chased, or stale;
- whether the same thesis previously failed.

Verdicts:

- `SURVIVE`
- `DOWNGRADE_EARLY_WATCH`
- `REJECT`

Only `SURVIVE` may remain `trigger_ready`.

## Required outputs

A research run produces:

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
data/recommendations.csv
data/recommendation_reviews.csv
research/decisions/decisions-YYYY-MM-DD.csv
research/decisions/decisions-YYYY-MM-DD.meta.json
research/recommendation-book.md
```

Repeated same-day runs use a time suffix for report, manifest, and decision archive. Never
overwrite earlier run artifacts.

The Markdown report is the concise human decision review. The JSON manifest remains the
evidence contract. The recommendation registry is current state; review rows and decision
archives preserve what was decided at the time.

Run:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
python scripts/validate_recommendations.py
python scripts/archive_recommendation_reviews.py --date YYYY-MM-DD
python scripts/summarize_recommendations.py
python scripts/validate_data.py
```

Nothing in this workflow writes to `trades.csv`. It may update `data/proposals.csv` only in
a separate explicit proposal-writing step after the research artifacts validate.

## Success criteria

- Every active prior recommendation receives a current decision.
- Every open position receives a linked management review.
- New names compete with carry-over names.
- Every weekly action is explicit and auditable.
- Trigger-ready rows have complete setup math and expire promptly.
- No name is bought merely because it appeared in research.
- Every status change appends a review row.
- Archived decisions match the append-only review ledger.
- A no-new-trade week is allowed and stated plainly.
- Research quality, mechanical recommendation outcome, and human execution are graded
  separately.
