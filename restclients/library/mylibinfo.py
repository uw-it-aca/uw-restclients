"""
This is the interface for interacting with the UW Libraries Web Service.
"""

from datetime import datetime
import logging
import json
from restclients.models.library import MyLibAccount
from restclients.library import get_resource


RESPONSE_STYLES = ['html', 'json']
url_prefix = "/mylibinfo/v1/?id="
logger = logging.getLogger(__name__)


def get_account(netid, timestamp=None):
    """
    The Libraries object has a method for getting information
    about a user's library account
    """
    response = _get_resource(netid, timestamp=timestamp)
    return _account_from_json(response)


def get_account_html(netid, timestamp=None):
    """
    The Libraries object has a method for getting information
    about a user's library account
    """
    return _get_resource(netid, timestamp=timestamp, style='html')


def _get_resource(netid, timestamp=None, style=None):
    """
    Return an Account object for the given netid
    """
    url = "%s%s" % (url_prefix, netid)
    if timestamp is not None:
        url += "&timestamp=" + str(timestamp)

    if style is not None:
        url += "&style=" + style
    return get_resource(url)


def _account_from_json(body):
    account_data = json.loads(body)
    account = MyLibAccount()
    account.fines = account_data["fines"]
    account.holds_ready = account_data["holds_ready"]
    account.items_loaned = account_data["items_loaned"]
    if account_data.get("next_due") is None:
        account.next_due = None
    else:
        account.next_due = datetime.strptime(account_data["next_due"],
                                             "%Y-%m-%d").date()
    return account

