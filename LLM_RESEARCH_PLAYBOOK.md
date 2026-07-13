# LLM Research Playbook

This repository uses one evidence-first weekly research and decision workflow for Claude,
ChatGPT, and other models. The model maintains durable research objects, reviews prior
recommendations, and issues conditional actions for the next five trading sessions.

**Not financial advice.** Research output is a draft. Only an explicit human statement that
a trade occurred may create or alter a row in `trades.csv`.

## Core principle

Do not ask a model to recall promising stocks or produce a fresh disconnected list. Split
the work:

| Job | Input | Output |
|---|---|---|
| Continuity | last six weeks, recommendation ledgers, open trades | prior-decision audit |
| Discovery | normalized snapshot, scanner, event leads | broad traceable pool |
| Verification | opened primary sources, structured data | verified/rejected facts |
| Analysis | verified names, expectations, price structure | durable research objects |
| Red team | prior history, candidate cards, evidence | survive, downgrade, or remove |
| Weekly decision | complete setups and active objects | enter-if-triggered, wait, monitor, manage, remove |
| Measurement | review history, proposals, trades, later prices | research, recommendation, and execution attribution |

The canonical method is `RESEARCH_BRIEF.md` plus `research_method/`. Model-native skills
cannot alter the evidence standard, lifecycle, or output contract.

## Weekly preparation

1. Update scanner data normally.
2. Generate the common data pack:

   ```bash
   python scripts/build_research_snapshot.py --archive
   ```

3. Record the snapshot SHA-256 from `data/research_snapshot.meta.json`.
4. Read:
   - `trades.csv` and `data/proposals.csv`;
   - `data/recommendations.csv` and `data/recommendation_reviews.csv`;
   - `research/recommendation-book.md`;
   - candidate reports/manifests from the prior six weeks;
   - every older report linked by an unresolved recommendation;
   - recent US/EU scanner reports and measured outcomes.
5. Run the model using `RESEARCH_BRIEF.md`.
6. Validate and archive the reviewed artifacts:

   ```bash
   python scripts/validate_candidate_manifest.py research/manifests/candidates-YYYY-MM-DD.json
   python scripts/validate_recommendations.py
   python scripts/archive_recommendation_reviews.py --date YYYY-MM-DD
   python scripts/summarize_recommendations.py
   python scripts/validate_data.py
   ```

## Required sequence

A weekly run follows this order:

1. Review every active recommendation.
2. Review every open position without inferring an execution.
3. Measure what happened to prior triggers where data permits.
4. Discover and verify new names.
5. Make new names compete with carry-over names.
6. Run a skeptical red-team pass.
7. Issue exactly one weekly action for every surviving object.
8. State `NO NEW TRADE` when no complete trigger exists.
9. Append review rows and archive them; never rewrite prior decisions.

## Recommendation versus proposal

A recommendation may say wait, monitor, manage, or remove. It becomes proposal-quality only
when it is `trigger_ready` and uses `enter_if_triggered` with:

- an allowed setup;
- numeric trigger, stop, target, and valid planned R;
- an observable trigger rule;
- a short expiry, normally five trading sessions;
- current market data;
- a removal condition;
- a surviving red-team verdict.

No current-price market-order language is allowed. Missing a trigger is a valid zero-cost
outcome.

## Continuity and immutability

- `data/recommendations.csv` is the current registry.
- `data/recommendation_reviews.csv` is append-only history.
- `research/decisions/decisions-*.csv` files are immutable run archives.
- `research/recommendation-book.md` is generated current state.

Preserve recommendation IDs across weeks. A name leaves the active book only through an
explicit `invalidated`, `expired`, or `archived` review. Never delete a failed idea.

## Scanner use

Scanner output prioritizes research; it does not establish a thesis or an entry. Verify the
reason for the move, whether the information is already public, financing/dilution, event
risk, liquidity, and current structure. Reject a name whose only rationale is score or
price movement.

## Source and level discipline

The final synthesizing pass opens the primary source. Search snippets, calendars, scanner
rows, prior reports, and subagent summaries are leads only.

Entry, stop, and target must come from observable structure or thesis invalidation. Do not
turn a broker-page day low or arbitrary percentage into a proposal merely because it is
available. When no defensible setup exists, use `wait_pullback` or `monitor`.

## Outcome attribution

Keep three questions separate:

1. **Research:** did the company/event thesis identify a meaningful opportunity?
2. **Recommendation:** did the recorded trigger produce a measurable setup outcome?
3. **Execution:** did the actual trade follow and improve upon the recommendation?

Do not call a stopped trade a research failure when the candidate later worked, and do not
call a research mention a success when no valid trigger existed. The append-only reviews
are the evidence needed to distinguish those cases.

## ChatGPT and Claude

- ChatGPT: use `CHATGPT_RESEARCH_PROMPT.md`, preferably with Deep research and GitHub/public
  web reading. Persist reviewed files in a separate explicit write step.
- Claude: point the routine at `RESEARCH_BRIEF.md` on `main`. Claude-native research skills
  may organize work but must still use the common snapshot, ledgers, manifest, validators,
  and immutable archives.

## Weekly rhythm

- During the week: scanners collect observations; no screen-watching requirement.
- Weekend: update outcomes, snapshot data, review continuity, and research new names.
- Before the week: inspect the maximum-five decision sheet and trigger expiries.
- During the week: record whether triggers occurred; do not reinterpret them after the fact.
- Monday digest/review: manage open positions and expired triggers.
- Monthly: compare research outcomes, mechanical recommendations, passed proposals, and
  actual execution separately.

A no-new-trade report is a successful result when no setup has earned an entry.
