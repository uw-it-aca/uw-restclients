"""
Contains Amazon SWS DAO implementations.
"""
from restclients.models import MockAmazonSQSQueue
from boto.sqs.connection import SQSConnection
from boto.sqs.message import RawMessage
from django.db import IntegrityError
from django.conf import settings


class Local(object):
    """
    This implements a local queue, using django models.
    """
    def create_queue(self, queue_name):
        try:
            queue = MockAmazonSQSQueue(name=queue_name)
            queue.save()
            return queue
        except IntegrityError as ex:
            return self.get_queue(queue_name)

    def get_queue(self, queue_name):
        queues = MockAmazonSQSQueue.objects.filter(name=queue_name)
        if len(queues):
            return queues[0]

        return None


class Live(object):
    """
    This implements a connection to the Amazon SQS service.  Requires the
    following configuration:

    AMAZON_AWS_ACCESS_KEY
    AMAZON_AWS_SECRET_KEY
    """

    def create_queue(self, queue_name):
        conn = self._get_connection()
        return conn.create_queue(queue_name)

    def get_queue(self, queue_name):
        conn = self._get_connection()
        return conn.get_queue(queue_name)

    def _get_connection(self):
        access_key = settings.AMAZON_AWS_ACCESS_KEY
        secret_key = settings.AMAZON_AWS_SECRET_KEY

        conn = SQSConnection(access_key, secret_key)
        return conn
