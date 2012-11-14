from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException


class NWSTestSubscription(TestCase):
    #Expected values will have to change when the json files are updated
    def test_subscription_channel_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_channel_id("uw_student_course_available|2012,winter,cse,120,w")
            self.assertEquals(len(subscriptions), 3)

    def test_subscription_subscriber_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            subscriptions = nws.get_subscriptions_by_subscriber_id("jrenfro")
            self.assertEquals(len(subscriptions), 2)
