# Stage 5 — Outputs

Every run produces one human report and one machine-readable evidence manifest with the
same basename.

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
```

A repeated same-day run uses `-HHMM` in both names. Never overwrite an earlier run.

## Markdown report

Keep the report decision-focused. Do not include a long compliance table; the manifest
and validator own compliance.

```markdown
# Candidate Research — YYYY-MM-DD
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode:
- Input snapshot / SHA-256:
- Method / sources enabled:
- Preliminary / Actionable / Early Watch / Reject counts:

## Actionable Shortlist
### TICKER — Company
- Catalyst / verified date / days:
- Primary-source evidence:
- Why now / setup:
- Expectations / priced-in:
- Entry / stop / target / planned R / level basis:
- Bull / base / bear:
- Liquidity / event / financing / FX risks:
- Exit before catalyst / max holding days:
- Red-team result / pre-mortem:
- Confidence / what changes it:

## Early Watch
### TICKER — Company
- Verified catalyst / date / days:
- Why it matters:
- Promotion condition:
- Next review date:
- Removal condition:

## Rejected
- TICKER — exact rejection reason and failed gate

## Sources used
- Primary sources first, then market data and context sources.
```

## JSON manifest

The canonical schema is `research_method/candidate_manifest.schema.json`. Required run
metadata:

- schema version, report date, generation timestamp;
- model and research mode;
- discovery method and enabled data sources;
- input snapshot path and SHA-256;
- source counts;
- one object for every Actionable, Early Watch, and rejected lead discussed.

Required non-rejected candidate evidence:

- verified primary-source catalyst date;
- dated structured market data;
- expectations/priced-in evidence or an explicit `unknown` statement;
- red-team verdict;
- evidence records linking each material claim to a URL or repository source.

Actionable candidates additionally require direction, entry, stop, target, planned R,
level basis, maximum holding days, and exit-before-catalyst policy.

## Validation

Run:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
```

The validator enforces horizon, source, evidence, and setup requirements. Fix errors
before committing. Warnings may remain only when the Markdown report states the same
uncertainty plainly.
