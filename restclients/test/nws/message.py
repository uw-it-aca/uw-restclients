from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException
from restclients.models import Message, CourseAvailableEvent
from unittest import skipIf

class NWSTestMessage(TestCase):
    def test_create_message(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            
            course_available_event = CourseAvailableEvent()
            course_available_event.event_id = "blah"
            course_available_event.last_modified = "2012-12-23T09:00:00"
            course_available_event.status = "open"
            course_available_event.space_available = 1
            course_available_event.quarter = "winter"
            course_available_event.year = 2013
            course_available_event.curriculum_abbr = "CSE"
            course_available_event.course_number = "100"
            course_available_event.section_id = "aa"
            course_available_event.sln = "12345"
            
            message = Message()
            message.type =  "uw_student_courseavailable"
            message.content = course_available_event

            nws = NWS()
            response_status = nws.create_new_message(message)
            self.assertEquals(response_status, 201)


    @skipIf(True, "Used only for live testing")
    def _create_message_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            course_available_event = CourseAvailableEvent()
            course_available_event.event_id = "blah"
            course_available_event.last_modified = "2012-12-23T09:00:00"
            course_available_event.status = "open"
            course_available_event.space_available = 1
            course_available_event.quarter = "autumn"
            course_available_event.year = 2012
            course_available_event.curriculum_abbr = "ling"
            course_available_event.course_number = "200"
            course_available_event.section_id = "ac"
            course_available_event.sln = "16116"
            
            message = Message()
            message.type =  "uw_student_courseavailable"
            message.content = course_available_event

            nws = NWS()
            response_status = nws.create_new_message(message)
            self.assertEquals(response_status, 201)

