from django.test import TestCase
from django.conf import settings
from restclients.pws import PWS

class PWSTestJAverage(TestCase):
    def test_by_regid(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            person = pws.get_person_by_regid('9136CCB8F66711D5BE060004AC494FFE')

            self.assertEquals(person.uwnetid, "javerage", "javerage's netid")
            self.assertEquals(person.uwregid, "9136CCB8F66711D5BE060004AC494FFE", "javerage's regid")

    def test_by_netid(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            person = pws.get_person_by_netid('javerage')

            self.assertEquals(person.uwnetid, "javerage", "javerage's netid")
            self.assertEquals(person.uwregid, "9136CCB8F66711D5BE060004AC494FFE", "javerage's regid")



