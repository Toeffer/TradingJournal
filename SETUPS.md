# SETUPS.md — Setup Definitions and the Proposal Standard

A trade idea only becomes a **proposal** when it matches one of the setups defined
here and every field of the proposal card is filled. This is what turns "HIMS looks
strong" into something that can be measured, simulated, and graded.

`setup_type` in `trades.csv` and `data/proposals.csv` must use the names defined
below. If an idea doesn't fit any definition, either it's not a trade — or the
definition needs a deliberate edit (log the change in the changelog at the bottom,
never bend a definition mid-trade).

**Not financial advice.** These are personal, mechanical descriptions of when I am
allowed to propose a trade to myself. The machine proposes; I decide.

---

## The proposal card (required for every proposal)

Every proposal — whatever the setup — must specify **all** of:

| Field | Rule |
|---|---|
| `ticker` + `direction` | eToro-tradeable (see `ETORO_TRADEABILITY.md`) |
| `setup_type` | one of the setups below |
| `entry_price` | a level, not "current price" — where the setup triggers |
| `stop_price` | the invalidation level; no stop, no proposal, ever |
| `target_price` | realistic first target, not the dream case |
| `planned_r` | (target − entry) / (entry − stop); **must be ≥ 1.5** |
| `catalyst` + `catalyst_date` | required for catalyst-driven setups; DATE_VERIFIED flag applies |
| `regime` | copied from the newest `data/market_regime.csv` row at proposal time |
| `thesis` | one line: why this, why now |

A proposal missing any field is rejected — by me, before it ever gets simulated.
Higher risk never means bigger size (see `RISK_RULES.md`).

Proposals are logged to `data/proposals.csv` whether or not I trade them. The
untraded ones are the control group — they're how I learn whether my picking among
proposals adds value or subtracts it.

---

## Setup 1: `breakout`

A stock clearing a meaningful high with volume confirmation.

- **Conditions (all):** close above the 20-day high; relative volume ≥ 2x pace;
  daily move between +3% and +15% (beyond that it's chase territory, see
  `pullback`); not more than ~25% above the 5-day high.
- **Entry:** the breakout level itself on a same/next-day retest, or the breakout
  day's close if the close is within ~2% of the breakout level.
- **Stop:** below the breakout day's low, or below the breakout level if the
  day's range is unusually wide.
- **Target:** prior swing high / measured move of the base; must give R ≥ 1.5.
- **Regime rule:** in a `defensive` regime, breakout proposals are logged but
  flagged `regime-against` — the stats will show whether they deserve to exist.
- **Half size:** if the stock has a history of gaps larger than the stop distance.

## Setup 2: `pullback`

The anti-chase setup — a **confirmed** runner bought on retracement, not on the day
it runs. This is the default answer to "the scanner found a big mover."

- **Conditions (all):** the name had a scanner alert or obvious momentum day with a
  *verified* reason (real catalyst or sector move — "it went up" is not a reason);
  clean invalidation exists; the pullback holds above the breakout level or rising
  10/20-day MA.
- **Entry:** the retest zone — prior breakout level or the rising MA, defined as a
  price, set in advance. The proposal *activates on the retest*; if price never
  pulls back, the proposal expires untriggered. **Missing a runner is a zero-cost
  outcome; chasing one is not.**
- **Stop:** below the pullback low once formed, or below the breakout level.
- **Target:** the momentum high first; must give R ≥ 1.5 from the *pullback* entry
  (this is the whole advantage — the same target gives better R from lower).
- **Expiry:** if not triggered within ~5 trading days, the proposal expires.

## Setup 3: `post-earnings-drift`

Riding the tendency of big earnings surprises to keep drifting — a non-binary
catalyst trade (the event is already public; nothing explodes overnight).

- **Conditions (all):** earnings gap of roughly +5% or more on a genuine beat /
  raised guidance (verified from the actual report, not headlines); gap holds —
  price stays above the gap-day midpoint on the first 1–2 sessions after.
- **Entry:** after the first consolidation/inside day, above that day's high.
- **Stop:** below the gap day's low (the drift thesis is dead if the gap fills).
- **Target:** measured from historical drift, conservatively; R ≥ 1.5 required.
- **Note:** this is the *preferred* earnings setup — entering after the binary
  event instead of holding through it.

## Setup 4: `special-situation`

Dated, structural, non-binary catalysts: index inclusion, lockup expiry with
verified date, spin-off mechanics, regulatory decision *positioning* (exit before
the binary event, per `RISK_RULES.md` half-size rule if held through).

- **Conditions (all):** the catalyst date is verified against a primary source;
  the mechanism is written in one sentence in the thesis ("index funds must buy X
  on date Y"); the exit plan relative to the event date is set at proposal time.
- **Entry / stop / target:** case-by-case, but all three set in advance; R ≥ 1.5.
- **Rule:** if the plan is to hold *through* a binary event, the half-size trigger
  from `RISK_RULES.md` applies automatically.

---

## What is deliberately NOT a setup

- "Scanner score is high" — that's a *reason to research*, which may end in a
  `pullback` or `breakout` proposal, or in nothing.
- "It's down a lot" / "it's cheap now" — falling-knife catching has no
  invalidation logic and no catalyst.
- "Conviction" without a matching definition — conviction is a field on the card,
  not a setup.

---

## Changelog

| Date | Change | Why |
|------|--------|-----|
| 2026-07-02 | Initial definitions (breakout, pullback, post-earnings-drift, special-situation) + proposal card standard | Make setup_type meaningful and proposals measurable |
