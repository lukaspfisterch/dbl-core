# session.py
#
# DblSession: Container for everything the Kernel does not know.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Set
import uuid

from kl_kernel_logic import ExecutionTrace

from .shadow_state import ShadowState


@dataclass
class DblSession:
    """
    Container for DBL execution context.
    
    The Kernel knows nothing about sessions.
    DBL uses sessions to aggregate traces, maintain state,
    and provide context for policy decisions.
    """
    
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Caller identification
    caller_id: str = ""
    caller_type: str = "user"  # user, system, tenant
    
    # Structured context
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Shadow state (DBL-internal, not visible to Kernel)
    shadow_state: ShadowState = field(default_factory=ShadowState)
    
    # Aggregated traces from Kernel executions
    traces: List[ExecutionTrace[Any]] = field(default_factory=list)
    
    # Tags for filtering and categorization
    tags: Set[str] = field(default_factory=set)
    
    def add_trace(self, trace: Any) -> None:
        """Add a trace to this session."""
        self.traces.append(trace)
    
    def append_trace(self, trace: Any) -> None:
        """Alias for add_trace."""
        self.add_trace(trace)
    
    @property
    def success(self) -> bool:
        """True if all traces succeeded."""
        return all(t.success for t in self.traces)
    
    @property
    def trace_count(self) -> int:
        return len(self.traces)

