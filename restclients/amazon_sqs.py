"""
This is the interface for interacting with Amazon's Simple Queue Service.
"""

from restclients.dao import AmazonSQS_DAO


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
