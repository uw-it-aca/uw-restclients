from django.test import TestCase
from django.conf import settings
from restclients.models import CanvasEnrollment, CanvasCourse
from restclients.exceptions import DataFailureException

class CanvasBadSISIDs(TestCase):
    def test_enrollment(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):

            enrollment = CanvasEnrollment()
            enrollment.sis_id = "2013-winter-CHEM-121"
            sws_id = enrollment.sws_course_id()

            self.assertEquals(sws_id, None, "Invalid SIS ID leads to an sws_id of None")

    def test_course(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):

            course = CanvasCourse()
            course.sis_id = "2013-winter-CHEM-121"
            sws_id = course.sws_course_id()

            self.assertEquals(sws_id, None, "Invalid SIS ID leads to an sws_id of None")


