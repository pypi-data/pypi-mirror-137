from typing import Dict

from ts_t1_validator.services.t1 import T1Service
from ts_t1_validator.validators.abstract_validator import AbstractValidator
from ts_t1_validator.validators.campaign_post_validator import CampaignPostValidator


class T1Validator:
    def __init__(self, dto: Dict, t1_creds: Dict, validator_type="campaign"):
        self.validator = None
        t1_service = T1Service(t1_creds=t1_creds)
        if validator_type == "campaign":
            self.validator = CampaignPostValidator(dto=dto, t1_service=t1_service)
        else:
            raise NotImplemented()

    def validate(self):
        """
        Proxy validate method to proper class
        :return:
        """
        return self.validator.validate()
