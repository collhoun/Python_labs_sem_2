from typing import Protocol, Any
from src.constants import POSSIBBLE_EVENTS, POSSIBBLE_DATA, POSSIBBLE_NAMES
import random


class Task:
    """
    класс описывающий минимальный набор для описания задачи
    """

    def __init__(self, task_id: int, payload: Any) -> None:
        self.id: int = task_id
        self.payload: Any = payload

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id},{self.payload})"


class TaskSource(Protocol):
    """
    Протокол, описывающий свойсва вызываемых обьектов
    """

    def get_tasks(self) -> list[Task]: ...


class TextTaskSource:
    """
    класс, описывающий загрузку задач из json файла
    """

    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def get_tasks(self) -> list[Task]:
        with open(self.filename, 'r', encoding='utf-8') as file:
            info = file.read().split('\n')
            return [Task(int(i.split('.')[0]), i.split('.')[1].strip()) for i in info]


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
    obj = TextTaskSource('tasks_examples/task_exmaple.txt')
    print(obj.get_tasks())
