from __future__ import annotations

from dbl_core import AnchorRef, BehaviorV, DblEvent, DblEventKind


def test_anchors_used_changes_event_digest() -> None:
    event_a = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={
            "decision": "ALLOW",
            "anchors_used": [AnchorRef(anchor_id="a1", anchor_type="axiom")],
        },
    )
    event_b = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={
            "decision": "ALLOW",
            "anchors_used": [AnchorRef(anchor_id="a2", anchor_type="axiom")],
        },
    )
    assert event_a.digest() != event_b.digest()


def test_observational_fields_do_not_affect_digest() -> None:
    base = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={
            "decision": "ALLOW",
            "anchors_used": [AnchorRef(anchor_id="a1", anchor_type="axiom")],
        },
        observational={"note": "one"},
    )
    modified = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={
            "decision": "ALLOW",
            "anchors_used": [AnchorRef(anchor_id="a1", anchor_type="axiom")],
        },
        observational={"note": "two"},
    )
    assert base.digest() == modified.digest()


def test_behaviorv_digest_stable_with_anchors() -> None:
    event = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={
            "decision": "ALLOW",
            "anchors_used": [AnchorRef(anchor_id="a1", anchor_type="axiom")],
        },
    )
    v1 = BehaviorV(events=(event,))
    v2 = BehaviorV(events=(event,))
    assert v1.digest() == v2.digest()
