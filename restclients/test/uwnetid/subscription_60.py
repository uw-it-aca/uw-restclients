from django.test import TestCase
from restclients.uwnetid.subscription_60 import is_current_staff,\
    is_current_faculty, get_kerberos_subs, is_current_clinician
from restclients.exceptions import DataFailureException
from restclients.test import fdao_uwnetid_override


@fdao_uwnetid_override
class KerberosSubsTest(TestCase):

    def test_get_kerberos_subs_permits(self):
        self.assertTrue(is_current_staff("bill"))
        self.assertFalse(is_current_faculty("bill"))

        self.assertFalse(is_current_staff("phil"))
        self.assertTrue(is_current_faculty("phil"))

        self.assertTrue(is_current_clinician("james"))
        self.assertTrue(is_current_clinician("fred"))
        self.assertFalse(is_current_clinician("bill"))

        subs = get_kerberos_subs("bill")
        self.assertTrue(subs.is_status_active())

        subs = get_kerberos_subs("phil")
        self.assertTrue(subs.is_status_active())

    def test_unpermitted(self):
        subs = get_kerberos_subs("none")
        self.assertFalse(subs.is_status_active())
        self.assertFalse(subs.is_status_inactive())
        self.assertFalse(subs.permitted)

    def test_expiring_subs(self):
        subs = get_kerberos_subs("eight")
        self.assertTrue(subs.is_status_active())
        self.assertFalse(subs.is_status_inactive())
        self.assertFalse(subs.permitted)

    def test_invalid_user(self):
        #Testing error message in a 200 response
        self.assertRaises(DataFailureException,
                          is_current_staff,
                          "invalidnetid")
        #Testing non-200 response
        self.assertRaises(DataFailureException,
                          is_current_faculty,
                          "jnewstudent")
