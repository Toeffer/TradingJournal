#!/usr/bin/env python3
"""Remove stale manual Finviz seeds from the active scoring input.

Expired rows are preserved in data/finviz_watchlist_archive.csv. This prevents a
one-day screenshot from adding score indefinitely while keeping an audit trail.
"""

from __future__ import annotations

import argparse
import csv
import tomllib
from datetime import date, timedelta
from pathlib import Path

from io_utils import atomic_write_csv

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE = REPO_ROOT / "data/finviz_watchlist.csv"
ARCHIVE = REPO_ROOT / "data/finviz_watchlist_archive.csv"
CONFIG = REPO_ROOT / "scanner/config.toml"
FIELDS = ["ticker", "added_at", "expires_at", "finviz_screen", "notes"]
ARCHIVE_FIELDS = FIELDS + ["archived_at"]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def expiry_for(row: dict[str, str], max_age_days: int) -> date | None:
    explicit = (row.get("expires_at") or "").strip()
    if explicit:
        return date.fromisoformat(explicit)
    added = (row.get("added_at") or "").strip()
    if not added:
        return None
    return date.fromisoformat(added) + timedelta(days=max_age_days)


def expire_rows(as_of: date, max_age_days: int) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    active: list[dict[str, str]] = []
    expired: list[dict[str, str]] = []
    for row in read_rows(ACTIVE):
        cutoff = expiry_for(row, max_age_days)
        normalized = {field: row.get(field, "") for field in FIELDS}
        if cutoff is not None and cutoff < as_of:
            expired.append({**normalized, "archived_at": as_of.isoformat()})
        else:
            active.append(normalized)
    return active, expired


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()

    with CONFIG.open("rb") as handle:
        max_age_days = int(tomllib.load(handle)["scanner"]["finviz_seed_max_age_days"])

    active, expired = expire_rows(args.as_of, max_age_days)
    if not expired:
        print(f"No Finviz seeds expired; {len(active)} active.")
        return 0

    archive = read_rows(ARCHIVE)
    archived_keys = {
        (row.get("ticker", ""), row.get("added_at", ""), row.get("expires_at", ""))
        for row in archive
    }
    for row in expired:
        key = (row["ticker"], row["added_at"], row["expires_at"])
        if key not in archived_keys:
            archive.append(row)
            archived_keys.add(key)

    atomic_write_csv(ACTIVE, FIELDS, active)
    atomic_write_csv(ARCHIVE, ARCHIVE_FIELDS, archive)
    print(f"Archived {len(expired)} expired Finviz seed(s); {len(active)} remain active.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
