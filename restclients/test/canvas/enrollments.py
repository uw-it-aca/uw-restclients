from django.test import TestCase
from django.conf import settings
from restclients.canvas import Canvas
from restclients.exceptions import DataFailureException

class CanvasTestEnrollment(TestCase):

    #Expected values will have to change when the json files are updated
    def test_enrollment(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            # Javerage's regid
            enrollments = canvas.get_enrollments_for_regid("9136CCB8F66711D5BE060004AC494FFE")

            self.assertEquals(len(enrollments), 1, "Has 1 canvas enrollment")

            enrollment = enrollments[0]

            self.assertEquals(enrollment.course_url, "https://canvas.uw.edu/courses/149650", "Has proper course url")
            self.assertEquals(enrollment.sis_id, "2012-summer-PHYS-121-A")
            self.assertEquals(enrollment.sws_course_id(), "2012,summer,PHYS,121/A")

    def test_courses(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            # Javerage's regid
            courses = canvas.get_courses_for_regid("9136CCB8F66711D5BE060004AC494FFE")

            self.assertEquals(len(courses), 1, "Has 1 canvas enrollment")

            course = courses[0]

            self.assertEquals(course.course_url, "https://canvas.uw.edu/courses/149650", "Has proper course url")
            self.assertEquals(course.sis_id, "2012-summer-PHYS-121-A")
            self.assertEquals(course.sws_course_id(), "2012,summer,PHYS,121/A")


