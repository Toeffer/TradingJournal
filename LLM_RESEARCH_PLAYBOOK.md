# LLM Research Playbook — Swing-Trade Candidate Workflow

A model-assisted system for using large language models (Claude, ChatGPT, etc.) to prep
1–4 week swing-trade candidates when you don't have time to do all the research yourself.
Covers **US, European, and Asian** listed shares for manual research, with an optional
US-focused scanner layer for price/volume anomaly discovery.

**This is the model-agnostic layer.** The prompts below work in any research-enabled
model (Claude, ChatGPT, Gemini, etc.). The automated routine (`RESEARCH_BRIEF.md`) runs
on Claude Code; this playbook is for manual use and for cross-checking with a different
model. Keep them in sync — same intent, same constraints, same discipline.

**Not financial advice.** This is a research-and-triage workflow. You make every
trade decision. Treat the first few months as *measurement* (is this improving my
hit rate?), not income.

---

## The one idea that makes this work

LLMs gave you "BTC / Nvidia" because you asked them to *recall* what's promising now.
They can't — no live data + caution training = the most famous names in training data.

Split the work into two different jobs and never mix them in one prompt:

| Job | Who's good at it | What it needs |
|---|---|---|
| **Retrieval / screening** — what has a catalyst or anomaly in my window, liquid enough | Current data + search + optional scanner | NOT the model's memory |
| **Judgment / synthesis** — bull case, bear case, what invalidates this | The LLM (genuinely) | Specific names + context fed in |

So: use the model **with web/research turned on**, force it to find *current, dated*
catalysts, and ask it for *judgment*, not predictions. When scanner output exists, use it
as an anomaly-discovery input — not as proof. Then verify the facts yourself.

---

## Setup (one-time)

- Use a model with **web search / research mode enabled.** This is non-negotiable —
  without it you get stale, generic answers.
- Have a real **earnings calendar** open in another tab to verify dates (the model's
  recalled dates are unreliable).
- Keep `trades.csv` as the source of truth for actual trades.
- Optional scanner layer:
  - `scanner/run_scan.py` collects US price/volume anomalies.
  - `data/scanner_signals.csv` stores raw signal observations.
  - `research/scans/scan-*.md` stores Markdown reports.
  - `SCANNER_RESEARCH_PROMPT.md` is the Claude/GPT review prompt for scanner reports.

---

## Scanner layer — optional, not a signal engine

The scanner is a data-collection and discovery tool. It should never create trades by
itself.

Use it like this:

1. Let the scanner find unusual-volume / breakout names.
2. Use Finviz free/Elite as a discovery surface. Free Finviz is manual; copy names into
   `data/finviz_watchlist.csv`. Finviz Elite can later replace the manual seed step if it
   proves worth the cost.
3. Paste the latest `research/scans/scan-*.md` into Claude and GPT using
   `SCANNER_RESEARCH_PROMPT.md`.
4. Save useful reviews as `research/scanner-review-claude-YYYY-MM-DD-HHMM.md` and
   `research/scanner-review-gpt-YYYY-MM-DD-HHMM.md` if you want history.
5. Only log a trade in `trades.csv` after you personally decide to enter.

High scanner score = **research priority**, not buy signal.

---

## Continuity — giving the routine memory of last week

Each run starts cold (new session, fresh repo clone). To avoid re-reviewing the same
names and missing imminent catalysts, do this before running Prompt 1:

1. **Save last week's output.** After each Prompt 1 run, save the candidates to
   `research/candidates-YYYY-MM-DD.md` (create the `research/` directory if needed).
   Include ticker, catalyst, catalyst date, and your pass/watch/act verdict.

2. **Feed last week's file into the new run.** Before Prompt 1, open the most recent
   `research/candidates-*.md` and paste it into the prompt context (or attach the file
   if the model supports it). Add this instruction block before the main prompt:

```text
CONTINUITY — LAST WEEK'S CANDIDATES:

[paste or attach the previous candidates file]

Before generating new candidates:
- MARK REPEATS: if a name appeared last week and still qualifies, note it as
  "REPEAT" and say what changed (price moved, catalyst closer, new info).
- DROP EXPIRED: if a catalyst date has already passed, drop the name unless there's
  a new catalyst.
- FLAG ACT-NOW: if any remaining catalyst is within 7 calendar days, tag it "ACT-NOW"
  at the top of your output so I see it before anything else.
```

3. **Optional scanner continuity.** If scanner reports exist, attach or paste the latest
   one from `research/scans/`. Add this instruction before Prompt 1:

```text
SCANNER INPUT — PRICE/VOLUME ANOMALIES:

[paste latest research/scans/scan-*.md]

Treat these as anomaly seeds only. For each scanner name you carry forward, independently
verify current news/catalyst, sector sympathy, dilution/offering risk, liquidity, and a
clear invalidation level. Reject scanner names where the only reason is "it moved."
```

4. **Archive, don't delete.** Keep old candidates and scanner files — they feed the
   monthly self-grading routine (see `MONTHLY_SELF_GRADE.md`).

---

## PROMPT 1 — Weekly candidate discovery

Run this once a week. Fill the brackets first. Paste into a research-enabled model.
Include the continuity block above if you have previous candidates or scanner output.

```text
You are an experienced swing-trading research analyst. Use web search and cite
recent sources (flag anything older than 2 weeks). Today's date is [DATE].

TASK: Find me [5-8] swing-trade CANDIDATES with a specific, dated catalyst in the
next 1 to 4 weeks. I hold positions for days to a few weeks. I trade these myself —
you are surfacing candidates for me to research, not giving advice.

HARD CONSTRAINTS:
- Common shares listed on major US, European, or Asian exchanges. Accepted
  exchanges include (not exhaustive): NYSE, NASDAQ, LSE, XETRA, Euronext,
  SIX, TSE (Tokyo), HKEX, SGX, ASX, KRX.
- Market cap roughly [$500M] to [$10B] USD equivalent. Small and mid cap.
- EXCLUDE mega-caps, the "Magnificent 7," and the obvious AI/headline names.
  If a name is the first thing a generic list would mention, leave it out.
- Minimum liquidity: average daily dollar volume above [$10M] USD equivalent
  for US names, above [$5M] USD equivalent for European and Asian names
  (thinner markets, but still tradeable). Skip anything below the floor.
- The catalyst must be SPECIFIC and DATED (e.g., earnings on a known date, a product
  launch, FDA/regulatory decision, investor day, index rebalance, lockup expiry).
  "General momentum" is not a catalyst.
- Scanner candidates, if provided, are allowed as seeds, but must still pass all checks.
- For non-US names: state the exchange and the local currency. Note if the stock
  has a US-listed ADR as an alternative.

FOR EACH CANDIDATE, give me:
1. Ticker, exchange, currency, and one-line description of the company.
   (For non-US names, note if a US ADR exists.)
2. Source tag: routine / scanner_seed / routine+scanner_seed.
3. The catalyst and its exact date (or date window).
4. Why now — the current price setup in plain language (e.g., basing near support,
   breaking out of a range, pulling back in an uptrend).
5. Bull case — what goes right.
6. Bear case — what goes wrong, including downside-gap risk.
7. What would INVALIDATE the idea (the level or event that means "I'm wrong, get out").
8. Liquidity note (approx. avg daily dollar volume in USD equivalent).
9. Your confidence (low/med/high) and what specifically would raise it.

RULES:
- Do NOT pad the list with generic large-caps. If you can't find enough specific,
  current catalysts, give me fewer names and say so.
- Cite a recent source for each catalyst date.
- Reject scanner names that have no current reason beyond price movement.
- End by reminding me to independently verify every earnings/catalyst date, because
  your recalled dates can be wrong.

Format as a table or one clean block per candidate.
```

**After running it:** verify every date against your calendar, throw out anything you
can't confirm, and keep the 1–3 best setups on a watchlist. Don't act on the rest.
Save the output to `research/candidates-YYYY-MM-DD.md` so next week's run has memory.

---

## PROMPT 2 — Deep dive on one candidate (before you trade)

Run this on a single name once it's on your watchlist and the catalyst is near.

```text
You are a swing-trading analyst doing a pre-trade workup on [TICKER]. Use web search;
cite recent sources. Today is [DATE]. I am deciding whether to take a days-to-weeks
swing trade around [the catalyst, with date]. I trade this myself — give me analysis,
not advice.

Give me:
1. The catalyst mechanics — what exactly happens, when, and what the market already
   EXPECTS (consensus). I want to avoid trading something already priced in.
2. The bull case and the bear case, each in 3-4 specific points.
3. Key technical levels in plain terms: where support and resistance are, and a
   sensible level where the idea is clearly wrong. State levels in the local currency.
4. The main risk specific to this name (e.g., binary gap risk through earnings,
   thin float, dilution history, sector dependence).
5. For non-US names: any region-specific risks — FX headwinds/tailwinds relative to
   USD, local regulatory or political risk, settlement differences, restricted trading
   hours, or thin after-hours liquidity. If there's a US ADR, compare liquidity.
6. A PRE-MORTEM: assume I took this trade and lost money. What is the single most
   likely reason? What would I have ignored?
7. Position-sizing consideration: given the gap/binary risk (and FX risk for non-USD
   trades), what should I keep in mind about size? (Not a recommendation — just the
   risk framing.)

Be concrete. If something can't be known, say so rather than guessing.
```

**Key discipline:** if the pre-mortem reason is something you can't live with, that's
the trade telling you to size small or pass.

---

## PROMPT 3 — Weekly journal review (the part that builds the edge)

This is where you find out whether any of this actually works *for you*. Paste your
journal entries from the week.

```text
You are a trading coach reviewing my journal. Here are my trades and notes for the
period [dates]:

[paste your journal entries]

Analyze MY behavior, not the market. Specifically:
1. Recurring patterns — am I overtrading, holding losers too long, cutting winners
   early, ignoring my own invalidation levels, sizing inconsistently?
2. Where did following my plan help, and where did deviating hurt or help?
3. Is there a TYPE of setup or catalyst where I do better or worse?
4. Are routine-sourced, scanner-sourced, or my own ideas performing better?
5. Two or three concrete, specific things to change next week.

Be direct. I want the uncomfortable observations, not encouragement.
```

---

## Verification rules — what to NEVER trust without checking

LLMs are confident and sometimes wrong on specifics. Before risking money, you
personally confirm:

- **Earnings / catalyst dates** — against a real calendar. This is the #1 thing models
  get wrong, and acting on a wrong date is the classic event-trade blow-up.
- **Any number** (EPS, revenue, float, short interest, price level) — against a primary
  source. Models hallucinate figures.
- **Whether the catalyst already happened** — recency gaps are real, even with search.
- **That the name actually meets your liquidity floor** — check real volume yourself.
- **Scanner anomalies** — verify why the move happened. Relative volume is a clue, not a reason.

**Additional checks for non-US names:**
- **Exchange and ticker** — verify the exact exchange. Many European companies trade on
  multiple exchanges (e.g., Philips on Euronext Amsterdam vs XETRA) with different
  liquidity. Trade the most liquid listing.
- **Trading hours and holidays** — European and Asian exchanges have different trading
  hours and local holidays. A catalyst timed to a US event may land outside your
  market's hours, causing a gap open. Know when your exchange is open.
- **Currency** — confirm the listing currency. Some LSE stocks trade in GBX (pence),
  not GBP. Some HKEX stocks are denominated in HKD, others in CNH.
- **Settlement rules** — T+2 is standard in the US and EU, but some Asian markets
  differ (e.g., T+1 in India/China, T+2 in Japan/HK). Know when you actually receive
  shares and can sell.
- **ADR vs local** — if both exist, check which is more liquid and whether the ADR
  has a premium/discount. ADR fees (depositary charges) eat into returns on small
  positions.

If you can't verify it, you don't trade it.

---

## A realistic weekly rhythm (for a full-time job + family)

- **During the week, optional:** Let the scanner collect `research/scans/` and
  `data/scanner_signals.csv`. Do not screen-watch. Treat this as data collection.
- **Sunday, ~30 min:** Open last week's candidates file and latest scanner report, paste
  into continuity blocks, run Prompt 1. Verify dates. Pick 1–3 candidates to watch. Save
  output to `research/`.
- **Sunday, ~10 min extra:** Paste the candidates into a *different* model (e.g. ChatGPT)
  using the `SECOND_OPINION.md` red-team prompt. Where the two models **disagree** is
  exactly where you should dig hardest before trading.
- **Per candidate, ~10 min before entry:** Run Prompt 2. Decide pass / small / normal.
- **During the week, minimal:** Only act if your level/plan triggers. No screen-watching.
- **Weekend, ~10 min:** Update the journal. Run Prompt 3 every 2–4 weeks.

Total: still under an hour most weeks if you avoid watching every scanner alert. The
journal review is the part most people skip and the only part that tells you whether the
edge is real.

---

## Honest limitations

- The model surfaces *ideas*; it has no edge of its own. The edge, if any, is your
  judgment and discipline applied to a good shortlist.
- The scanner finds *anomalies*; it also has no edge until the journal proves that its
  scores predicted useful follow-through.
- Small-cap coverage is thin even with search — expect gaps and the occasional dud.
- **International coverage is thinner still.** LLM web search is biased toward
  English-language US financial media. European and Asian small/mid-caps get less
  coverage, so expect more gaps, stale data, and occasional wrong exchange/ticker
  mappings. Verify everything harder for non-US names.
- **FX adds a hidden variable.** A winning trade in local currency can be a losing
  trade in USD terms (and vice versa). The journal tracks both, but the research
  prompt doesn't forecast FX — that's your judgment call.
- This won't beat just holding your ETFs or BTC unless your decision-making genuinely
  adds value. The journal is how you find out, cheaply, before it costs much.
- Short volatility / binary catalysts cut both ways. Size so no single gap can hurt you.

---

## Grading the engine (optional, after one month)

After a month of live use, run the monthly self-grading routine described in
`MONTHLY_SELF_GRADE.md`. It looks back at old candidates files and records how each
name actually moved around its catalyst — grading the *discovery process* itself,
separate from your trading. This tells you whether the research playbook has any
signal before you bet more time or money on it.

For scanner grading, compare `data/scanner_signals.csv` by score bucket, Finviz seed
status, and whether Claude/GPT agreed on Deep dive / Watch / Reject.

---

## When to graduate to paid tooling

The natural upgrade is no longer "build a tool" — the first tool exists. Graduation now means:

1. The free/manual scanner has 30–60 days of observations.
2. Score 70+ names show better follow-through than lower-score names.
3. Claude/GPT agreement improves the shortlist.
4. The workflow does not cause overtrading.
5. Your account size makes the subscription cost reasonable.

Only then consider Finviz Elite or other paid data. Paid data should lower friction and
improve measurement; it should not be used to justify bigger trades.
