from logging import getLogger
from src.contracts.task_handlerable import TaskHandlerable


logger = getLogger(__name__)


async def process(worker: TaskHandlerable):
    """
    Асинхронная обработка задач с помощью воркера

    Args:
        worker (TaskHandlerable): воркер
    """
    logger.info(f"Запуск воркера {worker}")
    try:
        await worker.work()
    except Exception as e:
        logger.error(f"Ошибка в воркере {worker.worker_id}: {e}")
        raise
    logger.info(f"Воркер {worker.worker_id} завершил работу")
