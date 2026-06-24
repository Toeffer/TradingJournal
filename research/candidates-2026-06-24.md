# Candidate Shortlist — 2026-06-24

DRAFT for human review. Verify all dates/numbers before trading.
Any size shown is YOUR fixed rule as arithmetic, not a recommendation.

## Summary

- 2 candidates, 2 deep-dived.
- This ad-hoc run used `RESEARCH_BRIEF.md` plus `ETORO_TRADEABILITY.md` as the active broker/universe overlay.
- Main candidates are limited to eToro-verified stocks/shares, preferred-liquidity names, and dated catalysts inside the next 28 days.
- The cleanest verified setups found quickly were still mostly US-listed because eToro-verifiable European/Asian names with near-term, high-quality dated catalysts were harder to confirm in this run.
- Risk rule context: `RISK_RULES.md` is present, but the key inputs are blank. Max risk per trade, max open positions, max total portfolio risk, hold-through-earnings policy, non-USD exposure, FX policy, and circuit breakers are all **risk rule not set**.

## Shortlist

### 1. BB — BlackBerry Limited

- eToro: `ETORO_TRADEABLE: YES` | Mode: stock/share | Evidence: eToro page says “Create an eToro account to buy BB stock” and shows BB as BlackBerry Limited.
- Exchange / Currency: NYSE / USD.
- Market-cap bucket: core universe.
- Catalyst: earnings week candidate; Kiplinger lists BlackBerry (BB) in the Thursday 2026-06-25 earnings slate. | DATE_VERIFIED: NO
- Why now: eToro shows BB down 5.10% on the day and 9.80% over the past week, which creates a possible post-earnings reaction/bounce-or-breakdown setup rather than a clean pre-earnings buy setup.
- Bull / Bear: Bull case is a software-turnaround/QNX/cybersecurity narrative with prior upbeat guidance context; bear case is very high event risk around earnings and valuation sensitivity after a volatile move.
- Priced-in check: eToro already shows BB down sharply into the event; Reuters reported in April that BlackBerry said its turnaround was complete and forecast Q1 revenue above estimates, so some optimism may already be reflected despite the recent pullback.
- Invalidation: preliminary planning invalidation below the current day-low area around $8.20. Because this is an earnings/binary setup, a gap through that level is possible; do not treat this as a reliable stop through earnings.
- Liquidity: eToro reports average volume of 27.54M shares and price $8.38, roughly $231M average daily dollar value. Preferred liquidity floor passed.
- Non-US notes: company is Canadian, but this is the NYSE USD listing on eToro. FX/local-hours risk is limited to the USD-listed instrument, but company fundamentals still include Canada exposure.
- Risk: High — binary earnings event, high recent volatility, beta 1.57, unclear hold-through-earnings rule, and gap risk.
- Risk/share: planning proxy $8.38 - $8.20 = $0.18. This is not valid if holding through an earnings gap; verify on chart before any trade.
- Suggested size: risk rule not set. Set `ACCOUNT_SIZE` and `RISK_PER_TRADE_PCT` only after filling `RISK_RULES.md`.
- Confidence: Medium-low — eToro tradeability and liquidity are verified; catalyst date is from a high-quality earnings calendar but should be verified from BlackBerry IR before use.
- Sources: eToro BB page: https://www.etoro.com/markets/bb ; Kiplinger earnings calendar: https://www.kiplinger.com/investing/stocks/17494/next-week-earnings-calendar-stocks ; Reuters BlackBerry turnaround/Q1 guidance context: https://www.reuters.com/business/blackberry-forecasts-upbeat-quarterly-revenue-says-turnaround-complete-2026-04-09/

### 2. AYI — Acuity Inc.

- eToro: `ETORO_TRADEABLE: YES` | Mode: stock/share | Evidence: eToro page says “Create an eToro account to buy AYI stock” and shows Acuity Inc. / AYI.
- Exchange / Currency: NYSE / USD.
- Market-cap bucket: core universe.
- Catalyst: earnings week candidate; Kiplinger lists Acuity (AYI) in the Thursday 2026-06-25 earnings slate. | DATE_VERIFIED: NO
- Why now: AYI is a core-market-cap name with a near-term earnings catalyst. eToro shows the stock down 3.68% over the past week but up 1.24% on the day, so the setup is a possible pre-event stabilization/pullback rather than an already extended move.
- Bull / Bear: Bull case is that the company can show continued benefits from building-management/lighting demand and integration of acquired assets; bear case is that earnings disappoint, recent weakness continues, or margins/guidance fail to support the valuation.
- Priced-in check: AYI had strong prior-year earnings reaction after QSC helped results, so the market may already expect execution from the acquisition and Intelligent Spaces segment.
- Invalidation: preliminary planning invalidation below the current day-low area around $291.50.
- Liquidity: eToro reports average volume of 405,365.61 shares and price $299.88, roughly $121.6M average daily dollar value. Preferred liquidity floor passed.
- Non-US notes: N/A; USD US listing.
- Risk: Medium-high — earnings event, but better liquidity and a more established business than many small caps. Risk is elevated because the catalyst is binary and the personal hold-through-earnings rule is blank.
- Risk/share: planning proxy $299.88 - $291.49 = $8.39. Verify on chart before use.
- Suggested size: risk rule not set. Set `ACCOUNT_SIZE` and `RISK_PER_TRADE_PCT` only after filling `RISK_RULES.md`.
- Confidence: Medium — eToro tradeability/liquidity are verified and catalyst is dated via earnings calendar; should still be verified on Acuity IR before use.
- Sources: eToro AYI page: https://www.etoro.com/markets/ayi ; Kiplinger earnings calendar: https://www.kiplinger.com/investing/stocks/17494/next-week-earnings-calendar-stocks ; prior AYI/QSC earnings context: https://www.investopedia.com/acuity-stock-jumps-on-strong-results-thanks-to-lighting-firm-s-qSC-acquisition-11761679

## Conditional Watchlist

None. I did not include lower-liquidity names because the two shortlisted candidates already passed preferred liquidity floors, and lower-liquidity names should not be promoted without stronger verification and personal risk rules.

## Rejected Candidates

- KFY — rejected because the earnings catalyst was listed for Tuesday 2026-06-23, already past at run time. eToro tradeability and liquidity appear acceptable, but the routine is looking for live forward catalysts. eToro KFY: https://www.etoro.com/markets/kfy ; Kiplinger earnings calendar: https://www.kiplinger.com/investing/stocks/17494/next-week-earnings-calendar-stocks
- JEF — rejected because it is a larger-cap exception name around $12.84B and the Wednesday earnings catalyst was too close/possibly already in progress at run time. It did not clearly beat the core-universe names for clean setup quality. eToro JEF: https://www.etoro.com/markets/jef ; Kiplinger earnings calendar: https://www.kiplinger.com/investing/stocks/17494/next-week-earnings-calendar-stocks
- DRI — rejected because it is a larger-cap exception name around $24.12B and did not clearly deserve one of the limited exception slots versus core names. eToro verifies tradeability, and Kiplinger lists it for Thursday earnings, but it looks more like a broad consumer earnings read-through than an underfollowed small/mid-cap breakout. eToro DRI: https://www.etoro.com/markets/dri ; Kiplinger earnings calendar: https://www.kiplinger.com/investing/stocks/17494/next-week-earnings-calendar-stocks
- MKC — rejected because it is a larger-cap exception name around $13.15B and the setup appears more defensive/low-beta than breakout-oriented. eToro verifies tradeability, but it did not clearly beat AYI/BB on event-driven swing setup quality. eToro MKC: https://www.etoro.com/markets/mkc ; Kiplinger earnings calendar: https://www.kiplinger.com/investing/stocks/17494/next-week-earnings-calendar-stocks
- PAYX — rejected as an excluded mega-cap/large-cap context name rather than small/mid-cap candidate. eToro verifies tradeability, but the market cap is outside the preferred/exception universe. eToro PAYX: https://www.etoro.com/markets/payx
- SNX / TD Synnex — rejected because the eToro `/markets/snx` page resolved to Synthetix crypto, not a clearly verified TD Synnex stock/share instrument. eToro tradeability as the intended stock could not be verified.
- European/Asian candidates — no final non-US candidate was included because I did not verify both eToro tradeability and a clean dated catalyst inside the 28-day window during this run. The report should not pad with unverified instruments.

## Deep Dives (top 2 front-runners)

### BB — BlackBerry Limited

- eToro tradeability: verified via public eToro BB page; eToro displays BB as BlackBerry Limited and says users can buy BB stock. Public availability may still differ by account status; verify inside the logged-in Germany/EU account.
- Catalyst mechanics & what's priced in: BB is listed by Kiplinger in the Thursday 2026-06-25 earnings slate. Reuters' April context said BlackBerry forecast Q1 revenue above estimates and declared its turnaround complete, so earnings expectations may already include a turnaround/QNX narrative. The current eToro page shows a sharp one-week pullback, so the market may be resetting expectations into the event rather than fully rewarding the story.
- Bull:
  - Core turnaround narrative remains active; prior Reuters coverage cited above-estimate Q1 revenue outlook.
  - QNX/embedded software exposure gives a differentiated software angle rather than old handset baggage.
  - High liquidity on the NYSE listing makes it executable compared with many small caps.
  - Recent pullback could create a clearer post-earnings level if reaction is constructive.
- Bear:
  - Earnings is a binary event and can gap through any stop.
  - eToro shows high beta and steep recent drawdown; volatility risk is high.
  - Prior positive guidance may already be priced in by investors who know the turnaround story.
  - No personal hold-through-earnings rule is set, so the routine cannot assume this is acceptable to hold through the event.
- Key levels: support/invalidation proxy near $8.20 day-low area; resistance/decision area near $9.02 day-high and then the broader 52-week high around $10.90. Verify on a real chart.
- Main risk: binary earnings gap plus unfilled personal risk policy.
- Pre-mortem: the trade loses because earnings/guidance are merely okay, the turnaround story was already priced in, and the stock gaps below the pre-event range before a stop can work.
- Risk: High | Risk/share: planning proxy $0.18 | Suggested size: risk rule not set.
- Sources: eToro BB, Kiplinger earnings calendar, Reuters April BlackBerry context. DATE_VERIFIED: NO.

### AYI — Acuity Inc.

- eToro tradeability: verified via public eToro AYI page; eToro displays AYI as Acuity Inc. and says users can buy AYI stock. Verify inside the logged-in Germany/EU account before acting.
- Catalyst mechanics & what's priced in: AYI is listed by Kiplinger in the Thursday 2026-06-25 earnings slate. Prior-year coverage showed AYI jumped after strong results helped by QSC, so the market likely expects acquisition/Intelligent Spaces contribution. The current eToro page shows a weekly decline, which may suggest some caution before the report.
- Bull:
  - Core $9.09B market-cap name with enough liquidity for clean execution.
  - Earnings catalyst is imminent and dated.
  - Prior QSC/Intelligent Spaces contribution gives a concrete metric area to watch.
  - Recent weakness could provide a defined reaction setup after results.
- Bear:
  - Earnings expectations may already include QSC/acquisition benefits.
  - A miss or margin/guidance disappointment could gap below the day-low support area.
  - At nearly $300/share, position sizing can become lumpy for a smaller account unless fractional trading is available/desired.
  - Personal hold-through-earnings and max-risk rules are blank.
- Key levels: support/invalidation proxy near $291.49 day low; resistance/decision area near $302.38 day high and broader 52-week range high around $379.18. Verify on a real chart.
- Main risk: earnings/guidance disappointment and gap risk.
- Pre-mortem: the trade loses because the market wanted stronger margin or QSC contribution, and the stock gaps below the planned invalidation level before execution is possible.
- Risk: Medium-high | Risk/share: planning proxy $8.39 | Suggested size: risk rule not set.
- Sources: eToro AYI, Kiplinger earnings calendar, prior AYI/QSC context. DATE_VERIFIED: NO.

## Notes for the next scheduled run

- Best next improvement: verify catalyst dates from company IR pages, not only the public earnings calendar.
- Non-US coverage needs a better event-calendar source plus eToro instrument verification; otherwise the routine will continue to lean US-heavy.
- Fill `RISK_RULES.md` before relying on any suggested sizing. Right now every sizing-related output correctly says `risk rule not set`.
