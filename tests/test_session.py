# test_session.py

from dbl_core.core.session import DblSession
from dbl_core.core.shadow_state import ShadowState


class DummyTrace:
    def __init__(self, success: bool):
        self.success = success


def test_session_creation_defaults():
    session = DblSession(caller_id="test-user")
    assert session.run_id
    assert session.caller_id == "test-user"
    assert session.trace_count == 0
    assert session.success is True
    assert isinstance(session.shadow_state, ShadowState)
    assert isinstance(session.context, dict)
    assert session.context == {}


def test_session_run_id_is_unique():
    s1 = DblSession()
    s2 = DblSession()
    assert s1.run_id != s2.run_id


def test_session_add_trace_success():
    session = DblSession()
    session.add_trace(DummyTrace(success=True))
    assert session.trace_count == 1
    assert session.traces[0].success is True
    assert session.success is True


def test_session_add_trace_failure():
    session = DblSession()
    session.add_trace(DummyTrace(success=True))
    session.add_trace(DummyTrace(success=False))
    assert session.trace_count == 2
    assert session.success is False


def test_shadow_state_defaults_and_update():
    session = DblSession()
    assert session.shadow_state.risk_score == 0.0
    assert session.shadow_state.confidence == 1.0
    session.shadow_state.update(risk_score=0.5)
    assert session.shadow_state.risk_score == 0.5
    assert session.shadow_state.confidence == 1.0


def test_session_repr_contains_useful_info():
    session = DblSession(caller_id="abc")
    text = repr(session)
    assert "DblSession" in text
    assert "abc" in text
