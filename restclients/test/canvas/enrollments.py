from django.test import TestCase
from django.conf import settings
from restclients.canvas.enrollments import Enrollments
from restclients.exceptions import DataFailureException
from restclients.models.canvas import CanvasEnrollment


class CanvasTestEnrollment(TestCase):
    def test_enrollments_for_course_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Enrollments()

            enrollments = canvas.get_enrollments_for_course_by_sis_id("2013-autumn-PHYS-248-A")

            self.assertEquals(len(enrollments), 3, "Has 3 canvas enrollments")

            students = canvas.get_enrollments_for_course_by_sis_id("2013-autumn-PHYS-248-A",
                    {"role": "student"})

            self.assertEquals(len(students), 2, "Has 2 student enrollments")

    def test_search_enrollments_for_course_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Enrollments()

            enrollments = canvas.search_enrollments_for_course("862539", "jav")

            self.assertEquals(len(enrollments), 3, "Found 3 canvas enrollments")

            enrollment = enrollments[0]
            self.assertEquals(enrollment.sis_course_id, "2015-summer-TRAIN-100-A")
            self.assertEquals(enrollment.login_id, "javerage", "Login ID")
            self.assertEquals(enrollment.sis_user_id, "15AE3883B6EC44C349E04E5FE089ABEB", "SIS User ID")
            self.assertEquals(enrollment.name, "JAMES AVERAGE", "Name")
            self.assertEquals(enrollment.sortable_name, "AVERAGE, JAMES", "Sortable Name")
            self.assertEquals(enrollment.role, "DesignerEnrollment", "Role")

    def test_enrollments_for_section_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):

            canvas = Enrollments()

            enrollments = canvas.get_enrollments_for_section_by_sis_id("2013-autumn-PHYS-248-A--")
            self.assertEquals(len(enrollments), 3, "Has 3 canvas enrollments")

            students = canvas.get_enrollments_for_section_by_sis_id("2013-autumn-PHYS-248-A--",
                {"role": "student"})

            self.assertEquals(len(students), 2, "Has 2 student enrollments")

    #Expected values will have to change when the json files are updated
    def test_enrollments_by_regid(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Enrollments()

            # Javerage's regid
            enrollments = canvas.get_enrollments_for_regid("9136CCB8F66711D5BE060004AC494FFE")

            self.assertEquals(len(enrollments), 2, "Has 2 canvas enrollments")

            enrollment = enrollments[0]

            self.assertEquals(enrollment.course_url, "https://canvas.uw.edu/courses/149650", "Has proper course url")
            self.assertEquals(enrollment.sis_course_id, "2013-spring-PHYS-121-A")
            self.assertEquals(enrollment.sws_course_id(), "2013,spring,PHYS,121/A")

            stu_enrollment = enrollments[1]
            self.assertEquals(stu_enrollment.grade_html_url, "https://uw.test.instructure.com/courses/862539/grades/496164", "Grade URL")
            self.assertEquals(stu_enrollment.current_score, 23.0, "Current score")
            self.assertEquals(stu_enrollment.login_id, "javerage", "Login ID")
            self.assertEquals(stu_enrollment.sis_user_id, "9136CCB8F66711D5BE060004AC494FFE", "SIS User ID")
            self.assertEquals(stu_enrollment.name, "JAMES AVERAGE STUDENT", "Name")
            self.assertEquals(enrollment.sortable_name, "STUDENT, JAMES AVERAGE", "Sortable Name")
            self.assertEquals(str(stu_enrollment.last_activity_at), "2012-08-18 23:08:51-06:00", "Last activity datetime")
            self.assertEquals(stu_enrollment.total_activity_time, 100, "Total activity time")
            self.assertEquals(stu_enrollment.status, CanvasEnrollment.STATUS_ACTIVE, "Status")

    def test_pending_enrollments(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Enrollments()

            enrollments = canvas.get_enrollments_for_course("862539")

            self.assertEquals(len(enrollments), 1, "Has 1 canvas enrollment")

            enrollment = enrollments[0]
            self.assertEquals(enrollment.name, "j.average@gmail.com", "Name")
            self.assertEquals(enrollment.sortable_name, "j.average@gmail.com", "Sortable Name")
            self.assertEquals(enrollment.login_id, None)
            self.assertEquals(enrollment.status, CanvasEnrollment.STATUS_INVITED, "Status")

