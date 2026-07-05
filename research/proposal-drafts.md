# Proposal Drafts

Auto-generated from the latest scanner alerts. **Not proposals, not
trades, not advice** — pre-filled scaffolding so logging a real proposal
into `data/proposals.csv` is fast. Nothing here enters proposals.csv or
trades.csv automatically; the entry, stop, target and thesis are yours.
Regenerated every scan run — never edit this file by hand.

Latest scan day: **2026-07-03** · alert threshold: score ≥ 70 · regime: **supportive**

## Draft cards

### RIVN — scanner score 80 (US)

**Reason to research — NOT a proposal yet.** Fill the judgment fields below, then log it into `data/proposals.csv` if it survives triage.

_Auto-filled (mechanical — do not treat as a recommendation):_
- `date`: 2026-07-03 | `direction`: long | `source`: scanner
- `candidate_ref`: scanner_signals.csv#2026-07-03:RIVN
- `regime`: supportive (newest data/market_regime.csv)
- reference price: 18.62 — intraday snapshot, **NOT** an entry level
- context (not scored): RSI14 n/a | vs EMA20 n/a | vs EMA50 n/a | BB %B n/a | 20d-high: true
- day move 8.5082% | rel vol 7.4223x | 5d extension 4.6361%
- suggested `setup_type`: **pullback** — SETUPS.md's default for a scanner mover (buy the retest, don't chase). Change if a different setup fits.

_You must decide (a proposal missing any of these is rejected):_
- [ ] `entry_price`: ______  (a LEVEL where the setup triggers, not "current")
- [ ] `stop_price`: ______  (invalidation — no stop, no proposal, ever)
- [ ] `target_price`: ______  (realistic first target, not the dream case)
- [ ] `planned_r` = (target − entry) / (entry − stop) — **must be ≥ 1.5**
- [ ] `thesis`: ______  (one line: why this, why now)
- [ ] `catalyst` / `catalyst_date`: ______  (if catalyst-driven; verify the date)

### HOOD — scanner score 70 (US)

**Reason to research — NOT a proposal yet.** Fill the judgment fields below, then log it into `data/proposals.csv` if it survives triage.

_Auto-filled (mechanical — do not treat as a recommendation):_
- `date`: 2026-07-03 | `direction`: long | `source`: scanner
- `candidate_ref`: scanner_signals.csv#2026-07-03:HOOD
- `regime`: supportive (newest data/market_regime.csv)
- reference price: 112.71 — intraday snapshot, **NOT** an entry level
- context (not scored): RSI14 n/a | vs EMA20 n/a | vs EMA50 n/a | BB %B n/a | 20d-high: true
- day move 3.7081% | rel vol 4.2306x | 5d extension 2.9127%
- suggested `setup_type`: **pullback** — SETUPS.md's default for a scanner mover (buy the retest, don't chase). Change if a different setup fits.

_You must decide (a proposal missing any of these is rejected):_
- [ ] `entry_price`: ______  (a LEVEL where the setup triggers, not "current")
- [ ] `stop_price`: ______  (invalidation — no stop, no proposal, ever)
- [ ] `target_price`: ______  (realistic first target, not the dream case)
- [ ] `planned_r` = (target − entry) / (entry − stop) — **must be ≥ 1.5**
- [ ] `thesis`: ______  (one line: why this, why now)
- [ ] `catalyst` / `catalyst_date`: ______  (if catalyst-driven; verify the date)

## Proposal hygiene (existing proposals.csv)

No proposals logged yet — nothing to validate.

---
To log a draft: append one row to `data/proposals.csv` with a new
`proposal_id` (e.g. `P2026-0001`) and `status = pending`. See AGENTS.md
→ "Proposals". Log it whether or not you trade it — the untraded ones are
the control group.
