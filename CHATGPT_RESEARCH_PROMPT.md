# ChatGPT research runbook

Use this for the ChatGPT version of the weekly research and decision review. It follows
`RESEARCH_BRIEF.md` and `research_method/` exactly.

## Recommended setup

1. Generate and commit the normalized data pack first:

   ```bash
   python scripts/build_research_snapshot.py --archive
   ```

2. Prefer **Deep research** for the multi-source research pass.
3. Enable the GitHub connection for this repository and the public web.
4. Prioritize company IR, filings, regulators, exchanges, EQS/RNS, official index/event
   calendars, and dated structured market data.
5. Review the proposed plan before research starts. It must begin with continuity and open-
   position review, then discovery, verification, analysis, red team, and synthesis.

Deep research uses connected apps for reading. Persisting files to GitHub is a separate,
explicit write step after reviewing the output.

## Deep research prompt

```text
Use the GitHub repository Toeffer/TradingJournal at main and the public web.

Follow, in order:
- RESEARCH_BRIEF.md
- research_method/README.md
- research_method/discovery.md
- research_method/verification.md
- research_method/analysis.md
- research_method/red_team.md
- research_method/output_schema.md
- SETUPS.md

Use data/research_snapshot.csv as the canonical structured market-data input and record
its SHA-256 from data/research_snapshot.meta.json.

Before finding new names, read:
- trades.csv and data/proposals.csv;
- data/recommendations.csv and data/recommendation_reviews.csv;
- research/recommendation-book.md;
- candidate reports and manifests from the previous six calendar weeks;
- every older report referenced by an unresolved recommendation;
- newest relevant US/EU scanner reports and measured outcomes.

Review every active recommendation and every open position first. Preserve stable
recommendation IDs. State what changed, whether the previous trigger fired, and choose one
weekly action: enter_if_triggered, wait_pullback, monitor, manage, or remove. Never silently
drop a prior name and never infer that a trade occurred.

New names must compete with carry-over names. Do not prefer novelty. Scanner output and
manual seeds are leads only.

Do not use model memory for current dates or market figures. Open a primary source yourself
for every catalyst date that survives. Secondary-only, derived, or unverified dates cannot
support Actionable or Early Watch classification.

A trigger-ready recommendation requires an allowed setup, numeric entry trigger, observable
trigger rule, expiry normally within five trading sessions, stop, target, planned R of at
least the configured minimum, current market data, removal condition, and red-team SURVIVE.
Do not recommend entering at the current price. Do not chase. If no complete trigger exists,
state NO NEW TRADE.

Produce complete, mutually consistent artifacts:
1. research/candidates-YYYY-MM-DD.md
2. research/manifests/candidates-YYYY-MM-DD.json
3. updated data/recommendations.csv
4. append-only data/recommendation_reviews.csv rows for this run
5. the rows that belong in research/decisions/decisions-YYYY-MM-DD.csv

The Markdown must include run metadata, prior recommendation audit, existing positions,
coming-week decision sheet, new research, and removals. The JSON must follow
research_method/candidate_manifest.schema.json.

Return the complete Markdown, JSON, replacement current registry, append-only review rows,
and a short evidence-gap list. Do not write to trades.csv. Do not claim a proposal or trade
triggered without data confirming it.
```

## Persist after review

In a normal ChatGPT turn with GitHub write access, attach or reference the reviewed output
and say:

```text
Write the reviewed report, manifest, current recommendation registry, and appended review
rows to their specified paths. Validate the candidate manifest and recommendations. Archive
this run's recommendation reviews, regenerate the recommendation book, run repository-data
validation and tests, and open a PR. Do not alter trades.csv. Do not update proposals.csv
unless I explicitly request a separate proposal-writing step.
```

Required checks:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
python scripts/validate_recommendations.py
python scripts/archive_recommendation_reviews.py --date YYYY-MM-DD
python scripts/summarize_recommendations.py
python scripts/validate_data.py
```

## Fair model comparison

Both models must use the same commit, snapshot hash, recommendation history, source
permissions, time window, and output schema. Grade research accuracy separately from
mechanical recommendation outcomes and actual human execution.
