# Weekly Research and Decision Review — 2026-11-22
DRAFT for human review. Not financial advice.

## Run metadata
- Model / mode: GPT-6, continuity-first, catalyst-first, separate skeptical red-team review.
- Main source-of-truth commit: `bd8acb0af5ef62c39d7582961b13ca48cdf5f6c3`.
- Canonical input: `data/research_snapshot.csv`, SHA-256 `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`; generated November 21, 2026 01:28 UTC; **0 rows**. No fresh snapshot generation could be executed through GitHub; dated public market data supplements, not replaces, the committed file.
- Prior committed reports: October 25, November 1, November 8 and November 15 (plus rolling registry and November 15 manifest). Prior six-week coverage is limited by available committed reports.
- Prior active recommendations: 1 (TUI1.DE); open positions: 0; proposals: 0.
- Discovery: catalyst-first, 6 leads (4 XETRA/EU, 2 US). EU scanners November 17–20: no alerts; scanner summary has no current qualifying signals. No padding with undated events.
- Classifications: **0 ACTIONABLE / 0 EARLY_WATCH / 6 REJECT**. Earnings-driven Actionable: 0 of maximum 2.
- Next five trading sessions: **NO NEW TRADE**.

## Prior recommendation audit
| Ticker | First mention | Previous action | Latest reference | Since mention | Trigger result | New status / action |
|---|---|---|---|---|---|---|
| TUI1.DE | Nov 1 at €6.956 | monitor | €6.86, Nov 20 XETRA close | −1.4%; down 8.8% from Nov 13 €7.52 | No trigger was ever defined | expired / remove |

The original recommendation ID `REC-TUI1-2026-1101` is preserved. TUI's December 9 issuer-confirmed results are now **17 days away**, inside the Actionable horizon. A transition from Early Watch to Actionable is **not automatic**. The share has fallen below its first-mention price, and no validated breakout, pullback, structure-based stop, first target or ≥1.5R was established. The original watch is expired, not reset. Terminal PATH, FTK.DE, LW and CELC are not resurrected.

## Existing positions
No `status=open` trade exists in the committed journal. No management order or execution is implied.

## Coming-week decision sheet
**NO NEW TRADE** for November 23–27. No `enter_if_triggered` or proposal-quality `wait_pullback` survived verification and red team.

### TUI1.DE — REMOVE / REJECT (REPEAT)
- Recommendation ID: `REC-TUI1-2026-1101`; lifecycle **expired**, weekly action **remove**.
- [Issuer's September 22 pre-close release](https://www.tuigroup.com/en/investors/financial-news/pre-close-trading-update-2026) explicitly schedules FY2026 results for **December 9, 2026 (17 days)** and tightens underlying EBIT guidance to **€1.2–1.3bn**. Revenue guidance remains suspended. The known earnings outlook is not an unpriced catalyst.
- [Dated XETRA market data](https://stockanalysis.com/quote/etr/TUI1/) show **€6.86 close November 20**, market cap approximately **€3.48bn**, versus €7.52 November 13 and €6.956 at first mention. [eToro Germany](https://www.etoro.com/de/markets/tui1.de) publicly offers the TUI1.DE XETRA ordinary share in EUR: **ETORO_TRADEABLE: YES (public stock/share listing)**. Account-specific permissions and executable spread remain unverified. Its indicative three-month average ~2.85m shares/day corresponds to ~€19.6m/day using November 20 close, not canonical 20-day ADV.
- Expectations/priced-in: FY26 guidance was narrowed in September, and the main incremental uncertainty is FY27 winter booking momentum, airline margins and fuel/geopolitical costs. November price weakness does not establish support or a bargain. Exact refreshed consensus revisions were not independently verified.
- Bull: hotel/cruise pricing and winter bookings improve FY27 outlook. Base: FY26 roughly meets public EBIT guidance but guidance for FY27 stays cautious. Bear: weaker bookings, fuel or airline costs and geopolitical disruption lead to sell-the-news repricing.
- Risks: earnings gap; financing/debt and any offering or insider/short-positioning changes not fully independently resolved; FX-sensitive operating cash flows despite EUR share; XETRA hours/holidays/settlement, executable spread and slippage. **Risk High; trade confidence Low.** Default €150 position ceiling, 10-session holding period and exit-before-catalyst policy would apply to any *new* complete setup, but none exists.
- Red team: **REJECT**. Strongest argument: the 17-day binary event and price reversal do not substitute for an observable setup; an arbitrary day low would manufacture a stop. Pre-mortem: FY26 meets guidance yet winter bookings disappoint and the stock gaps below presumed support. Remove this watch; do not silently restart its first-mention clock. A new post-results setup would require genuinely new evidence.

## New research / rejected leads
- **GAP — Gap Inc. — REJECT (US, NYSE/USD):** [Issuer reported Q3 results on November 19](https://investors.gapinc.com/press-releases/news-details/2026/Gap-Inc--Reports-Third-Quarter-Fiscal-2026-Results/default.aspx), including 2% net sales growth, flat comparable sales and an updated outlook. [Issuer's stock page](https://investors.gapinc.com/stock-information/default.aspx) reports November 20 close **$20.94** following $18.79 on November 19. This is a **completed event**, not a verified future catalyst; no post-earnings consolidation/retest and ≥1.5R have been established. eToro Germany tradeability was not verified, so the hard broker gate independently rejects it. Red team: post-print momentum can reverse amid weak October/November demand and new Athleta leadership. Pre-mortem: gap retraces before a valid setup forms.
- **PATH — UiPath — REJECT (US, NYSE/USD):** December 3 earnings were previously verified, but the recommendation was already marked expired November 15 as it entered the 21-day horizon without a setup. No independently verified new thesis or complete structure justifies reopening. Prior [issuer announcement](https://ir.uipath.com/news/detail/480/uipath-announces-third-quarter-fiscal-2027-financial-results-conference-call) is context, not a new date verification this run. Red team: earnings gap risk, automation expectations and FX. Pre-mortem: prior watch is resurrected without new information.
- **SDF.DE — K+S — REJECT (XETRA/EUR):** November 10 reporting catalyst has passed. No newly opened future issuer catalyst or current structured setup. Financing/acquisition complexity remains a risk; prior broker eligibility is not current verification. Pre-mortem: treating stale event as fresh edge.
- **BC8.DE — Bechtle — REJECT (XETRA/EUR):** November 13 results have passed. July guidance increase was already known, no new verified catalyst and no defensible post-event structure. Pre-mortem: stale earnings surprise gets double-counted.
- **EVD.DE — CTS Eventim — REJECT (XETRA/EUR):** November 12 quarterly publication has passed. CFO-transition/governance questions and absent new structure preclude a setup. Pre-mortem: known growth is priced in and margins disappoint.

The four European preliminaries were TUI1.DE, SDF.DE, BC8.DE and EVD.DE. Only TUI had an opened future primary-source date and verified public broker availability; the other three were screened out early, not presented as verified new events.

## Sources used
[TUI issuer](https://www.tuigroup.com/en/investors/financial-news/pre-close-trading-update-2026); [TUI dated XETRA market data](https://stockanalysis.com/quote/etr/TUI1/); [TUI eToro Germany](https://www.etoro.com/de/markets/tui1.de); [Gap Q3 issuer release](https://investors.gapinc.com/press-releases/news-details/2026/Gap-Inc--Reports-Third-Quarter-Fiscal-2026-Results/default.aspx); [Gap issuer market data](https://investors.gapinc.com/stock-information/default.aspx); repository main snapshot, recommendation registry, prior manifests and EU scanner reports.

**NO NEW TRADE.** Evidence gaps: account-specific broker order eligibility and spreads, full updated 20-session structure, consensus revisions, financing/dilution and insider/short changes. No `trades.csv` or `data/proposals.csv` changes.
