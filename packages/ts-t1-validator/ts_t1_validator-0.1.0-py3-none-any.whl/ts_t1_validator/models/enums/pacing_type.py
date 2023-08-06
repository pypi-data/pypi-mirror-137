from enum import Enum, unique


@unique
class PacingTypeEnum(Enum):
    EVEN = "even"
    ASAP = "asap"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
