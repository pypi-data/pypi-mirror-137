from enum import Enum, unique


@unique
class ImpressionPacingTypeEnum(Enum):
    EVEN = "even"
    ASAP = "asap"
    NO_LIMIT = "no-limit"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
