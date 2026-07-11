#!/usr/bin/env python3
"""Validate candidate evidence manifests without third-party dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = REPO_ROOT / "research/manifests"
HEX64 = re.compile(r"^[a-f0-9]{64}$")
CLASSIFICATIONS = {"ACTIONABLE", "EARLY_WATCH", "REJECT"}
SOURCE_TYPES = {"primary", "market_data", "reputable_secondary", "repository", "other"}
SOURCE_TAGS = {"routine", "scanner_seed", "routine+scanner_seed", "prior_report"}


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def parse_date(value: Any, label: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{label}: expected YYYY-MM-DD string")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: invalid date `{value}`")
        return None


def parse_datetime(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{label}: expected ISO datetime string")
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label}: invalid datetime `{value}`")
        return None


def number(value: Any, label: str, errors: list[str], *, positive: bool = False) -> float | None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append(f"{label}: expected number")
        return None
    result = float(value)
    if positive and result <= 0:
        errors.append(f"{label}: must be positive")
    return result


def required_text(mapping: dict[str, Any], key: str, label: str, errors: list[str]) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{key}: required non-empty text")
        return ""
    return value.strip()


def validate_evidence(
    candidate: dict[str, Any],
    label: str,
    errors: list[str],
) -> tuple[int, int]:
    evidence = candidate.get("evidence")
    if not isinstance(evidence, list):
        errors.append(f"{label}.evidence: expected list")
        return 0, 0
    primary = 0
    market_data = 0
    for index, item in enumerate(evidence):
        item_label = f"{label}.evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_label}: expected object")
            continue
        required_text(item, "claim", item_label, errors)
        source_type = item.get("source_type")
        if source_type not in SOURCE_TYPES:
            errors.append(f"{item_label}.source_type: invalid `{source_type}`")
        location = required_text(item, "location", item_label, errors)
        parse_datetime(item.get("accessed_at"), f"{item_label}.accessed_at", errors)
        if source_type == "primary":
            primary += 1
            if not is_url(location):
                errors.append(f"{item_label}.location: primary evidence must be an opened URL")
        if source_type == "market_data":
            market_data += 1
    return primary, market_data


def validate_catalyst(
    candidate: dict[str, Any],
    label: str,
    report_date: date,
    classification: str,
    errors: list[str],
) -> None:
    catalyst = candidate.get("catalyst")
    if not isinstance(catalyst, dict):
        errors.append(f"{label}.catalyst: required object")
        return
    required_text(catalyst, "event", f"{label}.catalyst", errors)
    event_date = parse_date(catalyst.get("date"), f"{label}.catalyst.date", errors)
    if catalyst.get("date_status") != "verified":
        errors.append(f"{label}.catalyst.date_status: final candidates require `verified`")
    if catalyst.get("source_type") != "primary":
        errors.append(f"{label}.catalyst.source_type: final candidates require `primary`")
    source_url = required_text(catalyst, "source_url", f"{label}.catalyst", errors)
    if source_url and not is_url(source_url):
        errors.append(f"{label}.catalyst.source_url: expected opened http(s) URL")
    parse_datetime(catalyst.get("verified_at"), f"{label}.catalyst.verified_at", errors)
    if event_date is None:
        return
    days = (event_date - report_date).days
    if classification == "ACTIONABLE" and not 0 <= days <= 21:
        errors.append(f"{label}: Actionable catalyst is {days} days away, expected 0..21")
    if classification == "EARLY_WATCH" and not 22 <= days <= 42:
        errors.append(f"{label}: Early Watch catalyst is {days} days away, expected 22..42")


def validate_market_data(candidate: dict[str, Any], label: str, errors: list[str]) -> None:
    market = candidate.get("market_data")
    if not isinstance(market, dict):
        errors.append(f"{label}.market_data: required object")
        return
    parse_datetime(market.get("as_of"), f"{label}.market_data.as_of", errors)
    required_text(market, "data_source", f"{label}.market_data", errors)
    number(market.get("price"), f"{label}.market_data.price", errors, positive=True)
    number(
        market.get("avg_dollar_volume"),
        f"{label}.market_data.avg_dollar_volume",
        errors,
        positive=True,
    )
    market_cap = market.get("market_cap")
    if market_cap is not None:
        number(market_cap, f"{label}.market_data.market_cap", errors, positive=True)


def validate_setup(candidate: dict[str, Any], label: str, errors: list[str]) -> None:
    setup = candidate.get("setup")
    if not isinstance(setup, dict):
        errors.append(f"{label}.setup: Actionable candidate requires setup object")
        return
    direction = setup.get("direction")
    if direction not in {"long", "short"}:
        errors.append(f"{label}.setup.direction: expected long or short")
    required_text(setup, "why_now", f"{label}.setup", errors)
    required_text(setup, "level_basis", f"{label}.setup", errors)
    entry = number(setup.get("entry"), f"{label}.setup.entry", errors, positive=True)
    stop = number(setup.get("stop"), f"{label}.setup.stop", errors, positive=True)
    target = number(setup.get("target"), f"{label}.setup.target", errors, positive=True)
    planned = number(setup.get("planned_r"), f"{label}.setup.planned_r", errors)
    holding = setup.get("max_holding_days")
    if not isinstance(holding, int) or isinstance(holding, bool) or holding < 1:
        errors.append(f"{label}.setup.max_holding_days: expected positive integer")
    if not isinstance(setup.get("exit_before_catalyst"), bool):
        errors.append(f"{label}.setup.exit_before_catalyst: expected boolean")
    if None in {entry, stop, target, planned} or direction not in {"long", "short"}:
        return
    if direction == "long":
        if not target > entry > stop:
            errors.append(f"{label}.setup: long requires target > entry > stop")
            return
        computed = (target - entry) / (entry - stop)
    else:
        if not target < entry < stop:
            errors.append(f"{label}.setup: short requires target < entry < stop")
            return
        computed = (entry - target) / (stop - entry)
    if planned < 1.5:
        errors.append(f"{label}.setup.planned_r: {planned:.2f} is below 1.5")
    if abs(planned - computed) > 0.05:
        errors.append(
            f"{label}.setup.planned_r: logged {planned:.2f}, computed {computed:.2f}"
        )


def validate_candidate(
    candidate: Any,
    index: int,
    report_date: date,
    errors: list[str],
) -> tuple[str, int, int]:
    label = f"candidates[{index}]"
    if not isinstance(candidate, dict):
        errors.append(f"{label}: expected object")
        return "", 0, 0
    ticker = required_text(candidate, "ticker", label, errors).upper()
    required_text(candidate, "company", label, errors)
    required_text(candidate, "exchange", label, errors)
    currency = required_text(candidate, "currency", label, errors)
    if currency and len(currency) != 3:
        errors.append(f"{label}.currency: expected three-letter code")
    classification = candidate.get("classification")
    if classification not in CLASSIFICATIONS:
        errors.append(f"{label}.classification: invalid `{classification}`")
        classification = ""
    if candidate.get("source_tag") not in SOURCE_TAGS:
        errors.append(f"{label}.source_tag: invalid `{candidate.get('source_tag')}`")
    primary_count, market_count = validate_evidence(candidate, label, errors)

    if classification == "REJECT":
        required_text(candidate, "rejection_reason", label, errors)
        if candidate.get("red_team_verdict") != "REJECT":
            errors.append(f"{label}.red_team_verdict: rejected candidate requires REJECT")
        return ticker, primary_count, market_count

    validate_catalyst(candidate, label, report_date, classification, errors)
    validate_market_data(candidate, label, errors)
    if primary_count < 1:
        errors.append(f"{label}.evidence: final candidate requires primary evidence")
    if market_count < 1:
        errors.append(f"{label}.evidence: final candidate requires market-data evidence")
    for field in ("expectations", "priced_in", "bull_case", "bear_case", "pre_mortem"):
        required_text(candidate, field, label, errors)
    if candidate.get("risk_rating") not in {"Low", "Medium", "High"}:
        errors.append(f"{label}.risk_rating: invalid")
    if candidate.get("confidence") not in {"Low", "Medium", "High"}:
        errors.append(f"{label}.confidence: invalid")
    required_text(candidate, "red_team_argument", label, errors)

    verdict = candidate.get("red_team_verdict")
    if classification == "ACTIONABLE":
        if verdict != "SURVIVE":
            errors.append(f"{label}.red_team_verdict: Actionable candidate must SURVIVE")
        validate_setup(candidate, label, errors)
    elif classification == "EARLY_WATCH":
        if verdict not in {"SURVIVE", "DOWNGRADE_EARLY_WATCH"}:
            errors.append(f"{label}.red_team_verdict: invalid for Early Watch")
        parse_date(candidate.get("next_review_date"), f"{label}.next_review_date", errors)
    return ticker, primary_count, market_count


def validate_manifest(data: Any, *, root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest: expected JSON object"]
    if data.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    report_date = parse_date(data.get("report_date"), "report_date", errors)
    parse_datetime(data.get("generated_at"), "generated_at", errors)
    for key in ("model", "research_mode", "repository_commit", "input_snapshot"):
        required_text(data, key, "manifest", errors)
    if data.get("method") not in {"screener-first", "catalyst-first", "hybrid"}:
        errors.append("method: expected screener-first, catalyst-first, or hybrid")
    enabled = data.get("enabled_sources")
    if not isinstance(enabled, list) or not all(isinstance(item, str) and item for item in enabled):
        errors.append("enabled_sources: expected list of non-empty strings")
    digest = data.get("input_snapshot_sha256")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        errors.append("input_snapshot_sha256: expected lowercase SHA-256")
    snapshot = data.get("input_snapshot")
    if isinstance(snapshot, str) and snapshot:
        snapshot_path = root / snapshot
        if not snapshot_path.exists():
            errors.append(f"input_snapshot: `{snapshot}` does not exist")
        elif isinstance(digest, str) and HEX64.fullmatch(digest):
            actual = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
            if actual != digest:
                errors.append(f"input_snapshot_sha256: expected {actual} for `{snapshot}`")

    counts = data.get("source_counts")
    if not isinstance(counts, dict):
        errors.append("source_counts: expected object")
        counts = {}
    for key in ("opened", "primary"):
        if not isinstance(counts.get(key), int) or isinstance(counts.get(key), bool) or counts.get(key, -1) < 0:
            errors.append(f"source_counts.{key}: expected non-negative integer")

    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        errors.append("candidates: expected list")
        return errors
    seen: set[str] = set()
    actual_primary = 0
    actual_evidence = 0
    safe_report_date = report_date or date.min
    for index, candidate in enumerate(candidates):
        ticker, primary_count, market_count = validate_candidate(
            candidate, index, safe_report_date, errors
        )
        actual_primary += primary_count
        actual_evidence += primary_count + market_count
        if ticker in seen:
            errors.append(f"candidates[{index}].ticker: duplicate `{ticker}`")
        elif ticker:
            seen.add(ticker)
    if isinstance(counts.get("primary"), int) and counts["primary"] < actual_primary:
        errors.append(
            f"source_counts.primary: {counts['primary']} is below manifest evidence count {actual_primary}"
        )
    if isinstance(counts.get("opened"), int) and counts["opened"] < actual_evidence:
        errors.append(
            f"source_counts.opened: {counts['opened']} is below required evidence count {actual_evidence}"
        )
    return errors


def validate_path(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]
    return validate_manifest(data)


def manifest_paths(arguments: list[str], all_manifests: bool) -> list[Path]:
    if all_manifests:
        return sorted(MANIFEST_DIR.glob("candidates-*.json"))
    return [Path(argument) for argument in arguments]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--all", action="store_true", help="Validate all candidate manifests")
    args = parser.parse_args()
    paths = manifest_paths(args.paths, args.all)
    if not paths:
        print("No candidate manifests selected.")
        return 0
    failed = False
    for path in paths:
        errors = validate_path(path)
        if errors:
            failed = True
            print(f"{path}:")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{path}: valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
