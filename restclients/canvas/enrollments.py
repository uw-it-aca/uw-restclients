from restclients.canvas import Canvas
from restclients.canvas.courses import Courses
from restclients.models.canvas import CanvasEnrollment
import dateutil.parser
import re


class Enrollments(Canvas):
    def get_enrollments_for_course(self, course_id, params={}):
        """
        Return a list of all enrollments for the passed course_id.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = "/api/v1/courses/%s/enrollments" % (course_id)

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            enrollment = self._enrollment_from_json(datum)
            enrollments.append(enrollment)

        return enrollments

    def get_enrollments_for_course_by_sis_id(self, sis_course_id, params={}):
        """
        Return a list of all enrollments for the passed course sis id.
        """
        return self.get_enrollments_for_course(
            self._sis_id(sis_course_id, sis_field="course"), params)

    def get_enrollments_for_section(self, section_id, params={}):
        """
        Return a list of all enrollments for the passed section_id.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = "/api/v1/sections/%s/enrollments" % (section_id)

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            enrollment = self._enrollment_from_json(datum)
            enrollments.append(enrollment)

        return enrollments

    def get_enrollments_for_section_by_sis_id(self, sis_section_id, params={}):
        """
        Return a list of all enrollments for the passed section sis id.
        """
        return self.get_enrollments_for_section(
            self._sis_id(sis_section_id, sis_field="section"), params)

    def get_enrollments_for_regid(self, regid, params={}):
        """
        Return a list of enrollments for the passed user regid.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = "/api/v1/users/%s/enrollments" % (
            self._sis_id(regid, sis_field="user"))

        courses = Courses()

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            course_id = datum["course_id"]
            course = courses.get_course(course_id)

            if course.sis_course_id is not None:
                enrollment = self._enrollment_from_json(datum)
                enrollment.course_url = course.course_url
                enrollment.course_name = course.name
                enrollment.sis_course_id = course.sis_course_id
                enrollments.append(enrollment)

        return enrollments

    def enroll_user_in_course(self, course_id, user_id, role, status="active"):
        """
        Enroll a user into a course.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create
        """
        url = "/api/v1/courses/%s/enrollments" % course_id
        body = {"enrollment": {"user_id": user_id,
                               "type": role,
                               "enrollment_state": status}}

        data = self._post_resource(url, body)
        return self._enrollment_from_json(data)

    def _enrollment_from_json(self, data):
        enrollment = CanvasEnrollment()
        enrollment.user_id = data["user_id"]
        enrollment.course_id = data["course_id"]
        enrollment.section_id = data["course_section_id"]
        enrollment.role = data["type"]
        enrollment.status = data["enrollment_state"]
        enrollment.html_url = data["html_url"]
        enrollment.total_activity_time = data["total_activity_time"]
        if data["last_activity_at"] is not None:
            date_str = data["last_activity_at"]
            enrollment.last_activity_at = dateutil.parser.parse(date_str)
        if "sis_course_id" in data:
            enrollment.sis_course_id = data["sis_course_id"]
        if "sis_section_id" in data:
            enrollment.sis_section_id = data["sis_section_id"]
        if "user" in data:
            enrollment.name = data["user"]["name"]
            enrollment.sortable_name = data["user"]["sortable_name"]
            if "login_id" in data["user"]:
                enrollment.login_id = data["user"]["login_id"]
            if "sis_user_id" in data["user"]:
                enrollment.sis_user_id = data["user"]["sis_user_id"]
        if "grades" in data:
            enrollment.current_score = data["grades"]["current_score"]
            enrollment.final_score = data["grades"]["final_score"]
            enrollment.current_grade = data["grades"]["current_grade"]
            enrollment.final_grade = data["grades"]["final_grade"]
            enrollment.grade_html_url = data["grades"]["html_url"]
        return enrollment
