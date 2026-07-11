# LLM Research Playbook

This repository uses one evidence-first workflow for Claude, ChatGPT, and other models.
The model is responsible for judgment and synthesis; current structured data and opened
sources are responsible for facts.

**Not financial advice.** Research output is a draft. Only an explicit human statement
that a trade occurred may create a row in `trades.csv`.

## Core principle

Never ask a model to recall “promising stocks.” Split the work:

| Job | Input | Output |
|---|---|---|
| Discovery | normalized snapshot, scanner, event leads | broad traceable pool |
| Verification | opened primary sources, structured data | verified/rejected facts |
| Analysis | verified names, expectations, price structure | testable candidate cards |
| Red team | candidate cards and evidence | survive, downgrade, or reject |
| Measurement | proposals and later outcomes | evidence about whether the process works |

The canonical method is in `research_method/`. Model-native skills are optional
references only and cannot alter the evidence standard or output contract.

## Weekly preparation

1. Update scanner data normally.
2. Generate the common data pack:

   ```bash
   python scripts/build_research_snapshot.py
   ```

3. Record the snapshot SHA-256 from `data/research_snapshot.meta.json`.
4. Read the newest prior candidate report/manifest and relevant scanner reports.
5. Run the model using `RESEARCH_BRIEF.md` and the files in `research_method/`.
6. Validate the resulting manifest before committing:

   ```bash
   python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
   ```

## ChatGPT

Use `CHATGPT_RESEARCH_PROMPT.md`. Prefer Deep research for the multi-source research pass.
Use the GitHub connection and public web, prioritize primary-source domains, and review
the proposed plan before it runs. Persist the reviewed artifacts in a separate explicit
GitHub write step.

## Claude

Point the routine at `RESEARCH_BRIEF.md` on `main`. Claude-native equity-research skills
may help organize work, but the routine must still use the common snapshot, primary-
source gate, JSON manifest, and validator.

## Continuity

Each run reads the newest prior pair:

```text
research/candidates-*.md
research/manifests/candidates-*.json
```

- Mark a surviving prior name `REPEAT` and state what changed.
- Drop events that passed unless a new verified event exists.
- Mark catalysts inside seven days `ACT-NOW`.
- Preserve prior reports; never overwrite same-day work.

## Scanner use

Scanner score is a research-priority signal, not a thesis.

For scanner-seeded names independently verify:

- reason for the move and whether it is already public;
- forward catalyst and primary-source date;
- financing/dilution and event risk;
- liquidity and spread;
- current invalidation structure.

Reject any name whose only rationale is that it moved or scored highly.

## Primary-source discipline

The final synthesizing pass must open the source. A citation copied from a subagent,
search snippet, calendar aggregation, or prior report does not count.

- Company IR, filings, exchange/regulator notices, prospectuses, and official calendars:
  primary evidence.
- FMP, Alpaca, Stooq, Yahoo, or another dated provider: market-data evidence.
- Reuters and other reputable news: expectations/context evidence.
- Blogs, forums, analyst notes, and social media: leads only.

Final Actionable and Early Watch dates require `date_status = verified` and a primary
source recorded in the manifest.

## Technical-level discipline

Do not turn whatever price a broker page exposes into a stop. Entry, stop, and target
must be based on observable structure or thesis invalidation and state that basis.
Examples:

- below a confirmed swing/base low;
- below a breakout level after failed acceptance;
- below a gap-support level;
- thesis invalidation caused by a filing or event change.

When no defensible level exists, keep the name in Early Watch or Reject it.

## Second opinion

Use `SECOND_OPINION.md` only after the first report and manifest exist. Give the second
model the same snapshot and sources. Disagreement is a prompt to inspect evidence, not a
vote between models.

## Fair comparison

Use `research_method/evaluation_rubric.md`. A matched comparison requires the same:

- repository commit;
- snapshot hash;
- source permissions and providers;
- time and catalyst window;
- research method and output schema.

Blind-score primary verification, accuracy, company-specific depth, expectations,
setup quality, bear case, and usability. Keep market outcome grading separate from
research-quality grading.

## Weekly rhythm

- During the week: scanners collect observations; do not screen-watch.
- Weekend: generate snapshot and run research.
- Before any proposal: verify the manifest and current chart/market data.
- Monday: read the digest and inspect imminent event exits.
- Monthly: compare proposals, passed ideas, and matched model runs.

A no-candidate report is a successful result when evidence or setup quality is weak.
