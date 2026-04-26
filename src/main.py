import asyncio
from logging import getLogger
from src.logging_config import setup_logging
from src.tasks import ApiTaskSource, GeneratorTaskSource
from src.worker import Worker
from src.iterators.task_queue import TaskQueue
from src.simulation import process


setup_logging()

logger = getLogger(__name__)


async def main():
    """
    Демонстрационный сценарий асинхронного исполнения задач
    """
    logger.info("=== Демонстрация асинхронного исполнения задач ===")

    queue = TaskQueue()
    workers = [Worker(queue) for _ in range(3)]
    logger.info(f"Создано {len(workers)} воркеров")

    api_source = ApiTaskSource()
    generator_source = GeneratorTaskSource()

    api_tasks = api_source.get_tasks()
    for task in api_tasks:
        await queue.put(task)
    logger.info(f"Добавлено {len(api_tasks)} задач из API источника")

    for task in generator_source.get_tasks():
        await queue.put(task)
    logger.info("Добавлены задачи из генератора")

    worker_tasks = [process(worker) for worker in workers]
    queue.close()

    logger.info("Запуск воркеров...")
    try:
        # собираем все корутины
        await asyncio.gather(*worker_tasks, return_exceptions=True)
    except Exception as e:
        logger.error(f"Ошибка при выполнении: {e}")
    finally:
        queue.close()
        logger.info("Очередь закрыта")

    logger.info("=== Демонстрация завершена ===")


if __name__ == '__main__':
    asyncio.run(main())
