from typing import Protocol
from src.constants import POSSIBBLE_EVENTS, POSSIBBLE_DATA, POSSIBBLE_NAMES
import random


class Task:
    """
    класс описывающий минимальный набор для описания задачи
    """

    def __init__(self, task_id: int, payload: dict) -> None:
        self.id: int = task_id
        self.payload: dict = payload

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id},{self.payload})"


class TaskSource(Protocol):
    """
    Протокол, описывающий свойсва вызываемых обьектов
    """

    def get_tasks(self) -> list[Task]: ...


class JsonTaskSource:
    """
    класс, описывающий загрузку задач из json файла
    """

    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def get_tasks(self) -> list[Task]:
        raise NotImplementedError(
            "JsonTaskSource.get_tasks is not implemented yet")


class GeneratorTaskSource:
    """
    класс, описывающий генерацию задач
    """

    def __init__(self) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        return [Task(random.randint(1, 100), {"action": random.choice(POSSIBBLE_EVENTS), "name": random.choice(POSSIBBLE_NAMES), "info": random.choice(POSSIBBLE_DATA)}) for _ in range(30)]


class ApiTaskSource:
    """
    класс, имитирующий поступление задачи по api из сторонних источников
    """

    def __init__(self) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        raise NotImplementedError(
            "ApiTaskSource.get_tasks is not implemented yet")


if __name__ == '__main__':
    obj = GeneratorTaskSource()
    print(obj.get_tasks())
