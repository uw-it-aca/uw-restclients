"""
This is the interface for interacting with the Notifications Web Service.
"""

from restclients.dao import NWS_DAO
from restclients.models import Subscription, Channel
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

        return self._subscriptions_from_json(json.loads(response.data))

    def get_subscriptions_by_subscriber_id(self, subscriber_id):
        """
        Search for all subscriptions by a given subscriber
        """
        url = "/notification/v1/subscription.json?subscriber_id=%s" % (subscriber_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._subscriptions_from_json(json.loads(response.data))

    def get_channel_by_channel_id(self, channel_id):
        """
        Search for all subscriptions on a given channel
        """
        url = "/notification/v1/channel/%s.json" % (channel_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        
        return self._channel_from_json(json.loads(response.data))

    def get_channels_by_surrogate_id(self, channel_type, surrogate_id):
        """
        Search for all channels by surrogate id
        """
        url = "/notification/v1/channel.json?type=%s&surrogate_id=%s" % (channel_type, surrogate_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
  
        return self._channels_from_json(json.loads(response.data))

    def get_channels_by_sln(self, channel_type, sln):
        """
        Search for all channels by sln
        """
        url = "/notification/v1/channel.json?type=%s&tag_sln=%s" % (channel_type, sln)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._channels_from_json(json.loads(response.data))

    def get_template_by_surrogate_id(self, surrogate_id):
        """
        Get a template given a specific surrogate id
        """
        url = "/notification/v1/template/%s.json" % (surrogate_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._template_from_json(response.data)

    def _subscriptions_from_json(self, data):
        """
        Returns a subscription model created from the passed json.
        """
        subscriptions = []
        for subscription_data in data['Subscriptions']:
            subscriptions.append(self._get_subscription(subscription_data))

        return subscriptions

    def _get_subscription(self, subscription_data):
        """
        Returns a subscription
        """
        subscription = Subscription()

        subscription.subscription_id = subscription_data['SubscriptionID']
        subscription.channel_id = subscription_data['ChannelID']
        subscription.end_point = subscription_data['EndPoint']
        subscription.protocol = subscription_data['Protocol']
        subscription.subscriber_id = subscription_data['SubscriberID']
        subscription.owner_id = subscription_data['OwnerID']
        subscription.clean_fields()
        
        return subscription

    def _channels_from_json(self, data):
        """
        Returns a list of channels created from the passed json.
        """
        channels = []
        for channel_data in data['Channels']:
            channels.append(self._get_channel(channel_data))
        return channels

    def _channel_from_json(self, data):
        """
        Returns a list of channels created from the passed json.
        """

        return self._get_channel(data['Channel'])

    def _get_channel(self, channel_data):
        """
        Returns a channel model
        """
        channel = Channel()
        
        channel.channel_id = channel_data['ChannelID']
        channel.surrogate_id = channel_data['SurrogateID']
        channel.type = channel_data['Type']
        channel.name = channel_data['Name']
        channel.template_surrogate_id = channel_data['TemplateSurrogateID']
        channel.description = channel_data['Description']
        channel.expires = channel_data['Expires']
        channel.last_modified = channel_data['LastModified']
        channel.clean_fields()
        return channel
        
    def _template_from_json(self, data):
        """
        Returns a template model created from the passed json.
        """
        template_data = json.loads(data)
        return template_data
