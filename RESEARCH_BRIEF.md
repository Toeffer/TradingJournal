# RESEARCH_BRIEF.md — Weekly Candidate Research

This is the canonical instruction set for Claude, ChatGPT, or any other research-capable
model. It creates a draft shortlist for human review; it never creates a trade and never
changes risk rules.

**Not financial advice. Verify every date, price, and claim before acting.**

## Canonical method

Read and follow these files in order:

1. `research_method/README.md`
2. `research_method/discovery.md`
3. `research_method/verification.md`
4. `research_method/analysis.md`
5. `research_method/red_team.md`
6. `research_method/output_schema.md`

Claude-native skills are optional methodology references only. They must not grant Claude
a different workflow, evidence standard, or output contract from ChatGPT.

## Required data pack

Immediately before research, generate:

```bash
python scripts/build_research_snapshot.py --archive
```

Use `data/research_snapshot.csv` as the canonical structured market-data input and
record the SHA-256 from `data/research_snapshot.meta.json`. Connected financial data may
supplement the snapshot, but it may not silently replace the common comparison input.

Also read:

- `RISK_RULES.md`, `SETUPS.md`, and `ETORO_TRADEABILITY.md`;
- newest relevant US/EU scanner reports and `data/scanner_signals.csv`;
- newest prior candidate report and manifest for continuity.

Scanner names are leads, never evidence or pre-approved ideas.

## Operating horizons

A distant catalyst is useful for discovery but is not automatically actionable. Price,
expectations, financing, regime, and the company can change before the event.

- **Actionable:** verified catalyst or intermediate trigger inside 21 calendar days.
- **Early Watch:** verified catalyst 22–42 days away with no nearer verified trigger.
- **Proposal holding period:** 10 trading sessions by default, set explicitly in the
  proposal with `exit_before_catalyst = yes` unless the human chooses otherwise.

A 22–42-day event may become Actionable only when a separate, dated, primary-source-
verified trigger inside 21 days creates the current setup. State the exception plainly.

## Configuration

```text
REGION:                         US common shares + XETRA shares
MARKET_CAP_MIN:                 500000000
MARKET_CAP_MAX:                 10000000000
MIN_AVG_DOLLAR_VOLUME:          25000000
PRELIMINARY_SCAN_COUNT:         12
NUM_ACTIONABLE_CANDIDATES:       5
NUM_EARLY_WATCH:                 5
NUM_DEEP_DIVES:                  3
MIN_EU_PRELIMINARY:              4
ASIA_POLICY:                     exceptional-only
ACTIONABLE_CATALYST_DAYS:       21
DISCOVERY_CATALYST_DAYS:        42
ACT_NOW_DAYS:                    7
MAX_EARNINGS_CANDIDATES:         2
SCANNER_LOOKBACK_DAYS:           7
SCANNER_MIN_SCORE:              70
MAX_SCANNER_CANDIDATES:          5
FIXED_POSITION_SIZE_EUR:       150
```

`config/risk.toml` and `RISK_RULES.md` are authoritative for risk and holding periods.
`ETORO_TRADEABILITY.md` is authoritative for broker availability. Never invent a blank
value.

## Source policy

Use sources in this order:

1. Company investor relations, regulatory filings, exchange notices, prospectuses,
   regulator announcements, and official index/event calendars.
2. Dated structured market-data providers and the normalized repository snapshot.
3. Reputable financial news for expectations and context.
4. Scanner output as discovery context only.
5. Analyst notes, blogs, forums, newsletters, and social media as leads only.

For European candidates prefer issuer Finanzkalender pages, EQS/DGAP, Deutsche Börse,
RNS, Euronext/SIX notices, and issuer IR pages. For lockup expiries, verify prospectus
terms, early-release provisions, waivers, and later offerings; never rely on “IPO date +
N days.”

For every non-US candidate state exchange, currency, local share versus ADR, FX exposure,
and market hours. Name UK stamp duty for LSE shares.

### Primary-source gate

A search snippet, third-party calendar, scanner row, subagent summary, or model memory can
create a lead but cannot verify a final date. The synthesizing pass must open the primary
source itself and record it in the JSON manifest.

Use these date statuses:

- `verified`: opened primary source states the date or binding window;
- `secondary_only`: reputable secondary source only;
- `derived`: calculated rather than explicitly stated;
- `unverified`: insufficient evidence.

Only `verified` may appear as Actionable or Early Watch. All other statuses are Reject.

## Stage 1 — Discovery

Build up to `PRELIMINARY_SCAN_COUNT` traceable leads inside the 42-day discovery horizon.

- Source at least `MIN_EU_PRELIMINARY` European names before quality filtering, or state
  precisely what the EU search found and why none qualified.
- Include up to `MAX_SCANNER_CANDIDATES` recent scanner names meeting the threshold.
- Record each lead's origin and current snapshot row.
- Check eToro tradeability before expensive deep research, especially for IPOs.
- Do not rank names, set stops, or calculate sizes during discovery.
- Do not pad. A sparse pool is acceptable when evidence is weak.

## Stage 2 — Verification

For every plausible survivor:

- open and record the primary catalyst source;
- verify event date and mechanics, and confirm it has not moved or already occurred;
- verify market data with the snapshot or another dated structured source;
- check intervening earnings, financing, dilution, offerings, waivers, and lockups;
- record claim-level evidence with access timestamps in the manifest.

A non-rejected candidate needs at least:

- one primary catalyst source;
- one structured market-data source;
- expectations/priced-in evidence or an explicit statement that it is unknown.

## Stage 3 — Classification and analysis

Classify every discussed lead:

- `ACTIONABLE`: verified trigger inside 0–21 days and a current setup;
- `EARLY_WATCH`: verified catalyst 22–42 days away, or a real event without a current
  defensible setup;
- `REJECT`: fails evidence, tradeability, liquidity, expectations, setup, or risk.

No more than `MAX_EARNINGS_CANDIDATES` final Actionable names may use earnings as the
primary catalyst. Prefer structural or already-public catalysts over binary event gambling.

### Actionable requirements

For each Actionable candidate provide:

1. Ticker, company, exchange, currency, and source tag.
2. Verified catalyst mechanics, exact date, days remaining, and primary-source URL.
3. Why now: the present setup, not the future event alone.
4. Market expectations and priced-in assessment.
5. Entry, initial stop/invalidation, first target, planned R, and the basis of each level.
6. Bull, base, and bear scenarios.
7. Liquidity, spread, financing, dilution, event-gap, insider, short, and FX risks.
8. Risk rating and confidence, including evidence that would change either.
9. Exit-before-catalyst policy and maximum holding days.
10. Pre-mortem and red-team verdict.

A stop may not be a broker-page day-low proxy merely because it is convenient. Tie levels
to actual structure or thesis invalidation. A candidate without a defensible entry, stop,
target, and planned R of at least 1.5 is Early Watch or Reject—not a proposal.

### Early Watch requirements

For each Early Watch name provide:

- verified catalyst mechanics, date, and days remaining;
- why it may matter;
- promotion condition and next review date;
- removal condition;
- primary-source evidence.

Do not calculate size or present Early Watch as a current trade setup.

## Stage 4 — Red team

Run a separate skeptical pass over every survivor. Attack date accuracy, event materiality,
expectations, crowding, financing/dilution, arbitrary levels, gap risk, liquidity, and
intervening events.

Use one verdict:

- `SURVIVE`
- `DOWNGRADE_EARLY_WATCH`
- `REJECT`

Only `SURVIVE` may remain Actionable. Do not weaken bear cases to preserve shortlist size.

## Required outputs

Before writing, check for a same-day file and never overwrite it. A repeated run adds
`-HHMM` to both filenames.

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
```

The Markdown report is the concise human analysis. The JSON manifest is the evidence and
compliance contract and must follow `research_method/candidate_manifest.schema.json`.
Do not add a repetitive compliance table to the Markdown report.

Run:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
```

Fix validation errors before committing. Nothing in this workflow writes to `trades.csv`
or `data/proposals.csv`.

## Success criteria

- All models use the same method, snapshot, horizon, and output schema.
- Every Actionable and Early Watch date has an opened primary source in the manifest.
- Every market number has a date and source.
- Every Actionable level has an evidence-based technical or thesis rationale.
- Every Actionable candidate survived the red-team pass.
- A no-candidate week is allowed and recorded honestly.
- Model comparisons use `research_method/evaluation_rubric.md` and multiple matched runs.
