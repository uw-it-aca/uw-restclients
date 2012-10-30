from django.test import TestCase
from django.conf import settings
from restclients.sms import SMSService
from restclients.exceptions import DataFailureException, InvalidPhoneNumber, PhoneNumberRequired


class SMSInvalidNumbers(TestCase):
    def test_validate_valid_number(self):
        sms = SMSService()

        sms.validate_phone_number("2065550000")
        sms.validate_phone_number("(206)555-0000")
        sms.validate_phone_number("206-555-0000")
        sms.validate_phone_number("206.555.0000")
        sms.validate_phone_number("206 555 0000")
        sms.validate_phone_number("(206) 555 0000")
        sms.validate_phone_number("(206) 555-0000")

    def test_validate_invalid_number(self):
        sms = SMSService()

        self.assertRaises(InvalidPhoneNumber, sms.validate_phone_number, "abc")
        self.assertRaises(InvalidPhoneNumber, sms.validate_phone_number, "555-0000")
        self.assertRaises(InvalidPhoneNumber, sms.validate_phone_number, "0")
        self.assertRaises(InvalidPhoneNumber, sms.validate_phone_number, "-234")
        self.assertRaises(InvalidPhoneNumber, sms.validate_phone_number, "000-000-abcd")
        self.assertRaises(InvalidPhoneNumber, sms.validate_phone_number, "")

    def test_missing_number(self):
        sms = SMSService()

        self.assertRaises(PhoneNumberRequired, sms.create_message, "", "")
