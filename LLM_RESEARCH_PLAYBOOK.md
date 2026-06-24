# LLM Research Playbook — Swing-Trade Candidate Workflow

A no-build system for using large language models (Claude, ChatGPT, etc.) to prep
1–4 week swing-trade candidates when you don't have time to do the research yourself.
Covers **US, European, and Asian** listed shares.

**Not financial advice.** This is a research-and-triage workflow. You make every
trade decision. Treat the first few months as *measurement* (is this improving my
hit rate?), not income.

**This playbook is the model-agnostic layer.** Everything here runs in ChatGPT, Claude,
Gemini, or any research-enabled model — it is plain prompts, not a tool. The automated
`RESEARCH_BRIEF.md` routine is the *Claude-side* engine that produces
`candidates/CANDIDATES_<date>.md`; this file is the *manual + second-model* layer that
sits around it. Keep the two in sync in intent (same universe, same catalyst discipline,
same "verify every date" rule). The highest-value habit added here is the **second
opinion**: run the routine's shortlist past a *different* model (see
`SECOND_OPINION.md`) so its blind spots aren't correlated with the first model's.

---

## The one idea that makes this work

LLMs gave you "BTC / Nvidia" because you asked them to *recall* what's promising now.
They can't — no live data + caution training = the most famous names in training data.

Split the work into two different jobs and never mix them in one prompt:

| Job | Who's good at it | What it needs |
|---|---|---|
| **Retrieval / screening** — what has a catalyst in my window, in my universe, liquid enough | Current data + search | NOT the model's memory |
| **Judgment / synthesis** — bull case, bear case, what invalidates this | The LLM (genuinely) | Specific names + context fed in |

So: use the model **with web/research turned on**, force it to find *current, dated*
catalysts, and ask it for *judgment*, not predictions. Then verify the facts yourself.

---

## Setup (one-time)

- Use a model with **web search / research mode enabled.** This is non-negotiable —
  without it you get stale, generic answers.
- Have a real **earnings calendar** open in another tab to verify dates (the model's
  recalled dates are unreliable).
- Keep a simple **journal** (a spreadsheet is fine): date, ticker, catalyst, why you
  entered, entry/stop/target, size, outcome, and one lesson.

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

```
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

3. **Archive, don't delete.** Keep old candidates files — they feed the monthly
   self-grading routine (see `MONTHLY_SELF_GRADE.md`).

---

## PROMPT 1 — Weekly candidate discovery

Run this once a week. Fill the brackets first. Paste into a research-enabled model.
Include the continuity block above if you have a previous candidates file.

```
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
- For non-US names: state the exchange and the local currency. Note if the stock
  has a US-listed ADR as an alternative.

FOR EACH CANDIDATE, give me:
1. Ticker, exchange, currency, and one-line description of the company.
   (For non-US names, note if a US ADR exists.)
2. The catalyst and its exact date (or date window).
3. Why now — the current price setup in plain language (e.g., basing near support,
   breaking out of a range, pulling back in an uptrend).
4. Bull case — what goes right.
5. Bear case — what goes wrong, including downside-gap risk.
6. What would INVALIDATE the idea (the level or event that means "I'm wrong, get out").
7. Liquidity note (approx. avg daily dollar volume in USD equivalent).
8. Your confidence (low/med/high) and what specifically would raise it.

RULES:
- Do NOT pad the list with generic large-caps. If you can't find enough specific,
  current catalysts, give me fewer names and say so.
- Cite a recent source for each catalyst date.
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

```
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

```
You are a trading coach reviewing my journal. Here are my trades and notes for the
period [dates]:

[paste your journal entries]

Analyze MY behavior, not the market. Specifically:
1. Recurring patterns — am I overtrading, holding losers too long, cutting winners
   early, ignoring my own invalidation levels, sizing inconsistently?
2. Where did following my plan help, and where did deviating hurt or help?
3. Is there a TYPE of setup or catalyst where I do better or worse?
4. Two or three concrete, specific things to change next week.

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

## Second opinion — red-team the shortlist with a different model

A second model is valuable only when it *challenges* the shortlist rather than re-running
it. A different model's mistakes aren't correlated with the first model's, so where the
two **disagree** is the signal — that's where to dig hardest before risking money.

- After the routine writes `candidates/CANDIDATES_<date>.md` (or after you run Prompt 1),
  paste that file into a **different** model along with the prompt in `SECOND_OPINION.md`.
- That prompt makes the second model attack each name: strongest bear case, what's already
  priced in, the single invalidating fact (and whether it's knowable *before* the
  catalyst), an independent catalyst/date check, and a PASS / WORTH-A-LOOK verdict.
- Treat **disagreement between the two models** as a flag, not a tiebreaker: if the second
  model calls a name uninvestable or can't verify its catalyst, that's your cue to verify
  harder or drop it — never to size up.
- This sharpens *reasoning*, not data. It does not fix a wrong web-sourced date — keep the
  `DATE_VERIFIED: NO` discipline and confirm every date yourself regardless.

---

## A realistic weekly rhythm (for a full-time job + family)

- **Sunday, ~30 min:** Open last week's candidates file, paste into continuity block,
  run Prompt 1 (or let the `RESEARCH_BRIEF.md` routine produce the shortlist). Verify
  dates. Pick 1–3 candidates to watch. Save output to `research/`.
- **Sunday, ~10 min:** Red-team the shortlist with a second model using `SECOND_OPINION.md`.
  Where the two models disagree, dig hardest before trading.
- **Per candidate, ~10 min before entry:** Run Prompt 2. Decide pass / small / normal.
- **During the week, minimal:** Only act if your level/plan triggers. No screen-watching.
- **Weekend, ~10 min:** Update the journal. Run Prompt 3 every 2–4 weeks.

Total: well under an hour most weeks. The journal review is the part most people skip
and the only part that tells you whether the edge is real.

---

## Honest limitations

- The model surfaces *ideas*; it has no edge of its own. The edge, if any, is your
  judgment and discipline applied to a good shortlist.
- Small-cap coverage is thin even with search — expect gaps and the occasional dud.
- **International coverage is thinner still.** LLM web search is biased toward
  English-language US financial media. European and Asian small/mid-caps get less
  coverage, so expect more gaps, stale data, and occasional wrong exchange/ticker
  mappings. Verify everything harder for non-US names.
- **FX adds a hidden variable.** A winning trade in local currency can be a losing
  trade in USD terms (and vice versa). The journal tracks both, but the research
  prompt doesn't forecast FX — that's your judgment call.
- This won't beat just holding your ETFs unless your decision-making genuinely adds
  value. The journal is how you find out, cheaply, before it costs much.
- Short volatility / binary catalysts cut both ways. Size so no single gap can hurt you.

---

## Grading the engine (optional, after one month)

After a month of live use, run the monthly self-grading routine described in
`MONTHLY_SELF_GRADE.md`. It looks back at old candidates files and records how each
name actually moved around its catalyst — grading the *discovery process* itself,
separate from your trading. This tells you whether the research playbook has any
signal before you bet more time or money on it.

---

## When to graduate to a tool

Once this manual flow has proven it helps, the natural upgrade (ties to your
`AGENTS.md`): let a small screener do the **retrieval** job — pull the universe, find
catalysts in the window, apply the liquidity floor — and hand the shortlist to an LLM
(via API) for the **judgment** layer using Prompt 2's structure. Build that only after
the manual version earns it. Manual first costs nothing and tells you if it's worth it.
