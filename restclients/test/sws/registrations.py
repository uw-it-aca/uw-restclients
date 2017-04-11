from django.test import TestCase
from django.conf import settings
from restclients.models.sws import Term
from restclients.sws.section import get_section_by_label
from restclients.sws.registration import get_active_registrations_by_section
from restclients.sws.registration import get_all_registrations_by_section
from restclients.sws.registration import get_schedule_by_regid_and_term
from restclients.exceptions import DataFailureException
from decimal import Decimal
import mock


class SWSTestRegistrations(TestCase):

    def test_active_registrations_for_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Valid section, missing file resources
            section = get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              get_active_registrations_by_section,
                              section)

    def test_all_registrations_by_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Valid section, missing file resources
            section = get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              get_all_registrations_by_section,
                              section)

    def test_active_registration_status_after_drop(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = get_section_by_label('2013,winter,DROP_T,100/A')

            registrations = get_all_registrations_by_section(section)

            self.assertEquals(len(registrations), 2)
            javerage_reg = registrations[0]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, False)
            self.assertEquals(javerage_reg.is_auditor, False)
            self.assertEquals(javerage_reg.is_credit, True)
            self.assertEquals(str(javerage_reg.request_date.date()), '2015-11-18')
            self.assertEquals(javerage_reg.request_status, 'DROPPED FROM CLASS')
            self.assertEquals(javerage_reg.duplicate_code, '')
            self.assertEquals(javerage_reg.repository_timestamp.isoformat(), '2016-01-05T02:45:15')

    def test_active_registration_status_after_drop_and_add(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = get_section_by_label('2013,winter,DROP_T,100/B')
            registrations = get_all_registrations_by_section(section)

            self.assertEquals(len(registrations), 3)
            javerage_reg = registrations[2]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, True)
            self.assertEquals(javerage_reg.is_auditor, True)
            self.assertEquals(javerage_reg.is_credit, True)
            self.assertEquals(str(javerage_reg.request_date.date()), '2015-11-18')
            self.assertEquals(javerage_reg.request_status, 'ADDED TO CLASS')
            self.assertEquals(javerage_reg.duplicate_code, 'A')
            self.assertEquals(javerage_reg.repository_timestamp.isoformat(), '2016-01-05T02:45:15')

    @mock.patch('uw_sws.registration.get_resource')
    def test_all_registrations_with_transcriptable_course(self, mock_get_resource):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = get_section_by_label('2013,winter,DROP_T,100/B')

            # Test for default resource, i.e. transcriptable_course=yes
            registrations = get_all_registrations_by_section(section)
            mock_get_resource.assert_called_with('/student/v5/registration.json?curriculum_abbreviation=DROP_T&instructor_reg_id=&course_number=100&verbose=true&year=2013&quarter=winter&is_active=&section_id=B')

            # Test for transcriptable_course=yes explicitly
            registrations = get_all_registrations_by_section(
                section, transcriptable_course='yes')
            mock_get_resource.assert_called_with('/student/v5/registration.json?curriculum_abbreviation=DROP_T&instructor_reg_id=&course_number=100&verbose=true&year=2013&quarter=winter&is_active=&section_id=B&transcriptable_course=yes')

            # Test for transcriptable_course=all resource
            registrations = get_all_registrations_by_section(
                section, transcriptable_course='all')
            mock_get_resource.assert_called_with('/student/v5/registration.json?curriculum_abbreviation=DROP_T&instructor_reg_id=&course_number=100&verbose=true&year=2013&quarter=winter&is_active=&section_id=B&transcriptable_course=all')

            # Test for transcriptable_course=no
            registrations = get_all_registrations_by_section(
                section, transcriptable_course='no')
            mock_get_resource.assert_called_with('/student/v5/registration.json?curriculum_abbreviation=DROP_T&instructor_reg_id=&course_number=100&verbose=true&year=2013&quarter=winter&is_active=&section_id=B&transcriptable_course=no')

    def test_get_schedule_by_regid_and_term(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            term = Term(quarter="spring", year=2013)
            class_schedule = get_schedule_by_regid_and_term(
                '9136CCB8F66711D5BE060004AC494FFE',
                term)
            for section in class_schedule.sections:
                if section.section_label() == '2013,spring,TRAIN,100/A':
                    self.assertEquals(len(section.get_instructors()), 1)
                    self.assertEquals(section.student_credits, Decimal("%s" % 1.0))
                    self.assertEquals(section.student_grade, "X")
                    self.assertEquals(section.get_grade_date_str(), None)
                    self.assertTrue(section.is_primary_section)
                    self.assertEquals(section.is_auditor, False)

                if section.section_label() == '2013,spring,PHYS,121/AC':
                    self.assertEquals(section.student_credits, Decimal("%s" % 3.0))
                    self.assertEquals(section.student_grade, "4.0")
                    self.assertEquals(section.get_grade_date_str(), "2013-06-11")
                    self.assertFalse(section.is_primary_section)
                    self.assertEquals(section.is_auditor, False)

            class_schedule = get_schedule_by_regid_and_term(
                '9136CCB8F66711D5BE060004AC494FFE',
                term, False)
            for section in class_schedule.sections:
                if section.section_label() == '2013,spring,TRAIN,100/A':
                    self.assertEquals(len(section.get_instructors()), 0)

            class_schedule = get_schedule_by_regid_and_term(
                '12345678901234567890123456789012', term)
            for section in class_schedule.sections:
                if section.section_label() == '2013,spring,,MATH,125/G':
                    self.assertEquals(section.student_credits, Decimal("%s" % 5.0))
                    self.assertEquals(section.student_grade, "3.5")
                    self.assertEquals(section.is_auditor, True)
                    self.assertTrue(section.is_primary_section)

    def test_get_schedule_by_regid_and_term(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
            RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            term = Term(quarter="spring", year=2013)
            class_schedule = get_schedule_by_regid_and_term(
                'FE36CCB8F66711D5BE060004AC494FCE',
                term, transcriptable_course="no")

            for section in class_schedule.sections:
                if section.section_label() == '2013,spring,ESS,107/A':
                    self.assertEquals(len(section.get_instructors()), 1)
                    self.assertEquals(section.student_credits, Decimal("%s" % 3.0))
                    self.assertEquals(section.student_grade, "X")
                    self.assertEquals(section.get_grade_date_str(), None)
                    self.assertTrue(section.is_primary_section)
                    self.assertEquals(section.is_auditor, False)
