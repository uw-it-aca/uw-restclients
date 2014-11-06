'''
Created on Nov 27, 2012

@author: James Renfro
'''
from django.test import TestCase
from vm.v1.viewmodels import MessageType, MessageTypeList, Serializer

import simplejson as json
import os
 
class ExampleMessageType(object):
    
    def create(self, to_consume=True):
        message_type = MessageType()
        message_type.message_type_id = 'd097a66a-23bb-4b2b-bb44-01fe1d11aab0'
        #if not to_consume:
        message_type.message_type_uri = '/notification/v1/message-type/d097a66a-23bb-4b2b-bb44-01fe1d11aab0'
        message_type.surrogate_id = 'uw_student_courseavailable1'
        message_type.content_type = 'application/json'
        message_type.destination_id = 'uw_student_courseavailable1|{{ Content.Event.Section.Course.Year }},{{ Content.Event.Section.Course.Quarter }},{{ Content.Event.Section.Course.CurriculumAbbreviation }},{{ Content.Event.Section.Course.CourseNumber }},{{ Content.Event.Section.SectionID }}'
        message_type.destination_type = 'channel'
        message_type.sender = '{{ System.DispatcherName }}'
        message_type.to = '{{ Endpoint.EndpointAddress }}'
        message_type.subject = '{{ Channel.Name }}'
        message_type.body = 'Section is OPEN for: {{ Channel.Name }}'
        message_type.short = 'Section is OPEN for: {{ Channel.SurrogateID }}'
        
        if not to_consume:
            message_type.created = '2012-11-13 21:49:07.162630+00:00'
            message_type.last_modified = '2012-11-13 21:49:07.162630+00:00'
            
        return message_type 

    def create_alternative(self, to_consume=True):
        message_type = MessageType()
        message_type.message_type_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119a'
        message_type.message_type_uri = '/notification/v1/message-type/b779df7b-d6f6-4afb-8165-8dbe6232119a'
        message_type.surrogate_id = 'uw_direct_notification'
        message_type.content_type = 'application/json'
        message_type.destination_id = '{{ Content.Recipient }}'
        message_type.destination_type = 'netid'
        message_type.sender = '{{ System.DispatcherName }}'
        message_type.to = '{{ Endpoint.EndpointAddress }}'
        message_type.subject = '{{ Content.Subject }}'
        message_type.body = '{{ Content.Body }}'
        message_type.short = '{{ Content.SMSText }}'
        
        if not to_consume:
            message_type.created = '2012-11-13 21:49:07.162630+00:00'
            message_type.last_modified = '2012-11-13 21:49:07.162630+00:00'
            
        return message_type 

    def create_from_file(self, to_consume=True, invalid=False, alternate=False):
    
        data = self.get_file_content_as_string(to_consume=to_consume, invalid=invalid, alternate=alternate)
        message_type = MessageType()
        Serializer().deserialize(message_type, data)
    
        return message_type
    
    def get_file_content_as_string(self, to_consume=True, invalid=False, alternate=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'message_type_to_produce.json'
        
        if to_consume:
            filename = 'message_type_to_consume.json'
            if alternate:
                filename = 'message_type_to_consume_alternate.json'
            if invalid:
                filename = 'message_type_to_consume_invalid.json'
        else:
            filename = 'message_type_to_produce.json'
            if alternate:
                filename = 'message_type_to_produce_alternate.json'


        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data

class ExampleMessageTypeList(object):
    
    def create_from_file(self, to_consume=True, invalid=False, alternate=False):
    
        data = self.get_file_content_as_string(to_consume=to_consume, invalid=invalid, alternate=alternate)
        message_type_list = MessageTypeList()
        Serializer().deserialize(message_type_list, data)
    
        return message_type_list
    
    def get_file_content_as_string(self, to_consume=True, invalid=False, alternate=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'message_type_list_to_produce.json'
        
        if to_consume:
            filename = 'message_type_list_to_consume.json'
            if alternate:
                filename = 'message_type_list_to_consume_alternate.json'
            if invalid:
                filename = 'message_type_list_to_consume_invalid.json'
        else:
            filename = 'message_type_list_to_produce.json'
            if alternate:
                filename = 'message_type_list_to_produce_alternate.json'


        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data


class MessageTypeTest(TestCase):

    def setUp(self):
        self.example_message_type = ExampleMessageType().create()

    def test_compare_same_view_model(self):

        first = ExampleMessageType().create()
        second = ExampleMessageType().create()
        second.created = '2012-12-13 21:49:07.162630+00:00'
        
        self.assertEqual(first, second)

    def test_compare_different_view_model(self):

        first = ExampleMessageType().create()
        second = ExampleMessageType().create()
        second.subject = 'SOMETHING NEW'
        
        self.assertNotEqual(first, second)
        
    def test_compare_completely_different_view_model(self):

        first = ExampleMessageType().create()
        second = ExampleMessageType().create_alternative()

        self.assertNotEqual(first, second)

    def test_compare_view_model_to_consume_with_view_model_to_produce(self):
        ''' 
            Although the view model we consume is different from the one we produce, 
            the fields that make them different (created/last_modified) are not
            compared in the __eq__ function
        '''
        expected = ExampleMessageType().create(to_consume=True)
        actual = ExampleMessageType().create(to_consume=False)
        
        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_consume(self):
        
        serializer = Serializer()
        
        expected = serializer.deserialize(MessageType(), serializer.serialize(ExampleMessageType().create(to_consume=True), partial=True))
        actual = serializer.deserialize(MessageType(), serializer.serialize(ExampleMessageType().create_from_file(to_consume=True), partial=True))

        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_produce(self):
        
        expected = ExampleMessageType().create(to_consume=False)
        actual = ExampleMessageType().create_from_file(to_consume=False)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_from_invalid(self):
        
        try:
            ExampleMessageType().create_from_file(to_consume=True, invalid=True)
            self.fail('The expected error was not raised when trying to decode an invalid representation')
        except json.JSONDecodeError:
            pass

    def test_unmarshall_valid_view_model_to_consume(self):

        serializer = Serializer()

        expected = serializer.deserialize(MessageType(), ExampleMessageType().get_file_content_as_string(to_consume=True))
        actual = serializer.deserialize(MessageType(), Serializer().serialize(ExampleMessageType().create(to_consume=True), partial=True))

        self.assertEqual(expected, actual)
    
    def test_unmarshall_valid_view_model_to_produce(self):

        serializer = Serializer()

        expected = serializer.deserialize(MessageType(), ExampleMessageType().get_file_content_as_string(to_consume=False))
        actual = serializer.deserialize(MessageType(), Serializer().serialize(ExampleMessageType().create(to_consume=False), partial=False))

        self.assertEqual(expected, actual)

    def test_unmarshall_then_marshall_with_two_message_types(self):
        
        first = ExampleMessageType().create(to_consume=False)
        second = ExampleMessageType().create_alternative(to_consume=False)

        serializer = Serializer()

        first_serialized = serializer.serialize(first)
        second_serialized = serializer.serialize(second)
        
        first_deserialized = serializer.deserialize(MessageType(), first_serialized)
        second_deserialized = serializer.deserialize(MessageType(), second_serialized)

        self.assertEqual(first, first_deserialized)
        self.assertEqual(second, second_deserialized)

        first_reserialized = serializer.serialize(first_deserialized)
        second_reserialized = serializer.serialize(second_deserialized)
        
        self.assertEqual(first_serialized, first_reserialized)
        self.assertEqual(second_serialized, second_reserialized)
        

        