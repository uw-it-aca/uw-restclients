from django.test import TestCase
from django.conf import settings
from restclients.pws import PWS
from restclients.exceptions import InvalidRegID, InvalidNetID

class PWSTestPersonData(TestCase):
    
    def test_by_regid(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Valid data, shouldn't throw exceptions
            self._test_regid('javerage', '9136CCB8F66711D5BE060004AC494FFE')
            self._test_regid('pmichaud', 'A9D2DDFA6A7D11D5A4AE0004AC494FFE')
            self._test_regid('kroberts', '0F01799E6A7D11D5A4AE0004AC494FFE')
            self._test_regid('mwinslow', '6DF0A9206A7D11D5A4AE0004AC494FFE')
            self._test_regid('lmanes', '260A0DEC95CB11D78BAA000629C31437')
            self._test_regid('tbohn', 'B814EFBC6A7C11D5A4AE0004AC494FFE')
            self._test_regid('rjansson', 'FBB38FE46A7C11D5A4AE0004AC494FFE')

    def test_by_netid(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Valid data, shouldn't throw exceptions
            self._test_netid('javerage', '9136CCB8F66711D5BE060004AC494FFE')
            self._test_netid('pmichaud', 'A9D2DDFA6A7D11D5A4AE0004AC494FFE')
            self._test_netid('kroberts', '0F01799E6A7D11D5A4AE0004AC494FFE')
            self._test_netid('mwinslow', '6DF0A9206A7D11D5A4AE0004AC494FFE')
            self._test_netid('lmanes', '260A0DEC95CB11D78BAA000629C31437')
            self._test_netid('tbohn', 'B814EFBC6A7C11D5A4AE0004AC494FFE')
            self._test_netid('rjansson', 'FBB38FE46A7C11D5A4AE0004AC494FFE')

    def test_bad_netids(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Invalid data, should throw exceptions
            pws = PWS()
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, " ")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "one two")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "</html>")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "aaaaaaaaa")

            self.assertEquals(None, pws.get_person_by_netid('hello'))

    def test_bad_regids(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Invalid data, should throw exceptions
            pws = PWS()
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, "")
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, " ")
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, "AAA")

            self.assertRaises(InvalidRegID, 
                              pws.get_person_by_regid, 
                              "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

            self.assertRaises(InvalidRegID, 
                              pws.get_person_by_regid, 
                              "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG")

            self.assertEquals(None, 
                              pws.get_person_by_regid('9136CCB8F66711D5BE060004AC494FFF'))
        
    def _test_regid(self, netid, regid):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            
            pws = PWS()
            person = pws.get_person_by_regid(regid)

            self.assertEquals(person.uwnetid, netid, netid + "'s netid")
            self.assertEquals(person.uwregid, regid, netid + "'s regid")

    def _test_netid(self, netid, regid):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            person = pws.get_person_by_netid(netid)

            self.assertEquals(person.uwnetid, netid, netid + "'s netid")
            self.assertEquals(person.uwregid, regid, netid + "'s regid")

