# test_policy_engine.py

from dbl_core.policy.engine import PolicyEngine, PolicyDecision, PolicyAction
from dbl_core.core.session import DblSession
from dbl_core.core.task import DblTask
from kl_kernel_logic import PsiDefinition


class NoOpTask(DblTask):
    def build_psi(self, session: DblSession) -> PsiDefinition:
        return PsiDefinition(psi_type="test", name="noop")

    def build_callable(self, session: DblSession):
        def fn():
            return "ok"
        return fn

    def build_kwargs(self, session: DblSession) -> dict:
        return {}

    def describe(self) -> str:
        return "NoOp task"


def test_policy_engine_default_allows_execution():
    engine = PolicyEngine()
    session = DblSession(caller_id="user-1")
    task = NoOpTask()

    decision = engine.before_execute(session=session, task=task)

    assert isinstance(decision, PolicyDecision)
    assert decision.action == PolicyAction.ALLOW


def test_policy_engine_after_execute_hook_runs():
    engine = PolicyEngine()
    session = DblSession()
    task = NoOpTask()

    class DummyTrace:
        def __init__(self) -> None:
            self.success = True

    trace = DummyTrace()
    engine.after_execute(session=session, task=task, trace=trace)
    # Default implementation does nothing, but we assert no exception

