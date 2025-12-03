# flow.py
#
# ExecutionPlan and DblStep: Higher orchestration layer above CAEL.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, List, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .task import DblTask
    from .session import DblSession


@dataclass
class DblStep:
    """
    Single step in an execution plan.
    """
    
    step_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    task: DblTask | None = None
    
    # Optional condition: (session) -> bool
    condition: Callable[[DblSession], bool] | None = None
    
    def should_execute(self, session: DblSession) -> bool:
        """Check if this step should execute."""
        if self.condition is None:
            return True
        return self.condition(session)


@dataclass
class ExecutionPlan:
    """
    Sequence of DblSteps to execute.
    """
    
    steps: List[DblStep] = field(default_factory=list)
    name: str = ""
    
    def add_step(
        self,
        task: DblTask,
        condition: Callable[[DblSession], bool] | None = None,
    ) -> DblStep:
        """Add a step to the plan."""
        step = DblStep(task=task, condition=condition)
        self.steps.append(step)
        return step
    
    def __iter__(self) -> Iterator[DblStep]:
        return iter(self.steps)
    
    def __len__(self) -> int:
        return len(self.steps)
