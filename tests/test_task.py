# test_task.py

import pytest
from dbl_core.core.task import DblTask
from dbl_core.core.session import DblSession
from kl_kernel_logic import PsiDefinition


class DummyTask(DblTask):
    def build_psi(self, session: DblSession) -> PsiDefinition:
        return PsiDefinition(
            psi_type="test",
            name="dummy",
            metadata={"caller_id": session.caller_id},
        )

    def build_callable(self, session: DblSession):
        def task_fn(value: int) -> int:
            return value + 1
        return task_fn

    def build_kwargs(self, session: DblSession) -> dict:
        return {"value": 41}

    def describe(self) -> str:
        return "Dummy task for testing"


def test_dbl_task_is_abstract():
    with pytest.raises(TypeError):
        DblTask()


def test_dummy_task_builds_psi_callable_kwargs():
    session = DblSession(caller_id="tester")
    task = DummyTask()

    psi = task.build_psi(session)
    fn = task.build_callable(session)
    kwargs = task.build_kwargs(session)

    assert psi.psi_type == "test"
    assert psi.name == "dummy"
    assert psi.metadata["caller_id"] == "tester"
    assert callable(fn)
    assert kwargs == {"value": 41}
    assert fn(**kwargs) == 42


def test_dummy_task_describe():
    task = DummyTask()
    text = task.describe()
    assert "Dummy" in text

