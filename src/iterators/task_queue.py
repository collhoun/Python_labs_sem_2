from src.contracts.task import Task
from src.descriptors.numeric_descriptors import Priority
from src.descriptors.string_descriptors import StatusDescriptor
from collections import deque
from typing import Generator, Iterable
from src.custom_exceptions.queue_exceptions import PopFromEmptyQueue


class TaskQueue:
    def __init__(self, tasks: Iterable[Task] | Task) -> None:
        self._tasks = deque(self.fit(tasks))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._tasks})"

    @classmethod
    def fit(cls, tasks: Iterable[Task] | Task) -> Iterable[Task]:
        """
            Подготавливает входные данные для инициализации очереди
        Args:
            tasks (list[Task] | Task): Список задач либо единственная задача

        Returns:
            list[Task]: список задач
        """
        if isinstance(tasks, Task):
            yield tasks
            return

        for task in tasks:
            if not isinstance(task, Task):
                raise TypeError("Задача должна быть экземпляром Task")
            yield task

    def __iter__(self):
        return iter(self._tasks)

    def filter_by_priority(self, priority: int) -> Generator[Task]:
        """
        Фильтр задач по приоритету
        Args:
            priority (int): приоритет задачи

        Yields:
            Generator[Task]: задача с заданным приоритетом
        """
        Priority.verify_value(priority)
        for task in self._tasks:
            if task.priority == priority:
                yield task

    def filter_by_status(self, status: str) -> Generator[Task]:
        """
        Фильтр задач по статусу
        Args:
            status (str): статус задачи

        Yields:
            Generator[Task]: задача с заданным статусом
        """
        StatusDescriptor.verify_value(status)
        for task in self._tasks:
            if task.status == status:
                yield task

    def append(self, task: Task) -> None:
        """
        Добавляет задачу в очередь

        Args:
            task (Task): задача для добавления
        """
        if not isinstance(task, Task):
            raise TypeError("Задача должна быть экземпляром Task")
        self._tasks.append(task)

    def pop_left(self) -> Task:
        """
        Удаляет первую задачу из очереди

        Returns:
            Task: задача из очереди
        """
        if len(self._tasks) != 0:
            return self._tasks.popleft()
        raise PopFromEmptyQueue("Удаление из пустой очереди")

    def __len__(self):
        return len(self._tasks)

    def is_empty(self):
        return len(self._tasks) == 0
