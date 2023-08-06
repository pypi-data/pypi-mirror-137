import os
from typing import Dict

from ts_t1_validator.validators.rules.amount_ranges import T1AmountRanges, CampaignRanges, StrategyFrequencyRanges
from ts_t1_validator.validators.rules.cap_required_fields import CapRequiredFieldsRule
from .abstract_validator import AbstractValidator
from .rules.cap_amount import CapAmountRule
from .rules.cap_automatic import CapAutomaticRule
from .rules.dates_overlap import DatesOverlapRule
from .rules.frequency_required_fields import FrequencyRequiredFieldsRule
from .rules.frequency_type import FrequencyTypeRule
from .rules.goal_type import GoalTypeRule
from .rules.programmatic_guaranteed_overrides import ProgrammaticGuaranteedOverridesRule
from .rules.t1_advertiser import T1AdvertiserRule
from .rules.t1_budget import T1BudgetRule
from .. import T1Service
from ..models.enums.cap_type import CapTypeEnum
from ..models.enums.frequency_interval import FrequencyIntervalEnum
from ..models.enums.frequency_type import FrequencyTypeEnum
from ..models.enums.goal_type import GoalTypeEnum
from ..models.enums.input_type import InputTypeEnum


class CampaignPostValidator(AbstractValidator):
    def __init__(self, dto: Dict, t1_service: T1Service):
        """
        campaign validation manager
        :param dto: Dict
        """
        self.rules = list()
        self.errors = list()
        self.json_schema = os.path.dirname(os.path.abspath(__file__)) + "/campaign/schema/campaign_schema.json"
        self.dto = dto
        self.t1_service = t1_service

        # init campaign parameters
        advertiser_id = dto.get("advertiser_id")
        is_programmatic_guaranteed = dto.get("is_programmatic_guaranteed")
        zone_name = dto.get("zone_name")
        start_date = dto.get("start_date")
        end_date = dto.get("end_date")
        currency_code = dto.get("currency_code")
        budget = dto.get("budget")
        goal_type = GoalTypeEnum.set(dto.get("goal_type"))
        goal_value = dto.get("goal_value")
        spend_cap_type = CapTypeEnum.set(dto.get("spend_cap_type"))
        spend_cap_automatic = dto.get("spend_cap_automatic")
        spend_cap_amount = dto.get("spend_cap_amount")
        frequency_optimization = dto.get("frequency_optimization")
        frequency_type = FrequencyTypeEnum.set(dto.get("frequency_type"))
        frequency_interval = FrequencyIntervalEnum.set(dto.get("frequency_interval"))
        frequency_amount = dto.get("frequency_amount")
        restrict_targeting_to_same_device_id = dto.get("restrict_targeting_to_same_device_id")

        # check for advertiser
        self.rules.append(T1AdvertiserRule(
            advertiser_id=advertiser_id,
            t1_service=self.t1_service))

        # start_date is later than end_date. Message "start_date must be earlier than end_date"
        # start_time is later than end_time. Message " start_time must be earlier than end_time"
        # start_date is in the past. Message "start_date must be in the future"
        # start_date & end_date should be in YYYY-MM-DDTHH:MM:SS format
        if start_date is not None and end_date is not None:
            self.rules.append(DatesOverlapRule(start_date, end_date, zone_name))

        # budget should be converted based on currency code and not be greater than 9,999,999.99.00 in USD
        if budget is not None:
            self.rules.append(T1BudgetRule(
                budget=budget,
                currency=currency_code,
                t1_service=self.t1_service))

        # goal_type should be one of ctr, vcr, viewability_rate, cpa, cpc, reach, roi, spend, vcpm
        # goal_value Must be > 0 and <= 9,999,999.9999 if goal_type in (ROI, CPA, CPC, Viewable
        # CPM, CPM Reach, CPM Spend)
        # goal_value Must be > 0 and <= 100 if goal_type in (CTR, Video Completion Rate (VCR), Viewability Rate (VR))
        if goal_type is not None:
            self.add_rule(GoalTypeRule(goal_type=goal_type,
                                       goal_value=goal_value))

        # pg campaign override values
        if is_programmatic_guaranteed:
            self.rules.append(ProgrammaticGuaranteedOverridesRule(spend_cap_automatic=spend_cap_automatic,
                                                                  spend_cap_type=spend_cap_type,
                                                                  spend_cap_amount=spend_cap_amount,
                                                                  frequency_optimization=frequency_optimization,
                                                                  frequency_type=frequency_type,
                                                                  frequency_interval=frequency_interval,
                                                                  frequency_amount=frequency_amount,
                                                                  restrict_targeting_to_same_device_id=restrict_targeting_to_same_device_id))

        # validate PMP only fields
        else:
            # if present at least one spend cap field, all other should exists as well
            self.rules.append(
                CapRequiredFieldsRule(cap_type=spend_cap_type,
                                      cap_automatic=spend_cap_automatic,
                                      cap_amount=spend_cap_amount,
                                      cap_fields={"cap_automatic": "spend_cap_automatic",
                                                  "cap_type": "spend_cap_type",
                                                  "cap_amount": "spend_cap_amount"}))

            # require spend_cap_automatic if spend_cap_type is not no-limit
            self.rules.append(CapAutomaticRule(cap_type=spend_cap_type,
                                               cap_automatic=spend_cap_automatic,
                                               cap_fields={"cap_automatic": "spend_cap_automatic",
                                                           "cap_type": "spend_cap_type"}))

            # require spend_cap_amount if spend_cap_type is not no-limit and spend_cap_automatic = 0
            self.rules.append(CapAmountRule(
                cap_type=spend_cap_type,
                cap_automatic=spend_cap_automatic,
                cap_amount=spend_cap_amount,
                cap_fields={"cap_automatic": "spend_cap_automatic",
                            "cap_type": "spend_cap_type",
                            "cap_amount": "spend_cap_amount"}))

            # spend_cap_amount should be float >= 1 and <= 9999999.99
            if spend_cap_amount is not None:
                self.rules.append(T1AmountRanges(
                    input_type=InputTypeEnum.FIXED,
                    type_ranges=CampaignRanges,
                    amount=spend_cap_amount,
                    amount_field="spend_cap_amount"))

            # verify frequency fields
            self.rules.append(FrequencyTypeRule(frequency_optimization=frequency_optimization,
                                                frequency_type=frequency_type,
                                                frequency_amount=frequency_amount,
                                                frequency_interval=frequency_interval,
                                                input_type=InputTypeEnum.FIXED))

            self.rules.append(FrequencyRequiredFieldsRule(frequency_type=frequency_type,
                                                          frequency_optimization=frequency_optimization,
                                                          frequency_interval=frequency_interval,
                                                          frequency_amount=frequency_amount,
                                                          cap_fields={
                                                              "frequency_optimization": "frequency_optimization",
                                                              "frequency_type": "frequency_type",
                                                              "frequency_amount": "frequency_amount",
                                                              "frequency_interval": "frequency_interval"}))

            # frequency_amount should be type of float >= 1 and <= 9999999
            if frequency_amount is not None:
                self.rules.append(T1AmountRanges(
                    input_type=InputTypeEnum.FIXED,
                    type_ranges=StrategyFrequencyRanges,
                    amount=frequency_amount,
                    amount_field="frequency_amount"))
