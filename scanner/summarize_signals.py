#!/usr/bin/env python3
"""Summarize recorded scanner signals into research/scanner-summary.md.

Answers the question the raw CSV can't: how did the runners the scanner flagged
actually end up 1 day / 1 week / 2 weeks / 1 month later? Groups outcomes by
score bucket and source so the 30-day evaluation in docs/SCANNER_WORKFLOW.md
has something readable to work from.

Derived artifact only: regenerated from data/scanner_signals.csv on every run,
never edited by hand, and never a trade signal. Not financial advice.
"""

from __future__ import annotations

import csv
import statistics
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
SUMMARY_MD = REPO_ROOT / "research/scanner-summary.md"

HORIZONS = [
    ("one_day_return", "1d"),
    ("three_day_return", "3d"),
    ("five_day_return", "5d"),
    ("ten_day_return", "10d"),
    ("twenty_one_day_return", "21d"),
]

# 40-59 exists because min_score_to_record was temporarily 40 (2026-06-30 to
# 2026-07-01); keep it as its own bucket per docs/SCANNER_WORKFLOW.md.
BUCKETS = [(40, 59), (60, 69), (70, 79), (80, 999)]


def bucket_label(lo: int, hi: int) -> str:
    return f"{lo}+" if hi >= 999 else f"{lo}-{hi}"


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fmt_pct(value: float | None) -> str:
    return "—" if value is None else f"{value:+.2f}%"


def horizon_stats(rows: list[dict[str, str]], field: str) -> dict[str, float | int] | None:
    values = [v for row in rows if (v := parse_float(row.get(field))) is not None]
    if not values:
        return None
    return {
        "n": len(values),
        "avg": statistics.mean(values),
        "median": statistics.median(values),
        "hit_rate": 100.0 * sum(1 for v in values if v > 0) / len(values),
        "best": max(values),
        "worst": min(values),
    }


def stats_table(groups: list[tuple[str, list[dict[str, str]]]]) -> list[str]:
    lines = [
        "| Group | Signals | Horizon | Filled | Avg | Median | Hit rate | Best | Worst |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, rows in groups:
        if not rows:
            continue
        printed_any = False
        for field, hname in HORIZONS:
            s = horizon_stats(rows, field)
            if s is None:
                continue
            group_cell = label if not printed_any else ""
            count_cell = str(len(rows)) if not printed_any else ""
            lines.append(
                f"| {group_cell} | {count_cell} | {hname} | {s['n']} | {fmt_pct(s['avg'])} "
                f"| {fmt_pct(s['median'])} | {s['hit_rate']:.0f}% "
                f"| {fmt_pct(s['best'])} | {fmt_pct(s['worst'])} |"
            )
            printed_any = True
        if not printed_any:
            lines.append(f"| {label} | {len(rows)} | — | 0 | — | — | — | — | — |")
    return lines


def main() -> int:
    if not SIGNALS_CSV.exists() or SIGNALS_CSV.stat().st_size == 0:
        print("No scanner_signals.csv to summarize.")
        return 0

    with SIGNALS_CSV.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("Signals file has no rows.")
        return 0

    rows.sort(key=lambda r: (r.get("timestamp", ""), r.get("ticker", "")))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines: list[str] = []
    lines.append("# Scanner Signal Summary")
    lines.append("")
    lines.append(f"Auto-generated from `data/scanner_signals.csv` on {now}. Do not edit by hand.")
    lines.append("")
    lines.append("Not financial advice and not a trade signal. Returns are close-to-signal-price")
    lines.append("moves on IEX data; the signal price is an intraday snapshot, so treat these as")
    lines.append("rough process measurements, not precise performance numbers. Small sample sizes")
    lines.append("prove nothing — look for patterns only once dozens of rows have filled in.")
    lines.append("")

    filled_1d = sum(1 for r in rows if parse_float(r.get("one_day_return")) is not None)
    filled_21d = sum(1 for r in rows if parse_float(r.get("twenty_one_day_return")) is not None)
    lines.append("## Coverage")
    lines.append("")
    lines.append(f"- Signals recorded: {len(rows)}")
    lines.append(f"- With 1-day outcome: {filled_1d}")
    lines.append(f"- With 21-day outcome: {filled_21d}")
    lines.append("")

    lines.append("## Outcomes by score bucket")
    lines.append("")
    bucket_groups = []
    for lo, hi in BUCKETS:
        members = [r for r in rows if lo <= int(parse_float(r.get("score")) or 0) <= hi]
        bucket_groups.append((bucket_label(lo, hi), members))
    lines.extend(stats_table(bucket_groups))
    lines.append("")

    lines.append("## Outcomes by source")
    lines.append("")
    sources = sorted({r.get("source", "") for r in rows if r.get("source")})
    source_groups = [(src, [r for r in rows if r.get("source") == src]) for src in sources]
    lines.extend(stats_table(source_groups))
    lines.append("")

    lines.append("## Runner board (every recorded signal)")
    lines.append("")
    lines.append("| Date | Ticker | Score | Signal price | Day move | 1d | 5d | 10d | 21d |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in sorted(rows, key=lambda r: (r.get("timestamp", ""), r.get("ticker", "")), reverse=True):
        lines.append(
            "| {date} | {ticker} | {score} | {price} | {move} | {r1} | {r5} | {r10} | {r21} |".format(
                date=r.get("timestamp", "")[:10],
                ticker=r.get("ticker", ""),
                score=r.get("score", ""),
                price=r.get("price", "") or "—",
                move=fmt_pct(parse_float(r.get("change_pct"))),
                r1=fmt_pct(parse_float(r.get("one_day_return"))),
                r5=fmt_pct(parse_float(r.get("five_day_return"))),
                r10=fmt_pct(parse_float(r.get("ten_day_return"))),
                r21=fmt_pct(parse_float(r.get("twenty_one_day_return"))),
            )
        )
    lines.append("")

    lines.append("## How to read this")
    lines.append("")
    lines.append("- **Hit rate** = share of filled outcomes that were positive at that horizon.")
    lines.append("- If higher score buckets don't show better outcomes than lower ones once the")
    lines.append("  sample grows, the score has no edge and chasing alerts is unjustified.")
    lines.append("- Compare against trades in `trades.csv` with `source = scanner` to see whether")
    lines.append("  your selection among alerts beats the alert average.")

    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {SUMMARY_MD.relative_to(REPO_ROOT)} ({len(rows)} signals).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
