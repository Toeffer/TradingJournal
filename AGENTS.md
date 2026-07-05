# AGENTS.md — Trading Journal

This repository **is** my trading journal. You (Claude Code) are the interface to it.
I will talk to you in plain language; you keep the records structured, compute real
stats from the data, and review my behavior honestly.

This works from the command line **and the Claude Code mobile app** — so I can log a
trade by talking to you right after I make it. Keep every interaction fast and
low-friction; if logging is slow, I won't do it, and an empty journal is useless.

**Not financial advice.** This is reflection on my own past decisions. Never tell me
what to buy. Your job is to record, measure, and hold up a mirror.

---

## How I'll talk to you

Recognize these intents from natural language (I won't use exact commands):

- **Log a trade** — e.g. "opened ABCD at 12.40, stop 11.50, target 15, half size,
  earnings catalyst May 2, basing breakout, from the routine, risk medium." -> create a
  new entry (see Logging).
- **Close a trade** — e.g. "closed ABCD at 14.10" or "stopped out of ABCD at 11.45."
  -> update the open entry, compute results (see Closing).
- **Stats** — e.g. "how am I doing this month?" -> compute from the data (see Stats).
- **Review** — e.g. "review my last two weeks." -> the honest coaching pass (see Review).
- **Scanner review** — e.g. "review the latest scanner output" -> read the newest
  `research/scans/scan-*.md` plus `SCANNER_RESEARCH_PROMPT.md`, then classify names as
  Deep dive / Watch / Reject. This is research triage only; do not log trades unless I
  explicitly say I entered one.
- **Log a proposal** — e.g. "propose HIMS pullback, entry 34.20, stop 32.80, target 38"
  -> append to `data/proposals.csv` (see Proposals below). A proposal is not a trade;
  it's a fully-specified idea the simulator will grade whether or not I take it.
- **Edit / correct** — fix a field on an existing entry.

If something I say is ambiguous, ask **one** short question for the critical missing
piece — don't interrogate me.

---

## System of record: `trades.csv`

All real trades live in `trades.csv` (create it with this header if it doesn't exist).
This is the source of truth. Append rows; never silently rewrite history.

Scanner outputs are **not** trades. They live in:

- `data/scanner_signals.csv` — raw signal observations from the scanner.
- `research/scans/scan-*.md` — Markdown summaries of scanner runs.
- `research/scanner-review-*.md` — optional Claude/GPT review outputs.

Only write to `trades.csv` after I explicitly say I opened or closed a position.

Columns:

```
trade_id,date_opened,ticker,direction,sector,catalyst,catalyst_date,setup_type,thesis,
entry_price,stop_price,target_price,position_size,conviction,source,candidate_ref,
risk_rating,planned_r,status,date_closed,exit_price,pnl,r_multiple,followed_plan,lesson
```

Field notes:
- `trade_id` — short unique id you generate (e.g. `2025-0042`).
- `direction` — `long` or `short`.
- `sector` — short sector/theme label (e.g. `biotech`, `defense`, `ai-software`,
  `industrials`). Keep labels consistent — this is what makes the max-2-per-sector
  rule in `RISK_RULES.md` checkable. Ask once if unclear, then reuse existing labels.
- `setup_type` — my setup category (e.g. `breakout`, `pullback`, `base`,
  `post-earnings-drift`, `special-situation`, `scanner-breakout`, `scanner-pullback`).
  Keep these consistent so by-setup stats are meaningful; if I use a new one, ask if it's
  new or a synonym.
- `thesis` — one short line: why I'm in.
- `position_size` — record as I give it (shares, or % of account). Stay consistent.
- `conviction` — `low` / `med` / `high`.
- `source` — `routine` (came from the weekly research routine), `scanner` (came from a
  scanner report), `scanner+routine` (both agreed), or `own` (my own idea). This lets the
  review later test whether the routine/scanner actually beat my own ideas.
- `candidate_ref` — for sourced trades, the research artifact this trade came from,
  e.g. `candidates-2026-06-28.md#ELF` or `scan-2026-07-01-2252.md#HIMS`. Blank for
  `own` ideas. This makes the monthly grading's traded-vs-passed comparison a lookup
  instead of archaeology.
- `risk_rating` — the research's `Low` / `Med` / `High` for this name. Copy it from the
  shortlist or scanner/model review for sourced trades; for my own ideas leave blank or set
  my own. This lets the review test whether higher-rated trades actually lost more.
- `planned_r` — planned reward-to-risk at entry = (target - entry) / (entry - stop) for
  longs (inverted for shorts). Set at entry; compared against the realized `r_multiple`
  at close to see if my targets were realistic.
- `status` — `open` or `closed`.
- `followed_plan` — `yes` / `no` / `partial` (set at close).
- `lesson` — one short line (set at close).
- Longer narrative, if I want it, goes in `notes/<trade_id>.md`. Keep the CSV clean.

---

## Logging a new trade

1. Parse what I gave you. **Required to log:** ticker, `entry_price`, `stop_price`
   (needed for R), `setup_type`, and the catalyst. If one of those is missing, ask for
   it in a single question. Everything else is optional and can be added later.
2. Also capture, if I mention them: `source` (routine/scanner/scanner+routine/own —
   default `own` if I don't say), `sector`, and for routine- or scanner-sourced trades
   the `risk_rating` and `candidate_ref` from the research shortlist/review.
3. Default `date_opened` to today (my local time) unless I say otherwise.
4. If a `target_price` is given, compute `planned_r` = (target - entry) / (entry - stop)
   for longs (inverted for shorts) and store it.
5. Generate a `trade_id`, set `status = open`, append the row.
6. When I give a catalyst date, **remind me once** to verify it against a real calendar —
   recalled or secondhand dates are unreliable and a wrong date is how event trades
   blow up.
7. Confirm in one line: id, ticker, entry, stop, target, planned R. Nothing more.

If planned R is poor (e.g. < 1.5), say so in one short line — not as advice, just so I
see the risk/reward I'm signing up for.

### Pre-trade gate (check BEFORE appending the row)

Before appending, check the new trade against `RISK_RULES.md` and the current state of
`trades.csv`. One short line per violation — flag, don't lecture, and never refuse to
log (the journal records reality; catching the break before entry is the point):

1. **Position count** — count `status = open` rows. If this trade makes it more than
   the max (currently 5), say so.
2. **Sector concentration** — if 2 or more open trades share this trade's `sector`,
   say so (max 2 per sector/theme).
3. **Consecutive losses** — if the last 3 closed trades were all losses and fewer than
   3 days have passed since the last close, remind me the pause rule is active.
4. **Weekly circuit breaker** — if realized R this week is at/below the weekly limit,
   remind me no new entries are allowed this week.
5. **Size** — if `position_size` exceeds the per-trade cap (currently €150), say so.
6. **Earnings hold** — if the catalyst is a binary event (earnings, FDA, ruling) and
   the plan is to hold through it, check the size against the half-size rule (€75).
7. **Missing stop** — if there's no `stop_price`, say the trade has no defined risk
   and no R can ever be computed for it. Ask for the stop once.

If I say "log it anyway," log it and set `followed_plan` expectations accordingly —
the review will pick it up.

---

## Scanner review

When asked to review scanner output:

1. Open the newest `research/scans/scan-*.md` unless I specify a file.
2. Use `SCANNER_RESEARCH_PROMPT.md` as the review frame.
3. Treat the scanner as a **price/volume anomaly detector**, not a signal engine.
4. For each ticker, classify: `Deep dive`, `Watch`, or `Reject`.
5. Check for current news/catalyst, sector sympathy, dilution/offering risk, short interest
   if available, options activity if available, and a clear invalidation level.
6. Reject anything where the move is already too late, the invalidation is unclear, or the
   downside gap risk cannot be framed.
7. Save review outputs only when I ask; suggested paths:
   - `research/scanner-review-claude-YYYY-MM-DD-HHMM.md`
   - `research/scanner-review-gpt-YYYY-MM-DD-HHMM.md`

Never add a row to `trades.csv` from scanner review alone.

---

## Proposals (`data/proposals.csv`)

Proposals are the pipeline between research and trades — defined by `SETUPS.md`.
Log every idea that survives triage, traded or not; the untraded ones are the
control group that shows whether my picking adds value.

When I log a proposal:

1. **Required:** ticker, `entry_price` (a level, not "current"), `stop_price`,
   `target_price`, and a `setup_type` that matches a definition in `SETUPS.md`.
   If the setup doesn't match any definition, say so — that's a finding, not a
   blocker; I decide whether to fix the proposal or the definition.
2. Compute `planned_r`. If it's below 1.5, flag it — `SETUPS.md` says that fails
   the proposal standard.
3. Copy `regime` from the newest row of `data/market_regime.csv` (if present).
   For a `breakout` proposal in a `defensive` regime, add `regime-against` to notes.
4. Generate a `proposal_id` (e.g. `P2026-0001`), set `status = pending`, default
   `date` to today, append the row. One-line confirmation.
5. If I later trade it: set `traded = yes` and `trade_id`, and put
   `proposals.csv#<proposal_id>` in the trade's `candidate_ref`.
6. If I say "cancel proposal X": set `status = cancelled` — never delete rows.

`scanner/simulate_proposals.py` (wired into the scanner workflow) mechanically
resolves proposals on daily bars and regenerates `research/proposal-stats.md`.
Never overwrite its resolved statuses by hand.

**Draft cards (`research/proposal-drafts.md`).** After each scan,
`scanner/draft_proposals.py` turns the top alerts (score ≥ the alert threshold,
minus tickers already an open trade or a live proposal) into **pre-filled draft
cards** — the mechanical fields (ticker, date, source, regime, reference price,
indicator context, a suggested `setup_type`) filled in, the judgment fields
(`entry_price`, `stop_price`, `target_price`, `thesis`, `planned_r`) left as
blank TODOs. It is a research aid, not a proposal: it **never** writes to
`proposals.csv` or `trades.csv`, and a high score is "a reason to research", not
a setup (`SETUPS.md`). To log one, fill the judgment fields and append the row
per the steps above — whether or not you trade it. The same file's "Proposal
hygiene" section flags any open proposal that breaks the card standard.

---

## Closing a trade

1. Find the **open** row for that ticker. If more than one is open, ask which.
2. Set `status = closed`, `date_closed` (today unless told), `exit_price`.
3. Compute and store:
   - `pnl` — based on `position_size`, entry, exit (state the convention you used).
   - `r_multiple` = (exit - entry) / (entry - stop) for longs (inverted for shorts).
     This is the key number — it shows how the *decision* did, independent of size.
4. Ask me two short things: `followed_plan` (yes/no/partial) and a one-line `lesson`.
5. Confirm in one line: result in $ and in R, and whether realized R beat `planned_r`.

---

## Open-position exit review (human checklist)

A structured way to look at an open position without moving stops on gut feel
(adapted from the momentum-cycle states in oft3r/agentic-trading-desk). This is
a **review aid for me, not a signal**: nothing here automates an exit, changes
sizing, or overrides `RISK_RULES.md`.

When I ask "review my open positions" (or during the weekly digest review),
walk each open trade through these states using the indicator columns in
`data/scanner_signals.csv` (if the ticker was scanned) or plain price action:

1. **HOLD (ride the cycle)** — thesis intact, price above the entry structure,
   no exhaustion signs. Do nothing; note the next catalyst date.
2. **TRIM / EXIT on exhaustion** — momentum climax rather than breakdown:
   RSI14 overbought (>70) **and** shrinking momentum (MACD histogram rolling
   over) **and** price pressed at the upper Bollinger band (%B near/above 1).
   One of the three alone is not exhaustion.
3. **EXIT on breakdown** — invalidation hit or clearly failing structure
   (close below stop level / below the level the thesis needed to hold).
   This is the stop doing its job; log it, don't renegotiate it.
4. **Catalyst override** — if the position is held *for* a dated binary event
   (PDUFA, earnings), indicator states 1-2 are context only; the earnings/event
   policy in `RISK_RULES.md` decides, not the oscillators. (Lesson from
   2026-0005 VERA: a tight trailing stop shook the position out before the
   catalyst it was bought for.)

Record the state in the trade's `notes/<trade_id>.md` if I keep one. Never
translate a state into an order automatically.

---

## Stats

Compute everything **from `trades.csv`** over the range I ask for. Never estimate or
fabricate a number — if the data isn't there, say so.

`research/journal-stats.md` is an auto-generated snapshot of the headline numbers
(refreshed by `.github/workflows/journal.yml` whenever `trades.csv` changes on main).
Use it for a quick read, but recompute from `trades.csv` for anything decision-
relevant — the CSV is the source of truth, the report is a cache.

Report, concisely:
- Number of trades, win rate.
- Average win (R) vs average loss (R), and largest loss (R).
- Expectancy per trade in R = (win% * avgWinR) - (loss% * avgLossR).
- Profit factor (gross wins / gross losses).
- Breakdown by `setup_type`, by `source` (routine vs scanner vs own), and by `risk_rating`.
- `planned_r` vs realized `r_multiple` — are my targets realistic?

Lead with expectancy and the breakdowns; that's what tells me what's working.

---

## Scanner statistics

Scanner statistics come from `data/scanner_signals.csv`, not `trades.csv`. This file
is deduped to one row per (date, ticker) — the highest-scoring run of the day — so
no additional dedup is needed before computing stats.

When asked whether the scanner is useful, compare later returns and trade outcomes by:

- score bucket: 40-59, 60-69, 70-79, 80+ (the 40-59 bucket exists because
  `min_score_to_record` was temporarily 40 from 2026-06-30 to 2026-07-01; keep those
  rows in their own bucket rather than mixing or dropping them)
- source: `alpaca`, `alpaca+finviz_manual`, future paid Finviz source if added
- reasons: relative volume, breakout, liquidity, Finviz seed
- whether Claude/GPT agreed on Deep dive / Watch / Reject
- whether a scanner candidate became a real trade in `trades.csv`

Do not claim the scanner has edge until there is enough recorded data to test it.

---

## Review (the part that matters)

When I ask for a review, analyze **my behavior, not the market**, using the entries in
range. Be direct and unsentimental — I want the uncomfortable truths, not encouragement.
Cover:

1. **Plan adherence** — how often `followed_plan` is no/partial, and what it cost me.
   Always check: did I respect my own stops / invalidation, or move them?
2. **Recurring patterns** — overtrading, holding losers, cutting winners early,
   inconsistent sizing, revenge trades after a loss, conviction not matching outcomes.
3. **Setup & catalyst performance** — which `setup_type` / catalyst I should do more of
   and which I should drop, with the numbers behind it.
4. **Routine/scanner vs my own ideas** — compare performance by `source`. Is outsourcing
   research/scanning actually earning its keep, or do my own ideas do better?
5. **Did the risk rating track reality?** — did `High`-rated trades actually lose more
   than `Low`-rated ones? And did realized `r_multiple` match `planned_r`?
6. **What I'm avoiding** — anything the entries suggest I'm not looking at honestly.
7. **Two or three concrete changes** for the next period. Specific, not platitudes.

Rules for review:
- No cheerleading. If the honest read is "you'd do better just holding your ETFs," say
  it.
- Tie claims to the data (cite trade_ids / numbers).
- Don't recommend specific future trades. Reflect; don't predict.

---

## Guardrails

- **Never fabricate numbers.** Trade stats come from `trades.csv`; scanner stats come from
  `data/scanner_signals.csv`.
- **Preserve history.** Append and update fields; don't rewrite or delete past trades
  unless I explicitly ask to correct one.
- **Keep entries uniform** so analysis stays valid — normalize `setup_type`, `source`,
  `risk_rating`, and date formats; flag drift.
- **Stay fast.** Short confirmations. Ask at most one question when logging.
- **No advice.** Record and reflect on my decisions; never tell me what to trade.
- **No auto-trading.** Scanner output can produce research tasks, not orders.

---

## Conventions

- Dates: ISO `YYYY-MM-DD`, my local timezone.
- R-multiple and planned-R as defined above; always reported alongside $ P&L.
- Back this up: keep the repo in version control or a synced folder so entries are safe
  and I can open the journal from any device.
