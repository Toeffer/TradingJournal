#!/usr/bin/env python3
"""Shared access to the self-accumulating EU quote history.

The FMP plan in use provides real-time XETRA/LSE quotes but not historical
bars, so the EU scanner builds its own history: every scan day it upserts one
row per ticker into data/eu_quote_history.csv (the last run of the day — the
post-close run — finalizes that day's open/high/low/close/volume). After ~20
sessions the derived metrics (20d average volume, 20d highs) reach full
quality; until then consumers must degrade gracefully.

Bars are exposed Alpaca-shaped ({"t","o","h","l","c","v"}) so
backfill_returns.py and simulate_proposals.py can treat EU tickers exactly
like US ones, just with a local data source.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
HISTORY_CSV = REPO_ROOT / "data/eu_quote_history.csv"

FIELDS = [
    "date",
    "ticker",
    "exchange",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "avg_volume_reported",
]

EU_SUFFIXES = (".DE", ".L")


def is_eu_symbol(ticker: str) -> bool:
    return ticker.upper().endswith(EU_SUFFIXES)


def load_rows(path: Path = HISTORY_CSV) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def bars_for(ticker: str, path: Path = HISTORY_CSV) -> list[dict[str, Any]]:
    """Alpaca-shaped daily bars for one ticker, oldest first."""
    bars: list[dict[str, Any]] = []
    for row in load_rows(path):
        if row.get("ticker", "").upper() != ticker.upper():
            continue
        try:
            bars.append(
                {
                    "t": row["date"],
                    "o": float(row["open"]) if row.get("open") else None,
                    "h": float(row["high"]) if row.get("high") else None,
                    "l": float(row["low"]) if row.get("low") else None,
                    "c": float(row["close"]) if row.get("close") else None,
                    "v": float(row["volume"]) if row.get("volume") else 0.0,
                }
            )
        except ValueError:
            continue
    return sorted(bars, key=lambda b: b["t"])


def merge_bars(
    bars_by_ticker: dict[str, list[dict[str, Any]]],
    today: str,
    path: Path = HISTORY_CSV,
) -> int:
    """Backfill history bars, filling only (date, ticker) rows that don't exist
    yet — never overwriting scanner-accumulated or seeded data. Bars dated
    `today` or later are skipped: the live scanner owns today via upsert_today.

    Bar dicts use the seeder's shape: date/open/high/low/close/volume.
    Returns the number of rows added.
    """
    existing = load_rows(path)
    have = {(r["date"], r["ticker"].upper()) for r in existing}
    added = 0
    for ticker, bars in bars_by_ticker.items():
        exchange = "LSE" if ticker.upper().endswith(".L") else "XETRA"
        for bar in bars:
            date_str = str(bar["date"])
            key = (date_str, ticker.upper())
            if date_str >= today or key in have or bar.get("close") is None:
                continue
            existing.append(
                {
                    "date": date_str,
                    "ticker": ticker.upper(),
                    "exchange": exchange,
                    "open": "" if bar.get("open") is None else f"{bar['open']:.4f}",
                    "high": "" if bar.get("high") is None else f"{bar['high']:.4f}",
                    "low": "" if bar.get("low") is None else f"{bar['low']:.4f}",
                    "close": f"{bar['close']:.4f}",
                    "volume": int(bar.get("volume") or 0),
                    "avg_volume_reported": "",
                }
            )
            have.add(key)
            added += 1
    if added:
        existing.sort(key=lambda r: (r.get("date", ""), r.get("ticker", "")))
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for r in existing:
                writer.writerow({k: r.get(k, "") for k in FIELDS})
    return added


def upsert_today(date_str: str, rows_by_ticker: dict[str, dict[str, Any]], path: Path = HISTORY_CSV) -> None:
    """One row per (date, ticker); a later run the same day replaces the earlier
    row, so the final (post-close) scan of the day finalizes that day's bar."""
    existing = load_rows(path)
    keep = [r for r in existing if not (r.get("date") == date_str and r.get("ticker", "").upper() in rows_by_ticker)]
    for ticker, row in rows_by_ticker.items():
        keep.append({**row, "date": date_str, "ticker": ticker})
    keep.sort(key=lambda r: (r.get("date", ""), r.get("ticker", "")))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in keep:
            writer.writerow({k: r.get(k, "") for k in FIELDS})
