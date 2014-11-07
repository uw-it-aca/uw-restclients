"""
This is the interface for interacting with the UWNetID Subscription Web Service.
"""

from datetime import datetime
import logging
import json
from restclients.models.uwnetid import UwEmailForwarding
from restclients.uwnetid import get_resource


url_prefix = "/nws/v1/uwnetid/"
url_suffix = "/subscription/105"
logger = logging.getLogger(__name__)


def get_email_forwarding(netid):
    """
    Return a restclients.models.uwnetid.UwEmailForwarding object
    on the given uwnetid
    """
    url = "%s%s%s" % (url_prefix, netid, url_suffix)
    response = get_resource(url)
    return _get_forwarding_from_json(response)


def _get_forwarding_from_json(response_body):
    json_data = json.loads(response_body)

    if json_data.get('subscriptionList') is not None:
        if len(json_data['subscriptionList']) > 0:
            u_forwarding = json_data['subscriptionList'][0]
            if u_forwarding.get('subscriptionCode') == 105:
                return_obj = UwEmailForwarding()
                if u_forwarding.get('dataValue'):
                    return_obj.fwd = u_forwarding['dataValue']
                return_obj.permitted = bool(u_forwarding['permitted'])
                return_obj.status = u_forwarding['statusName']
                return return_obj
    return None


