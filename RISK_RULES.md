# Risk Rules

These are the human-readable personal rules. Executable values live in
`config/risk.toml`; change both together and record the reason below.

Review monthly. Change rules from accumulated evidence, never immediately after a
large win or loss.

## Position sizing — learning phase

- `position_size` means EUR capital deployed.
- Maximum position value: **€150**.
- Maximum binary-event hold: **€75**.
- Maximum open positions: **5**.
- Maximum same-sector/theme positions: **2**.
- Maximum total open position value: **€750**.

The fixed position value is deliberately not equal-risk sizing. Graduation to
risk-based sizing remains a later phase gate.

## Stops and reward/risk

- No stop, no defined risk, no computable R.
- Never move a stop farther away to avoid taking a loss.
- Never average down as a strategy.
- Proposal planned R must be at least **1.5R**.

## Catalyst and holding-period policy

A future event date is not itself a current setup.

- **Actionable research horizon:** catalyst inside **21 calendar days**.
- **Early Watch:** catalyst **22–42 days** away; review weekly, do not treat as a
  current proposal unless a separate verified trigger exists inside 21 days.
- **Default proposal holding period:** **10 trading sessions**.
- Every proposal records `max_holding_days` explicitly.
- Every catalyst-driven proposal defaults to `exit_before_catalyst = yes`.
- Holding through earnings, FDA/PDUFA, a court ruling, or another binary decision
  requires an explicit `exit_before_catalyst = no` and position value of €75 or less.

The 21-trading-day scanner return remains a research measurement only. It is not a
recommended holding period.

## Portfolio circuit breakers

Limits are expressed in R, where 1R is the entry-to-initial-stop risk.

- Daily realized loss limit: **−2R**. Stop opening trades for the day.
- Weekly realized loss limit: **−4R**. No new entries for the rest of the week.
- After **3 consecutive losses**, pause new entries for **3 calendar days** and
  review the journal.

A trade without a recorded initial stop cannot participate in R calculations; that
missing data is itself a rule breach.

## Earnings and other binary events

Preferred approach: trade after the information is public or exit before the event.

- Hold through only when planned at entry.
- Hold through only at €75 or less.
- Record the verified event date.
- Do not convert a pre-event trade into an event gamble because price moved against it.

## Currency and international exposure

The account is EUR-denominated.

- Accept small learning-phase FX exposure; no hedging at current size.
- Record and use broker-confirmed P&L for cross-currency trades.
- Price-level R remains valid when entry, stop, and exit share the same instrument currency.
- Enter foreign-market positions only during the allowed overlap-hours policy.
- Revisit explicit quantity, instrument-currency, and FX-rate fields before scaling.

## Known rule breaks

Record recurring behavior honestly:

1. _Fill as evidence accumulates._
2. _
3. _

## Changelog

| Date | Rule changed | Old | New | Why |
|---|---|---|---|---|
| 2026-06-27 | Initial learning rules | blank | €150 fixed position value and basic limits | Establish a measurable baseline |
| 2026-07-02 | Daily/weekly breakers | €150 / €300 | −2R / −4R | EUR limits could not trigger sensibly under fixed small positions |
| 2026-07-03 | Position size review | €150 | unchanged | Account deposit is not evidence to size up |
| 2026-07-10 | Research and proposal horizons | single 42-day catalyst window; 21-session proposal timeout | 21-day actionable / 22–42 Early Watch; 10-session default; pre-catalyst exit explicit | Distant catalysts allow too much thesis and price drift before the event |
| 2026-07-10 | Executable rule source | Python constants and prose | `config/risk.toml` plus this explanation | Prevent code/document drift |
