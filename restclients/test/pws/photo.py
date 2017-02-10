from django.test import TestCase
from restclients.models.sws import Person
from restclients.pws import PWS
from restclients.exceptions import InvalidIdCardPhotoSize, InvalidNetID
from restclients.exceptions import DataFailureException
from restclients.test import fdao_pws_override


@fdao_pws_override
class IdCardTestPhoto(TestCase):

    def test_actas(self):
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
        person = Person(uwregid="9136CCB8F66711D5BE060004AC494FFE")

        pws = PWS()

        img = pws.get_idcard_photo(person.uwregid)
        self.assertEquals(img.len, 4661, "Correct file for default size")

        img = pws.get_idcard_photo(person.uwregid, size="medium")
        self.assertEquals(img.len, 4661, "Correct file for medium size")

        img = pws.get_idcard_photo(person.uwregid, size="small")
        self.assertEquals(img.len, 4661, "Correct file for small size")

        img = pws.get_idcard_photo(person.uwregid, size="large")
        self.assertEquals(img.len, 4661, "Correct file for large size")

        img = pws.get_idcard_photo(person.uwregid, size=100)
        self.assertEquals(img.len, 4661, "Correct file for custom size")

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
                          person.uwregid, 01)
        self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                          person.uwregid, -50)
        self.assertRaises(InvalidIdCardPhotoSize, pws.get_idcard_photo,
                          person.uwregid, 20.5)
