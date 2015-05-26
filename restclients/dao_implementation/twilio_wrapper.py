'''
This serves as the Twilio wrapper class
'''
import twilio
from twilio.rest import TwilioRestClient
from restclients.exceptions import DataFailureException
from django.conf import settings


class Twilio(object):
    def __init__(self):
        '''
        RESTCLIENTS_SMS_MODE needs to be configured in settings.py.
        RESTCLIENTS_SMS_MODE allows you to have multiple configuration
        in your settings.py file, such as 'Test'
        or 'Live'.  For 'Live', your settings.py should include this:

        RESTCLIENTS_SMS_ACCOUNT = {
            'Live': {
                "sid": <your twilio sid>,
                "token": <your twilio token>,
                "from": <your from number>,
            }
        }
        '''
        self.sid = settings.RESTCLIENTS_SMS_ACCOUNT[
            settings.RESTCLIENTS_SMS_MODE]['sid']
        self.token = settings.RESTCLIENTS_SMS_ACCOUNT[
            settings.RESTCLIENTS_SMS_MODE]['token']
        self.from_number = settings.RESTCLIENTS_SMS_ACCOUNT[
            settings.RESTCLIENTS_SMS_MODE]['from']

    def send(self, message):
        # Using Twilio Python Library
        try:
            client = TwilioRestClient(self.sid, self.token)
            twilio_response = client.sms.messages.create(
                to="+1" + message.to,
                from_=self.from_number,
                body=message.body)
            # Twilio requries a '+1' prepended to every
            # SMS North America phone number
        except twilio.TwilioRestException as e:
            raise DataFailureException(e.uri, e.status, e.msg)

        return twilio_response
