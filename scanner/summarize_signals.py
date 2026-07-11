#!/usr/bin/env python3
"""Summarize recorded scanner-signal outcomes.

The 1/3/5/10-session results are the primary evaluation windows. Twenty-one
sessions is retained as slower context and must not be read as a recommended hold.
"""

from __future__ import annotations

import csv
import statistics
from datetime import datetime, timezone
from pathlib import Path

from io_utils import atomic_write_text

REPO_ROOT = Path(__file__).resolve().parents[1]
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
SUMMARY_MD = REPO_ROOT / "research/scanner-summary.md"

HORIZONS = [
    ("one_day_return", "1d", "primary"),
    ("three_day_return", "3d", "primary"),
    ("five_day_return", "5d", "primary"),
    ("ten_day_return", "10d", "primary"),
    ("twenty_one_day_return", "21d", "context"),
]
BUCKETS = [(40, 59), (60, 69), (70, 79), (80, 999)]


def bucket_label(low: int, high: int) -> str:
    return f"{low}+" if high >= 999 else f"{low}-{high}"


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
    values = [value for row in rows if (value := parse_float(row.get(field))) is not None]
    if not values:
        return None
    return {
        "n": len(values),
        "avg": statistics.mean(values),
        "median": statistics.median(values),
        "hit_rate": 100.0 * sum(value > 0 for value in values) / len(values),
        "best": max(values),
        "worst": min(values),
    }


def stats_table(groups: list[tuple[str, list[dict[str, str]]]]) -> list[str]:
    lines = [
        "| Group | Signals | Horizon | Role | Filled | Avg | Median | Hit rate | Best | Worst |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, rows in groups:
        if not rows:
            continue
        printed = False
        for field, horizon, role in HORIZONS:
            stats = horizon_stats(rows, field)
            if stats is None:
                continue
            lines.append(
                f"| {label if not printed else ''} | {len(rows) if not printed else ''} | {horizon} | {role} "
                f"| {stats['n']} | {fmt_pct(stats['avg'])} | {fmt_pct(stats['median'])} "
                f"| {stats['hit_rate']:.0f}% | {fmt_pct(stats['best'])} | {fmt_pct(stats['worst'])} |"
            )
            printed = True
        if not printed:
            lines.append(f"| {label} | {len(rows)} | — | — | 0 | — | — | — | — | — |")
    return lines


def main() -> int:
    if not SIGNALS_CSV.exists() or SIGNALS_CSV.stat().st_size == 0:
        print("No scanner_signals.csv to summarize.")
        return 0

    with SIGNALS_CSV.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        print("Signals file has no rows.")
        return 0

    rows.sort(key=lambda row: (row.get("timestamp", ""), row.get("ticker", "")))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    filled_1d = sum(parse_float(row.get("one_day_return")) is not None for row in rows)
    filled_10d = sum(parse_float(row.get("ten_day_return")) is not None for row in rows)
    filled_21d = sum(parse_float(row.get("twenty_one_day_return")) is not None for row in rows)

    lines = [
        "# Scanner Signal Summary",
        "",
        f"Auto-generated from `data/scanner_signals.csv` on {now}. Do not edit by hand.",
        "",
        "Not financial advice and not a trade signal. Signal prices are intraday snapshots.",
        "The 1/3/5/10-day columns are the primary scanner evaluation. The 21-day column is",
        "slow context only; it is not a holding-period recommendation. Small, repeated, or",
        "provider-mixed samples are descriptive—not evidence of an edge.",
        "",
        "## Coverage",
        "",
        f"- Signals recorded: {len(rows)}",
        f"- With 1-day outcome: {filled_1d}",
        f"- With 10-day outcome: {filled_10d}",
        f"- With 21-day context outcome: {filled_21d}",
        "",
        "## Outcomes by score bucket",
        "",
    ]

    bucket_groups: list[tuple[str, list[dict[str, str]]]] = []
    for low, high in BUCKETS:
        members = [
            row for row in rows
            if low <= int(parse_float(row.get("score")) or 0) <= high
        ]
        bucket_groups.append((bucket_label(low, high), members))
    lines.extend(stats_table(bucket_groups))
    lines.extend(["", "## Outcomes by source", ""])

    sources = sorted({row.get("source", "") for row in rows if row.get("source")})
    lines.extend(stats_table([(source, [row for row in rows if row.get("source") == source]) for source in sources]))
    lines.append("")

    markets = sorted({row.get("market", "") for row in rows if row.get("market")})
    if len(markets) > 1:
        lines.extend(["## Outcomes by market", ""])
        lines.extend(stats_table([(market, [row for row in rows if row.get("market") == market]) for market in markets]))
        lines.append("")

    lines.extend([
        "## Runner board",
        "",
        "| Date | Ticker | Market | Score | Signal price | Day move | 1d | 5d | 10d | 21d context |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for row in sorted(rows, key=lambda item: (item.get("timestamp", ""), item.get("ticker", "")), reverse=True):
        lines.append(
            f"| {row.get('timestamp', '')[:10]} | {row.get('ticker', '')} | {row.get('market', '')} "
            f"| {row.get('score', '')} | {row.get('price', '') or '—'} "
            f"| {fmt_pct(parse_float(row.get('change_pct')))} "
            f"| {fmt_pct(parse_float(row.get('one_day_return')))} "
            f"| {fmt_pct(parse_float(row.get('five_day_return')))} "
            f"| {fmt_pct(parse_float(row.get('ten_day_return')))} "
            f"| {fmt_pct(parse_float(row.get('twenty_one_day_return')))} |"
        )

    lines.extend([
        "",
        "## Interpretation guardrails",
        "",
        "- Compare medians as well as averages; one crash or squeeze can dominate the mean.",
        "- Do not compare score buckets with only a handful of filled outcomes.",
        "- Repeated observations in the same ticker are not independent evidence.",
        "- US and EU scores/providers should be evaluated separately before being combined.",
        "- If higher score buckets do not improve short-horizon outcomes after a meaningful sample,",
        "  the score has not earned a role in decisions.",
    ])

    atomic_write_text(SUMMARY_MD, "\n".join(lines) + "\n")
    print(f"Wrote {SUMMARY_MD.relative_to(REPO_ROOT)} ({len(rows)} signals).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
