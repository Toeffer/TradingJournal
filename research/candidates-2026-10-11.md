# Weekly Research and Decision Review — 2026-10-11

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: Claude Opus 5 (Claude Code cloud session) / continuity-first, catalyst-first discovery
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `f08ca585cd4f22f9f5c2194e03bde3122eb914d4af2dc9b5979669da3fa354b8`
- Snapshot generated: 2026-10-11 21:38 UTC via `python scripts/build_research_snapshot.py --archive`; **2 rows** (`MRVL`, `RXRX`), archived as `research/snapshots/research_snapshot-2026-10-11.csv`
- Repository commit: `b9e6798`
- Prior reports reviewed: `research/candidates-2026-09-20.md`, `-09-13`, `-09-06`, `-08-30`, `-08-23`, `-08-16` and matching manifests
- **Reporting gap:** no research run exists for 2026-09-27 or 2026-10-04. This is the first run in three weeks; the 2026-10-05 digest already flagged research as 15 days old.
- Active recommendations reviewed: **0** (all three registry objects are terminal: `REC-CELC-2026-0004` archived, `REC-FTK-2026-0906` invalidated, `REC-LW-2026-0913` expired)
- Open positions reviewed: **0** (`trades.csv` has no open rows; 18 closed)
- Preliminary pool: 12 leads — 5 Europe/XETRA, 7 US (2 of them scanner rows)
- Final classifications: 0 `ACTIONABLE` / 0 `EARLY_WATCH` / 12 `REJECT`
- Primary sources opened by the synthesizing pass: **0** — see *Evidence-gate failure* below
- Weekly decision: **NO NEW TRADE**

## Evidence-gate failure (read this first)

This run could not satisfy the repository's own verification gate, and the reason is
infrastructure, not an absence of candidates. Recording it plainly so the next run does not
repeat the search:

1. **Primary sources are unreachable.** Outbound egress in this session is allow-listed.
   `www.sec.gov`, `investors.lambweston.com`, `www.sap.com`, `stooq.com`,
   `query1.finance.yahoo.com`, `data.alpaca.markets`, `financialmodelingprep.com`,
   `www.boerse-frankfurt.de` and `api.nasdaq.com` were all refused at the proxy
   (`connect_rejected`, organization policy) or failed DNS resolution for the fetch tool.
   `research_method/verification.md` requires the synthesizing pass to *open* the primary
   source itself. It could not open a single one. Every date below is therefore
   `secondary_only` at best, and `secondary_only` is `REJECT` by rule.
2. **No structured market data for the universe.** The FMP connector is on a tier that
   denies `quote`, `search` (screener), `news` and `technicalIndicators` outright, and
   restricts `chart`/`earnings-company` to a handful of mega-cap symbols (AAPL works, AYI
   and RXRX are refused). What does work: `earnings-calendar` (mega-caps only),
   `secFilings` (EDGAR metadata), `marketPerformance` and `splits-calendar`. The Quartr
   connector returns `subscription_required` (`currentPlan: none`) for every tool.
   Consequence: no price, no market cap, no average dollar volume and **no OHLCV history**
   for any core-universe name — so eToro/market-cap/liquidity gates cannot be evidenced and
   no 20-day high, swing low or ATR exists from which to derive a non-arbitrary trigger,
   stop and target.
3. **The canonical snapshot is effectively empty.** Two rows in the seven-day lookback, and
   neither is usable: `MRVL` is a mega-cap (excluded by default) and `RXRX` shows
   $5.36M average dollar volume, below even the $10–25M conditional tier for US names, on a
   day it had already run +15.98%. The scanner recorded 0 signals in the week to 2026-10-05
   and only 2 since 2026-09-04.

Under these conditions the honest output is a lead inventory plus `NO NEW TRADE`. Inventing
levels from a search snippet would be exactly the failure `SETUPS.md` and
`research_method/analysis.md` prohibit. **This is now the fourth consecutive run without a
single Actionable name, and the blocker has shifted from "no setup" to "no evidence
channel" — that is a tooling decision for the human, not a research finding.**

## Prior recommendation audit

| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|
| CELC | 2026-08-09 | remove | trade closed 2026-07-09 at 108.00 (+4.04R) | n/a | `archived` (unchanged) | no review needed — terminal |
| FTK.DE | 2026-09-06 at €37.74 | remove | €30.18 at last review, about -20% | no trigger ever existed | `invalidated` (unchanged) | no review needed — terminal |
| LW | 2026-09-13 at $47.37 | remove | $42.01 at last review, about -11% | no trigger ever existed | `expired` (unchanged) | no review needed — terminal |

The active book is empty, so no recommendation review rows are appended this week and
`research/decisions/decisions-2026-10-11.csv` is correctly a zero-row archive. Nothing was
dropped silently: all three objects reached a terminal status in an earlier append-only
review row and remain in the registry for outcome analysis.

One carry-over outcome worth recording, since both objects left the book just before their
events: **Lamb Weston reported fiscal Q1 2027 on 2026-10-06 as scheduled** — net sales
about $1.67B (+1%), adjusted EPS $0.75, adjusted EBITDA $286M (-5%), and raised FY2027
Adjusted EBITDA guidance to $1.125–1.215B. The `expired` decision of 2026-09-20 was a
decision not to anticipate a binary event without a setup; it was not a view that the print
would be bad. Do not re-read it as a missed trade. (Source: web-search summary of the
company's 8-K exhibit and press coverage; the filing itself could not be opened here.)

## Existing positions

None. `trades.csv` contains no open rows, so there is no `manage` recommendation this week.

## Coming-week decision sheet

No candidate has a complete trigger-ready setup, and none has verified primary-source
evidence. **NO NEW TRADE.**

Nothing is promoted to `data/proposals.csv`.

## New research

All twelve leads are recorded as discovery objects and rejected before they enter the
registry. Dates are third-party/aggregator-sourced leads, **not verified**, and are flagged
for human verification per `CLAUDE.md`.

### Europe / XETRA

| Ticker | Company | Lead event | Lead date | Days | Rejected because |
|---|---|---|---|---|---|
| DB1.DE | Deutsche Börse AG | Q3 2026 results | 2026-10-20 | 9 | Market cap far above the €/$50B default exclusion; no larger-cap exception justified; also a carry-over reject from 2026-09-20. Date `secondary_only`. |
| BEI.DE | Beiersdorf AG | Q3 2026 statement | 2026-10-27 | 16 | Larger-cap exception bucket with no case for the exception over a core-universe name; no market data to evidence the bucket. Date `secondary_only`. |
| BAS.DE | BASF SE | Q3 2026 results | 2026-10-28 | 17 | Same bucket problem; a sector-wide chemicals print is not a company-specific edge. Date `secondary_only`. |
| MTX.DE | MTU Aero Engines AG | Q3 2026 results | 2026-10-29 | 18 | Larger-cap exception bucket; binary earnings; no structure available. Date `secondary_only`. |
| AOF.DE | ATOSS Software SE | Q3 2026 figures | 2026-10-23 | 12 | The only core-universe European lead found. Rejected on evidence, not thesis: the date came from an undated aggregator calendar the German-language search itself called probably stale, and ATOSS's traded value is in or below the €3–5M conditional tier, which `ETORO_TRADEABILITY.md` keeps off the main shortlist. Date `secondary_only`. |

The configured `MIN_EU_PRELIMINARY: 4` was met in count, but honestly: four of the five are
universe-excluded by market cap. The European core-universe channel (MDAX/SDAX dated
calendars) was **not reachable** — two separate searches, including one in German, returned
only DAX constituents and no dated MDAX/SDAX list. This is a discovery-breadth failure to
fix with a data source, not with more prose.

Checked and ruled out as a European special situation: there is **no DAX-family index
review in the decision window**. STOXX reviews fall in March, June, September and December;
the last was effective 2026-09-21 (Ströer into MDAX, Hugo Boss down to SDAX, OHB into
TecDAX) and the next scheduled review is 2026-12-03.

### US

| Ticker | Company | Lead event | Lead date | Days | Rejected because |
|---|---|---|---|---|---|
| FCN | FTI Consulting, Inc. | Q3 2026 results, pre-market | 2026-10-29 | 18 | Best-looking core/boundary lead of the week and the one worth re-running when data returns. Rejected only on the gate: company press release could not be opened, and no price/market-cap/liquidity row or OHLCV history exists to build a setup. Date `secondary_only`. |
| CNOB | ConnectOne Bancorp, Inc. | Q3 2026 results, pre-market | 2026-10-22 | 11 | Core market cap but a small regional bank whose dollar volume is very unlikely to clear the $25M preferred floor, and that cannot be checked here. Binary earnings with no setup. Date `secondary_only`. |
| GSBD | Goldman Sachs BDC, Inc. | Q3 2026 results, post-close | 2026-11-05 | 25 | Inside the 22–42 day Early Watch window, but Early Watch requires `verified` date status, which failed. A BDC's NAV print is also not a swing-trade catalyst with an observable trigger. Date `secondary_only`. |
| INO | Inovio Pharmaceuticals, Inc. | PDUFA target date, INO-3107 | 2026-10-30 | 19 | Binary FDA decision on a micro-cap. Sources conflict and none is sponsor-confirmed; FDA publishes no forward calendar, so the date can only come from a company filing this session cannot open. Financing/dilution risk is material and uncheckable. Date `secondary_only` at best. |
| AGIO | Agios Pharmaceuticals, Inc. | PDUFA target date, mitapivat | 2026-11-01 | 21 | Binary FDA decision at the edge of the Actionable horizon; single aggregator source, not sponsor-confirmed. `RISK_RULES.md` caps a deliberate binary hold at €75 and requires an explicit decision; nothing here justifies proposing one. Date `secondary_only`. |
| MRVL | Marvell Technology, Inc. | scanner breakout 2026-10-07, score 60 | n/a | n/a | Only non-stale snapshot row besides RXRX. Mega-cap and a crowded headline AI name — excluded by default under `ETORO_TRADEABILITY.md`. The scanner row is a lead, never evidence. Snapshot price $286.50; the 2026-10-07 signal is already -4.1% one day on. |
| RXRX | Recursion Pharmaceuticals, Inc. | scanner breakout 2026-10-06, score 65 | n/a | n/a | $5.36M average dollar volume is below even the $10–25M conditional tier, and the signal fired on an intraday move already +15.98% with the scanner's own `already extended` warning. One and three days on it is -10.9% and -9.1%. No forward catalyst was found. |

Also screened and found empty: `splits-calendar` returned no stock splits in the
2026-10-12 → 2026-11-01 window, and the FMP IPO calendar (which would carry lockup-expiry
leads) is denied on this tier, so no verified lockup or spin-off mechanics were available
to research.

## Red team

Applied to the pool as a whole, since no object survived to need an individual pass:

- **Every date is a third-party claim.** The PDUFA searches returned open conflicts — one
  source assigns bepirovirsen to Ionis and another to GSK; Mineralys appears as November in
  one calendar and December 27 in another — and the search itself warned that two of the
  top-ranked "November PDUFA" articles were from 2017 and 2020. That is precisely the
  failure mode the verification gate exists to catch.
- **Earnings-week sympathy is not a thesis.** Six of the twelve leads are simply companies
  that happen to report inside the window. Without expectations evidence (consensus,
  revisions, prior reaction) — none of which is obtainable on this tier — none of them would
  deserve research on its own merits.
- **The two scanner names are the strongest temptation and the clearest rejects.** Both
  cleared the 20-day high on heavy relative volume; both are down sharply days later, and
  the repository's own measurement says the 60–69 bucket averages -0.98% at ten sessions.
  "Scanner score is high" is explicitly not a setup.
- **Sunk-cost check.** FTK.DE and LW were carried for two and one weeks respectively and
  removed without ever producing a trigger. Nothing in this week's pool is being retained
  on the strength of past research effort; the book is empty on purpose.

Verdict for all twelve objects: `REJECT`.

## Removed or expired

Nothing new. The registry's three terminal objects (`CELC` archived, `FTK.DE` invalidated,
`LW` expired) were already removed in prior append-only reviews and are not re-decided here.

## What would change next week's answer

In priority order, and all of it is tooling rather than research:

1. **A working market-data source for the core universe** — an FMP tier that serves
   `quote`/`chart`/screener, or a restored Alpaca/Stooq path for the scanner. Without OHLCV
   history no run can produce a defensible trigger, stop or target, so no run can produce an
   `enter_if_triggered` row. This single gap is sufficient to explain four sterile weeks.
2. **Egress access to `www.sec.gov` and issuer IR domains**, so the verification stage can
   open a primary source and a catalyst date can reach `verified`.
3. **A scanner that is actually firing** — 2 recorded signals in five weeks is not a
   discovery channel, and it leaves the canonical snapshot too thin to meet breadth
   requirements on its own.
4. A dated MDAX/SDAX earnings calendar, to make the required European pass something other
   than a list of excluded mega-caps.

Until at least items 1 and 2 are addressed, the expected output of this routine is
`NO NEW TRADE` regardless of what the market is doing, and the weekly run should be read as
a calendar inventory rather than a decision engine.

## Sources used

### Primary / issuer sources

**None opened.** Every attempt was refused by the session's egress policy. All event dates
below are secondary and flagged for human verification.

### Structured market data and repository sources

- `data/research_snapshot.csv` + `data/research_snapshot.meta.json` (2 rows, SHA-256 `f08ca58…`), archived at `research/snapshots/research_snapshot-2026-10-11.csv`
- `data/scanner_signals.csv`, `data/market_regime.csv` (regime `mixed`, 2026-10-10), `research/scanner-summary.md`
- FMP connector: `calendar/earnings-calendar` (mega-caps only), `calendar/splits-calendar` (empty for the window), `secFilings/search-by-symbol` and `secFilings/8k-latest` (EDGAR metadata), `marketPerformance/most-active`
- `data/recommendations.csv`, `data/recommendation_reviews.csv`, `data/proposals.csv`, `trades.csv`
- `RESEARCH_BRIEF.md`, `RISK_RULES.md`, `SETUPS.md`, `ETORO_TRADEABILITY.md`, `MASTERPLAN.md`, `research_method/*`
- Prior reports `research/candidates-2026-09-20.md` … `-2026-08-16.md` and matching manifests

### Secondary leads (search-surfaced, not opened)

- Lamb Weston Q1 FY2027 results of 2026-10-06 — SEC 8-K exhibit `lw-20260830x8kxexx9911q27.htm` (summarized, not opened) and press coverage
- DAX-constituent Q3 dates — quartalszahlen.info and boerse.de calendars, plus a dpa-AFX weekly preview
- ATOSS Software Q3 date — boerse.de calendar (the search flagged it as likely stale)
- US small/mid-cap Q3 dates — company press releases surfaced for FCN, CNOB, BAFN and GSBD
- PDUFA leads — biopharmawatch, pdufa.bio, assyro and dansfera PDUFA calendars (mutually inconsistent)
- DAX-family index review schedule — STOXX index-review announcements and Deutsche Börse index-composition news
