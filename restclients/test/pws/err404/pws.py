from django.test import TestCase
from django.conf import settings
from restclients.pws import PWS
from restclients.exceptions import DataFailureException

class PWSTest404(TestCase):
    def test_pws_regid_404(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.errors.Always404'):
            pws = PWS()
            self.assertRaises(DataFailureException, pws.get_person_by_regid, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    def test_pws_netid_404(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.errors.Always404'):
            pws = PWS()
            self.assertRaises(DataFailureException, pws.get_person_by_netid, "fake")

