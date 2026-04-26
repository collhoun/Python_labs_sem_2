import asyncio
from logging import getLogger
from src.contracts.task import Task
from src.custom_exceptions.queue_exceptions import PopFromEmptyQueue


logger = getLogger(__name__)

# метка для закрытия очереди
EVENT_EMPTY_QUEUE = object()


class TaskQueue:
    def __init__(self) -> None:
        self._tasks: asyncio.PriorityQueue = asyncio.PriorityQueue(
            maxsize=10_000)
        self._closed = False
        self._is_drained = False  # флаг, очередь закрыта и полностью исчерпана
        self._counter = 0
        self._close_task = None   # сслыка на фоновую задачу, чтобы её не убил сборщик мусора

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self.get()
        except PopFromEmptyQueue:
            raise StopAsyncIteration

    async def put(self, task: Task):
        """
        Добавление задачи в очередь
        Args:
            task (Task): задача

        Raises:
            TypeError: задача не экземпляр Task
            RuntimeError: очередь закрыта для новых задач
        """
        if not isinstance(task, Task):
            logger.error("Попытка добавить не Task объект в очередь")
            raise TypeError("Задача должна быть экземпляром Task")
        if self._closed:
            logger.warning("Попытка добавить задачу в закрытую очередь")
            raise RuntimeError("Очередь закрыта для новых задач")

        self._counter += 1
        await self._tasks.put((task.priority, self._counter, task))
        logger.debug(
            f"Задача {task.id} добавлена в очередь (приоритет: {task.priority})")

    async def get(self) -> Task:
        """
        Получение задачи из очереди

        Raises:
            PopFromEmptyQueue: если очередь уже исчерпана, сразу отсекаем вызов
            PopFromEmptyQueue: если очередь закрыли, и в ней нет даже маркера (например, еще не успел положиться)
            PopFromEmptyQueue: _description_

        Returns:
            Task: _description_
        """

        if self._is_drained:
            logger.debug("Попытка извлечь задачу из исчерпанной очереди")
            raise PopFromEmptyQueue("Очередь закрыта и пуста")

        if self._closed and self._tasks.empty():
            logger.debug("Очередь закрыта и пуста")
            raise PopFromEmptyQueue("Очередь закрыта и пуста")

        priority, count, task = await self._tasks.get()

        #  мы достали маркер закрытия
        if task is EVENT_EMPTY_QUEUE:
            self._is_drained = True  # больше никому ничего не выдаем
            logger.info("Очередь полностью исчерпана")

            self._tasks.put_nowait((priority, count, task))
            raise PopFromEmptyQueue("Очередь закрыта и пуста")

        logger.debug(f"Задача {task.id} извлечена из очереди")
        return task

    def close(self):
        """
        Закрытие очереди.
        """
        if self._closed:
            logger.debug("Очередь уже закрыта")
            return

        self._closed = True
        logger.info("Очередь закрыта для новых задач")

        async def _put_empty_queue():
            await self._tasks.put((float('inf'), 0, EVENT_EMPTY_QUEUE))

        # защита от сборщика мусора
        self._close_task = asyncio.create_task(_put_empty_queue())
