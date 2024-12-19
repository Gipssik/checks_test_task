from enum import Enum, EnumMeta, auto
from typing import Any


class EnumDirectValueMeta(EnumMeta):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value
        return value


class AutoEnum(str, Enum, metaclass=EnumDirectValueMeta):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name


class PaymentType(str, Enum):
    CASH = "CASH"
    CASHLESS = "CASHLESS"


class ErrorMessages(AutoEnum):
    USER_NOT_AUTHORIZED = auto()
    INVALID_CREDENTIALS = auto()
    USER_ALREADY_EXISTS = auto()
    CHECK_AMOUNT_EXCEEDED = auto()
    CHECK_DOES_NOT_EXIST = auto()
