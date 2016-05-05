"""
This is the interface for interacting with the UWNetID Subscription Web Service.
"""

from datetime import datetime
import logging
import json
from restclients.models.uwnetid import UwEmailForwarding, \
    Subscription, SubscriptionAction, SubscriptionPermit
from restclients.uwnetid import get_resource, put_resource


u_forwarding_subscription = 105
logger = logging.getLogger(__name__)


def get_email_forwarding(netid):
    """
    Return a restclients.models.uwnetid.UwEmailForwarding object
    on the given uwnetid
    """
    subscriptions = get_netid_subscriptions(netid, u_forwarding_subscription)
    for subscription in subscriptions:
        if subscription.subscription_code == u_forwarding_subscription:
            return_obj = UwEmailForwarding()
            if subscription.data_value:
                return_obj.fwd = subscription.data_value
            return_obj.permitted = subscription.permitted
            return_obj.status = subscription.status_name
            return return_obj

    return None


def get_netid_subscriptions(netid, subscription_codes):
    """
    Returns a list of restclients.uwnetid.Subscription objects
    corresponding to the netid and subscription code or list provided
    """
    url = _netid_subscription_url(netid, subscription_codes)
    response = get_resource(url)
    return _json_to_subscriptions(response)


def put_netid_subscription(netid, action, subscription_code, data_field=None):
    """
    Put a subscription action for the given netid and subscription_code
    """
    url = _netid_subscription_url(netid, subscription_code)
    body = {
        'actionList': [
            {
                'action': action,
                'subscriptionCode': str(subscription_code),
                'uwNetID': netid
            }
        ]
    }

    if data_field:
        body.get('message').get('message')['dataField'] = str(data_field)

    response = put_resource(url, json.dumps(body))
    return _json_to_subscriptions(response)


def _netid_subscription_url(netid, subscription_codes):
    """
    Return UWNetId resource for provided netid and subscription
    code or code list
    """
    return "/nws/v1/uwnetid/%s/subscription/%s" % (
        netid, (','.join([str(n) for n in subscription_codes])
                if isinstance(subscription_codes, (list, tuple))
                else subscription_codes))


def _json_to_subscriptions(response_body):
    """
    Returns a list of Subscription objects
    """
    subscriptions = []
    data = json.loads(response_body)
    for subscription_data in data.get("subscriptionList", []):
        subscription = Subscription(
            uwnetid=data.get('uwNetID'),
            subscription_code=subscription_data['subscriptionCode'],
            subscription_name=subscription_data['subscriptionName'],
            permitted=subscription_data['permitted'],
            status_code=subscription_data['statusCode'],
            status_name=subscription_data['statusName'])

        if 'dataField' in subscription_data:
            subscription.data_field = subscription_data['dataField']

        if 'dataValue' in subscription_data:
            subscription.data_value = subscription_data['dataValue']

        for action_data in subscription_data.get('actions', []):
            action = SubscriptionAction(
                action=action_data)
            subscription.actions.append(action)

        for permit_data in subscription_data.get('permits', []):
            permit = SubscriptionPermit(
                mode=permit_data['mode'],
                category_code=permit_data['categoryCode'],
                category_name=permit_data['categoryName'],
                status_code=permit_data['statusCode'],
                status_name=permit_data['statusName'])

            if 'dataValue' in permit_data:
                permit.data_value=permit_data['dataValue']

            subscription.permits.append(permit)

        subscriptions.append(subscription)

    return subscriptions
