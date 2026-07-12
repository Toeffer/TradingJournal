from datetime import date, datetime, timezone

from scripts import build_research_snapshot as builder
from scripts.build_research_snapshot import (
    active_discovery_seeds,
    build_rows,
    latest_signals,
    listing_for,
    recent_signals,
)


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
    assert output[0]["score"] == "70"
    assert output[0]["discovery_seed"] == "false"


def test_listing_defaults_to_usd() -> None:
    assert listing_for("ABC", "US") == ("US", "USD")


def test_recent_signals_drops_rows_outside_lookback() -> None:
    rows = [
        {"ticker": "OLD", "market": "US", "timestamp": "2026-07-01T12:00:00Z"},
        {"ticker": "NEW", "market": "US", "timestamp": "2026-07-09T12:00:00Z"},
    ]

    result = recent_signals(
        rows,
        as_of=datetime(2026, 7, 12, 12, tzinfo=timezone.utc),
        lookback_days=7,
    )

    assert [row["ticker"] for row in result] == ["NEW"]


def test_expired_manual_seed_is_not_active() -> None:
    seeds = [
        {
            "ticker": "OLD",
            "added_at": "2026-07-01",
            "expires_at": "2026-07-06",
        },
        {
            "ticker": "NEW",
            "added_at": "2026-07-11",
            "expires_at": "2026-07-13",
        },
    ]

    active = active_discovery_seeds(seeds, as_of=date(2026, 7, 12), max_age_days=2)

    assert set(active) == {"NEW"}


def test_legacy_finviz_bonus_is_removed_from_quantitative_score() -> None:
    rows = [
        {
            "ticker": "ABC",
            "market": "US",
            "timestamp": "2026-07-09T12:00:00Z",
            "price": "10",
            "avg_volume_20d": "1000000",
            "source": "alpaca+finviz_manual",
            "score": "70",
        }
    ]

    output = build_rows(rows, "mixed", active_seeds={})

    assert output[0]["score"] == "60"
    assert output[0]["signal_source"] == "alpaca"
    assert output[0]["legacy_seed_tag"] == "true"
    assert output[0]["discovery_seed"] == "false"


def test_active_manual_seed_is_separate_from_score() -> None:
    rows = [
        {
            "ticker": "ABC",
            "market": "US",
            "timestamp": "2026-07-13T12:00:00Z",
            "price": "10",
            "avg_volume_20d": "1000000",
            "source": "alpaca+finviz_manual",
            "score": "60",
        }
    ]

    output = build_rows(rows, "mixed", active_seeds={"ABC": {"ticker": "ABC"}})

    assert output[0]["score"] == "60"
    assert output[0]["discovery_seed"] == "true"
    assert output[0]["discovery_seed_source"] == "finviz_manual"


def test_archive_snapshot_never_overwrites(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(builder, "ARCHIVE_DIR", tmp_path / "research/snapshots")
    when = datetime(2026, 1, 1, 9, 30, tzinfo=timezone.utc)

    first = builder.archive_snapshot(b"a,b\n1,2\n", now=when)
    assert first.name == "research_snapshot-2026-01-01.csv"

    # Same content, same day: reuse the existing archive.
    assert builder.archive_snapshot(b"a,b\n1,2\n", now=when) == first

    # Different content, same day: a suffixed sibling, original untouched.
    second = builder.archive_snapshot(b"a,b\n3,4\n", now=when.replace(hour=15))
    assert second.name == "research_snapshot-2026-01-01-1530.csv"
    assert first.read_bytes() == b"a,b\n1,2\n"
