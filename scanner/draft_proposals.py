#!/usr/bin/env python3
"""Generate human-completed proposal-card scaffolding from recent alerts."""

from __future__ import annotations

import csv
import sys
import tomllib
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_utils import atomic_write_text  # noqa: E402
from run_scan import REPO_ROOT, load_config  # noqa: E402

SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
REGIME_CSV = REPO_ROOT / "data/market_regime.csv"
PROPOSALS_CSV = REPO_ROOT / "data/proposals.csv"
TRADES_CSV = REPO_ROOT / "trades.csv"
DRAFTS_MD = REPO_ROOT / "research/proposal-drafts.md"
RISK_CONFIG = REPO_ROOT / "config/risk.toml"

VALID_SETUPS = {"breakout", "pullback", "post-earnings-drift", "special-situation"}
LIVE_PROPOSAL_STATES = {"pending", "triggered"}


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def default_holding_days() -> int:
    with RISK_CONFIG.open("rb") as handle:
        return int(tomllib.load(handle)["horizons"]["default_proposal_holding_days"])


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


def covered_tickers(signal_tickers: set[str]) -> set[str]:
    covered: set[str] = set()
    for trade in load_csv(TRADES_CSV):
        if trade.get("status") == "open" and trade.get("ticker"):
            covered.add(trade["ticker"].strip().upper())
    for proposal in load_csv(PROPOSALS_CSV):
        if proposal.get("status", "").strip().lower() in LIVE_PROPOSAL_STATES:
            covered.add(proposal.get("ticker", "").strip().upper())
    return covered & signal_tickers


def latest_scan_date(signals: list[dict[str, str]]) -> str | None:
    dates = [row.get("timestamp", "")[:10] for row in signals if row.get("timestamp")]
    return max(dates) if dates else None


def draft_candidates(config: dict[str, Any]) -> tuple[list[dict[str, str]], str | None, str]:
    signals = load_csv(SIGNALS_CSV)
    if not signals:
        return [], None, ""
    scan_date = latest_scan_date(signals)
    alert = int(config["scanner"].get("min_score_to_alert", 70))
    max_rows = int(config["scanner"].get("max_candidates_per_report", 10))
    current = [
        row for row in signals
        if row.get("timestamp", "")[:10] == scan_date
        and (parse_float(row.get("score")) or 0) >= alert
    ]
    covered = covered_tickers({row["ticker"].strip().upper() for row in current})
    fresh = [row for row in current if row["ticker"].strip().upper() not in covered]
    fresh.sort(key=lambda row: parse_float(row.get("score")) or 0, reverse=True)
    return fresh[:max_rows], scan_date, latest_regime()


def fmt(value: str | None, suffix: str = "") -> str:
    parsed = parse_float(value)
    return "n/a" if parsed is None else f"{parsed:g}{suffix}"


def card(signal: dict[str, str], regime: str, holding_days: int) -> list[str]:
    ticker = signal["ticker"].strip().upper()
    market = signal.get("market", "US")
    regime_flag = ""
    if regime == "defensive":
        regime_flag = " — breakout proposals require `regime-against` in notes"
    return [
        f"### {ticker} — scanner score {signal.get('score', '')} ({market})",
        "",
        "**Reason to research—not a proposal and not a trade.**",
        "",
        "_Mechanical context:_",
        f"- date: {signal.get('timestamp', '')[:10]} | direction: long | source: scanner",
        f"- candidate_ref: scanner_signals.csv#{signal.get('timestamp', '')[:10]}:{ticker}",
        f"- regime: {regime or 'n/a'}{regime_flag}",
        f"- reference price: {fmt(signal.get('price'))} (not an entry level)",
        f"- move {fmt(signal.get('change_pct'), '%')} | rel vol {fmt(signal.get('rel_volume'), 'x')} | 5d extension {fmt(signal.get('extension_5d_pct'), '%')}",
        f"- indicators, context only: RSI14 {fmt(signal.get('rsi14'))} | EMA20 distance {fmt(signal.get('ema20_dist_pct'), '%')} | BB %B {fmt(signal.get('bb_percent_b'))}",
        "- suggested setup to investigate: `pullback`; a high score is not itself a setup",
        "",
        "_Human judgment required before logging:_",
        "- [ ] entry_price: ______",
        "- [ ] stop_price: ______",
        "- [ ] target_price: ______",
        "- [ ] planned_r: ______ (must be at least 1.5)",
        "- [ ] thesis: ______ (why this, why now)",
        "- [ ] catalyst / catalyst_date: ______ (primary-source verified)",
        f"- [ ] max_holding_days: {holding_days} (change only with a written reason)",
        "- [ ] exit_before_catalyst: yes (default; `no` is an explicit binary-risk decision)",
        "- [ ] catalyst horizon: inside 21 days, or keep it in Early Watch instead",
        "",
    ]


def validate_proposals(holding_days: int) -> list[str]:
    rows = load_csv(PROPOSALS_CSV)
    if not rows:
        return ["No proposals logged yet — nothing to validate."]
    issues: list[str] = []
    seen_ids: set[str] = set()
    for row in rows:
        proposal_id = (row.get("proposal_id") or "?").strip()
        if proposal_id in seen_ids:
            issues.append(f"- `{proposal_id}`: duplicate proposal_id.")
        seen_ids.add(proposal_id)
        if row.get("status", "").strip().lower() not in LIVE_PROPOSAL_STATES:
            continue
        setup = (row.get("setup_type") or "").strip()
        if setup not in VALID_SETUPS:
            issues.append(f"- `{proposal_id}` ({row.get('ticker', '?')}): invalid setup_type `{setup or 'blank'}`.")
        for field in (
            "entry_price", "stop_price", "target_price", "thesis", "regime", "direction",
            "max_holding_days", "exit_before_catalyst",
        ):
            if not (row.get(field) or "").strip():
                issues.append(f"- `{proposal_id}` ({row.get('ticker', '?')}): `{field}` is blank.")
        entry = parse_float(row.get("entry_price"))
        stop = parse_float(row.get("stop_price"))
        target = parse_float(row.get("target_price"))
        planned = parse_float(row.get("planned_r"))
        if None not in (entry, stop, target) and entry != stop:
            computed = (target - entry) / (entry - stop)
            if computed < 1.5:
                issues.append(f"- `{proposal_id}` ({row.get('ticker', '?')}): planned R {computed:.2f} is below 1.5.")
            if planned is not None and abs(planned - computed) > 0.05:
                issues.append(f"- `{proposal_id}` ({row.get('ticker', '?')}): logged planned R {planned} differs from {computed:.2f}.")
        logged_days = parse_float(row.get("max_holding_days"))
        if logged_days is not None and (logged_days < 1 or not logged_days.is_integer()):
            issues.append(f"- `{proposal_id}` ({row.get('ticker', '?')}): max_holding_days must be a positive integer (default {holding_days}).")
        if row.get("exit_before_catalyst", "").strip().lower() not in {"yes", "no"}:
            issues.append(f"- `{proposal_id}` ({row.get('ticker', '?')}): exit_before_catalyst must be yes or no.")
    return issues or ["All open proposals satisfy the card standard."]


def main() -> int:
    config = load_config()
    holding_days = default_holding_days()
    candidates, scan_date, regime = draft_candidates(config)
    lines = [
        "# Proposal Drafts",
        "",
        "Auto-generated research scaffolding. **Not proposals, trades, or advice.**",
        "Judgment fields remain blank and nothing writes to proposals.csv automatically.",
        "",
    ]
    if scan_date:
        alert = int(config["scanner"].get("min_score_to_alert", 70))
        lines.extend([
            f"Latest scan day: **{scan_date}** · alert threshold: score ≥ {alert} · regime: **{regime or 'n/a'}**",
            "",
        ])
    lines.extend(["## Draft cards", ""])
    if candidates:
        for signal in candidates:
            lines.extend(card(signal, regime, holding_days))
    else:
        lines.extend([
            "No alert-worthy uncovered candidates on the latest scan day. That is a normal result.",
            "",
        ])
    lines.extend(["## Proposal hygiene", "", *validate_proposals(holding_days), "", "---", ""])
    lines.extend([
        "Log a completed card as a new row in `data/proposals.csv` whether or not it is traded.",
        "The untraded rows are the control group.",
    ])
    atomic_write_text(DRAFTS_MD, "\n".join(lines) + "\n")
    print(f"Wrote {DRAFTS_MD.relative_to(REPO_ROOT)} ({len(candidates)} draft card(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
