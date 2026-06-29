#!/usr/bin/env python3
"""TradingJournal unusual-volume scanner.

This script is intentionally a candidate-discovery and measurement tool.
It does not place trades and does not write to trades.csv.

Data sources in v1:
- Alpaca Market Data API for U.S. price/volume bars and snapshots.
- Finviz free-tier manual seed list via data/finviz_watchlist.csv.

The Finviz integration deliberately avoids brittle scraping. Use Finviz free screener
manually, paste tickers into data/finviz_watchlist.csv, and the scanner gives those
names a small score boost while Alpaca supplies objective price/volume data.
"""

from __future__ import annotations

import csv
import json
import math
import os
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - GitHub Actions uses Python 3.11+
    print("Python 3.11+ is required because this script uses tomllib.", file=sys.stderr)
    raise


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / os.environ.get("SCANNER_CONFIG", "scanner/config.toml")
SIGNALS_CSV = REPO_ROOT / "data/scanner_signals.csv"
REPORT_DIR = REPO_ROOT / "research/scans"

CSV_FIELDS = [
    "timestamp",
    "ticker",
    "market",
    "price",
    "change_pct",
    "rel_volume",
    "volume",
    "avg_volume_20d",
    "above_20d_high",
    "above_50d_high",
    "extension_5d_pct",
    "score",
    "source",
    "reasons",
    "warnings",
    "one_day_return",
    "three_day_return",
    "five_day_return",
    "notes",
]


@dataclass
class Candidate:
    timestamp: str
    ticker: str
    market: str = "US"
    price: float | None = None
    change_pct: float | None = None
    rel_volume: float | None = None
    volume: int | None = None
    avg_volume_20d: float | None = None
    above_20d_high: bool = False
    above_50d_high: bool = False
    extension_5d_pct: float | None = None
    score: int = 0
    source: str = "alpaca"
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_csv_row(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "ticker": self.ticker,
            "market": self.market,
            "price": fmt_float(self.price),
            "change_pct": fmt_float(self.change_pct),
            "rel_volume": fmt_float(self.rel_volume),
            "volume": self.volume or "",
            "avg_volume_20d": fmt_float(self.avg_volume_20d),
            "above_20d_high": str(self.above_20d_high).lower(),
            "above_50d_high": str(self.above_50d_high).lower(),
            "extension_5d_pct": fmt_float(self.extension_5d_pct),
            "score": self.score,
            "source": self.source,
            "reasons": "; ".join(self.reasons),
            "warnings": "; ".join(self.warnings),
            "one_day_return": "",
            "three_day_return": "",
            "five_day_return": "",
            "notes": "",
        }


def fmt_float(value: float | None, digits: int = 4) -> str:
    if value is None or not math.isfinite(value):
        return ""
    return f"{value:.{digits}f}"


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config file: {CONFIG_PATH}")
    with CONFIG_PATH.open("rb") as f:
        return tomllib.load(f)


def read_ticker_list(path: Path) -> list[str]:
    if not path.exists():
        return []
    tickers: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip().upper()
        if not line or line.startswith("#"):
            continue
        tickers.append(line)
    return sorted(set(tickers))


def read_finviz_manual(path: Path) -> dict[str, dict[str, str]]:
    """Read optional tickers copied from a Finviz free screener.

    Expected CSV columns: ticker, notes, finviz_screen, added_at. Only ticker is required.
    """
    if not path.exists():
        return {}
    out: dict[str, dict[str, str]] = {}
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = (row.get("ticker") or "").strip().upper()
            if not ticker or ticker.startswith("#"):
                continue
            out[ticker] = {k: (v or "") for k, v in row.items()}
    return out


def chunked(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def alpaca_credentials() -> tuple[str | None, str | None]:
    key = os.getenv("APCA_API_KEY_ID") or os.getenv("ALPACA_API_KEY_ID")
    secret = os.getenv("APCA_API_SECRET_KEY") or os.getenv("ALPACA_API_SECRET_KEY")
    return key, secret


def alpaca_get(path: str, params: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    key, secret = alpaca_credentials()
    if not key or not secret:
        raise RuntimeError("Missing Alpaca API credentials in repository secrets.")

    base_url = config["alpaca"].get("base_url", "https://data.alpaca.markets").rstrip("/")
    query = urllib.parse.urlencode(params, doseq=True)
    url = f"{base_url}{path}?{query}"
    req = urllib.request.Request(
        url,
        headers={
            "APCA-API-KEY-ID": key,
            "APCA-API-SECRET-KEY": secret,
            "Accept": "application/json",
            "User-Agent": "TradingJournalScanner/0.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Alpaca HTTP {e.code}: {body[:500]}") from e


def fetch_snapshots(tickers: list[str], config: dict[str, Any]) -> dict[str, Any]:
    feed = config["alpaca"].get("feed", "iex")
    batch_size = int(config["alpaca"].get("batch_size", 50))
    snapshots: dict[str, Any] = {}
    for batch in chunked(tickers, batch_size):
        data = alpaca_get(
            "/v2/stocks/snapshots",
            {"symbols": ",".join(batch), "feed": feed},
            config,
        )
        snapshots.update(data)
        time.sleep(0.25)
    return snapshots


def fetch_daily_bars(tickers: list[str], config: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    feed = config["alpaca"].get("feed", "iex")
    batch_size = int(config["alpaca"].get("batch_size", 50))
    lookback_days = int(config["alpaca"].get("lookback_days", 90))
    start = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).date().isoformat()
    bars: dict[str, list[dict[str, Any]]] = {}
    for batch in chunked(tickers, batch_size):
        data = alpaca_get(
            "/v2/stocks/bars",
            {
                "symbols": ",".join(batch),
                "timeframe": "1Day",
                "start": start,
                "adjustment": "raw",
                "feed": feed,
                "limit": 10000,
            },
            config,
        )
        for ticker, ticker_bars in data.get("bars", {}).items():
            bars[ticker.upper()] = sorted(ticker_bars, key=lambda b: b.get("t", ""))
        time.sleep(0.25)
    return bars


def safe_mean(values: list[float]) -> float | None:
    clean = [v for v in values if v is not None and math.isfinite(v)]
    if not clean:
        return None
    return float(statistics.mean(clean))


def latest_price(snapshot: dict[str, Any], daily_bar: dict[str, Any] | None) -> float | None:
    trade = snapshot.get("latestTrade") or {}
    for candidate in [trade.get("p"), (daily_bar or {}).get("c")]:
        if candidate is not None:
            return float(candidate)
    return None


def score_candidate(
    ticker: str,
    timestamp: str,
    snapshot: dict[str, Any],
    bars: list[dict[str, Any]],
    finviz_manual: dict[str, dict[str, str]],
    config: dict[str, Any],
) -> Candidate | None:
    filters = config["filters"]
    weights = config["score"]

    daily = snapshot.get("dailyBar") or (bars[-1] if bars else {})
    prev = snapshot.get("prevDailyBar") or (bars[-2] if len(bars) >= 2 else {})
    price = latest_price(snapshot, daily)
    if price is None:
        return None

    min_price = float(filters.get("min_price", 2.0))
    max_price = float(filters.get("max_price", 500.0))
    if price < min_price or price > max_price:
        return None

    hist = bars[:-1] if len(bars) > 1 else []
    last20 = hist[-20:]
    last50 = hist[-50:]
    last5 = hist[-5:]
    avg_volume_20d = safe_mean([float(b.get("v", 0)) for b in last20])
    if not avg_volume_20d:
        return None

    min_avg_volume = int(filters.get("min_avg_volume_20d", 300000))
    if avg_volume_20d < min_avg_volume:
        return None

    volume = int(float(daily.get("v", 0) or 0))
    rel_volume = volume / avg_volume_20d if avg_volume_20d else None
    prev_close = float(prev.get("c", 0) or 0)
    change_pct = ((price / prev_close) - 1) * 100 if prev_close > 0 else None

    high20 = max([float(b.get("h", 0)) for b in last20], default=0.0)
    high50 = max([float(b.get("h", 0)) for b in last50], default=0.0)
    high5 = max([float(b.get("h", 0)) for b in last5], default=0.0)

    above_20d_high = bool(high20 and price > high20)
    above_50d_high = bool(high50 and price > high50)
    extension_5d_pct = ((price / high5) - 1) * 100 if high5 else None

    candidate = Candidate(
        timestamp=timestamp,
        ticker=ticker,
        price=price,
        change_pct=change_pct,
        rel_volume=rel_volume,
        volume=volume,
        avg_volume_20d=avg_volume_20d,
        above_20d_high=above_20d_high,
        above_50d_high=above_50d_high,
        extension_5d_pct=extension_5d_pct,
    )

    min_rel_volume = float(filters.get("min_rel_volume", 2.0))
    min_change_pct = float(filters.get("min_change_pct", 3.0))
    max_change_pct = float(filters.get("max_change_pct", 15.0))
    max_extension = float(filters.get("max_extension_5d_pct", 25.0))

    if rel_volume and rel_volume >= min_rel_volume:
        rel_points = int(round(float(weights.get("rel_volume", 20)) * min(rel_volume / 3.0, 1.0)))
        candidate.score += rel_points
        candidate.reasons.append(f"relative volume {rel_volume:.2f}x")
    else:
        candidate.warnings.append(f"relative volume below trigger ({fmt_float(rel_volume) or 'n/a'}x)")

    if change_pct is not None and min_change_pct <= change_pct <= max_change_pct:
        candidate.score += int(weights.get("daily_change", 10))
        candidate.reasons.append(f"daily move {change_pct:.2f}% inside target range")
    elif change_pct is not None and change_pct > max_change_pct:
        candidate.score += max(0, int(weights.get("daily_change", 10)) // 2)
        candidate.warnings.append(f"already extended intraday/day move {change_pct:.2f}%")
    elif change_pct is not None:
        candidate.warnings.append(f"daily move only {change_pct:.2f}%")

    if above_20d_high:
        candidate.score += int(weights.get("break_20d_high", 15))
        candidate.reasons.append("breaking above 20-day high")

    if above_50d_high:
        candidate.reasons.append("also above 50-day high")

    open_price = float(daily.get("o", 0) or 0)
    if open_price and price > open_price:
        candidate.score += int(weights.get("close_above_open", 5))
        candidate.reasons.append("price above today's open")

    if extension_5d_pct is not None and extension_5d_pct <= max_extension:
        candidate.score += int(weights.get("not_overextended", 10))
        candidate.reasons.append(f"not too extended vs 5-day high ({extension_5d_pct:.2f}%)")
    elif extension_5d_pct is not None:
        candidate.warnings.append(f"extended vs 5-day high ({extension_5d_pct:.2f}%)")

    if avg_volume_20d >= min_avg_volume * 3:
        candidate.score += int(weights.get("liquidity", 10))
        candidate.reasons.append("liquidity comfortably above floor")

    if ticker in finviz_manual:
        candidate.score += int(weights.get("finviz_seed", 10))
        candidate.source = "alpaca+finviz_manual"
        note = finviz_manual[ticker].get("notes") or "seeded from Finviz manual watchlist"
        candidate.reasons.append(note)

    return candidate


def append_signal_rows(path: Path, candidates: list[Candidate]) -> None:
    if not candidates:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not exists:
            writer.writeheader()
        for candidate in candidates:
            writer.writerow(candidate.to_csv_row())


def write_report(
    timestamp: datetime,
    candidates: list[Candidate],
    recorded: list[Candidate],
    config: dict[str, Any],
    warnings: list[str],
    universe_count: int,
    finviz_count: int,
) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    local_ts = timestamp.strftime("%Y-%m-%d %H:%M %Z")
    file_ts = timestamp.strftime("%Y-%m-%d-%H%M")
    report_path = REPORT_DIR / f"scan-{file_ts}.md"
    alert_score = int(config["scanner"].get("min_score_to_alert", 70))
    record_score = int(config["scanner"].get("min_score_to_record", 60))
    max_rows = int(config["scanner"].get("max_candidates_per_report", 10))
    top = sorted(recorded, key=lambda c: c.score, reverse=True)[:max_rows]

    lines: list[str] = []
    lines.append(f"# Pump Scanner — {local_ts}")
    lines.append("")
    lines.append("DRAFT for human review. This is candidate discovery, not financial advice and not a trade signal.")
    lines.append("")
    lines.append("## Run summary")
    lines.append(f"- Universe tickers scanned: {universe_count}")
    lines.append(f"- Finviz manual seeds loaded: {finviz_count}")
    lines.append(f"- Candidates scored: {len(candidates)}")
    lines.append(f"- Recorded candidates with score >= {record_score}: {len(recorded)}")
    if warnings:
        lines.append("- Warnings:")
        for w in warnings:
            lines.append(f"  - {w}")
    lines.append("")

    lines.append("## Top alerts")
    alerts = [c for c in top if c.score >= alert_score]
    if not alerts:
        lines.append("No candidates reached the alert threshold this run.")
    else:
        for idx, c in enumerate(alerts, 1):
            lines.extend(candidate_markdown(idx, c))
    lines.append("")

    lines.append("## Watchlist candidates")
    watch = [c for c in top if c.score < alert_score]
    if not watch:
        lines.append("No additional watchlist candidates above the record threshold.")
    else:
        for idx, c in enumerate(watch, 1):
            lines.extend(candidate_markdown(idx, c))
    lines.append("")

    lines.append("## Finviz free-tier workflow")
    lines.append("Use Finviz manually as a discovery surface, then paste interesting tickers into `data/finviz_watchlist.csv`. The scanner does not scrape Finviz; it only uses your manually curated Finviz seeds and validates price/volume through Alpaca.")
    lines.append("")
    lines.append("Suggested Finviz screen to replicate manually:")
    lines.append("- Price above $2")
    lines.append("- Average volume above 500k")
    lines.append("- Relative volume above 2")
    lines.append("- Current change between roughly +3% and +15%")
    lines.append("- New high / above 20-day moving average / strong technical setup")
    lines.append("- Exclude names that are already +40% to +100% unless you explicitly want ultra-high risk")
    lines.append("")
    lines.append("## Next human step")
    lines.append("For any ticker you care about, run the Claude/GPT deep-dive prompt before trading: check current news, upcoming catalyst, dilution/offering risk, short interest, options activity, and a clear invalidation level.")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def candidate_markdown(idx: int, c: Candidate) -> list[str]:
    lines = [f"### {idx}. {c.ticker} — score {c.score}"]
    lines.append(f"- Price: {fmt_float(c.price, 2)} | Move: {fmt_float(c.change_pct, 2)}% | Rel volume: {fmt_float(c.rel_volume, 2)}x")
    lines.append(f"- Volume: {c.volume or ''} | Avg 20d volume: {fmt_float(c.avg_volume_20d, 0)}")
    lines.append(f"- Breakout: 20d={str(c.above_20d_high).lower()}, 50d={str(c.above_50d_high).lower()} | 5d extension: {fmt_float(c.extension_5d_pct, 2)}%")
    lines.append(f"- Source: {c.source}")
    lines.append(f"- Reasons: {'; '.join(c.reasons) if c.reasons else 'n/a'}")
    if c.warnings:
        lines.append(f"- Warnings: {'; '.join(c.warnings)}")
    lines.append("- Human check: news/catalyst, dilution risk, spread/liquidity, and invalidation level required before any trade.")
    lines.append("")
    return lines


def main() -> int:
    config = load_config()
    tz = ZoneInfo(config["scanner"].get("timezone", "Europe/Berlin"))
    now = datetime.now(tz)
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    warnings: list[str] = []

    universe_file = REPO_ROOT / config["universe"].get("file", "scanner/universe.txt")
    finviz_file = REPO_ROOT / config["universe"].get("finviz_manual_file", "data/finviz_watchlist.csv")
    base_universe = read_ticker_list(universe_file)
    finviz_manual = read_finviz_manual(finviz_file)
    tickers = sorted(set(base_universe) | set(finviz_manual.keys()))

    if not tickers:
        warnings.append("No tickers found in scanner/universe.txt or data/finviz_watchlist.csv.")
        report = write_report(now, [], [], config, warnings, 0, len(finviz_manual))
        print(f"Wrote report: {report}")
        return 0

    key, secret = alpaca_credentials()
    if not key or not secret:
        warnings.append("Alpaca credentials are not configured. Add repository secrets APCA_API_KEY_ID and APCA_API_SECRET_KEY, then run again.")
        report = write_report(now, [], [], config, warnings, len(tickers), len(finviz_manual))
        print(f"Wrote report without market data: {report}")
        return 0

    try:
        snapshots = fetch_snapshots(tickers, config)
        bars = fetch_daily_bars(tickers, config)
    except Exception as exc:  # noqa: BLE001 - report and keep workflow non-destructive
        warnings.append(f"Data fetch failed: {exc}")
        report = write_report(now, [], [], config, warnings, len(tickers), len(finviz_manual))
        print(f"Wrote report after data error: {report}")
        return 0

    candidates: list[Candidate] = []
    for ticker in tickers:
        candidate = score_candidate(
            ticker=ticker,
            timestamp=timestamp,
            snapshot=snapshots.get(ticker, {}),
            bars=bars.get(ticker, []),
            finviz_manual=finviz_manual,
            config=config,
        )
        if candidate is not None:
            candidates.append(candidate)

    record_score = int(config["scanner"].get("min_score_to_record", 60))
    recorded = sorted([c for c in candidates if c.score >= record_score], key=lambda c: c.score, reverse=True)
    append_signal_rows(SIGNALS_CSV, recorded)
    report = write_report(now, candidates, recorded, config, warnings, len(tickers), len(finviz_manual))
    print(f"Wrote report: {report}")
    print(f"Recorded candidates: {len(recorded)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
