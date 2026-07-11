#!/usr/bin/env python3
"""Simulate outcomes for logged proposals and summarize proposal quality.

The proposal ledger measures every fully specified idea, traded or not. Simulation
is deliberately conservative and uses a short, explicit swing horizon rather than
pretending a setup remains unchanged for a month.

Rules:
- Day 0 is the first trading day on/after the proposal date.
- Entry must trigger within five trading sessions.
- Stop wins same-bar stop/target ambiguity.
- ``max_holding_days`` defaults to 10 trading sessions, configurable per proposal.
- ``exit_before_catalyst=yes`` exits at the final available pre-catalyst close if
  neither stop nor target has resolved first.
- Terminal rows are never rewritten.
"""

from __future__ import annotations

import csv
import statistics
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_history import bars_for as eu_bars_for, is_eu_symbol  # noqa: E402
from io_utils import atomic_write_csv, atomic_write_text  # noqa: E402
from run_scan import alpaca_credentials, alpaca_get, load_config  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_CSV = REPO_ROOT / "data/proposals.csv"
STATS_MD = REPO_ROOT / "research/proposal-stats.md"
RISK_CONFIG = REPO_ROOT / "config/risk.toml"

TRIGGER_WINDOW = 5
TERMINAL = {"expired", "stopped", "target", "timeout", "catalyst_exit", "cancelled"}
RESOLVED = {"stopped", "target", "timeout", "catalyst_exit"}


def default_holding_days() -> int:
    with RISK_CONFIG.open("rb") as handle:
        return int(tomllib.load(handle)["horizons"]["default_proposal_holding_days"])


def parse_float(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_positive_int(value: str | None, default: int) -> int:
    parsed = parse_float(value)
    if parsed is None or parsed < 1 or not parsed.is_integer():
        return default
    return int(parsed)


def truthy_yes(value: str | None, default: bool = False) -> bool:
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in {"yes", "true", "1"}


def fetch_daily_bars(ticker: str, start_date: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    feed = config["alpaca"].get("feed", "iex")
    data = alpaca_get(
        "/v2/stocks/bars",
        {
            "symbols": ticker,
            "timeframe": "1Day",
            "start": start_date,
            "adjustment": "all",
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


def resolve_row(
    row: dict[str, str],
    status: str,
    date_str: str,
    exit_price: float,
    entry: float,
    stop: float,
    direction: str,
) -> None:
    row.update(status=status, resolved_date=date_str, exit_price=f"{exit_price:.4f}")
    result = sim_r_value(entry, exit_price, stop, direction)
    row["sim_r"] = f"{result:.2f}" if result is not None else ""


def simulate_row(row: dict[str, str], bars: list[dict[str, Any]]) -> bool:
    """Advance one proposal on daily bars. Return True when the row changed."""
    entry = parse_float(row.get("entry_price"))
    stop = parse_float(row.get("stop_price"))
    target = parse_float(row.get("target_price"))
    if entry is None or stop is None:
        return False
    direction = (row.get("direction") or "long").strip().lower()
    holding_days = parse_positive_int(row.get("max_holding_days"), default_holding_days())
    catalyst_date = (row.get("catalyst_date") or "").strip()
    exit_before = truthy_yes(row.get("exit_before_catalyst"), default=bool(catalyst_date))

    all_bars = [
        (str(b.get("t", ""))[:10], float(b.get("h", 0)), float(b.get("l", 0)), float(b.get("c", 0)))
        for b in bars
        if b.get("h") is not None and b.get("l") is not None and b.get("c") is not None
    ]
    start_date = row.get("triggered_date") or row.get("date", "")
    all_bars = [bar for bar in all_bars if bar[0] >= start_date]
    if not all_bars:
        return False

    catalyst_reached = bool(
        exit_before and catalyst_date and any(date_str >= catalyst_date for date_str, *_ in all_bars)
    )
    day_bars = [
        bar for bar in all_bars if not (exit_before and catalyst_date and bar[0] >= catalyst_date)
    ]
    if not day_bars:
        return False

    changed = False
    start_idx = 0
    if not row.get("triggered_date"):
        trigger_idx: int | None = None
        for index, (_, high, low, _) in enumerate(day_bars[:TRIGGER_WINDOW]):
            if low <= entry <= high:
                trigger_idx = index
                break
        if trigger_idx is None:
            if len(day_bars) >= TRIGGER_WINDOW or catalyst_reached:
                row["status"] = "expired"
                row["resolved_date"] = day_bars[min(len(day_bars), TRIGGER_WINDOW) - 1][0]
                return True
            return False
        row["triggered_date"] = day_bars[trigger_idx][0]
        row["status"] = "triggered"
        changed = True
        start_idx = trigger_idx

    active_bars = day_bars[start_idx:]
    for offset, (date_str, high, low, close) in enumerate(active_bars):
        stop_hit = (low <= stop) if direction != "short" else (high >= stop)
        target_hit = target is not None and (
            (high >= target) if direction != "short" else (low <= target)
        )
        if stop_hit:
            resolve_row(row, "stopped", date_str, stop, entry, stop, direction)
            return True
        if target_hit:
            resolve_row(row, "target", date_str, target, entry, stop, direction)
            return True
        if offset + 1 >= holding_days:
            resolve_row(row, "timeout", date_str, close, entry, stop, direction)
            return True

    if catalyst_reached:
        date_str, _, _, close = active_bars[-1]
        resolve_row(row, "catalyst_exit", date_str, close, entry, stop, direction)
        return True
    return changed


def group_stats(rows: list[dict[str, str]]) -> dict[str, Any]:
    resolved = [row for row in rows if row.get("status") in RESOLVED]
    values = [value for row in resolved if (value := parse_float(row.get("sim_r"))) is not None]
    return {
        "n": len(rows),
        "resolved": len(resolved),
        "expectancy": statistics.mean(values) if values else None,
        "hit_rate": (100.0 * sum(value > 0 for value in values) / len(values)) if values else None,
    }


def stats_line(label: str, stats: dict[str, Any]) -> str:
    expectancy = f"{stats['expectancy']:+.2f}R" if stats["expectancy"] is not None else "—"
    hit_rate = f"{stats['hit_rate']:.0f}%" if stats["hit_rate"] is not None else "—"
    return f"| {label} | {stats['n']} | {stats['resolved']} | {expectancy} | {hit_rate} |"


def write_stats(rows: list[dict[str, str]]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Proposal Stats",
        "",
        f"Auto-generated from `data/proposals.csv` on {now}. Do not edit by hand.",
        "",
        "Simulation uses conservative daily-bar rules: same-bar ambiguity counts as a",
        "stop-out, fills ignore spread/slippage, the default holding period is 10 trading",
        "sessions, and catalyst-sensitive proposals exit at the final pre-event close when",
        "`exit_before_catalyst = yes`. Sim R measures the pipeline, not real P&L.",
        "",
    ]
    if not rows:
        lines.extend([
            "No proposals logged yet. Log the first one per SETUPS.md and this report",
            "fills itself in.",
        ])
        atomic_write_text(STATS_MD, "\n".join(lines) + "\n")
        return

    by_status: dict[str, int] = {}
    for row in rows:
        status = row.get("status", "?")
        by_status[status] = by_status.get(status, 0) + 1
    lines.extend(["## Pipeline state", "", "- " + " | ".join(f"{k}: {v}" for k, v in sorted(by_status.items())), ""])

    header = [
        "| Group | Proposals | Resolved | Sim expectancy | Hit rate |",
        "|---|---:|---:|---:|---:|",
    ]
    lines.extend(["## Overall", "", *header, stats_line("all", group_stats(rows)), ""])

    for field, title in (("setup_type", "setup"), ("regime", "regime"), ("source", "source")):
        lines.extend([f"## By {title}", "", *header])
        for value in sorted({row.get(field, "").strip() or "(blank)" for row in rows}):
            group = [row for row in rows if (row.get(field, "").strip() or "(blank)") == value]
            lines.append(stats_line(value, group_stats(group)))
        lines.append("")

    traded = [row for row in rows if row.get("traded", "").strip().lower() == "yes"]
    passed = [row for row in rows if row.get("traded", "").strip().lower() != "yes"]
    lines.extend([
        "## Traded vs passed (the picker test)",
        "",
        *header,
        stats_line("traded", group_stats(traded)),
        stats_line("passed", group_stats(passed)),
        "",
        "If `passed` beats `traded` once samples are meaningful, discretionary selection",
        "is subtracting value — trade the process, not the feeling.",
    ])
    atomic_write_text(STATS_MD, "\n".join(lines) + "\n")


def main() -> int:
    if not PROPOSALS_CSV.exists() or PROPOSALS_CSV.stat().st_size == 0:
        print("No proposals.csv found.")
        write_stats([])
        return 0

    with PROPOSALS_CSV.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    open_rows = [row for row in rows if row.get("status") not in TERMINAL]
    changed = 0
    config = load_config() if open_rows else None
    key, secret = alpaca_credentials()
    for row in open_rows:
        try:
            if is_eu_symbol(row["ticker"]):
                bars = [bar for bar in eu_bars_for(row["ticker"]) if bar["t"] >= row["date"]]
            elif key and secret and config is not None:
                bars = fetch_daily_bars(row["ticker"], row["date"], config)
            else:
                print(f"Skipping {row.get('ticker')}: Alpaca credentials not configured.", file=sys.stderr)
                continue
        except Exception as exc:  # noqa: BLE001 - one provider failure must not block other rows
            print(f"Skipping {row.get('ticker')}: {exc}", file=sys.stderr)
            continue
        if simulate_row(row, bars):
            changed += 1

    if changed:
        atomic_write_csv(PROPOSALS_CSV, fieldnames, rows)
        print(f"Updated {changed} proposal(s).")
    else:
        print("No proposal state changes.")

    write_stats(rows)
    print(f"Wrote {STATS_MD.relative_to(REPO_ROOT)} ({len(rows)} proposals).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
