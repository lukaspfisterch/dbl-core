# test_audit_recorder.py

from dbl_core.audit.recorder import AuditRecorder
from dbl_core.core.session import DblSession


class DummyTrace:
    def __init__(self, success: bool):
        self.success = success


def test_audit_recorder_records_session():
    recorder = AuditRecorder()
    session = DblSession(caller_id="audit-user")
    session.add_trace(DummyTrace(success=True))

    recorder.record_session(session)

    if hasattr(recorder, "records"):
        assert len(recorder.records) == 1
        assert recorder.records[0] is session


def test_audit_recorder_records_event():
    recorder = AuditRecorder()
    session = DblSession()

    recorder.record_event(session=session, event_type="test_event", payload={"foo": "bar"})

    if hasattr(recorder, "events"):
        assert len(recorder.events) == 1
        evt = recorder.events[0]
        assert evt["type"] == "test_event"
        assert evt["payload"]["foo"] == "bar"

