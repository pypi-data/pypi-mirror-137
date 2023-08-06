from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.amount_ranges import T1AmountRanges, StrategyMaxBidRanges, StrategyMinBidRanges
from ts_t1_validator.models.enums.input_type import InputTypeEnum


class BidsRule(ValidationRule):
    def __init__(self, input_type, min_bid, max_bid):

        assert type(input_type) is InputTypeEnum, "input_type should be InputTypeEnum"

        self.input_type = input_type
        self.min_bid = min_bid
        self.max_bid = max_bid

    def execute(self):
        """
        rules:
        if both defined min <= max
        range:  0.01 - 9,999,999.99 for input type='fixed'
        range:  -99.99 to 9,999,999.99 for input type='percentage'
        """

        if self.min_bid is not None and self.max_bid is not None and self.input_type is not InputTypeEnum.PERCENTAGE:
            if self.min_bid >= self.max_bid:
                raise ValidationException("min_bid must be less than max_bid")

        T1AmountRanges(input_type=self.input_type,
                       type_ranges=StrategyMinBidRanges,
                       amount=self.min_bid,
                       amount_field="min_bid").execute()

        T1AmountRanges(input_type=self.input_type,
                       type_ranges=StrategyMaxBidRanges,
                       amount=self.max_bid,
                       amount_field="max_bid").execute()
