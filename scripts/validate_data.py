#!/usr/bin/env python3
"""Validate the journal's CSV sources of truth.

Structural corruption exits non-zero. Incomplete historical rows are warnings by
default so the validator can be introduced without pretending old gaps do not
exist. Use ``--strict`` to make warnings fail as well.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

TRADE_FIELDS = [
    "trade_id", "date_opened", "ticker", "direction", "sector", "catalyst",
    "catalyst_date", "setup_type", "thesis", "entry_price", "stop_price",
    "target_price", "position_size", "conviction", "source", "candidate_ref",
    "risk_rating", "planned_r", "status", "date_closed", "exit_price", "pnl",
    "r_multiple", "followed_plan", "lesson",
]

PROPOSAL_FIELDS = [
    "proposal_id", "date", "ticker", "direction", "source", "setup_type", "regime",
    "entry_price", "stop_price", "target_price", "planned_r", "catalyst",
    "catalyst_date", "thesis", "risk_rating", "max_holding_days",
    "exit_before_catalyst", "status", "triggered_date", "resolved_date", "exit_price",
    "sim_r", "traded", "trade_id", "notes",
]

SIGNAL_FIELDS = [
    "timestamp", "ticker", "market", "price", "change_pct", "rel_volume", "volume",
    "avg_volume_20d", "above_20d_high", "above_50d_high", "extension_5d_pct", "rsi14",
    "ema20_dist_pct", "ema50_dist_pct", "macd_hist_pct", "bb_percent_b", "score",
    "source", "reasons", "warnings", "one_day_return", "three_day_return",
    "five_day_return", "ten_day_return", "twenty_one_day_return", "notes",
]

FINVIZ_FIELDS = ["ticker", "added_at", "expires_at", "finviz_screen", "notes"]


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
    if value is None or value.strip() == "":
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def require_header(path: Path, expected: list[str], issues: list[Issue]) -> list[dict[str, str]]:
    header, rows = read_csv(path)
    if not header:
        issues.append(Issue("error", str(path.relative_to(REPO_ROOT)), "file is missing or empty"))
    elif header != expected:
        issues.append(
            Issue(
                "error",
                str(path.relative_to(REPO_ROOT)),
                f"header mismatch; expected {expected}, got {header}",
            )
        )
    return rows


def load_rules() -> dict[str, float | int]:
    path = REPO_ROOT / "config/risk.toml"
    with path.open("rb") as handle:
        return tomllib.load(handle)["learning_phase"]


def validate_trades(issues: list[Issue], rules: dict[str, float | int]) -> None:
    path = REPO_ROOT / "trades.csv"
    rows = require_header(path, TRADE_FIELDS, issues)
    ids: set[str] = set()
    allowed_status = {"open", "closed"}
    allowed_direction = {"long", "short"}

    for line, row in enumerate(rows, start=2):
        ref = f"trades.csv:{line}"
        trade_id = row.get("trade_id", "").strip()
        if not trade_id or trade_id in ids:
            issues.append(Issue("error", ref, "trade_id is blank or duplicated"))
        ids.add(trade_id)

        if row.get("direction") not in allowed_direction:
            issues.append(Issue("error", ref, "direction must be long or short"))
        if row.get("status") not in allowed_status:
            issues.append(Issue("error", ref, "status must be open or closed"))
        for field in ("date_opened", "catalyst_date", "date_closed"):
            value = row.get(field, "").strip()
            if value and not valid_date(value):
                issues.append(Issue("error", ref, f"{field} is not ISO YYYY-MM-DD"))

        for field in (
            "entry_price", "stop_price", "target_price", "position_size", "planned_r",
            "exit_price", "pnl", "r_multiple",
        ):
            value = row.get(field, "").strip()
            if value and parse_number(value) is None:
                issues.append(Issue("error", ref, f"{field} is not a finite number"))

        status = row.get("status")
        if status == "open" and (row.get("date_closed") or row.get("exit_price")):
            issues.append(Issue("error", ref, "open trade has close fields populated"))
        if status == "closed" and not row.get("date_closed"):
            issues.append(Issue("warning", ref, "closed trade is missing date_closed"))
        if status == "closed" and not row.get("exit_price"):
            issues.append(Issue("warning", ref, "closed trade is missing exit_price"))

        for field in ("stop_price", "setup_type"):
            if not row.get(field, "").strip():
                issues.append(Issue("warning", ref, f"missing {field}"))
        if status == "closed":
            for field in ("followed_plan", "lesson"):
                if not row.get(field, "").strip():
                    issues.append(Issue("warning", ref, f"missing {field}"))
        if status == "open" and not row.get("sector", "").strip():
            issues.append(Issue("warning", ref, "open trade is missing sector"))

        entry = parse_number(row.get("entry_price"))
        stop = parse_number(row.get("stop_price"))
        exit_price = parse_number(row.get("exit_price"))
        recorded_r = parse_number(row.get("r_multiple"))
        direction = row.get("direction")
        if entry is not None and stop is not None:
            risk = entry - stop if direction == "long" else stop - entry
            if risk <= 0:
                issues.append(Issue("error", ref, "stop is on the wrong side of entry"))
            elif exit_price is not None and recorded_r is not None:
                move = exit_price - entry if direction == "long" else entry - exit_price
                calculated = move / risk
                if abs(calculated - recorded_r) > 0.03:
                    issues.append(
                        Issue("error", ref, f"r_multiple {recorded_r:.2f} disagrees with prices ({calculated:.2f})")
                    )

        size = parse_number(row.get("position_size"))
        max_size = float(rules["max_position_size_eur"])
        if size is not None and size > max_size + 0.01:
            issues.append(Issue("warning", ref, f"position_size {size:.2f} exceeds {max_size:.2f}"))

        catalyst = row.get("catalyst", "").lower()
        binary = any(word in catalyst for word in ("earnings", "pdufa", "fda", "ruling", "decision"))
        cat_date = row.get("catalyst_date", "")
        close_date = row.get("date_closed", "")
        held_through = binary and cat_date and close_date and valid_date(cat_date) and valid_date(close_date) and close_date >= cat_date
        binary_cap = float(rules["binary_event_max_position_size_eur"])
        if held_through and size is not None and size > binary_cap + 0.01:
            issues.append(Issue("warning", ref, f"binary-event hold exceeded half-size cap {binary_cap:.2f}"))


def validate_proposals(issues: list[Issue], rules: dict[str, float | int]) -> None:
    path = REPO_ROOT / "data/proposals.csv"
    rows = require_header(path, PROPOSAL_FIELDS, issues)
    ids: set[str] = set()
    terminal = {"expired", "stopped", "target", "timeout", "catalyst_exit", "cancelled"}
    allowed_status = terminal | {"pending", "triggered"}
    minimum_r = float(rules["proposal_min_planned_r"])

    for line, row in enumerate(rows, start=2):
        ref = f"data/proposals.csv:{line}"
        proposal_id = row.get("proposal_id", "").strip()
        if not proposal_id or proposal_id in ids:
            issues.append(Issue("error", ref, "proposal_id is blank or duplicated"))
        ids.add(proposal_id)
        if row.get("status") not in allowed_status:
            issues.append(Issue("error", ref, "unknown proposal status"))
        for field in ("ticker", "entry_price", "stop_price", "target_price", "setup_type"):
            if not row.get(field, "").strip():
                issues.append(Issue("error", ref, f"missing required field {field}"))
        planned_r = parse_number(row.get("planned_r"))
        if planned_r is None:
            issues.append(Issue("error", ref, "planned_r is missing or invalid"))
        elif planned_r < minimum_r:
            issues.append(Issue("warning", ref, f"planned_r {planned_r:.2f} is below {minimum_r:.2f}"))
        hold_days = parse_number(row.get("max_holding_days"))
        if hold_days is not None and (hold_days < 1 or not hold_days.is_integer()):
            issues.append(Issue("error", ref, "max_holding_days must be a positive integer"))
        exit_before = row.get("exit_before_catalyst", "").strip().lower()
        if exit_before and exit_before not in {"yes", "no"}:
            issues.append(Issue("error", ref, "exit_before_catalyst must be yes or no"))


def validate_signals(issues: list[Issue]) -> None:
    for relative in ("data/scanner_signals.csv", "data/scanner_events.csv"):
        path = REPO_ROOT / relative
        if relative.endswith("events.csv") and not path.exists():
            continue
        rows = require_header(path, SIGNAL_FIELDS, issues)
        seen: set[tuple[str, str, str]] = set()
        for line, row in enumerate(rows, start=2):
            ref = f"{relative}:{line}"
            if not row.get("timestamp") or not row.get("ticker"):
                issues.append(Issue("error", ref, "timestamp and ticker are required"))
            key = (row.get("timestamp", ""), row.get("ticker", ""), row.get("market", ""))
            if relative.endswith("events.csv") and key in seen:
                issues.append(Issue("error", ref, "duplicate scanner event"))
            seen.add(key)
            score = parse_number(row.get("score"))
            if score is None or score < 0:
                issues.append(Issue("error", ref, "score must be non-negative"))


def validate_finviz(issues: list[Issue]) -> None:
    path = REPO_ROOT / "data/finviz_watchlist.csv"
    rows = require_header(path, FINVIZ_FIELDS, issues)
    tickers: set[str] = set()
    for line, row in enumerate(rows, start=2):
        ref = f"data/finviz_watchlist.csv:{line}"
        ticker = row.get("ticker", "").strip().upper()
        if not ticker or ticker in tickers:
            issues.append(Issue("error", ref, "ticker is blank or duplicated"))
        tickers.add(ticker)
        for field in ("added_at", "expires_at"):
            value = row.get(field, "").strip()
            if value and not valid_date(value):
                issues.append(Issue("error", ref, f"{field} is not ISO YYYY-MM-DD"))


def run_validation() -> list[Issue]:
    issues: list[Issue] = []
    rules = load_rules()
    validate_trades(issues, rules)
    validate_proposals(issues, rules)
    validate_signals(issues)
    validate_finviz(issues)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()

    issues = run_validation()
    for issue in issues:
        print(f"{issue.level.upper()}: {issue.path}: {issue.message}")
    errors = sum(issue.level == "error" for issue in issues)
    warnings = sum(issue.level == "warning" for issue in issues)
    print(f"Validation complete: {errors} error(s), {warnings} warning(s).")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
