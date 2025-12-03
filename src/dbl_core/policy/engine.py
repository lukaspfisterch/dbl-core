# engine.py
#
# PolicyEngine: Central policy hook for DBL.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from kl_kernel_logic import ExecutionTrace
    from ..core.session import DblSession
    from ..core.task import DblTask


class PolicyAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    MODIFY = "modify"
    SIMULATE = "simulate"


@dataclass
class PolicyDecision:
    """Result of a policy evaluation."""
    
    action: PolicyAction
    reason: str = ""
    modified_task: Any = None  # DblTask | None
    constraints: dict[str, Any] | None = None


class PolicyEngine:
    """
    Default policy engine that allows everything.
    
    Subclass to implement specific policy rules.
    """
    
    def before_execute(
        self,
        session: DblSession,
        task: DblTask,
    ) -> PolicyDecision:
        """
        Evaluate policy before execution.
        Default: ALLOW.
        """
        return PolicyDecision(action=PolicyAction.ALLOW)
    
    def after_execute(
        self,
        session: DblSession,
        task: DblTask,
        trace: Any,  # ExecutionTrace
    ) -> None:
        """
        Called after execution.
        Default: no-op.
        """
        pass
