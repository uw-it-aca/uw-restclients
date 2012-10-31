"""
This is the interface for interacting with the Notifications Web Service.
"""

from restclients.dao import NWS_DAO
#from restclients.models import Subscriptions
from restclients.exceptions import DataFailureException
from urllib import urlencode
from datetime import datetime
import json
import re


class NWS(object):
    """
    The NWS object has methods for getting information
    about channels, subscriptions, and templates.
    """

    def get_subscriptions_by_channel_id(self, channel_id):
        """
        Search for all subscriptions on a given channel
        """
        url = "/notification/v1/subscription.json?channel_id=%s" % (channel_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return response.data
