'''
Created on Nov 27, 2012

@author: James Renfro
'''
from django.db import models
from django.test import TestCase
from vm.v1.viewmodels import Channel, ChannelList, ParameterDetailViewModel, Serializer

import simplejson as json
import os
 
class ChannelModel(models.Model):
    channel_id = models.CharField(max_length=36, primary_key=True)
    surrogate_id = models.CharField(max_length=140, db_index=True)
    channel_type = models.CharField(max_length=140, db_index=True)
    name = models.CharField(max_length=255, )
    template_surrogate_id = models.CharField(max_length=140)
    description = models.CharField(max_length=5000, null=True)
    expires = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    modified_by = models.CharField(max_length=80, null=True)

    class Meta:
        app_label = 'vm'
 
class ExampleChannel(object):
    
    def create(self, to_consume=True):        
        channel = Channel()
        channel.channel_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119f'
        channel.channel_uri = '/notification/v1/channel/b779df7b-d6f6-4afb-8165-8dbe6232119f'
        channel.surrogate_id = '2012,autumn,cse,100,w'
        channel.type = 'uw_student_courseavailable1'
        channel.name = 'FLUENCY IN INFORMATION TECHNOLOGY'
        channel.description = 'Introduces skills, concepts, and capabilities necessary to effectively use information technology. Includes logical reasoning, managing complexity, operation of computers and networks, and contemporary applications such as effective web searching and database manipulation, ethical aspects, and social impacts of information technology. Offered: jointly with INFO 100.\n'
        
        channel.add_tag('sln', '12345')
        channel.add_tag('quarter', 'autumn')
        channel.add_tag('year', '2012')
        
        if not to_consume:
            channel.created = '2012-11-13 21:49:07.162630+00:00'
            channel.last_modified = '2012-11-13 21:49:07.162630+00:00'
            channel.modified_by = None
            
        return channel 

    def create_alternative(self, to_consume=True):        
        
        channel = Channel()
        channel.channel_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119a'
        channel.channel_uri = '/notification/v1/channel/b779df7b-d6f6-4afb-8165-8dbe6232119a'
        channel.surrogate_id = '2014,winter,engl,240,q'
        channel.type = 'uw_student_courseavailable1'
        channel.name = 'TOPICS IN THE MODERN BRITISH NOVEL'
        channel.description = 'Virginia Woolf is great!\n'
        
        channel.add_tag('sln', '65432')
        channel.add_tag('quarter', 'winter')
        channel.add_tag('year', '2014')

        if not to_consume:
            channel.created = '2012-11-13 21:49:07.162630+00:00'
            channel.last_modified = '2012-11-13 21:49:07.162630+00:00'
            
        return channel 

    def create_from_file(self, partial=False, to_consume=True, invalid=False, alternate=False, no_id=False):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, alternate=alternate)
        channel = Channel()
        Serializer().deserialize(channel, data)
    
        return channel
    
    def get_file_content_as_string(self, partial=False, to_consume=True, invalid=False, alternate=False, no_id=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'channel_to_produce.json'
        
        if to_consume:
            filename = 'channel_to_consume.json'
            if no_id:
                filename = 'channel_to_consume_no_id.json'
            if invalid:
                filename = 'channel_to_consume_invalid.json'
            if alternate:
                filename = 'channel_to_consume_alternate.json'
        elif alternate:
            filename = 'channel_to_produce_alternate.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data

class ExampleChannelList(object):
    
    def create_from_file(self, partial=False, to_consume=True, invalid=False, verbose=False, no_id=False, alternate=False):
    
        data = self.get_file_content_as_string(partial=partial, to_consume=to_consume, invalid=invalid, verbose=verbose, no_id=no_id, alternate=alternate)
        list_view_model = ChannelList()
        Serializer().deserialize(list_view_model, data)
    
        return list_view_model
    
    def get_file_content_as_string(self, partial=False, to_consume=True, invalid=False, verbose=False, no_id=False, alternate=False):
    
        directory = os.path.join(os.path.dirname(__file__), 'resources/')
        filename = 'channel_list_to_produce.json'
        
        if verbose:
            filename = 'channel_list_to_produce_verbose.json'
        elif to_consume:
            filename = 'channel_list_to_consume.json'
            if no_id:
                filename = 'channel_list_to_consume_no_id.json'
            elif invalid:
                filename = 'channel_list_to_consume_invalid.json'
            elif alternate:
                filename = 'channel_list_to_consume_alternate.json'

        path = os.path.join(directory, filename)

        with open(path) as stream:
            data = stream.read()
            
        return data
    
class ChannelDetailViewModelTest(TestCase):

    def setUp(self):
        self.example_channel = ExampleChannel().create()

    def test_compare_same_view_model(self):

        first = ExampleChannel().create()
        second = ExampleChannel().create()
        second.created = '2012-12-13 21:49:07.162630+00:00'
        
        self.assertEqual(first, second)

    def test_compare_different_view_model(self):

        first = ExampleChannel().create()
        second = ExampleChannel().create()
        second.type = 'SOMETHING ELSE'
        
        self.assertNotEqual(first, second)
        
    def test_compare_completely_different_view_model(self):

        first = ExampleChannel().create()
        second = ExampleChannel().create_alternative()

        self.assertNotEqual(first, second)
        
    def test_compare_same_view_model_with_different_tags(self):

        first = ExampleChannel().create()
        second = ExampleChannel().create()
        second.tags.view_models[0] = ParameterDetailViewModel('sln', '123456')
        
        self.assertNotEqual(first, second)

    def test_compare_view_model_to_consume_with_view_model_to_produce(self):
        ''' 
            Although the view model we consume is different from the one we produce, 
            the fields that make them different (created/last_modified) are not
            compared in the __eq__ function
        '''
        expected = ExampleChannel().create(to_consume=True)
        actual = ExampleChannel().create(to_consume=False)
        
        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_consume(self):
        
        expected = ExampleChannel().create(to_consume=True)
        actual = ExampleChannel().create_from_file(to_consume=True)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_to_produce(self):
        
        expected = ExampleChannel().create(to_consume=False)
        actual = ExampleChannel().create_from_file(to_consume=False)

        self.assertEqual(expected, actual)

    def test_marshall_view_model_from_invalid(self):
        
        try:
            ExampleChannel().create_from_file(to_consume=True, invalid=True)
            self.fail('The expected error was not raised when trying to decode an invalid representation')
        except json.JSONDecodeError:
            pass

    def test_unmarshall_valid_view_model_to_consume(self):

        serializer = Serializer()
        
        expected = serializer.deserialize(Channel(), ExampleChannel().get_file_content_as_string(to_consume=True))
        actual = serializer.deserialize(Channel(), serializer.serialize(ExampleChannel().create(to_consume=True), partial=True))
        
        self.assertEqual(expected, actual)


    def test_unmarshall_then_marshall_with_two_channels(self):
        
        first = ExampleChannel().create(to_consume=False)
        second = ExampleChannel().create_alternative(to_consume=False)

        serializer = Serializer()

        first_serialized = serializer.serialize(first)
        second_serialized = serializer.serialize(second)
        
        first_deserialized = serializer.deserialize(Channel(), first_serialized)
        second_deserialized = serializer.deserialize(Channel(), second_serialized)

        self.assertEqual(first, first_deserialized)
        self.assertEqual(second, second_deserialized)

        first_reserialized = serializer.serialize(first_deserialized)
        second_reserialized = serializer.serialize(second_deserialized)
        
        self.assertEqual(first_serialized, first_reserialized)
        self.assertEqual(second_serialized, second_reserialized)
    
    def test_from_model(self):
        
        channel_model = ChannelModel()
        channel_model.channel_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119f'
        channel_model.name = 'FLUENCY IN INFORMATION TECHNOLOGY'
        channel_model.surrogate_id = '2012,autumn,cse,100,w'
        channel_model.channel_type = 'uw_student_courseavailable1'
        channel_model.template_surrogate_id = 'CourseAvailableNotificationTemplate'
        channel_model.description = 'Introduces skills, concepts, and capabilities necessary to effectively use information technology. Includes logical reasoning, managing complexity, operation of computers and networks, and contemporary applications such as effective web searching and database manipulation, ethical aspects, and social impacts of information technology. Offered: jointly with INFO 100.\n'
        channel_model.expires = None;
        
        view_model = Channel().from_model(channel_model)
        
        self.assertEqual(channel_model.channel_id, view_model.channel_id)
        self.assertEqual(channel_model.name, view_model.name)
        self.assertEqual(channel_model.surrogate_id, view_model.surrogate_id)
        self.assertEqual(channel_model.channel_type, view_model.type)
        #self.assertEqual(channel_model.template_surrogate_id, view_model.template_surrogate_id)
        self.assertEqual(channel_model.description, view_model.description)
        self.assertEqual(channel_model.expires, view_model.expires)
        
    def test_to_model(self):
        
        view_model = Channel()
        view_model.channel_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119f'
        view_model.name = 'FLUENCY IN INFORMATION TECHNOLOGY'
        view_model.surrogate_id = '2012,autumn,cse,100,w'
        view_model.type = 'uw_student_courseavailable1'
        view_model.template_surrogate_id = 'CourseAvailableNotificationTemplate'
        view_model.description = 'Introduces skills, concepts, and capabilities necessary to effectively use information technology. Includes logical reasoning, managing complexity, operation of computers and networks, and contemporary applications such as effective web searching and database manipulation, ethical aspects, and social impacts of information technology. Offered: jointly with INFO 100.\n'
        view_model.expires = None;
        
        channel_model = view_model.to_model(ChannelModel())
        
        self.assertEqual(channel_model.channel_id, view_model.channel_id)
        self.assertEqual(channel_model.name, view_model.name)
        self.assertEqual(channel_model.surrogate_id, view_model.surrogate_id)
        self.assertEqual(channel_model.channel_type, view_model.type)
        #self.assertEqual(channel_model.template_surrogate_id, view_model.template_surrogate_id)
        self.assertEqual(channel_model.description, view_model.description)
        self.assertEqual(channel_model.expires, view_model.expires)

