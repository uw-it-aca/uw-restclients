#'''
#Created on Nov 27, 2012
#
#@author: James Renfro
#'''
#from django.test import TestCase
#from vm.v1.viewmodels import TemplateDetailViewModel, Serializer
#
#import simplejson as json
#import os
# 
#class ExampleTemplate(object):
#    
#    def create(self, to_consume=True):
#        template = TemplateDetailViewModel()
#        template.template_id = 'd097a66a-23bb-4b2b-bb44-01fe1d11aab0'
#        #if not to_consume:
#        template.template_uri = '/notification/v1/template/d097a66a-23bb-4b2b-bb44-01fe1d11aab0'
#        template.template_surrogate_id = 'CourseAvailableNotificationTemplate'
#        template.subject = '{{channel.name}}'
#        template.brief = 'Section is {{ event.status }} for: {{ channel.surrogate_id }}'
#        template.extensive = 'Section is {{ event.status }} for your section. Year: {{ event.year }} Quarter: {{ event.quarter }} Course Title: {{ channel.name }} Curriculum: {{ event.curriculum }} Course Number: {{ event.course_number }} Section ID: {{ event.section_id }} Course Description: {{ channel.description }}'
#        
#        if not to_consume:
#            template.created = '2012-11-13 21:49:07.162630+00:00'
#            template.last_modified = '2012-11-13 21:49:07.162630+00:00'
#            
#        return template 
#
#    def create_alternative(self, to_consume=True):
#        template = TemplateDetailViewModel()
#        template.template_id = 'b779df7b-d6f6-4afb-8165-8dbe6232119a'
#        #if not to_consume:
#        template.template_uri = '/notification/v1/template/b779df7b-d6f6-4afb-8165-8dbe6232119a'
#        template.template_surrogate_id = 'CourseAvailableNotificationTemplate'
#        template.subject = '{{channel.name}}'
#        template.brief = 'There''s a space available!'
#        template.extensive = 'Section is {{ event.status }} for your section. Year: {{ event.year }} Quarter: {{ event.quarter }} Course Title: {{ channel.name }} Curriculum: {{ event.curriculum }} Course Number: {{ event.course_number }} Section ID: {{ event.section_id }} Course Description: {{ channel.description }}'
#        
#        if not to_consume:
#            template.created = '2012-11-13 21:49:07.162630+00:00'
#            template.last_modified = '2012-11-13 21:49:07.162630+00:00'
#            
#        return template 
#
#    def create_from_file(self, to_consume=True, invalid=False, alternate=False):
#    
#        data = self.get_file_content_as_string(to_consume=to_consume, invalid=invalid, alternate=alternate)
#        template = TemplateDetailViewModel()
#        Serializer().deserialize(template, data)
#    
#        return template
#    
#    def get_file_content_as_string(self, to_consume=True, invalid=False, alternate=False):
#    
#        directory = os.path.join(os.path.dirname(__file__), 'resources/')
#        filename = 'template_to_produce.json'
#        
#        if to_consume:
#            filename = 'template_to_consume.json'
#            if alternate:
#                filename = 'template_to_consume_alternate.json'
#            if invalid:
#                filename = 'template_to_consume_invalid.json'
#        else:
#            filename = 'template_to_produce.json'
#            if alternate:
#                filename = 'template_to_produce_alternate.json'
#
#
#        path = os.path.join(directory, filename)
#
#        with open(path) as stream:
#            data = stream.read()
#            
#        return data
#
#class TemplateDetailViewModelTest(TestCase):
#
#    def setUp(self):
#        self.example_template = ExampleTemplate().create()
#
#    def test_compare_same_view_model(self):
#
#        first = ExampleTemplate().create()
#        second = ExampleTemplate().create()
#        second.created = '2012-12-13 21:49:07.162630+00:00'
#        
#        self.assertEqual(first, second)
#
#    def test_compare_different_view_model(self):
#
#        first = ExampleTemplate().create()
#        second = ExampleTemplate().create()
#        second.brief = 'SOMETHING NEW'
#        
#        self.assertNotEqual(first, second)
#        
#    def test_compare_completely_different_view_model(self):
#
#        first = ExampleTemplate().create()
#        second = ExampleTemplate().create_alternative()
#
#        self.assertNotEqual(first, second)
#
#    def test_compare_view_model_to_consume_with_view_model_to_produce(self):
#        ''' 
#            Although the view model we consume is different from the one we produce, 
#            the fields that make them different (created/last_modified) are not
#            compared in the __eq__ function
#        '''
#        expected = ExampleTemplate().create(to_consume=True)
#        actual = ExampleTemplate().create(to_consume=False)
#        
#        self.assertEqual(expected, actual)
#
#    def test_marshall_view_model_to_consume(self):
#        
#        expected = ExampleTemplate().create(to_consume=True)
#        actual = ExampleTemplate().create_from_file(to_consume=True)
#
#        self.assertEqual(expected, actual)
#
#    def test_marshall_view_model_to_produce(self):
#        
#        expected = ExampleTemplate().create(to_consume=False)
#        actual = ExampleTemplate().create_from_file(to_consume=False)
#
#        self.assertEqual(expected, actual)
#
#    def test_marshall_view_model_from_invalid(self):
#        
#        try:
#            ExampleTemplate().create_from_file(to_consume=True, invalid=True)
#            self.fail('The expected error was not raised when trying to decode an invalid representation')
#        except json.JSONDecodeError:
#            pass
#
#    def test_unmarshall_valid_view_model_to_consume(self):
#
#        expected = ExampleTemplate().get_file_content_as_string(to_consume=True)
#        actual = Serializer().serialize(ExampleTemplate().create(to_consume=True), partial=True)
#
#        self.assertEqual(expected, actual)
#    
#    def test_unmarshall_valid_view_model_to_produce(self):
#
#        expected = ExampleTemplate().get_file_content_as_string(to_consume=False)
#        actual = Serializer().serialize(ExampleTemplate().create(to_consume=False), partial=False)
#
#        self.assertEqual(expected, actual)
#
#    def test_unmarshall_then_marshall_with_two_templates(self):
#        
#        first = ExampleTemplate().create(to_consume=False)
#        second = ExampleTemplate().create_alternative(to_consume=False)
#
#        serializer = Serializer()
#
#        first_serialized = serializer.serialize(first)
#        second_serialized = serializer.serialize(second)
#        
#        first_deserialized = serializer.deserialize(TemplateDetailViewModel(), first_serialized)
#        second_deserialized = serializer.deserialize(TemplateDetailViewModel(), second_serialized)
#
#        self.assertEqual(first, first_deserialized)
#        self.assertEqual(second, second_deserialized)
#
#        first_reserialized = serializer.serialize(first_deserialized)
#        second_reserialized = serializer.serialize(second_deserialized)
#        
#        self.assertEqual(first_serialized, first_reserialized)
#        self.assertEqual(second_serialized, second_reserialized)
#        
#
#        