from django.test import TestCase
from django.conf import settings
from restclients.uwnetid.subscription_60 import is_current_staff,\
    is_current_faculty
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
                              "none")
