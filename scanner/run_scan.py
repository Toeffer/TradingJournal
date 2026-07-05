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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from indicators import compute_indicator_columns  # noqa: E402

NY_TZ = ZoneInfo("America/New_York")

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
    # Measurement-only technical indicators (see scanner/indicators.py).
    # Never part of the score until the bucket evaluation proves they
    # separate forward returns (MASTERPLAN Phase 1).
    "rsi14",
    "ema20_dist_pct",
    "ema50_dist_pct",
    "macd_hist_pct",
    "bb_percent_b",
    "score",
    "source",
    "reasons",
    "warnings",
    "one_day_return",
    "three_day_return",
    "five_day_return",
    "ten_day_return",
    "twenty_one_day_return",
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
    rsi14: float | None = None
    ema20_dist_pct: float | None = None
    ema50_dist_pct: float | None = None
    macd_hist_pct: float | None = None
    bb_percent_b: float | None = None
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
            "rsi14": fmt_float(self.rsi14, 2),
            "ema20_dist_pct": fmt_float(self.ema20_dist_pct, 2),
            "ema50_dist_pct": fmt_float(self.ema50_dist_pct, 2),
            "macd_hist_pct": fmt_float(self.macd_hist_pct),
            "bb_percent_b": fmt_float(self.bb_percent_b, 3),
            "score": self.score,
            "source": self.source,
            "reasons": "; ".join(self.reasons),
            "warnings": "; ".join(self.warnings),
            "one_day_return": "",
            "three_day_return": "",
            "five_day_return": "",
            "ten_day_return": "",
            "twenty_one_day_return": "",
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


def session_elapsed_fraction(now: datetime) -> float | None:
    """Fraction of the US regular session (9:30-16:00 America/New_York) elapsed at `now`.

    avg_volume_20d is a full-day average, but a mid-session snapshot only has a
    partial day's volume. Comparing the two directly (as before) makes relative
    volume nearly unreachable except right at the close. This gives a cheap
    pro-rata baseline instead of requiring intraday bars.
    """
    now_ny = now.astimezone(NY_TZ)
    if now_ny.weekday() >= 5:
        return None
    open_dt = now_ny.replace(hour=9, minute=30, second=0, microsecond=0)
    close_dt = now_ny.replace(hour=16, minute=0, second=0, microsecond=0)
    if now_ny < open_dt:
        return None
    if now_ny >= close_dt:
        return 1.0
    elapsed = (now_ny - open_dt).total_seconds()
    total = (close_dt - open_dt).total_seconds()
    # Floor at 5% of the session so the first few minutes after the open don't
    # divide by a near-zero expected volume and produce absurd ratios.
    return max(elapsed / total, 0.05)


def latest_price(snapshot: dict[str, Any], daily_bar: dict[str, Any] | None) -> float | None:
    trade = snapshot.get("latestTrade") or {}
    for candidate in [trade.get("p"), (daily_bar or {}).get("c")]:
        if candidate is not None:
            return float(candidate)
    return None


def score_candidate(
    ticker: str,
    timestamp: str,
    now: datetime,
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
    session_fraction = session_elapsed_fraction(now)
    expected_volume_to_date = (
        avg_volume_20d * session_fraction if session_fraction is not None else None
    )
    rel_volume = (
        volume / expected_volume_to_date
        if expected_volume_to_date
        else None
    )
    prev_close = float(prev.get("c", 0) or 0)
    change_pct = ((price / prev_close) - 1) * 100 if prev_close > 0 else None

    high20 = max([float(b.get("h", 0)) for b in last20], default=0.0)
    high50 = max([float(b.get("h", 0)) for b in last50], default=0.0)
    high5 = max([float(b.get("h", 0)) for b in last5], default=0.0)

    above_20d_high = bool(high20 and price > high20)
    above_50d_high = bool(high50 and price > high50)
    extension_5d_pct = ((price / high5) - 1) * 100 if high5 else None

    # Measurement-only indicator columns: history closes plus the live price
    # as today's close (same intraday convention as the score components).
    # These are recorded for later bucket analysis and never enter the score.
    closes = [float(b["c"]) for b in hist if b.get("c") is not None]
    ind = compute_indicator_columns(closes + [price])

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
        **ind,
    )

    min_rel_volume = float(filters.get("min_rel_volume", 2.0))
    min_change_pct = float(filters.get("min_change_pct", 3.0))
    max_change_pct = float(filters.get("max_change_pct", 15.0))
    max_extension = float(filters.get("max_extension_5d_pct", 25.0))

    if session_fraction is None:
        candidate.warnings.append("relative volume not computed (outside US regular session)")
    elif rel_volume and rel_volume >= min_rel_volume:
        rel_points = int(round(float(weights.get("rel_volume", 20)) * min(rel_volume / 3.0, 1.0)))
        candidate.score += rel_points
        candidate.reasons.append(f"relative volume {rel_volume:.2f}x pace (session {session_fraction * 100:.0f}% elapsed)")
    else:
        candidate.warnings.append(f"relative volume below trigger ({fmt_float(rel_volume) or 'n/a'}x pace)")

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


RETURN_FIELDS = (
    "one_day_return",
    "three_day_return",
    "five_day_return",
    "ten_day_return",
    "twenty_one_day_return",
    "notes",
)


def _merge_return_fields(preferred: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
    """Keep `preferred`'s values but backfill any blank return/notes fields from `other`."""
    merged = dict(preferred)
    for key in RETURN_FIELDS:
        if not merged.get(key) and other.get(key):
            merged[key] = other[key]
    return merged


def append_signal_rows(path: Path, candidates: list[Candidate]) -> None:
    """Write new candidates, deduped to one row per (date, ticker) keeping the highest score.

    A stock that stays elevated all session gets re-recorded on every scan run, which
    would bias later score-bucket stats toward persistent names. Same-day duplicates are
    collapsed here; rows from other days are left untouched. Backfilled return columns
    are preserved across the merge regardless of which run's row is kept.
    """
    if not candidates:
        return
    path.parent.mkdir(parents=True, exist_ok=True)

    existing: list[dict[str, Any]] = []
    if path.exists() and path.stat().st_size > 0:
        with path.open("r", newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    best: dict[tuple[str, str], dict[str, Any]] = {}
    for row in existing:
        key = (row["timestamp"][:10], row["ticker"])
        if key not in best or int(row.get("score") or 0) > int(best[key].get("score") or 0):
            best[key] = row

    for candidate in candidates:
        key = (candidate.timestamp[:10], candidate.ticker)
        new_row = candidate.to_csv_row()
        if key not in best:
            best[key] = new_row
        elif candidate.score > int(best[key].get("score") or 0):
            best[key] = _merge_return_fields(new_row, best[key])
        else:
            best[key] = _merge_return_fields(best[key], new_row)

    rows = sorted(best.values(), key=lambda r: (r["timestamp"], r["ticker"]))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


REGIME_CSV = REPO_ROOT / "data/market_regime.csv"
REGIME_FIELDS = [
    "timestamp",
    "spy_close",
    "spy_50d_ma",
    "spy_above_50d",
    "breadth_pct_above_20d_ma",
    # Cross-asset measurement columns (idea from oft3r/agentic-trading-desk's
    # macro pillar): 20-trading-day % change of three risk-appetite ratios.
    # Rising HYG/LQD = credit risk-on; rising IWM/SPY = small-cap risk-on;
    # rising XLY/XLP = consumer risk-on. Logged only — the `regime` label
    # formula is unchanged so the Phase 1/2 regime data stays comparable.
    "credit_hyg_lqd_20d_pct",
    "size_iwm_spy_20d_pct",
    "risk_xly_xlp_20d_pct",
    "cross_asset_score",
    "regime",
]

# ETFs fetched for regime context only; never scored or recorded as signals.
REGIME_ETFS = ["SPY", "HYG", "LQD", "IWM", "XLY", "XLP"]


def ratio_20d_change(
    num_bars: list[dict[str, Any]], den_bars: list[dict[str, Any]]
) -> float | None:
    """% change of the close ratio numerator/denominator over 20 trading days.

    Bars are aligned by date first — the two ETFs can have slightly different
    bar sets on the IEX feed, and a misaligned ratio series would be noise.
    """
    num = {str(b.get("t", ""))[:10]: float(b["c"]) for b in num_bars if b.get("c")}
    den = {str(b.get("t", ""))[:10]: float(b["c"]) for b in den_bars if b.get("c")}
    dates = sorted(set(num) & set(den))
    if len(dates) < 21:
        return None
    ratio_now = num[dates[-1]] / den[dates[-1]]
    ratio_then = num[dates[-21]] / den[dates[-21]]
    if ratio_then == 0:
        return None
    return (ratio_now / ratio_then - 1) * 100


def compute_regime(
    timestamp: str,
    etf_bars: dict[str, list[dict[str, Any]]],
    universe_bars: dict[str, list[dict[str, Any]]],
) -> dict[str, Any] | None:
    """Classify the market backdrop so every proposal/signal carries its context.

    Deliberately crude: SPY vs its 50-day MA plus universe breadth (% of scanned
    tickers above their own 20-day MA). The point is not precision — it's that
    'did breakout proposals work in defensive tape?' becomes answerable later.

    The cross-asset ratio columns are measurement-only context; they do not
    move the `regime` label. Folding them into the label is a phase-transition
    decision once there is enough history to see whether they add anything.
    """
    spy_bars = etf_bars.get("SPY", [])
    spy_closes = [float(b.get("c", 0)) for b in spy_bars if b.get("c") is not None]
    if len(spy_closes) < 50:
        return None
    spy_close = spy_closes[-1]
    spy_50 = float(statistics.mean(spy_closes[-50:]))

    above = 0
    counted = 0
    for ticker_bars in universe_bars.values():
        closes = [float(b.get("c", 0)) for b in ticker_bars if b.get("c") is not None]
        if len(closes) < 20:
            continue
        counted += 1
        if closes[-1] > statistics.mean(closes[-20:]):
            above += 1
    breadth = (100.0 * above / counted) if counted else None

    credit = ratio_20d_change(etf_bars.get("HYG", []), etf_bars.get("LQD", []))
    size = ratio_20d_change(etf_bars.get("IWM", []), etf_bars.get("SPY", []))
    risk = ratio_20d_change(etf_bars.get("XLY", []), etf_bars.get("XLP", []))
    # -3..+3: each ratio votes +1 above +1%, -1 below -1%, 0 in between.
    votes = [v for v in (credit, size, risk) if v is not None]
    cross_score = sum(1 if v >= 1.0 else -1 if v <= -1.0 else 0 for v in votes)

    spy_above = spy_close > spy_50
    if spy_above and breadth is not None and breadth >= 50:
        label = "supportive"
    elif not spy_above and breadth is not None and breadth < 35:
        label = "defensive"
    else:
        label = "mixed"

    return {
        "timestamp": timestamp,
        "spy_close": fmt_float(spy_close, 2),
        "spy_50d_ma": fmt_float(spy_50, 2),
        "spy_above_50d": str(spy_above).lower(),
        "breadth_pct_above_20d_ma": fmt_float(breadth, 1) if breadth is not None else "",
        "credit_hyg_lqd_20d_pct": fmt_float(credit, 2),
        "size_iwm_spy_20d_pct": fmt_float(size, 2),
        "risk_xly_xlp_20d_pct": fmt_float(risk, 2),
        "cross_asset_score": str(cross_score) if votes else "",
        "regime": label,
    }


def append_regime_row(path: Path, row: dict[str, Any]) -> None:
    """Append a regime row, migrating the file in place if columns were added.

    Older files carry fewer columns; blindly appending a wider row would
    desync data from the header. On mismatch the file is rewritten with the
    current header and old rows padded with blanks.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    header: list[str] | None = None
    if path.exists() and path.stat().st_size > 0:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = list(reader.fieldnames or [])
            existing = list(reader)

    if header == REGIME_FIELDS:
        with path.open("a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=REGIME_FIELDS).writerow(row)
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REGIME_FIELDS)
        writer.writeheader()
        for old in existing:
            writer.writerow({k: old.get(k, "") for k in REGIME_FIELDS})
        writer.writerow(row)


def write_report(
    timestamp: datetime,
    candidates: list[Candidate],
    recorded: list[Candidate],
    config: dict[str, Any],
    warnings: list[str],
    universe_count: int,
    finviz_count: int,
    regime: dict[str, Any] | None = None,
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
    lines.append("Volume figures use the IEX feed only (a minority of consolidated U.S. volume), not full-tape liquidity. Relative volume is normalized against the elapsed fraction of the US regular session (9:30-16:00 ET), not the full-day average.")
    lines.append("")
    lines.append("## Run summary")
    if regime:
        lines.append(
            f"- Market regime: **{regime['regime']}** (SPY {regime['spy_close']} vs 50d MA "
            f"{regime['spy_50d_ma']}; breadth {regime['breadth_pct_above_20d_ma'] or 'n/a'}% "
            "of universe above 20d MA)"
        )
        if regime.get("cross_asset_score") != "":
            lines.append(
                f"- Cross-asset context (measurement-only, 20d ratio moves): score "
                f"{regime['cross_asset_score']}/±3 — credit HYG/LQD "
                f"{regime['credit_hyg_lqd_20d_pct'] or 'n/a'}%, size IWM/SPY "
                f"{regime['size_iwm_spy_20d_pct'] or 'n/a'}%, risk XLY/XLP "
                f"{regime['risk_xly_xlp_20d_pct'] or 'n/a'}%"
            )
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
    if any(v is not None for v in (c.rsi14, c.ema20_dist_pct, c.macd_hist_pct, c.bb_percent_b)):
        lines.append(
            f"- Indicators (context only, not scored): RSI14 {fmt_float(c.rsi14, 1) or 'n/a'} | "
            f"vs EMA20 {fmt_float(c.ema20_dist_pct, 1) or 'n/a'}% | vs EMA50 {fmt_float(c.ema50_dist_pct, 1) or 'n/a'}% | "
            f"MACD hist {fmt_float(c.macd_hist_pct, 2) or 'n/a'}% | BB %B {fmt_float(c.bb_percent_b, 2) or 'n/a'}"
        )
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
        # Regime ETFs are fetched for context only; never scored or recorded.
        bars = fetch_daily_bars(tickers + REGIME_ETFS, config)
    except Exception as exc:  # noqa: BLE001 - report and keep workflow non-destructive
        warnings.append(f"Data fetch failed: {exc}")
        report = write_report(now, [], [], config, warnings, len(tickers), len(finviz_manual))
        print(f"Wrote report after data error: {report}")
        return 0

    etf_bars = {etf: bars.pop(etf, []) for etf in REGIME_ETFS}
    regime = compute_regime(timestamp, etf_bars, bars)
    if regime:
        append_regime_row(REGIME_CSV, regime)
    else:
        warnings.append("Market regime not computed (insufficient SPY history).")

    candidates: list[Candidate] = []
    for ticker in tickers:
        candidate = score_candidate(
            ticker=ticker,
            timestamp=timestamp,
            now=now,
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
    report = write_report(now, candidates, recorded, config, warnings, len(tickers), len(finviz_manual), regime)
    print(f"Wrote report: {report}")
    print(f"Recorded candidates: {len(recorded)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
