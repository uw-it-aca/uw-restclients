'''
Created on Dec 17, 2012

@author: James Renfro
'''
from django.test import TestCase
from vm.v1.viewmodels import *
from vm.v1.test.channel import ExampleChannel
from vm.v1.test.message import ExampleMessage
from vm.v1.test.receipt import ExampleReceipt

import os
     
class ExampleDispatch(object):
    
    def create(self, to_consume=True):
        
        channel_view_model = ExampleChannel().create(to_consume=to_consume)
        
        dispatch_view_model = Dispatch()
        dispatch_view_model.dispatch_id = 'aa53f5b8-f7f9-4eae-9d8b-b92717d4b670'
        if not to_consume:
            dispatch_view_model.dispatch_uri = '/notification/v1/dispatch/aa53f5b8-f7f9-4eae-9d8b-b92717d4b670'
        dispatch_view_model.directive = "queue"
        dispatch_view_model.destination_id = channel_view_model.channel_id
        dispatch_view_model.destination_type = 'channel'
        dispatch_view_model.locked = False
        
        if not to_consume:
            dispatch_view_model.message.message_id = None
            dispatch_view_model.message.message_uri = None
            dispatch_view_model.message = ExampleMessage().create(to_consume=to_consume, child=True)
            dispatch_view_model.message.created = None
            dispatch_view_model.message.last_modified = None
      
            dispatch_view_model.recipients = 1
            dispatch_view_model.created = '2012-11-13 21:49:07.162630+00:00'
            dispatch_view_model.last_modified = '2012-11-13 21:49:07.162630+00:00'

        return dispatch_view_model
    
    def create_alternative(self, to_consume=True):
        
        channel_view_model = ExampleChannel().create_alternative(to_consume)
        
        receipt_view_models = list()
        receipt_view_models.append(ExampleReceipt().create(to_consume=to_consume))
        
        dispatch_view_model = Dispatch()
        dispatch_view_model.dispatch_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119b'
        dispatch_view_model.dispatch_uri = '/notification/v1/dispatch/b779df7b-d6f6-4afb-8165-8dbe6232119b'
        dispatch_view_model.destination_id = channel_view_model.channel_id
        dispatch_view_model.destination_type = 'channel'
        dispatch_view_model.message = ExampleMessage().create(to_consume=False)
        
#        dispatch_view_model.receipts = ReceiptList()
#        dispatch_view_model.receipts.view_models = receipt_view_models
        
        if not to_consume:
            dispatch_view_model.created = '2012-11-13 21:49:07.162630+00:00'
            dispatch_view_model.last_modified = '2012-11-13 21:49:07.162630+00:00'

        return dispatch_view_model
    
    def create_from_file(self, partial=False, to_consume=True, invalid=False, alternate=False, no_id=False, directive=None):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, alternate=alternate, directive=directive)
        dispatch = Dispatch()
        Serializer().deserialize(dispatch, data)
    
        return dispatch
    
    def get_file_content_as_string(self, partial=False, to_consume=True, invalid=False, alternate=False, no_id=False, directive=None):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'dispatch_to_produce.json'
        
        if to_consume:
            filename = 'dispatch_to_consume.json'
            if directive is not None:
                filename = 'dispatch_to_consume_' + directive + '.json' 
            else:
                if no_id:
                    filename = 'dispatch_to_consume_no_id.json'
                if invalid:
                    filename = 'dispatch_to_consume_invalid.json'
                if alternate:
                    filename = 'dispatch_to_consume_alternate.json'
        elif directive is not None:
            filename = 'dispatch_to_produce_' + directive + '.json'
        elif alternate:
            filename = 'dispatch_to_produce_alternate.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data
    
class ExampleDispatchList(object):
    
    
    def create_from_file(self, partial=False, to_consume=True, invalid=False, verbose=False, no_id=False, alternate=False):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, verbose=verbose, no_id=no_id, alternate=alternate)
        list_view_model = DispatchList()
        Serializer().deserialize(list_view_model, data)
    
        return list_view_model
    
    def get_file_content_as_string(self, partial=False, to_consume=True, invalid=False, verbose=False, no_id=False, alternate=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'dispatch_list_to_produce.json'
        
        if to_consume:
            filename = 'dispatch_list_to_consume.json'
            if no_id:
                filename = 'dispatch_list_to_consume_no_id.json'
            elif invalid:
                filename = 'dispatch_list_to_consume_invalid.json'
            elif alternate:
                filename = 'dispatch_list_to_consume_alternate.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data
    
class DispatchDetailViewModelTest(TestCase):
    
    def setUp(self):
        self.example_channel = ExampleDispatch().create()

    def test_compare_same_view_model(self):

        first = ExampleDispatch().create()
        second = ExampleDispatch().create()
        second.created = '2012-12-13 21:49:07.162630+00:00'
        
        #first.receipts.view_models[0].receipt_id = second.receipts.view_models[0].receipt_id
        self.assertEqual(first, second)

    def test_compare_different_view_model(self):

        first = ExampleDispatch().create()
        second = ExampleDispatch().create()
        second.destination_type = 'SOMETHING ELSE'
        #first.receipts.view_models[0].receipt_id = second.receipts.view_models[0].receipt_id
        
        self.assertNotEqual(first, second)
        
    def test_compare_completely_different_view_model(self):

        first = ExampleDispatch().create()
        second = ExampleDispatch().create_alternative()
#        first.receipts.view_models[0].receipt_id = second.receipts.view_models[0].receipt_id
        
        self.assertNotEqual(first, second)

    def test_marshall_view_model_to_consume(self):
        
        expected = ExampleDispatch().create(to_consume=True)
        actual = ExampleDispatch().create_from_file(to_consume=True)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_produce(self):
        
        expected = ExampleDispatch().create(to_consume=False)
        actual = ExampleDispatch().create_from_file(to_consume=False)
        
        # Need to do some fiddling here to avoid the generated stuff
        expected.message.message_id = None
        expected.receipts.view_models[0].receipt_id = actual.receipts.view_models[0].receipt_id
        
        self.assertEqual(expected, actual)

    def test_marshall_view_model_from_invalid(self):
        
        try:
            ExampleDispatch().create_from_file(to_consume=True, invalid=True)
            self.fail('The expected error was not raised when trying to decode an invalid representation')
        except json.JSONDecodeError:
            pass

    def test_unmarshall_valid_view_model_to_consume(self):

        expected = ExampleDispatch().get_file_content_as_string(to_consume=True)
        actual = Serializer().serialize(ExampleDispatch().create(to_consume=True), partial=True)
        
        self.assertEqual(expected, actual)
        
#    def test_unmarshall_valid_view_model_to_produce(self):
#
#        expected = ExampleDispatch().get_file_content_as_string(to_consume=False)
#        actual = Serializer().serialize(ExampleDispatch().create(to_consume=False), partial=True)
#
#        self.assertEqual(expected, actual)

    def test_unmarshall_then_marshall_with_two_dispatches(self):
        
        first = ExampleDispatch().create(to_consume=False)
        second = ExampleDispatch().create_alternative(to_consume=False)

        serializer = Serializer()

        first_serialized = serializer.serialize(first)
        second_serialized = serializer.serialize(second)
        
        first_deserialized = serializer.deserialize(Dispatch(), first_serialized)
        second_deserialized = serializer.deserialize(Dispatch(), second_serialized)

        self.assertEqual(first, first_deserialized)
        self.assertEqual(second, second_deserialized)

        first_reserialized = serializer.serialize(first_deserialized)
        second_reserialized = serializer.serialize(second_deserialized)
        
        self.assertEqual(first_serialized, first_reserialized)
        self.assertEqual(second_serialized, second_reserialized)
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     

