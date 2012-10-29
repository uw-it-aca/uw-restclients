"""
Contains SMS DAO implementations.
This abstracts the underlying SMS providers (i.e. Twilio or AWS SNS)
"""
import twilio
from twilio.rest import TwilioRestClient
from restclients.models import SMSRequest, SMSResponse
from restclients.exceptions import DataFailureException
from django.db import IntegrityError

"""
List of available live SMS providers
"""
class SMSProviders:
    Twilio, Mock = range(2)
    
"""
This implements creating a message, using a mock models.
"""
class Local(object):
    def __init__(self):
        self.ACTIVE_SMS_PROVIDER = SMSProviders.Mock
    

    def create_message(self, to = "", body = ""):
        try:
            message = SMSRequest()
            message.to = to
            message.body = body
            message.save()
            return message
        except IntegrityError as ex:
            return None

    def send_message(self, message):
        #Mock SMS Response
        response = SMSResponse()
        response.status = "queued"
        response.body = message.get_body()
        response.to = message.get_to()
        response.rid = "blahblahblah"

        return response


"""
This implements creating a message
"""
class Live(object):
    
    def __init__(self):
        #Twilio account test account that can be used without incurring msg charges
        #Twilio test numbers: http://www.twilio.com/docs/api/rest/test-credentials
        self.account_info = {'sid': 'AC749d0af386dc8c8ed5e41bdfb33a71be',
                       'token': '444e519fd9ffdfe548587a05669b6df5',
                       'from': '+15005550006'}
        #Set active SMS provider
        self.ACTIVE_SMS_PROVIDER = SMSProviders.Twilio

    def create_message(self, to = "", body = ""):
        message = SMSRequest()
        message.to = to
        message.body = body
        message.save()
        return message


    def send_message(self, message):
        response = SMSResponse()

        if self.ACTIVE_SMS_PROVIDER == 0:
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

            response.to = twilio_response.to
            response.body = twilio_response.body
            response.status = twilio_response.status
            response.rid = twilio_response.sid

            return response


    '''
    Dictionary helpers: Get value given key and run_type
    '''
    def get_value(self, key):
        """find the value given a key"""
        return self.account_info[key]
        
    
