# Weekly Research and Decision Review — 2026-10-04

DRAFT for human review. Not financial advice.

## Run metadata

- Model / research mode: Claude Opus 5 (`claude-opus-5`) / continuity-first, evidence-gated catalyst-first
- Canonical market-data input: `data/research_snapshot.csv`
- Snapshot SHA-256: `564467de230c68e0f3429fa65168d4b551a892a28f1b2f963063c07841a81334`
- Snapshot generated: 2026-10-04 21:39 UTC; **0 rows** (archived to `research/snapshots/research_snapshot-2026-10-04.csv`)
- Prior reports reviewed: `research/candidates-2026-09-20.md` and matching manifest, plus the 2026-08-09 … 2026-09-13 series
- Active recommendations reviewed: **0** (the active book was empty before this run)
- Open positions reviewed: **0** (`trades.csv` holds no open trade)
- Preliminary pool: **15 leads — 8 Europe/XETRA, 7 US** (configured minimum 12 total / 4 European)
- Final classifications: **0 `ACTIONABLE` / 0 `EARLY_WATCH` / 15 `REJECT`**
- Scanner input: reviewed; no signal inside the seven-day lookback. Latest recorded signal remains VOW3.DE on 2026-09-04, 30 days ago.
- Weekly decision: **NO NEW TRADE**

### Gap in the weekly series

No report exists for 2026-09-27. The routine did not run that week, so this is the first
decision review in two weeks. Nothing was carried across the gap because the active book
was already empty.

## This week's binding constraint: the evidence channels are down

The last four reviews each concluded `NO NEW TRADE` citing the empty canonical snapshot.
That diagnosis was incomplete. `discovery.md` explicitly says a missing snapshot or Finviz
preflight must *not* reduce breadth — the fallback is catalyst-first research against
primary sources. This run attempted that fallback and found the primary-source path itself
is now blocked. The relevant checks, all made this run:

| Channel | Status this run | Consequence |
|---|---|---|
| Issuer IR sites, `sec.gov`, newswires | **Egress-blocked** by the environment network policy | No catalyst date can reach `verified` |
| Quartr MCP (primary filings/events) | **`subscription_required`**, plan `none` | Primary-source substitute unavailable |
| `etoro.com` | **Egress-blocked** | `ETORO_TRADEABLE` unverifiable for every name |
| FMP MCP — quotes, screener, OHLC, non-US | **Plan-denied** | No intraday highs/lows, no EU prices, no screening |
| FMP MCP — earnings calendar, market cap | Working | Leads and cap/liquidity gates only |
| FMP MCP — US close history | Working but capped at **~10 calendar days** | Cannot compute a 20-day high or EMA20/50 |
| `stooq.com`, `finance.yahoo.com` | **Egress-blocked** | No substitute price history |
| `data/scanner_signals.csv` | Pipeline healthy, **0 qualifying signals in 30 days** | No scanner structure rows |
| `data/eu_quote_history.csv` | 46 XETRA names, 186 sessions, but ends **2026-09-22** | Structure 12 days stale, no current price |
| `data/finviz_watchlist.csv` | Empty (header only) | No manual discovery seeds |

Two independent hard gates therefore fail for every name in the pool:

1. **Verification gate.** `verification.md` allows only `verified` catalyst dates into the
   Actionable or Early Watch lists, and `verified` requires the synthesizing pass to open
   the primary source itself. A third-party calendar, a search snippet or model memory is
   explicitly a lead only. Every date available this run is `secondary_only` or worse.
2. **Broker gate.** `ETORO_TRADEABILITY.md` makes verified eToro availability a hard
   precondition for the final shortlist and directs rejection when availability *cannot be
   verified*. It cannot be verified this run.

This is not a thin-opportunity week being reported as a tooling problem. It is the reverse:
there is at least one structurally interesting name in the pool (ETSY, below), and the
process is refusing to promote it because the evidence standard cannot be met. That is the
method working as designed. But five consecutive no-trade weeks are now driven by tooling,
not by the market, and the fixes are listed under *Operator actions* at the end.

The scanner itself deserves a separate note: it is **not** broken. It has run every weekday
through 2026-10-03, scanning 54 tickers and scoring 31 candidates on its last run, and has
simply found nothing at or above its score-60 threshold for 30 days. In a `mixed` regime
with 47.2% of the universe above its 20-day moving average, zero breakout signals is a
plausible reading rather than a fault.

## Prior recommendation audit

| Ticker | First mentioned | Previous action | Since mention | Trigger result | New status | This week |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

The active book was empty at the start of this run. The three recommendations in the
registry all reached terminal status earlier and correctly stay in the registry for outcome
analysis: `REC-CELC-2026-0004` (`archived` 2026-08-10, trade closed +4.04R),
`REC-FTK-2026-0906` (`invalidated` 2026-09-20) and `REC-LW-2026-0913` (`expired`
2026-09-20). No prior recommendation required a decision this week, so no review row was
appended and the weekly decision archive is empty by design.

Both of last week's removals are worth checking against what has happened since, because a
removal is a decision that can also be wrong:

- **FTK.DE** — the monthly KPI release the object was built around is dated 2026-10-05, i.e.
  tomorrow. Removing it on 2026-09-20 meant giving up the thesis one session before the
  event. No current price is reachable to score that decision, and the governance risk from
  the 2026-09-11 chairman resignation was a sound reason not to anticipate. Recorded here so
  the outcome can be graded later rather than quietly forgotten.
- **LW** — fiscal Q1 2027 results are dated 2026-10-06. Same situation; the object was
  removed 16 days before its catalyst without a setup ever forming.

Neither is being re-opened: re-entering a removed object on the eve of a binary event, with
no verified date and no current price, is precisely the anticipation `SETUPS.md` rules out.

## Existing positions

None. `trades.csv` contains 18 trades and all are `closed`. No `manage` recommendation is
required this week, and nothing in this run infers any execution.

## Coming-week decision sheet

No candidate has a complete trigger-ready setup, and none can legitimately hold Early Watch
either. **NO NEW TRADE.**

Zero `enter_if_triggered` rows, zero `wait_pullback`, zero `monitor`, zero `manage`, zero
`remove`. The active book stays empty.

## New research

Fifteen leads were discovered catalyst-first and are recorded in full in the manifest. All
fifteen are `REJECT`. Grouped by the reason that actually decided each one:

### Structurally interesting, blocked only by the evidence gate

**ETSY — Etsy, Inc. (NASDAQ, USD)** — the strongest lead in the pool.
- Discovery origin: FMP earnings calendar, 2026-10-05 … 2026-11-15 window.
- Market data: closed $72.77 on 2026-10-02, up 6.3% across the six sessions from 2026-09-25
  and closing at the top of that range; about $194M average daily traded value; $6.91B market
  cap, squarely core universe.
- Why it did not displace anything: its calendar date, 2026-11-04, is 31 days out — inside
  the 22–42 day Early Watch band, so it could not have produced an entry this week under any
  circumstances. And because the date is `secondary_only` (secondary trackers describe it as
  an estimate from past reporting cadence, not a company confirmation), it cannot hold Early
  Watch either. This is the first name to re-examine once an evidence channel is restored.

**NDX1.DE — Nordex SE (XETRA, EUR)** — best European structure, defeated by staleness.
- Discovery origin: `data/eu_quote_history.csv` structure pass over 46 XETRA names.
- Market data: closed €41.90 on 2026-09-22 — exactly its 20-session high — above EMA20
  (€39.34) and EMA50 (€39.69), with about €22.1M average daily traded value, comfortably
  above the €5M non-US floor.
- Why rejected: the structure is 12 days stale and no current EU price is reachable. A
  secondary snippet quotes Nordex near €38.78, which would mean the breakout level has
  already failed. Setting a trigger off a 12-day-old level with no visibility into the
  intervening eight sessions is the arbitrary level `red_team.md` forbids. The Q3 date is not
  even settled between secondary sources (2026-11-05 versus 2026-10-29/30).

**WAF.DE — Siltronic AG (XETRA, EUR)** — second-best European structure: €82.75 on
2026-09-22, 1.0% below its 20-session high, above EMA20 and EMA50. Rejected for the same
staleness and missing-current-price reasons, with about €6.8M traded value only modestly
above the floor and the 50-session high (€92.80) 12% overhead.

### Rejected on universe or liquidity rules, before the evidence gate mattered

- **TLRY — Tilray Brands** — about $404M market cap, below the $500M core-universe floor; no
  exception applies. Its 2026-10-08 date would otherwise have been the nearest event in the pool.
- **FUBO — fuboTV** — about $10M average daily traded value, at the very bottom of the
  $10–25M conditional band and far below the $25M preferred US floor; Conditional Watchlist
  at best, never main shortlist. Price also fell 10.2% over six sessions to close at the low.
- **JEN.DE — JENOPTIK** — sat 0.1% under its 20-session high above EMA20, but about €4.4M
  traded value is below the €5M preferred non-US floor, so it is a Conditional Watchlist
  object only, absent explicit human approval of a lower-liquidity setup.

### Rejected on price structure — no allowed setup exists

- **AAL — American Airlines** ($8.57B, core) — the only core-universe US name with a calendar
  date inside the 0–21 day actionable window (2026-10-22). The six sessions into it fell 6.7%
  and closed at the low of the range. A declining tape into a binary print is not one of the
  four allowed setups, and `RISK_RULES.md` prefers trading after the information is public.
- **RIOT — Riot Platforms** ($7.46B) — fell 14.2% over six sessions, 23.00 → 19.73, with no
  stabilisation; date 25 days out.
- **BILI — Bilibili** ($6.06B) — drifted down 3.1% to close at the six-session low; date 39
  days out, at the far edge of the discovery horizon; as a US-listed ADR it would also need
  local-listing-versus-ADR verification that is unreachable this run.
- **KGX.DE — KION GROUP** — 15.1% below its 20-session high, below EMA20 and EMA50. A
  downtrend, not a pullback; `SETUPS.md` excludes "it is down a lot". KION also already
  produced a −1.00R loss as trade `2026-0017`.
- **PUM.DE — PUMA** — 13.5% below its 20-session high, below EMA20 and EMA50, with the
  50-session high far overhead.
- **AIXA.DE — AIXTRON** — 6.6% below its 20-session high, only marginally above EMA20 and
  still below EMA50.
- **S92.DE — SMA Solar Technology** — held above EMA20 and EMA50 but 3.0% below the
  20-session high, traded value (~€6.2M) close to the floor.
- **TKA.DE — thyssenkrupp** — deepest European liquidity at about €32M and above both EMAs,
  but 3.5% below the 20-session high with no verified near-term event.
- **LCID — Lucid Group** ($1.31B) — carried for breadth from the earnings calendar and
  dropped at discovery before market-data work; a pre-revenue-scale EV issuer carries exactly
  the financing and dilution risk `red_team.md` requires to be ruled out from primary filings
  that cannot be opened this run.

## Red team

The pass was run against the one conclusion this report actually makes — that no name
qualifies — and against the two names that came closest.

- *Is the report hiding a real setup behind a process complaint?* ETSY is the test case. Its
  tape is genuinely constructive. But its own calendar date is 31 days out, so even a fully
  verified ETSY could only have been `monitor` this week, never an entry. No entry was
  forgone by the evidence gate.
- *Is NDX1.DE being rejected too cautiously?* No. The only concrete current data point —
  a secondary quote near €38.78 against a €41.90 close — points to the breakout having
  already failed. Acting on the stale level would have been a chase into a broken structure.
- *Is the pool padded to look like breadth?* Eight of the fifteen leads were rejected on
  rules that need no judgement (market cap, liquidity tier, distance from structure), which is
  what an honest funnel looks like. No name was retained for sunk effort.
- *Has this thesis failed before?* KGX.DE (trade `2026-0017`, −1.00R) is in the pool and was
  rejected again on fresh structure grounds, not on the prior loss.

Verdict for all fifteen: `REJECT`. No object enters the active book.

## Removed or expired

Nothing was removed this week; the active book was already empty. The three terminal
recommendations listed in the audit above remain in the registry with their existing status.

## Operator actions — what would restore the routine

In rough order of leverage:

1. **Restore a primary-source channel.** This is the binding constraint. Either widen the
   environment's network egress policy to allow issuer IR domains and `sec.gov`, or activate
   the Quartr subscription (the MCP server is already wired up and reports plan `none` for
   `chris.bloeffer@gmail.com`). Without one of these, no future run can produce an
   `ACTIONABLE` name no matter how good the tape looks.
2. **Unblock `etoro.com`**, or record a verified eToro instrument list in the repository that
   the routine can check offline. The broker gate alone is enough to reject every candidate.
3. **Upgrade or replace the FMP plan** so quotes, OHLC history and non-US symbols resolve.
   Closing prices capped at ten days cannot express a 20-day high, which is a precondition of
   three of the four setups in `SETUPS.md`.
4. **Refresh `data/eu_quote_history.csv`.** It stopped on 2026-09-22 and is the only
   multi-session European structure source the repository has.
5. **Re-seed `data/finviz_watchlist.csv`** when convenient. Not a blocker — `discovery.md`
   treats absent manual seeds as normal — but it is currently empty.
6. **Check why no run happened on 2026-09-27**, so the weekly series does not silently skip
   again.

Nothing above changes `trades.csv`, `data/proposals.csv`, or any risk rule.

## Sources used

### Primary / issuer sources

**None.** No primary source could be opened in this run. Issuer IR domains, `sec.gov` and
newswires are egress-blocked, and the Quartr MCP primary-source channel returned
`subscription_required`. This is recorded as `source_counts.primary = 0` in the manifest
rather than padded with secondary citations.

### Structured market data

- FMP MCP `calendar/earnings-calendar` — event leads for 2026-10-05 … 2026-11-15 (third-party
  calendar; leads only, cannot verify a date)
- FMP MCP `company/batch-market-cap` — market capitalisation as of 2026-10-02
- FMP MCP `chart/historical-price-eod-light` — US closes and volumes, 2026-09-25 … 2026-10-02

### Repository sources

- `data/research_snapshot.csv` and `data/research_snapshot.meta.json` (0 rows; archived to
  `research/snapshots/research_snapshot-2026-10-04.csv`)
- `data/eu_quote_history.csv` — 46 XETRA names, 186 sessions, through 2026-09-22
- `data/scanner_signals.csv`, `research/scans/scan-2026-10-03-0056.md`, `data/market_regime.csv`
- `data/recommendations.csv`, `data/recommendation_reviews.csv`, `trades.csv`, `data/proposals.csv`
- `RESEARCH_BRIEF.md`, `RISK_RULES.md`, `SETUPS.md`, `ETORO_TRADEABILITY.md`, `config/risk.toml`,
  and the `research_method/` files
- Prior `research/candidates-2026-09-20.md` and matching manifest

### Secondary context (leads only)

- marketscreener.com — Nordex SE financial calendar (conflicting Q3 dates)
- ad-hoc-news.de — Nordex price snippet near €38.78
- marketbeat.com — Etsy earnings-date estimate of 2026-11-04
- Search-level PDUFA calendar summaries for October/November 2026; no October decision
  belonged to a core-universe, eToro-verifiable issuer, and none could be verified against a
  primary FDA or issuer source
