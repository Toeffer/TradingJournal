from scripts.validate_data import run_validation


def test_repository_has_no_structural_data_errors() -> None:
    errors = [issue for issue in run_validation() if issue.level == "error"]
    assert errors == []
