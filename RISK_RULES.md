# Risk Rules

These are your personal risk rules. The journal's `followed_plan` check is only
meaningful if there's a written plan to check against — this is that plan.

**Review these monthly.** Tighten or loosen based on what the journal data says, not
on how you feel after a win or loss.

---

## Per-trade risk

- **Max risk per trade:** €150 fixed position size per trade (learning phase — every
  euro at risk is tuition). This is the total position, not just the risk-to-stop.
- **Default position size formula:** €150 per trade, regardless of stop distance.
  When graduating to percentage-based sizing, switch to: account × max-risk% ÷
  (entry − stop).
- **Future rule (not active yet):** max 30% of account per trade, and only for
  low-risk setups with high reward-to-risk (planned R ≥ 2.0).
- **Reduced size triggers:** use half size (€75 or less) when:
  - [x] Holding through a binary event (earnings, FDA, etc.)
  - [x] Conviction is `low`
  - [x] The stock has a history of gaps larger than your stop distance
  - [ ] _(add your own)_

---

## Portfolio-level limits

- **Max open positions at once:** 5
- **Max correlated exposure:** no more than 2 positions in the same sector / theme
  at the same time.
- **Max total portfolio risk:** €750 across all open positions combined (5 × €150).

---

## Hold-through-earnings policy

This is the rule that matters most for event-driven trades and the one most often
broken.

- [ ] **Never hold through earnings** — always flat before the report.
- [x] **Hold through earnings only at half size or less.**
- [ ] **Hold through earnings only when planned at entry** (noted in thesis).
- [ ] _(your own rule)_

If you choose to hold, the journal will flag it against this rule at close.

---

## Currency and international exposure

Account is EUR-denominated (eToro, Germany/EU). Most positions will be in
USD-denominated US stocks, so there is baseline EUR/USD exposure on every trade.

- **Max non-USD exposure:** not applicable during learning phase — all positions are
  small (€150). Revisit when scaling up.
- **FX hedging policy:**
  - [x] **No hedging** — accept FX as part of the trade. Simpler, works for short holds
    and small positions.
  - [ ] **Hedge positions held longer than ___ days** (via FX forward, inverse ETF, etc.)
- **Reduced size for non-USD trades:** not applied during learning phase (positions are
  already small). Revisit when scaling up.
- **Overlap hours only:** only enter non-US positions during hours when both your local
  market and the foreign market are open.
  - [x] Yes, overlap-hours-only
  - [ ] No, I'll use limit orders and accept gap risk

---

## Loss limits (circuit breakers)

Limits are defined in **R** (multiples of risk-to-stop), not in position size. With
€150 fixed positions, a full stop-out typically loses €5-€25 depending on stop
distance — €-denominated limits sized like "one full position" could never trigger
(that would require the stock going to zero). R-based limits fire when the process
is actually going wrong.

Note the distinction: **position size** (€150, capital deployed) is not **risk**
(entry − stop × shares, what a stop-out actually costs). 1R = this trade's
risk-to-stop.

- **Daily loss limit:** stop trading for the day after **−2R realized** across
  closed trades that day.
- **Weekly loss limit:** no new entries for the rest of the week after **−4R
  realized** that week.
- **Consecutive-loss rule:** after 3 consecutive losses, pause for 3 days and run a
  journal review before the next trade.
- Trades with no recorded stop can't be counted in R — that is itself a rule break
  (see the pre-trade gate in `AGENTS.md`).

---

## Rules I know I break

Be honest. List the rules above (or unwritten habits) that you've historically
violated. The journal review will watch these specifically.

1. _(fill in as you start trading — the journal will help you spot these)_
2.
3.

---

## Changelog

Record when you change a rule and why, so you can see whether tightening or loosening
helped.

| Date | Rule changed | Old value | New value | Why |
|------|-------------|-----------|-----------|-----|
| 2026-06-27 | All rules | blank | Initial values | First fill based on learning-phase sizing (€150/trade) |
| 2026-07-02 | Daily/weekly loss limits | €150 / €300 | −2R / −4R realized | Old € limits equaled a full position loss (stock to zero) and could mathematically never trigger with €150 fixed sizing; R-based limits actually fire |
| 2026-07-03 | Position size (reviewed, unchanged) | €150 fixed | €150 fixed | Account was topped up (~2x; 5 full positions now ≈ half the depot). Deliberate decision to KEEP the fixed size: sizing graduates at the MASTERPLAN Phase 2 gate (data: 50+ closed trades, positive trailing expectancy, clean weeks) — not on deposits. Worst-case risk-to-stop across 5 positions is ~4-5% of the new depot, a sane learning-phase footprint; the extra capital is cushion, not license. |
