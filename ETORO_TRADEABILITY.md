# eToro Tradeability Filter

Use this file together with `RESEARCH_BRIEF.md`.

The weekly research routine should only include stocks/shares that the user can trade on eToro.

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

## Output fields

For every final candidate, include:

- `ETORO_TRADEABLE: YES`
- eToro evidence/source
- ticker used on eToro, if different from the exchange ticker
- exchange
- currency
- local listing vs ADR/proxy, where relevant
- non-US notes: FX, local market hours, settlement, and holiday-calendar risk

For rejected candidates, include the rejection reason, especially when the reason is eToro availability or verification failure.

## Liquidity floors

Keep the existing `RESEARCH_BRIEF.md` liquidity discipline, but apply it by region:

- US-listed names: minimum average daily dollar volume of $25M
- non-US names: minimum average daily value equivalent of $5M USD

A sparse report is better than a padded report. If few or no eToro-verified candidates qualify, say so.
