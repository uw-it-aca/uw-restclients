'''
Created on Nov 27, 2012

@author: James Renfro
'''
from django.test import TestCase
from vm.v1.viewmodels import Endpoint, EndpointList, Serializer

import simplejson as json
import os
 
class ExampleEndpoint(object):
    
    def create(self, to_consume=True, confirmed=False, format=1):
        endpoint = Endpoint()
        endpoint.endpoint_id = 'ff53f5b8-f7f9-4eae-9d8b-b92717d4b670'
        endpoint.endpoint_uri = '/notification/v1/endpoint/b779df7b-d6f6-4afb-8165-8dbe6232119f'
        endpoint.carrier = 'AT&T'
        endpoint.protocol = 'sms'
        endpoint.user = 'javerage@washington.edu'
        endpoint.owner = 'javerage@washington.edu'
        
        if not to_consume:
            endpoint.status = 'unverified'
            endpoint.created = '2012-11-13 21:49:07.162630+00:00'
            endpoint.last_modified = '2012-11-13 21:49:07.162630+00:00'
            endpoint.modified_by = None
            endpoint.active = False
        
        if format == 1:
            endpoint.endpoint_address = '+12223334444'
        elif format == 2:
            endpoint.endpoint_address = '222-333-4444'
        elif format == 3:
            endpoint.endpoint_address = '(222)333-4444'
            
        if confirmed:
            endpoint.status = 'verified'
            endpoint.active = True
            
        return endpoint 

    def create_alternative(self, to_consume=True):
        endpoint = Endpoint()
        endpoint.endpoint_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119a'
        endpoint.endpoint_uri = '/notification/v1/endpoint/b779df7b-d6f6-4afb-8165-8dbe6232119a'
        endpoint.endpoint_address = 'javerage@uw.edu'
        endpoint.protocol = 'email'
        endpoint.user = 'javerage@washington.edu'
        endpoint.owner = 'javerage@washington.edu'
                
        if not to_consume:
            endpoint.status = 'unverified'
            endpoint.created = '2012-11-13 21:49:07.162630+00:00'
            endpoint.last_modified = '2012-11-13 21:49:07.162630+00:00'
            endpoint.modified_by = None
            endpoint.active = True
            
        return endpoint 

    def create_from_file(self, to_consume=True, invalid=False, active=False, alternate=False, no_id=False):
    
        data = self.get_file_content_as_string(to_consume, invalid, active, alternate, no_id)
        endpoint = Endpoint()
        Serializer().deserialize(endpoint, data)
    
        return endpoint
    
    def get_file_content_as_string(self, to_consume=True, invalid=False, active=False, alternate=False, no_id=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'endpoint_to_produce.json'
        
        if to_consume:
            filename = 'endpoint_to_consume.json'
            if no_id:
                filename = 'endpoint_to_consume_no_id.json'
            elif alternate:
                filename = 'endpoint_to_consume_alternate.json'
            elif invalid:
                filename = 'endpoint_to_consume_invalid.json'
        elif alternate:
            filename = 'endpoint_to_produce_alternate.json'
        elif active:
            filename = 'endpoint_to_produce_active.json'
        

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data

class ExampleEndpointList(object):
    
    def create_from_file(self, to_consume=True, invalid=False, active=False):
    
        data = self.get_file_content_as_string(to_consume, invalid, active)
        endpoint = EndpointList()
        Serializer().deserialize(endpoint, data)
    
        return endpoint
    
    def get_file_content_as_string(self, to_consume=True, invalid=False, active=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'endpoint_list_to_produce.json'
        
        if to_consume:
            filename = 'endpoint_list_to_consume.json'
            if invalid:
                filename = 'endpoint_list_to_consume_invalid.json'
        elif active:
            filename = 'endpoint_list_to_produce_active.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data

class EndpointDetailViewModelTest(TestCase):

    def setUp(self):
        self.example_endpoint = ExampleEndpoint().create()

    def test_compare_same_view_model(self):

        first = ExampleEndpoint().create()
        second = ExampleEndpoint().create()
        second.created = '2012-12-13 21:49:07.162630+00:00'
        
        self.assertEqual(first, second)

    def test_compare_different_view_model(self):

        first = ExampleEndpoint().create()
        second = ExampleEndpoint().create()
        second.carrier = 'Verizon'
        
        self.assertNotEqual(first, second)
        
    def test_compare_completely_different_view_model(self):

        first = ExampleEndpoint().create()
        second = ExampleEndpoint().create_alternative()

        self.assertNotEqual(first, second)


    def test_marshall_view_model_to_consume(self):
        
        expected = ExampleEndpoint().create(to_consume=True)
        actual = ExampleEndpoint().create_from_file(to_consume=True)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_produce(self):
        
        expected = ExampleEndpoint().create(to_consume=False)
        actual = ExampleEndpoint().create_from_file(to_consume=False)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_from_invalid(self):
        
        try:
            ExampleEndpoint().create_from_file(to_consume=True, invalid=True)
            self.fail('The expected error was not raised when trying to decode an invalid representation')
        except json.JSONDecodeError:
            pass

    def test_unmarshall_valid_view_model_to_consume(self):
        serializer = Serializer()
        
        expected = Endpoint()
        serializer.deserialize(expected, ExampleEndpoint().get_file_content_as_string(to_consume=True))
        actual = ExampleEndpoint().create(to_consume=True)

        self.assertEqual(expected, actual)

    def test_unmarshall_then_marshall_with_two_endpoints(self):
        
        first = ExampleEndpoint().create(to_consume=False)
        second = ExampleEndpoint().create_alternative(to_consume=False)

        serializer = Serializer()

        first_serialized = serializer.serialize(first)
        second_serialized = serializer.serialize(second)
        
        first_deserialized = serializer.deserialize(Endpoint(), first_serialized)
        second_deserialized = serializer.deserialize(Endpoint(), second_serialized)

        self.assertEqual(first, first_deserialized)
        self.assertEqual(second, second_deserialized)

        first_reserialized = serializer.serialize(first_deserialized)
        second_reserialized = serializer.serialize(second_deserialized)
        
        self.assertEqual(first_serialized, first_reserialized)
        self.assertEqual(second_serialized, second_reserialized)
        
    def test_phone_number_format1(self):
        
        endpoint = ExampleEndpoint().create(format=1)
        self.assertEqual(0, len(endpoint.validate()))
        
        self.assertEqual("+12223334444", endpoint.get_endpoint_address())
    
    def test_phone_number_format2(self):
        
        endpoint = ExampleEndpoint().create(format=2)
        self.assertEqual(0, len(endpoint.validate()))
        
        self.assertEqual("+12223334444", endpoint.get_endpoint_address())
        
    def test_phone_number_format3(self):
        
        endpoint = ExampleEndpoint().create(format=3)
        self.assertEqual(0, len(endpoint.validate()))
        
        self.assertEqual("+12223334444", endpoint.get_endpoint_address())    
       
    def test_invalid_phone_number(self):
        
        endpoint = ExampleEndpoint().create()
        endpoint.endpoint_address = '12345678900'
        invalid_fields = endpoint.validate()
        self.assertEqual(1, len(invalid_fields))
        self.assertEqual('Invalid format for a phone number; should be one or these: +###########, ###-###-####, or (###)###-####', invalid_fields['EndpointAddress'])
       
    def test_invalid_phone_number_with_extra_characters(self):
       
        endpoint = ExampleEndpoint().create()
        endpoint.endpoint_address = '12345678<b>90</b>'
        invalid_fields = endpoint.validate()
        self.assertEqual(1, len(invalid_fields))
        self.assertEqual('Invalid format for a phone number; should be one or these: +###########, ###-###-####, or (###)###-####', invalid_fields['EndpointAddress'])

    def test_invalid_phone_number_with_infix_characters(self):
    
        endpoint = ExampleEndpoint().create()
        endpoint.endpoint_address = '+12345bbb678900'
        invalid_fields = endpoint.validate()
        self.assertEqual(1, len(invalid_fields))
        self.assertEqual('Invalid format for a phone number; should be one or these: +###########, ###-###-####, or (###)###-####', invalid_fields['EndpointAddress'])

        
    def test_invalid_phone_number_with_prefix_characters(self):
    
        endpoint = ExampleEndpoint().create()
        endpoint.endpoint_address = 'aaa:+12345678900'
        invalid_fields = endpoint.validate()
        self.assertEqual(1, len(invalid_fields))
        self.assertEqual('Invalid format for a phone number; should be one or these: +###########, ###-###-####, or (###)###-####', invalid_fields['EndpointAddress'])

    def test_invalid_phone_number_with_suffix_characters(self):
    
        endpoint = ExampleEndpoint().create()
        endpoint.endpoint_address = '+12345678900:bbb'
        invalid_fields = endpoint.validate()
        self.assertEqual(1, len(invalid_fields))
        self.assertEqual('Invalid format for a phone number; should be one or these: +###########, ###-###-####, or (###)###-####', invalid_fields['EndpointAddress'])
        
        