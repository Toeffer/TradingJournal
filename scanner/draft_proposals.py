#!/usr/bin/env python3
"""Draft proposal cards from the latest scanner alerts — a research aid.

WHY THIS EXISTS
data/proposals.csv is the control group (SETUPS.md): every idea that survives
triage, logged whether traded or not, so the journal can measure whether the
human's picking adds value. It stays empty when logging a card by hand is too
much friction. This script removes the friction for the *mechanical* half of a
card and leaves the *judgment* half explicitly blank.

WHAT IT IS NOT
- It does NOT write to data/proposals.csv. Logging a proposal stays a human
  decision (AGENTS.md: "human decides"); this only writes a draft file.
- It does NOT write to trades.csv and is never a trade signal.
- It does NOT fill entry/stop/target/thesis. SETUPS.md is explicit that a high
  scanner score is "a reason to research", not a setup; the invalidation level
  and targets are the human's judgment and are left as TODO on every card.
- It does NOT jump the Phase 3 automation gate (MASTERPLAN): approval here is
  not a trade decision — the human still writes the risk levels and logs the
  card into proposals.csv through the normal flow.

Derived artifact: research/proposal-drafts.md is regenerated on every scan run.
Never edit it by hand; edit the card you copy into proposals.csv instead.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_scan import REPO_ROOT, load_config  # noqa: E402

SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
REGIME_CSV = REPO_ROOT / "data/market_regime.csv"
PROPOSALS_CSV = REPO_ROOT / "data/proposals.csv"
TRADES_CSV = REPO_ROOT / "trades.csv"
DRAFTS_MD = REPO_ROOT / "research/proposal-drafts.md"

# The paper control-group setups a scanner mover can legitimately become.
VALID_SETUPS = {"breakout", "pullback", "post-earnings-drift", "special-situation"}
# Proposal states that still occupy a ticker (skip drafting a duplicate).
LIVE_PROPOSAL_STATES = {"pending", "triggered"}


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def latest_regime() -> str:
    rows = load_csv(REGIME_CSV)
    return rows[-1].get("regime", "") if rows else ""


def parse_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def already_covered(signals_tickers: set[str]) -> set[str]:
    """Tickers to skip: an open trade or a live proposal already exists."""
    covered: set[str] = set()
    for t in load_csv(TRADES_CSV):
        if t.get("status") == "open" and t.get("ticker"):
            covered.add(t["ticker"].strip().upper())
    for p in load_csv(PROPOSALS_CSV):
        if p.get("status", "").strip().lower() in LIVE_PROPOSAL_STATES and p.get("ticker"):
            covered.add(p["ticker"].strip().upper())
    return covered & signals_tickers


def latest_scan_date(signals: list[dict[str, str]]) -> str | None:
    dates = [s.get("timestamp", "")[:10] for s in signals if s.get("timestamp")]
    return max(dates) if dates else None


def draft_candidates(config: dict[str, Any]) -> tuple[list[dict[str, str]], str | None, str]:
    """Alert-worthy signals from the most recent scan day, minus already-covered
    tickers. Returns (candidates, scan_date, regime)."""
    signals = load_csv(SIGNALS_CSV)
    if not signals:
        return [], None, ""
    scan_date = latest_scan_date(signals)
    alert = int(config["scanner"].get("min_score_to_alert", 70))
    max_rows = int(config["scanner"].get("max_candidates_per_report", 10))

    todays = [
        s for s in signals
        if s.get("timestamp", "")[:10] == scan_date
        and (parse_float(s.get("score")) or 0) >= alert
    ]
    covered = already_covered({s["ticker"].strip().upper() for s in todays})
    fresh = [s for s in todays if s["ticker"].strip().upper() not in covered]
    fresh.sort(key=lambda s: parse_float(s.get("score")) or 0, reverse=True)
    return fresh[:max_rows], scan_date, latest_regime()


def fmt(value: str | None, suffix: str = "") -> str:
    v = parse_float(value)
    return "n/a" if v is None else f"{v:g}{suffix}"


def card(sig: dict[str, str], regime: str) -> list[str]:
    ticker = sig["ticker"].strip().upper()
    market = sig.get("market", "US")
    score = sig.get("score", "")
    ref_price = fmt(sig.get("price"))
    regime_flag = ""
    # Doctrine: a breakout logged in defensive tape is flagged regime-against
    # (SETUPS.md). The scanner mover is breakout-shaped, so surface the flag.
    if regime == "defensive":
        regime_flag = "  ⚠️ defensive regime → a breakout here must be flagged `regime-against`"

    lines = [
        f"### {ticker} — scanner score {score} ({market})",
        "",
        "**Reason to research — NOT a proposal yet.** Fill the judgment fields below,"
        " then log it into `data/proposals.csv` if it survives triage.",
        "",
        "_Auto-filled (mechanical — do not treat as a recommendation):_",
        f"- `date`: {sig.get('timestamp', '')[:10]} | `direction`: long | `source`: scanner",
        f"- `candidate_ref`: scanner_signals.csv#{sig.get('timestamp','')[:10]}:{ticker}",
        f"- `regime`: {regime or 'n/a'} (newest data/market_regime.csv){regime_flag}",
        f"- reference price: {ref_price} — intraday snapshot, **NOT** an entry level",
        f"- context (not scored): RSI14 {fmt(sig.get('rsi14'))} | vs EMA20 "
        f"{fmt(sig.get('ema20_dist_pct'), '%')} | vs EMA50 {fmt(sig.get('ema50_dist_pct'), '%')} | "
        f"BB %B {fmt(sig.get('bb_percent_b'))} | 20d-high: {sig.get('above_20d_high','')}",
        f"- day move {fmt(sig.get('change_pct'), '%')} | rel vol {fmt(sig.get('rel_volume'), 'x')}"
        f" | 5d extension {fmt(sig.get('extension_5d_pct'), '%')}",
        "- suggested `setup_type`: **pullback** — SETUPS.md's default for a scanner"
        " mover (buy the retest, don't chase). Change if a different setup fits.",
        "",
        "_You must decide (a proposal missing any of these is rejected):_",
        "- [ ] `entry_price`: ______  (a LEVEL where the setup triggers, not \"current\")",
        "- [ ] `stop_price`: ______  (invalidation — no stop, no proposal, ever)",
        "- [ ] `target_price`: ______  (realistic first target, not the dream case)",
        "- [ ] `planned_r` = (target − entry) / (entry − stop) — **must be ≥ 1.5**",
        "- [ ] `thesis`: ______  (one line: why this, why now)",
        "- [ ] `catalyst` / `catalyst_date`: ______  (if catalyst-driven; verify the date)",
        "",
    ]
    return lines


def validate_proposals() -> list[str]:
    """Flag existing proposals that break the SETUPS.md card standard, so the
    control-group data stays clean for later evaluation. Read-only."""
    rows = load_csv(PROPOSALS_CSV)
    if not rows:
        return ["No proposals logged yet — nothing to validate."]
    issues: list[str] = []
    seen_ids: set[str] = set()
    for r in rows:
        pid = (r.get("proposal_id") or "?").strip()
        if pid in seen_ids:
            issues.append(f"- `{pid}`: duplicate proposal_id.")
        seen_ids.add(pid)
        if r.get("status", "").strip().lower() not in LIVE_PROPOSAL_STATES:
            continue  # only police still-open cards
        setup = (r.get("setup_type") or "").strip()
        if setup not in VALID_SETUPS:
            issues.append(f"- `{pid}` ({r.get('ticker','?')}): setup_type '{setup or 'blank'}'"
                          f" is not one of {sorted(VALID_SETUPS)} (SETUPS.md).")
        for field in ("entry_price", "stop_price", "target_price", "thesis", "regime", "direction"):
            if not (r.get(field) or "").strip():
                issues.append(f"- `{pid}` ({r.get('ticker','?')}): required field `{field}` is blank.")
        entry, stop, target = (parse_float(r.get("entry_price")),
                               parse_float(r.get("stop_price")),
                               parse_float(r.get("target_price")))
        planned = parse_float(r.get("planned_r"))
        if entry is not None and stop is not None and target is not None and entry != stop:
            computed = (target - entry) / (entry - stop)
            if computed < 1.5:
                issues.append(f"- `{pid}` ({r.get('ticker','?')}): planned_r {computed:.2f} < 1.5"
                              " — fails the proposal standard (SETUPS.md).")
            if planned is not None and abs(planned - computed) > 0.05:
                issues.append(f"- `{pid}` ({r.get('ticker','?')}): logged planned_r {planned}"
                              f" ≠ computed {computed:.2f}.")
    return issues or ["All open proposals satisfy the card standard."]


def main() -> int:
    config = load_config()
    candidates, scan_date, regime = draft_candidates(config)

    lines: list[str] = ["# Proposal Drafts", ""]
    lines.append("Auto-generated from the latest scanner alerts. **Not proposals, not")
    lines.append("trades, not advice** — pre-filled scaffolding so logging a real proposal")
    lines.append("into `data/proposals.csv` is fast. Nothing here enters proposals.csv or")
    lines.append("trades.csv automatically; the entry, stop, target and thesis are yours.")
    lines.append("Regenerated every scan run — never edit this file by hand.")
    lines.append("")
    if scan_date:
        alert = int(config["scanner"].get("min_score_to_alert", 70))
        lines.append(f"Latest scan day: **{scan_date}** · alert threshold: score ≥ {alert} · "
                     f"regime: **{regime or 'n/a'}**")
        lines.append("")

    lines.append("## Draft cards")
    lines.append("")
    if not candidates:
        lines.append("No alert-worthy candidates on the latest scan day that aren't already an")
        lines.append("open trade or a live proposal. Nothing to draft — that is a normal result.")
        lines.append("")
    else:
        for sig in candidates:
            lines.extend(card(sig, regime))

    lines.append("## Proposal hygiene (existing proposals.csv)")
    lines.append("")
    lines.extend(validate_proposals())
    lines.append("")
    lines.append("---")
    lines.append("To log a draft: append one row to `data/proposals.csv` with a new")
    lines.append("`proposal_id` (e.g. `P2026-0001`) and `status = pending`. See AGENTS.md")
    lines.append("→ \"Proposals\". Log it whether or not you trade it — the untraded ones are")
    lines.append("the control group.")

    DRAFTS_MD.parent.mkdir(parents=True, exist_ok=True)
    DRAFTS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {DRAFTS_MD.relative_to(REPO_ROOT)} ({len(candidates)} draft card(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
