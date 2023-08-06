from enum import Enum, unique


@unique
class PercentageGoalTypeEnum(Enum):
    CTR = "ctr"
    VCR = "vcr"
    VR = "viewability_rate"

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else None

    @classmethod
    def asList(cls) -> list:
        return [x.value for x in list(cls)]


@unique
class FixedGoalTypeEnum(Enum):
    CPA = "cpa"
    CPC = "cpc"
    REACH = "reach"
    ROI = "roi"
    SPEND = "spend"
    VCPM = "vcpm"

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else None

    @classmethod
    def asList(cls) -> list:
        return [x.value for x in list(cls)]


@unique
class GoalTypeEnum(Enum):
    CPA = "cpa"
    CPC = "cpc"
    REACH = "reach"
    ROI = "roi"
    SPEND = "spend"
    VCPM = "vcpm"
    CTR = "ctr"
    VCR = "vcr"
    VR = "viewability_rate"
    UNDEFINED = None

    def isFixed(self) -> bool:
        """
        check value in fixed list
        :return: bool
        """
        return self.value in FixedGoalTypeEnum.asList()

    def isPercentage(self) -> bool:
        """
        check value in percentage list
        :return: bool
        """
        return self.value in PercentageGoalTypeEnum.asList()

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)

    @classmethod
    def list(cls) -> str:
        return ", ".join("'{0}'".format(x.value) for x in cls if x.value is not None)
