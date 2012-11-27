from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException, InvalidUUID, InvalidNetID
from restclients.models import Subscription
from unittest import skipIf


class NWSTestSubscription(TestCase):
    def test_subscription_channel_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_channel_id("b779df7b-d6f6-4afb-8165-8dbe6232119f")
            self.assertEquals(len(subscriptions), 5)

    def test_subscription_subscriber_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_subscriber_id("javerage")
            self.assertEquals(len(subscriptions), 5)

    def test_create_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.end_point = "javerage0@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = "javerage"
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            response_status = nws.create_new_subscription(subscription)
            self.assertEquals(response_status, 201)

    def test_create_invalid_subscriberid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.end_point = "javerage0@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = "-@#$ksjdsfkli13290243290490"
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.create_new_subscription, subscription)

    def test_create_empty_subscriberid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.end_point = "javerage0@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = ""
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.create_new_subscription, subscription)

    def test_create_empty_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.create_new_subscription, subscription)

    def test_update_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.subscription_id = "c4597f93-0f62-4feb-ac88-af5f0329001f"
            subscription.end_point = "javerage0@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = "javerage"
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            response_status = nws.update_subscription(subscription)
            self.assertEquals(response_status, 204)

    def test_update_invalid_subscriberid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.end_point = "javerage0@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = "-@#$ksjdsfkli13290243290490"
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.update_subscription, subscription)

    def test_update_empty_subscriberid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            subscription = Subscription()
            subscription.end_point = "javerage0@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = ""
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            self.assertRaises(InvalidNetID, nws.update_subscription, subscription)

    def test_delete_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            response_status = nws.delete_subscription("652236c6-a85a-4845-8dc5-3e518bec044c")
            self.assertEquals(response_status, 204)

    def test_delete_invalid_subscription(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            #Invalid UUID - missing the last character
            self.assertRaises(InvalidUUID, nws.delete_subscription, "652236c6-a85a-4845-8dc5-3e518bec044")

    @skipIf(True, "Used only for live testing")
    def test_subscription_channel_id_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_channel_id("b779df7b-d6f6-4afb-8165-8dbe6232119f")
            self.assertTrue(len(subscriptions) > 0)
            #print len(subscriptions)

    @skipIf(True, "Used only for live testing")
    def test_create_subscription_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            subscription = Subscription()
            subscription.end_point = "javerage09@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = "javerage"
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            response_status = nws.create_new_subscription(subscription)
            self.assertEquals(response_status, 201)

    @skipIf(True, "Used only for live testing")
    def test_update_subscription_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            subscription = Subscription()
            subscription.subscription_id = "6445864b-6d1c-47b7-a409-279ba4a4ccf4"
            subscription.end_point = "javerage10@uw.edu"
            subscription.protocol = "Email"
            subscription.subscriber_id = "javerage"
            subscription.channel_id = "b779df7b-d6f6-4afb-8165-8dbe6232119f"
            subscription.owner_id = "javerage"
            #subscription.subscriber_type = "Individual"

            nws = NWS()
            response_status = nws.update_subscription(subscription)
            self.assertEquals(response_status, 204)

    @skipIf(True, "Used only for live testing")
    def test_delete_subscription_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            response_status = nws.delete_subscription("6445864b-6d1c-47b7-a409-279ba4a4ccf4")
            self.assertEquals(response_status, 204)
