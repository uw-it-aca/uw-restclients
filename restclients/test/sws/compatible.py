from django.test import TestCase
from django.conf import settings
from datetime import datetime, timedelta
from restclients.sws import SWS
from restclients.models.sws import Term, Curriculum, Person
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidSectionURL

class SWSTest(TestCase):
    def test_mock_data_fake_grading_window(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            sws = SWS()

            # backwards compatible for term
            term = sws.get_current_term()
            self.assertEquals(term.year, 2013)
            self.assertEquals(term.quarter, 'spring')
                
            term = sws.get_term_by_year_and_quarter(2013, 'spring')
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

            section = sws.get_section_by_label('2013,summer,TRAIN,100/A')
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

            section_status = sws.get_section_status_by_label(
                '2012,autumn,CSE,100/W')
            self.assertEquals(section_status.sln, 12588)

            section = sws.get_section_by_label('2013,winter,DROP_T,100/A')
            registrations = sws.get_all_registrations_for_section(section)
            self.assertEquals(len(registrations), 1)

            term = sws.get_current_term()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE',
                                            term)
            grades = sws.grades_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            self.assertEquals(grades.user.uwnetid, "javerage")

            campuses = sws.get_all_campuses()
            self.assertEquals(len(campuses), 3)
