"""
This is the interface for interacting with Amazon's Simple Queue Service.
"""
from restclients.dao import AmazonSQS_DAO
from boto.sqs.message import RawMessage
from django.conf import settings

class AmazonSQS(object):
    """
    The AmazonSQS class has methods for getting/creating queues.
    """
    def create_queue(self, queue_name):
        """
        This will create a new queue, or return an existing queue with the
        given name.
        """
        dao = AmazonSQS_DAO()
        return dao.create_queue(queue_name)

    def get_queue(self, queue_name):
        dao = AmazonSQS_DAO()
        return dao.get_queue(queue_name)

    def read_queue(self):
        """
        This is responsible for reading events off the queue, and sending
        notifications to users, via email or SMS.
        The following are necessary for AWS access:
        RESTCLIENTS_AMAZON_AWS_ACCESS_KEY
        RESTCLIENTS_AMAZON_AWS_SECRET_KEY
        RESTCLIENTS_AMAZON_QUEUE - the AWS Queue name you want to read events
        from
        RESTCLIENTS_AMAZON_SQS_DAO_CLASS
        """
        queue = AmazonSQS().create_queue(settings.RESTCLIENTS_AMAZON_QUEUE)
        queue.set_message_class(RawMessage)
        message = queue.read()
        if message is None:
            return

        body = message.get_body()
        queue.delete_message(message)
        return body
