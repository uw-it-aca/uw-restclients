from django.test import TestCase
from restclients.uwnetid.subscription_233 import get_office365edu_prod_subs,\
    get_office365edu_test_subs
from restclients.exceptions import DataFailureException
from restclients.test import fdao_uwnetid_override


@fdao_uwnetid_override
class Office365EduSubsTest(TestCase):

    def test_get_office365edu_prod_subs(self):
        subs = get_office365edu_prod_subs("bill")
        self.assertFalse(subs.is_status_active())

    def test_get_office365edu_test_subs(self):
        subs = get_office365edu_test_subs("bill")
        self.assertFalse(subs.is_status_active())
