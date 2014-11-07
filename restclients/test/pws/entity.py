from django.test import TestCase
from django.conf import settings
from restclients.pws import PWS
from restclients.exceptions import InvalidRegID, InvalidNetID, DataFailureException

class PWSTestEntityData(TestCase):

    def test_by_regid(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Valid data, shouldn't throw exceptions
            self._test_regid('somalt', '605764A811A847E690F107D763A4B32A')

    def test_by_netid(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Valid data, shouldn't throw exceptions
            self._test_netid('somalt', '605764A811A847E690F107D763A4B32A')

    def test_bad_netids(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Invalid data, should throw exceptions
            pws = PWS()
            self.assertRaises(InvalidNetID, pws.get_entity_by_netid, "")
            self.assertRaises(InvalidNetID, pws.get_entity_by_netid, " ")
            self.assertRaises(InvalidNetID, pws.get_entity_by_netid, "one two")
            self.assertRaises(InvalidNetID, pws.get_entity_by_netid, "</html>")
            self.assertRaises(InvalidNetID, pws.get_entity_by_netid, "aaaaaaaaa")
            self.assertRaises(DataFailureException, pws.get_entity_by_netid, "hello")

    def test_bad_regids(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Invalid data, should throw exceptions
            pws = PWS()
            self.assertRaises(InvalidRegID, pws.get_entity_by_regid, "")
            self.assertRaises(InvalidRegID, pws.get_entity_by_regid, " ")
            self.assertRaises(InvalidRegID, pws.get_entity_by_regid, "AAA")

            self.assertRaises(InvalidRegID,
                              pws.get_entity_by_regid,
                              "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

            self.assertRaises(InvalidRegID,
                              pws.get_entity_by_regid,
                              "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG")

            self.assertNotEquals(None,
                              pws.get_entity_by_regid,
                              "605764A811A847E690F107D763A4B32A")

    def _test_regid(self, netid, regid):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            pws = PWS()
            entity = pws.get_entity_by_regid(regid)

            self.assertEquals(entity.uwnetid, netid, netid + "'s netid")
            self.assertEquals(entity.uwregid, regid, netid + "'s regid")

    def _test_netid(self, netid, regid):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            entity = pws.get_entity_by_netid(netid)

            self.assertEquals(entity.uwnetid, netid, netid + "'s netid")
            self.assertEquals(entity.uwregid, regid, netid + "'s regid")
