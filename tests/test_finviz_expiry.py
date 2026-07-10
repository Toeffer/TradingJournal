from datetime import date
from pathlib import Path

from scanner import expire_finviz_seeds


def test_explicitly_expired_seed_is_archived(tmp_path: Path, monkeypatch) -> None:
    active_file = tmp_path / "finviz_watchlist.csv"
    active_file.write_text(
        "ticker,added_at,expires_at,finviz_screen,notes\n"
        "OLD,2026-01-01,2026-01-03,screen,old seed\n"
        "NEW,2026-01-04,2026-01-10,screen,new seed\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(expire_finviz_seeds, "ACTIVE", active_file)

    active, expired = expire_finviz_seeds.expire_rows(date(2026, 1, 5), 2)

    assert [row["ticker"] for row in active] == ["NEW"]
    assert [row["ticker"] for row in expired] == ["OLD"]
