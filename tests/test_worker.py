import pytest
from src.worker import Worker
from src.iterators.task_queue import TaskQueue
from src.contracts.task import Task
from src.custom_exceptions.queue_exceptions import PopFromEmptyQueue


class TestWorker:
    @pytest.mark.asyncio
    async def test_worker_processes_single_task(self):
        queue = TaskQueue()
        worker = Worker(queue)
        task = Task("test_payload", 1)
        await queue.put(task)
        queue.close()
        with pytest.raises(PopFromEmptyQueue):
            await worker.work()
        assert task.status == "выполнено"

    @pytest.mark.asyncio
    async def test_worker_processes_multiple_tasks(self):
        queue = TaskQueue()
        worker = Worker(queue)
        tasks = [Task(f"task{i}", 1) for i in range(3)]
        for task in tasks:
            await queue.put(task)
        queue.close()
        with pytest.raises(PopFromEmptyQueue):
            await worker.work()
        for task in tasks:
            assert task.status == "выполнено"

    @pytest.mark.asyncio
    async def test_worker_id_increment(self):
        queue = TaskQueue()
        worker1 = Worker(queue)
        worker2 = Worker(queue)
        worker3 = Worker(queue)
        assert worker2.worker_id == worker1.worker_id + 1
        assert worker3.worker_id == worker2.worker_id + 1
