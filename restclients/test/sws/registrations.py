from django.test import TestCase
from django.conf import settings
from restclients.models.sws import Term
from restclients.sws.section import get_section_by_label
from restclients.sws.registration import get_active_registrations_by_section
from restclients.sws.registration import get_all_registrations_by_section
from restclients.sws.registration import get_schedule_by_regid_and_term
from restclients.exceptions import DataFailureException

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

            self.assertEquals(len(registrations), 1)
            javerage_reg = registrations[0]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, False)

    def test_active_registration_status_after_drop_and_add(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = get_section_by_label('2013,winter,DROP_T,100/B')
            registrations = get_all_registrations_by_section(section)

            self.assertEquals(len(registrations), 1)
            javerage_reg = registrations[0]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, True)

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
                    self.assertEquals(section.student_credits, 1.5)
                    self.assertEquals(section.student_grade, "P")
                    self.assertEquals(section.get_grade_date_str(), "2013-06-10")

                if section.section_label() == '2013,spring,PHYS,121/AC':
                    self.assertEquals(section.student_credits, 3.0)
                    self.assertEquals(section.student_grade, "4.0")
                    self.assertEquals(section.get_grade_date_str(), "2013-06-11")

            class_schedule = get_schedule_by_regid_and_term(
                '9136CCB8F66711D5BE060004AC494FFE',
                term, False)
            for section in class_schedule.sections:
                if section.section_label() == '2013,spring,TRAIN,100/A':
                    self.assertEquals(len(section.get_instructors()), 0)

