from enum import Enum


class CampaignTypeEnum(Enum):
    PMP = "HAN/PMP"
    PG = "PG"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
