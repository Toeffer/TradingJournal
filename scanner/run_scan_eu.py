#!/usr/bin/env python3
"""EU (XETRA/LSE) unusual-volume scanner on FMP real-time quotes.

Same philosophy as run_scan.py: candidate discovery and measurement, never a
trade signal, never writes to trades.csv. Differences forced by data reality:

- Data source is Financial Modeling Prep batch quotes (secret: FMP_API_KEY).
  The current FMP plan has EU quotes but NO EU historical bars, so this script
  self-accumulates history into data/eu_quote_history.csv (see eu_history.py).
  The final run of each day (after the local close) finalizes that day's bar.
- Derived metrics degrade gracefully while history builds: day-move and
  price-vs-open work from day one; the quote's own avgVolume is used for
  relative volume when FMP provides it, otherwise the accumulated 20d average;
  breakout components activate once min_history_days_for_breakout is reached.
- Session model per exchange: XETRA 09:00-17:30 Europe/Berlin, LSE 08:00-16:30
  Europe/London.

Signals append into the same data/scanner_signals.csv with market="EU-XETRA"
or "EU-LSE", so all downstream stats can separate by market.
"""

from __future__ import annotations

import csv
import json
import os
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_history import HISTORY_CSV, bars_for, upsert_today  # noqa: E402
from run_scan import (  # noqa: E402
    REPO_ROOT,
    REPORT_DIR,
    SIGNALS_CSV,
    Candidate,
    append_signal_rows,
    candidate_markdown,
    fmt_float,
    load_config,
    read_ticker_list,
)

BERLIN = ZoneInfo("Europe/Berlin")
LONDON = ZoneInfo("Europe/London")

SESSIONS = {
    "EU-XETRA": (BERLIN, 9, 0, 17, 30),
    "EU-LSE": (LONDON, 8, 0, 16, 30),
}


def market_for(ticker: str) -> str:
    return "EU-LSE" if ticker.upper().endswith(".L") else "EU-XETRA"


def session_elapsed_fraction_eu(now: datetime, market: str) -> float | None:
    tz, oh, om, ch, cm = SESSIONS[market]
    local = now.astimezone(tz)
    if local.weekday() >= 5:
        return None
    open_dt = local.replace(hour=oh, minute=om, second=0, microsecond=0)
    close_dt = local.replace(hour=ch, minute=cm, second=0, microsecond=0)
    if local < open_dt:
        return None
    if local >= close_dt:
        return 1.0
    elapsed = (local - open_dt).total_seconds()
    total = (close_dt - open_dt).total_seconds()
    return max(elapsed / total, 0.05)


def fmp_batch_quotes(tickers: list[str], config: dict[str, Any]) -> list[dict[str, Any]]:
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        raise RuntimeError("Missing FMP_API_KEY secret.")
    base = config["eu"].get("base_url", "https://financialmodelingprep.com").rstrip("/")
    symbols = ",".join(tickers)

    # The stable API is current; /api/v3 is the legacy fallback (its quote
    # payload includes avgVolume, which stable batch-quote may omit).
    attempts = [
        f"{base}/stable/batch-quote?{urllib.parse.urlencode({'symbols': symbols, 'apikey': api_key})}",
        f"{base}/api/v3/quote/{urllib.parse.quote(symbols)}?{urllib.parse.urlencode({'apikey': api_key})}",
    ]
    last_error: Exception | None = None
    for url in attempts:
        req = urllib.request.Request(url, headers={"User-Agent": "TradingJournalScanner/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and data:
                return data
            last_error = RuntimeError(f"Empty/unexpected FMP response from {url.split('?')[0]}")
        except urllib.error.HTTPError as e:
            last_error = RuntimeError(f"FMP HTTP {e.code} from {url.split('?')[0]}")
    raise last_error or RuntimeError("FMP quote fetch failed.")


def qfloat(quote: dict[str, Any], *keys: str) -> float | None:
    for key in keys:
        value = quote.get(key)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return None


def score_eu_candidate(
    ticker: str,
    timestamp: str,
    now: datetime,
    quote: dict[str, Any],
    hist_bars: list[dict[str, Any]],
    config: dict[str, Any],
) -> Candidate | None:
    filters = config["eu"]["filters"]
    weights = config["score"]
    min_breakout_history = int(config["eu"].get("min_history_days_for_breakout", 15))
    market = market_for(ticker)

    price = qfloat(quote, "price")
    if price is None:
        return None
    if price < float(filters.get("min_price", 2.0)) or price > float(filters.get("max_price", 2000.0)):
        return None

    prev_close = qfloat(quote, "previousClose")
    change_pct = qfloat(quote, "changePercentage", "changesPercentage")
    if change_pct is None and prev_close:
        change_pct = ((price / prev_close) - 1) * 100
    volume = qfloat(quote, "volume") or 0.0
    open_price = qfloat(quote, "open")
    day_high = qfloat(quote, "dayHigh")
    day_low = qfloat(quote, "dayLow")

    # History excludes today (today's row is being written by this same run).
    today = timestamp[:10]
    hist = [b for b in hist_bars if b["t"] < today]
    reported_avg = qfloat(quote, "avgVolume")
    accumulated_avg = statistics.mean([b["v"] for b in hist[-20:]]) if hist else None
    avg_volume_20d = reported_avg or accumulated_avg

    min_avg_volume = float(filters.get("min_avg_volume_20d", 100000))
    if avg_volume_20d is not None and avg_volume_20d < min_avg_volume:
        return None

    high20 = max([b["h"] for b in hist[-20:] if b["h"]], default=0.0)
    high50 = max([b["h"] for b in hist[-50:] if b["h"]], default=0.0)
    high5 = max([b["h"] for b in hist[-5:] if b["h"]], default=0.0)
    breakout_ready = len(hist) >= min_breakout_history

    session_fraction = session_elapsed_fraction_eu(now, market)
    rel_volume = None
    if avg_volume_20d and session_fraction:
        rel_volume = volume / (avg_volume_20d * session_fraction)

    candidate = Candidate(
        timestamp=timestamp,
        ticker=ticker,
        market=market,
        price=price,
        change_pct=change_pct,
        rel_volume=rel_volume,
        volume=int(volume),
        avg_volume_20d=avg_volume_20d,
        above_20d_high=bool(breakout_ready and high20 and price > high20),
        above_50d_high=bool(len(hist) >= 50 and high50 and price > high50),
        extension_5d_pct=((price / high5) - 1) * 100 if high5 else None,
        source="fmp",
    )

    min_rel_volume = float(filters.get("min_rel_volume", 2.0))
    min_change = float(filters.get("min_change_pct", 3.0))
    max_change = float(filters.get("max_change_pct", 15.0))
    max_extension = float(filters.get("max_extension_5d_pct", 25.0))

    if session_fraction is None:
        candidate.warnings.append("relative volume not computed (outside local regular session)")
    elif rel_volume is None:
        candidate.warnings.append(
            f"relative volume unavailable (no avg volume yet; history {len(hist)} day(s))"
        )
    elif rel_volume >= min_rel_volume:
        rel_points = int(round(float(weights.get("rel_volume", 20)) * min(rel_volume / 3.0, 1.0)))
        candidate.score += rel_points
        source_note = "reported avg" if reported_avg else f"accumulated avg ({len(hist)}d)"
        candidate.reasons.append(
            f"relative volume {rel_volume:.2f}x pace ({source_note}; session {session_fraction * 100:.0f}% elapsed)"
        )
    else:
        candidate.warnings.append(f"relative volume below trigger ({fmt_float(rel_volume) or 'n/a'}x pace)")

    if change_pct is not None and min_change <= change_pct <= max_change:
        candidate.score += int(weights.get("daily_change", 10))
        candidate.reasons.append(f"daily move {change_pct:.2f}% inside target range")
    elif change_pct is not None and change_pct > max_change:
        candidate.score += max(0, int(weights.get("daily_change", 10)) // 2)
        candidate.warnings.append(f"already extended day move {change_pct:.2f}%")
    elif change_pct is not None:
        candidate.warnings.append(f"daily move only {change_pct:.2f}%")

    if candidate.above_20d_high:
        candidate.score += int(weights.get("break_20d_high", 15))
        candidate.reasons.append(f"breaking above 20-day high (from {len(hist)}d accumulated history)")
    elif not breakout_ready:
        candidate.warnings.append(
            f"breakout components inactive (history {len(hist)}/{min_breakout_history} days)"
        )

    if candidate.above_50d_high:
        candidate.reasons.append("also above 50-day high")

    if open_price and price > open_price:
        candidate.score += int(weights.get("close_above_open", 5))
        candidate.reasons.append("price above today's open")

    if candidate.extension_5d_pct is not None and candidate.extension_5d_pct <= max_extension:
        candidate.score += int(weights.get("not_overextended", 10))
        candidate.reasons.append(f"not too extended vs 5-day high ({candidate.extension_5d_pct:.2f}%)")
    elif candidate.extension_5d_pct is not None:
        candidate.warnings.append(f"extended vs 5-day high ({candidate.extension_5d_pct:.2f}%)")

    if avg_volume_20d and avg_volume_20d >= min_avg_volume * 3:
        candidate.score += int(weights.get("liquidity", 10))
        candidate.reasons.append("liquidity comfortably above floor")

    # unused for EU: day_low/day_high kept for the history row, not scoring
    _ = (day_low, day_high)
    return candidate


def write_eu_report(
    timestamp: datetime,
    recorded: list[Candidate],
    config: dict[str, Any],
    warnings: list[str],
    universe_count: int,
    scored_count: int,
    history_days: int,
) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    local_ts = timestamp.strftime("%Y-%m-%d %H:%M %Z")
    file_ts = timestamp.strftime("%Y-%m-%d-%H%M")
    report_path = REPORT_DIR / f"scan-eu-{file_ts}.md"
    alert_score = int(config["scanner"].get("min_score_to_alert", 70))
    record_score = int(config["scanner"].get("min_score_to_record", 60))
    max_rows = int(config["scanner"].get("max_candidates_per_report", 10))
    top = sorted(recorded, key=lambda c: c.score, reverse=True)[:max_rows]

    lines: list[str] = []
    lines.append(f"# EU Scanner (XETRA/LSE) — {local_ts}")
    lines.append("")
    lines.append("DRAFT for human review. Candidate discovery only — not financial advice, not a trade signal.")
    lines.append("")
    lines.append(
        "Data: FMP real-time quotes with self-accumulated daily history "
        f"(data/eu_quote_history.csv, {history_days} distinct day(s) so far). Breakout and "
        "accumulated rel-volume components reach full quality after ~20 sessions. "
        "Relative volume is normalized against the elapsed fraction of the local session "
        "(XETRA 09:00-17:30 Berlin; LSE 08:00-16:30 London)."
    )
    lines.append("")
    lines.append("## Run summary")
    lines.append(f"- Universe tickers scanned: {universe_count}")
    lines.append(f"- Candidates scored: {scored_count}")
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

    lines.append("## Next human step")
    lines.append(
        "Verify eToro tradeability (ETORO_TRADEABILITY.md) and run the scanner review "
        "prompt before considering any proposal. XETRA names trade in EUR (no FX for a "
        "EUR account); LSE adds 0.5% UK stamp duty per buy plus GBP exposure."
    )
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> int:
    config = load_config()
    now = datetime.now(BERLIN)
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    today = now.strftime("%Y-%m-%d")
    warnings: list[str] = []

    universe_file = REPO_ROOT / config["eu"].get("universe_file", "scanner/universe_eu.txt")
    tickers = read_ticker_list(universe_file)
    if not tickers:
        print("No tickers in EU universe; nothing to scan.")
        return 0

    try:
        quotes = fmp_batch_quotes(tickers, config)
    except Exception as exc:  # noqa: BLE001 - non-destructive: report and exit clean
        report = write_eu_report(now, [], config, [f"Data fetch failed: {exc}"], len(tickers), 0, 0)
        print(f"Wrote report after data error: {report}")
        return 0

    quotes_by_ticker = { (q.get("symbol") or "").upper(): q for q in quotes }

    # Update the accumulated history first (this run's snapshot becomes/updates
    # today's bar; the last run of the day finalizes it).
    history_rows: dict[str, dict[str, Any]] = {}
    for ticker in tickers:
        q = quotes_by_ticker.get(ticker.upper())
        if not q:
            continue
        history_rows[ticker.upper()] = {
            "exchange": q.get("exchange", ""),
            "open": fmt_float(qfloat(q, "open")),
            "high": fmt_float(qfloat(q, "dayHigh")),
            "low": fmt_float(qfloat(q, "dayLow")),
            "close": fmt_float(qfloat(q, "price")),
            "volume": int(qfloat(q, "volume") or 0),
            "avg_volume_reported": fmt_float(qfloat(q, "avgVolume"), 0),
        }
    if history_rows:
        upsert_today(today, history_rows)

    candidates: list[Candidate] = []
    scored = 0
    for ticker in tickers:
        q = quotes_by_ticker.get(ticker.upper())
        if not q:
            continue
        scored += 1
        candidate = score_eu_candidate(
            ticker=ticker.upper(),
            timestamp=timestamp,
            now=now,
            quote=q,
            hist_bars=bars_for(ticker),
            config=config,
        )
        if candidate is not None:
            candidates.append(candidate)

    missing = len(tickers) - scored
    if missing:
        warnings.append(f"{missing} universe ticker(s) had no quote in the FMP response.")

    record_score = int(config["scanner"].get("min_score_to_record", 60))
    recorded = sorted([c for c in candidates if c.score >= record_score], key=lambda c: c.score, reverse=True)
    append_signal_rows(SIGNALS_CSV, recorded)

    history_days = len({r["date"] for r in csv.DictReader(HISTORY_CSV.open())}) if HISTORY_CSV.exists() else 0
    report = write_eu_report(now, recorded, config, warnings, len(tickers), scored, history_days)
    print(f"Wrote report: {report}")
    print(f"Recorded candidates: {len(recorded)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
