# Weekly Research and Decision Review — 2026-09-27

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: claude-opus-5 (Claude Code scheduled routine) / continuity-first, catalyst-first
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`
- Snapshot generated: 2026-09-27 21:39 UTC via `build_research_snapshot.py --archive`; **0 rows**
- Prior reports reviewed: `candidates-2026-08-16`, `-08-23`, `-08-30`, `-09-06`, `-09-13`, `-09-20` and matching manifests
- Active recommendations reviewed: **0** — the registry holds only terminal rows (CELC `archived`, FTK.DE `invalidated`, LW `expired`)
- Open positions reviewed: **0** — `trades.csv` has no open trades; `data/proposals.csv` is empty
- New leads / Actionable / Early Watch / Reject: **9 / 0 / 0 / 9**
- Preliminary pool: 7 US + 2 Europe/XETRA (below the configured `MIN_EU_PRELIMINARY: 4`; see *European pass* below)
- Weekly decision: **NO NEW TRADE**

## Why this week is different from the last six

The last six reports all concluded NO NEW TRADE and all gave essentially one reason: names
were "absent from the canonical snapshot," so no structure existed. This run establishes that
the cause is not market conditions and not a thin week. **Three independent hard gates in the
method now fail for every possible candidate, and two of them cannot be cleared by any amount
of research effort from inside this environment.**

1. **Primary-source verification is impossible.** `verification.md` requires the synthesizing
   pass to open the primary source itself, and only `verified` may enter Actionable or Early
   Watch. Every primary-source domain tried this run is refused by the environment's network
   egress policy: `about.puma.com`, `www.kiongroup.com`, `www.aixtron.com`, **`www.sec.gov`**,
   `www.globenewswire.com`, `www.businesswire.com`, `finance.yahoo.com`, `www.nasdaq.com`,
   even `en.wikipedia.org`. WebSearch returns snippets, and `RESEARCH_BRIEF.md` states plainly
   that a search snippet cannot verify a final date. So **no candidate can reach `verified`,
   which means the Actionable and Early Watch lists are mechanically guaranteed to be empty.**
2. **eToro tradeability is unverifiable.** `ETORO_TRADEABILITY.md` makes verified eToro
   availability a hard condition for the final shortlist and requires rejection when it cannot
   be verified. `www.etoro.com` is egress-blocked, so `ETORO_TRADEABLE: YES` cannot be
   evidenced for any name. Earlier reports cited "public eToro Germany/EU instrument pages";
   those are not reachable from this session.
3. **The data pack is dead, not merely thin.** The snapshot is built only from
   `data/scanner_signals.csv`, whose newest row is `VOW3.DE` on **2026-09-04 — 23 days old**,
   far outside the 7-day `SCANNER_LOOKBACK_DAYS`. The snapshot has therefore been empty since
   2026-09-11 and will stay empty at 0 rows until the scanner produces signals again.

The one genuinely new capability this run found is that FMP does supply dated structured market
data for US symbols (price, market cap, average volume), which let this report screen market-cap
bucket and liquidity against **real numbers** rather than skipping the test. That is why the
rejections below cite measured figures. But FMP on the current plan **denies all non-US symbols**
and denies EOD price history for every US name in the pool except TLRY, so multi-session
structure remains unavailable for the names that would otherwise qualify.

**Conclusion: this routine cannot currently produce an `enter_if_triggered` recommendation
regardless of market conditions.** That is a tooling and access problem, not a research verdict,
and it needs a human decision (see *What would unblock this*).

## Prior recommendation audit

| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

No active recommendations exist. All three registry objects reached terminal status on or before
2026-09-20: `REC-CELC-2026-0004` (`archived`, trade closed and reconciled), `REC-FTK-2026-0906`
(`invalidated` 2026-09-20), `REC-LW-2026-0913` (`expired` 2026-09-20). Terminal objects are
retained in the registry for outcome analysis and are not re-reviewed, so **no review rows were
appended this week and the registry is unchanged.**

`FTK.DE` deserves one note for continuity honesty: its removal condition said to archive "unless
a genuinely new thesis/event creates a new research object." Its 2026-10-05 monthly KPIs are now
8 days away and its Q3 update is ~24 days away, but nothing genuinely new has appeared, the
September 11 chairman-resignation governance risk is unresolved, and its date could not be
verified this week either. It stays removed rather than being quietly resurrected.

## Existing positions

None. `trades.csv` contains no open positions, so no `manage` recommendation is due. The most
recent trade closed on 2026-07-08; the book has been flat for 81 days.

## Coming-week decision sheet

No candidate has a verified catalyst, verified broker availability, or a defensible
structure-based setup. **NO NEW TRADE.**

There are no `enter_if_triggered`, `wait_pullback`, `monitor`, `manage` or `remove` rows this
week: every lead was rejected before it could enter the registry, and nothing was carried over
to act on. Per `output_schema.md`, a rejected lead never enters the recommendation registry.

## New research

Market data below is FMP `company/profile-symbol`, EOD 2026-09-25. Average daily dollar volume
is average volume × last price. Bucket tests are against `MARKET_CAP_MIN` $500M / `MARKET_CAP_MAX`
$10B and the $25M US preferred liquidity floor.

| Ticker | Price | Market cap | Avg vol | Avg $ vol | Bucket | Liquidity | Catalyst lead | Days | Date status |
|---|---|---|---|---|---|---|---|---|---|
| LEVI | $19.74 | $7.72B | 2.50M | **$49.4M** | core | pass | Q3 FY26 results | 10 | secondary_only |
| CALM | $67.43 | $3.16B | 0.90M | **$60.5M** | core | pass | Q1 FY27 results | 3 | secondary_only |
| OZK | $46.89 | $5.12B | 1.13M | **$53.2M** | core | pass | Q3 2026 earnings | 18 | unverified |
| AZZ | $137.17 | $4.12B | 0.28M | **$38.3M** | core | pass | Q2 FY27 results | 16 | secondary_only |
| SMPL | $9.60 | $0.85B | 2.31M | $22.2M | core | conditional | none found | — | — |
| TLRY | $4.13 | **$0.46B** | 3.84M | $15.9M | **below min** | conditional | quarterly results | 11 | secondary_only |
| HELE | $28.63 | $0.67B | 0.48M | $13.7M | core | conditional | none found | — | — |
| PUM.DE | n/a | n/a | n/a | n/a | unknown | unknown | Q3 2026 statement | 32 | secondary_only |
| KGX.DE | n/a | n/a | n/a | n/a | unknown | unknown | Q3 2026 statement | 32 | secondary_only |

### LEVI — Levi Strauss & Co. — REJECT

- Discovery origin: US catalyst-first sourcing; fiscal Q3 ended 2026-08-30.
- Evidence: core-universe $7.72B cap and about **$49.4M** average daily dollar volume, comfortably
  clear of the $25M floor — the cleanest measurable profile in the pool. Search results report a
  Businesswire release dated 2026-09-23 scheduling Q3 FY26 results for **2026-10-07**, 10 days out
  and inside the Actionable window.
- Expectations: **not established.** The FMP plan denies per-symbol earnings and estimate endpoints,
  and no expectations page could be opened. Price 19.74 against a 52-week range of 17.72–25.70 is
  context only.
- Why rejected: the date rests on a search-result summary of a release that was never opened, so it
  is `secondary_only`. eToro availability is unverifiable and no multi-session structure exists
  (FMP denied LEVI EOD history; snapshot 0 rows). No level was invented.
- Red-team verdict: `REJECT`. Pre-mortem: mistaking an unusually clean liquidity profile for a
  substitute for the verification gate, and buying a weak apparel name into an unread print.

### CALM — Cal-Maine Foods, Inc. — REJECT

- Discovery origin: US catalyst-first sourcing; fiscal Q1 FY2027.
- Evidence: core-universe $3.16B cap, about **$60.5M** average daily dollar volume — deepest in the
  pool. Search results report results scheduled for **2026-09-30**, only 3 days away.
- Why rejected: two independent kills. The date is `secondary_only`, and at 3 days out no pre-event
  structure trade is permissible under the `exit_before_catalyst = yes` default — an entry here
  would be an unsanctioned binary bet at full size, which `RISK_RULES.md` caps at €75 and only with
  an explicit prior decision that does not exist.
- Note: 67.43 against a 52-week range of 66.62–98.44 puts it within ~1.2% of its 52-week low. "It is
  down a lot" is listed in `SETUPS.md` under *deliberately not a setup*.
- Red-team verdict: `REJECT`.

### AZZ — AZZ Inc. — REJECT

- Discovery origin: US catalyst-first sourcing; fiscal Q2 FY2027.
- Evidence: core-universe $4.12B cap, about **$38.3M** average daily dollar volume. Search results
  report results after the close on **2026-10-13** with a call on 2026-10-14, 16 days out.
- Why rejected: date traces to an aggregator summary of a scheduling release, not an opened AZZ or
  SEC document, so `secondary_only`; no expectations readable; no structure available.
- Risk note the numbers flag: average volume is only 279k shares, so the dollar-volume test passes
  largely on a $137 share price. Depth at the intended entry is thinner than $38M/day suggests.
- Red-team verdict: `REJECT`.

### OZK — Bank OZK — REJECT

- Discovery origin: US catalyst-first sourcing.
- Evidence: core-universe $5.12B cap, about **$53.2M** average daily dollar volume.
- Why rejected: the **only** support for 2026-10-15 is an aggregator's *expected* date, which is
  `unverified` — weaker than the other US leads, which at least trace to company scheduling
  releases. A regional bank with CRE concentration also carries credit-disclosure gap risk a price
  stop cannot bound.
- Red-team verdict: `REJECT`.

### SMPL — The Simply Good Foods Company — REJECT

- Discovery origin: US catalyst-first sourcing (fiscal Q4, August year-end).
- Why rejected: about **$22.2M** average daily dollar volume falls in the $10–25M conditional band,
  below the $25M preferred floor, so the broker overlay confines it to the Conditional Watchlist at
  best; and no catalyst date could be established even to `secondary_only` standard.
- Context: 9.60 against a 52-week range of 9.375–25.66 — down ~63% from the high, within ~2.4% of
  the low. A collapsed multiple is not evidence of cheapness.
- Red-team verdict: `REJECT`.

### HELE — Helen of Troy Limited — REJECT

- Discovery origin: US catalyst-first sourcing (fiscal Q2, February year-end).
- Why rejected: about **$13.7M** average daily dollar volume — roughly half the preferred floor,
  firmly conditional-tier — and no catalyst date could be established. The share has also roughly
  doubled off its 52-week low (13.85) to 28.63 near the high (30.68): a move that should not be
  chased, in a thin name where the exit is harder than the entry.
- Red-team verdict: `REJECT`.

### TLRY — Tilray Brands, Inc. — REJECT

- Discovery origin: the FMP structured earnings calendar — the only name in the pool that appeared
  in a structured catalyst calendar *and* for which FMP allowed EOD history.
- Evidence: 18 sessions of dated OHLCV (2026-09-01 → 2026-09-25) show a drift from 4.50 to 4.13
  inside a recent 4.03–4.29 range, with **no** close above a 20-day high and **no** 2× relative-volume
  expansion — so measured against `SETUPS.md`, neither a `breakout` nor a `pullback` setup exists.
  Calendar consensus for **2026-10-08** is −0.164 EPS on ~$267.8M revenue.
- Why rejected: market cap **$461.9M is below the $500M `MARKET_CAP_MIN`**, so it is outside the
  configured universe before any setup question arises; liquidity ~$15.9M/day is conditional-tier;
  and it is a loss-making issuer with a long equity-issuance record, so dilution can overwhelm any
  technical setup.
- Worth recording: the one name where structure *could* be measured showed no setup. Data
  availability is not an edge.
- Red-team verdict: `REJECT`.

### European pass — PUM.DE and KGX.DE — REJECT, and why the EU minimum was missed

`MIN_EU_PRELIMINARY` is 4 and this run produced 2. Stating precisely why, as `discovery.md`
requires: **no structured market data of any kind is obtainable for XETRA listings.** FMP returns
ACCESS DENIED for non-US symbols on the current plan — confirmed on both `company/profile-symbol`
and `chart/historical-price-eod-light` for `PUM.DE` — and the canonical snapshot holds 0 rows. Adding
two more European tickers would have produced names with no price, no market cap, no liquidity
figure and no verifiable date, which is padding; `discovery.md` forbids padding and the broker
overlay states a sparse report is better than a padded one. The two names below are carried as
documented leads for a future run that has data access, not as candidates.

- **PUM.DE — PUMA SE** — search results report a Q3 2026 quarterly statement on **2026-10-29**
  (32 days out, i.e. the Early Watch window) per PUMA's IR calendar, which is egress-blocked.
  Rejected: no market-data row exists at all, so the name cannot be liquidity-screened or sized;
  date `secondary_only`; eToro unverifiable.
- **KGX.DE — KION GROUP AG** — search results report a Q3 2026 statement for the period ended
  2026-09-30 on **2026-10-29**. Rejected for the same absent-data reason, **plus prior-failure
  history**: `trades.csv` records trade `2026-0017`, KGX.DE long opened 2026-07-07 at 45.43 and
  stopped out 2026-07-08 at 41.22 for −€11.93 / −1.00R, with a note stating no supporting research
  file exists anywhere in the repo. `red_team.md` requires showing what is genuinely different now;
  with no data and no verified date, nothing is.

### Universe-excluded context (not leads)

The FMP date-range earnings calendar is the only structured catalyst calendar this run could reach,
and for 2026-09-28 → 2026-10-16 it returned just 13 names, of which **12 are mega-caps excluded by
default** under `ETORO_TRADEABILITY.md` (TSM, BAC, GS, JNJ, JPM, WFC, C, UNH, DAL, PEP, NKE, CCL).
The 13th was TLRY, which fails the market-cap floor. They are recorded here as context, not as
rejected leads: the universe rule excludes them before analysis. **The only structured catalyst
calendar available to this routine is therefore almost entirely outside its own investable
universe** — a discovery-channel problem worth fixing alongside the scanner.

## Removed or expired

Nothing was removed this week; the three terminal objects were already removed on or before
2026-09-20 and are retained for outcome analysis. `research/decisions/decisions-2026-09-27.csv`
is written with **0 rows**, which is the correct and auditable record that this run reviewed no
active recommendation because none existed.

## What would unblock this

Listed for the human because the routine cannot fix any of these itself, in priority order:

1. **Restore the scanner.** No signal since 2026-09-04 means the canonical snapshot is permanently
   0 rows and every report will keep rejecting names for "no structure." This is the single
   highest-value fix and it is upstream of everything else.
2. **Allow primary-source domains through the egress policy** for this environment — at minimum
   `www.sec.gov`, the newswires (`businesswire.com`, `globenewswire.com`, `prnewswire.com`) and
   issuer IR domains. Until then `date_status: verified` is unreachable and the method's own rules
   guarantee an empty shortlist every week.
3. **Allow `www.etoro.com`**, or record tradeability in-repo (e.g. a checked-in eToro universe file),
   so the broker gate can be satisfied without a live page fetch.
4. **Decide on market-data access.** The FMP plan blocks non-US symbols, per-symbol calendars,
   estimates and most EOD history. Without non-US coverage the mandatory European pass cannot be
   run on evidence at all, whatever the egress policy allows.

Items 1–3 are each independently sufficient to keep the output at NO NEW TRADE forever.

## Sources used

### Primary sources

**None.** No primary source could be opened in this run; every primary-source domain attempted was
refused by the network egress policy. This is recorded as `source_counts.primary: 0` in the manifest
and is the binding constraint on the week's output.

### Market data

- FMP MCP `company/profile-symbol` — LEVI, CALM, AZZ, OZK, SMPL, HELE, TLRY (EOD 2026-09-25)
- FMP MCP `calendar/earnings-calendar` — window 2026-09-28 → 2026-10-16, last updated 2026-09-27
- FMP MCP `chart/historical-price-eod-full` — TLRY, 2026-09-01 → 2026-09-25 (denied for all others)

### Repository

- `data/research_snapshot.csv` (0 rows) and `data/research_snapshot.meta.json`
- `data/scanner_signals.csv` (newest signal 2026-09-04), `data/market_regime.csv`
- `data/recommendations.csv`, `data/recommendation_reviews.csv`, `trades.csv`, `data/proposals.csv`
- `research/candidates-2026-08-16` → `-09-20` and matching manifests
- `RESEARCH_BRIEF.md`, `RISK_RULES.md`, `SETUPS.md`, `ETORO_TRADEABILITY.md`, `research_method/*`

### Context (snippet level, pages not opened)

- WebSearch result summaries for LEVI, CALM, AZZ and OZK earnings scheduling, and for the PUMA SE
  and KION GROUP Q3 2026 calendar dates. Every underlying page was egress-blocked; these support
  `secondary_only` / `unverified` date status only and cannot promote a candidate.
