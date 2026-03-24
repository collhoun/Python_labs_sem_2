from src.tasks import Task, TextTaskSource, ApiTaskSource, GeneratorTaskSource
from contextlib import nullcontext as does_not_raise
from src.errors.numeric_error import NotBinaryError, PriorityValueError
from src.errors.string_error import InvalidStatusError
from datetime import datetime
import pytest


class TestTask:
    @pytest.mark.parametrize(
        "payload, priority, obj_payload, obj_priority,expectation",
        [
            ("some", 1, "some", 1, does_not_raise()),
            ("TAska", 9, "TAska", 9, does_not_raise()),
            ("some", 11, "some", 11, pytest.raises(PriorityValueError)),
            (1, 1, 1, 1, pytest.raises(TypeError)),
            ("some", "1", "some", "1", pytest.raises(TypeError)),
        ]
    )
    def test_task_init(self, payload, priority, obj_payload, obj_priority, expectation):
        with expectation:
            task = Task(payload, priority)
            assert task.payload == obj_payload
            assert task.priority == obj_priority

    @pytest.mark.parametrize(
        "payload, priority, expectation",
        [
            ("some", 1, does_not_raise()),
            ("TAska", 9, does_not_raise()),
            ("some", 11, pytest.raises(PriorityValueError)),
            (1, 1, pytest.raises(TypeError)),
            ("some", "1", pytest.raises(TypeError)),
        ]

    )
    def test_task_eq(self, payload, priority, expectation):
        with expectation:
            task1 = Task(payload, priority)
            task2 = Task(payload, priority)
            assert task1 == task2

    @pytest.mark.parametrize(
        "payload1, priority1, payload2, priority2, expectation",
        [
            ("some", 1, "some", 2, does_not_raise()),
            ("TAska", 9, "Taska", 9, does_not_raise()),
            ("None", 1, "some", 11, pytest.raises(PriorityValueError)),
            ("some", 11, "other", 11, pytest.raises(PriorityValueError)),
            (1, 1, 1, 1, pytest.raises(TypeError)),
        ]

    )
    def test_task_not_eq(self, payload1, priority1, payload2, priority2, expectation):
        with expectation:
            task1 = Task(payload1, priority1)
            task2 = Task(payload2, priority2)
            assert task1 != task2

    @pytest.mark.parametrize(
        "payload, priority, new_status, expectation",
        [
            ("some", 1, "выполнено", does_not_raise()),
            ("TAska", 9, "выполнено", does_not_raise()),
            ("some", 1, "other", pytest.raises(InvalidStatusError)),
            ("some", 10, "mewo", pytest.raises(InvalidStatusError)),
            ("some", 1, "почти готово", pytest.raises(InvalidStatusError)),
        ]
    )
    def test_task_change_status(self, payload, priority, new_status, expectation):
        with expectation:
            task = Task(payload, priority)
            task.status = new_status
            assert task.status == new_status

    def test_task_change_id(self):
        with pytest.raises(AttributeError):
            task = Task("test_payload", 5)
            task.id = 1

    def test_task_change_priority(self):
        with pytest.raises(AttributeError):
            task = Task("test_payload", 5)
            task.priority = 1

    def test_task_change_is_ready(self):
        task = Task("test_payload", 5)
        task.is_ready = 1
        assert task.is_ready == 1

    def test_task_change_status_not_binary(self):
        with pytest.raises(NotBinaryError):
            task = Task("test_payload", 5)
            task.is_ready = 2

    def test_task_change_created_at(self):
        with pytest.raises(AttributeError):
            task = Task("test_payload", 5)
            task.created_at = datetime.now()  # type: ignore
            assert isinstance(task.created_at, datetime)

    def test_task_repr(self):
        task = Task("test_payload", 5)
        repr_str = repr(task)
        assert "Task" in repr_str
        assert str(task.id) in repr_str
        assert "test_payload" in repr_str

    def test_task_created_at(self):
        task = Task("test_payload", 5)
        assert hasattr(task, 'created_at')
        assert isinstance(task.created_at, datetime)

    def test_task_is_ready_initialization(self):
        task = Task("test_payload", 5)
        assert task.is_ready == 0

    def test_task_id_is_positive_integer(self):
        task = Task("test_payload", 5)
        assert isinstance(task.id, int)
        assert task.id > 0


class TestTextTaskSource:
    @pytest.mark.parametrize(
        "filename, expectation",
        [
            ("tasks.txt", does_not_raise()),
            ("TASKS.TXT", does_not_raise()),
            ("tasks", pytest.raises(ValueError)),
            ("", pytest.raises(ValueError)),
            (123, pytest.raises(TypeError)),
        ]
    )
    def test_text_task_source_filename_validation(self, filename, expectation):
        with expectation:
            source = TextTaskSource(filename)
            assert source._filename == filename

    def test_text_task_source_get_tasks_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            source = TextTaskSource("nonexistent_file.txt")
            source.get_tasks()


class TestGeneratorTaskSource:
    def test_generator_task_source_init(self):
        source = GeneratorTaskSource()
        assert source is not None

    def test_generator_task_source_get_tasks(self):
        source = GeneratorTaskSource()
        tasks = list(source.get_tasks())
        assert len(tasks) == 1
        task = tasks[0]
        assert isinstance(task, Task)
        assert task.payload is not None
        assert 1 <= task.priority <= 10


class TestApiTaskSource:
    def test_api_task_source_init(self):
        source = ApiTaskSource()
        assert source is not None

    def test_api_task_source_get_tasks(self):
        source = ApiTaskSource()
        tasks = source.get_tasks()
        assert len(tasks) == 7
        assert tasks[0].payload == 'one'
        assert tasks[0].priority == 1
        assert tasks[1].payload == 'two'
        assert tasks[1].priority == 2
        assert tasks[6].payload == 'seven'
        assert tasks[6].priority == 7
