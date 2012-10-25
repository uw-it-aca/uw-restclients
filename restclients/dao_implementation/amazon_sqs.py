"""
Contains Amazon SWS DAO implementations.
"""
from restclients.models import MockAmazonSQSQueue
from django.db import IntegrityError


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
