from django.test import TestCase
from django.conf import settings
from restclients.uwnetid.subscription_233 import get_office365edu_prod_subs,\
    get_office365edu_test_subs
from restclients.exceptions import DataFailureException


class Office365EduSubsTest(TestCase):

    def test_get_office365edu_prod_subs(self):
        with self.settings(
            RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):

            subs = get_office365edu_prod_subs("bill")
            self.assertFalse(subs.is_status_active())

    def test_get_office365edu_test_subs(self):
        with self.settings(
                RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.uwnetid.File'):

            subs = get_office365edu_test_subs("bill")
            self.assertFalse(subs.is_status_active())
