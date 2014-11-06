'''
Created on Nov 27, 2012

@author: James Renfro
'''
from dateutil import parser, tz
from django.test import TestCase
from vm.v1.viewmodels import EndpointList, Person, PersonList, Serializer

import simplejson as json
import os
 
class ExamplePerson(object):
    
    def create(self, to_consume=True):
        person = Person()
        person.person_id = '9136CCB8F66711D5BE060004AC494FFE'
        person.person_uri = '/notification/v1/person/9136CCB8F66711D5BE060004AC494FFE'
        person.surrogate_id = 'javerage@washington.edu'
        person.add_attribute("AcceptedTermsOfUse", None, None, False)
        
        person.default_endpoint_id = None
        
        if not to_consume:
            person.add_attribute("DispatchedEmailCount", None, 0, None)
            person.add_attribute("DispatchedTextMessageCount", None, 0, None)
            person.add_attribute("SentTextMessageCount", None, 0, None)
            person.add_attribute("SubscriptionCount", None, 0, None)
            person.endpoints = EndpointList()
            person.created = parser.parse('2012-11-13 21:49:07.162630+00:00').astimezone(tz.tzutc())
            person.last_modified = parser.parse('2012-11-13 21:49:07.162630+00:00').astimezone(tz.tzutc())
            person.modified_by = None
            
        return person 

    def create_alternative(self, to_consume=True):
        person = Person()
        person.person_id = '9136CCB8F66711D5BE060004AC494FFE'
        person.person_uri = '/notification/v1/person/9136CCB8F66711D5BE060004AC494FFE'
        person.surrogate_id = 'jnotaverage@washington.edu'
        person.default_endpoint_id = None
        person.add_attribute("AcceptedTermsOfUse", None, None, False)
        
        if not to_consume:
            person.add_attribute("DispatchedEmailCount", None, 0, None)
            person.add_attribute("DispatchedTextMessageCount", None, 0, None)
            person.add_attribute("SentTextMessageCount", None, 0, None)
            person.add_attribute("SubscriptionCount", None, 0, None)
            person.endpoints = EndpointList()
            person.created = parser.parse('2012-11-13 21:49:07.162630+00:00').astimezone(tz.tzutc())
            person.last_modified = parser.parse('2012-11-13 21:49:07.162630+00:00').astimezone(tz.tzutc())
            person.modified_by = None
            
        return person 

    def create_from_file(self, to_consume=True, invalid=False, active=False, alternate=False):
    
        data = self.get_file_content_as_string(to_consume, invalid, active, alternate)
        person = Person()
        Serializer().deserialize(person, data)
    
        return person
    
    def get_file_content_as_string(self, to_consume=True, invalid=False, active=False, alternate=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'person_to_produce.json'
        
        if to_consume:
            filename = 'person_to_consume.json'
            if alternate:
                filename = 'person_to_consume_alternate.json'
            elif invalid:
                filename = 'person_to_consume_invalid.json'
        elif alternate:
            filename = 'person_to_produce_alternate.json'        

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data

class ExamplePersonList(object):
    
    def create_from_file(self, to_consume=True, invalid=False, active=False):
    
        data = self.get_file_content_as_string(to_consume, invalid, active)
        person = PersonList()
        Serializer().deserialize(person, data)
    
        return person
    
    def get_file_content_as_string(self, to_consume=True, invalid=False, active=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'person_list_to_produce.json'
        
        if to_consume:
            filename = 'person_list_to_consume.json'
            if invalid:
                filename = 'person_list_to_consume_invalid.json'
        elif active:
            filename = 'person_list_to_produce_active.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data

class PersonTest(TestCase):

    def setUp(self):
        self.example_person = ExamplePerson().create()

    def test_compare_same_view_model(self):

        first = ExamplePerson().create()
        second = ExamplePerson().create()
        
        self.assertEqual(first, second)

    def test_compare_different_view_model(self):

        first = ExamplePerson().create()
        second = ExamplePerson().create_alternative()
        
        self.assertNotEqual(first, second)
        
    def test_marshall_view_model_to_consume(self):
        
        expected = ExamplePerson().create(to_consume=True)
        actual = ExamplePerson().create_from_file(to_consume=True)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_produce(self):
        
        expected = ExamplePerson().create(to_consume=False)
        actual = ExamplePerson().create_from_file(to_consume=False)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_from_invalid(self):
        
        try:
            ExamplePerson().create_from_file(to_consume=True, invalid=True)
            self.fail('The expected error was not raised when trying to decode an invalid representation')
        except json.JSONDecodeError:
            pass

    def test_unmarshall_valid_view_model_to_consume(self):
        serializer = Serializer()
        
        expected = Person()
        serializer.deserialize(expected, ExamplePerson().get_file_content_as_string(to_consume=True))
        actual = ExamplePerson().create(to_consume=True)

        self.assertEqual(expected, actual)
    
    def test_unmarshall_then_marshall_with_two_persons(self):
        
        first = ExamplePerson().create(to_consume=False)
        second = ExamplePerson().create_alternative(to_consume=False)

        serializer = Serializer()

        first_serialized = serializer.serialize(first)
        second_serialized = serializer.serialize(second)
        
        first_deserialized = serializer.deserialize(Person(), first_serialized)
        second_deserialized = serializer.deserialize(Person(), second_serialized)

        self.assertEqual(first, first_deserialized)
        self.assertEqual(second, second_deserialized)

        first_reserialized = serializer.serialize(first_deserialized)
        second_reserialized = serializer.serialize(second_deserialized)
        
        self.assertEqual(first_serialized, first_reserialized)
        self.assertEqual(second_serialized, second_reserialized)
        
    def test_validate(self):

        person = ExamplePerson().create()
        
        errors = person.validate()
        
        self.assertEqual(0, len(errors))
        
        
        