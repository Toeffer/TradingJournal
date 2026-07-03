# Candidate Shortlist — 2026-07-03
DRAFT for human review. Verify all dates/numbers before trading.
Any size shown is YOUR fixed rule as arithmetic, not a recommendation.

## Summary
- 3 candidates, 3 deep-dived. Quality is **moderate**: three clean, dated, primary-source-verified catalysts — one FDA decision, two reporting events — but all three are **binary events held through**, so every name carries HIGH gap risk. A calmer week would offer more drift/structural setups; this week the best-verified catalysts are event-day catalysts. Nothing was padded.
- Method: **catalyst-first hybrid** with scanner seeds. Parallel agents: **yes** — three research sub-agents ran (EU/XETRA catalysts, US non-earnings/structural catalysts, REPEAT-name earnings dates). They hit a session limit mid-run and returned partial leads only; **every finalist's catalyst date was then re-verified by the main agent against a primary source** (VERA via company IR + FDA priority-review release; RIVN via SEC 8-K; SUSS MicroTec via the company financial calendar). Sub-agent output was treated as leads, not evidence.
- Region mix: preliminary list ~15 names — **8 US** (VERA, RIVN, CROX, ELF, OSCR, SG, HOOD, OWL) / **7 Europe** (SUSS MicroTec, PVA TePla, Nordex, Jenoptik, Rheinmetall, Hensoldt, AIXTRON) / **0 Asia**. `MIN_EU_PRELIMINARY` (4) met. Final shortlist: **2 US / 1 Europe (XETRA) / 0 Asia.**
- Scanner input: **used.** Newest US scan `research/scans/scan-2026-07-02-2236.md` (RIVN score 76–80, HOOD 70, OWL 60, PLTR 64, GIS 59) and newest EU scan `research/scans/scan-eu-2026-07-03-1552.md` (**0 candidates — the EU scan failed with an HTTP 404 data-fetch error and recorded nothing**, so EU discovery ran on web search against primary sources instead). One scanner name (RIVN) was promoted after independent catalyst verification; the rest were rejected (see Rejected).
- Catalyst window: 42 days → through **2026-08-14**. ACT-NOW threshold: within 7 days → through **2026-07-10**.
- Earnings-candidate cap (`MAX_EARNINGS_CANDIDATES: 2`) respected: exactly 2 earnings-primary names (RIVN, SUSS MicroTec). VERA is an FDA decision, not earnings.
- US market note: **2026-07-03 is a US market holiday** (Independence Day observed; July 4 falls on Saturday). US quotes below are the last available NASDAQ/NYSE session prints and may be stale into the long weekend — re-check live before acting.
- Risk rules: `RISK_RULES.md` sets a **fixed €150 learning-phase position size**, half size (€75 or less) when holding through a binary event / low conviction / gap history > stop distance, max 5 open positions, max 2 per sector, R-based circuit breakers (−2R day / −4R week). The routine applies these as context/arithmetic only — it does not change the rule.
- This report **supersedes the earlier same-day test run** that previously occupied this path (that run was all US earnings names and predated the scanner output).

## Shortlist

### 1. VERA — Vera Therapeutics, Inc.
- Source tag: routine.
- eToro: `ETORO_TRADEABLE: YES` | Mode: stock/share | Evidence: public eToro page resolves — https://www.etoro.com/markets/vera . Verify inside the logged-in Germany/EU account before acting.
- Exchange / Currency: NASDAQ / USD. Market-cap bucket: **core universe** (~$2.96B).
- Catalyst: **FDA PDUFA decision on atacicept for IgA nephropathy — target action date 2026-07-07** (accelerated-approval BLA, Priority Review). | DATE_VERIFIED: NO — re-verify against Vera IR before any action, but this run confirmed it from the company's own priority-review press release and multiple medical-news sources.
- Why now: clinical-stage biotech drifting up into a hard, dated regulatory decision 4 days out. Not a momentum chase — the setup is entirely the binary event.
- Bull / Bear: **Bull** — first BAFF/APRIL dual B-cell modulator for IgAN, strong ORIGIN Phase-3 data behind the filing, priority review signals FDA engagement; approval unlocks a mid-2026 commercial launch. **Bear** — a PDUFA is maximally binary; a Complete Response Letter or a restrictive label can gap the stock −30% to −50% overnight, and a stop cannot protect through it.
- Priced-in check: priority review has been known since early 2026 and the stock sits well off its lows (52-wk $19–$56, now ~$41, above both the 50- and 200-day averages). A clean approval may be substantially anticipated; the asymmetric surprise is arguably to the downside (CRL) rather than the upside.
- Invalidation: as a *swing* idea, loss of the ~$36 area (near the 50-day avg and today's low) breaks the pre-event uptrend. As an *event* idea there is no real stop — a CRL gaps through any level.
- Liquidity: ~$206M ADV (≈5.0M shares × ~$41). Well above the $25M floor.
- Non-US notes: USD listing; EUR account carries EUR/USD exposure. Overlap-hours-only rule applies for the US session.
- Risk: **High** — binary FDA event held through (event type), biotech single-asset concentration (float/volatility), large historical swings, and much of the good case possibly priced in. This is a caution gauge from imperfect data, not a precise score. Higher risk = size down or skip, never up.
- Risk/share: planning proxy $41.20 − $36.50 = **$4.70** (event gap risk far exceeds this — do not treat as a real stop through the PDUFA).
- Suggested size: floor(€150 ÷ $41.20) = **3 shares** (learning-phase €150 rule as arithmetic; half size €75 / ~1–2 shares applies for holding through this binary event). FX caveat: €150 is a euro budget spent on a USD share. Not advice.
- Confidence: **Medium** on the setup, **High** on the date. What would raise it: Vera IR confirmation of the July 7 date and a clear pre-mortem on CRL scenarios; an entry plan that does *not* hold through the decision.
- Flags: **ACT-NOW** (catalyst within 7 days). Not a REPEAT.
- Source: Vera IR priority-review release https://ir.veratx.com/news-releases/news-release-details/vera-therapeutics-announces-us-fda-granted-priority-review ; SEC 8-K https://www.sec.gov/Archives/edgar/data/0001831828/000119312526073421/vera-ex99_1.htm ; eToro https://www.etoro.com/markets/vera

### 2. RIVN — Rivian Automotive, Inc.
- Source tag: **routine+scanner_seed.**
- Scanner context: score **76–80** (newest US scan, 2026-07-02); +14.2% day move, rel-volume ~6.4x, broke 20- and 50-day highs. Independent research **confirmed the reason**: Rivian reported Q2 deliveries of 12,194 (vs a 9,000–11,000 outlook) and **raised full-year guidance to 65,000–70,000** on July 2 — a real fundamental beat, not an unexplained move.
- eToro: `ETORO_TRADEABLE: YES` | Mode: stock/share | Evidence: https://www.etoro.com/markets/rivn .
- Exchange / Currency: NASDAQ / USD. Market-cap bucket: **larger-cap exception** (~$23.4B, inside the $10–50B bucket — see exception justification below).
- Catalyst: **Q2 2026 financial results — 2026-07-30, after market close** (announced in the same delivery release). | DATE_VERIFIED: NO — re-verify against Rivian IR/SEC, but this run confirmed it from the SEC 8-K delivery/production release.
- Larger-cap exception justification (required by the eToro overlay): included as the run's **1 exception name** because it is the strongest scanner signal of the week (score 80) *and* carries a confirmed, dated forward catalyst on the back of a confirmed delivery/guidance beat — clearly better-evidenced than the core-universe momentum names the scanner surfaced (OWL, GIS). It remains a genuine swing candidate (discrete event, defined invalidation), not just a large quality company. **Caveat honored:** it is also the most crowded of the three — see priced-in check.
- Why now: post-delivery-beat drift into an earnings confirmation. The stock gapped from ~$17.18 to ~$18.63 on the beat and is holding the gap.
- Bull / Bear: **Bull** — deliveries beat and guidance raised, R2 launch ramping, gap held so far, high liquidity. **Bear** — a +14% one-day spike means much is already in; earnings on July 30 is binary and RIVN has a history of large post-earnings gaps; cash burn / margin scrutiny can dominate a delivery beat; high beta (~2).
- Priced-in check: **strong.** eToro/analyst consensus 12-month price target is ~$18.78 versus a ~$18.6 price — i.e. the Street sees almost no upside from here after the pop. The delivery beat looks largely discounted; the remaining edge is whether July 30 margins/guidance surprise again.
- Invalidation: a fill of the July 2 delivery gap back below ~**$16.80** (loss of the breakout base) says the beat was sold and the drift thesis is wrong.
- Liquidity: very high, ~$400M+ ADV (tens of millions of shares daily). Far above the floor.
- Non-US notes: USD listing; EUR/USD exposure; overlap-hours-only.
- Risk: **High** — larger-cap exception, binary earnings held through July 30 (event type), high beta and gap history (volatility), and a catalyst that is largely priced in (data/priced-in). Caution gauge, not a score. Size down or skip.
- Risk/share: planning proxy $18.63 − $16.80 = **$1.83** (earnings gap risk beyond this).
- Suggested size: floor(€150 ÷ $18.63) = **8 shares** (€150 learning-phase rule; half size €75 / ~4 shares if held through the July 30 report). FX caveat as above. Not advice.
- Confidence: **Medium** — catalyst and reason are well verified; the concern is that the reward-to-risk is thin after the pop. What would raise it: a constructive pullback that holds the gap (better entry), or evidence Q2 margins/FCF will beat, not just deliveries.
- Flags: none (catalyst > 7 days out; not in last week's file).
- Source: SEC 8-K delivery/production release https://www.sec.gov/Archives/edgar/data/0001874178/000187417826000048/ex-9912q26deliveryproducti.htm ; CNBC https://www.cnbc.com/2026/07/02/rivian-raises-2026-delivery-outlook-after-strong-q2-demand.html ; eToro https://www.etoro.com/markets/rivn ; scanner `scan-2026-07-02-2236.md`

### 3. SMHN.DE — SUSS MicroTec SE
- Source tag: routine.
- eToro: `ETORO_TRADEABLE: YES` | Mode: stock/share | Evidence: public eToro page resolves — https://www.etoro.com/markets/smhn.de (eToro ticker `SMHN.DE`).
- Exchange / Currency: **XETRA (Frankfurt) / EUR — no FX drag for the EUR account.** Market-cap bucket: **core universe** (~€1.96B).
- Catalyst: **H1 2026 half-year financial report — 2026-08-06, 07:30 CEST** (company financial calendar). | DATE_VERIFIED: NO — re-verify on the SUSS IR Finanzkalender before acting, but this run took the date from the company's own financial-calendar page (primary source).
- Why now: semiconductor advanced-packaging / photomask equipment maker riding the AI back-end-packaging cycle; the stock is in a strong uptrend (~+10% on the week, ~+159% over the year) heading into an H1 print that will test whether order momentum is still accelerating.
- Bull / Bear: **Bull** — structural exposure to advanced packaging (hybrid bonding, HBM/AI supply chain), record sales trajectory, analyst consensus "Buy." **Bear** — up ~159% in a year and near highs, so a *lot* of good news is priced in; a merely in-line H1 or any order-momentum wobble can gap it down hard; semiconductor-equipment names are cyclical and sentiment-driven.
- Priced-in check: **elevated.** After a ~159% run the market already expects strong H1 growth; the bar for a positive surprise is high and the asymmetric risk is a "good-but-not-good-enough" sell-off.
- Invalidation: loss of the recent breakout base (planning proxy ~**€94**) breaks the uptrend structure ahead of the report.
- Liquidity: SDAX/TecDAX semiconductor name, comfortably above the €5M-equivalent non-US floor (typical daily value tens of € millions). Verify live.
- Non-US notes: **EUR-denominated, no FX** for the EUR account; XETRA hours 09:00–17:30 CEST (fully inside the user's local session — overlap-hours rule easily satisfied); standard T+2 settlement; watch German market holidays.
- Risk: **Medium-High** — binary H1 report held through (event type), extended/priced-in after a large run (setup), cyclical semi-cap volatility. Lower than VERA/RIVN on liquidity/FX (EUR, no FX) but the crowding/priced-in risk is real. Caution gauge, not a score.
- Risk/share: planning proxy €103 − €94 = **€9** (report gap risk beyond this).
- Suggested size: floor(€150 ÷ €103) = **1 share** (€150 learning-phase rule; half size €75 → the €150 rule already buys ≤1 share here, so this is effectively a single-share/skip decision — a known limitation of a fixed-€ rule on a €100+ share). Not advice.
- Confidence: **Medium** — date is primary-sourced and the theme is real; the worry is that the setup is extended into the print. What would raise it: a pullback into support (€94–98) that improves reward-to-risk, or channel-check evidence of continued order acceleration.
- Flags: none (catalyst > 7 days; not in last week's file).
- Source: SUSS financial calendar https://www.suss.com/en/investor-relations/financial-calendar (H1 report 2026-08-06) ; EQS advance-report notice (WpHG Art. 114/115/117) https://www.eqs-news.com/news/financial-reports/suss-microtec-se-preliminary-announcement-of-the-publication-of-financial-reports-according-to-articles-114-115-117-of-the-wphg-the-german-securities-act/146da27e-b394-4951-9804-0e067f93f006_en ; eToro https://www.etoro.com/markets/smhn.de

## Rejected Candidates
- **CROX — Crocs Inc.** — rejected on the earnings-candidate cap. Its Q2 report (~2026-08-06, aggregator-estimated, not IR-confirmed) would be a **third earnings-primary name**, violating `MAX_EARNINGS_CANDIDATES: 2`. eToro-tradeable, core cap (~$6.2B), liquid (~$150M ADV). Revisit if RIVN or SUSS is dropped. (REPEAT — was on last week's 06-28 rejected list.) Source: eToro/MarketBeat CROX earnings.
- **OSCR — Oscar Health** — rejected: no company-IR-confirmed Q2 date found this run (Q1 was reported 2026-05-06; Q2 date only estimated), and the stock is printing a fresh 52-week high (~$32.2 vs $33.1 high) into an unconfirmed earnings event — priced-in / chase risk too high without a verified date. (REPEAT from 06-28.) Source: SEC 8-K Q1 https://www.sec.gov/Archives/edgar/data/0001568651/000156865126000036/oscarhealthfirstquarter202.htm
- **ELF — e.l.f. Beauty** — rejected: earnings-primary (would exceed the cap) and the report date (~2026-08-05) was not IR-confirmed this run; stock is volatile (52-wk $48–$151). (REPEAT from 06-28.) Source: prior candidates file note.
- **HOOD — Robinhood** — rejected: scanner score 70, but market cap ~**$101B** is a mega-cap excluded by default; no eligible-universe fit. Source: scanner `scan-2026-07-02-2236.md`; FMP quote.
- **OWL — Blue Owl Capital** — rejected: scanner score 60 but the only reason is "it moved" — no dated catalyst inside the window was found; larger-cap (~$14.1B) asset manager, momentum-only. Source: scanner `scan-2026-07-02-2236.md`.
- **PLTR — Palantir** — rejected: scanner score 64 but ~$314B mega-cap and a crowded headline AI name — excluded by CONFIG/overlay. Source: scanner `scan-2026-07-02-2236.md`.
- **EU scanner names** — none: the newest EU scan (`scan-eu-2026-07-03-1552.md`) recorded **0 candidates** because the data fetch failed with an HTTP 404, so there were no EU scanner seeds to evaluate. EU candidates this week came from web/primary-source discovery, not the scanner.

## Deep Dives (top 3 front-runners)

### VERA — Vera Therapeutics, Inc.
- Source tag / scanner context: routine; not scanner-seeded.
- Catalyst mechanics & what's priced in: FDA PDUFA target action date **2026-07-07** on the atacicept BLA (accelerated approval, priority review) for IgA nephropathy. Three outcomes: approval (base case, partly anticipated after priority review), CRL/deficiency (sharp downside gap), or approval with a restrictive label (mixed). Because priority review has been public since early 2026 and the stock is well off its lows, an approval may be largely in the price — the fatter tail is a negative surprise. A follow-on ORIGIN eGFR readout is slated for Q3 2026 with an sBLA in Q4, so this is the first of several 2026 events, not the last word.
- Bull: (1) dual BAFF/APRIL mechanism is differentiated in IgAN; (2) ORIGIN Phase-3 data underpins the filing; (3) priority review implies FDA engagement; (4) approval enables a mid-2026 launch and a re-rating on commercial optionality.
- Bear (incl. gap risk): (1) a CRL can gap the stock −30% to −50% and no stop protects through it; (2) single-asset biotech — this decision is most of the equity story; (3) even on approval, label/reimbursement disappointment can sell the news; (4) the run into the event raises the "priced-for-approval" risk.
- Key levels (support / resistance / invalidation): support ~$36–37 (50-day avg / today's low); resistance ~$45–47 then the 52-wk high ~$56; swing invalidation loss of ~$36. Event invalidation = the outcome itself, not a level.
- Main risk: holding a single-asset biotech *through* a binary FDA decision — the one setup where a stop is an illusion.
- Pre-mortem: a month from now this lost money because the position was **held through July 7**, the FDA issued a CRL or a narrow label, and the stock gapped below any planned stop. What I'd have ignored: that priority-review approval was already largely priced in, so the risk/reward through the event was skewed against me. The disciplined version trades *around* the event (or sits it out), it doesn't hold through it.
- Risk: High | Risk/share: $4.70 planning proxy | Suggested size: 3 shares (€150 rule; half size for the binary hold). DATE_VERIFIED: NO.
- Sources: Vera IR priority-review release; SEC 8-K; eToro VERA page (URLs above).

### RIVN — Rivian Automotive, Inc.
- Source tag / scanner context: routine+scanner_seed; score 76–80, +14.2% on 2026-07-02, reason **confirmed** = Q2 delivery beat (12,194 vs 9,000–11,000) and FY guidance raise to 65,000–70,000.
- Catalyst mechanics & what's priced in: **Q2 2026 financial results, 2026-07-30 after close.** Deliveries and guidance are already known and largely discounted (analyst consensus 12-mo target ~$18.78 ≈ spot). The unresolved variable is profitability — gross margin trajectory, R2 ramp costs, and cash burn. A margin/FCF beat could extend the move; an in-line delivery story with soft margins likely sells off.
- Bull: (1) delivery beat + guidance raise is a real fundamental improvement; (2) R2 launch broadens the demand base; (3) the July 2 gap has held, showing the beat wasn't immediately faded; (4) deep liquidity makes it easy to trade around the event.
- Bear (incl. gap risk): (1) a +14% spike means the good news is largely in — thin remaining reward-to-risk; (2) July 30 earnings is binary and RIVN has a history of large post-earnings gaps; (3) margins/cash burn can dominate a delivery beat and gap it down; (4) high beta (~2) and EV-sentiment sensitivity amplify both directions.
- Key levels (support / resistance / invalidation): support = the July 2 gap base ~$17.0–17.2; resistance ~$19.8 (day high) then the 52-wk high ~$22.7; invalidation = a gap fill below **~$16.80**.
- Main risk: chasing a name that already moved +14% into a binary earnings print where the Street sees ~0% upside to its 12-month target.
- Pre-mortem: a month out this lost money because I bought the post-delivery pop, RIVN drifted or slipped into July 30, then reported thin margins / heavier cash burn and gapped down through the gap base. What I'd have ignored: the consensus price target already sitting *at* the price — the market had already paid for the good news.
- Risk: High | Risk/share: $1.83 planning proxy | Suggested size: 8 shares (€150 rule; half size if held through July 30). DATE_VERIFIED: NO.
- Sources: SEC 8-K delivery release; CNBC; eToro RIVN page; scanner file (URLs above).

### SMHN.DE — SUSS MicroTec SE
- Source tag / scanner context: routine; not scanner-seeded (EU scan returned 0 due to a 404).
- Catalyst mechanics & what's priced in: **H1 2026 half-year report, 2026-08-06 07:30 CEST.** After a ~159% one-year run, the market expects continued strong advanced-packaging order momentum. The report will be judged on order intake / book-to-bill and margin guidance more than the headline H1 number. Consensus is "Buy," so positioning is likely already long — the surprise risk is skewed toward disappointment.
- Bull: (1) structural exposure to AI back-end packaging (hybrid bonding, HBM) and photomask; (2) record sales trajectory and a multi-quarter order tailwind; (3) analyst consensus supportive; (4) EUR listing removes FX drag and the session sits fully inside the user's local hours.
- Bear (incl. gap risk): (1) extremely extended (+159% YoY, near highs) — a lot is priced in; (2) an in-line or softening order print can gap a crowded winner down sharply; (3) semiconductor-equipment demand is cyclical and lumpy; (4) a single quarter's book-to-bill can swing sentiment hard.
- Key levels (support / resistance / invalidation): support/breakout base ~€94–98; resistance = recent highs ~€105–110; invalidation = loss of ~**€94**.
- Main risk: buying an extended, crowded semi-cap winner *into* an H1 report where expectations are already high.
- Pre-mortem: a month out this lost money because I bought near the highs, H1 order intake merely met (not beat) elevated expectations, and the stock gapped back to its breakout base. What I'd have ignored: that +159% already embedded the "orders keep accelerating" thesis, leaving no cushion for merely-good results. The fixed-€150 rule also buys only ~1 share here — the position is too small to matter unless sized differently, which is a rule decision for the human, not the model.
- Risk: Medium-High | Risk/share: €9 planning proxy | Suggested size: 1 share (€150 rule; EUR, no FX). DATE_VERIFIED: NO.
- Sources: SUSS financial calendar; EQS advance-report notice; eToro SMHN.DE page (URLs above).

## Compliance Check
| Requirement | Status | Notes |
|---|---|---|
| Read `RESEARCH_BRIEF.md` / `ETORO_TRADEABILITY.md` / `RISK_RULES.md` | PASS | Config, broker overlay, and risk rules applied. |
| eToro tradeability for all final candidates | PASS | VERA, RIVN, SMHN.DE public eToro pages all resolve; in-account check still advised. |
| Market-cap buckets | PASS | VERA (~$2.96B) and SUSS (~€1.96B) core; RIVN (~$23.4B) is the run's 1 larger-cap exception, justified in-line. |
| Liquidity floors | PASS | All above their floors ($25M US / $5M-equiv EU). |
| Catalyst window (≤42d, ≤2026-08-14) | PASS | Jul 7, Jul 30, Aug 6. |
| Max earnings candidates (2) | PASS | RIVN + SUSS = 2; VERA is FDA. |
| `MIN_EU_PRELIMINARY` (4) | PASS | 7 EU names in the preliminary list; 1 EU in the final shortlist. |
| Scanner input used | PASS | US scan seeds evaluated (RIVN promoted, HOOD/OWL/PLTR rejected); EU scan returned 0 (404) — stated. |
| Primary-source catalyst verification | PASS (with re-verify note) | VERA (IR + SEC), RIVN (SEC 8-K), SUSS (company calendar). All flagged DATE_VERIFIED: NO for human re-check. |
| Risk rating + risk/share + size for all finalists | PASS | Present for all three. |
| Deep dives for top `NUM_DEEP_DIVES` (3) | PASS | All 3 deep-dived. |
| Rejected candidates included | PASS | 6 named with specific reasons. |
| No padding / honest counts | PASS | 3 verified names; nothing stretched to hit 5. |
| No financial advice | PASS | Draft, process/risk language only. |

## Notes for the next scheduled run
- **All three catalysts are binary events held through** — a thin week for drift/structural setups. If the human's rule is not to hold through binaries at full size, the practical read is: trade *around* these events or sit them out. The deep-dive pre-mortems all point to the same failure mode (holding through the gap).
- **Fix the EU scanner 404** — the EU scan (`scan-eu-2026-07-03`) recorded 0 candidates on a data-fetch error, forcing EU discovery onto manual web search. A working EU scan would surface XETRA seeds directly.
- **German H1 reporting season (late July–mid August)** is a rich vein of dated, primary-sourced catalysts (Finanzkalender pages are binding) — worth a dedicated EU catalyst-calendar pass next run (PVA TePla, Nordex, Jenoptik, and others were leads this week but not verified in time after the research agents hit a session limit).
- **Fixed-€150 sizing breaks down on €100+ shares** (SUSS buys ~1 share). Flagged for the human; the routine cannot change the rule.
