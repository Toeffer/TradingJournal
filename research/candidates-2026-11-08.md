# Weekly Research and Decision Review — 2026-11-08

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: GPT-6; continuity-first hybrid discovery, independent skeptical red team; main source commit `d6a5f2cacefe5777272cf2c5882edcfb4dccb6ed`.
- Canonical input: `data/research_snapshot.csv`, SHA-256 `c9846a1ae3c174f1711c9d5056e38b3fad0803696581fbf67d79c8475c039d96`, generated 2026-11-07T00:05:41.529306+00:00; 2 US rows (ARRY Nov 5, GRAB Nov 6), zero XETRA rows. Exact bytes archived as `research/snapshots/research_snapshot-2026-11-08.csv`. Repository connector cannot execute the snapshot builder; no other data silently replaced the committed input.
- Prior committed reports reviewed: 2026-11-01 and 2026-10-25 plus 2026-09-20 for terminal history; their available manifests and rolling recommendation ledger were consulted. No other report/manifest pairs exist on main in the six-week window.
- Active prior recommendations: 1 (TUI1.DE); open trades: 0; proposals: 0. Terminal CELC/FTK.DE/LW unchanged.
- Discovery: hybrid (2 recent US scanner leads plus issuer-calendar search). Recent US scan Nov 7: no alerts; latest EU scan Nov 3: no alerts. Scanner regime defensive. No manual Finviz seed. EU preliminary: 8 XETRA shares.
- Preliminary: 12 (8 EU, 4 US). Final: **0 ACTIONABLE / 2 EARLY_WATCH / 10 REJECT**. Earnings-driven Actionable: 0/2. No ACT-NOW 0–7-day setup, no trigger-ready candidate.
- Weekly decision, Nov 9–13: **NO NEW TRADE**. No entry/stop/target or planned R invented. Fixed position cap EUR150, default 10 trading sessions, exit before catalyst yes; EUR75 only for explicitly approved binary hold, which does not exist.

## Prior recommendation audit

| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|
| TUI1.DE | 2026-11-01 at EUR6.956 | monitor | EUR7.57 Nov 6, **+8.8%** | No trigger ever defined or fired | carry (REPEAT) | monitor |

Prior FTK.DE and LW remain terminal; no reactivation. No open positions exist in `trades.csv`; no `manage` rows or inferred executions.

## Coming-week decision sheet

**NO NEW TRADE.** The scanner's ARRY and GRAB rows are discovery signals only; both followed completed issuer events. TUI has no canonical XETRA 20-session setup; PATH has dated NYSE OHLCV but no accepted structural entry/stop/target with >=1.5R.

### TUI1.DE — MONITOR / EARLY_WATCH (carry, REPEAT)

- Recommendation `REC-TUI1-2026-1101`. [TUI issuer pre-close update](https://www.tuigroup.com/en/investors/financial-news/pre-close-trading-update-2026) confirms **December 9, 2026** annual results (**31 days**). The September 22 tightened underlying EBIT guidance of EUR1.2–1.3bn and suspended revenue guidance are already public.
- [Dated XETRA reference](https://www.debelegger.nl/de/aktie/TUI1.XETRA): **EUR7.57** at Nov 6 17:35 CET, market cap EUR3.84bn; +8.8% from first mention EUR6.956. [eToro Germany share](https://www.etoro.com/de/markets/tui1.de): **ETORO_TRADEABLE: YES** public purchase page, ticker TUI1.DE, local XETRA EUR ordinary share. 3M average volume ~2.85m shares gives ~EUR21.6m/day at the Nov 6 close (proxy, not canonical 20d ADV). Core cap and preferred non-US liquidity pass; executable spread/account order permission not verified.
- Why not now: no current validated 20-session breakout, retest, stop or first target. A recent rally and already narrowed guidance argue against chasing. Promotion requires a new dated price structure and defensible >=1.5R plus reconfirmed event and broker.
- Bull: cruise/hotel rates and late bookings support FY27; base: FY26 meets known guidance with modest repricing; bear: winter bookings, fuel and airline costs undermine FY27 commentary. Risks: earnings gap, geopolitical/fuel and operating FX, possible financing, insider/short data unverified, broker slippage; EUR listing avoids direct share FX but local hours/settlement/holiday risk remains. Risk **High**, confidence **Low**.
- Red-team **DOWNGRADE_EARLY_WATCH**: 8.8% move since mention is not a validated setup. Pre-mortem: December print meets FY26 guidance yet FY27 winter outlook disappoints and price gaps down. **monitor** until 2026-11-15; remove if event moves/completes or risk/eligibility deteriorates. No trade; any later proposal must exit before catalyst by default.

### PATH — MONITOR / EARLY_WATCH (new)

- Recommendation `REC-PATH-2026-1108`. [UiPath issuer announcement](https://ir.uipath.com/news/detail/480/uipath-announces-third-quarter-fiscal-2027-financial-results-conference-call) dated Nov 5 explicitly schedules **December 3, 2026** fiscal Q3 FY27 earnings after US close (**25 days**) and 17:00 ET call. This **supersedes third-party calendars showing December 2**.
- [Dated NYSE structured reference](https://chartexchange.com/symbol/nyse-path/): Nov 6 close about **USD13.00**, market cap ~USD6.75bn, 30d average ~27.97m shares (~USD364m/day proxy), 50d SMA around USD14.04. [eToro Germany share](https://www.etoro.com/de/markets/path): **ETORO_TRADEABLE: YES**, NYSE USD common stock, core cap and preferred US liquidity pass; exact executable broker spread/account eligibility unverified.
- Expectations: issuer July ARR ~$1.938bn (+12% year-on-year), dollar retention 109%; fresh Q3 consensus revisions not independently confirmed. Price is below 50d average, not a validated breakout. Bull: automation/agentic ARR acceleration; base: growth roughly matches guidance; bear: renewals slow and valuation de-rates.
- Risks: USD/EUR FX for EUR account, US overlap-hours execution, overnight earnings gap, short-interest volatility (ChartExchange indicative ~25.44% of float, not independently confirmed), unknown insider/offering updates and spread. Risk **High**, confidence **Low**. Red-team **DOWNGRADE_EARLY_WATCH**: date alone does not produce entry/stop/target and >=1.5R. Pre-mortem: event misses inflated AI expectations and gaps through any imagined stop. **monitor** until 2026-11-15; remove if event changes or financing/setup fails. No trade.

## New research and rejected leads

Preliminary discovery was not ranked. The following were rejected only after issuer/broker checks and a separate skeptical review. The two new US scanner names were not treated as catalyst verification.

### SDF.DE — K+S Aktiengesellschaft — REJECT

- Origin: prior_report. [Opened primary source](https://www.kpluss.com/en-us/investor-relations/events/ks-q3-2026-earnings-release/): Q3/2026 quarterly report 07:00 CET, **2026-11-10** (2 days away). [Public eToro Germany stock page](https://www.etoro.com/de/markets/sdf.de) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: Guidance and financing already known; fresh consensus revisions not verified. Near-term binary print dominates any generic earnings-anticipation thesis.
- Classification and red-team **REJECT**: Two days to a binary earnings release; financing, salt-acquisition exposure and already-public guidance create gap and dilution risk; no current structure-based >=1.5R setup.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### BC8.DE — Bechtle AG — REJECT

- Origin: prior_report. [Opened primary source](https://www.bechtle.com/de-en/about-bechtle/investors/financial-calendar): Q3 2026 quarterly statement and call, **2026-11-13** (5 days away). [Public eToro Germany stock page](https://www.etoro.com/de/markets/bc8.de) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: July preliminary beat and guidance upgrade are already known. Positive operating momentum is not a surprise absent fresh estimates.
- Classification and red-team **REJECT**: Five days to earnings; prior July guidance raise lifted expectations; no multi-session technical invalidation or realistic >=1.5R target.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### EVD.DE — CTS Eventim AG & Co. KGaA — REJECT

- Origin: prior_report. [Opened primary source](https://corporate.eventim.de/en/investor-relations): Q3 quarterly statement publication, **2026-11-12** (4 days away). [Public eToro Germany stock page](https://www.etoro.com/de/markets/evd.de) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: H1 double-digit growth public; exact Q3 consensus not established. Positive concert/ticket demand and analyst optimism are already visible.
- Classification and red-team **REJECT**: Four days to earnings; September 30 CFO departure and H1 growth raise governance/expectation risk; no validated stop/target.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### DUE.DE — Dürr AG — REJECT

- Origin: prior_report. [Opened primary source](https://www.durr-group.com/en/investor-relations/financial-calendar/financial-calendar-detailseite/view/interim-statement-for-the-first-nine-months-of-2026-analysts-investors-call-95061): Q3/9M financial figures and analyst call, **2026-11-12** (4 days away). [Public eToro Germany stock page](https://www.etoro.com/de/markets/due.de) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: Vector efficiency plan already public; fresh estimates unknown. Any positive restructuring narrative competes with illiquidity and execution risk.
- Classification and red-team **REJECT**: Four days to results; eToro delayed EUR16.36 x 141081 three-month average shares = ~EUR2.31m/day, below EUR3m conditional liquidity floor; restructuring risk.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### AT1.DE — Aroundtown SA — REJECT

- Origin: prior_report. [Opened primary source](https://www.aroundtown.de/investor-relations): Q3 2026 financial report, **2026-11-25** (17 days away). [Public eToro Germany stock page](https://www.etoro.com/de/markets/at1.de) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: Transaction exposure and property refinancing risk dominate expectations; consensus not verified. October real-estate transaction is already public; financing is a possible adverse surprise.
- Classification and red-team **REJECT**: Seventeen-day event but October 20 Grand City/LEG stake transaction and financing complexity, ~EUR3.3m/day conditional liquidity proxy and no complete setup. Not promoted to conditional watchlist.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### TKA.DE — thyssenkrupp AG — REJECT

- Origin: routine. [Opened primary source](https://www.thyssenkrupp.com/en/investor-relations/calendar): Annual report FY2025/26, **2026-12-08** (30 days away). [Public eToro Germany stock page](https://www.etoro.com/de/markets/tka.de) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: Prior annual outlook and steel restructuring costs are widely known; current consensus revisions unverified. The date is not a trade trigger; substantial negative operational expectations already exist.
- Classification and red-team **REJECT**: Thirty-day verified event, but steel restructuring, expected losses and potential divestment/financing overwhelm a catalyst-only thesis; no defensible technical levels or current expectation edge.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### AAG.DE — Aumann AG — REJECT

- Origin: prior_report. [Opened primary source](https://www.aumann.com/en/investor-relations/financial-calendar): Nine-month interim statement, **2026-11-12** (4 days away). [Public eToro Germany stock page](https://www.etoro.com/de/markets/aag.de) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: Small-cap machinery order sensitivity; consensus not verified. Any event reaction can be dominated by spread and market impact.
- Classification and red-team **REJECT**: Market cap ~EUR178m below EUR500m core floor and delayed EUR13.90 x 33,364 three-month shares ~EUR0.46m/day far below liquidity floor.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### ARRY — Array Technologies, Inc. — REJECT

- Origin: scanner_seed. [Opened primary source](https://ir.arraytechinc.com/news-releases/news-release-details/array-technologies-and-shoals-technologies-group-announce): Q3 results and Shoals stock-for-stock merger announcement (already occurred), **2026-11-04** (4 days already past). [Public eToro Germany stock page](https://www.etoro.com/de/markets/arry) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: Record $2.6bn orderbook but 2026 revenue/EBITDA guidance reduced; merger synergies only indicative. Nov 5 14.16% move is reaction to disclosed news, not an unpriced upcoming event.
- Classification and red-team **REJECT**: Nov 5 scanner breakout followed Nov 4 Q3 results and merger announcement; no future dated binding closing/vote in 42 days. Stock-for-stock 1.6931 exchange ratio, preferred redemptions and reduced FY26 guidance complicate the risk. Canonical IEX value only $2.56m/day, not full-tape.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### GRAB — Grab Holdings Ltd — REJECT

- Origin: scanner_seed. [Opened primary source](https://investors.grab.com/news-and-events/news-details/2026/Grab-to-Announce-Third-Quarter-2026-Results-on-2-November-2026-2026-IH3lUy3opQ/default.aspx): Q3 2026 results (already occurred), **2026-11-02** (6 days already past). [Public eToro Germany stock page](https://www.etoro.com/de/markets/grab) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: Q2 guidance raise, buybacks and Atome acquisition already public; Q3 event completed. Nov 6 scanner move is a reaction, not an independently verified future catalyst.
- Classification and red-team **REJECT**: Nov 6 breakout followed completed Nov 2 earnings; eToro cap ~USD13.9bn larger-cap exception not justified, no dated forward catalyst or post-event consolidation/stop.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

### SHLS — Shoals Technologies Group Inc — REJECT

- Origin: routine. [Opened primary source](https://ir.arraytechinc.com/news-releases/news-release-details/array-technologies-and-shoals-technologies-group-announce): Shoals/Array merger announced (already occurred), **2026-11-04** (4 days already past). [Public eToro Germany stock page](https://www.etoro.com/de/markets/shls) confirms the displayed share instrument; this is not account-specific execution verification.
- Expectations/priced-in: $100m potential annual synergies are management projections, not realized; proxy materials pending. Merger terms and synergies publicly announced; no new timed edge.
- Classification and red-team **REJECT**: Nov 4 definitive merger announcement has no fixed closing/vote date within 42 days (Q1 2027 is only expected); 1.6931 ARRY shares per SHLS share and ~65% combined ownership bring exchange-ratio, dilution, approval and gap risks.
- Pre-mortem: disclosed expectations, merger/financing or an earnings gap overwhelms the thesis; no arbitrary entry, stop, target or >=1.5R was claimed.

## Removed or expired

No new removals. Historical FTK.DE, LW and CELC remain terminal; TUI1.DE retains its original recommendation ID. No trade or proposal records were modified.

## Sources used

Primary issuer links and public broker/dated structured sources are embedded in each company section; claim-level URLs and access timestamps are in the matching JSON manifest. Scanner snapshot is a discovery lead only.
