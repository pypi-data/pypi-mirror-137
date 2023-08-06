from ts_t1_validator.models.enums.input_type import InputTypeEnum
from .abstract_rule import ValidationRule
from enum import Enum

from ..exceptions import ValidationException


class CampaignRanges(Enum):
    FIXED_MIN_VALUE = 1.00
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class CampaignImpressionRanges(Enum):
    FIXED_MIN_VALUE = 1
    FIXED_MAX_VALUE = 9999999
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyFrequencyRanges(Enum):
    FIXED_MIN_VALUE = 1
    FIXED_MAX_VALUE = 9999999
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyImpressionRanges(Enum):
    FIXED_MIN_VALUE = 1
    FIXED_MAX_VALUE = 9999999
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyGoalRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyRoiTargetRanges(Enum):
    FIXED_MIN_VALUE = 1
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyMaxBidRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyMinBidRanges(Enum):
    FIXED_MIN_VALUE = 0
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class T1AmountRanges(ValidationRule):
    def __init__(self, input_type, amount, type_ranges, amount_field):
        assert isinstance(input_type, InputTypeEnum)
        assert type(type_ranges) is Enum.__class__

        self.input_type = input_type
        self.type_ranges = type_ranges
        self.amount = amount
        self.amount_field = amount_field

    def execute(self):
        """
        rules:
            for input_type=percentage valid range is -99.99 and 9999999.99
            for input_type=fixed valid range is 0.01 and 9999999.99
        """
        if self.amount is None or self.input_type is InputTypeEnum.UNDEFINED:
            return

        if not (isinstance(self.amount, float) or self.amount is None or isinstance(self.amount, int)):
            raise ValidationException(f"{self.amount_field} must be numeric type")

        if self.input_type is InputTypeEnum.PERCENTAGE:
            if not (self.type_ranges.PERCENTAGE_MIN_VALUE.value <= self.amount <= self.type_ranges.PERCENTAGE_MAX_VALUE.value):
                raise ValidationException(
                    "value for {field_name} when input_type=percentage must be between {min_value:,.2f} and "
                    "{max_value:,.2f}".format(
                        **{
                            "field_name": self.amount_field,
                            "min_value": self.type_ranges.PERCENTAGE_MIN_VALUE.value,
                            "max_value": self.type_ranges.PERCENTAGE_MAX_VALUE.value
                        }))
        else:
            template = "value for {field_name} when input_type=fixed must be between " \
                       "{min_value:,.2f} and {max_value:,.2f}"
            if type(self.type_ranges.FIXED_MIN_VALUE.value) is int:
                template = "value for {field_name} when input_type=fixed must be between " \
                           "{min_value:,} and {max_value:,}"

            if not (self.type_ranges.FIXED_MIN_VALUE.value <= self.amount <= self.type_ranges.FIXED_MAX_VALUE.value):
                raise ValidationException(template.format(
                    **{
                        "field_name": self.amount_field,
                        "min_value": self.type_ranges.FIXED_MIN_VALUE.value,
                        "max_value": self.type_ranges.FIXED_MAX_VALUE.value
                    }))
