import pytest
from src.iterators.task_queue import TaskQueue
from src.contracts.task import Task
from src.custom_exceptions.queue_exceptions import PopFromEmptyQueue


class TestTaskQueueInit:

    @pytest.mark.parametrize(
        "tasks_input",
        [
            Task("task1", 1),
            [Task("task1", 1), Task("task2", 2)],
        ]
    )
    def test_init_with_various_inputs(self, tasks_input):
        queue = TaskQueue(tasks_input)
        assert len(queue) == (1 if isinstance(
            tasks_input, Task) else len(tasks_input))

    def test_init_empty_iterable(self):
        queue = TaskQueue([])
        assert queue.is_empty()


class TestTaskQueueIteration:

    def test_iteration(self):
        tasks = [Task(f"task{i}", i) for i in range(1, 4)]
        queue = TaskQueue(tasks)
        iterated = list(queue)
        assert len(iterated) == 3
        assert all(isinstance(t, Task) for t in iterated)

    def test_reiteration(self):
        tasks = [Task(f"task{i}", i) for i in range(1, 3)]
        queue = TaskQueue(tasks)
        first_iter = list(queue)
        second_iter = list(queue)
        assert first_iter == second_iter

    def test_list(self):
        tasks = [Task("task", 1), Task("task2", 2)]
        queue = TaskQueue(tasks)
        lst = list(queue)
        assert len(lst) == 2


class TestTaskQueueFiltering:

    @pytest.mark.parametrize(
        "priorities, filter_value, expected_count",
        [
            ([1, 2, 1], 1, 2),
            ([1, 2, 3], 2, 1),
            ([1, 1, 1], 1, 3)
        ]
    )
    def test_filter_by_priority(self, priorities, filter_value, expected_count):
        tasks = [Task(f"task{i}", p) for i, p in enumerate(priorities)]
        queue = TaskQueue(tasks)
        filtered = list(queue.filter_by_priority(filter_value))
        assert len(filtered) == expected_count
        assert all(task.priority == filter_value for task in filtered)

    @pytest.mark.parametrize(
        "statuses, filter_value, expected_count",
        [
            (["ожидание", "выполнено", "ожидание"], "ожидание", 2),
            (["выполнено", "выполнено"], "выполнено", 2)
        ]
    )
    def test_filter_by_status(self, statuses, filter_value, expected_count):
        tasks = []
        for i, status in enumerate(statuses):
            task = Task(f"task{i}", i + 1)
            task.status = status
            tasks.append(task)
        queue = TaskQueue(tasks)
        filtered = list(queue.filter_by_status(filter_value))
        assert len(filtered) == expected_count
        assert all(task.status == filter_value for task in filtered)


class TestTaskQueueOperations:

    def test_append(self):
        queue = TaskQueue([])
        task = Task("new_task", 1)
        queue.append(task)
        assert len(queue) == 1
        assert list(queue)[0] == task

    def test_pop_left(self):
        tasks = [Task(f"task{i}", i) for i in range(1, 3)]
        queue = TaskQueue(tasks)
        popped = queue.pop_left()
        assert popped == tasks[0]
        assert len(queue) == 1

    def test_pop_left_empty_queue(self):
        queue = TaskQueue([])
        with pytest.raises(PopFromEmptyQueue):
            queue.pop_left()

    def test_len_and_is_empty(self):
        queue = TaskQueue([Task("task", 1)])
        assert len(queue) == 1
        assert not queue.is_empty()
        queue.pop_left()
        assert len(queue) == 0
        assert queue.is_empty()
