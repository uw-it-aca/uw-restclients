from django.test import TestCase
from django.conf import settings
from datetime import datetime, timedelta
from restclients.sws import SWS, encode_section_label, get_resource
from restclients.models.sws import Term, Curriculum, Person, College, Department
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidSectionURL

class UtilFunctionTest(TestCase):
    def test_encode_section_label(self):
        self.assertEquals(encode_section_label('2013,winter,C LIT,396/A'),
                          '2013,winter,C%20LIT,396/A')

    def test_get_resource(self):
        self.assertEquals(get_resource('/student/v5/campus.json'),
                          "{u'PageSize': u'10', u'Campuses': [{u'CampusShortName': u'BOTHELL', u'Href': u'/student/v5/campus/BOTHELL.json', u'CampusName': u'UW Bothell', u'CampusFullName': u'UNIVERSITY OF WASHINGTON BOTHELL'}, {u'CampusShortName': u'SEATTLE', u'Href': u'/student/v5/campus/SEATTLE.json', u'CampusName': u'UW Seattle', u'CampusFullName': u'UNIVERSITY OF WASHINGTON SEATTLE'}, {u'CampusShortName': u'TACOMA', u'Href': u'/student/v5/campus/TACOMA.json', u'CampusName': u'UW Tacoma', u'CampusFullName': u'UNIVERSITY OF WASHINGTON TACOMA'}], u'Next': None, u'Current': {u'Href': u'/student/v5/campus.json&page_start=1&page_size=10'}, u'TotalCount': 3, u'PageStart': u'1', u'Previous': None}")

class SWSTest(TestCase):
    def test_mock_data_fake_grading_window(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            sws = SWS()

            # backwards compatible for term
            term = sws.get_term_by_year_and_quarter(2013, 'spring')
            self.assertEquals(term.year, 2013)
            self.assertEquals(term.quarter, 'spring')

            term = sws.get_current_term()
            self.assertEquals(term.year, 2013)
            self.assertEquals(term.quarter, 'spring')
                
            prev_term = sws.get_previous_term()
            self.assertEquals(prev_term.year, 2013)
            self.assertEquals(prev_term.quarter, 'winter')

            next_term = sws.get_next_term()
            self.assertEquals(next_term.year, 2013)
            self.assertEquals(next_term.quarter, 'summer')

            term_before = sws.get_term_before(next_term)
            self.assertEquals(term_before.year, 2013)
            self.assertEquals(term_before.quarter, 'spring')

            term_after = sws.get_term_after(prev_term)
            self.assertEquals(term_after.year, 2013)
            self.assertEquals(term_after.quarter, 'spring')

            # backwards compatible for section
            section = sws.get_section_by_label('2013,winter,ASIAN,203/A')
            joint_sections = sws.get_joint_sections(section)
            self.assertEquals(len(joint_sections), 1)

            section = sws.get_section_by_url('/student/v5/course/2013,summer,TRAIN,100/A.json')
            sws.get_linked_sections(section)
            section.linked_section_urls = ['2012,summer,TRAIN,100/A']
            self.assertRaises(InvalidSectionURL,
                              sws.get_linked_sections, section)

            term = Term(quarter="summer", year=2013)
            person = Person(uwregid="FBB38FE46A7C11D5A4AE0004AC494FFE")
            sections = sws.get_sections_by_instructor_and_term(person, term)
            self.assertEquals(len(sections), 1)

            sections = sws.get_sections_by_delegate_and_term(person, term)
            self.assertEquals(len(sections), 2)

            term = Term(quarter="winter", year=2013)
            curriculum = Curriculum(label="ENDO")
            sections = sws.get_sections_by_curriculum_and_term(curriculum, term)
            self.assertEquals(len(sections), 2)

            # backwards compatible for section_status
            section_status = sws.get_section_status_by_label(
                '2012,autumn,CSE,100/W')
            self.assertEquals(section_status.sln, 12588)

            # backwards compatible for registration
            section = sws.get_section_by_label('2013,winter,DROP_T,100/A')
            registrations = sws.get_active_registrations_for_section(section)
            self.assertEquals(len(registrations), 0)
            registrations = sws.get_all_registrations_for_section(section)
            self.assertEquals(len(registrations), 1)

            term = sws.get_current_term()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE',
                                            term)
            # backwards compatible for enrollment
            grades = sws.grades_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            self.assertEquals(grades.user.uwnetid, "javerage")

            # backwards compatible for campus
            campuses = sws.get_all_campuses()
            self.assertEquals(len(campuses), 3)

            # backwards compatible for college
            colleges = sws.get_all_colleges()
            self.assertEquals(len(colleges), 20)

            # backwards compatible for department
            college = College(label="MED")
            depts = sws.get_departments_for_college(college)
            self.assertEquals(len(depts), 30)

            # backwards compatible for curriculum
            department = Department(label="EDUC")
            curricula = sws.get_curricula_for_department(department)
            self.assertEquals(len(curricula), 7)

            term = Term(quarter='winter', year=2013)
            curricula = sws.get_curricula_for_term(term)
            self.assertEquals(len(curricula), 423)
