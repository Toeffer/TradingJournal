# Stage 5 — Outputs

Every run produces evidence artifacts, rolling recommendation state, and an immutable
weekly decision archive.

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
data/recommendations.csv
data/recommendation_reviews.csv
research/decisions/decisions-YYYY-MM-DD.csv
research/decisions/decisions-YYYY-MM-DD.meta.json
research/recommendation-book.md
```

A repeated same-day run uses `-HHMM` for the report, manifest, and decision archive. Never
overwrite an earlier run.

## Markdown report

The report is a weekly research and decision review, not a disconnected shortlist. Keep it
concise and decision-focused. The manifest and validators own compliance details.

```markdown
# Weekly Research and Decision Review — YYYY-MM-DD
DRAFT for human review. Not financial advice.

## Run metadata
- Model / research mode:
- Input snapshot / SHA-256:
- Prior reports reviewed:
- Active recommendations reviewed:
- Open positions reviewed:
- New leads / Actionable / Early Watch / Reject counts:
- Weekly decision: TRIGGERS AVAILABLE or NO NEW TRADE

## Prior recommendation audit
| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|

## Existing positions
### TICKER — MANAGE
- Linked trade:
- Original thesis / current thesis:
- Original invalidation:
- Event/time risk:
- This week's management review:

## Coming-week decision sheet
Maximum five names, normally no more than two `enter_if_triggered` rows.

### TICKER — ENTER IF TRIGGERED
- Recommendation ID / continuity:
- Verified reason and evidence:
- Current reference price / timestamp / source:
- Setup type:
- Trigger rule / numeric trigger / expiry:
- Stop / target / planned R / level basis:
- Do-not-chase condition:
- Catalyst / exit policy / max holding days:
- Removal condition / next review date:
- Red-team verdict / pre-mortem:

### TICKER — WAIT PULLBACK | MONITOR | MANAGE | REMOVE
- Recommendation ID / continuity:
- What changed:
- Why this action:
- Promotion or removal condition:
- Next review date:

## New research
### TICKER — Company
- Discovery origin:
- Evidence and classification:
- Why it did or did not displace a carry-over name:

## Removed or expired
- TICKER — exact reason and final status

## Sources used
- Primary sources first, then market data and context sources.
```

No current-price market order language is allowed. `enter_if_triggered` must be conditional
and expire. A report with no complete trigger states **NO NEW TRADE**.

## JSON evidence manifest

The canonical schema remains `research_method/candidate_manifest.schema.json`. It records
research evidence for every discussed candidate. Required run metadata includes:

- schema version, report date, generation timestamp;
- model and research mode;
- discovery method and enabled data sources;
- input snapshot path and SHA-256;
- source counts;
- one object for every Actionable, Early Watch, and rejected lead discussed.

Non-rejected catalyst candidates require verified primary-source date evidence, dated
structured market data, expectations evidence or an explicit unknown statement, and a
red-team verdict.

The manifest proves research claims. It does not replace the recommendation registry or
weekly review history.

## Current recommendation registry

`data/recommendations.csv` contains one current row per durable recommendation ID. It is a
convenience view of the latest state, not the historical record.

Required concepts:

- stable recommendation ID and first-mention date;
- latest source report and review timestamp;
- lifecycle status;
- weekly action;
- reference and mention prices;
- trigger, expiry, stop, target, planned R when trigger-ready;
- next review or removal condition;
- optional proposal and trade links.

A recommendation remains in the registry after removal with a terminal status. Do not
delete losing or expired objects.

## Append-only review ledger

`data/recommendation_reviews.csv` gets one new row whenever the model reviews or changes a
recommendation. The row records prior/new status, this week's action, levels as they existed
at the time, rationale, and links.

Never edit an old row to make a past recommendation look better. A factual correction is a
new review row with a note explaining the correction.

## Immutable weekly archive

After registry and review updates validate, run:

```bash
python scripts/archive_recommendation_reviews.py --date YYYY-MM-DD
```

The archive contains exactly that run's review rows. The matching metadata file records its
hash and row count. A repeated same-day run uses a time suffix.

## Human recommendation book

Run:

```bash
python scripts/summarize_recommendations.py
```

This renders `research/recommendation-book.md`, showing current actions and recently removed
ideas. It is derived output and must not be edited by hand.

## Validation

Run all applicable checks:

```bash
python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
python scripts/validate_recommendations.py
python scripts/validate_data.py
```

Fix errors before committing. Research uncertainty may remain only when the report states it
plainly and the action is no stronger than the evidence supports.
