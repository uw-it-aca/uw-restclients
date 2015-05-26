"""
Contains SMS DAO implementations.
This abstracts the underlying SMS providers (i.e. Twilio or AWS SNS)
"""
from restclients.models import SMSRequest, SMSResponse
from restclients.exceptions import DataFailureException
from restclients.dao_implementation.twilio_wrapper import Twilio
from django.db import IntegrityError
from django.core.mail import EmailMessage
from django.conf import settings


class Local(object):
    """
    This implements creating a message, using a mock models.
    """
    def create_message(self, to, body):
        try:
            message = SMSRequest()
            message.to = to
            message.body = body
            message.save()
            return message
        except IntegrityError as ex:
            return None

    def send_message(self, message):
        # Mock SMS Response
        response = SMSResponse()
        response.status = "queued"
        response.body = message.get_body()
        response.to = message.get_to()
        response.rid = "blahblahblah"

        return response


class Email(object):
    """
    This implementation sends an email with the content of the SMS, for
    testing purposes
    """
    def create_message(self, to, body):
        message = SMSRequest()
        message.to = to
        message.body = body
        return message

    def send_message(self, message):
        content = "Phone number: %s\nMessage:\n\n%s" %\
            (message.to, message.body)
        email = EmailMessage('SMS Message',
                             content,
                             settings.RESTCLIENTS_SMS_EMAIL_TO)
        email.to = [settings.RESTCLIENTS_SMS_EMAIL_TO]
        email.send()

        response = SMSResponse()
        response.to = message.to
        response.body = message.body
        response.status = "queued"
        response.rid = "email_sms"


class Live(object):
    """
    This implements creating a message
    """
    def create_message(self, to, body):
        message = SMSRequest()
        message.to = to
        message.body = body
        message.save()
        return message

    def send_message(self, message):
        provider_request = Twilio()
        provider_response = provider_request.send(message)

        response = SMSResponse()
        response.to = provider_response.to
        response.body = provider_response.body
        response.status = provider_response.status
        response.rid = provider_response.sid
        return response
