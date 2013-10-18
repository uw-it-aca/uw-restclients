from django.test import TestCase
from django.conf import settings
from restclients.canvas.enrollments import Enrollments
from restclients.exceptions import DataFailureException

class CanvasTestEnrollment(TestCase):
    def test_enrollments_for_course_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Enrollments()

            enrollments = canvas.get_enrollments_for_course("2013-autumn-PHYS-248-A")

            self.assertEquals(len(enrollments), 3, "Has 3 canvas enrollments")

            students = canvas.get_enrollments_for_course("2013-autumn-PHYS-248-A",
                    {"role": "student"})

            self.assertEquals(len(students), 2, "Has 2 student enrollments")

    def test_enrollments_for_section_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):

            canvas = Enrollments()

            enrollments = canvas.get_enrollments_for_section("2013-autumn-PHYS-248-A--")
            self.assertEquals(len(enrollments), 3, "Has 3 canvas enrollments")

            students = canvas.get_enrollments_for_section("2013-autumn-PHYS-248-A--",
                {"role": "student"})

            self.assertEquals(len(students), 2, "Has 2 student enrollments")

    #Expected values will have to change when the json files are updated
    def test_enrollments_by_regid(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Enrollments()

            # Javerage's regid
            enrollments = canvas.get_enrollments_for_regid("9136CCB8F66711D5BE060004AC494FFE")

            self.assertEquals(len(enrollments), 1, "Has 1 canvas enrollment")

            enrollment = enrollments[0]

            self.assertEquals(enrollment.course_url, "https://canvas.uw.edu/courses/149650", "Has proper course url")
            self.assertEquals(enrollment.sis_course_id, "2012-summer-PHYS-121-A")
            self.assertEquals(enrollment.sws_course_id(), "2012,summer,PHYS,121/A")
