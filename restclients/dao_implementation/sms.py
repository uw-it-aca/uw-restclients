"""
Contains SMS DAO implementations.
This abstracts the underlying SMS providers (i.e. Twilio or AWS SNS)
"""
from restclients.models import MockSMS
from django.db import IntegrityError


class Local(object):
    """
    This implements sending a message, using django models.
    """
    def create_message(self):
        try:
            message = MockSMS()
            message.save()
            return message
        except IntegrityError as ex:
            return None
