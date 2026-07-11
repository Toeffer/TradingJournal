#!/usr/bin/env python3
"""Recompute journal statistics and executable risk checks from trades.csv."""

from __future__ import annotations

import csv
import statistics
import sys
import tomllib
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TRADES_CSV = REPO_ROOT / "trades.csv"
STATS_MD = REPO_ROOT / "research/journal-stats.md"
RISK_CONFIG = REPO_ROOT / "config/risk.toml"

sys.path.insert(0, str(REPO_ROOT / "scanner"))
from io_utils import atomic_write_text  # noqa: E402


def load_rules() -> dict[str, float | int]:
    with RISK_CONFIG.open("rb") as handle:
        return tomllib.load(handle)["learning_phase"]


def parse_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fmt(value: float | None, digits: int = 2, suffix: str = "") -> str:
    return "—" if value is None else f"{value:+.{digits}f}{suffix}"


def r_stats(trades: list[dict[str, str]]) -> dict[str, float | int | None]:
    values = [value for trade in trades if (value := parse_float(trade.get("r_multiple"))) is not None]
    wins = [value for value in values if value > 0]
    losses = [value for value in values if value <= 0]
    pnls = [value for trade in trades if (value := parse_float(trade.get("pnl"))) is not None]
    gross_win = sum(value for value in pnls if value > 0)
    gross_loss = -sum(value for value in pnls if value < 0)
    return {
        "n": len(trades),
        "n_with_r": len(values),
        "win_rate": len(wins) / len(values) if values else None,
        "avg_win_r": statistics.mean(wins) if wins else None,
        "avg_loss_r": statistics.mean(losses) if losses else None,
        "worst_r": min(values) if values else None,
        "expectancy_r": statistics.mean(values) if values else None,
        "total_pnl": sum(pnls) if pnls else None,
        "profit_factor": (gross_win / gross_loss) if gross_loss > 0 else None,
    }


def breakdown_table(closed: list[dict[str, str]], field: str, title: str) -> list[str]:
    lines = [f"### By {title}", ""]
    values = sorted({trade.get(field, "").strip() or "(blank)" for trade in closed})
    lines.extend([
        f"| {title} | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for value in values:
        group = [trade for trade in closed if (trade.get(field, "").strip() or "(blank)") == value]
        stats = r_stats(group)
        win_rate = f"{stats['win_rate'] * 100:.0f}%" if stats["win_rate"] is not None else "—"
        lines.append(
            f"| {value} | {stats['n']} | {stats['n_with_r']} | {win_rate} "
            f"| {fmt(stats['expectancy_r'])} | {fmt(stats['total_pnl'])} |"
        )
    lines.append("")
    return lines


def iso_week(value: str) -> str:
    year, week, _ = date.fromisoformat(value).isocalendar()
    return f"{year}-W{week:02d}"


def binary_event(trade: dict[str, str]) -> bool:
    text = f"{trade.get('catalyst', '')} {trade.get('thesis', '')}".lower()
    return any(word in text for word in ("earnings", "pdufa", "fda", "ruling", "decision"))


def held_through_event(trade: dict[str, str], today: date) -> bool:
    catalyst_date = trade.get("catalyst_date", "").strip()
    if not catalyst_date:
        return False
    try:
        event = date.fromisoformat(catalyst_date)
    except ValueError:
        return False
    if trade.get("status") == "closed" and trade.get("date_closed"):
        return date.fromisoformat(trade["date_closed"]) >= event
    return trade.get("status") == "open" and event <= today


def main() -> int:
    if not TRADES_CSV.exists():
        print("No trades.csv found.")
        return 0

    with TRADES_CSV.open("r", newline="", encoding="utf-8") as handle:
        trades = list(csv.DictReader(handle))

    rules = load_rules()
    closed = [trade for trade in trades if trade.get("status") == "closed"]
    open_trades = [trade for trade in trades if trade.get("status") == "open"]
    today = date.today()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Journal Stats",
        "",
        f"Auto-generated from `trades.csv` on {now}. Do not edit by hand.",
        "Arithmetic and executable rule checks only; the behavioral review remains human work.",
        "",
    ]

    stats = r_stats(closed)
    lines.extend([
        "## Closed trades",
        "",
        f"- Trades closed: {stats['n']} (of {len(trades)} total; {len(open_trades)} open)",
        f"- With computable R: {stats['n_with_r']}" + (
            " — **every closed trade without a stop is invisible to R stats**"
            if stats["n_with_r"] < stats["n"] else ""
        ),
    ])
    if stats["win_rate"] is not None:
        lines.append(f"- Win rate (R-trades): {stats['win_rate'] * 100:.0f}%")
    lines.extend([
        f"- Avg win: {fmt(stats['avg_win_r'])}R | Avg loss: {fmt(stats['avg_loss_r'])}R | Worst: {fmt(stats['worst_r'])}R",
        f"- **Expectancy per trade: {fmt(stats['expectancy_r'])}R**",
        f"- Total P&L: {fmt(stats['total_pnl'])} € | Profit factor: " + (
            f"{stats['profit_factor']:.2f}" if stats["profit_factor"] is not None else "—"
        ),
        "",
    ])

    lines.extend(breakdown_table(closed, "source", "source"))
    lines.extend(breakdown_table(closed, "setup_type", "setup_type"))
    lines.extend(breakdown_table(closed, "risk_rating", "risk_rating"))

    weekly_limit = float(rules["weekly_loss_limit_r"])
    lines.extend([
        "### Realized R by week",
        "",
        f"| Week | Trades closed | Realized R | Weekly limit ({weekly_limit}R) |",
        "|---|---:|---:|---|",
    ])
    weeks = sorted({iso_week(trade["date_closed"]) for trade in closed if trade.get("date_closed")})
    for week in weeks:
        group = [
            trade for trade in closed
            if trade.get("date_closed") and iso_week(trade["date_closed"]) == week
        ]
        values = [value for trade in group if (value := parse_float(trade.get("r_multiple"))) is not None]
        total = sum(values) if values else None
        state = "**BREACHED**" if total is not None and total <= weekly_limit else "ok"
        lines.append(f"| {week} | {len(group)} | {fmt(total)} | {state} |")
    lines.append("")

    daily_limit = float(rules["daily_loss_limit_r"])
    lines.extend([
        "### Realized R by day",
        "",
        f"| Date | Trades closed | Realized R | Daily limit ({daily_limit}R) |",
        "|---|---:|---:|---|",
    ])
    close_dates = sorted({trade["date_closed"] for trade in closed if trade.get("date_closed")})
    for close_date in close_dates:
        group = [trade for trade in closed if trade.get("date_closed") == close_date]
        values = [value for trade in group if (value := parse_float(trade.get("r_multiple"))) is not None]
        total = sum(values) if values else None
        state = "**BREACHED**" if total is not None and total <= daily_limit else "ok"
        lines.append(f"| {close_date} | {len(group)} | {fmt(total)} | {state} |")
    lines.append("")

    lines.extend([
        "## Open positions",
        "",
        "| Trade | Ticker | Sector | Entry | Stop | Size (€) | Catalyst date |",
        "|---|---|---|---:|---:|---:|---|",
    ])
    for trade in open_trades:
        lines.append(
            f"| {trade.get('trade_id', '')} | {trade.get('ticker', '')} | {trade.get('sector', '') or '—'} "
            f"| {trade.get('entry_price', '') or '—'} | {trade.get('stop_price', '') or '—'} "
            f"| {trade.get('position_size', '') or '—'} | {trade.get('catalyst_date', '') or '—'} |"
        )
    lines.append("")

    flags: list[str] = []
    max_open = int(rules["max_open_positions"])
    max_sector = int(rules["max_per_sector"])
    max_size = float(rules["max_position_size_eur"])
    max_total = float(rules["max_total_position_value_eur"])
    binary_cap = float(rules["binary_event_max_position_size_eur"])

    if len(open_trades) > max_open:
        flags.append(f"Open positions: {len(open_trades)} > max {max_open}.")
    sector_counts: dict[str, int] = {}
    for trade in open_trades:
        sector = trade.get("sector", "").strip()
        if sector:
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
    for sector, count in sector_counts.items():
        if count > max_sector:
            flags.append(f"Sector concentration: {count} open in `{sector}` > max {max_sector}.")

    open_total = sum(parse_float(trade.get("position_size")) or 0.0 for trade in open_trades)
    if open_total > max_total + 0.01:
        flags.append(f"Open position value: €{open_total:.2f} > €{max_total:.2f} cap.")

    for trade in trades:
        size = parse_float(trade.get("position_size"))
        if size is not None and size > max_size + 0.01:
            flags.append(f"{trade.get('trade_id')} ({trade.get('ticker')}): size €{size:.2f} > €{max_size:.0f} cap.")
        if binary_event(trade) and held_through_event(trade, today) and size is not None and size > binary_cap + 0.01:
            flags.append(
                f"{trade.get('trade_id')} ({trade.get('ticker')}): held through binary event at €{size:.2f} > €{binary_cap:.0f} half-size cap."
            )

    for trade in open_trades:
        if parse_float(trade.get("stop_price")) is None:
            flags.append(f"{trade.get('trade_id')} ({trade.get('ticker')}): open with **no stop** — undefined risk.")

    ordered_closed = sorted(
        [trade for trade in closed if trade.get("date_closed")],
        key=lambda trade: (trade["date_closed"], trade.get("trade_id", "")),
    )
    streak_required = int(rules["consecutive_loss_count"])
    pause_days = int(rules["pause_days_after_consecutive_losses"])
    streak = 0
    last_loss_date: date | None = None
    for trade in ordered_closed:
        result = parse_float(trade.get("r_multiple"))
        if result is not None and result <= 0:
            streak += 1
            last_loss_date = date.fromisoformat(trade["date_closed"])
        elif result is not None:
            streak = 0
            last_loss_date = None
    if streak >= streak_required and last_loss_date is not None:
        pause_until = last_loss_date + timedelta(days=pause_days)
        if today <= pause_until:
            flags.append(
                f"Consecutive-loss pause active: {streak} losses; no new trade before {pause_until.isoformat()}."
            )

    lines.extend(["## Rule checks (config/risk.toml)", ""])
    if flags:
        lines.extend(f"- ⚠️ {flag}" for flag in flags)
    else:
        lines.append("- No rule violations detected in current data.")
    lines.append("")

    gaps: list[str] = []
    for trade in closed:
        missing = [
            field for field in ("followed_plan", "lesson", "stop_price", "setup_type")
            if not trade.get(field, "").strip()
        ]
        if missing:
            gaps.append(f"{trade.get('trade_id')} ({trade.get('ticker')}): missing {', '.join(missing)}")
    for trade in open_trades:
        missing = [
            field for field in ("sector", "setup_type", "catalyst")
            if not trade.get(field, "").strip()
        ]
        if missing:
            gaps.append(f"{trade.get('trade_id')} ({trade.get('ticker')}): missing {', '.join(missing)}")

    lines.extend(["## Data gaps (fill these for the review to work)", ""])
    if gaps:
        lines.extend(f"- {gap}" for gap in gaps)
    else:
        lines.append("- None — every trade is fully recorded.")
    lines.append("")

    atomic_write_text(STATS_MD, "\n".join(lines) + "\n")
    print(f"Wrote {STATS_MD.relative_to(REPO_ROOT)} ({len(trades)} trades, {len(closed)} closed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
