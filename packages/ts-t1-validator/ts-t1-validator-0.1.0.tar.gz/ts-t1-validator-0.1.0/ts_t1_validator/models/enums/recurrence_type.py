from enum import Enum


class RecurrenceTypeEnum(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
