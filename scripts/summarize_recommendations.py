#!/usr/bin/env python3
"""Render the current rolling recommendation registry as a concise Markdown book."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

try:
    from scripts.validate_recommendations import REGISTRY_PATH, REPO_ROOT, run_validation
except ModuleNotFoundError:  # Direct execution: python scripts/summarize_recommendations.py
    from validate_recommendations import (  # type: ignore[no-redef]
        REGISTRY_PATH,
        REPO_ROOT,
        run_validation,
    )

OUTPUT = REPO_ROOT / "research/recommendation-book.md"
TERMINAL = {"invalidated", "expired", "archived"}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fmt(value: str) -> str:
    return value.strip() or "—"


def main() -> int:
    errors = [issue for issue in run_validation() if issue.level == "error"]
    if errors:
        for issue in errors:
            print(f"ERROR: {issue.path}: {issue.message}")
        return 1

    rows = load_rows(REGISTRY_PATH)
    active = [row for row in rows if row.get("status") not in TERMINAL]
    inactive = [row for row in rows if row.get("status") in TERMINAL]
    counts = Counter(row.get("action_for_week", "?") for row in active)

    lines = [
        "# Rolling Recommendation Book",
        "",
        "Auto-generated from `data/recommendations.csv`. Research decisions are not trade executions.",
        "",
        "## Current decision load",
        "",
        f"- Active recommendations: {len(active)}",
        f"- Archived/removed recommendations: {len(inactive)}",
    ]
    if counts:
        lines.append("- Actions: " + " | ".join(f"{key}: {value}" for key, value in sorted(counts.items())))
    lines.extend(["", "## Active recommendations", ""])

    if active:
        lines.extend([
            "| Ticker | Status | This week | Setup | Trigger | Expiry | Stop | Target | Next review |",
            "|---|---|---|---|---:|---|---:|---:|---|",
        ])
        for row in sorted(active, key=lambda item: (item.get("action_for_week", ""), item.get("ticker", ""))):
            lines.append(
                f"| {fmt(row.get('ticker', ''))} | {fmt(row.get('status', ''))} "
                f"| {fmt(row.get('action_for_week', ''))} | {fmt(row.get('setup_type', ''))} "
                f"| {fmt(row.get('entry_trigger', ''))} | {fmt(row.get('trigger_expiry', ''))} "
                f"| {fmt(row.get('stop_price', ''))} | {fmt(row.get('target_price', ''))} "
                f"| {fmt(row.get('next_review_date', ''))} |"
            )
        lines.extend(["", "### Decision reasons", ""])
        for row in sorted(active, key=lambda item: item.get("ticker", "")):
            lines.append(
                f"- **{row.get('ticker', '')}** — {row.get('action_for_week', '')}: "
                f"{fmt(row.get('action_reason', ''))}"
            )
    else:
        lines.append("No active recommendations. A no-new-trade week is a valid decision.")

    lines.extend(["", "## Recently removed", ""])
    if inactive:
        for row in sorted(inactive, key=lambda item: item.get("last_reviewed_at", ""), reverse=True)[:10]:
            lines.append(
                f"- **{row.get('ticker', '')}** — {row.get('status', '')}: "
                f"{fmt(row.get('removal_condition', ''))}"
            )
    else:
        lines.append("None recorded yet.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
