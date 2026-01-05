import dbl_core


def test_public_api_exports():
    expected = {
        "DblEvent",
        "DblEventKind",
        "BehaviorV",
        "GateDecision",
        "normalize_trace",
        "AnchorRef",
        "AnchorType",
        "normalize_anchor_refs",
    }
    assert set(dbl_core.__all__) == expected
