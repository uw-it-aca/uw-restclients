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

            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, " ")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "one two")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "</html>")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "aaaaaaaaa")
            
            expected_empty_string = pws.get_person_by_netid('hello') #no file for that netid
            self.assertEquals(None, expected_empty_string)
            expected_empty_string = pws.get_person_by_regid('9136CCB8F66711D5BE060004AC494FFF') #no file for that regid
            self.assertEquals(None, expected_empty_string)
