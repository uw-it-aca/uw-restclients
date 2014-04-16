"""
This is the interface for interacting with the UW Libraries Web Service.
"""

import re
import json
from restclients.dao import Libraries_DAO
from restclients.exceptions import DataFailureException
from restclients.models.libraries import Account




RESPONSE_STYLES = ['html', 'json']
INVALID_USER_MSG = "User not found"
class Account(object):
    """
    The Libraries object has a method for getting information
    about a user's library account
    """

    def get_account_html(self, netid, timestamp=None):
        return self._get_account_info(netid, timestamp=timestamp, style='html')

    def get_account(self, netid, timestamp=None):
        response = self._get_account_info(netid, timestamp=timestamp)
        return self._account_from_json(response)

    def _get_account_info(self, netid, timestamp=None, style=None):
        """
        Search for all endpoints
        """
        url = "/mylibinfo/v1/?id=%s" % netid
        if timestamp is not None:
            url += "&timestamp=" + str(timestamp)

        if style is not None:
            url += "&style=" + style


        dao = Libraries_DAO()
        response = dao.getURL(url, {})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        #'Bug' with lib API causing requests with no/invalid user to return a 200
        if INVALID_USER_MSG in response.data:
            raise DataFailureException(url, 404, response.data)

        return response.data


    def _account_from_json(self, body):
        account_data = json.loads(body)
        account = Account()
        account.fines = account_data["fines"]
        account.holds_ready = account_data["holds_ready"]
        account.items_loaned = account_data["items_loaned"]
        account.next_due = account_data["next_due"]
        return account

