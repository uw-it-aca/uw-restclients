from django.test import TestCase
from django.conf import settings
from restclients.sms import SMSService
from restclients.exceptions import DataFailureException
from unittest import skipIf


class SMS(TestCase):
    '''
    This test requires internet connectivity.
    If no network is found you will get this exception:
    ServerNotFoundError
    '''
#Live tests
    @skipIf(not hasattr(settings, 'SMS'), "Needs SMS configuration to test live SMS functionality")
    def test_send_default_number_live(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Live'):
            DEFAULT_NUMBER = "5005550006"
            sms = SMSService()

            message = sms.create_message(DEFAULT_NUMBER, "sending test message")

            response = sms.send_message(message)
            self.assertEquals(response.body, "sending test message")
            self.assertEquals(response.to, "+1" + DEFAULT_NUMBER)
            self.assertEquals(response.status, "queued")
            #Twilio sid confirms a live API call
            self.assertTrue(response.rid != None)

    @skipIf(not hasattr(settings, 'SMS'), "Needs SMS configuration to test live SMS functionality")
    def test_send_with_phonenumber_live(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Live'):
            TEST_NUMBER = "2065555555"
            sms = SMSService()

            message = sms.create_message(TEST_NUMBER, "sending test message")

            response = sms.send_message(message)
            self.assertEquals(response.body, "sending test message")
            self.assertEquals(response.to, "+1" + TEST_NUMBER)
            self.assertEquals(response.status, "queued")
            self.assertTrue(response.rid != None)

    @skipIf(not hasattr(settings, 'SMS'), "Needs SMS configuration to test live SMS functionality")
    def test_send_with_invalid_phonenumber_live(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Live'):
            TEST_NUMBER = "5005550001"
            sms = SMSService()

            message = sms.create_message(TEST_NUMBER, "sending test message")

            with self.assertRaises(DataFailureException) as sms_exception:
                sms.send_message(message)

            the_exception = sms_exception.exception
            self.assertEquals(the_exception.msg, "21211: The 'To' number +15005550001 is not a valid phone number.")
            self.assertEquals(the_exception.status, 400)

#Local tests
    def test_send_without_phonenumber(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Local'):
            DEFAULT_NUMBER = "5005550006"
            sms = SMSService()

            message = sms.create_message(DEFAULT_NUMBER, "sending test message")

            response = sms.send_message(message)
            self.assertEquals(response.body, "sending test message")
            self.assertEquals(response.to, DEFAULT_NUMBER)
            self.assertEquals(response.status, "queued")
            self.assertTrue(response.rid != None)

    def test_send_with_phonenumber(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Local'):
            TEST_NUMBER = "2065555555"
            sms = SMSService()

            message = sms.create_message(TEST_NUMBER, "sending test message")

            response = sms.send_message(message)
            self.assertEquals(response.body, "sending test message")
            self.assertEquals(response.to, TEST_NUMBER)
            self.assertEquals(response.status, "queued")
            self.assertTrue(response.rid != None)

    def test_create_message(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Local'):
            sms = SMSService()

            message = sms.create_message("555-555-5555", "test")
            self.assertTrue(message != None)
