# Monthly Self-Grade — Grading the Discovery Engine

This routine grades the **research playbook itself**, separate from your trading.
The question it answers: "Does the candidate discovery process have any signal, or
am I just generating busywork?"

**Add this only after a month of live use.** You need at least 4 weekly candidate
files and ideally some trades to compare against.

**Not financial advice.** This is measurement of a process, not a trading strategy.

---

## What you need

- The archived `research/candidates-*.md` files from the past month (this is why the
  playbook says to save them).
- Access to a chart or price-data source to look up what actually happened around each
  catalyst date.
- ~30 minutes once a month.

---

## The grading process

For each candidate file from the past month:

### 1. Record the outcome

For every candidate that was surfaced, look up what actually happened:

```
| Ticker | Catalyst date | Price at discovery | Price at catalyst | Move % | Direction called? | Traded? |
|--------|--------------|-------------------|------------------|--------|------------------|---------|
```

- **Move %** — from discovery price to the close on catalyst day (or +2 days if the
  catalyst was after-hours).
- **Direction called?** — did the bull/bear framing match what happened? `yes` / `no` / `mixed`.
- **Traded?** — did you actually take the trade? `yes` / `no` / `watched` / `missed`.

### 2. Compute discovery-level stats

These grade the *engine*, not you:

- **Hit rate** — what % of surfaced candidates moved favorably (in the direction the
  bull case implied) by more than 3% around their catalyst?
- **Average favorable move** vs **average adverse move** — is the engine surfacing
  names with asymmetric outcomes, or are the misses as big as the hits?
- **Repeat quality** — for names flagged as REPEAT across weeks, did persistence
  correlate with a better outcome? (i.e., was the routine right to keep surfacing them?)
- **ACT-NOW accuracy** — for names flagged ACT-NOW (catalyst within 7 days), what was
  the hit rate? These are the highest-urgency calls.

### 3. Compare against your actual trades

Cross-reference with `trades.csv` (filter by `source = routine`):

- **Conversion rate** — what % of surfaced candidates did you actually trade?
- **Selection quality** — did the candidates you *chose* to trade perform better or
  worse than the ones you passed on? If the passes did better, your picker isn't
  adding value on top of the engine.
- **Missed opportunity** — list candidates you didn't trade that moved significantly.
  Is there a pattern in what you skip?

### 4. Grade the engine

Based on the above, assign an honest grade:

- **A** — the discovery process surfaces names with genuine edge; your traded subset
  does better than random picks from the list.
- **B** — the process surfaces reasonable candidates but you can't yet tell if it beats
  your own idea generation.
- **C** — the candidates are fine but no better than what you'd find yourself; the
  routine is costing time without clear payoff.
- **D** — the candidates are actively misleading (wrong catalyst dates, priced-in
  events, poor setups) and you'd be better off without them.

### 5. Save the grading report

Save to `research/grade-YYYY-MM.md` so you can track the engine's performance over
time. Include the raw data table and your grade.

---

## What to do with the grade

- **A or B:** keep running the playbook. Consider tightening constraints (narrower
  market cap, higher liquidity floor) to improve signal.
- **C:** run for one more month with adjusted prompts before deciding. Check if the
  issue is the discovery or your candidate selection.
- **D:** stop the routine. Go back to your own ideas and compare your `source = own`
  performance in the journal. The playbook isn't helping.

---

## Honest limitations of this grading

- **After-the-fact price data is rough.** You're looking up closes, not intraday
  action. A stock that gapped down 8% then recovered to −1% scores as a small miss
  even though it would have stopped you out.
- **Small sample sizes.** One month of 5–8 candidates per week is ~20–30 data points.
  Don't over-interpret. Look for patterns, not precise numbers.
- **Survivorship in your trades.** You only traded the ones that looked best, so
  comparing traded vs passed is biased. The "missed opportunity" analysis partially
  corrects for this, but it's not perfect.

Do this for 3+ months before making any strong conclusions about the engine.
