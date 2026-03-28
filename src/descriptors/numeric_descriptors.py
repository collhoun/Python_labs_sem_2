from src.errors.numeric_error import NotNaturalNumberError, PriorityValueError, NotBinaryError
from typing import Union


class PositiveInteger:
    """
    Дескриптор данных для положительных целых чисел
    """

    def __set_name__(self, owner, name) -> None:
        self.name = name

    def __get__(self, instance, owner) -> Union['PositiveInteger', int]:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value: int) -> None:
        if self.name in instance.__dict__:
            raise AttributeError(
                f"Attribute {self.name} cant be modified or changed")
        self.verify_value(value)
        instance.__dict__[self.name] = value

    @classmethod
    def verify_value(cls, value: int) -> None:
        """Проверяет корректность входного значения value

        Args:
            value (int): значение, которое пользователь хочет установить

        Raises:
            TypeError: если value не является int
            NotNaturalNumberError: если value не натуральное
        """
        if not isinstance(value, int):
            raise TypeError(f"Value should be int, not {type(value).__name__}")

        if value < 1:
            raise NotNaturalNumberError("Value should be a natural number")


class Priority(PositiveInteger):

    @classmethod
    def verify_value(cls, value: int) -> None:
        """Проверяет корректность входного значения value

        Args:
            value (int): значение, которое пользователь хочет установить

        Raises:
            TypeError: если value не является int
            PriorityValueError: если value не лежит между нулем и десятью вкл
        """
        if not isinstance(value, int):
            raise TypeError(f"Value should be int, not {type(value).__name__}")

        if value > 10 or value < 1:
            raise PriorityValueError("Priority should be between 0 and 10")


class BinaryInteger(PositiveInteger):

    def __set__(self, instance, value: int) -> None:
        self.verify_value(value)
        instance.__dict__[self.name] = value

    @classmethod
    def verify_value(cls, value: int) -> None:
        """Проверяет корректность входного значения value

        Args:
            value (int): значение, которое пользователь хочет установить

        Raises:
            TypeError: если value не является int
            NotBinaryError: если value не 0 или 1
        """
        if not isinstance(value, int):
            raise TypeError(f"Value should be int, not {type(value).__name__}")

        if not (value == 1 or value == 0):
            raise NotBinaryError("Status should be between 0 or 1")
