# SETUPS.md — Recommendation, Setup, and Proposal Standard

Research objects, recommendations, proposals, and trades are different things:

- **Research object:** a company/event worth following.
- **Recommendation:** this week's explicit action for that object.
- **Proposal:** a complete, measurable setup with trigger, invalidation, target, and expiry.
- **Trade:** an execution explicitly confirmed by the human.

A strong research thesis does not automatically become a proposal. The machine may prepare
research and proposal drafts; the human decides and records execution.

**Not financial advice.**

## Recommendation lifecycle

Every durable recommendation uses one status:

- `new`: first recorded review;
- `carry`: thesis remains valid without a stronger or weaker change;
- `upgraded`: evidence or price structure improved;
- `trigger_ready`: complete proposal-quality trigger exists for this week;
- `triggered`: the recorded condition occurred; this does not prove a trade occurred;
- `manage`: linked to an existing open trade;
- `downgraded`: thesis remains but setup quality weakened;
- `invalidated`: thesis or structure failed;
- `expired`: event or trigger window passed;
- `archived`: complete and retained for outcome analysis.

Every weekly review chooses exactly one action:

- `enter_if_triggered`
- `wait_pullback`
- `monitor`
- `manage`
- `remove`

The rolling current state lives in `data/recommendations.csv`. Every review or status change
appends a row to `data/recommendation_reviews.csv`. Old review rows are never rewritten.

## When a recommendation becomes a proposal

Only `enter_if_triggered` may create a proposal draft. It requires:

| Field | Rule |
|---|---|
| `ticker` + `direction` | Broker-tradeable; see `ETORO_TRADEABILITY.md` |
| `setup_type` | One of the definitions below |
| `entry_price` | A numeric trigger where the setup activates, not “current price” |
| `trigger_rule` | Observable condition explaining how the trigger is confirmed |
| `trigger_expiry` | Normally within five trading sessions |
| `stop_price` | Thesis or structure invalidation; no stop, no proposal |
| `target_price` | Realistic first target |
| `planned_r` | Reward/risk; must meet the configured minimum, normally at least 1.5 |
| `catalyst` + `catalyst_date` | Required when catalyst-driven and primary-source verified |
| `regime` | Newest available market-regime label |
| `thesis` | One line: why this, why now |
| `max_holding_days` | Default 10 trading sessions; shorten when needed |
| `exit_before_catalyst` | `yes` by default; `no` is an explicit binary-risk decision |

Proposals are logged whether traded or passed. Untraded proposals are the control group for
the picker test. A trigger occurring does not create a trade row; only explicit human
confirmation does.

A catalyst 22–42 days away belongs in `monitor` or `wait_pullback`, not in
`data/proposals.csv`, unless a separate verified trigger inside 21 days creates the actual
setup.

## Weekly action definitions

### `enter_if_triggered`

Use only when all proposal fields are complete. The recommendation must state:

- exact numeric trigger and observable confirmation;
- expiry date;
- do-not-chase condition;
- stop, target, and planned R;
- removal condition if the setup fails before triggering.

No market-order wording and no “buy around current price.” Missing the trigger is a valid,
zero-cost outcome.

### `wait_pullback`

The thesis is valid but price is extended or the initial move should not be chased. State
the desired structure or zone, removal condition, and next review date. Do not invent a
complete setup merely to make the report feel actionable.

### `monitor`

Research remains useful, but no current setup exists. State what would promote the idea and
when it will be reviewed again.

### `manage`

Use only for an open recorded trade. Link the trade ID and review the original thesis,
invalidation, event risk, and time stop. Do not infer an add, sale, or changed stop.

### `remove`

Use with `invalidated`, `expired`, or `archived`. State the exact reason. Removed ideas stay
in the registry and history for outcome analysis.

## Setup 1: `breakout`

A stock clearing a meaningful high with volume confirmation.

- Conditions: close above the 20-day high; relative volume at least 2x pace; daily move
  approximately +3% to +15%; not excessively extended.
- Entry: breakout-level retest or a close within roughly 2% of that level.
- Stop: below the breakout-day low or failed breakout level.
- Target: prior swing high or conservative measured move; planned R at least 1.5.
- Trigger expiry: normally five trading sessions.
- Holding horizon: normally 5–10 trading sessions.
- Defensive regime: log `regime-against` in notes.

## Setup 2: `pullback`

A confirmed runner bought on a defined retracement, not chased on the momentum day.

- Conditions: verified reason for the original move; clean invalidation; pullback holds the
  breakout level or a rising 10/20-day moving average.
- Entry: pre-defined retest zone plus an observable reversal/acceptance condition.
- Stop: below the pullback low or failed breakout level.
- Target: momentum high first; planned R at least 1.5.
- Trigger expiry: about five trading sessions.
- Holding horizon after trigger: normally 5–10 sessions.

Missing a runner is a zero-cost outcome; chasing one is not.

## Setup 3: `post-earnings-drift`

A non-binary trade after earnings information is public.

- Conditions: genuine surprise or raised guidance, gap roughly +5% or more, and the gap
  holds above its midpoint during the first one or two sessions.
- Entry: after consolidation, above the consolidation high.
- Stop: below the gap-day low or another evidence-based invalidation.
- Target: conservative drift target with planned R at least 1.5.
- Trigger expiry: normally five trading sessions after the initial consolidation forms.
- Holding horizon: normally 5–10 sessions; the earnings event has already occurred.

## Setup 4: `special-situation`

A dated structural catalyst such as index inclusion, verified lockup mechanics, spin-off
mechanics, or positioning before a regulatory decision.

- The mechanism and date must be verified from a primary source.
- Entry, stop, target, event-exit policy, and holding horizon are set in advance.
- Default is `exit_before_catalyst = yes`.
- Holding through earnings, FDA/PDUFA, rulings, or similar binary events requires
  `exit_before_catalyst = no` and the half-size rule in `RISK_RULES.md`.
- A normal stop cannot protect against an overnight binary gap; do not pretend otherwise.

## Deliberately not a setup

- “Scanner score is high.” That is a reason to research.
- “The report mentioned it.” That creates no entry.
- “The catalyst is in six weeks.” That is monitoring unless a nearer trigger exists.
- “It went up after I sold.” That is an outcome-analysis question, not a re-entry rule.
- “It is down a lot.”
- “Conviction is high” without a defined trigger and invalidation.
- “Buy now so I do not miss it.”

## Changelog

| Date | Change | Why |
|---|---|---|
| 2026-07-02 | Initial setup definitions and proposal standard | Make proposals measurable |
| 2026-07-10 | Add 10-session default horizon, pre-catalyst exit field, and 21-day actionable catalyst gate | Prevent distant catalysts from being treated as current setups |
| 2026-07-13 | Add rolling recommendation lifecycle, weekly actions, and trigger expiry | Preserve research continuity while separating candidate quality from entry timing |
