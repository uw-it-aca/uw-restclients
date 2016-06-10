from django.test import TestCase
from django.conf import settings
from restclients.uwnetid.subscription_60 import is_current_staff,\
    is_current_faculty, get_kerberos_subs, has_active_kerberos_subs
from restclients.exceptions import DataFailureException


class KerberosSubsTest(TestCase):

    def test_get_kerberos_subs_permits(self):
        with self.settings(
            RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):

            self.assertTrue(is_current_staff("bill"))
            self.assertFalse(is_current_faculty("bill"))

            self.assertFalse(is_current_staff("phil"))
            self.assertTrue(is_current_faculty("phil"))

            self.assertTrue(has_active_kerberos_subs("bill"))
            self.assertTrue(has_active_kerberos_subs("phil"))

    def test_unpermitted(self):
        with self.settings(
            RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):
            subs = get_kerberos_subs("none")
            self.assertFalse(subs.is_status_active())
            self.assertFalse(subs.permitted)
            self.assertFalse(has_active_kerberos_subs("none"))

    def test_expiring_subs(self):
        with self.settings(
            RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):
            subs = get_kerberos_subs("eight")
            self.assertTrue(subs.is_status_active())
            self.assertFalse(subs.permitted)
            self.assertFalse(has_active_kerberos_subs("eight"))

    def test_invalid_user(self):
        with self.settings(
                RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):

            #Testing error message in a 200 response
            self.assertRaises(DataFailureException,
                              is_current_staff,
                              "invalidnetid")
            #Testing non-200 response
            self.assertRaises(DataFailureException,
                              is_current_faculty,
                              "jnewstudent")
