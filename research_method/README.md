# Model-neutral research method

This directory is the canonical research workflow for **every** model and tool.
Claude-specific skills may be consulted as optional background, but they do not define
the process. ChatGPT, Claude, or another model should receive the same snapshot, source
rules, stages, and output schema.

## Required inputs

1. `data/research_snapshot.csv`, generated immediately before the research run.
2. `data/research_snapshot.meta.json`, including the snapshot SHA-256.
3. The newest candidate report and relevant scanner reports.
4. `RESEARCH_BRIEF.md`, `RISK_RULES.md`, `SETUPS.md`, and
   `ETORO_TRADEABILITY.md`.

Build the normalized data pack with:

```bash
python scripts/build_research_snapshot.py
```

## Required sequence

1. `discovery.md` — create a broad candidate pool from current structured data.
2. `verification.md` — open primary sources and verify each material claim.
3. `analysis.md` — evaluate expectations, setup, invalidation, and risks.
4. `red_team.md` — try to reject each survivor.
5. `output_schema.md` — write the Markdown report and matching JSON evidence manifest.

Do not discover, verify, and rank in one undifferentiated pass. A model that cannot
obtain the required evidence must downgrade the name to Early Watch or Reject rather
than compensating with more prose.

## Outputs

Every run writes a pair:

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
```

A second same-day run adds `-HHMM` to both names. Run:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
```

The JSON manifest is the evidence contract. The Markdown report is the human-facing
analysis. A final candidate is invalid when the manifest fails validation.

## Fair model comparison

Use `evaluation_rubric.md`. Keep the input snapshot, source access, time, constraints,
and output schema identical. Record model, research mode, enabled data sources, input
snapshot hash, source count, and primary-source count in the manifest.
