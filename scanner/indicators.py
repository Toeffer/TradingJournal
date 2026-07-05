#!/usr/bin/env python3
"""Deterministic technical indicators for scanner measurement columns.

Stdlib-only, adapted from the approach in oft3r/agentic-trading-desk: the
indicator maths lives in plain Python so results are reproducible and never
depend on an LLM doing arithmetic.

IMPORTANT (MASTERPLAN Phase 1): these values are recorded in
data/scanner_signals.csv as measurement-only columns. They do NOT contribute
to the scanner score and must not, until the score-bucket evaluation shows
they separate forward returns — promoting an indicator into the score is a
phase-transition decision, not a code tweak.

Conventions (matching TradingView so values can be sanity-checked by eye):
- EMA is seeded with the SMA of the first `period` closes.
- RSI uses Wilder's smoothing (first average = simple mean of the first
  `period` gains/losses, then alpha = 1/period).
- MACD is EMA12 - EMA26 with an EMA9 signal line; we report the histogram.
- Bollinger Bands are 20-period SMA +/- 2 population standard deviations;
  we report %B (0 = lower band, 1 = upper band).

All functions return None when there is not enough history — consumers must
leave the CSV cell blank rather than guess.
"""

from __future__ import annotations

import math
import statistics


def ema_series(closes: list[float], period: int) -> list[float | None]:
    """EMA per bar, SMA-seeded; None until the seed window is full."""
    if period <= 0 or len(closes) < period:
        return [None] * len(closes)
    out: list[float | None] = [None] * (period - 1)
    seed = statistics.mean(closes[:period])
    out.append(seed)
    alpha = 2.0 / (period + 1)
    prev = seed
    for close in closes[period:]:
        prev = (close - prev) * alpha + prev
        out.append(prev)
    return out


def ema(closes: list[float], period: int) -> float | None:
    series = ema_series(closes, period)
    return series[-1] if series else None


def rsi(closes: list[float], period: int = 14) -> float | None:
    """Wilder's RSI; needs at least period+1 closes."""
    if len(closes) < period + 1:
        return None
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [max(d, 0.0) for d in deltas]
    losses = [max(-d, 0.0) for d in deltas]
    avg_gain = statistics.mean(gains[:period])
    avg_loss = statistics.mean(losses[:period])
    for g, l in zip(gains[period:], losses[period:]):
        avg_gain = (avg_gain * (period - 1) + g) / period
        avg_loss = (avg_loss * (period - 1) + l) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - 100.0 / (1.0 + rs)


def macd_histogram(
    closes: list[float], fast: int = 12, slow: int = 26, signal: int = 9
) -> float | None:
    """Latest MACD histogram (MACD line minus signal line)."""
    if len(closes) < slow + signal:
        return None
    fast_series = ema_series(closes, fast)
    slow_series = ema_series(closes, slow)
    macd_line = [
        f - s
        for f, s in zip(fast_series, slow_series)
        if f is not None and s is not None
    ]
    signal_series = ema_series(macd_line, signal)
    if not signal_series or signal_series[-1] is None:
        return None
    return macd_line[-1] - signal_series[-1]


def bollinger_percent_b(
    closes: list[float], period: int = 20, num_std: float = 2.0
) -> float | None:
    """%B of the last close: (close - lower) / (upper - lower)."""
    if len(closes) < period:
        return None
    window = closes[-period:]
    mid = statistics.mean(window)
    std = statistics.pstdev(window)
    if std == 0:
        return None
    upper = mid + num_std * std
    lower = mid - num_std * std
    return (closes[-1] - lower) / (upper - lower)


def compute_indicator_columns(closes: list[float]) -> dict[str, float | None]:
    """The measurement-only columns recorded per signal.

    `closes` is the daily close history oldest-first, with the current price
    appended as the latest close (the scanner runs intraday, so "close" for
    today is the live snapshot — same convention as the score components).

    Distances and the MACD histogram are expressed as % of price so values
    are comparable across tickers of any price level.
    """
    clean = [c for c in closes if c is not None and math.isfinite(c) and c > 0]
    if len(clean) < 2:
        return {
            "rsi14": None,
            "ema20_dist_pct": None,
            "ema50_dist_pct": None,
            "macd_hist_pct": None,
            "bb_percent_b": None,
        }
    price = clean[-1]
    ema20 = ema(clean, 20)
    ema50 = ema(clean, 50)
    hist = macd_histogram(clean)
    return {
        "rsi14": rsi(clean, 14),
        "ema20_dist_pct": ((price / ema20) - 1) * 100 if ema20 else None,
        "ema50_dist_pct": ((price / ema50) - 1) * 100 if ema50 else None,
        "macd_hist_pct": (hist / price) * 100 if hist is not None else None,
        "bb_percent_b": bollinger_percent_b(clean),
    }
