from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException, InvalidUUID, InvalidNetID
from vm.v1.viewmodels import Channel, Endpoint, Subscription
from unittest2 import skip, skipIf


class NWSTestSubscription(TestCase):
    def test_subscriptions_channel_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_channel_id("b779df7b-d6f6-4afb-8165-8dbe6232119f")
            self.assertEquals(len(subscriptions), 5)

    def test_subscriptions_subscriber_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_subscriber_id("javerage", "10")
            self.assertEquals(len(subscriptions), 5)

    def test_subscriptions_channel_id_subscriber_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_channel_id_and_subscriber_id("b779df7b-d6f6-4afb-8165-8dbe6232119f", "javerage")
            self.assertEquals(len(subscriptions), 5)

    def test_create_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.subscription_id = "c4597f93-0f62-4feb-ac88-af5f0329001f"
            subscription.endpoint = Endpoint()
            subscription.endpoint.endpoint_address = "javerage0@uw.edu"
            subscription.endpoint.protocol = "Email"
            subscription.endpoint.subscriber_id = "javerage@washington.edu"
            subscription.endpoint.owner = "javerage@washington.edu"
            subscription.channel = Channel()
            subscription.channel.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"

            nws = NWS()
            self.assertRaises(DataFailureException, nws.create_new_subscription, subscription)

    def test_create_invalid_subscriberid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.subscription_id = "c4597f93-0f62-4feb-ac88-af5f0329001f"
            subscription.endpoint = Endpoint()
            subscription.endpoint.endpoint_address = "javerage0@uw.edu"
            subscription.endpoint.protocol = "Email"
            subscription.endpoint.subscriber_id = "-@#$ksjdsfkli13290243290490"
            subscription.endpoint.owner = "javerage"
            subscription.channel = Channel()
            subscription.channel.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.create_new_subscription, subscription)

    def test_create_empty_channelid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.endpoint = Endpoint()
            subscription.endpoint.endpoint_address = "javerage0@uw.edu"
            subscription.endpoint.protocol = "Email"
            subscription.endpoint.owner = "javerage"
            subscription.endpoint.subscriber_id = "javerage@washington.edu"
            subscription.channel = Channel()

            nws = NWS()
            self.assertRaises(InvalidUUID, nws.create_new_subscription, subscription)

#    def test_create_empty_subscription(self):
#        with self.settings(
#                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
#            subscription = Subscription()
#
#            nws = NWS()
#            self.assertRaises(InvalidUUID, nws.create_new_subscription, subscription)

    @skip("Not implemented")
    def test_update_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.subscription_id = "c4597f93-0f62-4feb-ac88-af5f0329001f"
            subscription.endpoint = Endpoint()
            subscription.endpoint.endpoint_address = "javerage0@uw.edu"
            subscription.endpoint.protocol = "Email"
            subscription.endpoint.subscriber_id = "javerage@washington.edu"
            subscription.endpoint.owner = "javerage@washington.edu"
            subscription.channel = Channel()
            subscription.channel.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"

            nws = NWS()
            response_status = nws.update_subscription(subscription)
            self.assertEquals(response_status, 204)

    @skip("Not implemented")
    def test_update_invalid_subscriberid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.endpoint = Endpoint()
            subscription.endpoint.endpoint_address = "javerage0@uw.edu"
            subscription.endpoint.protocol = "Email"
            subscription.endpoint.subscriber_id = "-@#$ksjdsfkli13290243290490"
            subscription.endpoint.owner = "javerage"
            subscription.channel = Channel()
            subscription.channel.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"

            #subscription.subscriber_type = "Individual"

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.update_subscription, subscription)

    @skip("Not implemented")
    def test_update_empty_subscriberid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.endpoint = Endpoint()
            subscription.endpoint.endpoint_address = "javerage0@uw.edu"
            subscription.endpoint.protocol = "Email"
            subscription.endpoint.subscriber_id = ''
            subscription.endpoint.owner = "javerage"
            subscription.channel = Channel()
            subscription.channel.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.update_subscription, subscription)

    def test_delete_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            self.assertRaises(DataFailureException, nws.delete_subscription, "652236c6-a85a-4845-8dc5-3e518bec044c")

    def test_delete_invalid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            #Invalid UUID - missing the last character
            self.assertRaises(InvalidUUID, nws.delete_subscription, "652236c6-a85a-4845-8dc5-3e518bec044")

    def test_subscriber_id_validation(self):
        nws = NWS()
        nws._validate_subscriber_id('javerage')
        nws._validate_subscriber_id('javerage@washington.edu')

        self.assertRaises(InvalidNetID, nws._validate_subscriber_id, '00ok')
        self.assertRaises(InvalidNetID, nws._validate_subscriber_id, 'ok123456789')
        self.assertRaises(InvalidNetID, nws._validate_subscriber_id, 'javerage@gmail.com')
        self.assertRaises(InvalidNetID, nws._validate_subscriber_id, 'javerage@')

    @skipIf(True, "Used only for live testing")
    def test_subscription_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            self._subscription_channel_id_live()
            self._create_subscription_live()
            self._update_subscription_live()
            self._delete_subscription_live()

    def _subscription_channel_id_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_channel_id("ce1d46fe-1cdf-4c5a-a316-20f6c99789b8")
            self.assertTrue(len(subscriptions) > 0)

    def _create_subscription_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            subscription = Subscription()
            subscription.subscription_id = "6445864b-6d1c-47b7-a409-279ba4a4ccf4"
            subscription.end_point = "javerage09@uw.edu"
            subscription.protocol = "Email"
            subscription.user = "javerage"
            subscription.channel_id = "ce1d46fe-1cdf-4c5a-a316-20f6c99789b8"
            subscription.owner = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            response_status = nws.create_new_subscription(subscription)
            self.assertEquals(response_status, 201)

    @skip("Not implemented")
    def _update_subscription_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            subscription = Subscription()
            subscription.subscription_id = "6445864b-6d1c-47b7-a409-279ba4a4ccf4"
            subscription.end_point = "javerage10@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = "javerage"
            subscription.channel_id = "ce1d46fe-1cdf-4c5a-a316-20f6c99789b8"
            subscription.owner = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            response_status = nws.update_subscription(subscription)
            self.assertEquals(response_status, 204)

    def _delete_subscription_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            response_status = nws.delete_subscription("6445864b-6d1c-47b7-a409-279ba4a4ccf4")
            self.assertEquals(response_status, 204)
