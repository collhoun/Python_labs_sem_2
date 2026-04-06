from src.descriptors.numeric_descriptors import PositiveInteger, Priority, BinaryInteger
from src.descriptors.string_descriptors import StatusDescriptor, StringDescriptor
from logging import getLogger
from datetime import datetime
from uuid import uuid4
logger = getLogger(__name__)


class Task:
    """
    класс описывающий минимальный набор для описания задачи
    """
    id = PositiveInteger()
    payload = StringDescriptor()
    priority = Priority()
    is_ready = BinaryInteger()
    status = StatusDescriptor()

    def __init__(self, payload: str, priority: int) -> None:
        self.id = uuid4().int
        self.payload = payload
        self.priority = priority
        self.status = "ожидание"
        self._created_at = datetime.now()
        self.is_ready = 0

        logger.info(f"Создан обьект: {self.__repr__()}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id},{self.payload})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            logger.error(
                f"Обьект типа {type(other)} не является обьектом типа {type(Task)}")
            raise TypeError(
                f"Невозможно сравнить {Task} и {type(other)}")
        return self.payload == other.payload and self.priority == other.priority

    @property
    def created_at(self) -> datetime:
        """делаем атрибут неизменяемым по договоренности"""
        return self._created_at
