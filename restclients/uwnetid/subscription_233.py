"""
Interface for interacting with the UWNetID Subscription Web Service.
"""

import logging
from restclients.models.uwnetid import SubscriptionPermit, Subscription
from restclients.uwnetid.subscription import get_netid_subscriptions


u_office365edu_prod_subs_code = 233
u_office365edu_test_subs_code = 234
logger = logging.getLogger(__name__)


def get_office365edu_prod_subs(netid):
    """
    Return a restclients.models.uwnetid.Subscription objects
    on the given uwnetid
    """
    subs = get_netid_subscriptions(netid,
                                   u_office365edu_prod_subs_code)
    if subs is not None:
        for subscription in subs:
            if subscription.subscription_code == u_office365edu_prod_subs_code:
                return subscription
    return None


def get_office365edu_test_subs(netid):
    """
    Return a restclients.models.uwnetid.Subscription objects
    on the given uwnetid
    """
    subs = get_netid_subscriptions(netid,
                                   u_office365edu_test_subs_code)
    if subs is not None:
        for subscription in subs:
            if subscription.subscription_code == u_office365edu_test_subs_code:
                return subscription
    return None
