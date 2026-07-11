# Model comparison rubric

Compare models only when they receive the same repository commit, normalized snapshot,
source permissions, time window, research constraints, and output schema. Remove model
names before scoring when practical.

## Scorecard

| Criterion | Weight | Full-credit standard |
|---|---:|---|
| Primary-source catalyst verification | 25 | Every non-rejected date is supported by an opened primary source and recorded in the manifest |
| Freshness and numerical accuracy | 20 | Market data is dated, consistent with the snapshot, and material numbers are traceable |
| Candidate-specific thesis depth | 15 | Analysis explains the actual business/product/event mechanics rather than generic themes |
| Expectations and priced-in analysis | 15 | States what the market expects and why the event may or may not be reflected in price |
| Entry and invalidation quality | 10 | Levels have a technical/thesis basis; no arbitrary day-low proxies |
| Bear case and pre-mortem | 10 | Strongest failure path is specific, evidence-based, and capable of rejecting the idea |
| Clarity and usability | 5 | Sparse, decision-focused report with no repetitive compliance filler |

Maximum: 100.

## Automatic deductions

- Final candidate with `date_status != verified`: minus 25 and mark invalid.
- Primary-source URL not opened by the synthesizing pass: mark invalid.
- Market data has no as-of timestamp/source: minus 10.
- Entry/stop/target lacks basis: minus 10.
- Candidate retained after red-team Reject: mark invalid.
- Unsupported numerical claim: minus 2 each, up to 20.

## Metadata to preserve

Record in the manifest:

- model and version/display name;
- research mode;
- enabled connected apps/data providers;
- repository commit;
- input snapshot path and SHA-256;
- start/end timestamps when available;
- sources opened and primary-source count;
- preliminary, Actionable, Early Watch, and Reject counts.

## Outcome grading

Research quality and market outcome are separate:

1. Grade the report immediately with this rubric.
2. Later grade proposal outcomes through `data/proposals.csv`.
3. Do not retroactively change the research-quality score because price moved.
4. Compare models only after multiple matched runs; one strong report is anecdotal.
