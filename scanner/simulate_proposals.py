#!/usr/bin/env python3
"""Simulate outcomes for logged proposals and summarize proposal quality.

data/proposals.csv is the proposals ledger (see SETUPS.md): every idea that
survived research gets a card — entry, stop, target — whether or not it was
traded. This script mechanically walks each open proposal forward on Alpaca
daily bars and records what WOULD have happened, so the pipeline's quality is
measured on every proposal, not just the handful that became real trades.

Simulation rules (deliberately conservative):
- Day 0 = first trading day on/after the proposal date.
- Trigger: the first day whose range touches entry_price (low <= entry <= high).
  Not triggered within TRIGGER_WINDOW trading days -> status `expired` (a
  pullback that never came is a zero-cost outcome by design).
- After trigger, first touch wins: stop touched -> `stopped`; target touched ->
  `target`. If BOTH are touched in the same bar, count it as `stopped` — daily
  bars can't show intraday order, so ambiguity is scored against the idea.
- Neither touched within RESOLVE_HORIZON trading days after trigger ->
  `timeout`, exited at that day's close.
- sim_r = (exit - entry) / (entry - stop), inverted for shorts.

Only blank/open fields are ever filled; terminal rows are never rewritten.
Also regenerates research/proposal-stats.md. Not advice; measurement only.
"""

from __future__ import annotations

import csv
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_history import bars_for as eu_bars_for, is_eu_symbol  # noqa: E402
from run_scan import alpaca_credentials, alpaca_get, load_config  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_CSV = REPO_ROOT / "data/proposals.csv"
STATS_MD = REPO_ROOT / "research/proposal-stats.md"

TRIGGER_WINDOW = 5     # trading days a proposal waits for its entry
RESOLVE_HORIZON = 21   # trading days after trigger before timeout
TERMINAL = {"expired", "stopped", "target", "timeout", "cancelled"}


def parse_float(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fetch_daily_bars(ticker: str, start_date: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    feed = config["alpaca"].get("feed", "iex")
    data = alpaca_get(
        "/v2/stocks/bars",
        {
            "symbols": ticker,
            "timeframe": "1Day",
            "start": start_date,
            "adjustment": "raw",
            "feed": feed,
            "limit": 10000,
        },
        config,
    )
    bars = data.get("bars", {}).get(ticker, [])
    return sorted(bars, key=lambda b: b.get("t", ""))


def sim_r_value(entry: float, exit_price: float, stop: float, direction: str) -> float | None:
    risk = (entry - stop) if direction != "short" else (stop - entry)
    if risk <= 0:
        return None
    move = (exit_price - entry) if direction != "short" else (entry - exit_price)
    return move / risk


def simulate_row(row: dict[str, str], bars: list[dict[str, Any]]) -> bool:
    """Advance one proposal on daily bars. Returns True if the row changed."""
    entry = parse_float(row.get("entry_price"))
    stop = parse_float(row.get("stop_price"))
    target = parse_float(row.get("target_price"))
    if entry is None or stop is None:
        return False
    direction = (row.get("direction") or "long").strip().lower()

    day_bars = [
        (str(b.get("t", ""))[:10], float(b.get("h", 0)), float(b.get("l", 0)), float(b.get("c", 0)))
        for b in bars
        if b.get("h") is not None and b.get("l") is not None
    ]
    start_date = row.get("triggered_date") or row["date"]
    day_bars = [b for b in day_bars if b[0] >= start_date]
    if not day_bars:
        return False

    changed = False
    idx = 0

    if not row.get("triggered_date"):
        trigger_idx = None
        for i, (_, high, low, _) in enumerate(day_bars[:TRIGGER_WINDOW]):
            if low <= entry <= high:
                trigger_idx = i
                break
        if trigger_idx is None:
            if len(day_bars) >= TRIGGER_WINDOW:
                row["status"] = "expired"
                row["resolved_date"] = day_bars[TRIGGER_WINDOW - 1][0]
                return True
            return False  # still waiting for the trigger window to elapse
        row["triggered_date"] = day_bars[trigger_idx][0]
        row["status"] = "triggered"
        changed = True
        idx = trigger_idx

    for offset, (date_str, high, low, close) in enumerate(day_bars[idx:]):
        stop_hit = (low <= stop) if direction != "short" else (high >= stop)
        target_hit = (
            target is not None
            and ((high >= target) if direction != "short" else (low <= target))
        )
        if stop_hit:  # ambiguity (both in one bar) counts against the idea
            row.update(status="stopped", resolved_date=date_str, exit_price=f"{stop:.4f}")
            r = sim_r_value(entry, stop, stop, direction)
            row["sim_r"] = f"{r:.2f}" if r is not None else ""
            return True
        if target_hit:
            row.update(status="target", resolved_date=date_str, exit_price=f"{target:.4f}")
            r = sim_r_value(entry, target, stop, direction)
            row["sim_r"] = f"{r:.2f}" if r is not None else ""
            return True
        if offset >= RESOLVE_HORIZON:
            row.update(status="timeout", resolved_date=date_str, exit_price=f"{close:.4f}")
            r = sim_r_value(entry, close, stop, direction)
            row["sim_r"] = f"{r:.2f}" if r is not None else ""
            return True
    return changed


def group_stats(rows: list[dict[str, str]]) -> dict[str, Any]:
    resolved = [r for r in rows if r.get("status") in ("stopped", "target", "timeout")]
    rs = [v for r in resolved if (v := parse_float(r.get("sim_r"))) is not None]
    return {
        "n": len(rows),
        "resolved": len(resolved),
        "expectancy": statistics.mean(rs) if rs else None,
        "hit_rate": (100.0 * sum(1 for v in rs if v > 0) / len(rs)) if rs else None,
    }


def stats_line(label: str, s: dict[str, Any]) -> str:
    exp = f"{s['expectancy']:+.2f}R" if s["expectancy"] is not None else "—"
    hit = f"{s['hit_rate']:.0f}%" if s["hit_rate"] is not None else "—"
    return f"| {label} | {s['n']} | {s['resolved']} | {exp} | {hit} |"


def write_stats(rows: list[dict[str, str]]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []
    lines.append("# Proposal Stats")
    lines.append("")
    lines.append(f"Auto-generated from `data/proposals.csv` on {now}. Do not edit by hand.")
    lines.append("")
    lines.append("Simulated outcomes use conservative daily-bar rules (see")
    lines.append("`scanner/simulate_proposals.py`): same-bar ambiguity counts as a stop-out, and")
    lines.append("fills ignore slippage/spread. Sim R measures the *pipeline*, not real P&L.")
    lines.append("")

    if not rows:
        lines.append("No proposals logged yet. Log the first one per SETUPS.md and this report")
        lines.append("fills itself in.")
        STATS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    by_status: dict[str, int] = {}
    for r in rows:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
    lines.append("## Pipeline state")
    lines.append("")
    lines.append("- " + " | ".join(f"{k}: {v}" for k, v in sorted(by_status.items())))
    lines.append("")

    header = ["| Group | Proposals | Resolved | Sim expectancy | Hit rate |",
              "|---|---:|---:|---:|---:|"]

    lines.append("## Overall")
    lines.append("")
    lines.extend(header)
    lines.append(stats_line("all", group_stats(rows)))
    lines.append("")

    for field, title in (("setup_type", "setup"), ("regime", "regime"), ("source", "source")):
        lines.append(f"## By {title}")
        lines.append("")
        lines.extend(header)
        for value in sorted({r.get(field, "").strip() or "(blank)" for r in rows}):
            group = [r for r in rows if (r.get(field, "").strip() or "(blank)") == value]
            lines.append(stats_line(value, group_stats(group)))
        lines.append("")

    lines.append("## Traded vs passed (the picker test)")
    lines.append("")
    lines.extend(header)
    traded = [r for r in rows if (r.get("traded", "").strip().lower() == "yes")]
    passed = [r for r in rows if (r.get("traded", "").strip().lower() != "yes")]
    lines.append(stats_line("traded", group_stats(traded)))
    lines.append(stats_line("passed", group_stats(passed)))
    lines.append("")
    lines.append("If `passed` beats `traded` once samples are meaningful, my selection among")
    lines.append("proposals is subtracting value — trade the process, not the feeling.")

    STATS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not PROPOSALS_CSV.exists() or PROPOSALS_CSV.stat().st_size == 0:
        print("No proposals.csv found.")
        write_stats([])
        return 0

    with PROPOSALS_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    open_rows = [r for r in rows if r.get("status") not in TERMINAL]
    changed = 0
    if open_rows:
        key, secret = alpaca_credentials()
        if not key or not secret:
            print("Alpaca credentials not configured; skipping proposal simulation.")
        else:
            config = load_config()
            for row in open_rows:
                try:
                    if is_eu_symbol(row["ticker"]):
                        # EU proposals simulate on the self-accumulated local history.
                        bars = [b for b in eu_bars_for(row["ticker"]) if b["t"] >= row["date"]]
                    else:
                        bars = fetch_daily_bars(row["ticker"], row["date"], config)
                except Exception as exc:  # noqa: BLE001 - one bad ticker shouldn't stop the run
                    print(f"Skipping {row.get('ticker')}: {exc}", file=sys.stderr)
                    continue
                if simulate_row(row, bars):
                    changed += 1

    if changed:
        with PROPOSALS_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Updated {changed} proposal(s).")
    else:
        print("No proposal state changes.")

    write_stats(rows)
    print(f"Wrote {STATS_MD.relative_to(REPO_ROOT)} ({len(rows)} proposals).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
