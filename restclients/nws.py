"""
This is the interface for interacting with the Notifications Web Service.
"""

from restclients.dao import NWS_DAO
from restclients.models import Subscription, Channel
from restclients.exceptions import DataFailureException, InvalidUUID, InvalidNetID
from urllib import urlencode
from datetime import datetime
import json
import re


class NWS(object):
    """
    The NWS object has methods for getting, updating, deleting information
    about channels, subscriptions, and templates.
    """

    def delete_subscription(self, subscription_id):
        #Validate the subscription_id
        self._validate_uuid(subscription_id)

        #Delete the subscription
        url = "/notification/v1/subscription/%s" % (subscription_id)
        dao = NWS_DAO()
        delete_response = dao.deleteURL(url, None)

        #Http response code 204 No Content:
        #The server has fulfilled the request but does not need to return an entity-body
        if delete_response.status != 204:
            raise DataFailureException(url, delete_response.status, delete_response.data)

        return delete_response.status

    def update_subscription(self, subscription):
        """
        Update an existing subscription on a given channel

        :param subscription:
        is the updated subscription that the client wants to create
        """
        #Validate
        self._validate_subscriber_id(subscription.subscriber_id)
        self._validate_uuid(subscription.channel_id)

        #Update the subscription
        dao = NWS_DAO()
        url = "/notification/v1/subscription?subscriber_id=%s" % (subscription.subscriber_id)

        put_response = dao.putURL(url, {"Accept": "application/json"}, subscription.json_data())

        #Http response code 204 No Content:
        #The server has fulfilled the request but does not need to return an entity-body
        if put_response.status != 204:
            raise DataFailureException(url, put_response.status, put_response.data)

        return put_response.status

    def create_new_subscription(self, subscription):
        """
        Create a new subscription on a given channel

        :param subscription:
        is the new subscription that the client wants to create
        """
        #Validate input
        self._validate_subscriber_id(subscription.subscriber_id)
        self._validate_uuid(subscription.channel_id)

        #Create new subscription
        dao = NWS_DAO()
        url = "/notification/v1/subscription?subscriber_id=%s" % (subscription.subscriber_id)

        post_response = dao.postURL(url, {"Accept": "application/json"}, subscription.json_data())

        #HTTP Status Code 201 Created: The request has been fulfilled and resulted
        #in a new resource being created
        if post_response.status != 201:
            raise DataFailureException(url, post_response.status, post_response.data)

        return post_response.status

    def get_subscriptions_by_channel_id(self, channel_id):
        """
        Search for all subscriptions on a given channel
        """
        #Validate the channel_id
        self._validate_uuid(channel_id)

        url = "/notification/v1/subscription?channel_id=%s" % (channel_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._subscriptions_from_json(json.loads(response.data))

    def get_subscriptions_by_subscriber_id(self, subscriber_id):
        """
        Search for all subscriptions by a given subscriber
        """
        #Validate input
        self._validate_subscriber_id(subscriber_id)

        url = "/notification/v1/subscription?subscriber_id=%s" % (subscriber_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._subscriptions_from_json(json.loads(response.data))

    def get_channel_by_channel_id(self, channel_id):
        """
        Search for all subscriptions on a given channel
        """
        #Validate the channel_id
        self._validate_uuid(channel_id)

        url = "/notification/v1/channel/%s" % (channel_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._channel_from_json(json.loads(response.data))

    def get_channels_by_surrogate_id(self, channel_type, surrogate_id):
        """
        Search for all channels by surrogate id
        """
        url = "/notification/v1/channel/%s|%s" % (channel_type, surrogate_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._channel_from_json(json.loads(response.data))

    def get_channels_by_sln(self, channel_type, sln):
        """
        Search for all channels by sln
        """
        url = "/notification/v1/channel?type=%s&tag_sln=%s" % (channel_type, sln)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._channels_from_json(json.loads(response.data))

    def get_template_by_surrogate_id(self, surrogate_id):
        """
        Get a template given a specific surrogate id
        """
        url = "/notification/v1/template/%s" % (surrogate_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._template_from_json(response.data)

    def get_template_by_template_id(self, template_id):
        """
        Get a template given a specific template id
        """
        #Validate the template_id
        self._validate_uuid(template_id)

        url = "/notification/v1/template/%s" % (template_id)

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
        subscription.end_point = subscription_data['Endpoint']
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
        #channel.expires = channel_data['Expires']
        channel.last_modified = channel_data['LastModified']
        channel.clean_fields()
        return channel

    def _template_from_json(self, data):
        """
        Returns a template model created from the passed json.
        """
        template_data = json.loads(data)
        return template_data['Template']

    def _validate_uuid(self, id):
        if not re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', id):
            raise InvalidUUID(id)

    def _validate_subscriber_id(self, subscriber_id):
        if not re.match(r'^([a-z]adm_)?[a-z][a-z0-9]{0,7}$', subscriber_id, re.I):
            raise InvalidNetID(subscriber_id)
