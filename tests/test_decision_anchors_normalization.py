from __future__ import annotations

import pytest

from dbl_core import DblEvent, DblEventKind
from dbl_core.events.errors import InvalidEventError


def test_anchor_order_is_normalized() -> None:
    event_a = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={
            "decision": "ALLOW",
            "anchors_used": [
                {"anchor_id": "b", "anchor_type": "maxim"},
                {"anchor_id": "a", "anchor_type": "axiom"},
            ],
        },
    )
    event_b = DblEvent(
        event_kind=DblEventKind.DECISION,
        correlation_id="c-1",
        data={
            "decision": "ALLOW",
            "anchors_used": [
                {"anchor_id": "a", "anchor_type": "axiom"},
                {"anchor_id": "b", "anchor_type": "maxim"},
            ],
        },
    )
    assert event_a.digest() == event_b.digest()


def test_duplicate_anchors_rejected() -> None:
    with pytest.raises(InvalidEventError):
        DblEvent(
            event_kind=DblEventKind.DECISION,
            correlation_id="c-1",
            data={
                "decision": "ALLOW",
                "anchors_used": [
                    {"anchor_id": "a1", "anchor_type": "axiom"},
                    {"anchor_id": "a1", "anchor_type": "axiom"},
                ],
            },
        )


def test_invalid_anchor_type_rejected() -> None:
    with pytest.raises(InvalidEventError):
        DblEvent(
            event_kind=DblEventKind.DECISION,
            correlation_id="c-1",
            data={
                "decision": "ALLOW",
                "anchors_used": [{"anchor_id": "a1", "anchor_type": "unknown"}],
            },
        )


def test_anchor_with_extra_fields_rejected() -> None:
    with pytest.raises(InvalidEventError):
        DblEvent(
            event_kind=DblEventKind.DECISION,
            correlation_id="c-1",
            data={
                "decision": "ALLOW",
                "anchors_used": [
                    {"anchor_id": "a1", "anchor_type": "axiom", "drift_bound_ppm": 10}
                ],
            },
        )
