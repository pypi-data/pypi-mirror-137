from enum import Enum, unique


@unique
class NotificationTypeEnum(Enum):
    CAMPAIGN = "campaign"
    ORGANIZATION = "organization"
    AGENCY = "agency"
    ADVERTISER = "advertiser"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)
