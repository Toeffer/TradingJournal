#!/usr/bin/env python3
"""Backfill 1/3/5/10/21-trading-day forward returns for scanner signals.

The short horizons (1/3/5/10) are the primary evaluation windows. Twenty-one
trading days remains a slow context measure, not the default holding assumption.
Only blank cells are filled, so the operation is idempotent.
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_history import bars_for as eu_bars_for, is_eu_symbol  # noqa: E402
from io_utils import atomic_write_csv  # noqa: E402
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
    missing = [field for field in RETURN_OFFSETS if field not in fieldnames]
    if not missing:
        return fieldnames
    insert_at = fieldnames.index("notes") if "notes" in fieldnames else len(fieldnames)
    updated = fieldnames[:insert_at] + missing + fieldnames[insert_at:]
    for row in rows:
        for field in missing:
            row.setdefault(field, "")
    return updated


def read_rows(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def fetch_bars_for_ticker(ticker: str, start_date: str, config: dict[str, Any]) -> dict[str, float]:
    """Return adjusted closes keyed by YYYY-MM-DD."""
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
    output: dict[str, float] = {}
    for bar in data.get("bars", {}).get(ticker, []):
        date_str = str(bar.get("t", ""))[:10]
        close = bar.get("c")
        if date_str and close is not None:
            output[date_str] = float(close)
    return output


def main() -> int:
    if not SIGNALS_CSV.exists() or SIGNALS_CSV.stat().st_size == 0:
        print("No scanner_signals.csv to backfill.")
        return 0

    fieldnames, rows = read_rows(SIGNALS_CSV)
    original_fieldnames = list(fieldnames)
    fieldnames = ensure_return_columns(fieldnames, rows)
    today = datetime.now(timezone.utc).date()

    pending_by_ticker: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if all(row.get(field) for field in RETURN_OFFSETS):
            continue
        pending_by_ticker.setdefault(row["ticker"], []).append(row)

    if not pending_by_ticker:
        if fieldnames != original_fieldnames:
            atomic_write_csv(SIGNALS_CSV, fieldnames, rows)
            print("Migrated signals file to include return columns.")
        else:
            print("No rows need return backfilling.")
        return 0

    config = load_config()
    key, secret = alpaca_credentials()
    changed = 0
    for ticker, ticker_rows in pending_by_ticker.items():
        oldest_signal_date = min(row["timestamp"][:10] for row in ticker_rows)
        start = (
            datetime.strptime(oldest_signal_date, "%Y-%m-%d").date() - timedelta(days=3)
        ).isoformat()
        try:
            if is_eu_symbol(ticker):
                closes = {
                    bar["t"]: bar["c"]
                    for bar in eu_bars_for(ticker)
                    if bar["c"] is not None
                }
            elif key and secret:
                closes = fetch_bars_for_ticker(ticker, start, config)
            else:
                print(f"Skipping {ticker}: Alpaca credentials not configured.", file=sys.stderr)
                continue
        except Exception as exc:  # noqa: BLE001 - one bad ticker must not block others
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

            future_dates = [date_str for date_str in trading_dates if date_str >= signal_date]
            if not future_dates:
                continue
            base_idx = trading_dates.index(future_dates[0])
            row_changed = False
            for field, offset in RETURN_OFFSETS.items():
                if row.get(field):
                    continue
                target_idx = base_idx + offset
                if target_idx >= len(trading_dates):
                    continue
                target_date = trading_dates[target_idx]
                if datetime.strptime(target_date, "%Y-%m-%d").date() > today:
                    continue
                row[field] = f"{((closes[target_date] / signal_price) - 1) * 100:.4f}"
                row_changed = True
            if row_changed:
                changed += 1

    if changed or fieldnames != original_fieldnames:
        atomic_write_csv(SIGNALS_CSV, fieldnames, rows)
        print(f"Backfilled returns for {changed} row(s).")
    else:
        print("No rows had enough elapsed trading days yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
