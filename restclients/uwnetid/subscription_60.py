"""
Interface for interacting with the UWNetID Subscription Web Service.
"""

import logging
from restclients.models.uwnetid import SubscriptionPermit, Subscription
from restclients.uwnetid.subscription import get_netid_subscriptions


logger = logging.getLogger(__name__)


def get_kerberos_subs(netid):
    """
    Return a restclients.models.uwnetid.Subscription objects
    on the given uwnetid
    """
    subs = get_netid_subscriptions(netid, Subscription.SUBS_CODE_KERBEROS)
    if subs is not None:
        for subscription in subs:
            if subscription.subscription_code == Subscription.SUBS_CODE_KERBEROS:
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

def is_current_clinician(netid):
    permits = get_kerberos_subs_permits(netid)
    if permits is None:
        return False
    for permit in permits:
        if permit.is_status_current() and\
                (permit.is_category_clinician() or\
                     permit.is_category_clinician_netid_only()):
            return True
    return False
