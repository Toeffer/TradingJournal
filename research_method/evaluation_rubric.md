# Model comparison rubric

Compare models only when they receive the same repository commit, normalized snapshot,
recommendation history, source permissions, time window, research constraints, and output
schema. Remove model names before scoring when practical.

## Immediate research-and-decision scorecard

| Criterion | Weight | Full-credit standard |
|---|---:|---|
| Prior-recommendation continuity | 15 | Every active object and open position is reviewed; stable IDs are preserved; nothing disappears silently |
| Primary-source catalyst verification | 20 | Every non-rejected catalyst date is supported by an opened primary source and recorded in the manifest |
| Freshness and numerical accuracy | 15 | Market data is dated, consistent with the snapshot, and material numbers are traceable |
| Candidate-specific thesis and change analysis | 10 | Explains the actual business/event mechanics and what changed since prior reviews |
| Expectations and priced-in analysis | 10 | States what the market expects and whether recent price action already reflects it |
| Weekly action discipline | 15 | Each survivor gets one valid action; no forced buys; new names compete with carry-over names |
| Trigger and invalidation quality | 10 | Trigger-ready rows have observable rules, short expiry, defensible levels, valid R, and no chase language |
| Bear case and pre-mortem | 5 | Strongest failure path is specific and capable of downgrading or removing the object |

Maximum: 100.

## Automatic deductions

- Active prior recommendation omitted without a terminal review: minus 10 each.
- Open trade omitted from management review: minus 10 each.
- Final catalyst candidate with `date_status != verified`: minus 20 and mark invalid.
- Primary-source URL not opened by the synthesizing pass: mark invalid.
- Market data has no as-of timestamp/source: minus 10.
- `enter_if_triggered` without complete trigger, expiry, stop, target, or valid planned R:
  mark the recommendation invalid.
- Current-price market-order or chase wording: minus 15.
- Candidate retained after red-team Reject: mark invalid.
- Old review row rewritten instead of appending a new decision: mark run invalid.
- Unsupported numerical claim: minus 2 each, up to 20.

## Metadata to preserve

Record in the manifest/report:

- model and version/display name;
- research mode;
- enabled connected apps/data providers;
- repository commit;
- input snapshot path and SHA-256;
- recommendation history window and count reviewed;
- open-position count reviewed;
- start/end timestamps when available;
- sources opened and primary-source count;
- preliminary, Actionable, Early Watch, Reject, trigger-ready, and removed counts;
- explicit weekly decision: triggers available or no new trade.

## Outcome grading

Research quality, recommendation outcome, and human execution are separate:

1. Grade the report immediately with the scorecard above.
2. Grade each recorded recommendation from its immutable review row:
   - did the trigger occur before expiry;
   - stop-first versus target-first;
   - maximum favorable/adverse excursion after trigger;
   - mechanical R after the defined holding period.
3. Grade actual trades separately:
   - entry versus trigger;
   - early, on-time, or chased;
   - actual stop versus planned invalidation;
   - actual R versus mechanical recommendation R;
   - followed-plan result.
4. Do not retroactively change research quality because price moved.
5. Do not call an untriggered mention a trading success merely because the stock later rose.
6. Compare models only after multiple matched runs; one strong report is anecdotal.
