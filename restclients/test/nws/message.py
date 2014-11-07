from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException
from restclients.models import CourseAvailableEvent
from vm.v1.viewmodels import Message, MessageList, Serializer
from unittest2 import skipIf


class NWSTestMessage(TestCase):
    def test_create_message_with_model_open(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):

            course_available_event = CourseAvailableEvent()
            course_available_event.event_id = "blah"
            course_available_event.last_modified = "2012-12-23T09:00:00"
            course_available_event.space_available = 1
            course_available_event.quarter = "winter"
            course_available_event.year = 2012
            course_available_event.curriculum_abbr = "cse"
            course_available_event.course_number = "100"
            course_available_event.section_id = "aa"
            course_available_event.sln = "12345"
            course_available_event.notification_msg_0 = ""

            message = Message()
            message.message_type =  "uw_student_courseavailable"
            message.content = course_available_event.json_data()
            self.assertEquals(message.content['Event']['Section']['SectionID'], 'AA')
            self.assertEquals(message.content['Event']['Section']['Course']['CurriculumAbbreviation'], 'CSE')
            self.assertEquals(message.content['Event']['NotificationMsg0'], '')

            nws = NWS()
            response_status = nws.create_new_message(message)
            self.assertEquals(response_status, 200)

    def test_create_message_with_model_closed(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):

            course_available_event = CourseAvailableEvent()
            course_available_event.event_id = "blah"
            course_available_event.last_modified = "2012-12-23T09:00:00"
            course_available_event.space_available = 0
            course_available_event.quarter = "winter"
            course_available_event.year = 2012
            course_available_event.curriculum_abbr = "cse"
            course_available_event.course_number = "100"
            course_available_event.section_id = "aa"
            course_available_event.sln = "12345"
            course_available_event.notification_msg_0 = " NO"

            message = Message()
            message.message_type =  "uw_student_courseavailable"
            message.content = course_available_event.json_data()
            self.assertEquals(message.content['Event']['Section']['SectionID'], 'AA')
            self.assertEquals(message.content['Event']['Section']['Course']['CurriculumAbbreviation'], 'CSE')
            self.assertEquals(message.content['Event']['NotificationMsg0'], ' NO')

            nws = NWS()
            response_status = nws.create_new_message(message)
            self.assertEquals(response_status, 200)

    def test_create_message_with_json(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):

            json = {
                "Event": {
                    "EventID":"blah",
                    "Href":"",
                    "LastModified":"2012-12-23T09:00:00",
                    "Section": {
                        "Course": {
                            "CourseNumber":"100",
                            "CurriculumAbbreviation":"cse",
                            "Quarter":"winter",
                            "Year":2012
                        },
                        "Href":"",
                        "SLN":"12345",
                        "SectionID":"aa"
                    },
                    "SpaceAvailable":1
                }
            }

            message = Message()
            message.message_type =  "uw_student_courseavailable"
            message.content = json

            nws = NWS()
            response_status = nws.create_new_message(message)
            self.assertEquals(response_status, 200)

    @skipIf(True, "Used only for live testing")
    def _create_message_live_with_model(self):
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
            message.message_type =  "uw_student_courseavailable"
            message.content = course_available_event.json_data()

            nws = NWS()
            response_status = nws.create_new_message(message)
            self.assertEquals(response_status, 200)

    @skipIf(True, "Used only for live testing")
    def _create_message_live_with_json(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):

            json = {
                "Event": {
                    "EventID":"blah",
                    "Href":"",
                    "LastModified":"2012-12-23T09:00:00",
                    "Section": {
                        "Course": {
                            "CourseNumber":"200",
                            "CurriculumAbbreviation":"ling",
                            "Quarter":"autumn",
                            "Year":2012
                        },
                        "Href":"",
                        "SLN":"16116",
                        "SectionID":"ac"
                    },
                    "SpaceAvailable":1
                }
            }

            message = Message()
            message.message_type =  "uw_student_courseavailable"
            message.content = json

            nws = NWS()
            response_status = nws.create_new_message(message)
            self.assertEquals(response_status, 200)

