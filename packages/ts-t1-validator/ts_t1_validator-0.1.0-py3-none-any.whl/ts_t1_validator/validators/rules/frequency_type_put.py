from ts_t1_validator.utils import is_number
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.frequency_type import FrequencyTypeRule
from ts_t1_validator.models.enums.frequency_interval import FrequencyIntervalEnum
from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum
from ts_t1_validator.models.enums.input_type import InputTypeEnum


class FrequencyTypePutRule(ValidationRule):
    def __init__(self, frequency_optimization: bool,
                 frequency_type: FrequencyTypeEnum,
                 frequency_amount,
                 frequency_interval: FrequencyIntervalEnum,
                 input_type: InputTypeEnum):

        assert type(frequency_type) is FrequencyTypeEnum, "frequency_type should be type of FrequencyTypeEnum"
        assert type(frequency_interval) is FrequencyIntervalEnum, \
            "frequency_interval should be type of FrequencyIntervalEnum"
        assert type(input_type) is InputTypeEnum, "input_type should be type of InputTypeEnum"

        self.frequency_optimization = frequency_optimization
        self.frequency_type = frequency_type
        self.frequency_amount = frequency_amount
        self.frequency_interval = frequency_interval
        self.input_type = input_type

    def put(self, frequency_type: FrequencyTypeEnum,
            frequency_interval: FrequencyIntervalEnum,
            frequency_amount: int or float or None):
        """
        :param frequency_type: FrequencyTypeEnum
        :param frequency_interval: FrequencyIntervalEnum
        :param frequency_amount: int or float or None
        :return: self
        """

        if self.frequency_optimization:
            self.frequency_amount = frequency_amount
            self.frequency_type = frequency_type
            self.frequency_interval = frequency_interval

        if self.frequency_type is FrequencyTypeEnum.NO_LIMIT:
            self.frequency_interval = frequency_interval
            self.frequency_amount = frequency_amount

        if self.input_type is InputTypeEnum.FIXED and is_number(frequency_amount):
            self.frequency_amount = frequency_amount

        return self

    def execute(self):
        """
        rule:
        frequency_optimization, frequency_type, frequency_amount, frequency_interval
            - if undefined in DB, follow POST logic
        """

        postValidator = FrequencyTypeRule(
            frequency_optimization=self.frequency_optimization,
            frequency_type=self.frequency_type,
            frequency_amount=self.frequency_amount,
            frequency_interval=self.frequency_interval,
            input_type=self.input_type)

        return postValidator.execute()
