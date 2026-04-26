from logging import getLogger
from src.iterators.task_queue import TaskQueue
from src.task_handler import TaskContextHandler


logger = getLogger(__name__)


class Worker:
    worker_id: int = 0

    def __init__(self, task_queue: TaskQueue) -> None:
        self.task_queue = task_queue
        self.worker_id = Worker.worker_id
        Worker.worker_id += 1

    async def work(self) -> None:
        """
        Асинхронная обработка задач из очереди
        """
        while True:
            task = await self.task_queue.get()
            logger.info(f"Worker {self.worker_id} начал задачу {task.id}")

            async with TaskContextHandler(task):
                logger.info(
                    f"Worker {self.worker_id} обрабатывает payload: {task.payload}")

            logger.info(
                f"Worker {self.worker_id} завершил выполнение задачи {task.id} со статусом {task.status}")
