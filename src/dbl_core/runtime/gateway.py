# gateway.py
#
# DblGateway: Sync orchestrator for DBL execution.

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from kl_kernel_logic import Kernel

from ..core.session import DblSession
from ..core.flow import ExecutionPlan
from ..policy.engine import PolicyEngine, PolicyAction
from ..audit.recorder import AuditRecorder

if TYPE_CHECKING:
    from ..core.task import DblTask


class DblGateway:
    """
    Sync orchestrator for DBL.
    
    Executes plans via Kernel, applies policy, updates session.
    """
    
    def __init__(
        self,
        kernel: Kernel,
        policy_engine: PolicyEngine | None = None,
        audit_recorder: AuditRecorder | None = None,
    ) -> None:
        self._kernel = kernel
        self._policy = policy_engine or PolicyEngine()
        self._audit = audit_recorder
    
    def run(
        self,
        plan: ExecutionPlan,
        session: DblSession,
    ) -> DblSession:
        """
        Execute a plan within a session.
        
        Returns the session with updated traces.
        """
        for step in plan:
            if step.task is None:
                continue
            
            # Check condition
            if not step.should_execute(session):
                continue
            
            # Policy check
            decision = self._policy.before_execute(session, step.task)
            
            if decision.action == PolicyAction.DENY:
                continue
            
            task = decision.modified_task or step.task
            
            # Build execution parameters
            psi = task.build_psi(session)
            callable_ = task.build_callable(session)
            kwargs = task.build_kwargs(session)
            
            # Execute via Kernel
            trace = self._kernel.execute(psi=psi, task=callable_, **kwargs)
            
            # Update session
            session.add_trace(trace)
            
            # Policy after
            self._policy.after_execute(session, task, trace)
            
            # Stop on failure
            if not trace.success:
                break
        
        # Audit
        if self._audit:
            self._audit.record_session(session)
        
        return session
