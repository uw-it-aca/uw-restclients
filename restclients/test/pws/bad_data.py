from django.test import TestCase
from django.conf import settings
from restclients.pws import PWS
from restclients.exceptions import InvalidRegID, InvalidNetID

class PWSTestBadData(TestCase):
    def test_pws_404(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, "AAA")
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG")


            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "aaaaaaaaa")

