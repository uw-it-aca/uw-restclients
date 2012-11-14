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
        SMS_MODE needs to be configured in settings.py
        Only two options are supported either 'Test' or 'Live'
        Test - Twilio account test account that can be used without incurring msg charges but will call real Twilio APIs
        Live - Twilio account that will send REAL SMS msgs and our account WILL be charged
        '''
        self.sid = settings.SMS[settings.SMS_MODE]['sid']
        self.token = settings.SMS[settings.SMS_MODE]['token']
        self.from_number = settings.SMS[settings.SMS_MODE]['from']

    def send(self, message):
        #Using Twilio Python Library
        try:
            client = TwilioRestClient(self.sid, self.token)
            twilio_response = client.sms.messages.create(
                #Twilio requries a '+1' prepended to every SMS North America phone number
                to = "+1" + message.to,
                from_ = self.from_number,
                body = message.body)
        except twilio.TwilioRestException as e:
            raise DataFailureException(e.uri, e.status, e.msg)

        return twilio_response
