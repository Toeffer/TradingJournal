# Candidate Research — 2026-07-12
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode: GPT-5.6 Thinking / hybrid, evidence-gated
- Input snapshot / SHA-256: `data/research_snapshot.csv` / `e7599d5b012415f1497439cfc954d7b8fcf2790e0ced677fabd07b1588159adc`
- Snapshot generated: 2026-07-11 11:59:24 UTC; 13 rows
- Method / sources enabled: repository snapshot, current repository instructions, newest prior report, scanner data, GitHub connector, public web search
- Preliminary / Actionable / Early Watch / Reject counts: 12 / 0 / 0 / 12
- Continuity: the 2026-07-05 report named PENG and LEVI, but both catalysts occurred on 2026-07-07/08 and were not primary-source verified in that report. They are not carried forward.

## Actionable Shortlist

No candidates qualified. A valid Actionable name requires an opened primary source with a verified catalyst inside 21 days, current structured market data, eToro Germany/EU share tradeability, a defensible entry/stop/target with at least 1.5R, and a red-team verdict of `SURVIVE`. No lead met all gates.

## Early Watch

No candidates qualified. No lead had an opened primary source explicitly stating a catalyst 22–42 days away while also passing broker, universe, liquidity and evidence requirements.

## Rejected

- **QIA.DE — QIAGEN** (`scanner_seed`) — only current XETRA scanner lead in the canonical snapshot. Score 68 is below the configured scanner threshold of 70; market cap is absent from the snapshot; no opened issuer primary source explicitly verified a catalyst inside 42 days; eToro Germany/EU stock/share tradeability was not independently verified during this run.
- **RIVN — Rivian Automotive** (`scanner_seed`) — snapshot liquidity passes the preferred US floor, but the July 9 signal is a price/volume anomaly rather than catalyst evidence. No forward primary-source catalyst inside 42 days and no defensible current setup were verified; larger-cap exception status could not be established because snapshot market cap is blank.
- **HOOD — Robinhood Markets** (`scanner_seed`) — scanner score 70 and strong liquidity are discovery leads only. The snapshot observation is from July 3, market cap is blank, and no primary-source catalyst or current technical structure was verified. Prior expansion news had already occurred.
- **CELH — Celsius Holdings** (`scanner_seed`) — average dollar volume in the snapshot is about $14.0M, placing it in the conditional US liquidity range, not the main shortlist. Scanner score is below 70 and no primary-source catalyst was verified.
- **SMMT — Summit Therapeutics** (`scanner_seed`) — snapshot average dollar volume is about $5.9M, below even the conditional US liquidity floor. Rejected on liquidity before expensive catalyst research.
- **HIMS — Hims & Hers Health** (`scanner_seed`) — snapshot average dollar volume is about $22.0M, conditional rather than preferred, and the score is below 70. No verified primary catalyst or current setup was established.
- **GIS — General Mills** (`routine+scanner_seed`) — liquidity passes, but the signal is old, score is below 70, market cap is absent, and the company is likely outside the preferred core universe. No verified forward catalyst/setup was established.
- **SOFI — SoFi Technologies** (`scanner_seed`) — liquidity passes, but relative volume was below the scanner trigger, score was 50, and no primary-source catalyst was verified. Market-cap exception status could not be assessed from the snapshot.
- **TOST — Toast** (`scanner_seed`) — liquidity narrowly passes, but relative volume was below trigger, score was 50, and no primary-source catalyst or defensible setup was verified.
- **PLTR — Palantir Technologies** (`scanner_seed`) — excluded by default under the broker/universe overlay as an obvious crowded headline AI name and likely mega-cap; no exception was justified.
- **RHM.DE — Rheinmetall** (`prior_report`) — prior work placed market cap above the default €/$50B exclusion threshold. No new exception-quality setup was verified.
- **HAG.DE — Hensoldt** (`prior_report`) — included to satisfy the European preliminary pass, but no opened issuer primary source explicitly verified a catalyst inside 42 days and the canonical snapshot contains no current row for the name. Rejected rather than relying on prior-report memory.

## Red-team conclusion

The strongest counterargument to an empty list is that scanner leaders such as RIVN or HOOD may continue trending. That does not repair the missing primary catalyst, market-cap fields, broker-region verification, or evidence-based levels. Removing the scanner score and thematic story leaves no candidate with a complete, testable setup; all verdicts are therefore `REJECT`.

## Sources used

- Repository primary instructions: `RESEARCH_BRIEF.md`; `research_method/README.md`; `discovery.md`; `verification.md`; `analysis.md`; `red_team.md`; `output_schema.md`
- Risk and broker overlays: `RISK_RULES.md`; `SETUPS.md`; `ETORO_TRADEABILITY.md`
- Canonical structured data: `data/research_snapshot.csv`; metadata SHA-256 from `data/research_snapshot.meta.json`
- Continuity: `research/candidates-2026-07-05.md`
- Public web: issuer-calendar searches for QIAGEN, Hensoldt and AIXTRON returned no openable primary-source result sufficient to verify a date during this run.
