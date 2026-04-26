from typing import Protocol


class TaskHandlerable(Protocol):
    worker_id: int
    async def work(self) -> None: ...
