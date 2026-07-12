#!/usr/bin/env python3
"""Run the US scanner after enforcing manual-seed expiry.

This is the supported scheduled and local entry point. Finviz rows are optional
universe-expansion hints only; scanner/config.toml keeps their score weight at zero.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCANNER_DIR = Path(__file__).resolve().parent


def main() -> int:
    subprocess.run(
        [sys.executable, str(SCANNER_DIR / "expire_finviz_seeds.py")],
        check=True,
    )

    # Import only after expiry so run_scan reads the cleaned active watchlist.
    sys.path.insert(0, str(SCANNER_DIR))
    import run_scan  # noqa: PLC0415

    return run_scan.main()


if __name__ == "__main__":
    raise SystemExit(main())
