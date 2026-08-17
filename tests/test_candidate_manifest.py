import hashlib
from pathlib import Path

from scripts.validate_candidate_manifest import validate_manifest


def valid_manifest(tmp_path: Path) -> dict[str, object]:
    snapshot = tmp_path / "data/research_snapshot.csv"
    snapshot.parent.mkdir(parents=True)
    snapshot.write_text("ticker,price\nABC,10\n", encoding="utf-8")
    digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    return {
        "schema_version": 1,
        "report_date": "2026-01-01",
        "generated_at": "2026-01-01T12:00:00+00:00",
        "model": "test-model",
        "research_mode": "deep_research",
        "repository_commit": "abcdef1234567",
        "method": "hybrid",
        "enabled_sources": ["public_web", "github"],
        "input_snapshot": "data/research_snapshot.csv",
        "input_snapshot_sha256": digest,
        "source_counts": {"opened": 3, "primary": 1},
        "candidates": [
            {
                "ticker": "ABC",
                "company": "ABC Corp",
                "classification": "ACTIONABLE",
                "source_tag": "routine",
                "exchange": "NASDAQ",
                "currency": "USD",
                "catalyst": {
                    "event": "Investor day",
                    "date": "2026-01-15",
                    "date_status": "verified",
                    "source_type": "primary",
                    "source_url": "https://example.com/ir/event",
                    "verified_at": "2026-01-01T11:00:00+00:00",
                },
                "market_data": {
                    "as_of": "2026-01-01T10:00:00+00:00",
                    "data_source": "snapshot",
                    "price": 10.0,
                    "market_cap": 1_000_000_000,
                    "avg_dollar_volume": 30_000_000,
                },
                "expectations": "No material change is priced in.",
                "priced_in": "The stock remains inside its prior range.",
                "bull_case": "New targets exceed expectations.",
                "bear_case": "Targets disappoint and the range breaks down.",
                "pre_mortem": "The event proves incremental rather than material.",
                "risk_rating": "Medium",
                "confidence": "Medium",
                "setup": {
                    "direction": "long",
                    "why_now": "Price is testing the top of a six-week base.",
                    "entry": 10.0,
                    "stop": 9.0,
                    "target": 12.0,
                    "planned_r": 2.0,
                    "level_basis": "Stop below the confirmed base low.",
                    "max_holding_days": 10,
                    "exit_before_catalyst": True,
                },
                "red_team_verdict": "SURVIVE",
                "red_team_argument": "The event may be incremental, but guidance scope is material.",
                "evidence": [
                    {
                        "claim": "Investor day date",
                        "source_type": "primary",
                        "location": "https://example.com/ir/event",
                        "published_at": "2025-12-20",
                        "accessed_at": "2026-01-01T11:00:00+00:00",
                    },
                    {
                        "claim": "Price and liquidity",
                        "source_type": "market_data",
                        "location": "data/research_snapshot.csv",
                        "published_at": None,
                        "accessed_at": "2026-01-01T11:00:00+00:00",
                    },
                ],
            }
        ],
    }


def test_valid_actionable_manifest(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    assert validate_manifest(manifest, root=tmp_path) == []


def test_unverified_date_is_rejected(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["candidates"][0]["catalyst"]["date_status"] = "secondary_only"  # type: ignore[index]

    errors = validate_manifest(manifest, root=tmp_path)

    assert any("date_status" in error for error in errors)


def test_actionable_horizon_is_enforced(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    manifest["candidates"][0]["catalyst"]["date"] = "2026-02-15"  # type: ignore[index]

    errors = validate_manifest(manifest, root=tmp_path)

    assert any("expected 0..21" in error for error in errors)


def test_refreshed_snapshot_passes_when_archive_matches(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    live = tmp_path / "data/research_snapshot.csv"
    archive = tmp_path / "research/snapshots/research_snapshot-2026-01-01.csv"
    archive.parent.mkdir(parents=True)
    archive.write_bytes(live.read_bytes())
    # Automation refreshes the live snapshot after the research run.
    live.write_text("ticker,price\nXYZ,99\n", encoding="utf-8")

    assert validate_manifest(manifest, root=tmp_path) == []


def test_refreshed_snapshot_fails_without_matching_archive(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    live = tmp_path / "data/research_snapshot.csv"
    live.write_text("ticker,price\nXYZ,99\n", encoding="utf-8")

    errors = validate_manifest(manifest, root=tmp_path)

    assert any("input_snapshot_sha256" in error for error in errors)


def test_grandfathered_manifest_skips_unverifiable_snapshot_check(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    live = tmp_path / "data/research_snapshot.csv"
    live.write_text("ticker,price\nXYZ,99\n", encoding="utf-8")

    errors = validate_manifest(manifest, root=tmp_path, manifest_name="candidates-2026-07-26.json")

    assert errors == []


def test_grandfathering_is_scoped_to_named_manifests_only(tmp_path: Path) -> None:
    manifest = valid_manifest(tmp_path)
    live = tmp_path / "data/research_snapshot.csv"
    live.write_text("ticker,price\nXYZ,99\n", encoding="utf-8")

    errors = validate_manifest(manifest, root=tmp_path, manifest_name="candidates-2026-09-13.json")

    assert any("input_snapshot_sha256" in error for error in errors)
