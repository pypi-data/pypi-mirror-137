from edc_action_item.utils import register_actions
from edc_ltfu.action_items import LtfuAction
from edc_offstudy.action_items import EndOfStudyAction as BaseEndOfStudyAction
from edc_protocol_violation.action_items import (
    ProtocolDeviationViolationAction as BaseProtocolDeviationViolationAction,
)


class EndOfStudyAction(BaseEndOfStudyAction):

    reference_model = "mocca_prn.endofstudy"
    admin_site_name = "mocca_prn_admin"


class LossToFollowupAction(LtfuAction):

    admin_site_name = "mocca_prn_admin"


class ProtocolDeviationViolationAction(BaseProtocolDeviationViolationAction):
    reference_model = "mocca_prn.protocoldeviationviolation"
    admin_site_name = "mocca_prn_admin"


register_actions(
    EndOfStudyAction,
    ProtocolDeviationViolationAction,
    LossToFollowupAction,
)
