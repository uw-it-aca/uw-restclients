'''
Created on Dec 10, 2012

@author: James Renfro
'''
from dateutil import parser, tz
from django.test import TestCase
from vm.v1.test.channel import ExampleChannel
from vm.v1.test.receipt import ExampleReceipt
from vm.v1.viewmodels import Message, MessageList, ReceiptList, Serializer

import simplejson as json
import os

class ExampleMessage(object):
    
    def create(self, to_consume=True, sent=True, child=False):
        channel_view_model = ExampleChannel().create(to_consume=to_consume)
        
        message = Message()
        message.message_id = 'aa53f5b8-f7f9-4eae-9d8b-b92717d4b670'
        if not to_consume:
            message.message_uri = '/notification/v1/message/aa53f5b8-f7f9-4eae-9d8b-b92717d4b670'

        message.message_type = 'uw_student_courseavailable1'
        message.direction = 'outbound'
        message.destination_type = 'channel'
        message.destination_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119f'
        message.source_id = 'ASD234232DS1'
        message.subject = 'FLUENCY IN INFORMATION TECHNOLOGY'
        message.body = 'Section is OPEN for: FLUENCY IN INFORMATION TECHNOLOGY'
        message.short = 'Section is OPEN for: 2012,autumn,cse,100,w'
        message.created = parser.parse('2012-11-13T21:49:07.162630+00:00').astimezone(tz.tzutc())
        message.last_modified = parser.parse('2012-11-13T21:49:07.162630+00:00').astimezone(tz.tzutc())
        
        if not to_consume:
            if not child:
                receipt_view_models = list()
                receipt_view_models.append(ExampleReceipt().create(to_consume=to_consume, sent=sent, child=True))
                message.receipts = ReceiptList()
                message.receipts.view_models = receipt_view_models  
            message.created = '2012-11-13 21:49:07.162630+00:00'
            message.last_modified = '2012-11-13 21:49:07.162630+00:00'
        else:
            message.receipts = None
                
        return message 
    
    def create_alternative(self, to_consume=True, directive=None):
        channel_view_model = ExampleChannel().create_alternative(to_consume)
        
        message = Message()
        message.message_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119b'
        if not to_consume:
            message.message_uri = '/notification/v1/message/b779df7b-d6f6-4afb-8165-8dbe6232119b'
        message.message_type = 'uw_student_courseavailable1'
        message.direction = 'outbound'
        message.destination_type = 'channel'
        message.destination_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119f'
        message.source_id = 'ASD234232DS2'
        message.subject = 'A DIFFERENT SUBJECT'
        message.body = 'Section is CLOSED for: FLUENCY IN INFORMATION TECHNOLOGY'
        message.short = 'Section is CLOSED for: 2012,autumn,cse,100,w'
        message.created = parser.parse('2012-11-13T21:49:07.162630+00:00').astimezone(tz.tzutc())
        message.last_modified = parser.parse('2012-11-13T21:49:07.162630+00:00').astimezone(tz.tzutc())
        
        if not to_consume:
            message.recipients = 1
            receipt_view_models = list()
            receipt_view_models.append(ExampleReceipt().create(to_consume=to_consume))
            message.receipts = ReceiptList()
            message.receipts.view_models = receipt_view_models  
            message.created = '2012-11-13 21:49:07.162630+00:00'
            message.last_modified = '2012-11-13 21:49:07.162630+00:00'
        else:
            message.receipts = None
                
        return message 
    
    def create_from_file(self, partial=False, to_consume=True, invalid=False, alternate=False, no_id=False, sent=False):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, alternate=alternate, sent=sent)
        message = Message()
        Serializer().deserialize(message, data)
    
        return message
    
    def get_file_content_as_string(self, partial=False, to_consume=True, invalid=False, alternate=False, no_id=False, sent=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'message_to_produce.json'
        
        if to_consume:
            filename = 'message_to_consume.json'

            if no_id:
                filename = 'message_to_consume_no_id.json'
            if invalid:
                filename = 'message_to_consume_invalid.json'
            if alternate:
                filename = 'message_to_consume_alternate.json'
                
        elif alternate:
            filename = 'message_to_produce_alternate.json'
        elif sent:
            filename = 'message_to_produce_sent.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data
    
    
class ExampleMessageList(object):
    
    
    def create_from_file(self, partial=False, to_consume=True, invalid=False, verbose=False, no_id=False, alternate=False, sent=False):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, verbose=verbose, no_id=no_id, alternate=alternate, sent=sent)
        list_view_model = MessageList()
        Serializer().deserialize(list_view_model, data)
    
        return list_view_model
    
    def get_file_content_as_string(self, partial=False, to_consume=True, invalid=False, verbose=False, no_id=False, alternate=False, sent=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'message_list_to_produce.json'
        
        if to_consume:
            filename = 'message_list_to_consume.json'
            if no_id:
                filename = 'message_list_to_consume_no_id.json'
            elif invalid:
                filename = 'message_list_to_consume_invalid.json'
            elif alternate:
                filename = 'message_list_to_consume_alternate.json'
        elif sent:
            filename = 'message_list_to_produce_sent.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data    
    
class MessageTest(TestCase):
    
    def setUp(self):
        self.example_channel = ExampleMessage().create()

    def test_compare_same_view_model(self):

        first = ExampleMessage().create()
        second = ExampleMessage().create()
        second.created = '2012-12-13 21:49:07.162630+00:00'
        
        #first.receipts.view_models[0].receipt_id = second.receipts.view_models[0].receipt_id
        self.assertEqual(first, second)

    def test_compare_different_view_model(self):

        first = ExampleMessage().create()
        second = ExampleMessage().create()
        second.message_type = 'SOMETHING ELSE'
        #first.receipts.view_models[0].receipt_id = second.receipts.view_models[0].receipt_id
        
        self.assertNotEqual(first, second)
        
    def test_compare_completely_different_view_model(self):

        first = ExampleMessage().create()
        second = ExampleMessage().create_alternative()
#        first.receipts.view_models[0].receipt_id = second.receipts.view_models[0].receipt_id
        
        self.assertNotEqual(first, second)

#    def test_marshall_view_model_to_consume(self):
#        
#        expected = ExampleMessage().create(to_consume=True)
#        actual = ExampleMessage().create_from_file(to_consume=True)
#        expected.message_id = actual.message_id
#        
#        self.assertEqual(expected, actual)

#    def test_marshall_view_model_to_produce_unsent(self):
#        
#        directive = 'wait'
#        
#        expected = ExampleMessage().create(to_consume=False, sent=False, directive=directive)
#        actual = ExampleMessage().create_from_file(to_consume=False, sent=False, directive=directive)
#        
#        # Need to do some fiddling here to avoid the generated stuff
#        expected.message_id = actual.message_id
#        expected.receipts.view_models[0].receipt_id = actual.receipts.view_models[0].receipt_id
#        expected.receipts.view_models[0].delivered_on = actual.receipts.view_models[0].delivered_on
#        
#        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_produce_sent(self):
        
        expected = ExampleMessage().create(to_consume=False, sent=True)
        actual = ExampleMessage().create_from_file(to_consume=False, sent=True)
        
        # Need to do some fiddling here to avoid the generated stuff
        expected.message_id = actual.message_id
        #expected.receipts.view_models[0].receipt_id = actual.receipts.view_models[0].receipt_id
        
        self.assertEqual(expected, actual)

    def test_marshall_view_model_from_invalid(self):
        
        try:
            ExampleMessage().create_from_file(to_consume=True, invalid=True)
            self.fail('The expected error was not raised when trying to decode an invalid representation')
        except json.JSONDecodeError:
            pass

    def test_unmarshall_valid_view_model_to_consume(self):

        serializer = Serializer()

        expected = serializer.deserialize(Message(), ExampleMessage().get_file_content_as_string(to_consume=True))
        actual = serializer.deserialize(Message(), Serializer().serialize(ExampleMessage().create(to_consume=True), partial=True))
        
        self.assertEqual(expected, actual)
        
#    def test_unmarshall_valid_view_model_to_produce(self):
#
#        expected = ExampleMessage().get_file_content_as_string(to_consume=False)
#        actual = Serializer().serialize(ExampleMessage().create(to_consume=False), partial=True)
#
#        self.assertEqual(expected, actual)

    def test_unmarshall_then_marshall_with_two_messages(self):
        
        first = ExampleMessage().create(to_consume=False)
        second = ExampleMessage().create_alternative(to_consume=False)

        serializer = Serializer()

        first_serialized = serializer.serialize(first)
        second_serialized = serializer.serialize(second)
        
        first_deserialized = serializer.deserialize(Message(), first_serialized, force_consume=True)
        second_deserialized = serializer.deserialize(Message(), second_serialized, force_consume=True)

        self.assertEqual(first, first_deserialized)
        self.assertEqual(second, second_deserialized)

    
    
    
    
    
    
    
    
    
    