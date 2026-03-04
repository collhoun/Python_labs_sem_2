from typing import Protocol, Any, runtime_checkable
from src.constants import POSSIBBLE_EVENTS, POSSIBBLE_DATA, POSSIBBLE_NAMES, SEED
import random
import os


class Task:
    """
    класс описывающий минимальный набор для описания задачи
    """

    def __init__(self, task_id: int, payload: Any) -> None:
        self.id: int = task_id
        self.payload: Any = payload

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id},{self.payload})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            raise TypeError(
                f"Невозможно сравнить {type(Task)} и {type(other)}")
        return self.id == other.id and self.payload == other.payload


@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол, описывающий свойсва вызываемых обьектов
    """

    def get_tasks(self) -> list[Task]: ...


class TextTaskSource:
    """
    класс, описывающий загрузку задач из txt файла
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        self._validate_txt_filename(value)
        self._filename = value

    @staticmethod
    def _validate_txt_filename(value: str) -> None:
        """
        функция-валидатор имени текстового файла
        Args:
            value (str): имя файла

        Raises:
            TypeError: ошибка, если имя файла не строка
            ValueError: ошибка, если имя файла пустое или расширение не .txt
            ValueError: _description_
        """
        if not isinstance(value, str):
            raise TypeError("Имя файла должно быть str")
        if not value:
            raise ValueError("Имя файла не должно быть пустым")
        if not value.lower().endswith('.txt'):
            raise ValueError("Расширение файла должно быть текстовым")

    def get_tasks(self) -> list[Task]:
        """
        из входного файла получает таски и возвращает их

        Raises:
            FileNotFoundError: ошибка, если файл не найден

        Returns:
            list[Task]: список задач
        """
        if not os.path.isfile(self.filename):
            raise FileNotFoundError("Файл не найден")
        with open(self._filename, 'r', encoding='utf-8') as file:
            info = file.read().split('\n')
            return [Task(int(i.split('.')[0]), i.split('.')[1].strip()) for i in info if i]


class GeneratorTaskSource:
    """
    класс, описывающий генерацию задач
    """
    _rnd = random.Random(SEED)

    def __init__(self) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        """
        случайным образом генерирует задачи из возможных событий

        Returns:
            list[Task]: список задач
        """
        return [Task(self._rnd.randint(1, 100), {"action": self._rnd.choice(POSSIBBLE_EVENTS), "name": self._rnd.choice(POSSIBBLE_NAMES), "info": self._rnd.choice(POSSIBBLE_DATA)}) for _ in range(10)]


class ApiTaskSource:
    """
    класс, имитирующий поступление задачи по api из сторонних источников
    """

    def __init__(self) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        """
        Api-заглушка

        Returns:
            list[Task]: список задач
        """
        return [Task(1, 'one'), Task(2, 'two'), Task(3, 'three'), Task(4, 'four'), Task(5, 'five'), Task(6, 'six'), Task(7, 'seven')]


if __name__ == '__main__':
    obj = ApiTaskSource()
    print(obj.get_tasks())
