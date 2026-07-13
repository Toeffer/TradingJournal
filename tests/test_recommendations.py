from scripts.validate_recommendations import validate_registry, validate_reviews


def valid_registry_row() -> dict[str, str]:
    return {
        "recommendation_id": "REC-20260713-ABC",
        "ticker": "ABC",
        "first_mentioned_date": "2026-07-13",
        "last_reviewed_at": "2026-07-13T18:00:00+00:00",
        "source_report": "research/candidates-2026-07-13.md",
        "status": "trigger_ready",
        "direction": "long",
        "setup_type": "pullback",
        "catalyst": "Post-event continuation",
        "catalyst_date": "2026-07-13",
        "mention_price": "100",
        "reference_price": "101",
        "entry_trigger": "102",
        "trigger_rule": "Close above the two-day consolidation high",
        "trigger_expiry": "2026-07-17",
        "stop_price": "98",
        "target_price": "110",
        "planned_r": "2",
        "action_for_week": "enter_if_triggered",
        "action_reason": "Event gap held and a defined consolidation formed",
        "removal_condition": "Remove if price closes below 98 before triggering",
        "next_review_date": "2026-07-20",
        "triggered_at": "",
        "triggered_price": "",
        "outcome_status": "open",
        "linked_proposal_id": "",
        "linked_trade_id": "",
        "notes": "",
    }


def valid_review_row() -> dict[str, str]:
    return {
        "review_id": "REV-20260713-ABC-01",
        "recommendation_id": "REC-20260713-ABC",
        "reviewed_at": "2026-07-13T18:00:00+00:00",
        "ticker": "ABC",
        "source_report": "research/candidates-2026-07-13.md",
        "prior_status": "",
        "new_status": "trigger_ready",
        "action_for_week": "enter_if_triggered",
        "reference_price": "101",
        "entry_trigger": "102",
        "trigger_rule": "Close above the two-day consolidation high",
        "trigger_expiry": "2026-07-17",
        "stop_price": "98",
        "target_price": "110",
        "planned_r": "2",
        "catalyst_date": "2026-07-13",
        "action_reason": "Event gap held and a defined consolidation formed",
        "removal_condition": "Remove if price closes below 98 before triggering",
        "next_review_date": "2026-07-20",
        "linked_proposal_id": "",
        "linked_trade_id": "",
        "notes": "",
    }


def test_valid_trigger_ready_recommendation_and_review() -> None:
    issues = []
    registry = validate_registry([valid_registry_row()], issues, minimum_r=1.5)
    validate_reviews([valid_review_row()], registry, issues, minimum_r=1.5)

    assert issues == []


def test_trigger_ready_requires_complete_risk_math() -> None:
    row = valid_registry_row()
    row["stop_price"] = ""
    issues = []

    validate_registry([row], issues, minimum_r=1.5)

    assert any("stop_price is required" in issue.message for issue in issues)


def test_planned_r_must_match_levels() -> None:
    row = valid_registry_row()
    row["planned_r"] = "3"
    issues = []

    validate_registry([row], issues, minimum_r=1.5)

    assert any("disagrees with levels" in issue.message for issue in issues)


def test_review_history_must_chain_statuses() -> None:
    registry_row = valid_registry_row()
    registry_row["last_reviewed_at"] = "2026-07-20T18:00:00+00:00"
    first = valid_review_row()
    second = valid_review_row()
    second.update(
        {
            "review_id": "REV-20260720-ABC-01",
            "reviewed_at": "2026-07-20T18:00:00+00:00",
            "prior_status": "carry",
        }
    )
    issues = []
    registry = validate_registry([registry_row], issues, minimum_r=1.5)

    validate_reviews([first, second], registry, issues, minimum_r=1.5)

    assert any("prior_status must be 'trigger_ready'" in issue.message for issue in issues)


def test_manage_requires_linked_trade() -> None:
    row = valid_registry_row()
    row.update(
        {
            "status": "manage",
            "action_for_week": "manage",
            "entry_trigger": "",
            "trigger_rule": "",
            "trigger_expiry": "",
            "stop_price": "",
            "target_price": "",
            "planned_r": "",
            "linked_trade_id": "",
        }
    )
    issues = []

    validate_registry([row], issues, minimum_r=1.5)

    assert any("manage action requires linked_trade_id" in issue.message for issue in issues)
