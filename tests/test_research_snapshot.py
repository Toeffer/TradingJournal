from scripts.build_research_snapshot import build_rows, latest_signals, listing_for


def test_latest_signal_per_market_and_ticker() -> None:
    rows = [
        {"ticker": "ABC", "market": "US", "timestamp": "2026-01-01T10:00:00Z", "price": "10"},
        {"ticker": "ABC", "market": "US", "timestamp": "2026-01-01T11:00:00Z", "price": "11"},
        {"ticker": "ABC.DE", "market": "EU-XETRA", "timestamp": "2026-01-01T09:00:00Z", "price": "20"},
    ]

    latest = latest_signals(rows)

    assert len(latest) == 2
    assert next(row for row in latest if row["market"] == "US")["price"] == "11"


def test_snapshot_calculates_dollar_volume_and_listing() -> None:
    rows = [
        {
            "ticker": "ABC.DE",
            "market": "EU-XETRA",
            "timestamp": "2026-01-01T09:00:00Z",
            "price": "20",
            "avg_volume_20d": "100000",
            "source": "stooq",
            "score": "70",
        }
    ]

    output = build_rows(rows, "neutral")

    assert output[0]["exchange"] == "XETRA"
    assert output[0]["currency"] == "EUR"
    assert output[0]["avg_dollar_volume"] == "2000000"
    assert output[0]["market_regime"] == "neutral"


def test_listing_defaults_to_usd() -> None:
    assert listing_for("ABC", "US") == ("US", "USD")
