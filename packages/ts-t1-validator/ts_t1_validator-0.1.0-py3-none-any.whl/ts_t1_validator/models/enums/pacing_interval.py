from enum import Enum


class PacingIntervalEnum(Enum):
    HOUR = "hour"
    DAY = "day"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
