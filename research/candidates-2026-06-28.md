# Candidate Shortlist — 2026-06-28
DRAFT for human review. Verify all dates/numbers before trading.
Any size shown is YOUR fixed rule as arithmetic, not a recommendation.

## Summary
- 0 candidates, 0 deep-dived. Overall quality this week is **sparse**: several eToro-tradeable small/mid-cap stocks had acceptable market-cap and liquidity evidence, but I could not verify a specific catalyst date within the next 42 days from a primary or high-quality source during this run. Per the brief, a sparse report is better than padding.
- Final-shortlist rule applied: no name was promoted without `ETORO_TRADEABLE: YES` plus dated catalyst evidence.
- Risk context: RISK_RULES.md sets a fixed €150 total position size per trade during the learning phase; this is not risk-to-stop sizing. Half-size triggers include holding through binary events, low conviction, or gap history larger than stop distance. Max open positions: 5; max same sector/theme exposure: 2; daily loss limit: €150; weekly loss limit: €300.

## Shortlist
No final-main-shortlist candidates qualified this week.

Reason: I could verify public eToro stock/share pages for several preliminary names, but the catalyst-date evidence was either missing, stale, search-result-only, or not primary/high-quality enough to satisfy the brief. Because earnings dates can shift and the brief requires every catalyst to have at least one primary or high-quality source, these were rejected rather than padded into the shortlist.

## Conditional Watchlist
None. No lower-liquidity candidate was promoted because no conditional name had both verified eToro tradeability and catalyst evidence good enough for the separate watchlist.

## Rejected Candidates
- **CROX — Crocs Inc.** — rejected because eToro tradeability was publicly verified, but a specific upcoming dated catalyst within the 42-day window was not verified from a primary or high-quality source in this run. eToro evidence: public page shows “Invest in Crocs Inc,” “Buy CROX,” NASDAQ-delayed USD pricing, market cap about $6.21B, and 3-month average volume of 1.25M shares; at the eToro price of $125.05, approximate ADV is about $156M, above the preferred US floor. Market-cap bucket: core. ETORO_TRADEABLE: YES, but final-candidate catalyst verification: FAIL.
- **ELF — e.l.f. Beauty Inc.** — rejected because eToro tradeability was publicly verified, but the candidate would be an earnings-driven setup and I could not verify a current upcoming company-IR or high-quality dated earnings catalyst during this run. eToro evidence: public page shows “Invest in elf Beauty Inc,” “Buy ELF,” NYSE/NASDAQ-style US stock page with USD pricing, market cap about $3.87B, and 3-month average volume of 3.42M shares; at $67.43, approximate ADV is about $231M. Market-cap bucket: core. ETORO_TRADEABLE: YES, but final-candidate catalyst verification: FAIL.
- **OSCR — Oscar Health Inc.** — rejected because eToro tradeability was publicly verified and liquidity/market cap looked acceptable, but I could not verify a specific current upcoming catalyst date from a primary or high-quality source. eToro evidence: public page shows “Buy OSCR,” USD pricing, market cap about $8.64B, and 3-month average volume of 7.39M shares; at $29.79, approximate ADV is about $220M. Market-cap bucket: core. ETORO_TRADEABLE: YES, but final-candidate catalyst verification: FAIL.
- **SG — Sweetgreen Inc.** — rejected because eToro tradeability was publicly verified and market cap was core, but the setup quality was weak and no acceptable dated catalyst was verified. eToro evidence: public page shows “Buy SG,” USD pricing, market cap about $1.01B, 3-month average volume of 5.14M shares, beta 1.81, and a 52-week range of $4.46-$39.09; at $8.52, approximate ADV is about $44M, above the preferred US floor but with higher volatility risk. ETORO_TRADEABLE: YES, but final-candidate catalyst verification: FAIL.

## Deep Dives (top 0 front-runners)
None. No candidate met the final-main-shortlist bar, so there are no front-runners to deep-dive.

## Notes on Methodology Applied
- Used `RESEARCH_BRIEF.md` as the primary research instruction set: final candidates require the configured universe, liquidity discipline, specific dated catalysts within 42 days, risk rating, risk/share, fixed-size arithmetic, rejected candidates, and deep dives only for selected front-runners.
- Treated `ETORO_TRADEABILITY.md` as the active broker/universe overlay: final candidates must be verified tradeable as eToro stocks/shares for the Germany/EU baseline; market-cap exceptions and liquidity tiers follow that overlay.
- Read `RISK_RULES.md` before interpreting risk/sizing. No blank relevant sizing rule was used; fixed €150 total position size is active. The “rules I know I break” section remains blank, so: risk rule not set.
- Treated `.claude/skills/*` files as methodology references only, adapting the idea-generation, catalyst-calendar, and earnings-preview frameworks rather than treating them as executable skills.

## Compliance Check
- **RESEARCH_BRIEF.md — Read from main branch:** PASS. The file was read before producing the report.
- **ETORO_TRADEABILITY.md — Read and applied as active overlay:** PASS. No final candidate was included without eToro verification.
- **RISK_RULES.md — Read before sizing/risk interpretation:** PASS. Fixed €150 total position size and half-size triggers were considered; “rules I know I break” remains blank, so risk rule not set.
- **Main shortlist only includes eToro-tradeable stocks/shares:** PASS. Main shortlist is empty; no unverified name was promoted.
- **Catalyst dates verified before final inclusion:** PASS. Names without sufficient dated catalyst evidence were rejected.
- **Market-cap evidence:** PARTIAL. eToro public pages provided market-cap evidence for rejected names; no final candidates required market-cap proof.
- **Liquidity evidence:** PARTIAL. eToro public pages provided 3-month average share volume and prices for rejected names; approximate dollar-volume math was derived from those figures. No independent volume source was added.
- **Company-IR catalyst verification:** FAIL. I could not verify current catalyst dates from company IR pages in this run.
- **Europe/Asia candidates considered:** PARTIAL. The overlay permits US, Europe, and Asia, but this run’s verified preliminary examples were US-listed only. I did not promote any US-only list because no final candidates qualified.
- **Larger-cap exception discipline:** PASS. No $10B-$50B exception names were included.
- **Liquidity-tier discipline:** PASS. No conditional lower-liquidity name was moved into the main shortlist.
- **Risk rating/risk-per-share/suggested size for final names:** PASS by absence. No final candidates were included, so no final candidate is missing these fields.
- **Rejected candidates documented with specific reasons:** PASS.
- **Deep dives:** PASS by absence. No front-runners qualified, so no deep dives were produced.

## Source Log
- Project instructions: `RESEARCH_BRIEF.md`, `ETORO_TRADEABILITY.md`, `RISK_RULES.md` on the `main` branch of `Toeffer/TradingJournal`.
- eToro public pages used for tradeability/price/market-cap/volume evidence: CROX, ELF, OSCR, SG.
- Public web-search gap: current primary/high-quality catalyst dates were not sufficiently verified for final inclusion.

## Catalyst Update — added 2026-06-30 (NOT independently verified)

User-supplied catalyst dates for the rejected names, closing the gap that failed each
of them in the original run. **Source: recalled/secondhand, not a primary or
high-quality source.** Verify against company IR or an exchange earnings calendar
before sizing or entering any of these.

- **ELF** — earnings expected 2026-08-05. EPS beat of roughly +$0.69/share speculated (unverified, speculative).
- **CROX** — earnings window 2026-07-31 to 2026-08-07 (date not yet pinned down).
- **OSCR** — earnings expected 2026-08-05.
- **SG** — earnings window 2026-08-06 to 2026-08-10 (date not yet pinned down).

All four are still earnings-driven setups, not yet re-run through Stage 2 deep-dive.
None of this constitutes a final shortlist promotion — that would require re-running
the candidate evaluation with verified dates.
