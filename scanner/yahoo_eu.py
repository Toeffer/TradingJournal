#!/usr/bin/env python3
"""Yahoo Finance fallback for the EU scanner — keyless, no monthly cost.

Exists because the two other sources both have a blocker for scheduled runs:
Stooq rate-limits/blocks GitHub-hosted runner IPs, and FMP needs a paid key —
which the journal's own doctrine says not to buy until the EU pipeline has
proven itself (MASTERPLAN Phase 1).

Yahoo's v8 chart endpoint is public JSON, accepts the same symbol format the
repo already uses (SAP.DE, VOD.L — no mapping needed), and one request per
ticker returns BOTH the live quote (meta) and months of daily OHLCV bars.
The scanner uses the bars to backfill data/eu_quote_history.csv for free,
which removes the accumulator warm-up without any seeding step.

Politeness/robustness: one request per ticker with a small sleep, a browser
User-Agent (Yahoo 403s generic clients), and one retry on 429/5xx. Failures
are collected per ticker; only a full-universe failure raises.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://query1.finance.yahoo.com"
RANGE = "6mo"  # ~128 daily bars: covers 50d breakouts and EMA50/MACD warm-up
SLEEP_BETWEEN = 0.4
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

BLOCKED_HINT = (
    "Yahoo Finance chart API rejected the request. If this persists across "
    "runs it is rate-limiting this IP; the free options are exhausted for "
    "this run — the next scheduled scan will retry."
)


def _fetch_json(url: str, retries: int = 1) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            transient = e.code == 429 or e.code >= 500
            if transient and attempt < retries:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise RuntimeError(f"Yahoo HTTP {e.code} from {url.split('?')[0]}. {BLOCKED_HINT}") from e
    raise RuntimeError(f"Yahoo fetch failed for {url.split('?')[0]}")  # pragma: no cover


def _num(value: Any) -> float | None:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def fetch_chart(ticker: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Return (scanner-shaped quote, daily bars oldest-first) for one ticker."""
    url = f"{BASE_URL}/v8/finance/chart/{urllib.parse.quote(ticker)}?range={RANGE}&interval=1d"
    data = _fetch_json(url)
    chart = data.get("chart") or {}
    if chart.get("error"):
        raise RuntimeError(f"Yahoo chart error for {ticker}: {chart['error']}")
    results = chart.get("result") or []
    if not results:
        raise RuntimeError(f"Yahoo returned no chart result for {ticker}")
    result = results[0]
    meta = result.get("meta") or {}
    timestamps = result.get("timestamp") or []
    quote_arrays = ((result.get("indicators") or {}).get("quote") or [{}])[0]

    bars: list[dict[str, Any]] = []
    opens = quote_arrays.get("open") or []
    highs = quote_arrays.get("high") or []
    lows = quote_arrays.get("low") or []
    closes = quote_arrays.get("close") or []
    volumes = quote_arrays.get("volume") or []
    for i, ts in enumerate(timestamps):
        close = _num(closes[i] if i < len(closes) else None)
        if close is None:
            continue  # Yahoo pads holidays/suspensions with nulls
        bars.append(
            {
                "date": time.strftime("%Y-%m-%d", time.gmtime(int(ts))),
                "open": _num(opens[i] if i < len(opens) else None),
                "high": _num(highs[i] if i < len(highs) else None),
                "low": _num(lows[i] if i < len(lows) else None),
                "close": close,
                "volume": _num(volumes[i] if i < len(volumes) else None) or 0.0,
            }
        )
    bars.sort(key=lambda b: b["date"])

    price = _num(meta.get("regularMarketPrice"))
    if price is None and bars:
        price = bars[-1]["close"]
    last = bars[-1] if bars else {}
    # previousClose is left to the caller's history-derived fallback:
    # meta.chartPreviousClose is the close before the RANGE start (months old),
    # not yesterday's close — using it here would corrupt change_pct.
    quote = {
        "symbol": ticker.upper(),
        "price": price,
        "open": _num(meta.get("regularMarketOpen")) or last.get("open"),
        "dayHigh": _num(meta.get("regularMarketDayHigh")) or last.get("high"),
        "dayLow": _num(meta.get("regularMarketDayLow")) or last.get("low"),
        "volume": _num(meta.get("regularMarketVolume")) or last.get("volume") or 0.0,
        "previousClose": None,
        "avgVolume": None,
        "exchange": meta.get("exchangeName", ""),
    }
    return quote, bars


def fetch_batch_quotes(
    tickers: list[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]], list[str]]:
    """Return (quotes, history bars, per-ticker failure messages), keyed by
    canonical upper ticker. Raises only if every ticker failed."""
    quotes: dict[str, dict[str, Any]] = {}
    history: dict[str, list[dict[str, Any]]] = {}
    failures: list[str] = []
    for ticker in tickers:
        try:
            quote, bars = fetch_chart(ticker)
        except Exception as exc:  # noqa: BLE001 - one bad ticker shouldn't kill the run
            failures.append(f"{ticker}: {exc}")
            continue
        if quote["price"] is None:
            failures.append(f"{ticker}: no price in Yahoo response")
            continue
        key = ticker.upper()
        quotes[key] = quote
        history[key] = bars
        time.sleep(SLEEP_BETWEEN)
    if tickers and not quotes:
        raise RuntimeError(
            f"Yahoo returned no usable quotes for all {len(tickers)} ticker(s). "
            f"First error: {failures[0] if failures else 'unknown'}"
        )
    return quotes, history, failures
