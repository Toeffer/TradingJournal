# SETUPS.md — Setup Definitions and Proposal Standard

A trade idea becomes a **proposal** only when it matches a defined setup and every
required field is filled. The machine may prepare a draft; the human decides.

**Not financial advice.**

## Required proposal card

| Field | Rule |
|---|---|
| `ticker` + `direction` | Broker-tradeable; see `ETORO_TRADEABILITY.md` |
| `setup_type` | One of the definitions below |
| `entry_price` | A level where the setup triggers, not “current price” |
| `stop_price` | Invalidation; no stop, no proposal |
| `target_price` | Realistic first target |
| `planned_r` | Reward/risk; must be at least 1.5 |
| `catalyst` + `catalyst_date` | Required when catalyst-driven and primary-source verified |
| `regime` | Newest available market-regime label |
| `thesis` | One line: why this, why now |
| `max_holding_days` | Default 10 trading sessions; shorten when the setup needs it |
| `exit_before_catalyst` | `yes` by default; `no` is an explicit binary-risk decision |

Proposals are logged whether traded or passed. Untraded proposals are the control
group for the picker test.

A catalyst 22–42 days away belongs in the research **Early Watch** section, not in
`data/proposals.csv`, unless a separate verified trigger inside 21 days creates the
actual setup.

## Setup 1: `breakout`

A stock clearing a meaningful high with volume confirmation.

- Conditions: close above the 20-day high; relative volume at least 2x pace;
  daily move approximately +3% to +15%; not excessively extended.
- Entry: breakout-level retest or a close within roughly 2% of that level.
- Stop: below the breakout-day low or failed breakout level.
- Target: prior swing high or conservative measured move; planned R at least 1.5.
- Holding horizon: normally 5–10 trading sessions.
- Defensive regime: log `regime-against` in notes.

## Setup 2: `pullback`

A confirmed runner bought on a defined retracement, not chased on the momentum day.

- Conditions: verified reason for the original move; clean invalidation; pullback
  holds the breakout level or a rising 10/20-day moving average.
- Entry: pre-defined retest zone.
- Stop: below the pullback low or failed breakout level.
- Target: momentum high first; planned R at least 1.5.
- Trigger expiry: about five trading sessions.
- Holding horizon after trigger: normally 5–10 sessions.

Missing a runner is a zero-cost outcome; chasing one is not.

## Setup 3: `post-earnings-drift`

A non-binary trade after the earnings information is public.

- Conditions: genuine surprise or raised guidance, gap roughly +5% or more, and
  the gap holds above its midpoint during the first one or two sessions.
- Entry: after consolidation, above the consolidation high.
- Stop: below the gap-day low.
- Target: conservative drift target with planned R at least 1.5.
- Holding horizon: normally 5–10 sessions; the earnings event has already occurred.

## Setup 4: `special-situation`

A dated structural catalyst such as index inclusion, verified lockup mechanics,
spin-off mechanics, or positioning before a regulatory decision.

- The mechanism and date must be verified from a primary source.
- Entry, stop, target, event-exit policy, and holding horizon are set in advance.
- Default is `exit_before_catalyst = yes`.
- Holding through earnings, FDA/PDUFA, rulings, or similar binary events requires
  `exit_before_catalyst = no` and the half-size rule in `RISK_RULES.md`.

## Deliberately not a setup

- “Scanner score is high.” That is a reason to research.
- “The catalyst is in six weeks.” That is Early Watch unless a nearer trigger exists.
- “It is down a lot.”
- “Conviction is high” without a defined entry and invalidation.

## Changelog

| Date | Change | Why |
|---|---|---|
| 2026-07-02 | Initial setup definitions and proposal standard | Make proposals measurable |
| 2026-07-10 | Add 10-session default horizon, pre-catalyst exit field, and 21-day actionable catalyst gate | Prevent distant catalysts from being treated as current setups |
