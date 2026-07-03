#!/usr/bin/env python3
"""Stooq data access for the EU scanner — free CSV endpoints, no API key.

Stooq (stooq.com) serves delayed quotes and full daily OHLCV history as plain
CSV. It covers XETRA (`sap.de`) and London (`vod.uk` — note: Stooq uses .UK
where FMP/eToro use .L). Quotes are delayed ~15 minutes, which is fine for the
scan slots; history depth easily covers the 50-day lookback.

Endpoints:
- batch quotes:  /q/l/?s=sap.de+rhm.de&f=sd2t2ohlcv&h&e=csv
- daily history: /q/d/l/?s=rhm.de&i=d

Be polite: batch quotes into few requests, sleep between history fetches, and
expect "N/D" cells for unknown values. Stooq rate-limits heavy scraping by
daily hit count; the scanner's ~4 batch requests/day are far below that, but
the one-time history seeder (~1 request per ticker) should not be looped.
"""

from __future__ import annotations

import csv
import io
import time
import urllib.parse
import urllib.request

BASE_URL = "https://stooq.com"
BATCH_SIZE = 20
USER_AGENT = "TradingJournalScanner/0.1"


def to_stooq_symbol(ticker: str) -> str:
    """FMP/eToro-style symbol -> Stooq symbol (.L becomes .UK)."""
    t = ticker.strip().upper()
    if t.endswith(".L"):
        t = t[:-2] + ".UK"
    return t.lower()


def from_stooq_symbol(symbol: str) -> str:
    """Stooq symbol -> the repo's canonical form (.UK becomes .L)."""
    t = symbol.strip().upper()
    if t.endswith(".UK"):
        t = t[:-3] + ".L"
    return t


def _fetch_csv(path_and_query: str) -> list[list[str]]:
    url = f"{BASE_URL}{path_and_query}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    return list(csv.reader(io.StringIO(text)))


def _num(value: str) -> float | None:
    value = (value or "").strip()
    if not value or value.upper() == "N/D":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_quote_rows(rows: list[list[str]]) -> dict[str, dict[str, float | str | None]]:
    """Parse the batch-quote CSV (header: Symbol,Date,Time,Open,High,Low,Close,Volume)
    into normalized quote dicts keyed by canonical ticker."""
    out: dict[str, dict[str, float | str | None]] = {}
    for row in rows:
        if len(row) < 8 or row[0].strip().lower() == "symbol":
            continue
        ticker = from_stooq_symbol(row[0])
        close = _num(row[6])
        if close is None:
            continue
        out[ticker] = {
            "symbol": ticker,
            "quote_date": row[1].strip(),
            "price": close,
            "open": _num(row[3]),
            "dayHigh": _num(row[4]),
            "dayLow": _num(row[5]),
            "volume": _num(row[7]) or 0.0,
            # Not provided by Stooq; the scanner derives these from the
            # accumulated local history instead.
            "previousClose": None,
            "avgVolume": None,
            "exchange": "LSE" if ticker.endswith(".L") else "XETRA",
        }
    return out


def fetch_batch_quotes(tickers: list[str]) -> dict[str, dict[str, float | str | None]]:
    quotes: dict[str, dict[str, float | str | None]] = {}
    symbols = [to_stooq_symbol(t) for t in tickers]
    for i in range(0, len(symbols), BATCH_SIZE):
        batch = symbols[i : i + BATCH_SIZE]
        query = urllib.parse.urlencode({"s": " ".join(batch), "f": "sd2t2ohlcv", "h": "", "e": "csv"})
        # Stooq expects '+' between symbols; urlencode turns spaces into '+'.
        quotes.update(parse_quote_rows(_fetch_csv(f"/q/l/?{query}")))
        time.sleep(0.5)
    return quotes


def parse_history_rows(rows: list[list[str]]) -> list[dict[str, float | str | None]]:
    """Parse the daily-history CSV (header: Date,Open,High,Low,Close,Volume),
    oldest first, into bar dicts."""
    bars: list[dict[str, float | str | None]] = []
    for row in rows:
        if len(row) < 6 or row[0].strip().lower() == "date":
            continue
        close = _num(row[4])
        if close is None or not row[0].strip():
            continue
        bars.append(
            {
                "date": row[0].strip(),
                "open": _num(row[1]),
                "high": _num(row[2]),
                "low": _num(row[3]),
                "close": close,
                "volume": _num(row[5]) or 0.0,
            }
        )
    bars.sort(key=lambda b: b["date"])
    return bars


def fetch_daily_history(ticker: str) -> list[dict[str, float | str | None]]:
    query = urllib.parse.urlencode({"s": to_stooq_symbol(ticker), "i": "d"})
    return parse_history_rows(_fetch_csv(f"/q/d/l/?{query}"))
