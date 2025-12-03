# recorder.py
#
# AuditRecorder: Audit and logging for DBL.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.session import DblSession


@dataclass
class AuditEvent:
    """Single audit event."""
    
    timestamp: datetime
    event_type: str
    session_id: str
    payload: Dict[str, Any]


class AuditRecorder:
    """
    Default in-memory audit recorder.
    
    Subclass to implement persistent storage.
    """
    
    def __init__(self) -> None:
        self.records: List[Any] = []  # List[DblSession]
        self.events: List[Dict[str, Any]] = []
    
    def record_session(self, session: DblSession) -> None:
        """Record a complete session."""
        self.records.append(session)
    
    def record_event(
        self,
        session: DblSession,
        event_type: str,
        payload: Dict[str, Any],
    ) -> None:
        """Record a single event."""
        self.events.append({
            "timestamp": datetime.now(timezone.utc),
            "type": event_type,
            "session_id": session.run_id,
            "payload": payload,
        })
