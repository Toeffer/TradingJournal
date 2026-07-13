# Model-neutral research method

This directory is the canonical research workflow for every model and tool. Claude-specific
skills may be consulted as optional background, but they do not define the process. Every
model receives the same snapshot, recommendation history, source rules, stages, and output
contract.

## Required inputs

1. `data/research_snapshot.csv`, generated immediately before the research run.
2. `data/research_snapshot.meta.json`, including the snapshot SHA-256.
3. `data/recommendations.csv` and `data/recommendation_reviews.csv`.
4. `research/recommendation-book.md`.
5. Candidate reports/manifests from the previous six calendar weeks and every older report
   linked by an unresolved recommendation.
6. `trades.csv`, `data/proposals.csv`, and relevant scanner reports/outcomes.
7. `RESEARCH_BRIEF.md`, `RISK_RULES.md`, `SETUPS.md`, and
   `ETORO_TRADEABILITY.md`.

Build the normalized data pack with:

```bash
python scripts/build_research_snapshot.py --archive
```

## Required sequence

0. **Continuity review** — audit active recommendations and open positions before finding
   new names.
1. `discovery.md` — create a broad current pool; new names compete with carry-over names.
2. `verification.md` — open primary sources and verify each material claim.
3. `analysis.md` — evaluate expectations, setup, invalidation, and risks.
4. `red_team.md` — try to reject each survivor and each proposed trigger.
5. `output_schema.md` — write evidence, current state, append-only reviews, and the weekly
   decision archive.

Do not discover, verify, rank, and recommend in one undifferentiated pass. A model that
cannot obtain the required evidence must downgrade or remove the object rather than
compensating with more prose.

## Decision semantics

Every active recommendation receives exactly one weekly action:

- `enter_if_triggered`
- `wait_pullback`
- `monitor`
- `manage`
- `remove`

A research classification is not an entry. `enter_if_triggered` requires a complete setup,
short expiry, valid risk math, current data, and red-team survival. When none qualifies, the
report states **NO NEW TRADE**.

## Outputs

Every run writes evidence plus recommendation state/history:

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
data/recommendations.csv
data/recommendation_reviews.csv
research/decisions/decisions-YYYY-MM-DD.csv
research/decisions/decisions-YYYY-MM-DD.meta.json
research/recommendation-book.md
```

A second same-day run adds `-HHMM` where applicable. Validate and render with:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
python scripts/validate_recommendations.py
python scripts/archive_recommendation_reviews.py --date YYYY-MM-DD
python scripts/summarize_recommendations.py
```

The JSON manifest is the research evidence contract. The current registry is a convenience
view. The append-only review ledger and dated archives prove what the workflow actually
decided at the time.

## Fair model comparison

Use `evaluation_rubric.md`. Keep the repository commit, snapshot hash, recommendation
history, source access, time, constraints, and output schema identical. Grade research
quality separately from mechanical recommendation outcomes and human trade execution.
