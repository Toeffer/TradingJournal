#!/usr/bin/env python3
"""Twelve Data quotes for the EU scanner (TWELVE_DATA_API_KEY secret).

Slot in the source chain: after FMP, before the keyless fallbacks. Twelve
Data's /quote endpoint returns everything the scanner wants — including
previous_close and average_volume, which Stooq and Yahoo lack — so relative
volume and change% come straight from the source instead of the accumulated
history.

Free ("Basic") plan limits shape this module:
- 8 API credits per minute, 800 per day. Each symbol in a batch costs one
  credit, so symbols go out in batches of `credits_per_minute` with a ~60s
  pause between batches. A 46-ticker universe is ~6 batches ≈ 5-6 minutes per
  scan and ~184 credits/day across the 4 scheduled runs — comfortably inside
  the daily budget. If the plan is upgraded, raise credits_per_minute in
  config.toml ([eu.twelvedata]) and the pauses shrink accordingly.
- EU exchange coverage varies by plan. If XETRA/LSE symbols are plan-gated,
  the API answers per symbol with a code/message instead of a quote; those
  surface as warnings and the scanner falls through to the next source.

Symbol mapping: the repo's FMP/eToro format (SAP.DE, VOD.L) maps to Twelve
Data as symbol=SAP&exchange=XETRA / symbol=VOD&exchange=LSE. Requests are
grouped per exchange so the exchange parameter stays unambiguous.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://api.twelvedata.com"
USER_AGENT = "TradingJournalScanner/0.1"
DEFAULT_CREDITS_PER_MINUTE = 8
BATCH_PAUSE_SECONDS = 61.0


def split_symbol(ticker: str) -> tuple[str, str]:
    """Repo ticker -> (Twelve Data symbol, exchange name)."""
    t = ticker.strip().upper()
    if t.endswith(".L"):
        return t[:-2], "LSE"
    if t.endswith(".DE"):
        return t[:-3], "XETRA"
    return t, "XETRA"


def _fetch_json(url: str, retries: int = 1) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            if (e.code == 429 or e.code >= 500) and attempt < retries:
                time.sleep(BATCH_PAUSE_SECONDS)
                continue
            raise RuntimeError(f"Twelve Data HTTP {e.code} from {url.split('?')[0]}") from e
    raise RuntimeError("Twelve Data fetch failed")  # pragma: no cover


def _num(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _to_scanner_quote(ticker: str, payload: dict[str, Any], exchange: str) -> dict[str, Any]:
    return {
        "symbol": ticker.upper(),
        "price": _num(payload.get("close")),
        "open": _num(payload.get("open")),
        "dayHigh": _num(payload.get("high")),
        "dayLow": _num(payload.get("low")),
        "volume": _num(payload.get("volume")) or 0.0,
        "previousClose": _num(payload.get("previous_close")),
        "avgVolume": _num(payload.get("average_volume")),
        "changePercentage": _num(payload.get("percent_change")),
        "exchange": payload.get("exchange") or exchange,
    }


def fetch_batch_quotes(
    tickers: list[str],
    api_key: str,
    credits_per_minute: int = DEFAULT_CREDITS_PER_MINUTE,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Return (quotes keyed by canonical repo ticker, per-symbol failure
    messages). Raises only if the whole universe yields nothing usable —
    e.g. a bad key or an entirely plan-gated exchange."""
    by_exchange: dict[str, list[tuple[str, str]]] = {}
    for ticker in tickers:
        symbol, exchange = split_symbol(ticker)
        by_exchange.setdefault(exchange, []).append((ticker.upper(), symbol))

    quotes: dict[str, dict[str, Any]] = {}
    failures: list[str] = []
    batch_size = max(1, int(credits_per_minute))
    first_batch = True
    for exchange, pairs in by_exchange.items():
        for i in range(0, len(pairs), batch_size):
            batch = pairs[i : i + batch_size]
            if not first_batch:
                # Stay under the per-minute credit limit; each symbol = 1 credit.
                time.sleep(BATCH_PAUSE_SECONDS)
            first_batch = False
            symbols = ",".join(sym for _, sym in batch)
            query = urllib.parse.urlencode({"symbol": symbols, "exchange": exchange, "apikey": api_key})
            data = _fetch_json(f"{BASE_URL}/quote?{query}")

            if isinstance(data, dict) and data.get("status") == "error":
                # Whole-request error (bad key, hard rate limit): surface and stop.
                raise RuntimeError(f"Twelve Data error {data.get('code')}: {data.get('message')}")
            # Single-symbol requests return the quote flat; batches return
            # an object keyed by symbol.
            keyed = data if len(batch) > 1 else {batch[0][1]: data}
            if not isinstance(keyed, dict):
                raise RuntimeError(f"Unexpected Twelve Data response shape: {type(data).__name__}")

            for ticker, symbol in batch:
                entry = keyed.get(symbol)
                if not isinstance(entry, dict):
                    failures.append(f"{ticker}: missing from Twelve Data response")
                    continue
                if entry.get("status") == "error" or ("code" in entry and "close" not in entry):
                    failures.append(f"{ticker}: {entry.get('message') or entry.get('code')}")
                    continue
                quote = _to_scanner_quote(ticker, entry, exchange)
                if quote["price"] is None:
                    failures.append(f"{ticker}: no price in Twelve Data response")
                    continue
                quotes[ticker] = quote

    if tickers and not quotes:
        first = failures[0] if failures else "no data returned"
        raise RuntimeError(
            f"Twelve Data returned no usable quotes for all {len(tickers)} ticker(s). "
            f"First error: {first}"
        )
    return quotes, failures
