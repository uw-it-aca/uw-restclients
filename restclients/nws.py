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
        #TODO: create models when we start tying things together with live data
        return self._subscription_from_json(response.data)

    def get_subscriptions_by_subscriber_id(self, subscriber_id):
        """
        Search for all subscriptions by a given subscriber
        """
        url = "/notification/v1/subscription.json?subscriber_id=%s" % (subscriber_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        #TODO: create models when we start tying things together with live data
        return self._subscription_from_json(response.data)

    def get_channels_by_channel_id(self, channel_id):
        """
        Search for all subscriptions on a given channel
        """
        url = "/notification/v1/channel/%s.json" % (channel_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        #TODO: create models when we start tying things together with live data
        return self._channel_from_json(response.data)

    def get_template_by_surrogate_id(self, surrogate_id):
        """
        Get a template given a specific surrogate id
        """
        url = "/notification/v1/template/%s.json" % (surrogate_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        #TODO: create models when we start tying things together with live data
        return self._template_from_json(response.data)

    def _subscription_from_json(self, data):
        """
        Returns a subscription model created from the passed json.
        """
        subscription_data = json.loads(data)
        return subscription_data

    def _channel_from_json(self, data):
        """
        Returns a channel model created from the passed json.
        """
        channel_data = json.loads(data)
        return channel_data

    def _template_from_json(self, data):
        """
        Returns a template model created from the passed json.
        """
        template_data = json.loads(data)
        return template_data
