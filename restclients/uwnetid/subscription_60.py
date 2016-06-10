"""
Interface for interacting with the UWNetID Subscription Web Service.
"""

import logging
from restclients.models.uwnetid import SubscriptionPermit, Subscription
from restclients.uwnetid.subscription import get_netid_subscriptions


u_kerberos_subscription_code = 60
logger = logging.getLogger(__name__)


def get_kerberos_subs(netid):
    """
    Return a restclients.models.uwnetid.Subscription objects
    on the given uwnetid
    """
    subs = get_netid_subscriptions(netid, u_kerberos_subscription_code)
    if subs is not None:
        for subscription in subs:
            if subscription.subscription_code == u_kerberos_subscription_code:
                return subscription
    return None


def get_kerberos_subs_permits(netid):
    """
    Return a list of restclients.models.uwnetid.SubscriptionPermit objects
    on the given uwnetid
    """
    subs = get_kerberos_subs(netid)
    if subs is not None:
        return subs.permits
    return None


def is_current_staff(netid):
    permits = get_kerberos_subs_permits(netid)
    if permits is None:
        return False
    for permit in permits:
        if permit.is_category_staff() and permit.is_status_current():
            return True
    return False


def is_current_faculty(netid):
    permits = get_kerberos_subs_permits(netid)
    if permits is None:
        return False
    for permit in permits:
        if permit.is_category_faculty() and permit.is_status_current():
            return True
    return False


def has_active_kerberos_subs(netid):
    """
    Return true if the kerberos subscription is active and permitted
    """
    subs = get_kerberos_subs(netid)
    if subs is None:
        return False
    return subs.is_status_active() and subs.permitted
