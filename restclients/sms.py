"""
This is the interface for interacting with a SMS service.
"""

from restclients.dao import SMS_DAO


class SMSService(object):
    """
    The AmazonSQS class has methods for getting/creating queues.
    """
    def create_message(self):
        """
        This will send a SMS message with a body.
        """
        dao = SMS_DAO()
        return dao.create_message()
