# MASTERPLAN.md — The Long Game

Where this system is going, written down **before** the results exist, so decisions
get made by gates and data instead of by mood after a hot or cold streak.

Rules of this document:

- Each phase has **entry gates** (numeric, computed from the journal). No gate, no
  promotion — however good the last month felt.
- **Demotion is automatic**: hit a demotion trigger and you drop back one phase and
  its sizing, no debate.
- The plan can be edited, but only between phases and only with a changelog entry —
  never mid-drawdown, never mid-euphoria.
- Every phase keeps the same constitution: the journal measures everything, no
  advice, no auto-trading without an explicit phase gate, human decides.

**Not financial advice. This is a personal process roadmap.**

---

## Phase 0 — Foundation (NOW)

Everything is built; almost nothing is proven. The only job is **volume of
measured decisions**.

Focus:
- Trade small (€150 fixed, per `RISK_RULES.md`). Every trade fully recorded —
  stop, setup_type, sector, followed_plan, lesson. No exceptions; the data gaps
  list in `research/journal-stats.md` must trend to zero.
- Log proposals for everything that survives triage (`SETUPS.md`), traded or not.
- Let the scanner/backfill/simulation loops accumulate.

**Exit gates (all required):**
- ≥ 30 closed trades with computable R
- ≥ 20 resolved proposals in `research/proposal-stats.md`
- Scanner 30-day evaluation done (score buckets vs forward returns)
- Zero open data gaps for 4 consecutive weekly digests

## Phase 1 — Prove or kill each pipeline

The pipelines (scanner, weekly routine, own ideas) currently all *feel* useful.
Phase 1 makes each one earn its place — or die.

Focus:
- **Scanner:** do 70+ scores beat 60-69 and 40-59 on forward returns? If buckets
  don't separate, the score has no edge → either fix the inputs (this is where the
  Finviz Elite / Alpaca SIP data-upgrade decision belongs) or kill the scanner.
- **Routine:** grade monthly per `MONTHLY_SELF_GRADE.md`. Two consecutive C grades
  or one D → stop the routine, keep only what the grade says works.
- **Setups:** any setup with negative expectancy after n ≥ 10 gets suspended from
  proposals (it can be re-proposed in a phase transition with a written fix).
- **The picker test:** if `passed` beats `traded` in proposal-stats, the fix is
  behavioral, not technical — trade closer to the mechanical cards.

**Exit gates:**
- ≥ 50 closed trades total; overall expectancy > 0R over the trailing 30
- At least one setup with positive expectancy at n ≥ 10
- Every surviving pipeline has data justifying its existence (kill decisions count
  as passing — a smaller, proven system beats a bigger, unproven one)
- 8 consecutive weeks without a rule breach in the journal-stats flags

## Phase 2 — Size by risk, not by fixed euros

Graduation from "every trade €150" to "every trade risks the same fraction of the
account" — the future rule already sketched in `RISK_RULES.md`.

Focus:
- Risk-based sizing: shares = (account × risk%) / (entry − stop), starting at
  **0.5% risk per trade**, raising to 1% only after 20 more clean trades.
- Only setups that survived Phase 1 get proposed at all.
- Conviction-based size tiers ONLY if Phase 1 data shows conviction actually
  correlated with outcomes (check the journal; if `high` conviction didn't earn
  more R than `low`, conviction stays a diary field, not a sizing input).
- Regime-scaled exposure: in `defensive` regime, max open positions drops (e.g.
  5 → 3) and breakout proposals require an explicit override note.

**Demotion triggers (back to Phase 1 sizing):**
- −6R drawdown from equity peak, or
- 2 rule breaches in a month, or
- expectancy over trailing 30 trades goes negative

## Phase 3 — Systematize the winners

Turn the best-performing setup into a semi-mechanical playbook that runs with
minimal discretion — the human approves, the machine prepares.

Candidates for automation (in order):
1. Auto-draft proposal cards from scanner Deep-dives (machine fills the card,
   human approves/edits/rejects — approval is the trade decision).
2. Price alerts at proposal entry zones (broker alerts), so pullback entries
   don't require screen-watching.
3. A pre-earnings calendar sweep that flags open positions 10 days before any
   earnings date automatically.

**Hard line that stays in place: no order is ever placed by a machine in this
phase.** If a future phase ever proposes auto-execution, it happens in a separate
system (see Boundaries below), never in this repo.

**Exit gates:** 100+ closed trades, 12+ months of history, positive expectancy in
at least 2 distinct regimes (so the edge isn't just one market mood).

## Phase 4 — Scale and diversify

Only reachable with a multi-regime, multi-setup track record.

- Second strategy sleeve with different rhythm (e.g. post-earnings-drift as a
  slower systematic sleeve next to discretionary momentum) — measured under its
  own `source` tag from day one.
- Possibly: shorts (only with a written setup definition first), European names
  (the journal already handles them), larger account allocation.
- Revisit every data subscription against measured value per euro.

---

## Standing meta-rules (all phases)

- **The ETF question, quarterly:** compare total journal P&L (including time
  spent, honestly valued) against just holding a world ETF for the same period.
  The journal review must state the answer plainly. Two consecutive years of
  losing to the benchmark = the honest end state is "index and enjoy life" —
  written here now so future-you has to argue with present-you to ignore it.
- **Complexity budget:** one new mechanism (indicator, data source, rule) may be
  added per phase, and only by replacing or killing something. The system's edge
  is discipline and measurement, not sophistication.
- **What is permanently out:** leverage/CFDs beyond plain stock positions,
  averaging down as a "strategy", moving stops away from price, ML black-box
  signals before there are ~500 trades to validate on, and anything that can't
  state its invalidation in one sentence.
- **Boundaries with other systems:** this repo measures; it never executes. If a
  bot (e.g. Trading_Bot) ever trades the same account, its fills enter
  `trades.csv` tagged `source=bot` and get judged by the same R math as the human.
  No shared credentials, no shared execution code.

## Idea backlog (parked, not scheduled)

Things worth testing *someday*, recorded so they stop occupying headspace:

- ATR-based stops instead of level-based (test against realized stop-out quality)
- Time stops: exit if the thesis hasn't moved within N days (the journal can
  already measure how long winners vs losers take)
- Partial profit-taking at +1R (test: does it raise or lower expectancy?)
- Slippage tracking: record intended vs actual fill in trades.csv notes
- Sector-momentum ranking to tilt the scanner universe
- Form 4 insider cluster-buy screener as a discovery input (EDGAR is free; slots
  in where the Finviz seeds do) — build ONLY if the `insider-cluster` proposal
  tag shows measurable value first; insider *selling* stays a triage red flag,
  and politician/STOCK-Act feeds stay out (30-45 day lag kills timing value)
- FX overlay decision once average position size crosses ~€1,000
- Earnings-season calendar playbook (density of catalysts ≠ density of edges)
- A quarterly "red-team" pass where SECOND_OPINION.md is run against the
  masterplan itself, not just against candidates

## Changelog

| Date | Change | Why |
|------|--------|-----|
| 2026-07-02 | Initial masterplan: phases 0-4, gates, demotion triggers, meta-rules, backlog | Write the long game down before results exist, so gates beat moods |
