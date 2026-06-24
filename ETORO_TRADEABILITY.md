# eToro Tradeability Filter

Use this file together with `RESEARCH_BRIEF.md`.

The weekly research routine should only include stocks/shares that the user can trade on eToro.
When this file conflicts with the older CONFIG in `RESEARCH_BRIEF.md`, this file is the broker/universe overlay and should win for tradeability, market-cap exceptions, and liquidity tiers.

## Account baseline

- Broker: eToro
- Account region: Germany / EU, unless the user changes this later
- Asset class: stocks/shares only
- Regions allowed: US, Europe, Asia

## Hard rule

A candidate can only enter the final shortlist if eToro tradeability is verified.

For every preliminary candidate, check whether the stock/share appears tradeable on eToro for the account region at the time of the run.

Accept final candidates only when:

- `ETORO_TRADEABLE: YES`
- the evidence is listed in the report
- the instrument is a stock/share or clearly acceptable equivalent for the user

Reject candidates when:

- eToro availability cannot be verified
- the instrument is unavailable in the account region
- the instrument type is unclear
- the only available route is not suitable for the user

Do not assume that an exchange listing is enough. A stock listed on NYSE, NASDAQ, LSE, XETRA/Frankfurt, Euronext, SIX, TSE/Tokyo, HKEX, SGX, ASX, or KRX still needs eToro verification.

## Market-cap universe

The routine should prefer small/mid caps but should not blindly exclude a larger-cap setup if it is clearly the best trade-quality candidate.

Use three buckets:

1. **Core universe:** $500M-$10B market cap, or USD equivalent. This remains the main search area because it usually has better breakout potential than mega-caps.
2. **Larger-cap exception bucket:** $10B-$50B market cap, or USD equivalent. Include at most 1-2 names from this bucket per report, and only when the setup is clearly stronger than the available core-universe candidates.
3. **Excluded by default:** mega-caps above $50B, the Magnificent 7, and obvious crowded headline AI names. These may only appear in rejected candidates or market-context notes unless the user explicitly widens the routine.

For larger-cap exception names, the report must explain why the setup deserves an exception, why it is not already crowded/priced in, and why it is still suitable for a swing-trade candidate rather than just a high-quality company.

## Liquidity tiers

Keep liquidity discipline, but do not make the preferred floor the only signal.

Preferred floors:

- US-listed names: average daily dollar volume of at least $25M
- non-US names: average daily value equivalent of at least $5M USD

Conditional watchlist range:

- US-listed names: $10M-$25M average daily dollar volume
- non-US names: $3M-$5M USD-equivalent average daily value

Conditional names may be included only in a separate **Conditional Watchlist**, not the main shortlist, unless the user explicitly approves a lower-liquidity setup. For every conditional name:

- eToro tradeability must still be verified
- the catalyst must be primary-source or high-quality-source verified
- the report must discuss spread/liquidity/slippage risk
- risk rating must be `High`
- position size should be treated as reduced or `risk rule not set` if no personal rule exists
- do not hold through binary events unless the user has explicitly written that rule in `RISK_RULES.md`

A sparse report is better than a padded report. If few or no eToro-verified candidates qualify, say so.

## Output fields

For every final candidate, include:

- `ETORO_TRADEABLE: YES`
- eToro evidence/source
- ticker used on eToro, if different from the exchange ticker
- exchange
- currency
- market-cap bucket: core or larger-cap exception
- local listing vs ADR/proxy, where relevant
- non-US notes: FX, local market hours, settlement, and holiday-calendar risk

For rejected candidates, include the rejection reason, especially when the reason is eToro availability, market-cap exclusion, liquidity tier, or verification failure.

For conditional watchlist names, include the same fields plus the exact reason the name is not in the main shortlist.
