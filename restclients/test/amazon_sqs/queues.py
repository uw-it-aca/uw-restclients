from django.test import TestCase
from django.conf import settings
from restclients.amazon_sqs import AmazonSQS

class SQSQueue(TestCase):
    def test_create_and_get(self):
        with self.settings(AMAZON_SQS_DAO_CLASS='restclients.dao_implementation.amazon_sqs.Local'):
            sqs = AmazonSQS()

            queue = sqs.get_queue("test_null_get")
            self.assertEquals(queue, None, "No initial queue")

            queue = sqs.create_queue("test_queue_create")
            self.assertEquals(queue.name, "test_queue_create", "Queue has the right name")

            queue = sqs.create_queue("test_queue_create")
            self.assertEquals(queue.name, "test_queue_create", "Can create a queue with an existing name")

    def test_message_creation(self):
        with self.settings(AMAZON_SQS_DAO_CLASS='restclients.dao_implementation.amazon_sqs.Local'):
            sqs = AmazonSQS()

            queue = sqs.create_queue("sending_test_queue")
            message = queue.new_message(body="This is a message")
            queue.write(message)

            message = queue.read()
            self.assertEquals(message.get_body(), "This is a message", "Got the right message out")

            message = queue.read()
            self.assertEquals(message.get_body(), "This is a message", "Message stays in the queue until deleted")

            queue.delete_message(message)

            message = queue.read()
            self.assertEquals(message, None, "A deleted message is gone")


    def test_message_ordering(self):
        with self.settings(AMAZON_SQS_DAO_CLASS='restclients.dao_implementation.amazon_sqs.Local'):
            sqs = AmazonSQS()
            queue = sqs.create_queue("ordering_queue")

            message = queue.new_message(body="This is message #1")
            queue.write(message)
            message = queue.new_message(body="This is message #2")
            queue.write(message)
            message = queue.new_message(body="This is message #3")
            queue.write(message)

            m1 = queue.read()
            self.assertEquals(m1.get_body(), "This is message #1", "First in, first out")
            queue.delete_message(m1)

            m2 = queue.read()
            self.assertEquals(m2.get_body(), "This is message #2", "middle, middle")
            queue.delete_message(m2)

            m3 = queue.read()
            self.assertEquals(m3.get_body(), "This is message #3", "Last in, last out")
            queue.delete_message(m3)
