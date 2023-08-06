from enum import Enum


class InputTypeEnum(Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
