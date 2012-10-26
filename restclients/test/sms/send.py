from django.test import TestCase
from django.conf import settings
from restclients.sms import SMSService


class SMS(TestCase):

    def test_send_without_phonenumber(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Local'):
            DEFAULT_NUMBER = "+15005550006"
            sms = SMSService()

            message = sms.create_message()
            response = message.send_message("sending test message")
            self.assertEquals(response.body, "sending test message")
            self.assertEquals(response.to_number, DEFAULT_NUMBER)
            self.assertEquals(response.status, "queued")

    def test_send_with_phonenumber(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Local'):
            TEST_NUMBER = "+12065555555"
            sms = SMSService()

            message = sms.create_message()
            response = message.send_message("sending test message", TEST_NUMBER)
            self.assertEquals(response.body, "sending test message")
            self.assertEquals(response.to_number, TEST_NUMBER)
            self.assertEquals(response.status, "queued")

    def test_create_message(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Local'):
            sms = SMSService()

            message = sms.create_message()
            self.assertTrue(message != None)

    def test_get_message_status(self):
        with self.settings(SMS_DAO_CLASS='restclients.dao_implementation.sms.Local'):
            sms = SMSService()

            message = sms.create_message()
            status = message.get_status()
            self.assertTrue(status, "queued")
