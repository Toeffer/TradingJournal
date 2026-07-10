import csv
from pathlib import Path

from scanner.io_utils import atomic_write_csv, atomic_write_text


def test_atomic_write_text_replaces_file(tmp_path: Path) -> None:
    path = tmp_path / "report.md"
    path.write_text("old", encoding="utf-8")
    atomic_write_text(path, "new\n")
    assert path.read_text(encoding="utf-8") == "new\n"
    assert not list(tmp_path.glob("*.tmp"))


def test_atomic_write_csv_preserves_header_order(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    atomic_write_csv(path, ["a", "b"], [{"b": "2", "a": "1"}])
    with path.open(newline="", encoding="utf-8") as handle:
        assert list(csv.reader(handle)) == [["a", "b"], ["1", "2"]]
