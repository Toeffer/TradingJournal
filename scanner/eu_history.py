#!/usr/bin/env python3
"""Shared access to the self-accumulating EU quote history."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from io_utils import atomic_write_csv

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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bars_for(ticker: str, path: Path = HISTORY_CSV) -> list[dict[str, Any]]:
    """Return Alpaca-shaped daily bars for one ticker, oldest first."""
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
    return sorted(bars, key=lambda bar: bar["t"])


def merge_bars(
    bars_by_ticker: dict[str, list[dict[str, Any]]],
    today: str,
    path: Path = HISTORY_CSV,
) -> int:
    """Add missing historical bars without overwriting existing or today's rows."""
    existing = load_rows(path)
    have = {(row["date"], row["ticker"].upper()) for row in existing}
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
        existing.sort(key=lambda row: (row.get("date", ""), row.get("ticker", "")))
        atomic_write_csv(path, FIELDS, existing)
    return added


def upsert_today(
    date_str: str,
    rows_by_ticker: dict[str, dict[str, Any]],
    path: Path = HISTORY_CSV,
) -> None:
    """Replace the current day's row per ticker; later scans finalize the day."""
    existing = load_rows(path)
    keep = [
        row
        for row in existing
        if not (
            row.get("date") == date_str
            and row.get("ticker", "").upper() in rows_by_ticker
        )
    ]
    for ticker, row in rows_by_ticker.items():
        keep.append({**row, "date": date_str, "ticker": ticker})
    keep.sort(key=lambda row: (row.get("date", ""), row.get("ticker", "")))
    atomic_write_csv(path, FIELDS, keep)
