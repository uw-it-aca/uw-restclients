'''
Created on Nov 27, 2012

@author: James Renfro
'''
from django.test import TestCase

from vm.v1.viewmodels import Channel, Endpoint, Subscription, Serializer

import simplejson as json
import os

class ExampleSubscription(object):
    
    def create(self, partial=True, to_consume=True):
        channel = Channel()
        channel.channel_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119f'
        
        if not partial:
            channel.channel_uri = '/notification/v1/channel/b779df7b-d6f6-4afb-8165-8dbe6232119f'
            channel.surrogate_id = '2012,autumn,cse,100,w'
            channel.type = 'uw_student_courseavailable1'
            channel.name = 'FLUENCY IN INFORMATION TECHNOLOGY'
            channel.template_surrogate_id = 'CourseAvailableNotificationTemplate'
            channel.description = 'Introduces skills, concepts, and capabilities necessary to effectively use information technology. Includes logical reasoning, managing complexity, operation of computers and networks, and contemporary applications such as effective web searching and database manipulation, ethical aspects, and social impacts of information technology. Offered: jointly with INFO 100.\n'
        
        endpoint = Endpoint()
        endpoint.endpoint_id = 'ff53f5b8-f7f9-4eae-9d8b-b92717d4b670'
        
        if not partial:
            endpoint.endpoint_uri = '/notification/v1/endpoint/ff53f5b8-f7f9-4eae-9d8b-b92717d4b670'
            endpoint.endpoint_address = '+12223334444'
            endpoint.carrier = 'AT&T'
            endpoint.protocol = 'sms'
            endpoint.user = 'javerage@washington.edu'
            endpoint.owner = 'javerage@washington.edu'
            endpoint.status = 'unverified'
            endpoint.active = True
            endpoint.default = True
        
        subscription = Subscription()
        subscription.subscription_id = '6c9cd13c-10df-4f34-9023-d5e7316005c9'
        subscription.subscription_uri = '/notification/v1/subscription/6c9cd13c-10df-4f34-9023-d5e7316005c9'
#        subscription.subscription_type = 'Individual'
        subscription.channel = channel
        subscription.endpoint = endpoint
        
        if not to_consume:
            subscription.created = '2012-10-13 21:49:07.162630+00:00'
            subscription.last_modified = '2012-11-13 11:49:07.162630+00:00'
        
        return subscription
    
    def create_from_file(self, partial=True, to_consume=True, invalid=False, alternate=False):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, alternate=alternate)
        subscription = Subscription()
        Serializer().deserialize(subscription, data)
    
        return subscription
    
    def get_file_content_as_stream(self, partial=True, to_consume=True, invalid=False, alternate=False, no_id=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'subscription_to_produce.json'
        
        if to_consume:
            filename = 'subscription_to_consume.json'
            if alternate:
                filename = 'subscription_to_consume_alternate.json'
            elif no_id:
                filename = 'subscription_to_consume_no_id.json'
        else:
            if alternate:
                filename = 'subscription_to_produce_alternate.json'
            
        if partial:
            filename = 'subscription_to_consume_partial.json'
        if invalid:
            filename = 'subscription_to_consume_invalid.json'

        path = os.path.join(directory, filename)

        return open(path)
    
    def get_file_content_as_string(self, partial=True, to_consume=True, invalid=False, alternate=False, no_id=False):
    
        stream = self.get_file_content_as_stream(partial=partial, to_consume=to_consume, invalid=invalid, alternate=alternate, no_id=no_id)
        data = stream.read()
        stream.close()
        
        return data
 
class ExampleSubscriptionList(object):
    
    def create_from_file(self, partial=True, to_consume=True, invalid=False, alternate=False):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, alternate=alternate)
        subscription = Subscription()
        Serializer().deserialize(subscription, data)
    
        return subscription
    
    def get_file_content_as_stream(self, partial=True, to_consume=True, invalid=False, alternate=False, no_id=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'subscription_list_to_produce.json'
        
        if to_consume:
            filename = 'subscription_list_to_consume.json'
            if alternate:
                filename = 'subscription_list_to_consume_alternate.json'
            elif no_id:
                filename = 'subscription_list_to_consume_no_id.json'
        else:
            if alternate:
                filename = 'subscription_list_to_produce_alternate.json'
            
        if partial:
            filename = 'subscription_list_to_consume_partial.json'
        if invalid:
            filename = 'subscription_list_to_consume_invalid.json'

        path = os.path.join(directory, filename)

        return open(path)
    
    def get_file_content_as_string(self, partial=True, to_consume=True, invalid=False, alternate=False, no_id=False):
    
        stream = self.get_file_content_as_stream(partial=partial, to_consume=to_consume, invalid=invalid, alternate=alternate, no_id=no_id)
        data = stream.read()
        stream.close()
        
        return data
       

class SubscriptionDetailViewModelTest(TestCase):

    def test_compare_same_view_model(self):

        expected = ExampleSubscription().create()
        actual = ExampleSubscription().create()
        actual.created = '2012-12-13 21:49:07.162630+00:00'
        
        self.assertEqual(expected, actual)

    def test_compare_different_view_model(self):

        expected = ExampleSubscription().create()
        actual = ExampleSubscription().create()
        actual.subscription_type = 'Group'
        
        self.assertNotEqual(expected, actual)
   
    def test_compare_same_view_model_with_different_endpoint_details(self):

        expected = ExampleSubscription().create(partial=False)
        actual = ExampleSubscription().create(partial=False)
        actual.endpoint.endpoint_address = 'javerage@uw.edu'
        
        self.assertNotEqual(expected, actual)     
       
    def test_compare_view_model_to_consume_with_view_model_to_produce(self):
        ''' 
            Although the view model we consume is different from the one we produce, 
            the fields that make them different (created/last_modified) are not
            compared in the __eq__ function
        '''
        expected = ExampleSubscription().create(partial=False, to_consume=True)
        actual = ExampleSubscription().create(partial=False, to_consume=False)
        
        self.assertEqual(expected, actual)
        
    def test_compare_full_view_model_to_consume_with_partial(self):

        expected = ExampleSubscription().create(partial=False)
        actual = ExampleSubscription().create(partial=True)
        
        self.assertNotEqual(expected, actual)
        
    def test_compare_full_view_model_to_produce_with_partial(self):

        expected = ExampleSubscription().create(partial=False, to_consume=False)
        actual = ExampleSubscription().create(partial=True, to_consume=False)
        
        self.assertNotEqual(expected, actual)

    def test_marshall_view_model_to_consume(self):
        
        expected = ExampleSubscription().create(partial=True, to_consume=True)
        actual = ExampleSubscription().create_from_file(partial=True, to_consume=True)

        self.assertEqual(expected, actual)
        
    def test_marshall_view_model_to_produce(self):
        
        expected = ExampleSubscription().create(partial=False, to_consume=False)
        actual = ExampleSubscription().create_from_file(partial=False, to_consume=False)

        self.assertEqual(expected, actual)
      
    def test_marshall_view_model_from_invalid(self):
        
        try:
            ExampleSubscription().create_from_file(partial=True, to_consume=True, invalid=True)
            self.fail('The expected error was not raised when trying to decode an invalid representation')
        except json.JSONDecodeError:
            pass

    def test_unmarshall_valid_view_model_to_consume(self):
        serializer = Serializer()
        
        expected = serializer.deserialize(Subscription(), ExampleSubscription().get_file_content_as_string(partial=True, to_consume=True))
        actual = serializer.deserialize(Subscription(), serializer.serialize(ExampleSubscription().create(partial=True, to_consume=True), partial=True))
        
        self.assertEqual(expected, actual)
    
    def test_unmarshall_valid_view_model_to_produce(self):
        serializer = Serializer()
        
        expected = serializer.deserialize(Subscription(), ExampleSubscription().get_file_content_as_string(partial=False, to_consume=False))
        actual = serializer.deserialize(Subscription(), serializer.serialize(ExampleSubscription().create(partial=False, to_consume=False), partial=False))

        self.assertEqual(expected, actual)   
        
        