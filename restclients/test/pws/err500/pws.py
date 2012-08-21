from django.test import TestCase
from django.conf import settings
from restclients.pws import PWS
from restclients.exceptions import DataFailureException

class PWSTest500(TestCase):
    def test_pws_regid_500(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.errors.Always500'):
            pws = PWS()
            self.assertRaises(DataFailureException, pws.get_person_by_regid, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

            try:
                pws.get_person_by_regid("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                self.fail("This needs to be an exception")
            except DataFailureException as ex:
                self.assertEqual(ex.status, 500, "Exception has the right status")
                self.assertEqual(ex.url, "/identity/v1/person/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.json", "Exception has the right url")

    def test_pws_netid_500(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.errors.Always500'):
            pws = PWS()
            self.assertRaises(DataFailureException, pws.get_person_by_netid, "fake")

            try:
                pws.get_person_by_netid("fake")
                self.fail("This needs to be an exception")
            except DataFailureException as ex:
                self.assertEqual(ex.status, 500, "Exception has the right status")
                self.assertEqual(ex.url, "/identity/v1/person.json?netid=fake", "Exception has the right url")
