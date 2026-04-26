from logging import getLogger
from src.contracts.task import Task
import asyncio


logger = getLogger(__name__)


class TaskContextHandler:
    def __init__(self, task: Task) -> None:
        self.task = task

    async def __aenter__(self):
        self.task.status = "в работе"
        logger.debug(f"Задача {self.task.id} начата обработка")
        return self.task

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is None:
            # кастомная логика обработки задачи
            await asyncio.sleep(3)
            self.task.status = "выполнено"
            logger.info(f"Задача {self.task.id} выполнена успешно")
            return False
        else:
            # логирование ошибки
            logger.error(f"Ошибка при выполнении задачи {self.task.id}: {exc}")
            return False  # проброс исключения дальше
