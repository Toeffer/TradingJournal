# Stage 3 — Research-object analysis

Analyze only new or carry-over objects that passed verification. The goal is not to predict
price or force an entry. It is to decide whether the thesis remains useful and whether a
current, testable setup exists for the next five trading sessions.

## Continuity first

For a carry-over object, begin with:

- original mention date, price, thesis, and recommendation ID;
- previous status/action and whether its trigger occurred;
- price path and material evidence changes since the last review;
- whether the object should improve, retain, weaken, or leave the active book.

Do not reset the analysis merely because a new weekly report is being written.

## Expectations first

Before writing the bull case, establish what the market appears to expect:

- consensus or company guidance where available;
- recent estimate revisions or guidance changes;
- prior event reaction and current valuation/positioning context;
- recent price move, distance from support/resistance, and whether the catalyst is crowded
  or priced in.

If expectations cannot be established, lower confidence and choose no stronger than
`monitor` unless a purely price-structural setup has independent evidence.

## Research classification versus weekly action

Research classification and weekly action are separate decisions:

- An `ACTIONABLE` object may still receive `wait_pullback` or `monitor`.
- `EARLY_WATCH` normally receives `monitor`.
- `REJECT` receives `remove` or never enters the registry.
- Only a complete setup may receive `enter_if_triggered`.

## Trigger-ready requirements

An `enter_if_triggered` recommendation requires:

- a verified event or intermediate reason within 21 calendar days when catalyst-driven;
- current dated market data;
- an allowed setup from `SETUPS.md`;
- a numeric entry trigger tied to observable structure;
- an explicit trigger rule and expiry, normally within five trading sessions;
- a stop/invalidation tied to structure or thesis failure;
- a realistic first target;
- planned reward/risk of at least the configured minimum;
- a do-not-chase condition;
- a removal condition if the setup fails before triggering;
- maximum holding period and event-exit policy;
- red-team verdict `SURVIVE`.

Do not use a broker-page day low or arbitrary percentage merely because it is available.
When no defensible complete setup exists, use `wait_pullback`, `monitor`, or `remove`.

## Research card

For each survivor record:

1. Recommendation ID, continuity, company, exchange, currency, and source tag.
2. Verified catalyst mechanics, date, and days remaining when relevant.
3. What changed since the first mention and last review.
4. Why now—or why not now.
5. Market expectations and priced-in assessment.
6. Appropriate weekly action.
7. For trigger-ready objects: trigger, expiry, stop, target, planned R, and level basis.
8. Bull, base, and bear scenarios.
9. Financing, dilution, insider, short, liquidity, spread, FX, and gap risks.
10. Risk rating and confidence, with evidence that would change either.
11. Next review or removal condition.
12. A pre-mortem stating the most likely overlooked reason the object or setup fails.

## Open positions

An open trade is reviewed with action `manage`, linked by trade ID. Preserve its original
invalidation and distinguish a thesis review from an execution instruction. Do not infer
that a stop, target, or position size changed.

## Evidence density

Prefer company-specific and setup-specific facts over generic prose. Repeated compliance
language belongs in the manifest or validator output. A concise `NO NEW TRADE` conclusion is
better than a complete-looking but invalid setup.
