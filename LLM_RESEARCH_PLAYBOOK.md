# LLM Research Playbook — Swing-Trade Candidate Workflow

A no-build system for using large language models (Claude, ChatGPT, etc.) to prep
1–4 week swing-trade candidates when you don't have time to do the research yourself.

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

## PROMPT 1 — Weekly candidate discovery

Run this once a week. Fill the brackets first. Paste into a research-enabled model.

```
You are an experienced swing-trading research analyst. Use web search and cite
recent sources (flag anything older than 2 weeks). Today's date is [DATE].

TASK: Find me [5-8] swing-trade CANDIDATES with a specific, dated catalyst in the
next 1 to 4 weeks. I hold positions for days to a few weeks. I trade these myself —
you are surfacing candidates for me to research, not giving advice.

HARD CONSTRAINTS:
- US-listed common shares only.
- Market cap roughly [$500M] to [$10B]. Small and mid cap.
- EXCLUDE mega-caps, the "Magnificent 7," and the obvious AI/headline names.
  If a name is the first thing a generic list would mention, leave it out.
- Minimum liquidity: average daily dollar volume above [$10M]. Skip illiquid names.
- The catalyst must be SPECIFIC and DATED (e.g., earnings on a known date, a product
  launch, FDA/regulatory decision, investor day, index rebalance, lockup expiry).
  "General momentum" is not a catalyst.

FOR EACH CANDIDATE, give me:
1. Ticker and one-line description of the company.
2. The catalyst and its exact date (or date window).
3. Why now — the current price setup in plain language (e.g., basing near support,
   breaking out of a range, pulling back in an uptrend).
4. Bull case — what goes right.
5. Bear case — what goes wrong, including downside-gap risk.
6. What would INVALIDATE the idea (the level or event that means "I'm wrong, get out").
7. Liquidity note (approx. avg daily dollar volume).
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
   sensible level where the idea is clearly wrong.
4. The main risk specific to this name (e.g., binary gap risk through earnings,
   thin float, dilution history, sector dependence).
5. A PRE-MORTEM: assume I took this trade and lost money. What is the single most
   likely reason? What would I have ignored?
6. Position-sizing consideration: given the gap/binary risk, what should I keep in
   mind about size? (Not a recommendation — just the risk framing.)

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

If you can't verify it, you don't trade it.

---

## A realistic weekly rhythm (for a full-time job + family)

- **Sunday, ~30 min:** Run Prompt 1. Verify dates. Pick 1–3 candidates to watch.
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
- This won't beat just holding your ETFs unless your decision-making genuinely adds
  value. The journal is how you find out, cheaply, before it costs much.
- Short volatility / binary catalysts cut both ways. Size so no single gap can hurt you.

---

## When to graduate to a tool

Once this manual flow has proven it helps, the natural upgrade (ties to your
`AGENTS.md`): let a small screener do the **retrieval** job — pull the universe, find
catalysts in the window, apply the liquidity floor — and hand the shortlist to an LLM
(via API) for the **judgment** layer using Prompt 2's structure. Build that only after
the manual version earns it. Manual first costs nothing and tells you if it's worth it.
