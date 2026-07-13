#!/usr/bin/env python3
"""Validate the rolling recommendation registry and append-only weekly reviews."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
import tomllib
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data/recommendations.csv"
REVIEWS_PATH = REPO_ROOT / "data/recommendation_reviews.csv"
ARCHIVE_DIR = REPO_ROOT / "research/decisions"
RISK_CONFIG = REPO_ROOT / "config/risk.toml"

REGISTRY_FIELDS = [
    "recommendation_id", "ticker", "first_mentioned_date", "last_reviewed_at",
    "source_report", "status", "direction", "setup_type", "catalyst",
    "catalyst_date", "mention_price", "reference_price", "entry_trigger",
    "trigger_rule", "trigger_expiry", "stop_price", "target_price", "planned_r",
    "action_for_week", "action_reason", "removal_condition", "next_review_date",
    "triggered_at", "triggered_price", "outcome_status", "linked_proposal_id",
    "linked_trade_id", "notes",
]

REVIEW_FIELDS = [
    "review_id", "recommendation_id", "reviewed_at", "ticker", "source_report",
    "prior_status", "new_status", "action_for_week", "reference_price",
    "entry_trigger", "trigger_rule", "trigger_expiry", "stop_price", "target_price",
    "planned_r", "catalyst_date", "action_reason", "removal_condition",
    "next_review_date", "linked_proposal_id", "linked_trade_id", "notes",
]

STATUSES = {
    "new", "carry", "upgraded", "trigger_ready", "triggered", "manage",
    "downgraded", "invalidated", "expired", "archived",
}
TERMINAL_STATUSES = {"invalidated", "expired", "archived"}
ACTIONS = {"enter_if_triggered", "wait_pullback", "monitor", "manage", "remove"}
OUTCOMES = {
    "", "open", "not_triggered", "triggered", "stopped", "target", "timeout",
    "cancelled", "invalidated", "expired", "trade_closed",
}
ARCHIVE_RE = re.compile(r"decisions-(\d{4}-\d{2}-\d{2})(?:-\d{4})?\.csv$")


@dataclass(frozen=True)
class Issue:
    level: str
    path: str
    message: str


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def parse_number(value: str | None) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def parse_date(value: str | None) -> date | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def parse_datetime(value: str | None) -> datetime | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def minimum_planned_r() -> float:
    with RISK_CONFIG.open("rb") as handle:
        return float(tomllib.load(handle)["learning_phase"]["proposal_min_planned_r"])


def require_header(
    path: Path,
    expected: list[str],
    issues: list[Issue],
) -> list[dict[str, str]]:
    header, rows = read_csv(path)
    relative = str(path.relative_to(REPO_ROOT))
    if not header:
        issues.append(Issue("error", relative, "file is missing or empty"))
    elif header != expected:
        issues.append(Issue("error", relative, f"header mismatch; expected {expected}, got {header}"))
    return rows


def validate_trade_levels(row: dict[str, str], ref: str, issues: list[Issue], minimum_r: float) -> None:
    direction = row.get("direction", "").strip()
    entry = parse_number(row.get("entry_trigger"))
    stop = parse_number(row.get("stop_price"))
    target = parse_number(row.get("target_price"))
    planned = parse_number(row.get("planned_r"))

    if row.get("action_for_week") != "enter_if_triggered":
        return

    for field, value in (("entry_trigger", entry), ("stop_price", stop), ("target_price", target), ("planned_r", planned)):
        if value is None:
            issues.append(Issue("error", ref, f"{field} is required and must be finite for enter_if_triggered"))
    if direction not in {"long", "short"}:
        issues.append(Issue("error", ref, "direction must be long or short for enter_if_triggered"))
    if None in {entry, stop, target, planned} or direction not in {"long", "short"}:
        return

    assert entry is not None and stop is not None and target is not None and planned is not None
    risk = entry - stop if direction == "long" else stop - entry
    reward = target - entry if direction == "long" else entry - target
    if risk <= 0:
        issues.append(Issue("error", ref, "stop is on the wrong side of the entry trigger"))
        return
    if reward <= 0:
        issues.append(Issue("error", ref, "target is on the wrong side of the entry trigger"))
        return
    calculated = reward / risk
    if planned < minimum_r:
        issues.append(Issue("error", ref, f"planned_r {planned:.2f} is below {minimum_r:.2f}"))
    if abs(calculated - planned) > 0.05:
        issues.append(Issue("error", ref, f"planned_r {planned:.2f} disagrees with levels ({calculated:.2f})"))


def validate_registry(rows: list[dict[str, str]], issues: list[Issue], minimum_r: float) -> dict[str, dict[str, str]]:
    by_id: dict[str, dict[str, str]] = {}
    for line, row in enumerate(rows, start=2):
        ref = f"data/recommendations.csv:{line}"
        recommendation_id = row.get("recommendation_id", "").strip()
        ticker = row.get("ticker", "").strip().upper()
        status = row.get("status", "").strip()
        action = row.get("action_for_week", "").strip()

        if not recommendation_id or recommendation_id in by_id:
            issues.append(Issue("error", ref, "recommendation_id is blank or duplicated"))
        else:
            by_id[recommendation_id] = row
        if not ticker:
            issues.append(Issue("error", ref, "ticker is required"))
        if status not in STATUSES:
            issues.append(Issue("error", ref, f"unknown status {status!r}"))
        if action not in ACTIONS:
            issues.append(Issue("error", ref, f"unknown action_for_week {action!r}"))
        if row.get("outcome_status", "").strip() not in OUTCOMES:
            issues.append(Issue("error", ref, "unknown outcome_status"))
        if not row.get("source_report", "").strip():
            issues.append(Issue("error", ref, "source_report is required"))

        first_date = parse_date(row.get("first_mentioned_date"))
        reviewed_at = parse_datetime(row.get("last_reviewed_at"))
        if first_date is None:
            issues.append(Issue("error", ref, "first_mentioned_date must be ISO YYYY-MM-DD"))
        if reviewed_at is None:
            issues.append(Issue("error", ref, "last_reviewed_at must be timezone-aware ISO 8601"))
        if first_date is not None and reviewed_at is not None and first_date > reviewed_at.date():
            issues.append(Issue("error", ref, "first_mentioned_date is after last_reviewed_at"))

        for field in ("catalyst_date", "trigger_expiry", "next_review_date"):
            value = row.get(field, "").strip()
            if value and parse_date(value) is None:
                issues.append(Issue("error", ref, f"{field} must be ISO YYYY-MM-DD"))
        triggered_at = row.get("triggered_at", "").strip()
        if triggered_at and parse_datetime(triggered_at) is None:
            issues.append(Issue("error", ref, "triggered_at must be timezone-aware ISO 8601"))
        for field in ("mention_price", "reference_price", "entry_trigger", "stop_price", "target_price", "planned_r", "triggered_price"):
            value = row.get(field, "").strip()
            if value and parse_number(value) is None:
                issues.append(Issue("error", ref, f"{field} must be a finite number"))

        if status in TERMINAL_STATUSES:
            if action != "remove":
                issues.append(Issue("error", ref, "terminal recommendations must use action_for_week=remove"))
            if not row.get("removal_condition", "").strip():
                issues.append(Issue("error", ref, "terminal recommendations require removal_condition"))
        else:
            next_review = parse_date(row.get("next_review_date"))
            if next_review is None:
                issues.append(Issue("error", ref, "active recommendations require next_review_date"))
            elif reviewed_at is not None and next_review < reviewed_at.date():
                issues.append(Issue("error", ref, "next_review_date is before last_reviewed_at"))

        if action == "enter_if_triggered":
            if status != "trigger_ready":
                issues.append(Issue("error", ref, "enter_if_triggered requires status=trigger_ready"))
            for field in ("setup_type", "trigger_rule", "trigger_expiry"):
                if not row.get(field, "").strip():
                    issues.append(Issue("error", ref, f"enter_if_triggered requires {field}"))
        elif action == "manage":
            if status != "manage":
                issues.append(Issue("error", ref, "manage action requires status=manage"))
            if not row.get("linked_trade_id", "").strip():
                issues.append(Issue("error", ref, "manage action requires linked_trade_id"))
        elif action == "remove" and status not in TERMINAL_STATUSES:
            issues.append(Issue("error", ref, "remove action requires a terminal status"))
        elif action in {"wait_pullback", "monitor"} and status in {"trigger_ready", "triggered", "manage"}:
            issues.append(Issue("error", ref, f"{action} is inconsistent with status={status}"))

        validate_trade_levels(row, ref, issues, minimum_r)
    return by_id


def validate_reviews(
    rows: list[dict[str, str]],
    registry: dict[str, dict[str, str]],
    issues: list[Issue],
    minimum_r: float,
) -> dict[str, list[dict[str, str]]]:
    review_ids: set[str] = set()
    grouped: dict[str, list[dict[str, str]]] = {}
    for line, row in enumerate(rows, start=2):
        ref = f"data/recommendation_reviews.csv:{line}"
        review_id = row.get("review_id", "").strip()
        recommendation_id = row.get("recommendation_id", "").strip()
        if not review_id or review_id in review_ids:
            issues.append(Issue("error", ref, "review_id is blank or duplicated"))
        review_ids.add(review_id)
        if recommendation_id not in registry:
            issues.append(Issue("error", ref, "recommendation_id is missing from current registry"))
        grouped.setdefault(recommendation_id, []).append(row)

        if parse_datetime(row.get("reviewed_at")) is None:
            issues.append(Issue("error", ref, "reviewed_at must be timezone-aware ISO 8601"))
        if row.get("new_status", "").strip() not in STATUSES:
            issues.append(Issue("error", ref, "new_status is unknown"))
        prior = row.get("prior_status", "").strip()
        if prior and prior not in STATUSES:
            issues.append(Issue("error", ref, "prior_status is unknown"))
        if row.get("action_for_week", "").strip() not in ACTIONS:
            issues.append(Issue("error", ref, "action_for_week is unknown"))
        if not row.get("ticker", "").strip() or not row.get("source_report", "").strip():
            issues.append(Issue("error", ref, "ticker and source_report are required"))
        for field in ("trigger_expiry", "catalyst_date", "next_review_date"):
            value = row.get(field, "").strip()
            if value and parse_date(value) is None:
                issues.append(Issue("error", ref, f"{field} must be ISO YYYY-MM-DD"))
        for field in ("reference_price", "entry_trigger", "stop_price", "target_price", "planned_r"):
            value = row.get(field, "").strip()
            if value and parse_number(value) is None:
                issues.append(Issue("error", ref, f"{field} must be a finite number"))
        validate_trade_levels(
            {
                **row,
                "direction": registry.get(recommendation_id, {}).get("direction", ""),
            },
            ref,
            issues,
            minimum_r,
        )

    for recommendation_id, history in grouped.items():
        history.sort(key=lambda row: row.get("reviewed_at", ""))
        for index, row in enumerate(history):
            ref = f"data/recommendation_reviews.csv:{row.get('review_id', '?')}"
            expected_prior = "" if index == 0 else history[index - 1].get("new_status", "")
            if row.get("prior_status", "") != expected_prior:
                issues.append(
                    Issue("error", ref, f"prior_status must be {expected_prior!r} from the preceding review")
                )
        current = registry.get(recommendation_id)
        if current:
            latest = history[-1]
            comparisons = {
                "last_reviewed_at": "reviewed_at",
                "ticker": "ticker",
                "source_report": "source_report",
                "status": "new_status",
                "action_for_week": "action_for_week",
            }
            for current_field, review_field in comparisons.items():
                if current.get(current_field, "") != latest.get(review_field, ""):
                    issues.append(
                        Issue(
                            "error",
                            f"data/recommendations.csv:{recommendation_id}",
                            f"{current_field} does not match latest review {latest.get('review_id', '')}",
                        )
                    )

    for recommendation_id in registry:
        if recommendation_id not in grouped:
            issues.append(
                Issue("error", f"data/recommendations.csv:{recommendation_id}", "recommendation has no review history")
            )
    return grouped


def validate_archives(review_rows: list[dict[str, str]], issues: list[Issue]) -> None:
    master = {row.get("review_id", ""): row for row in review_rows}
    if not ARCHIVE_DIR.exists():
        return
    for path in sorted(ARCHIVE_DIR.glob("decisions-*.csv")):
        relative = str(path.relative_to(REPO_ROOT))
        if not ARCHIVE_RE.match(path.name):
            issues.append(Issue("error", relative, "unexpected decision archive filename"))
            continue
        header, rows = read_csv(path)
        if header != REVIEW_FIELDS:
            issues.append(Issue("error", relative, "archive header does not match review ledger"))
            continue
        for line, row in enumerate(rows, start=2):
            review_id = row.get("review_id", "")
            if review_id not in master:
                issues.append(Issue("error", f"{relative}:{line}", "archive row is absent from master review ledger"))
            elif row != master[review_id]:
                issues.append(Issue("error", f"{relative}:{line}", "archive row differs from master review ledger"))

        meta_path = path.with_suffix(".meta.json")
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                issues.append(Issue("error", str(meta_path.relative_to(REPO_ROOT)), "invalid JSON"))
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if meta.get("sha256") != digest:
                issues.append(Issue("error", str(meta_path.relative_to(REPO_ROOT)), "sha256 does not match archive"))
            if meta.get("row_count") != len(rows):
                issues.append(Issue("error", str(meta_path.relative_to(REPO_ROOT)), "row_count does not match archive"))


def run_validation() -> list[Issue]:
    issues: list[Issue] = []
    minimum_r = minimum_planned_r()
    registry_rows = require_header(REGISTRY_PATH, REGISTRY_FIELDS, issues)
    review_rows = require_header(REVIEWS_PATH, REVIEW_FIELDS, issues)
    registry = validate_registry(registry_rows, issues, minimum_r)
    validate_reviews(review_rows, registry, issues, minimum_r)
    validate_archives(review_rows, issues)
    return issues


def main() -> int:
    issues = run_validation()
    for issue in issues:
        print(f"{issue.level.upper()}: {issue.path}: {issue.message}")
    errors = sum(issue.level == "error" for issue in issues)
    warnings = sum(issue.level == "warning" for issue in issues)
    print(f"Recommendation validation complete: {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
