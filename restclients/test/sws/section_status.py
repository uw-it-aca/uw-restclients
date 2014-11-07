from django.test import TestCase
from django.conf import settings
from restclients.models.sws import Term, Curriculum, Person
from restclients.exceptions import DataFailureException, InvalidSectionID
from restclients.sws.section_status import get_section_status_by_label
from restclients.sws import get_resource

class SWSTestSectionStatusData(TestCase):
    def test_section_by_label(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            #Valid data, shouldn't throw any exceptions
            section_status = get_section_status_by_label('2012,autumn,CSE,100/W')

            self.assertFalse(section_status.add_code_required)
            self.assertEquals(section_status.current_enrollment, 305)
            self.assertEquals(section_status.current_registration_period, 3)
            self.assertFalse(section_status.faculty_code_required)
            self.assertEquals(section_status.limit_estimated_enrollment, 345)
            self.assertEquals(section_status.limit_estimate_enrollment_indicator, 'limit')
            self.assertEquals(section_status.room_capacity, 345)
            self.assertEquals(section_status.sln, 12588)
            self.assertEquals(section_status.space_available, 40)
            self.assertEquals(section_status.is_open, True)

# XXX - testing internal function - move to a v4 specific test?
#    def test_json_to_sectionstatus(self):
#        with self.settings(
#                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
#                ):
#            data = get_resource('/student/v4/course/2012,autumn,CSE,100/W/status.json')
#            section_status = _json_to_sectionstatus(data)
#            self.assertFalse(section_status.add_code_required)
#            self.assertEquals(section_status.current_enrollment, 305)
#            self.assertEquals(section_status.current_registration_period, 3)
#            self.assertFalse(section_status.faculty_code_required)
#            self.assertEquals(section_status.limit_estimated_enrollment, 345)
#            self.assertEquals(section_status.limit_estimate_enrollment_indicator, 'limit')
#            self.assertEquals(section_status.room_capacity, 345)
#            self.assertEquals(section_status.sln, 12588)
#            self.assertEquals(section_status.space_available, 40)
#            self.assertEquals(section_status.is_open, True)
