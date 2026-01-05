from __future__ import annotations

import pytest

from dbl_core import AnchorRef, DblEvent, DblEventKind
from dbl_core.events.errors import InvalidEventError


def _decision(data):
    return DblEvent(event_kind=DblEventKind.DECISION, correlation_id="c-1", data=data)


def test_anchors_used_changes_digest() -> None:
    event_a = _decision(
        {
            "decision": "ALLOW",
            "anchors_used": [AnchorRef(anchor_id="a1", anchor_type="axiom")],
        }
    )
    event_b = _decision(
        {
            "decision": "ALLOW",
            "anchors_used": [AnchorRef(anchor_id="a2", anchor_type="axiom")],
        }
    )
    assert event_a.digest() != event_b.digest()


def test_anchors_used_order_is_normalized() -> None:
    event_a = _decision(
        {
            "decision": "ALLOW",
            "anchors_used": [
                {"anchor_id": "b", "anchor_type": "maxim"},
                {"anchor_id": "a", "anchor_type": "axiom"},
            ],
        }
    )
    event_b = _decision(
        {
            "decision": "ALLOW",
            "anchors_used": [
                {"anchor_id": "a", "anchor_type": "axiom"},
                {"anchor_id": "b", "anchor_type": "maxim"},
            ],
        }
    )
    assert event_a.digest() == event_b.digest()


def test_invalid_anchor_type_raises() -> None:
    with pytest.raises(InvalidEventError):
        _decision(
            {
                "decision": "ALLOW",
                "anchors_used": [{"anchor_id": "a1", "anchor_type": "unknown"}],
            }
        )


def test_duplicate_anchor_rejected() -> None:
    with pytest.raises(InvalidEventError):
        _decision(
            {
                "decision": "ALLOW",
                "anchors_used": [
                    {"anchor_id": "a1", "anchor_type": "axiom"},
                    {"anchor_id": "a1", "anchor_type": "axiom"},
                ],
            }
        )
