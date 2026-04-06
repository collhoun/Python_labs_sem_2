
from typing import Protocol, runtime_checkable
from .task import Task


@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол, описывающий свойсва вызываемых обьектов
    """

    def get_tasks(self) -> list[Task] | Task: ...
