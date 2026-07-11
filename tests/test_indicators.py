from scanner.indicators import bollinger_percent_b, ema, rsi


def test_ema_is_sma_seeded() -> None:
    assert ema([1.0, 2.0, 3.0, 4.0], 3) == 3.0


def test_rsi_all_gains_is_one_hundred() -> None:
    closes = [float(value) for value in range(1, 17)]
    assert rsi(closes, 14) == 100.0


def test_bollinger_flat_series_is_undefined() -> None:
    assert bollinger_percent_b([10.0] * 20) is None
