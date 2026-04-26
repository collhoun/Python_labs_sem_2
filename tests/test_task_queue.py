import pytest
from src.iterators.task_queue import TaskQueue
from src.contracts.task import Task
from src.custom_exceptions.queue_exceptions import PopFromEmptyQueue


class TestTaskQueue:
    @pytest.mark.asyncio
    async def test_put_and_get_single_task(self):
        queue = TaskQueue()
        task = Task("test_payload", 1)
        await queue.put(task)
        retrieved = await queue.get()
        assert retrieved == task

    @pytest.mark.asyncio
    async def test_put_and_get_multiple_tasks(self):
        queue = TaskQueue()
        tasks = [Task(f"task{i}", i) for i in range(1, 4)]
        for task in tasks:
            await queue.put(task)
        retrieved = []
        for _ in range(3):
            retrieved.append(await queue.get())
        assert len(retrieved) == 3
        assert retrieved[0].payload == "task1"
        assert retrieved[1].payload == "task2"
        assert retrieved[2].payload == "task3"

    @pytest.mark.asyncio
    async def test_priority_order(self):
        queue = TaskQueue()
        task_low = Task("low_priority", 3)
        task_high = Task("high_priority", 1)
        task_mid = Task("mid_priority", 2)
        await queue.put(task_low)
        await queue.put(task_high)
        await queue.put(task_mid)
        first = await queue.get()
        assert first == task_high
        second = await queue.get()
        assert second == task_mid
        third = await queue.get()
        assert third == task_low

    @pytest.mark.asyncio
    async def test_close_empty_queue(self):
        queue = TaskQueue()
        queue.close()
        with pytest.raises(PopFromEmptyQueue):
            await queue.get()

    @pytest.mark.asyncio
    async def test_close_after_put(self):
        queue = TaskQueue()
        task = Task("test", 1)
        await queue.put(task)
        queue.close()
        retrieved = await queue.get()
        assert retrieved == task
        with pytest.raises(PopFromEmptyQueue):
            await queue.get()

    @pytest.mark.asyncio
    async def test_iteration_empty_queue(self):
        queue = TaskQueue()
        queue.close()
        iterated = []
        async for task in queue:
            iterated.append(task)
        assert iterated == []

    @pytest.mark.asyncio
    async def test_iteration_with_tasks(self):
        queue = TaskQueue()
        tasks = [Task(f"task{i}", i) for i in range(1, 4)]
        for task in tasks:
            await queue.put(task)
        queue.close()
        iterated = []
        async for task in queue:
            iterated.append(task)
        assert len(iterated) == 3
        assert iterated[0].priority == 1
        assert iterated[1].priority == 2
        assert iterated[2].priority == 3
        assert iterated[0].payload == "task1"
        assert iterated[1].payload == "task2"
        assert iterated[2].payload == "task3"

    @pytest.mark.asyncio
    async def test_put_after_close_raises(self):
        queue = TaskQueue()
        queue.close()
        task = Task("test", 1)
        with pytest.raises(RuntimeError):
            await queue.put(task)
