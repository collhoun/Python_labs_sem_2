from typing import Union
from src.errors.string_error import InvalidStatusError


class StringDescriptor:
    def __set_name__(self, owner, name) -> None:
        self.name = name

    def __get__(self, instance, owner) -> Union['StringDescriptor', str]:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value) -> None:
        self.verify_value(value)
        instance.__dict__[self.name] = value

    @classmethod
    def verify_value(cls, value: str) -> None:
        """
        проверяет что значение типа str
        Args:
            value (str): значение, которое верифицируется

        Raises:
            TypeError: если тип value не str
        """
        if not isinstance(value, str):
            raise TypeError(f"Value should be str not {type(value).__name__}")


class StatusDescriptor(StringDescriptor):

    POSSIBLE_STATUSES: tuple = ("ожидание", "в работе", "выполнено")

    def __get__(self, instance, owner) -> Union['StatusDescriptor', str]:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    @classmethod
    def verify_value(cls, value: str) -> None:
        """
        проверяет что значение типа str и соответствует возможным состояниям
        Args:
            value (str): значение, которое верифицируется

        Raises:
            TypeError: если тип value не str
            ValueError: если value не является одним из возможных статусов
        """
        if not isinstance(value, str):
            raise TypeError(f"Value should be str not {type(value).__name__}")
        if value not in cls.POSSIBLE_STATUSES:
            raise InvalidStatusError(
                f"Status can be: 'ожидание', 'в работе', 'выполнено', а не {value}")
