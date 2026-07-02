#!/usr/bin/env python3
"""Recompute journal statistics from trades.csv into research/journal-stats.md.

Runs automatically (via .github/workflows/journal.yml) whenever trades.csv
changes on main, so the headline numbers are always current without asking.

Everything here is computed from trades.csv — nothing is estimated or invented
(see the guardrails in AGENTS.md). The output is a derived artifact: regenerated
on every run, never edited by hand, never advice. The deeper behavioral review
(plan adherence, patterns, lessons) still belongs to the human+Claude review
pass described in AGENTS.md; this file only keeps the arithmetic fresh.
"""

from __future__ import annotations

import csv
import statistics
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TRADES_CSV = REPO_ROOT / "trades.csv"
STATS_MD = REPO_ROOT / "research/journal-stats.md"

# Learning-phase rules from RISK_RULES.md the report checks against.
MAX_OPEN_POSITIONS = 5
MAX_PER_SECTOR = 2
MAX_POSITION_SIZE_EUR = 150.0
WEEKLY_LOSS_LIMIT_R = -4.0


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
    rs = [v for t in trades if (v := parse_float(t.get("r_multiple"))) is not None]
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]
    win_rate = len(wins) / len(rs) if rs else None
    avg_win = statistics.mean(wins) if wins else None
    avg_loss = statistics.mean(losses) if losses else None
    expectancy = statistics.mean(rs) if rs else None
    pnls = [v for t in trades if (v := parse_float(t.get("pnl"))) is not None]
    gross_win = sum(p for p in pnls if p > 0)
    gross_loss = -sum(p for p in pnls if p < 0)
    return {
        "n": len(trades),
        "n_with_r": len(rs),
        "win_rate": win_rate,
        "avg_win_r": avg_win,
        "avg_loss_r": avg_loss,
        "worst_r": min(rs) if rs else None,
        "expectancy_r": expectancy,
        "total_pnl": sum(pnls) if pnls else None,
        "profit_factor": (gross_win / gross_loss) if gross_loss > 0 else None,
    }


def breakdown_table(closed: list[dict[str, str]], field: str, title: str) -> list[str]:
    lines = [f"### By {title}", ""]
    values = sorted({t.get(field, "").strip() or "(blank)" for t in closed})
    lines.append("| " + title + " | Trades | With R | Win rate | Expectancy (R) | Total P&L (€) |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for value in values:
        group = [t for t in closed if (t.get(field, "").strip() or "(blank)") == value]
        s = r_stats(group)
        win_rate = f"{s['win_rate'] * 100:.0f}%" if s["win_rate"] is not None else "—"
        lines.append(
            f"| {value} | {s['n']} | {s['n_with_r']} | {win_rate} "
            f"| {fmt(s['expectancy_r'])} | {fmt(s['total_pnl'])} |"
        )
    lines.append("")
    return lines


def iso_week(d: str) -> str:
    year, week, _ = date.fromisoformat(d).isocalendar()
    return f"{year}-W{week:02d}"


def main() -> int:
    if not TRADES_CSV.exists():
        print("No trades.csv found.")
        return 0

    with TRADES_CSV.open("r", newline="", encoding="utf-8") as f:
        trades = list(csv.DictReader(f))

    closed = [t for t in trades if t.get("status") == "closed"]
    open_trades = [t for t in trades if t.get("status") == "open"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines: list[str] = []
    lines.append("# Journal Stats")
    lines.append("")
    lines.append(f"Auto-generated from `trades.csv` on {now}. Do not edit by hand.")
    lines.append("Arithmetic only — the behavioral review in AGENTS.md is still the real review.")
    lines.append("")

    s = r_stats(closed)
    lines.append("## Closed trades")
    lines.append("")
    lines.append(f"- Trades closed: {s['n']} (of {len(trades)} total; {len(open_trades)} open)")
    lines.append(f"- With computable R: {s['n_with_r']}"
                 + (" — **every closed trade without a stop is invisible to R stats**"
                    if s["n_with_r"] < s["n"] else ""))
    if s["win_rate"] is not None:
        lines.append(f"- Win rate (R-trades): {s['win_rate'] * 100:.0f}%")
    lines.append(f"- Avg win: {fmt(s['avg_win_r'])}R | Avg loss: {fmt(s['avg_loss_r'])}R "
                 f"| Worst: {fmt(s['worst_r'])}R")
    lines.append(f"- **Expectancy per trade: {fmt(s['expectancy_r'])}R**")
    lines.append(f"- Total P&L: {fmt(s['total_pnl'])} € | Profit factor: "
                 + (f"{s['profit_factor']:.2f}" if s["profit_factor"] is not None else "—"))
    lines.append("")

    lines.extend(breakdown_table(closed, "source", "source"))
    lines.extend(breakdown_table(closed, "setup_type", "setup_type"))
    lines.extend(breakdown_table(closed, "risk_rating", "risk_rating"))

    lines.append("### Realized R by week")
    lines.append("")
    lines.append(f"| Week | Trades closed | Realized R | Weekly limit ({WEEKLY_LOSS_LIMIT_R}R) |")
    lines.append("|---|---:|---:|---|")
    weeks = sorted({iso_week(t["date_closed"]) for t in closed if t.get("date_closed")})
    for week in weeks:
        group = [t for t in closed if t.get("date_closed") and iso_week(t["date_closed"]) == week]
        rs = [v for t in group if (v := parse_float(t.get("r_multiple"))) is not None]
        total_r = sum(rs) if rs else None
        breached = "**BREACHED**" if total_r is not None and total_r <= WEEKLY_LOSS_LIMIT_R else "ok"
        lines.append(f"| {week} | {len(group)} | {fmt(total_r)} | {breached} |")
    lines.append("")

    lines.append("## Open positions")
    lines.append("")
    lines.append("| Trade | Ticker | Sector | Entry | Stop | Size (€) | Catalyst date |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for t in open_trades:
        lines.append(
            f"| {t.get('trade_id','')} | {t.get('ticker','')} | {t.get('sector','') or '—'} "
            f"| {t.get('entry_price','') or '—'} | {t.get('stop_price','') or '—'} "
            f"| {t.get('position_size','') or '—'} | {t.get('catalyst_date','') or '—'} |"
        )
    lines.append("")

    lines.append("## Rule checks (RISK_RULES.md)")
    lines.append("")
    flags: list[str] = []
    if len(open_trades) > MAX_OPEN_POSITIONS:
        flags.append(f"Open positions: {len(open_trades)} > max {MAX_OPEN_POSITIONS}.")
    sector_counts: dict[str, int] = {}
    for t in open_trades:
        sector = t.get("sector", "").strip()
        if sector:
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
    for sector, count in sector_counts.items():
        if count > MAX_PER_SECTOR:
            flags.append(f"Sector concentration: {count} open in `{sector}` > max {MAX_PER_SECTOR}.")
    for t in trades:
        size = parse_float(t.get("position_size"))
        if size is not None and size > MAX_POSITION_SIZE_EUR:
            flags.append(f"{t.get('trade_id')} ({t.get('ticker')}): size €{size:.2f} > €{MAX_POSITION_SIZE_EUR:.0f} cap.")
    no_stop_open = [t for t in open_trades if parse_float(t.get("stop_price")) is None]
    for t in no_stop_open:
        flags.append(f"{t.get('trade_id')} ({t.get('ticker')}): open with **no stop** — undefined risk.")
    if flags:
        lines.extend(f"- ⚠️ {f}" for f in flags)
    else:
        lines.append("- No rule violations detected in current data.")
    lines.append("")

    lines.append("## Data gaps (fill these for the review to work)")
    lines.append("")
    gaps: list[str] = []
    for t in closed:
        missing = [f for f in ("followed_plan", "lesson", "stop_price", "setup_type")
                   if not t.get(f, "").strip()]
        if missing:
            gaps.append(f"{t.get('trade_id')} ({t.get('ticker')}): missing {', '.join(missing)}")
    for t in open_trades:
        missing = [f for f in ("sector", "setup_type", "catalyst")
                   if not t.get(f, "").strip()]
        if missing:
            gaps.append(f"{t.get('trade_id')} ({t.get('ticker')}): missing {', '.join(missing)}")
    if gaps:
        lines.extend(f"- {g}" for g in gaps)
    else:
        lines.append("- None — every trade is fully recorded.")
    lines.append("")

    STATS_MD.parent.mkdir(parents=True, exist_ok=True)
    STATS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {STATS_MD.relative_to(REPO_ROOT)} ({len(trades)} trades, {len(closed)} closed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
