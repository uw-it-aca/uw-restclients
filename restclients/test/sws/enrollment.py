from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
import restclients.sws.term as TermSws
from restclients.exceptions import DataFailureException

class SWSTestEnrollments(TestCase):
    def test_javerage_grades(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = TermSws.get_current()
            grades = SWS().grades_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)

            self.assertEquals(grades.term.year, 2013)
            self.assertEquals(grades.term.quarter, "spring")
            self.assertEquals(grades.user.uwnetid, "javerage")
            self.assertEquals(grades.grade_points, 30)
            self.assertEquals(grades.credits_attempted, 10)
            self.assertEquals(grades.non_grade_credits, 2)

            self.assertEquals(grades.grades[0].grade, 'CR')
            self.assertEquals(grades.grades[2].grade, '3.1')
            self.assertEquals(grades.grades[2].credits, '3.0')
            self.assertEquals(grades.grades[2].section.course_number, '121')
