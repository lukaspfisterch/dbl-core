# task.py
#
# DblTask: Abstract execution unit that uses Kernel internally.

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, TYPE_CHECKING

from kl_kernel_logic import PsiDefinition, ExecutionTrace

if TYPE_CHECKING:
    from .session import DblSession


class DblTask(ABC):
    """
    Abstract base for DBL tasks.
    """
    
    @abstractmethod
    def build_psi(self, session: DblSession) -> PsiDefinition:
        """Build PsiDefinition for Kernel execution."""
        ...
    
    @abstractmethod
    def build_callable(self, session: DblSession) -> Callable[..., Any]:
        """Build the callable to execute."""
        ...
    
    @abstractmethod
    def build_kwargs(self, session: DblSession) -> Dict[str, Any]:
        """Build kwargs for the callable."""
        ...
    
    @abstractmethod
    def describe(self) -> str:
        """Return a description of this task."""
        ...
    
    def postprocess(
        self,
        session: DblSession,
        trace: ExecutionTrace[Any],
    ) -> Any:
        """
        Postprocess after Kernel execution.
        Default: return trace output.
        """
        return trace.output


class LlmTask(DblTask):
    """Task for LLM API calls. Subclass and implement."""
    pass


class ToolTask(DblTask):
    """Task for tool execution. Subclass and implement."""
    pass


class HttpTask(DblTask):
    """Task for HTTP calls. Subclass and implement."""
    pass
