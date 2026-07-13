# Stage 4 — Red team

Assume each surviving research object and each proposed trigger is wrong. When tooling
permits, the red-team pass is separate from the analyst who first liked the idea.

## Required attacks

For every object ask:

- Is the catalyst date, mechanism, or source wrong?
- Did the event already occur, move, or become less material?
- Is expected good news already reflected in price and estimates?
- Is the thesis merely a high-beta, sector-sympathy, scanner, or thematic move?
- Can financing, dilution, insider selling, lockup release, or an offering overwhelm it?
- Is liquidity adequate at intended entry and exit times, not only on average?
- Is there an intervening earnings or macro event?
- Would the object still deserve research without its scanner score or story?
- Has the same thesis or ticker already failed in the rolling book? What is genuinely
  different now?
- Is the object being retained because of sunk research effort rather than current evidence?

For every `enter_if_triggered` proposal additionally ask:

- Is this early anticipation disguised as confirmation?
- Has the move already happened, making the trigger a chase?
- Does the trigger represent observable acceptance, or merely crossing an arbitrary price?
- Is the stop real invalidation, or a nearby number selected to manufacture attractive R?
- Can an overnight gap make the risk arithmetic meaningless?
- Is the trigger expiry short enough to prevent a stale setup?
- Does the target remain realistic after spread, slippage, and nearby resistance?
- Would `wait_pullback`, `monitor`, or `NO NEW TRADE` be more honest?

For open positions ask:

- Is the recommendation quietly moving the original stop farther away?
- Is management being confused with an add-on entry?
- Has the original thesis expired even though price has not reached the stop?
- Is event risk inconsistent with the recorded size and policy?

## Verdicts

Use one:

- `SURVIVE`: evidence and, when relevant, complete setup remain intact.
- `DOWNGRADE_EARLY_WATCH`: research remains useful but current setup is premature.
- `REJECT`: evidence, tradeability, expectations, timing, or risk invalidates the object.

Only `SURVIVE` may receive `enter_if_triggered`. A surviving research object may still
receive `wait_pullback` or `monitor`. Record the strongest rejection argument and why the
object survived it. Never weaken bear cases to fill a decision sheet.
