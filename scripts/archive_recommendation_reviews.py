#!/usr/bin/env python3
"""Archive one research run's recommendation reviews without overwriting prior work."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from datetime import date, datetime, timezone
from pathlib import Path

from validate_recommendations import REPO_ROOT, REVIEW_FIELDS, REVIEWS_PATH, read_csv, run_validation

ARCHIVE_DIR = REPO_ROOT / "research/decisions"


def csv_bytes(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=REVIEW_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def choose_path(run_date: date, now: datetime) -> Path:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    base = ARCHIVE_DIR / f"decisions-{run_date.isoformat()}.csv"
    if not base.exists():
        return base
    suffixed = ARCHIVE_DIR / f"decisions-{run_date.isoformat()}-{now.strftime('%H%M')}.csv"
    if suffixed.exists():
        raise FileExistsError(f"refusing to overwrite {suffixed.relative_to(REPO_ROOT)}")
    return suffixed


def atomic_write(path: Path, content: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="review date to archive, ISO YYYY-MM-DD; defaults to today")
    args = parser.parse_args()

    run_date = date.fromisoformat(args.date) if args.date else date.today()
    issues = run_validation()
    errors = [issue for issue in issues if issue.level == "error"]
    if errors:
        for issue in errors:
            print(f"ERROR: {issue.path}: {issue.message}")
        return 1

    _, rows = read_csv(REVIEWS_PATH)
    selected = [
        row for row in rows
        if datetime.fromisoformat(row["reviewed_at"].replace("Z", "+00:00")).date() == run_date
    ]
    selected.sort(key=lambda row: (row.get("reviewed_at", ""), row.get("review_id", "")))

    now = datetime.now(timezone.utc)
    output = choose_path(run_date, now)
    content = csv_bytes(selected)
    atomic_write(output, content)

    meta = {
        "schema_version": 1,
        "generated_at": now.isoformat(),
        "review_date": run_date.isoformat(),
        "source": str(REVIEWS_PATH.relative_to(REPO_ROOT)),
        "row_count": len(selected),
        "review_ids": [row["review_id"] for row in selected],
        "sha256": hashlib.sha256(content).hexdigest(),
    }
    meta_path = output.with_suffix(".meta.json")
    atomic_write(meta_path, (json.dumps(meta, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print(
        f"Wrote {output.relative_to(REPO_ROOT)} with {len(selected)} weekly decision row(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
