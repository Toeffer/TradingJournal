#!/usr/bin/env python3
"""One-time backfill of the EU quote history from Stooq daily data.

Fetches full daily OHLCV history (free, keyless) for every ticker in
scanner/universe_eu.txt and merges the last LOOKBACK_DAYS bars into
data/eu_quote_history.csv — only filling (date, ticker) rows that don't
exist yet, never overwriting scanner-accumulated data. Today's (possibly
partial) bar is skipped; the live scanner owns today.

Run once via the EU Scanner workflow's `seed_history` dispatch input (or
locally). This removes the accumulator's warm-up entirely: 20d/50d breakout
components have real history from day one. ~1 request per ticker with a
polite delay — do not loop this script.
"""

from __future__ import annotations

import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stooq_eu  # noqa: E402
from eu_history import FIELDS, HISTORY_CSV, load_rows  # noqa: E402
from run_scan import read_ticker_list  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = REPO_ROOT / "scanner/universe_eu.txt"
LOOKBACK_DAYS = 90  # calendar bars kept per ticker; covers the 50-day lookback


def main() -> int:
    import csv

    tickers = read_ticker_list(UNIVERSE)
    if not tickers:
        print("No tickers in EU universe; nothing to seed.")
        return 0

    existing = load_rows()
    have = {(r["date"], r["ticker"].upper()) for r in existing}
    today = date.today().isoformat()

    added = 0
    failed: list[str] = []
    for ticker in tickers:
        try:
            bars = stooq_eu.fetch_daily_history(ticker)
        except Exception as exc:  # noqa: BLE001 - one bad ticker shouldn't stop the seed
            failed.append(f"{ticker}: {exc}")
            continue
        exchange = "LSE" if ticker.upper().endswith(".L") else "XETRA"
        for bar in bars[-LOOKBACK_DAYS:]:
            key = (str(bar["date"]), ticker.upper())
            if bar["date"] >= today or key in have:
                continue
            existing.append(
                {
                    "date": str(bar["date"]),
                    "ticker": ticker.upper(),
                    "exchange": exchange,
                    "open": "" if bar["open"] is None else f"{bar['open']:.4f}",
                    "high": "" if bar["high"] is None else f"{bar['high']:.4f}",
                    "low": "" if bar["low"] is None else f"{bar['low']:.4f}",
                    "close": f"{bar['close']:.4f}",
                    "volume": int(bar["volume"] or 0),
                    "avg_volume_reported": "",
                }
            )
            have.add(key)
            added += 1
        time.sleep(1.0)

    if added:
        existing.sort(key=lambda r: (r.get("date", ""), r.get("ticker", "")))
        HISTORY_CSV.parent.mkdir(parents=True, exist_ok=True)
        with HISTORY_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for row in existing:
                writer.writerow({k: row.get(k, "") for k in FIELDS})

    print(f"Seeded {added} bar(s) across {len(tickers) - len(failed)} ticker(s).")
    if failed:
        print("Failed tickers:")
        for f_ in failed:
            print(f"  - {f_}")
    if added == 0 and tickers:
        # Zero bars across a whole universe of liquid names is never "success" —
        # it means the data source returned nothing usable (Stooq serves its
        # rate-limit/block page with HTTP 200, which parses to zero bars).
        # Exit nonzero so the Actions run shows red instead of green.
        print(
            "ERROR: no bars were seeded for any ticker. "
            f"{stooq_eu.BLOCKED_HINT} "
            "Seeding from GitHub-hosted runners does not work; run this script "
            "locally and commit data/eu_quote_history.csv instead.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
