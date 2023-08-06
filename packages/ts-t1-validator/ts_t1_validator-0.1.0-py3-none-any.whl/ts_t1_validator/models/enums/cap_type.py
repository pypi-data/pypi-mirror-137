from enum import Enum, unique


@unique
class CapTypeEnum(Enum):
    EVEN = "even"
    ASAP = "asap"
    NO_LIMIT = "no-limit"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)

    @classmethod
    def list(cls) -> str:
        return ", ".join("'{0}'".format(x.value) for x in cls if x.value is not None)
