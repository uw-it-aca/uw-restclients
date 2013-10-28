from django.test import TestCase
from restclients.canvas.sections import Sections 

class CanvasTestSections(TestCase):

    def test_sections(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Sections()

            sections = canvas.get_sections_in_course_by_sis_id('2013-spring-CSE-142-A', {'include': 'students'})

            self.assertEquals(len(sections), 16, "Too few sections")

            n = 0
            for section in sections:
                n += len(section.students)

            self.assertEquals(n, 32, "Too few students")

    def test_sections_with_students(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Sections()

            sections = canvas.get_sections_with_students_in_course_by_sis_id('2013-spring-CSE-142-A')

            self.assertEquals(len(sections), 16, "Too few sections")

            n = 0
            for section in sections:
                n += len(section.students)

            self.assertEquals(n, 32, "Too few students")

