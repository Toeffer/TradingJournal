# SCANNER_RESEARCH_PROMPT.md — Claude/GPT Review Layer

Use this prompt after a scanner run produces `research/scans/scan-*.md`.

The scanner finds **price/volume anomalies**. The model review decides whether the anomaly deserves a deep dive.

```text
You are reviewing a TradingJournal pump-scanner report. This is research triage, not financial advice.
Today's date is [DATE]. My holding period is usually 1-10 trading days.

INPUT:
[paste the latest research/scans/scan-YYYY-MM-DD-HHMM.md]

TASK:
For each Top Alert and Watchlist Candidate, verify current context using web search.
Do not rely only on the scanner output.

For each ticker, return:
1. Verdict: Deep dive / Watch / Reject.
2. What likely caused the move: confirmed catalyst, sector sympathy, technical breakout, short squeeze, options/gamma possibility, or unknown.
3. Current catalyst check: earnings, FDA/regulatory, contract, index event, product launch, analyst action, macro/sector news, or none found.
4. Red flags: dilution/offering risk, reverse split history, weak liquidity/spread, already too extended, binary event risk, social-media pump risk, legal/accounting risk.
5. Setup quality: clean breakout / pullback candidate / too extended / failed move.
6. Clear invalidation level or event. If no clear invalidation exists, say Reject.
7. What would make me wait instead of chase.
8. For Deep dive verdicts only: a draft proposal card per SETUPS.md — usually a
   `pullback` (retest entry zone, stop, first target, planned R computed from the
   PULLBACK entry). If no acceptable pullback zone exists, say "no proposal — chase
   only," which means pass. Never draft a card that chases the day's move.

Rules:
- Cite current sources for every factual catalyst claim.
- Reject names where the move is already too late or the downside gap risk is unclear.
- Do not recommend position size except to say when a setup requires reduced size under RISK_RULES.md.
- End with a ranked list: 1-3 names for deep dive, 3-5 watch-only names, and rejects.
```

## How to use with two models

1. Run the same prompt in Claude and GPT.
2. Save outputs as:
   - `research/scanner-review-claude-YYYY-MM-DD-HHMM.md`
   - `research/scanner-review-gpt-YYYY-MM-DD-HHMM.md`
3. Prioritize overlap, but treat disagreement as the best place to investigate.
4. Log surviving proposal cards to `data/proposals.csv` (see SETUPS.md and AGENTS.md) —
   traded or not, so the pipeline gets graded on everything it produces.
5. Only log an actual trade in `trades.csv` after you make the decision yourself.
