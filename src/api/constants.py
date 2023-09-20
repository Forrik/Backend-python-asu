from enum import IntEnum

from typing import Any, Optional


class IntDescriptionEnum(IntEnum):
    descr: Optional[str]

    def __new__(
        cls, value: int, description: Optional[str] = None
    ) -> 'IntDescriptionEnum':
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.descr = description

        return obj

    @classmethod
    def _missing_(cls, _: Any) -> 'IntDescriptionEnum':
        return cls.UNKNOWN_VALUE  # type: ignore

    @classmethod
    def list(cls) -> Any:
        return list(map(lambda c: c.value, cls))  # type: ignore


class Role(IntDescriptionEnum):
    STUDENT = 1, "Студент"
    TEACHER = 2, "Учитель"
    SPECIALIST = 3, "Специалист УМР"

class TicketStatusEnum(IntDescriptionEnum):
    NEW = 1, "Новая"
    ACCEPTED = 2, "Принятая"
    REJECTED = 3, "Отклонено"