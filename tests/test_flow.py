# tests/test_flow.py

from dbl_core.core.flow import ExecutionPlan, DblStep
from dbl_core.core.task import DblTask
from dbl_core.core.session import DblSession
from kl_kernel_logic import PsiDefinition


class DummyTask(DblTask):
    def __init__(self, name: str):
        self._name = name

    def build_psi(self, session: DblSession) -> PsiDefinition:
        return PsiDefinition(psi_type="test", name=self._name)

    def build_callable(self, session: DblSession):
        def fn():
            return f"task-{self._name}"
        return fn

    def build_kwargs(self, session: DblSession) -> dict:
        return {}

    def describe(self) -> str:
        return f"DummyTask({self._name})"


def test_dblstep_default_step_id_and_task_assignment():
    task = DummyTask("alpha")
    step = DblStep(task=task)

    assert step.step_id
    assert len(step.step_id) == 8  # uuid.hex[:8]
    assert step.task is task


def test_dblstep_respects_condition_true_and_false():
    session = DblSession()

    # no condition -> always execute
    step_no_cond = DblStep(task=DummyTask("no-cond"))
    assert step_no_cond.should_execute(session) is True

    # condition returns True
    step_true = DblStep(
        task=DummyTask("t"),
        condition=lambda s: True,
    )
    assert step_true.should_execute(session) is True

    # condition returns False
    step_false = DblStep(
        task=DummyTask("f"),
        condition=lambda s: False,
    )
    assert step_false.should_execute(session) is False


def test_execution_plan_add_step_appends_in_order():
    plan = ExecutionPlan(name="test-plan")

    t1 = DummyTask("first")
    t2 = DummyTask("second")

    s1 = plan.add_step(task=t1)
    s2 = plan.add_step(task=t2)

    assert len(plan) == 2
    assert plan.steps[0] is s1
    assert plan.steps[1] is s2
    assert plan.steps[0].task is t1
    assert plan.steps[1].task is t2


def test_execution_plan_iterates_in_order():
    plan = ExecutionPlan()

    t1 = DummyTask("one")
    t2 = DummyTask("two")

    plan.add_step(task=t1)
    plan.add_step(task=t2)

    ids = [step.task._name for step in plan]
    assert ids == ["one", "two"]
