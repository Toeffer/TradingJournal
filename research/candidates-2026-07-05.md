# Candidate Shortlist — 2026-07-05
DRAFT for human review. Verify all dates/numbers before trading.
Any size shown is YOUR fixed rule as arithmetic, not a recommendation.

## Summary
- 2 candidates, 2 deep-dived. Honest read: **every primary-verifiable catalyst in the 42-day window this week is an earnings report** (German H1 season concentrated on 30 Jul; US Q2 season early Aug). No structural/non-binary catalyst (index inclusion, lockup, spin-off, regulatory decision) with a confirmed in-window date turned up — the next S&P index rebalance is September (out of window) and the thyssenkrupp TKMS spin-off already listed in Oct 2025. So the `MAX_EARNINGS_CANDIDATES: 2` cap binds hard and the shortlist is deliberately short rather than padded. A sparse report beats a stretched one.
- Method: **hybrid (scanner-seed + screener → catalyst-first verification)**. Pulled real FMP quotes for the scanner seeds and a ~24-name XETRA mid-cap set to screen market-cap/liquidity, then verified each surviving catalyst against IR / EQS-WpHG financial calendars via web search. Parallel agents: no — single main agent, all catalyst dates re-verified in-line (subagent findings were not used as evidence).
- Region mix: preliminary list ≈ **8 US / 7 Europe / 1 Asia** (US: PENG, LEVI, CELH, HIMS, RIVN, HOOD, SMMT, S; EU/XETRA: AIXA, WAF, KGX, JEN, SZG, TKA, AFX; Asia: GRAB). Europe is comfortably above `MIN_EU_PRELIMINARY: 4` this week — a deliberate fix of the last run's US-only preliminary list. Final shortlist: **1 EU (KGX) / 1 US (CELH)**.
- Scanner input: **used.** Newest US signals in `data/scanner_signals.csv` + `research/scanner-summary.md` (generated 2026-07-05 18:47 UTC); newest EU scan `research/scans/scan-eu-2026-07-04-1236.md` produced **0 alerts** (Twelve Data/Stooq feeds failed; Yahoo fallback found nothing ≥60). Considered scanner names RIVN(80), HOOD(70), PLTR(64), CELH(60), SMMT(60), OWL(60), GIS(59), HIMS(56). Only **CELH** advanced — it was the one scanner breakout that also fit the universe and had a real forward dated catalyst.
- Risk-rule context (`RISK_RULES.md`): fixed **€150** position per trade (learning phase, arithmetic only — the routine cannot change it); **half size (€75 or less) when holding through a binary event** such as earnings; max 5 open positions; max 2 per sector/theme; no FX hedging on small learning-phase trades; overlap-hours-only for non-US entries.
- ⚠️ Note on the previous file at this path: the earlier 2026-07-05 draft's top picks were PENG and LEVI on recalled Kiplinger dates. This run supersedes them — PENG **gapped −10.7% on Fri 3 Jul into its supposed print** (falling knife) and neither PENG nor LEVI's earnings date could be re-confirmed from a primary source, so both moved to Rejected.

## Shortlist

### 1. KGX.DE — Kion Group AG (warehouse automation & industrial trucks)
- Source tag: **routine** (not scanner-seeded).
- eToro: `ETORO_TRADEABLE: YES` | Mode: stock/share | Evidence: live eToro market page https://www.etoro.com/markets/kgx.de (XETRA, EUR).
- Ticker on eToro: KGX.DE | Exchange / Currency: **XETRA / EUR** (no FX for the EUR account) | Market-cap bucket: **core** (~€5.7B) | Local listing (not ADR).
- Non-US notes: EUR-denominated → no FX drag; XETRA hours 09:00–17:30 Berlin; no UK stamp duty (not LSE).
- Catalyst: **H1/Q2 2026 results on 2026-07-30** (25 days out). | DATE_VERIFIED: NO
- Why now: beaten down from a ~€70 52-wk high to a €35.80 low; now basing and **+4.65% on Fri 3 Jul, reclaiming the 50-day MA (~€42.5)** into the print. Low-expectations turnaround setup, not a chase of a high.
- Bull / Bear: **Bull** — analyst consensus Moderate/Strong Buy, targets ~€56–59 (well above ~€43 spot); reclaimed 50-day on volume; depressed valuation = low bar; European automation/supply-chain capex theme. **Bear** — binary H1 can gap through the stop; order intake / tariff & China-industrial softness could disappoint; still **below the 200-day (~€54)** so the downtrend isn't confirmed broken; auto/industrial end-markets soft.
- Priced-in check: the +4.65% pre-print pop and an already-"Buy" consensus mean a merely in-line H1 may not move it; the easy re-rating off the lows may be partly done.
- Invalidation: close below **~€41.50** (under Fri's €41.88 low) / loss of the 50-day MA.
- Liquidity: ~**€25–28M** ADV (Fri volume 641k × ~€43); comfortably above the €5M non-US floor.
- Risk: **Medium-High** — binary earnings held-through and still sub-200-day push it higher; good liquidity, a clean invalidation level, and much lower crowding than the semis pull it lower.
- Risk/share: €43.41 − €41.50 = **€1.91**. | Suggested size: floor(€150 ÷ €43.41) = **3 shares**; half-size if holding through the print: floor(€75 ÷ €43.41) = **1 share**.
- Confidence: **Medium** — date comes from Kion's legally-mandated WpHG advance financial-report disclosure (strong source); would rise with the company IR calendar page + a clean chart entry above the 50-day.
- Flags: none (25 days out, so not ACT-NOW; not a REPEAT — last week's shortlist was empty).
- Source: eToro KGX.DE page; Kion EQS/WpHG advance-disclosure (publication 2026-07-30), reported 2026-06-30; FMP quote (Fri close €43.41).

### 2. CELH — Celsius Holdings, Inc. (energy/fitness beverages)
- Source tag: **routine+scanner_seed.**
- Scanner context: score **60** (2026-07-03, `alpaca`), also score 40 on 07-01; reason = **+4.13% day, breaking above the 20-day high on ~3.9× relative volume**. Independent research **confirmed a real forward catalyst** (Q2 earnings) — so this is not merely "it moved."
- eToro: `ETORO_TRADEABLE: YES` | Mode: stock/share | Evidence: live eToro market page https://www.etoro.com/markets/celh (NASDAQ, USD).
- Ticker on eToro: CELH | Exchange / Currency: **NASDAQ / USD** | Market-cap bucket: **core** (~$8.5B) | Local US listing (not ADR).
- Non-US notes: EUR account carries EUR/USD exposure; no FX hedging in the learning phase; overlap-hours-only for entries.
- Catalyst: **Q2 2026 earnings ~2026-08-11** after close (some trackers say ~Aug 6; not yet company-confirmed). | DATE_VERIFIED: NO
- Why now: recovering off the $27.47 low; the scanner flagged a **20-day-high breakout on 3.9× rel-volume**, reclaiming the 50-day (~$30.7) into Q2. Momentum turn ahead of the print.
- Bull / Bear: **Bull** — analyst consensus Strong Buy, target ~$60 (large upside vs ~$33 spot); scanner breakout on real volume; **Alani Nu** acquisition adds scale/growth; expectations reset low after the 66→27 drawdown. **Bear** — CELH has a history of ±15–20% earnings gaps; energy-drink category decelerating + Monster/Red Bull competition; still far **below the 200-day (~$43.7)** = primary downtrend intact; Alani Nu integration/margin risk.
- Priced-in check: the bounce + Strong-Buy consensus + $60 targets mean optimism is already back; an in-line quarter could sell the news.
- Invalidation: close below **~$31.90** (under Fri's $32.21 low, near the 50-day).
- Liquidity: ~**$300M+** ADV (very liquid); well above the $25M US floor.
- Risk: **High** — binary earnings, high beta, large historical gaps, and price still in a primary downtrend below the 200-day.
- Risk/share: $33.16 − $31.90 = **$1.26**. | Suggested size: floor(€150 ÷ $33.16) = **4 shares** (€150 notional; apply EUR/USD at execution); half-size through the print: floor(€75 ÷ $33.16) = **2 shares**.
- Confidence: **Medium-low** — scanner + analyst context is strong, but the exact earnings date is not company-confirmed and this is a high-gap name.
- Flags: none (Aug 11 is >7 days out; not a REPEAT).
- Source: `data/scanner_signals.csv` (CELH 07-03, score 60); eToro CELH page; WallStreetZen/TipRanks earnings-date trackers (~Aug 11); FMP quote (Fri close $33.16).

## Conditional Watchlist — the semiconductor cluster (NOT promoted)
Both are eToro-tradeable XETRA core-bucket names with **confirmed H1/Q2 results on 2026-07-30**, and the strongest raw momentum on the tape (semi-wafer/AI theme). They are **excluded from the main shortlist on purpose**: adding either would break the `MAX_EARNINGS_CANDIDATES: 2` cap, and holding both would be two positions in one sector (semiconductors) gapping on the *same day* — exactly the concentration `RISK_RULES.md` limits to 2/sector. If trading the theme, pick **at most one**. eToro tradeability for these two is expected-YES (XETRA names) but was **not individually logged-in-verified** this run — check before acting.

- **AIXA.DE — Aixtron SE** (MOCVD semiconductor deposition equipment). H1 results **2026-07-30**. ~€49.3, **+6.0% Fri**, ~€5.6B core. Caution: **very extended** (price ~1.6× the 200-day ~€30; up from an €11.7 low) and **Q1 revenue was −47% YoY** — a lot of AI-photonics optimism is already in. Risk **High**. Risk/share proxy €49.28 − €47.20 = **€2.08**; size floor(€150 ÷ €49.28) = **3** (half-size 1). DATE_VERIFIED: NO. Source: aixtron.com IR calendar / MarketScreener; FMP quote.
- **WAF.DE — Siltronic AG** (hyperpure silicon wafers; supplies TSMC/Samsung). Q2 results **2026-07-30**. ~€92.5, **+9.6% Fri** (fresh breakout), ~€2.8B core. Caution: **thinner liquidity ~€11M ADV** (spread/slippage risk), a **history of violent gaps** (+23.7% in May 2026 *on a guidance cut* — gappy and a weak fundamental backdrop), so a wide **~€7.50 risk/share** and floor(€150 ÷ €92.5) = **1 share** (can't meaningfully half-size). Risk **High**. DATE_VERIFIED: NO. Source: siltronic.com financial calendar; FMP quote.

## Rejected Candidates
- **PENG — Penguin Solutions** — was last file's #1. **Gapped −10.7% on Fri 3 Jul** into its supposed ~7 Jul print (falling knife); exact earnings date could not be re-confirmed from FMP/primary this run. Binary gap risk too high, momentum against. Reject.
- **LEVI — Levi Strauss** — was last file's #2. Near its 52-wk high (likely priced-in) and the ~8 Jul date could not be confirmed from a primary source this run; superseded by cleaner, more-diversified names. Reject.
- **RIVN — Rivian** (scanner 80) — the +14%/+8.5% moves were the *reaction to an already-reported* Q2 delivery beat/raise — past news, not a forward dated catalyst. Also ~$23.4B = larger-cap exception bucket and already extended. Reject (scanner move had its reason, but it's behind us).
- **HOOD — Robinhood** (scanner 70) — **~$101B mega-cap**, excluded by the overlay; move tied to already-announced EU-expansion news. Reject.
- **SMMT — Summit Therapeutics** (scanner 60) — ~$12B larger-cap-exception biotech; the ivonescimab catalyst is a **binary data/regulatory event with no confirmable in-window date** this run. Too binary, thin verification. Reject.
- **HIMS — Hims & Hers** (scanner 56) — a *real* verified setup (~10 Aug Q2 earnings; Q2 rev guided $680–700M) but **rejected from the main shortlist to stay under the 2-earnings cap**, and it's a higher-hype, higher-gap telehealth/GLP-1 name than CELH. Held as the earnings alternate if CELH invalidates.
- **JEN.DE / SZG.DE / TKA.DE / AFX.DE** — eToro-tradeable XETRA core movers (+3.9%/+6.0%/+5.8%/+3.8% Fri) but their H1 dates weren't individually re-confirmed from a primary calendar this run, and none showed a cleaner reward-to-risk than KGX. Carried as EU watch names, not shortlisted.

## Deep Dives (top 2 front-runners)

### KGX.DE — Kion Group AG
- Source tag / scanner context: routine; not scanner-seeded.
- Catalyst mechanics & what's priced in: H1/Q2 2026 results on **2026-07-30** (date from Kion's WpHG advance disclosure). The market is watching **order intake and the Industrial Trucks & Services vs. Supply Chain Solutions (Dematic) split**, margin trajectory, and any full-year-guidance change. What's priced in: consensus is already **Moderate/Strong Buy with ~€56–59 targets** and the stock popped +4.65% *before* the print, so a decent H1 is partly anticipated — the edge is in a guide raise or order-intake inflection, not an in-line number.
- Bull: (1) Deeply beaten down (~€70 → €35.8 low) with a low expectations bar; (2) Reclaimed the 50-day MA on above-average volume Fri; (3) Analyst targets imply ~30–40% upside from spot; (4) Structural read-through to warehouse-automation/re-shoring capex.
- Bear (incl. gap risk): (1) A binary print can gap straight through the €41.5 invalidation before any stop fills; (2) Cyclical forklift/automation demand is tariff- and China-sensitive; (3) Still under the 200-day (~€54) — this is a counter-trend bounce until proven otherwise; (4) A guidance *cut* would re-open the downtrend toward the lows.
- Key levels: support ~€41.5 (Fri low / near 50-day); resistance ~€47–48, then the 200-day ~€54; invalidation **€41.5** close.
- Main risk: buying a counter-trend bounce into a binary event where the primary trend is still down.
- Pre-mortem: a month out this is red because I held through the 30 Jul print, order intake came in soft or guidance was merely maintained, the stock round-tripped the +4.65% pop, and I ignored that price was **still below the 200-day** — i.e. I treated a bounce as a trend change.
- Risk: Medium-High | Risk/share: €1.91 | Suggested size: 3 shares (€150 rule) / 1 share half-size through earnings.
- Sources: eToro KGX.DE; Kion WpHG advance disclosure (H1 publication 2026-07-30); FMP quote. DATE_VERIFIED: NO.

### CELH — Celsius Holdings, Inc.
- Source tag / scanner context: routine+scanner_seed — scanner score 60 (2026-07-03), 20-day-high breakout on ~3.9× rel-volume.
- Catalyst mechanics & what's priced in: Q2 2026 earnings **~2026-08-11** (not yet company-confirmed). The market is focused on **North-America energy-drink volume/share, the Alani Nu contribution and integration margins, and international expansion**. What's priced in: after the bounce off $27, consensus is **Strong Buy with a ~$60 target** — a lot of recovery optimism is back, so an in-line quarter or soft category commentary could sell the news.
- Bull: (1) Scanner breakout confirmed on real relative volume; (2) Alani Nu adds scale and a second growth engine; (3) Expectations reset low after the 66→27 drawdown; (4) Strong-Buy consensus with ~80% implied upside to target.
- Bear (incl. gap risk): (1) CELH routinely gaps ±15–20% on earnings — the $31.90 stop is not gap-proof; (2) Energy-drink category growth is decelerating and Monster/Red Bull compete hard; (3) Price is still far below the 200-day (~$43.7) — primary downtrend; (4) Alani Nu integration and promotional intensity could pressure margins.
- Key levels: support ~$31.9 (Fri low / 50-day); resistance ~$33.8 (Fri high) then the 200-day ~$43.7; invalidation **$31.9** close.
- Main risk: holding a high-beta, big-gap consumer name through a binary print while the primary trend is still down.
- Pre-mortem: a month out this loses because I held through an ~$Aug-11 report that beat but guided cautiously on category growth/margins, CELH gapped −15% below $31.90 overnight, and I had ignored that a Strong-Buy/$60-target crowd had already priced the recovery.
- Risk: High | Risk/share: $1.26 | Suggested size: 4 shares (€150 rule) / 2 shares half-size through earnings.
- Sources: `data/scanner_signals.csv` (CELH, 07-03, score 60); eToro CELH; WallStreetZen/TipRanks earnings trackers; FMP quote. DATE_VERIFIED: NO.

## Compliance / method notes
- Read `RESEARCH_BRIEF.md`, `ETORO_TRADEABILITY.md`, `RISK_RULES.md` before building the list. Applied the 42-day window, `MIN_EU_PRELIMINARY: 4` (met: 7 EU preliminary), `MAX_EARNINGS_CANDIDATES: 2` (met: exactly 2, both diversified by sector+region), eToro overlay (both finalists verified on live eToro market pages), core/exception market-cap buckets, and preferred/conditional liquidity tiers.
- Prices/market-caps/liquidity are **real FMP quotes as of Fri 2026-07-04 close** (markets closed today, Sun 2026-07-05). Entry/stop are planning proxies off that close — **chart-verify before acting**.
- Every catalyst carries **DATE_VERIFIED: NO** per the brief; earnings dates still need a final company-IR confirmation. Kion's date is the strongest (WpHG legal disclosure); the two US dates are high-quality-tracker estimates, not company-confirmed.
- Honest counts, no padding: only 2 names cleared the bar this week because the window is earnings-only and the earnings cap binds. The semis are the strongest momentum but are held on the watchlist by rule, not shortlisted.
- Not financial advice. This is a draft to research and verify — the size shown is your own €150 fixed rule as arithmetic, and the size/entry decisions are yours.
