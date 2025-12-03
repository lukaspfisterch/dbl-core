# test_shadow_state.py

from dbl_core.core.shadow_state import ShadowState, GuardMode


def test_shadow_state_defaults():
    state = ShadowState()
    assert state.risk_score == 0.0
    assert state.confidence == 1.0
    assert state.guard_mode == GuardMode.NORMAL


def test_shadow_state_partial_update():
    state = ShadowState(risk_score=0.2, confidence=0.7)
    state.update(risk_score=0.8)
    assert state.risk_score == 0.8
    assert state.confidence == 0.7


def test_shadow_state_repr():
    state = ShadowState(risk_score=0.3, confidence=0.9)
    text = repr(state)
    assert "ShadowState" in text
    assert "0.3" in text

