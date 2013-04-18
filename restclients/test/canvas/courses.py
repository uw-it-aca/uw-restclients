from django.test import TestCase
from restclients.canvas import Canvas


class CanvasTestCourses(TestCase):

    def test_courses(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            courses = canvas.get_courses_in_account_by_sis_id('uwcourse:seattle:arts-&-sciences:amath:amath',
                                                                 {'published': True})

            self.assertEquals(len(courses), 7, "Too few courses")

            course = courses[2]

            self.assertEquals(course['id'], 141414, "Has proper account id")
            self.assertEquals(course['name'], "AMATH 403 A: Methods For Partial Differential Equations")

    def test_published_courses(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            courses = canvas.get_published_courses_in_account_by_sis_id('uwcourse:seattle:arts-&-sciences:amath:amath')

            self.assertEquals(len(courses), 7, "Too few courses")

            course = courses[2]

            self.assertEquals(course['id'], 141414, "Has proper account id")
            self.assertEquals(course['name'], "AMATH 403 A: Methods For Partial Differential Equations")
