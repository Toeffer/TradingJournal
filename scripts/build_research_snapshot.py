#!/usr/bin/env python3
"""Build a normalized market-data snapshot for model-neutral research runs.

The snapshot is intentionally provider-agnostic. It converts the latest recent
scanner observation per ticker into one stable CSV so different models receive
identical market context. Fundamental fields that the current providers do not
supply remain blank rather than being invented.

Manual Finviz rows are optional discovery context only. They never increase the
quantitative score in this snapshot, and expired rows are not presented as active
seeds. Historical rows written before the score boost was removed are normalized.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import tomllib
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
REGIME_CSV = REPO_ROOT / "data/market_regime.csv"
FINVIZ_CSV = REPO_ROOT / "data/finviz_watchlist.csv"
CONFIG_TOML = REPO_ROOT / "scanner/config.toml"
OUTPUT_CSV = REPO_ROOT / "data/research_snapshot.csv"
OUTPUT_META = REPO_ROOT / "data/research_snapshot.meta.json"

# All scanner rows carrying finviz_manual before this instant were produced while
# the manual seed added 10 points. From this change onward the configured weight is
# zero, so newer rows must not be adjusted.
LEGACY_FINVIZ_BONUS = 10
LEGACY_FINVIZ_BONUS_REMOVED_AT = datetime(2026, 7, 12, tzinfo=timezone.utc)

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
    "discovery_seed",
    "discovery_seed_source",
    "legacy_seed_tag",
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


def load_scanner_config(path: Path = CONFIG_TOML) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def parse_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_timestamp(value: str | None) -> datetime | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


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


def recent_signals(
    rows: list[dict[str, str]],
    *,
    as_of: datetime,
    lookback_days: int,
) -> list[dict[str, str]]:
    cutoff = as_of.astimezone(timezone.utc) - timedelta(days=lookback_days)
    recent: list[dict[str, str]] = []
    for row in rows:
        observed_at = parse_timestamp(row.get("timestamp"))
        if observed_at is not None and cutoff <= observed_at <= as_of.astimezone(timezone.utc):
            recent.append(row)
    return recent


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


def seed_expiry(row: dict[str, str], max_age_days: int) -> date | None:
    explicit = (row.get("expires_at") or "").strip()
    if explicit:
        try:
            return date.fromisoformat(explicit)
        except ValueError:
            return None
    added = (row.get("added_at") or "").strip()
    if not added:
        return None
    try:
        return date.fromisoformat(added) + timedelta(days=max_age_days)
    except ValueError:
        return None


def active_discovery_seeds(
    rows: list[dict[str, str]],
    *,
    as_of: date,
    max_age_days: int,
) -> dict[str, dict[str, str]]:
    active: dict[str, dict[str, str]] = {}
    for row in rows:
        ticker = (row.get("ticker") or "").strip().upper()
        if not ticker:
            continue
        expiry = seed_expiry(row, max_age_days)
        if expiry is not None and expiry < as_of:
            continue
        active[ticker] = row
    return active


def quantitative_source(source: str, market: str) -> str:
    cleaned = source.replace("+finviz_manual", "").replace("finviz_manual+", "")
    if cleaned == "finviz_manual":
        cleaned = ""
    return cleaned or market


def normalized_score(row: dict[str, str]) -> int | None:
    value = parse_float(row.get("score"))
    if value is None:
        return None
    score = int(round(value))
    source = row.get("source", "")
    observed_at = parse_timestamp(row.get("timestamp"))
    if (
        "finviz_manual" in source
        and observed_at is not None
        and observed_at < LEGACY_FINVIZ_BONUS_REMOVED_AT
    ):
        score = max(0, score - LEGACY_FINVIZ_BONUS)
    return score


def build_rows(
    signal_rows: list[dict[str, str]],
    regime: str,
    *,
    active_seeds: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    seeds = active_seeds or {}
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
        original_source = row.get("source", "")
        provider = quantitative_source(original_source, market)
        legacy_seed_tag = "finviz_manual" in original_source
        is_active_seed = ticker in seeds
        notes = row.get("notes", "") or row.get("warnings", "")
        if legacy_seed_tag and not is_active_seed:
            legacy_note = "legacy manual-seed tag removed from quantitative score"
            notes = f"{notes}; {legacy_note}" if notes else legacy_note
        raw_score = normalized_score(row)
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
                "score": "" if raw_score is None else str(raw_score),
                "discovery_seed": str(is_active_seed).lower(),
                "discovery_seed_source": "finviz_manual" if is_active_seed else "",
                "legacy_seed_tag": str(legacy_seed_tag).lower(),
                "break_20d_high": row.get("above_20d_high", ""),
                "extension_5d_pct": row.get("extension_5d_pct", ""),
                "rsi14": row.get("rsi14", ""),
                "ema20_dist_pct": row.get("ema20_dist_pct", ""),
                "ema50_dist_pct": row.get("ema50_dist_pct", ""),
                "macd_hist_pct": row.get("macd_hist_pct", ""),
                "bb_percent_b": row.get("bb_percent_b", ""),
                "market_regime": regime,
                "signal_source": provider,
                "signal_timestamp": row.get("timestamp", ""),
                "data_source": provider,
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
    finviz_path: Path = FINVIZ_CSV,
    config_path: Path = CONFIG_TOML,
    *,
    as_of: datetime | None = None,
) -> tuple[bytes, list[dict[str, str]]]:
    config = load_scanner_config(config_path)
    scanner_config = config.get("scanner", {})
    lookback_days = int(scanner_config.get("research_snapshot_lookback_days", 7))
    max_seed_age = int(scanner_config.get("finviz_seed_max_age_days", 2))
    effective_as_of = (as_of or datetime.now(timezone.utc)).astimezone(timezone.utc)
    signal_rows = recent_signals(
        read_csv(signals_path),
        as_of=effective_as_of,
        lookback_days=lookback_days,
    )
    seeds = active_discovery_seeds(
        read_csv(finviz_path),
        as_of=effective_as_of.date(),
        max_age_days=max_seed_age,
    )
    rows = build_rows(signal_rows, latest_regime(read_csv(regime_path)), active_seeds=seeds)
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
    config = load_scanner_config()
    meta = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_files": [
            str(SIGNALS_CSV.relative_to(REPO_ROOT)),
            str(REGIME_CSV.relative_to(REPO_ROOT)),
            str(FINVIZ_CSV.relative_to(REPO_ROOT)),
        ],
        "research_snapshot_lookback_days": int(
            config.get("scanner", {}).get("research_snapshot_lookback_days", 7)
        ),
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
