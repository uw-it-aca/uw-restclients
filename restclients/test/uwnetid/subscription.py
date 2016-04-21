from datetime import date
from django.test import TestCase
from django.conf import settings
from restclients.uwnetid.subscription import get_email_forwarding, \
    get_netid_subscriptions, put_netid_subscription
from restclients.exceptions import DataFailureException

class EmailForwardingTest(TestCase):

    def test_get_email_forwarding(self):
        with self.settings(
            RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):

            uw_email = get_email_forwarding("javerage")
            self.assertEquals(uw_email.status, "Active")
            self.assertTrue(uw_email.is_active())
            self.assertTrue(uw_email.permitted)
            self.assertFalse(uw_email.is_uwgmail())
            self.assertTrue(uw_email.is_uwlive())
            self.assertEquals(uw_email.fwd,
                              "javerage@ol.uw.edu")

            uw_email = get_email_forwarding("none")
            self.assertTrue(uw_email.permitted)
            self.assertEquals(uw_email.status, "Inactive")
            self.assertIsNone(uw_email.fwd)
            self.assertFalse(uw_email.is_active())
            self.assertFalse(uw_email.is_uwgmail())
            self.assertFalse(uw_email.is_uwlive())

            uw_email = get_email_forwarding("jbothell")
            self.assertEquals(uw_email.status, "Active")
            self.assertEquals(uw_email.fwd,
                              "jbothell@gamail.uw.edu")
            self.assertTrue(uw_email.is_active())
            self.assertTrue(uw_email.permitted)
            self.assertTrue(uw_email.is_uwgmail())
            self.assertFalse(uw_email.is_uwlive())

            uw_email = get_email_forwarding("eight")
            self.assertEquals(uw_email.status, "Active")
            self.assertEquals(uw_email.fwd,
                              "eight@ol.uw.edu")
            self.assertTrue(uw_email.is_active())
            self.assertTrue(uw_email.permitted)
            self.assertFalse(uw_email.is_uwgmail())
            self.assertTrue(uw_email.is_uwlive())

    def test_invalid_user(self):
        with self.settings(
                RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):

            #Testing error message in a 200 response
            self.assertRaises(DataFailureException,
                              get_email_forwarding,
                              "invalidnetid")
            #Testing non-200 response
            self.assertRaises(DataFailureException,
                              get_email_forwarding,
                              "invalidnetid123")

            try:
                get_email_forwarding("invalidnetid")
            except DataFailureException as ex:
                self.assertEquals(ex.msg, "No such NetID 'invalidnetid'")


class NetidSubscriptionTest(TestCase):
    def test_get_netid_subscriptions(self):
        with self.settings(
                RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):
            subscriptions = get_netid_subscriptions(
                'javerage', [60, 20, 100, 105, 137, 41])
            self.assertEquals(len(subscriptions), 6)
            for subscription in subscriptions:
                if subscription.subscription_code == 60:
                    self.assertEquals(subscription.status_code, 20)
                    self.assertEquals(subscription.data_field, 'KPW')
                    self.assertTrue(subscription.permitted)
                    self.assertEquals(len(subscription.actions), 5)
                    self.assertEquals(len(subscription.permits), 1)
                    self.assertEquals(subscription.permits[0].category_code, 11)
                    self.assertEquals(subscription.permits[0].status_name, 'current')
                elif subscription.subscription_code == 20:
                    self.assertTrue(subscription.permitted)
                    self.assertEquals(len(subscription.actions), 6)
                elif subscription.subscription_code == 100:
                    self.assertTrue(subscription.permitted)
                elif subscription.subscription_code == 105:
                    self.assertTrue(subscription.permitted)
                    self.assertEquals(len(subscription.actions), 7)
                    self.assertEquals(subscription.data_field, 'FWD')
                    self.assertEquals(subscription.data_value,
                                      'javerage@javerage.deskmail.washington.edu')
                elif subscription.subscription_code == 137:
                    self.assertTrue(subscription.permitted)
                    self.assertEquals(len(subscription.actions), 8)
                    self.assertEquals(len(subscription.permits), 3)
                    self.assertEquals(subscription.permits[0].category_code, 0)
                    self.assertEquals(subscription.permits[0].data_value, 'disk=1024')
                    self.assertEquals(subscription.permits[1].status_code, 1)
                    self.assertEquals(subscription.permits[1].data_value, 'rate=4.17')
                    self.assertEquals(subscription.permits[2].category_code, 11)
                    self.assertEquals(subscription.permits[2].data_value,
                                      'max=1024.0 disk=1024.0')
                elif subscription.subscription_code == 41:
                    self.assertFalse(subscription.permitted)


class NetidPutSubscriptionTest(TestCase):
    def test_put_netid_subscription(self):
        with self.settings(
                RESTCLIENTS_NETID_DAO_CLASS =
                'restclients.dao_implementation.netid.File'):
            subscriptions = put_netid_subscription('javerage', 'Modify', 233)
            self.assertEquals(len(subscriptions), 1)
            self.assertEquals(subscriptions[0].subscription_code, 233)
            self.assertEquals(subscriptions[0].status_code, 20)
            self.assertEquals(len(subscriptions[0].actions), 1)
            self.assertEquals(len(subscriptions[0].permits), 2)
