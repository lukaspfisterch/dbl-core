# dbl_core.py

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Sequence, Literal

from kl_kernel_logic import PsiDefinition

DecisionOutcome = Literal["allow", "modify", "block"]


@dataclass(frozen=True)
class BoundaryContext:
    """
    Input context for DBL evaluation.
    """

    psi: PsiDefinition
    caller_id: Optional[str] = None
    tenant_id: Optional[str] = None
    channel: Optional[str] = None

    metadata: Mapping[str, Any] = field(default_factory=dict)

    def describe(self) -> Dict[str, Any]:
        return {
            "psi": self.psi.describe(),
            "caller_id": self.caller_id,
            "tenant_id": self.tenant_id,
            "channel": self.channel,
            "metadata": dict(self.metadata),
        }

    def __repr__(self) -> str:
        return (
            f"BoundaryContext(psi={self.psi.name}, "
            f"caller_id={self.caller_id}, tenant_id={self.tenant_id})"
        )


@dataclass(frozen=True)
class PolicyDecision:
    """
    Result of a single policy evaluation step.
    """

    outcome: DecisionOutcome
    reason: str
    details: Mapping[str, Any] = field(default_factory=dict)

    modified_psi: Optional[PsiDefinition] = None
    modified_metadata: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class BoundaryResult:
    """
    Aggregated DBL evaluation result.
    """

    context: BoundaryContext
    decisions: Sequence[PolicyDecision]

    final_outcome: DecisionOutcome
    effective_psi: PsiDefinition
    effective_metadata: Mapping[str, Any] = field(default_factory=dict)

    def is_allowed(self) -> bool:
        return self.final_outcome in ("allow", "modify")

    def describe(self) -> Dict[str, Any]:
        return {
            "context": self.context.describe(),
            "decisions": [
                {
                    "outcome": d.outcome,
                    "reason": d.reason,
                    "details": dict(d.details),
                    "modified_psi": (
                        d.modified_psi.describe() if d.modified_psi else None
                    ),
                    "modified_metadata": (
                        dict(d.modified_metadata)
                        if d.modified_metadata is not None
                        else None
                    ),
                }
                for d in self.decisions
            ],
            "final_outcome": self.final_outcome,
            "effective_psi": self.effective_psi.describe(),
            "effective_metadata": dict(self.effective_metadata),
        }


class DBLCore:
    """
    Deterministic Boundary Layer Core.
    """

    def __init__(self, *, config: Optional[Mapping[str, Any]] = None) -> None:
        self._config: Mapping[str, Any] = dict(config) if config is not None else {}

    def describe_config(self) -> Mapping[str, Any]:
        """Return a copy of the current config for debug/audit."""
        return dict(self._config)

    def evaluate(self, context: BoundaryContext) -> BoundaryResult:
        """
        Evaluate governance and boundaries for a single operation.
        Default: allow everything.
        """

        decision = PolicyDecision(
            outcome="allow",
            reason="DBLCore default allow",
            details={
                "config_present": bool(self._config),
                "policy_chain": ["default-allow"],
            },
        )

        return BoundaryResult(
            context=context,
            decisions=[decision],
            final_outcome=decision.outcome,
            effective_psi=context.psi,
            effective_metadata=copy.deepcopy(context.metadata) if context.metadata else {},
        )

