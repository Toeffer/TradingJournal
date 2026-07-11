#!/usr/bin/env python3
"""Build a normalized market-data snapshot for model-neutral research runs.

The snapshot is intentionally provider-agnostic. It converts the latest scanner
observation per ticker into one stable CSV so different models receive identical
market context. Fundamental fields that the current providers do not supply remain
blank rather than being invented.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
REGIME_CSV = REPO_ROOT / "data/market_regime.csv"
OUTPUT_CSV = REPO_ROOT / "data/research_snapshot.csv"
OUTPUT_META = REPO_ROOT / "data/research_snapshot.meta.json"

FIELDS = [
    "as_of",
    "ticker",
    "company",
    "market",
    "exchange",
    "currency",
    "price",
    "market_cap",
    "avg_volume_20d",
    "avg_dollar_volume",
    "change_pct",
    "rel_volume",
    "score",
    "break_20d_high",
    "extension_5d_pct",
    "rsi14",
    "ema20_dist_pct",
    "ema50_dist_pct",
    "macd_hist_pct",
    "bb_percent_b",
    "market_regime",
    "signal_source",
    "signal_timestamp",
    "data_source",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def format_number(value: float | None, digits: int = 4) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def listing_for(ticker: str, market: str) -> tuple[str, str]:
    upper = ticker.upper()
    market_upper = market.upper()
    if upper.endswith(".DE") or "XETRA" in market_upper:
        return "XETRA", "EUR"
    if upper.endswith(".L") or "LSE" in market_upper:
        return "LSE", "GBP"
    return (market if market and market != "US" else "US", "USD")


def latest_regime(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    ordered = sorted(rows, key=lambda row: row.get("timestamp") or row.get("date") or "")
    return ordered[-1].get("regime", "")


def latest_signals(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    latest: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        ticker = row.get("ticker", "").strip().upper()
        if not ticker:
            continue
        market = row.get("market", "US").strip() or "US"
        key = (market, ticker)
        if key not in latest or row.get("timestamp", "") > latest[key].get("timestamp", ""):
            latest[key] = row
    return [latest[key] for key in sorted(latest)]


def build_rows(
    signal_rows: list[dict[str, str]],
    regime: str,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in latest_signals(signal_rows):
        ticker = row.get("ticker", "").strip().upper()
        market = row.get("market", "US").strip() or "US"
        exchange, currency = listing_for(ticker, market)
        price = parse_float(row.get("price"))
        avg_volume = parse_float(row.get("avg_volume_20d"))
        avg_dollar_volume = (
            price * avg_volume if price is not None and avg_volume is not None else None
        )
        signal_source = row.get("source", "")
        notes = row.get("notes", "") or row.get("warnings", "")
        output.append(
            {
                "as_of": row.get("timestamp", ""),
                "ticker": ticker,
                "company": "",
                "market": market,
                "exchange": exchange,
                "currency": currency,
                "price": format_number(price),
                "market_cap": "",
                "avg_volume_20d": format_number(avg_volume),
                "avg_dollar_volume": format_number(avg_dollar_volume, 2),
                "change_pct": row.get("change_pct", ""),
                "rel_volume": row.get("rel_volume", ""),
                "score": row.get("score", ""),
                "break_20d_high": row.get("break_20d_high", ""),
                "extension_5d_pct": row.get("extension_5d_pct", ""),
                "rsi14": row.get("rsi14", ""),
                "ema20_dist_pct": row.get("ema20_dist_pct", ""),
                "ema50_dist_pct": row.get("ema50_dist_pct", ""),
                "macd_hist_pct": row.get("macd_hist_pct", ""),
                "bb_percent_b": row.get("bb_percent_b", ""),
                "market_regime": regime,
                "signal_source": signal_source,
                "signal_timestamp": row.get("timestamp", ""),
                "data_source": signal_source or market,
                "notes": notes,
            }
        )
    return output


def csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def build_snapshot(
    signals_path: Path = SIGNALS_CSV,
    regime_path: Path = REGIME_CSV,
) -> tuple[bytes, list[dict[str, str]]]:
    rows = build_rows(read_csv(signals_path), latest_regime(read_csv(regime_path)))
    return csv_bytes(rows), rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail when the committed CSV is stale")
    args = parser.parse_args()

    content, rows = build_snapshot()
    digest = hashlib.sha256(content).hexdigest()

    if args.check:
        if not OUTPUT_CSV.exists() or OUTPUT_CSV.read_bytes() != content:
            print("data/research_snapshot.csv is stale; run scripts/build_research_snapshot.py")
            return 1
        print(f"Research snapshot is current ({len(rows)} rows, sha256 {digest}).")
        return 0

    atomic_write(OUTPUT_CSV, content)
    meta = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_files": [
            str(SIGNALS_CSV.relative_to(REPO_ROOT)),
            str(REGIME_CSV.relative_to(REPO_ROOT)),
        ],
        "row_count": len(rows),
        "sha256": digest,
    }
    atomic_write(
        OUTPUT_META,
        (json.dumps(meta, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    print(f"Wrote {OUTPUT_CSV.relative_to(REPO_ROOT)} ({len(rows)} rows, sha256 {digest}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
