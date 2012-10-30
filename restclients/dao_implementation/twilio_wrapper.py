'''
This serves as the Twilio wrapper class
'''
import twilio
from twilio.rest import TwilioRestClient
from restclients.exceptions import DataFailureException

class Twilio(object):
    def __init__(self):
            #Twilio account test account that can be used without incurring msg charges
            #Twilio test numbers: http://www.twilio.com/docs/api/rest/test-credentials
            self.account_info = {'sid': 'AC749d0af386dc8c8ed5e41bdfb33a71be',
                           'token': '444e519fd9ffdfe548587a05669b6df5',
                           'from': '+15005550006'}

    def send(self, message):
        #Using Twilio Python Library
        try:
            client = TwilioRestClient(self.get_value('sid'),
                                               self.get_value('token'))

            twilio_response = client.sms.messages.create(
                #Twilio requries a '+1' prepended to every SMS North America phone number
                to = "+1" + message.to, 
                from_ = self.get_value('from'),
                body = message.body)
        except twilio.TwilioRestException as e:
            raise DataFailureException(e.uri, e.status, e.msg)

        return twilio_response
    
    '''
    Dictionary helpers: Get value given key and run_type
    '''
    def get_value(self, key):
        """find the value given a key"""
        return self.account_info[key]