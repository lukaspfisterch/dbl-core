# test_gateway.py

from dbl_core.runtime.gateway import DblGateway
from dbl_core.core.session import DblSession
from dbl_core.core.flow import ExecutionPlan, DblStep
from dbl_core.core.task import DblTask
from dbl_core.policy.engine import PolicyEngine
from dbl_core.audit.recorder import AuditRecorder
from kl_kernel_logic import Kernel, PsiDefinition


class SimpleTask(DblTask):
    def __init__(self, name: str):
        self._name = name

    def build_psi(self, session: DblSession) -> PsiDefinition:
        return PsiDefinition(psi_type="test", name=self._name)

    def build_callable(self, session: DblSession):
        def fn():
            return f"step-{self._name}"
        return fn

    def build_kwargs(self, session: DblSession) -> dict:
        return {}

    def describe(self) -> str:
        return f"SimpleTask({self._name})"


def test_gateway_runs_single_step_plan():
    kernel = Kernel()
    policy = PolicyEngine()
    audit = AuditRecorder()

    gateway = DblGateway(kernel=kernel, policy_engine=policy, audit_recorder=audit)

    session = DblSession(caller_id="gw-user")
    task = SimpleTask("one")
    plan = ExecutionPlan(steps=[DblStep(step_id="s1", task=task)])

    result_session = gateway.run(plan=plan, session=session)

    assert result_session is session
    assert session.trace_count == 1
    assert session.success is True


def test_gateway_stops_on_failure_if_policy_or_task_fail():
    kernel = Kernel()
    policy = PolicyEngine()
    audit = AuditRecorder()

    gateway = DblGateway(kernel=kernel, policy_engine=policy, audit_recorder=audit)

    class FailingTask(DblTask):
        def build_psi(self, session: DblSession) -> PsiDefinition:
            return PsiDefinition(psi_type="test", name="fail")

        def build_callable(self, session: DblSession):
            def fn():
                raise RuntimeError("fail")
            return fn

        def build_kwargs(self, session: DblSession) -> dict:
            return {}

        def describe(self) -> str:
            return "FailingTask"

    ok_task = SimpleTask("ok")
    fail_task = FailingTask()

    plan = ExecutionPlan(
        steps=[
            DblStep(step_id="ok", task=ok_task),
            DblStep(step_id="fail", task=fail_task),
        ]
    )

    session = DblSession()
    result_session = gateway.run(plan=plan, session=session)

    assert result_session is session
    assert session.trace_count == 2
    assert session.success is False

