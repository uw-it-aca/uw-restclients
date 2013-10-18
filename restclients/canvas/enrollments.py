from restclients.canvas import Canvas
from restclients.canvas.courses import Courses
from restclients.dao import Canvas_DAO
from restclients.models.canvas import Enrollment
from restclients.exceptions import DataFailureException
import json
import re


class Enrollments(Canvas):
    def get_enrollments_for_course(self, sis_course_id, params={}):
        """
        Return a list of all enrollments for the passed course_id.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = "/api/v1/courses/%s/enrollments%s" % (
            self._sis_id(sis_course_id, sis_field="course"),
            self._params(params))

        enrollments = []
        for datum in self._get_resource(url):
            enrollment = self._enrollment_from_json(datum)
            enrollment.sis_course_id = sis_course_id
            enrollments.append(enrollment)

        return enrollments

    def get_enrollments_for_section(self, sis_section_id, params={}):
        """
        Return a list of all enrollments for the passed section_id.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = "/api/v1/sections/%s/enrollments%s" % (
            self._sis_id(sis_section_id, sis_field="section"),
            self._params(params))

        enrollments = []
        for datum in self._get_resource(url):
            enrollment = self._enrollment_from_json(datum)
            enrollments.append(enrollment)

        return enrollments

    def get_enrollments_for_regid(self, regid, params={}):
        """
        Return a list of enrollments for the passed user regid.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = "/api/v1/users/%s/enrollments%s" % (
            self._sis_id(regid, sis_field="user"),
            self._params(params))

        courses = Courses()

        enrollments = []
        for datum in self._get_resource(url):
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
        body = json.dumps({"enrollment": {"user_id": user_id,
                                          "type": role,
                                          "enrollment_state": status}})

        dao = Canvas_DAO()
        response = dao.postURL(url, {"Content-Type": "application/json"},
                               body)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return self._enrollment_from_json(response.data)

    def _enrollment_from_json(self, data):
        enrollment = Enrollment()
        enrollment.user_id = data["user_id"]
        enrollment.course_id = data["course_id"]
        enrollment.section_id = data["course_section_id"]
        enrollment.role = data["type"]
        enrollment.status = data["enrollment_state"]
        enrollment.login_id = data["user"]["login_id"]
        enrollment.html_url = data["html_url"]
        return enrollment
