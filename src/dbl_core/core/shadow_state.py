# shadow_state.py
#
# ShadowState: DBL-internal adaptive state, not visible to Kernel.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict


class GuardMode(Enum):
    NORMAL = "normal"
    STRICT = "strict"
    READONLY = "readonly"


class ToolUsageMode(Enum):
    ALLOWED = "allowed"
    RESTRICTED = "restricted"
    OFF = "off"


@dataclass
class ShadowState:
    """
    DBL-internal state that adapts across Kernel calls.
    
    The Kernel never sees this. DBL uses it to control
    policy decisions, temperature caps, and guard modes.
    """
    
    risk_score: float = 0.0
    confidence: float = 1.0
    
    guard_mode: GuardMode = GuardMode.NORMAL
    tool_usage_mode: ToolUsageMode = ToolUsageMode.ALLOWED
    
    llm_temperature_cap: float | None = None
    
    # Extensible key-value store
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def update(self, **kwargs: Any) -> None:
        """Update shadow state fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.extra[key] = value

