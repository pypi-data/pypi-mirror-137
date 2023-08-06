from enum import Enum


class FrequencyIntervalEnum(Enum):
    HOUR = "hour"
    DAILY = "day"
    WEEKLY = "week"
    MONTH = "month"
    NOTAPPLICABLE = "not-applicable"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
