#!/usr/bin/env python3
"""Generate the Monday-morning weekly digest into research/digest-YYYY-MM-DD.md.

One page combining what already exists — journal results, scanner runner
outcomes, and the newest candidate shortlist — so the week starts from data
instead of memory. Runs from .github/workflows/digest.yml every Monday.

Derived artifact: computed only from trades.csv, data/scanner_signals.csv and
files in research/. Nothing here is estimated, invented, or advice. The digest
surfaces; the human decides.
"""

from __future__ import annotations

import csv
import re
from datetime import date, timedelta
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from journal_stats import parse_float, r_stats, fmt  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
TRADES_CSV = REPO_ROOT / "trades.csv"
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
RESEARCH_DIR = REPO_ROOT / "research"

CATALYST_LOOKAHEAD_DAYS = 14
STALE_CANDIDATES_DAYS = 10


def fmt_pct(value: float | None) -> str:
    return "—" if value is None else f"{value:+.2f}%"


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def newest_candidates_file() -> Path | None:
    files = sorted(RESEARCH_DIR.glob("candidates-*.md"))
    return files[-1] if files else None


def candidates_summary(path: Path) -> list[str]:
    """Extract the '## Summary' block from a candidates file, if present."""
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    in_summary = False
    for line in lines:
        if line.startswith("## "):
            if in_summary:
                break
            in_summary = line.strip().lower() == "## summary"
            continue
        if in_summary and line.strip():
            out.append(line)
    return out


def main() -> int:
    today = date.today()
    week_start = today - timedelta(days=7)
    trades = load_csv(TRADES_CSV)
    signals = load_csv(SIGNALS_CSV)

    closed_week = [
        t for t in trades
        if t.get("status") == "closed" and t.get("date_closed")
        and week_start.isoformat() <= t["date_closed"] < today.isoformat()
    ]
    open_trades = [t for t in trades if t.get("status") == "open"]
    all_closed = [t for t in trades if t.get("status") == "closed"]

    lines: list[str] = []
    lines.append(f"# Weekly Digest — {today.isoformat()}")
    lines.append("")
    lines.append(f"Auto-generated for the week {week_start.isoformat()} to {today.isoformat()}.")
    lines.append("Computed from trades.csv, scanner signals, and research files. Not advice —")
    lines.append("this page surfaces what happened; decisions and catalyst verification are yours.")
    lines.append("")

    # --- Journal ---
    lines.append("## Journal: last 7 days")
    lines.append("")
    if closed_week:
        week_rs = [v for t in closed_week if (v := parse_float(t.get("r_multiple"))) is not None]
        lines.append("| Trade | Ticker | Closed | R | P&L (€) | Followed plan |")
        lines.append("|---|---|---|---:|---:|---|")
        for t in sorted(closed_week, key=lambda t: t.get("date_closed", "")):
            lines.append(
                f"| {t.get('trade_id','')} | {t.get('ticker','')} | {t.get('date_closed','')} "
                f"| {fmt(parse_float(t.get('r_multiple')))} | {fmt(parse_float(t.get('pnl')))} "
                f"| {t.get('followed_plan','') or '—'} |"
            )
        lines.append("")
        lines.append(f"- Realized this week: **{fmt(sum(week_rs) if week_rs else None)}R** "
                     f"across {len(closed_week)} closed trade(s).")
    else:
        lines.append("No trades closed this week.")
    s = r_stats(all_closed)
    lines.append(f"- All-time: {s['n']} closed, expectancy {fmt(s['expectancy_r'])}R, "
                 f"total P&L {fmt(s['total_pnl'])} €. Details: `research/journal-stats.md`.")
    lines.append("")

    lines.append("### Open positions and upcoming catalysts")
    lines.append("")
    if open_trades:
        horizon = today + timedelta(days=CATALYST_LOOKAHEAD_DAYS)
        lines.append("| Trade | Ticker | Entry | Stop | Catalyst | Date | Within 14d? |")
        lines.append("|---|---|---:|---:|---|---|---|")
        for t in open_trades:
            cat_date = t.get("catalyst_date", "").strip()
            soon = ""
            if cat_date:
                try:
                    d = date.fromisoformat(cat_date)
                    if d <= horizon:
                        soon = "**YES — verify date & earnings-hold rule**"
                except ValueError:
                    soon = "unparseable date"
            lines.append(
                f"| {t.get('trade_id','')} | {t.get('ticker','')} | {t.get('entry_price','') or '—'} "
                f"| {t.get('stop_price','') or '—'} | {t.get('catalyst','') or '—'} "
                f"| {cat_date or '—'} | {soon or '—'} |"
            )
    else:
        lines.append("No open positions.")
    lines.append("")

    # --- Scanner ---
    lines.append("## Scanner: how the runners ended up")
    lines.append("")
    week_signals = [s_ for s_ in signals if s_.get("timestamp", "")[:10] >= week_start.isoformat()]
    lines.append(f"- Signals recorded this week: {len(week_signals)} "
                 f"(all-time: {len(signals)}). Full stats: `research/scanner-summary.md`.")
    resolved = [
        s_ for s_ in signals
        if parse_float(s_.get("five_day_return")) is not None
        and s_.get("timestamp", "")[:10] >= (week_start - timedelta(days=14)).isoformat()
    ]
    if resolved:
        lines.append("")
        lines.append("Recent signals with a 5-day outcome now known:")
        lines.append("")
        lines.append("| Date | Ticker | Score | 1d | 5d | 10d | 21d |")
        lines.append("|---|---|---:|---:|---:|---:|---:|")
        for s_ in sorted(resolved, key=lambda r: (r.get("timestamp", ""), r.get("ticker", "")), reverse=True):
            lines.append(
                f"| {s_.get('timestamp','')[:10]} | {s_.get('ticker','')} | {s_.get('score','')} "
                f"| {fmt_pct(parse_float(s_.get('one_day_return')))} "
                f"| {fmt_pct(parse_float(s_.get('five_day_return')))} "
                f"| {fmt_pct(parse_float(s_.get('ten_day_return')))} "
                f"| {fmt_pct(parse_float(s_.get('twenty_one_day_return')))} |"
            )
    else:
        lines.append("- No recent signals have a 5-day outcome yet.")
    lines.append("")

    # --- Proposals ---
    proposals = load_csv(REPO_ROOT / "data/proposals.csv")
    if proposals:
        lines.append("## Proposals (SETUPS.md pipeline)")
        lines.append("")
        by_status: dict[str, int] = {}
        for p in proposals:
            by_status[p.get("status", "?")] = by_status.get(p.get("status", "?"), 0) + 1
        lines.append("- " + " | ".join(f"{k}: {v}" for k, v in sorted(by_status.items())))
        resolved = [p for p in proposals if p.get("status") in ("stopped", "target", "timeout")]
        rs = [v for p in resolved if (v := parse_float(p.get("sim_r"))) is not None]
        if rs:
            lines.append(f"- Simulated expectancy across {len(rs)} resolved proposal(s): "
                         f"**{fmt(sum(rs) / len(rs))}R**. Details: `research/proposal-stats.md`.")
        pending = [p for p in proposals if p.get("status") in ("pending", "triggered")]
        if pending:
            lines.append("- Waiting: " + ", ".join(
                f"{p.get('ticker','')} ({p.get('status','')}, entry {p.get('entry_price','')})"
                for p in pending))
        lines.append("")

    # --- Research ---
    lines.append("## Research: newest candidate shortlist")
    lines.append("")
    newest = newest_candidates_file()
    if newest:
        match = re.search(r"candidates-(\d{4}-\d{2}-\d{2})", newest.name)
        file_date = date.fromisoformat(match.group(1)) if match else None
        lines.append(f"- Newest file: `research/{newest.name}`")
        if file_date and (today - file_date).days > STALE_CANDIDATES_DAYS:
            lines.append(f"- ⚠️ Shortlist is {(today - file_date).days} days old — "
                         "check whether the weekly routine is still running.")
        summary = candidates_summary(newest)
        if summary:
            lines.append("")
            lines.extend(summary)
    else:
        lines.append("- No candidates file found in research/.")
    lines.append("")

    # --- Hygiene ---
    lines.append("## Hygiene")
    lines.append("")
    gap_count = 0
    for t in all_closed:
        gap_count += sum(1 for f in ("followed_plan", "lesson", "stop_price", "setup_type")
                         if not t.get(f, "").strip())
    for t in open_trades:
        gap_count += sum(1 for f in ("sector", "setup_type", "catalyst")
                         if not t.get(f, "").strip())
    if gap_count:
        lines.append(f"- {gap_count} missing field(s) across trades — see the data-gaps list "
                     "in `research/journal-stats.md`. Blank fields make the reviews blind.")
    else:
        lines.append("- No data gaps. Journal is fully recorded.")
    no_stop = [t.get("ticker") for t in open_trades if parse_float(t.get("stop_price")) is None]
    if no_stop:
        lines.append(f"- ⚠️ Open with no stop: {', '.join(no_stop)} — undefined risk.")
    lines.append("")

    lines.append("## Reminders")
    lines.append("")
    lines.append("- Verify every catalyst date against a primary source before acting on it.")
    if open_trades:
        lines.append("- Walk each open position through the exit-review checklist in "
                     "`AGENTS.md` (HOLD / exhaustion / breakdown / catalyst override).")
    lines.append("- Scanner scores and shortlists surface names for research, never trades.")
    lines.append("- Log `followed_plan` and a one-line `lesson` at every close — that is the")
    lines.append("  raw material the monthly review runs on.")

    out_path = RESEARCH_DIR / f"digest-{today.isoformat()}.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
