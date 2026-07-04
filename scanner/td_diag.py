#!/usr/bin/env python3
"""One-shot Twelve Data diagnostic — TEMPORARY, delete after use.

Answers two questions the scan report can't separate:
1. Which addressing form does Twelve Data expect for XETRA/LSE symbols
   (exchange=XETRA vs mic_code=XETR vs symbol suffix/colon forms)?
2. Or are EU equities simply not visible on this plan ("symbol not found"
   for every form)?

Uses ~6 quote credits (free plan allows 8/minute). Never prints the key.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://api.twelvedata.com"
KEY = os.getenv("TWELVE_DATA_API_KEY")


def call(path: str, **params: str) -> None:
    label = f"{path}?" + "&".join(f"{k}={v}" for k, v in params.items())
    params["apikey"] = KEY or ""
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "TradingJournalScanner/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        print(f"--- {label}\n    EXCEPTION: {exc}")
        return
    try:
        data = json.loads(body)
        text = json.dumps(data, ensure_ascii=False)
    except ValueError:
        text = body
    print(f"--- {label}\n    {text[:600]}")


def main() -> int:
    if not KEY:
        print("TWELVE_DATA_API_KEY is empty — nothing to diagnose.", file=sys.stderr)
        return 1
    # Directory lookups are credit-free: what does TD know about these symbols?
    call("/stocks", symbol="ADS")
    call("/stocks", symbol="VOD", country="United Kingdom")
    time.sleep(1)
    # Quote addressing variants (1 credit each; 6 total, under the 8/min cap).
    call("/quote", symbol="ADS", exchange="XETRA")
    call("/quote", symbol="ADS", mic_code="XETR")
    call("/quote", symbol="ADS", exchange="XETR")
    call("/quote", symbol="ADS.DE")
    call("/quote", symbol="VOD", exchange="LSE")
    call("/quote", symbol="VOD", mic_code="XLON")
    time.sleep(1)
    call("/api_usage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
