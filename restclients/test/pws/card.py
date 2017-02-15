from django.test import TestCase
from restclients.pws import PWS
from restclients.exceptions import DataFailureException, InvalidProxRFID
from restclients.test import fdao_pws_override


@fdao_pws_override
class IdCardTestCard(TestCase):

    def test_by_rfid(self):
        pws = PWS()
        person = pws.get_person_by_prox_rfid('1223221621633408')
        self.assertEquals(person.uwnetid, 'javerage', "Correct netid")
        self.assertEquals(person.uwregid,
                          '9136CCB8F66711D5BE060004AC494FFE', "Correct regid")

        # Valid non-existent RFID
        self.assertRaises(DataFailureException,
                          pws.get_person_by_prox_rfid,
                          '1234567890123456')

        self.assertRaises(InvalidProxRFID,
                          pws.get_person_by_prox_rfid,
                          '123456')

    def test_bad_prox_rfids(self):
        pws = PWS()
        self.assertRaises(InvalidProxRFID, pws.get_person_by_prox_rfid, "")
        self.assertRaises(InvalidProxRFID,
                          pws.get_person_by_prox_rfid, " ")
        self.assertRaises(InvalidProxRFID,
                          pws.get_person_by_prox_rfid, "A")
        self.assertRaises(InvalidProxRFID,
                          pws.get_person_by_prox_rfid, "123456789012345N")
        self.assertRaises(InvalidProxRFID,
                          pws.get_person_by_prox_rfid, "1")
        self.assertRaises(InvalidProxRFID,
                          pws.get_person_by_prox_rfid, "1234567890")
