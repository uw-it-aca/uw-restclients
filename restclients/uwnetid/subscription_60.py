"""
Interface for interacting with the UWNetID Subscription Web Service.
"""

import logging
from restclients.models.uwnetid import SubscriptionPermit, Subscription
from restclients.uwnetid.subscription import get_netid_subscriptions


u_kerberos_subscription_code = 60
logger = logging.getLogger(__name__)


def _get_kerberos_subs_permits(netid):
    """
    Return a list of restclients.models.uwnetid.SubscriptionPermit objects
    on the given uwnetid
    """
    subscriptions = get_netid_subscriptions(netid,
                                            u_kerberos_subscription_code)
    for subscription in subscriptions:
        if subscription.subscription_code == u_kerberos_subscription_code:
            return subscription.permits
    return None


def is_current_staff(netid):
    permits = _get_kerberos_subs_permits(netid)
    if permits is None:
        return False
    for permit in permits:
        if permit.is_category_staff() and permit.is_status_current():
            return True
    return False


def is_current_faculty(netid):
    permits = _get_kerberos_subs_permits(netid)
    if permits is None:
        return False
    for permit in permits:
        if permit.is_category_faculty() and permit.is_status_current():
            return True
    return False
