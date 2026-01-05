from __future__ import annotations

from dbl_core import DblEvent, DblEventKind, GateDecision


def test_decision_without_anchors_used_is_valid() -> None:
    event = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={"decision": "ALLOW"},
    )
    assert event.data["decision"] == "ALLOW"


def test_gate_decision_still_valid() -> None:
    event = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data=GateDecision(decision="ALLOW", reason_code="ok"),
    )
    assert event.event_kind == DblEventKind.DECISION
