#!/usr/bin/env python3
"""Generate a compact Monday digest from journal, proposal, and scanner data."""

from __future__ import annotations

import csv
import re
import sys
import tomllib
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TRADES_CSV = REPO_ROOT / "trades.csv"
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
PROPOSALS_CSV = REPO_ROOT / "data/proposals.csv"
RESEARCH_DIR = REPO_ROOT / "research"
RISK_CONFIG = REPO_ROOT / "config/risk.toml"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from journal_stats import fmt, parse_float, r_stats  # noqa: E402
sys.path.insert(0, str(REPO_ROOT / "scanner"))
from io_utils import atomic_write_text  # noqa: E402

STALE_CANDIDATES_DAYS = 10
RESOLVED_PROPOSALS = {"stopped", "target", "timeout", "catalyst_exit"}


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_horizons() -> tuple[int, int]:
    with RISK_CONFIG.open("rb") as handle:
        horizons = tomllib.load(handle)["horizons"]
    return int(horizons["actionable_catalyst_days"]), int(horizons["discovery_catalyst_days"])


def fmt_pct(value: float | None) -> str:
    return "—" if value is None else f"{value:+.2f}%"


def newest_candidates_file() -> Path | None:
    files = list(RESEARCH_DIR.glob("candidates-*.md"))
    if not files:
        return None

    def sort_key(path: Path) -> tuple[str, str]:
        match = re.match(r"candidates-(\d{4}-\d{2}-\d{2})(?:-(\d{4}))?\.md$", path.name)
        return (match.group(1), match.group(2) or "0000") if match else ("", "")

    return max(files, key=sort_key)


def summary_block(path: Path) -> list[str]:
    output: list[str] = []
    in_summary = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if in_summary:
                break
            in_summary = line.strip().lower() == "## summary"
            continue
        if in_summary and line.strip():
            output.append(line)
    return output


def catalyst_bucket(value: str, today: date, actionable_days: int, discovery_days: int) -> str:
    if not value:
        return "no date"
    try:
        event = date.fromisoformat(value)
    except ValueError:
        return "invalid date"
    days = (event - today).days
    if days < 0:
        return f"past ({-days}d)"
    if days <= 7:
        return f"ACT-NOW ({days}d)"
    if days <= actionable_days:
        return f"actionable ({days}d)"
    if days <= discovery_days:
        return f"Early Watch only ({days}d)"
    return f"distant ({days}d)"


def main() -> int:
    today = date.today()
    week_start = today - timedelta(days=7)
    actionable_days, discovery_days = load_horizons()
    trades = load_csv(TRADES_CSV)
    signals = load_csv(SIGNALS_CSV)
    proposals = load_csv(PROPOSALS_CSV)

    closed_week = [
        trade for trade in trades
        if trade.get("status") == "closed"
        and trade.get("date_closed")
        and week_start.isoformat() <= trade["date_closed"] < today.isoformat()
    ]
    open_trades = [trade for trade in trades if trade.get("status") == "open"]
    all_closed = [trade for trade in trades if trade.get("status") == "closed"]

    lines = [
        f"# Weekly Digest — {today.isoformat()}",
        "",
        f"Auto-generated for {week_start.isoformat()} through {today.isoformat()}.",
        "This surfaces recorded facts; it is not advice.",
        "",
        "## Journal: last seven days",
        "",
    ]

    if closed_week:
        lines.extend([
            "| Trade | Ticker | Closed | R | P&L (€) | Followed plan |",
            "|---|---|---|---:|---:|---|",
        ])
        for trade in sorted(closed_week, key=lambda row: (row.get("date_closed", ""), row.get("trade_id", ""))):
            lines.append(
                f"| {trade.get('trade_id', '')} | {trade.get('ticker', '')} | {trade.get('date_closed', '')} "
                f"| {fmt(parse_float(trade.get('r_multiple')))} | {fmt(parse_float(trade.get('pnl')))} "
                f"| {trade.get('followed_plan', '') or '—'} |"
            )
        week_values = [value for trade in closed_week if (value := parse_float(trade.get("r_multiple"))) is not None]
        lines.extend(["", f"- Realized: **{fmt(sum(week_values) if week_values else None)}R**."])
    else:
        lines.append("No trades closed this week.")

    all_stats = r_stats(all_closed)
    lines.extend([
        f"- All-time: {all_stats['n']} closed; expectancy {fmt(all_stats['expectancy_r'])}R; P&L {fmt(all_stats['total_pnl'])} €.",
        "",
        "## Open positions and catalyst horizon",
        "",
    ])
    if open_trades:
        lines.extend([
            "| Trade | Ticker | Entry | Stop | Catalyst | Date | Horizon |",
            "|---|---|---:|---:|---|---|---|",
        ])
        for trade in open_trades:
            catalyst_date = trade.get("catalyst_date", "").strip()
            lines.append(
                f"| {trade.get('trade_id', '')} | {trade.get('ticker', '')} "
                f"| {trade.get('entry_price', '') or '—'} | {trade.get('stop_price', '') or '—'} "
                f"| {trade.get('catalyst', '') or '—'} | {catalyst_date or '—'} "
                f"| {catalyst_bucket(catalyst_date, today, actionable_days, discovery_days)} |"
            )
        lines.extend([
            "",
            f"- Actionable research window: 0–{actionable_days} calendar days.",
            f"- Days {actionable_days + 1}–{discovery_days} are Early Watch, not a reason to enter early.",
        ])
    else:
        lines.append("No open positions.")
    lines.append("")

    lines.extend(["## Proposal pipeline", ""])
    if proposals:
        by_status: dict[str, int] = {}
        for proposal in proposals:
            status = proposal.get("status", "?")
            by_status[status] = by_status.get(status, 0) + 1
        lines.append("- " + " | ".join(f"{key}: {value}" for key, value in sorted(by_status.items())))
        resolved = [proposal for proposal in proposals if proposal.get("status") in RESOLVED_PROPOSALS]
        values = [value for proposal in resolved if (value := parse_float(proposal.get("sim_r"))) is not None]
        if values:
            lines.append(f"- Simulated expectancy: **{fmt(sum(values) / len(values))}R** across {len(values)} resolved proposals.")
        pending = [proposal for proposal in proposals if proposal.get("status") in {"pending", "triggered"}]
        for proposal in pending:
            lines.append(
                f"- {proposal.get('ticker', '')}: {proposal.get('status', '')}; max hold "
                f"{proposal.get('max_holding_days', '') or 'default'} sessions; exit before catalyst "
                f"{proposal.get('exit_before_catalyst', '') or 'unspecified'}."
            )
    else:
        lines.append("- No proposals logged. The control group and picker test cannot work yet.")
    lines.append("")

    recent_signals = [signal for signal in signals if signal.get("timestamp", "")[:10] >= week_start.isoformat()]
    resolved_signals = [
        signal for signal in signals
        if parse_float(signal.get("five_day_return")) is not None
        and signal.get("timestamp", "")[:10] >= (week_start - timedelta(days=14)).isoformat()
    ]
    lines.extend([
        "## Scanner short-horizon outcomes",
        "",
        f"- Signals recorded this week: {len(recent_signals)}; all-time: {len(signals)}.",
    ])
    if resolved_signals:
        lines.extend([
            "",
            "| Date | Ticker | Score | 1d | 5d | 10d | 21d context |",
            "|---|---|---:|---:|---:|---:|---:|",
        ])
        for signal in sorted(resolved_signals, key=lambda row: (row.get("timestamp", ""), row.get("ticker", "")), reverse=True):
            lines.append(
                f"| {signal.get('timestamp', '')[:10]} | {signal.get('ticker', '')} | {signal.get('score', '')} "
                f"| {fmt_pct(parse_float(signal.get('one_day_return')))} "
                f"| {fmt_pct(parse_float(signal.get('five_day_return')))} "
                f"| {fmt_pct(parse_float(signal.get('ten_day_return')))} "
                f"| {fmt_pct(parse_float(signal.get('twenty_one_day_return')))} |"
            )
    else:
        lines.append("- No recent signals have a five-session outcome yet.")
    lines.append("")

    lines.extend(["## Research", ""])
    newest = newest_candidates_file()
    if newest:
        match = re.search(r"candidates-(\d{4}-\d{2}-\d{2})", newest.name)
        file_date = date.fromisoformat(match.group(1)) if match else None
        lines.append(f"- Newest file: `research/{newest.name}`")
        if file_date and (today - file_date).days > STALE_CANDIDATES_DAYS:
            lines.append(f"- ⚠️ Research is {(today - file_date).days} days old.")
        extracted = summary_block(newest)
        if extracted:
            lines.extend(["", *extracted])
    else:
        lines.append("- No candidate file found.")
    lines.append("")

    gap_count = 0
    for trade in all_closed:
        gap_count += sum(not trade.get(field, "").strip() for field in ("followed_plan", "lesson", "stop_price", "setup_type"))
    for trade in open_trades:
        gap_count += sum(not trade.get(field, "").strip() for field in ("sector", "setup_type", "catalyst"))
    lines.extend([
        "## Hygiene",
        "",
        f"- Missing trade fields: {gap_count}." if gap_count else "- No tracked trade-data gaps.",
        "- Run `python scripts/validate_data.py` after every source-data edit.",
        "- Verify catalyst dates against primary sources; distant events remain Early Watch.",
    ])

    output = RESEARCH_DIR / f"digest-{today.isoformat()}.md"
    atomic_write_text(output, "\n".join(lines) + "\n")
    print(f"Wrote {output.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
