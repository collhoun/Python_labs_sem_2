from src.simulation import process_taks
from contextlib import nullcontext as does_not_raise
from src.tasks import TextTaskSource, ApiTaskSource, GeneratorTaskSource
import pytest


class TestSimulation:

    @pytest.mark.parametrize(
        "task_source, expectation",
        [
            (TextTaskSource("tasks_examples/task_example.txt"), does_not_raise()),
            (ApiTaskSource(), does_not_raise()),
            (GeneratorTaskSource(), does_not_raise()),
            (1, pytest.raises(TypeError)),
            ("string", pytest.raises(TypeError)),
            (None, pytest.raises(TypeError)),
        ]
    )
    def test_process_taks(self, task_source, expectation):
        with expectation:
            process_taks(task_source)
