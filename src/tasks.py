from src.contracts.task import Task
from src.constants import POSSIBBLE_EVENTS, POSSIBBLE_DATA, POSSIBBLE_NAMES, SEED
from typing import Generator, Any
import random
import os
from logging import getLogger
logger = getLogger(__name__)


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
            logger.error(
                f"Имя файла {value} должно быть {type(str)}, а не {type(value)}")
            raise TypeError("Имя файла должно быть str")
        if not value:
            logger.error("Имя файла не должно быть пустым")
            raise ValueError("Имя файла не должно быть пустым")
        if not value.lower().endswith('.txt'):
            logger.error(
                f"Расширение файла должно быть с расширением .txt, а не {value}")
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
            logger.error(f"Файл {self.filename} не найден")
            raise FileNotFoundError("Файл не найден")
        with open(self._filename, 'r', encoding='utf-8') as file:
            info = file.read().split('\n')
            logger.info(f"Получены задачи из {self.__class__.__name__}")
            return [Task(i.split('.')[1], int(i.split('.')[0].strip())) for i in info if i]


class GeneratorTaskSource:
    """
    класс, описывающий генерацию задач
    """
    _rnd = random.Random(SEED)

    def __init__(self) -> None:
        pass

    def get_tasks(self) -> Generator[Task, Any, Any]:
        """
        случайным образом генерирует задачи из возможных событий

        Returns:
            list[Task]: список задач
        """
        logger.info(f"Получены задачи из {self.__class__.__name__}")
        yield Task(f"{self._rnd.choice(POSSIBBLE_EVENTS)}: {self._rnd.choice(POSSIBBLE_DATA)} by {self._rnd.choice(POSSIBBLE_NAMES)}", self._rnd.randint(1, 10))


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
        logger.info(f"Получены задачи из {self.__class__.__name__}")
        return [Task('one', 1), Task('two', 2), Task('three', 3), Task('four', 4), Task('five', 5), Task('six', 6), Task('seven', 7)]


if __name__ == '__main__':
    obj = TextTaskSource('')
    print(obj.get_tasks())
