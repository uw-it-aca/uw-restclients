from django.test import TestCase
from django.conf import settings
from restclients.models.sws import Person
from restclients.pws import PWS
from restclients.exceptions import InvalidIdCardPhotoSize, InvalidNetID
from restclients.exceptions import DataFailureException

class TestIdCardPhoto(TestCase):

    def test_actas(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            user = Person(uwnetid="bill")
            person = Person(uwregid="9136CCB8F66711D5BE060004AC494FFE")

            pws = PWS()
            self.assertEquals(pws.actas, None, "Correct actas attribute")

            pws = PWS(actas=user.uwnetid)
            self.assertEquals(pws.actas, user.uwnetid, "Correct actas attribute")

            pws = PWS(actas="")
            self.assertEquals(pws.actas, "", "Empty str actas attribute")
            self.assertRaises(InvalidNetID, pws.get_idcard_photo, person.uwregid)

            pws = PWS(actas="000")
            self.assertEquals(pws.actas, "000", "Invalid actas attribute")
            self.assertRaises(InvalidNetID, pws.get_idcard_photo, person.uwregid)

            pws = PWS(actas=67)
            self.assertEquals(pws.actas, 67, "Invalid actas attribute")
            self.assertRaises(InvalidNetID, pws.get_idcard_photo, person.uwregid)


    def test_photo_size(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            person = Person(uwregid="9136CCB8F66711D5BE060004AC494FFE")

            pws = PWS()

            img = pws.get_idcard_photo(person.uwregid)
            self.assertEquals(len(img), 4661, "Correct file for default size")

            img = pws.get_idcard_photo(person.uwregid, size="medium")
            self.assertEquals(len(img), 4661, "Correct file for medium size")

            img = pws.get_idcard_photo(person.uwregid, size="small")
            self.assertEquals(len(img), 4661, "Correct file for small size")

            img = pws.get_idcard_photo(person.uwregid, size="large")
            self.assertEquals(len(img), 4661, "Correct file for large size")

            img = pws.get_idcard_photo(person.uwregid, size=100)
            self.assertEquals(len(img), 4661, "Correct file for custom size")

            # Invalid size param, should throw exceptions
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, "tiny")
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, "larger")
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, "60000")
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, 60000)
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, 0)
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, 1)
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, -50)
            self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                              person.uwregid, 20.5)
