from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.models.sws import Section
from restclients.exceptions import DataFailureException
import random
import re


class SWSTestGradeRoster(TestCase):

    def test_get_graderoster(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            sws = SWS()

            section = sws.get_section_by_label('2013,summer,CSS,161/A')
            instructor = section.meetings[0].instructors[0]

            graderoster = sws.get_graderoster(section, instructor)

            self.assertEquals(len(graderoster.grade_submission_delegates), 2, "Grade submission delegates")
            self.assertEquals(len(graderoster.items), 5, "GradeRoster items")

            grades = ['0.7', None, '3.1', '1.5', '4.0']
            for idx, item in enumerate(graderoster.items):
                self.assertEquals(len(item.grades), 36, "Correct grade count")
                self.assertEquals(item.current_grade, grades[idx], "Correct grade")

    def test_put_graderoster(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            sws = SWS()

            section = sws.get_section_by_label('2013,summer,CSS,161/A')
            instructor = section.meetings[0].instructors[0]

            graderoster = sws.get_graderoster(section, instructor)

            for item in graderoster.items:
                new_grade = str(round(random.uniform(1, 4), 1))
                item.current_grade = new_grade

            orig_xhtml = split_xhtml(sws._xhtml_from_graderoster(graderoster))

            new_graderoster = sws.update_graderoster(graderoster)
            new_xhtml = split_xhtml(sws._xhtml_from_graderoster(new_graderoster))
            self.assertEquals(orig_xhtml, new_xhtml, "XHTML is equal")


def split_xhtml(xhtml):
    return re.split(r'\s*\n\s*', xhtml.strip())

