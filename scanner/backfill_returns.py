#!/usr/bin/env python3
"""Backfill 1/3/5/10/21-trading-day forward returns for recorded scanner signals.

run_scan.py writes candidates with one_day_return/three_day_return/five_day_return
left blank, since those outcomes don't exist yet at scan time. Nothing else in the
repo ever fills them in, which means the scanner's core purpose -- testing whether
scores had predictive value before paying for better data -- can't be evaluated.

This script reads data/scanner_signals.csv, and for any row where enough trading
days have now elapsed, fetches daily bars from Alpaca and fills in the return
columns relative to the price recorded at scan time. It only ever fills blank
cells; it never overwrites a value that's already there, and it's safe to run
repeatedly (idempotent, non-destructive on missing data/credentials).
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_scan import alpaca_credentials, alpaca_get, load_config  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"

RETURN_OFFSETS = {
    "one_day_return": 1,
    "three_day_return": 3,
    "five_day_return": 5,
    "ten_day_return": 10,
    "twenty_one_day_return": 21,
}


def ensure_return_columns(fieldnames: list[str], rows: list[dict[str, Any]]) -> list[str]:
    """Add any missing return columns (before `notes`) so older files keep working."""
    missing = [f for f in RETURN_OFFSETS if f not in fieldnames]
    if not missing:
        return fieldnames
    insert_at = fieldnames.index("notes") if "notes" in fieldnames else len(fieldnames)
    fieldnames = fieldnames[:insert_at] + missing + fieldnames[insert_at:]
    for row in rows:
        for f in missing:
            row.setdefault(f, "")
    return fieldnames


def read_rows(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return fieldnames, rows


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fetch_bars_for_ticker(ticker: str, start_date: str, config: dict[str, Any]) -> dict[str, float]:
    """Return {YYYY-MM-DD: close} for a ticker from start_date through today."""
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
    out: dict[str, float] = {}
    for bar in bars:
        date = str(bar.get("t", ""))[:10]
        close = bar.get("c")
        if date and close is not None:
            out[date] = float(close)
    return out


def main() -> int:
    config = load_config()

    if not SIGNALS_CSV.exists() or SIGNALS_CSV.stat().st_size == 0:
        print("No scanner_signals.csv to backfill.")
        return 0

    key, secret = alpaca_credentials()
    if not key or not secret:
        print("Alpaca credentials not configured; skipping return backfill.")
        return 0

    fieldnames, rows = read_rows(SIGNALS_CSV)
    original_fieldnames = list(fieldnames)
    fieldnames = ensure_return_columns(fieldnames, rows)
    today = datetime.now(timezone.utc).date()

    pending_by_ticker: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if all(row.get(f) for f in RETURN_OFFSETS):
            continue
        pending_by_ticker.setdefault(row["ticker"], []).append(row)

    if not pending_by_ticker:
        if fieldnames != original_fieldnames:
            write_rows(SIGNALS_CSV, fieldnames, rows)
            print("Migrated signals file to include new return columns.")
        else:
            print("No rows need return backfilling.")
        return 0

    changed = 0
    for ticker, ticker_rows in pending_by_ticker.items():
        oldest_signal_date = min(row["timestamp"][:10] for row in ticker_rows)
        start = (
            datetime.strptime(oldest_signal_date, "%Y-%m-%d").date() - timedelta(days=3)
        ).isoformat()
        try:
            closes = fetch_bars_for_ticker(ticker, start, config)
        except Exception as exc:  # noqa: BLE001 - one bad ticker shouldn't stop the run
            print(f"Skipping {ticker}: {exc}", file=sys.stderr)
            continue

        trading_dates = sorted(closes)
        if not trading_dates:
            continue

        for row in ticker_rows:
            signal_date = row["timestamp"][:10]
            try:
                signal_price = float(row["price"])
            except (KeyError, ValueError):
                continue

            # First trading day on/after the signal date is treated as day 0.
            future_dates = [d for d in trading_dates if d >= signal_date]
            if not future_dates:
                continue
            base_idx = trading_dates.index(future_dates[0])

            row_changed = False
            for field, offset in RETURN_OFFSETS.items():
                if row.get(field):
                    continue
                target_idx = base_idx + offset
                if target_idx >= len(trading_dates):
                    continue  # not enough trading days have elapsed yet
                target_date = trading_dates[target_idx]
                if datetime.strptime(target_date, "%Y-%m-%d").date() > today:
                    continue
                target_close = closes[target_date]
                row[field] = f"{((target_close / signal_price) - 1) * 100:.4f}"
                row_changed = True

            if row_changed:
                changed += 1

    if changed or fieldnames != original_fieldnames:
        write_rows(SIGNALS_CSV, fieldnames, rows)
        print(f"Backfilled returns for {changed} row(s).")
    else:
        print("No rows had enough elapsed trading days yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
