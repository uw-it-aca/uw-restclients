"""
This is the interface for interacting with the Notifications Web Service.
"""

from restclients.dao import NWS_DAO
from restclients.exceptions import DataFailureException, InvalidUUID, InvalidNetID, InvalidEndpointProtocol
from urllib import urlencode
from datetime import datetime
from vm.v1.viewmodels import Channel, ChannelList, Endpoint, EndpointList, Message, MessageList, Serializer, Subscription, SubscriptionList

import re


class NWS(object):
    """
    The NWS object has methods for getting, updating, deleting information
    about channels, subscriptions, endpoints, and templates.
    """

    #ENDPOINT RESOURCE
    def get_endpoint_by_endpoint_id(self, endpoint_id):
        """
        Get an endpoint by endpoint id
        """
        #Validate the channel_id
        self._validate_uuid(endpoint_id)

        url = "/notification/v1/endpoint/%s" % (endpoint_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        
        endpoint = Endpoint()
        Serializer().deserialize(endpoint, response.data)
        
        return endpoint
    
        #return self._endpoint_from_json(json.loads(response.data))

    def get_endpoints_by_subscriber_id(self, subscriber_id):
        """
        Search for all endpoints by a given subscriber
        """
        #Validate input
        self._validate_subscriber_id(subscriber_id)

        url = "/notification/v1/endpoint?subscriber_id=%s" % (subscriber_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        endpoint_list = EndpointList()
        Serializer().deserialize(endpoint_list, response.data)

        return endpoint_list.view_models

    def delete_endpoint(self, endpoint_id):
        """
        Deleting an existing endpoint

        :param endpoint_id:
        is the endpoint that the client wants to delete
        """

        #Validate the subscription_id
        self._validate_uuid(endpoint_id)

        #Delete the subscription
        url = "/notification/v1/endpoint/%s" % (endpoint_id)
        dao = NWS_DAO()
        delete_response = dao.deleteURL(url, None)

        #Http response code 204 No Content:
        #The server has fulfilled the request but does not need to return an entity-body
        if delete_response.status != 204:
            raise DataFailureException(url, delete_response.status, delete_response.data)

        return delete_response.status

    def update_endpoint(self, endpoint):
        """
        Update an existing endpoint

        :param endpoint:
        is the updated endpoint that the client wants to update
        """
        #Validate
        self._validate_uuid(endpoint.endpoint_id)
        self._validate_subscriber_id(endpoint.subscriber_id)

        #Update the subscription
        dao = NWS_DAO()
        url = "/notification/v1/endpoint/%s" % (endpoint.endpoint_id)

        put_response = dao.putURL(url, {"Content-Type": "application/json"}, Serializer().serialize(endpoint))

        #Http response code 204 No Content:
        #The server has fulfilled the request but does not need to return an entity-body
        if put_response.status != 204:
            raise DataFailureException(url, put_response.status, put_response.data)

        return put_response.status

    def create_new_endpoint(self, endpoint):
        """
        Create a new endpoint

        :param endpoint:
        is the new endpoint that the client wants to create
        """
        #Validate

        #For creating new endpoints an endpointid is optional however if
        #its present we should validate it
        if endpoint.end_point_id:
            self._validate_uuid(endpoint.endpoint_id)
        self._validate_subscriber_id(endpoint.subscriber_id)

        #Create new subscription
        dao = NWS_DAO()
        url = "/notification/v1/endpoint"

        post_response = dao.postURL(url, {"Content-Type": "application/json"}, Serializer().serialize(endpoint))

        #HTTP Status Code 201 Created: The request has been fulfilled and resulted
        #in a new resource being created
        if post_response.status != 201:
            raise DataFailureException(url, post_response.status, post_response.data)

        return post_response.status

    #SUBSCRIPTION RESOURCE
    def delete_subscription(self, subscription_id):
        """
        Deleting an existing subscription

        :param subscription_id:
        is the subscription that the client wants to delete
        """
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
        is the updated subscription that the client wants to update
        """
        #Validate
        if subscription.get_channel() is not None:
            self._validate_uuid(subscription.get_channel().get_channel_id())
        if subscription.get_endpoint() is not None:
            if subscription.get_endpoint().get_endpoint_id() is not None:
                self._validate_uuid(subscription.get_endpoint().get_endpoint_id())
            self._validate_subscriber_id(subscription.get_endpoint().get_subscriber_id())

        #Update the subscription
        dao = NWS_DAO()
        url = "/notification/v1/subscription/%s" % (subscription.subscription_id)

        put_response = dao.putURL(url, {"Content-Type": "application/json"}, Serializer().serialize(subscription))

        #Http response code 204 No Content:
        #The server has fulfilled the request but does not need to return an entity-body
        if put_response.status != 204:
            raise DataFailureException(url, put_response.status, put_response.data)

        return put_response.status

    def create_new_subscription(self, subscription):
        """
        Create a new subscription

        :param subscription:
        is the new subscription that the client wants to create
        """
        #Validate input
        if subscription.get_subscription_id() is not None:
            self._validate_uuid(subscription.get_subscription_id())

        if subscription.get_endpoint() is not None:
            if subscription.get_endpoint().subscriber_id:
                self._validate_subscriber_id(subscription.endpoint.subscriber_id)
    
            if subscription.get_endpoint().get_endpoint_id() is not None:
                self._validate_uuid(subscription.endpoint.get_endpoint_id())

        if subscription.get_channel() is not None:
            self._validate_uuid(subscription.channel.get_channel_id())

        #Create new subscription
        dao = NWS_DAO()
        url = "/notification/v1/subscription"

        post_response = dao.postURL(url, {"Content-Type": "application/json"}, Serializer().serialize(subscription))

        #HTTP Status Code 201 Created: The request has been fulfilled and resulted
        #in a new resource being created
        if post_response.status != 201:
            raise DataFailureException(url, post_response.status, post_response.data)

        return post_response.status

    def get_subscriptions_by_channel_id(self, channel_id):
        """
        Search for all subscriptions on a given channel
        """
        return self._get_subscriptions_from_nws(channel_id=channel_id)

    def get_subscriptions_by_subscriber_id(self, subscriber_id):
        """
        Search for all subscriptions by a given subscriber
        """
        return self._get_subscriptions_from_nws(subscriber_id=subscriber_id)

    def get_subscriptions_by_channel_id_and_subscriber_id(self, channel_id, subscriber_id):
        """
        Search for all subscriptions by a given channel and subscriber
        """
        return self._get_subscriptions_from_nws(channel_id=channel_id, subscriber_id=subscriber_id)

    def get_subscription_by_channel_id_and_endpoint_id(self, channel_id, endpoint_id):
        """
        Search for subscription by a given channel and endpoint
        """
        subscriptions = []
        try:
            subscriptions = self._get_subscriptions_from_nws(channel_id=channel_id, endpoint_id=endpoint_id)
        except Exception as ex:
            raise

        return subscriptions[0]

    def _get_subscriptions_from_nws(self, *args, **kwargs):
        """
        Search for all subscriptions by a parameter
        """
        url = "/notification/v1/subscription" #?subscriber_id=%s" % (subscriber_id)

        number_of_args = len(kwargs)
        if number_of_args > 0:
            url += '?'
            for k,v in kwargs.iteritems():
                url += k + '=' + v
                if number_of_args > 1:
                    url += '&'
                number_of_args -= 1

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        subscriptions = SubscriptionList()
        Serializer().deserialize(subscriptions, response.data)

        return subscriptions.view_models

    #MESSAGE RESOURCE
    def create_new_message(self, message):
        """
        Create a new message

        :param message:
        is the new message that the client wants to create
        """
        
        #Create new channel
        dao = NWS_DAO()
        url = "/notification/v1/message"

        post_response = dao.postURL(url, {"Content-Type": "application/json"}, Serializer().serialize(message))

        if post_response.status != 201:
            raise DataFailureException(url, post_response.status, post_response.data)

        return post_response.status

#        subscriptions = SubscriptionList()
#        Serializer().deserialize(subscriptions, response.data)
#
#        return subscriptions.view_models

    #CHANNEL RESOURCE
    def create_new_channel(self, channel):
        """
        Create a new channel

        :param channel:
        is the new channel that the client wants to create
        """
        #Validate
        #For creating new channels an channel_id is optional however if
        #its present we should validate it
        if channel.get_channel_id() is not None:
            self._validate_uuid(channel.get_channel_id())

        #Create new channel
        dao = NWS_DAO()
        url = "/notification/v1/channel"

        post_response = dao.postURL(url, {"Content-Type": "application/json"}, Serializer().serialize(channel))

        #HTTP Status Code 201 Created: The request has been fulfilled and resulted
        #in a new resource being created
        if post_response.status != 201:
            raise DataFailureException(url, post_response.status, post_response.data)

        return post_response.status

    def delete_channel(self, channel_id):
        """
        Deleting an existing channel

        :param channel_id:
        is the channel that the client wants to delete
        """

        #Validate the subscription_id
        self._validate_uuid(channel_id)

        #Delete the subscription
        url = "/notification/v1/channel/%s" % (channel_id)
        dao = NWS_DAO()
        delete_response = dao.deleteURL(url, None)

        #Http response code 204 No Content:
        #The server has fulfilled the request but does not need to return an entity-body
        if delete_response.status != 204:
            raise DataFailureException(url, delete_response.status, delete_response.data)

        return delete_response.status

    def get_channel_by_channel_id(self, channel_id):
        """
        Get a channel by channel id
        """
        #Validate the channel_id
        self._validate_uuid(channel_id)

        url = "/notification/v1/channel/%s" % (channel_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        channel = Channel()
        Serializer().deserialize(channel, response.data)

        return channel

    def get_channel_by_surrogate_id(self, channel_type, surrogate_id):
        """
        Get a channel by surrogate id
        """
        url = "/notification/v1/channel/%s|%s" % (channel_type, surrogate_id)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        channel = Channel()
        Serializer().deserialize(channel, response.data)

        return channel

    def get_channels_by_sln(self, channel_type, sln):
        """
        Search for all channels by sln
        """
        url = "/notification/v1/channel?type=%s&tag_sln=%s" % (channel_type, sln)

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        channel_list = ChannelList()
        Serializer().deserialize(channel_list, response.data)

        return channel_list.view_models

    def get_channels(self):
        """
        Search for all channels
        """
        url = "/notification/v1/channel"

        dao = NWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        channel_list = ChannelList()
        Serializer().deserialize(channel_list, response.data)

        return channel_list.view_models

#    def _subscriptions_from_json(self, data):
#        """
#        Returns a subscription model created from the passed json.
#        """
#        subscriptions = []
#        for subscription_data in data['Subscriptions']:
#            subscriptions.append(self._get_subscription(subscription_data))
#
#        return subscriptions

#    def _get_subscription(self, subscription_data):
#        """
#        Returns a subscription
#        """
#        subscription = Subscription()
#
#        subscription.subscription_id = subscription_data['SubscriptionID']
#        subscription.channel_id = subscription_data['Channel']['ChannelID']
#        subscription.end_point_id = subscription_data['Endpoint']['EndpointID']
#        subscription.end_point = subscription_data['Endpoint']['EndpointAddress']
#        subscription.protocol = subscription_data['Endpoint']['Protocol']
#        subscription.subscriber_id = subscription_data['Endpoint']['SubscriberID']
#        subscription.owner_id = subscription_data['Endpoint']['OwnerID']
#        #subscription.subscriber_type = subscription_data['Endpoint']['SubscriberType']
#        subscription.clean_fields()
#
#        return subscription

#    def _channels_from_json(self, data):
#        """
#        Returns a list of channels created from the passed json.
#        """
#        channels = []
#        for channel_data in data['Channels']:
#            channels.append(self._get_channel(channel_data))
#        return channels
#
#    def _channel_from_json(self, data):
#        """
#        Returns a list of channels created from the passed json.
#        """
#
#        return self._get_channel(data['Channel'])

#    def _get_channel(self, channel_data):
#        """
#        Returns a channel model
#        """
#        channel = Channel()
#
#        channel.channel_id = channel_data['ChannelID']
#        channel.surrogate_id = channel_data['SurrogateID']
#        channel.type = channel_data['Type']
#        channel.name = channel_data['Name']
#        channel.template_surrogate_id = channel_data['TemplateSurrogateID']
#        if 'Description' in channel_data:
#            channel.description = channel_data['Description']
#        #channel.expires = channel_data['Expires']
#        #channel.last_modified = channel_data['LastModified']
#        channel.clean_fields()
#        return channel
#
#    def _endpoints_from_view_model(self, list_view_model):
#        
#        endpoints = []
#        for view_model in list_view_model.view_models:
#            endpoints.append(self._endpoint_from_view_model(view_model))
#        return endpoints
#
#    def _endpoints_from_json(self, data):
#        """
#        Returns a list of endpoints created from the passed json.
#        """
#        endpoints = []
#        for endpoint_data in data['Endpoints']:
#            endpoints.append(self._get_endpoint(endpoint_data))
#        return endpoints
#
#    def _endpoint_from_view_model(self, view_model):
#        """
#        Returns a endpoint created from the passed view model.
#        """
#        
#        endpoint = Endpoint()
#
#        endpoint.end_point_id = view_model.endpoint_id
#        endpoint.end_point_uri = view_model.endpoint_uri
#        endpoint.end_point = view_model.endpoint_address
#        endpoint.carrier = view_model.carrier
#        endpoint.protocol = view_model.protocol
#        endpoint.subscriber_id = view_model.subscriber_id
#        endpoint.owner_id = view_model.owner_id
#        endpoint.active = view_model.active
#        endpoint.default = view_model.default
#        endpoint.clean_fields()
#        return endpoint
#    
#
#    def _endpoint_from_json(self, data):
#        """
#        Returns a endpoint created from the passed json.
#        """
#
#        return self._get_endpoint(data['Endpoint'])
#
#    def _get_endpoint(self, endpoint_data):
#        """
#        Returns a endpoint model
#        """
#        endpoint = Endpoint()
#
#        endpoint.end_point_id = endpoint_data['EndpointID']
#        endpoint.end_point_uri = endpoint_data['EndpointURI']
#        endpoint.end_point = endpoint_data['EndpointAddress']
#        endpoint.carrier = endpoint_data['Carrier']
#        endpoint.protocol = endpoint_data['Protocol']
#        endpoint.subscriber_id = endpoint_data['SubscriberID']
#        endpoint.owner_id = endpoint_data['OwnerID']
#        endpoint.active = endpoint_data['Active']
#        endpoint.default = endpoint_data['Default']
#        endpoint.clean_fields()
#        return endpoint
#
#    def _template_from_json(self, data):
#        """
#        Returns a template model created from the passed json.
#        """
#        template_data = json.loads(data)
#        return template_data['Template']

    def _validate_uuid(self, id):
        if id is None:
            raise InvalidUUID(id)
        if not re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', id):
            raise InvalidUUID(id)

    def _validate_subscriber_id(self, subscriber_id):
        if subscriber_id is None or subscriber_id == '':
            raise InvalidNetID(subscriber_id)
        if not re.match(r'^([a-z]adm_)?[a-z][a-z0-9]{0,7}$', subscriber_id, re.I):
            raise InvalidNetID(subscriber_id)

    def _validate_endpoint_protocol(self, protocol):
        if not re.match(r'^(Email|SMS)$', protocol, re.I):
            raise InvalidEndpointProtocol(protocol)
