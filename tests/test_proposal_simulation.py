from scanner.simulate_proposals import simulate_row


def bar(day: str, high: float, low: float, close: float) -> dict[str, object]:
    return {"t": f"{day}T00:00:00Z", "h": high, "l": low, "c": close}


def base_row() -> dict[str, str]:
    return {
        "date": "2026-01-02",
        "direction": "long",
        "entry_price": "10",
        "stop_price": "8",
        "target_price": "15",
        "max_holding_days": "3",
        "exit_before_catalyst": "no",
        "catalyst_date": "",
        "status": "pending",
        "triggered_date": "",
        "resolved_date": "",
        "exit_price": "",
        "sim_r": "",
    }


def test_timeout_uses_explicit_holding_period() -> None:
    row = base_row()
    bars = [
        bar("2026-01-02", 10.5, 9.5, 10.1),
        bar("2026-01-05", 11.0, 9.7, 10.3),
        bar("2026-01-06", 11.2, 9.8, 10.4),
    ]

    assert simulate_row(row, bars)
    assert row["status"] == "timeout"
    assert row["resolved_date"] == "2026-01-06"
    assert row["sim_r"] == "0.20"


def test_same_bar_ambiguity_counts_as_stop() -> None:
    row = base_row()
    row["target_price"] = "11"

    assert simulate_row(row, [bar("2026-01-02", 11.5, 7.5, 10.5)])
    assert row["status"] == "stopped"
    assert row["sim_r"] == "-1.00"


def test_unresolved_trade_exits_before_catalyst() -> None:
    row = base_row()
    row["max_holding_days"] = "10"
    row["exit_before_catalyst"] = "yes"
    row["catalyst_date"] = "2026-01-06"
    bars = [
        bar("2026-01-02", 10.5, 9.5, 10.1),
        bar("2026-01-05", 11.0, 9.7, 10.6),
        bar("2026-01-06", 20.0, 5.0, 12.0),
    ]

    assert simulate_row(row, bars)
    assert row["status"] == "catalyst_exit"
    assert row["resolved_date"] == "2026-01-05"
    assert row["exit_price"] == "10.6000"
