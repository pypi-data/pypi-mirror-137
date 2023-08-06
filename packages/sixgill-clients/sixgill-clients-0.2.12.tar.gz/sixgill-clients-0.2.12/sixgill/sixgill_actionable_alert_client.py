from sixgill.sixgill_base_client import SixgillBaseClient
from sixgill.sixgill_request_classes.sixgill_actionable_alerts_request import SixgillActionableAlertsGetRequest
from sixgill.sixgill_request_classes.sixgill_specific_actionable_alert_request import \
    SixgillSpecificActionableAlertGetRequest
from sixgill.sixgill_request_classes.sixgill_actionable_alert_content_request import \
    SixgillActionableAlertContentGetRequest
from sixgill.sixgill_request_classes.sixgill_actionable_alert_patch_request import SixgillActionableAlertPatchRequest


class SixgillActionableAlertClient(SixgillBaseClient):

    def __init__(self, client_id, client_secret, channel_id, logger=None, session=None, verify=False,
                 num_of_attempts=5):
        super(SixgillActionableAlertClient, self).__init__(client_id=client_id, client_secret=client_secret,
                                                           channel_id=channel_id, logger=logger,
                                                           session=session, verify=verify,
                                                           num_of_attempts=num_of_attempts)

    def get_actionable_alerts_bulk(self, limit=50, offset=0, sort_by=None,
                                   sort_order=None, is_read=None, threat_level=None,
                                   threat_type=None, organization_id=None):
        return self._send_request(
            SixgillActionableAlertsGetRequest(channel_id=self.channel_id, access_token=self._get_access_token(),
                                              limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order,
                                              is_read=is_read, threat_level=threat_level, threat_type=threat_type,
                                              organization_id=organization_id))

    def get_actionable_alert(self, actionable_alert_id, organization_id=None):
        return self._send_request(
            SixgillSpecificActionableAlertGetRequest(channel_id=self.channel_id, access_token=self._get_access_token(),
                                                     actionable_alert_id=actionable_alert_id,
                                                     organization_id=organization_id))

    def get_actionable_alert_content(self, actionable_alert_id, limit=100, highlight=False, organization_id=None,
                                     aggregate_alert_id=None):
        raw_response = self._send_request(
            SixgillActionableAlertContentGetRequest(channel_id=self.channel_id, access_token=self._get_access_token(),
                                                    actionable_alert_id=actionable_alert_id, limit=limit,
                                                    highlight=highlight, organization_id=organization_id,
                                                    aggregate_alert_id=aggregate_alert_id))
        alert_content = raw_response.get('content', {"items": [], "total": 0})

        return alert_content

    def update_actionable_alert(self, actionable_alert_id, json_body, organization_id=None):
        """
        This method is used update the actionable alert by id.
        :param actionable_alert_id: actionable alert ID
        :param json_body: updated fields data in a json format
        :param organization_id: required for multi-tenant
        :return: updated actionable alert message with status code and actionable alert ID
        """
        raw_response = self._send_request(
            SixgillActionableAlertPatchRequest(channel_id=self.channel_id, access_token=self._get_access_token(),
                                               actionable_alert_id=actionable_alert_id, organization_id=organization_id,
                                               json_body=json_body))
        return raw_response
