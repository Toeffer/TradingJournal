# ChatGPT research runbook

Use this for the ChatGPT version of the weekly candidate routine. It is deliberately
separate from Claude-native skills and follows `research_method/` exactly.

## Recommended ChatGPT setup

1. Generate and commit the normalized data pack first:

   ```bash
   python scripts/build_research_snapshot.py --archive
   ```

2. Start **Deep research** in ChatGPT rather than standard chat for the research pass.
3. Enable the GitHub app/plugin for this repository and the public web. Enable a
   financial-data app only as a supplement; the committed snapshot remains the common
   comparison input.
4. Prioritize company IR, SEC/EDGAR, regulator, exchange, EQS, RNS, Euronext/SIX, and
   official index/calendar domains. Allow broader web search for context.
5. Review the proposed research plan before it starts. It must contain separate
   discovery, verification, analysis, red-team, and synthesis stages.

Deep research uses connected apps for reading during research. Persisting files to
GitHub is a separate explicit write step after reviewing the report.

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

Use data/research_snapshot.csv as the canonical structured market-data input and
record the SHA-256 from data/research_snapshot.meta.json. Read the newest prior
candidate report and the newest relevant US/EU scanner reports for continuity.

Do not use model memory for current dates or market figures. Third-party calendars,
search snippets, scanner output, and subagent summaries are leads only. Open one
primary source yourself for every catalyst date that survives. A candidate whose date
is secondary-only, derived, or unverified must be rejected.

Do not rank during discovery. First build the broad pool, then verify facts, then
analyze expectations and current setup, then run a skeptical red-team pass. A final
Actionable candidate requires a verified catalyst inside 21 calendar days, dated market
data, evidence-based entry/stop/target levels, planned R of at least 1.5, a maximum
holding period, and an explicit exit-before-catalyst policy. Days 22–42 are Early Watch.

Produce two complete artifacts with matching basenames:
1. research/candidates-YYYY-MM-DD.md
2. research/manifests/candidates-YYYY-MM-DD.json

The JSON must follow research_method/candidate_manifest.schema.json. Keep the Markdown
report focused on company-specific evidence, expectations, priced-in analysis, setup,
risks, and the pre-mortem. Do not add a repetitive compliance table.

Return the complete Markdown and JSON, plus a short list of any evidence gaps. Do not
write to trades.csv or data/proposals.csv.
```

## Persist after review

In a normal ChatGPT turn with GitHub write access, attach or reference the completed
Deep Research output and say:

```text
Write these two reviewed artifacts to the paths specified in the report. Run or inspect
scripts/validate_candidate_manifest.py against the JSON. If validation fails, correct
the artifacts before committing. Open a PR; do not alter trades.csv or proposals.csv.
```

## Fair Claude/GPT comparison

For a comparison run, both models must use the same repository commit, snapshot hash,
source permissions, catalyst window, and output schema. Blind-score the reports with
`research_method/evaluation_rubric.md`; do not infer model superiority from one run.
