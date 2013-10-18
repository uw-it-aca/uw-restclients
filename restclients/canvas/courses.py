from restclients.canvas import Canvas
from restclients.dao import Canvas_DAO
from restclients.models.canvas import Course
from restclients.exceptions import DataFailureException
import json
import re


class Courses(Canvas):
    def get_course(self, course_id):
        """
        Return course resource for given canvas course id.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.show
        """
        url = "/api/v1/courses/%s" % course_id
        return self._course_from_json(self._get_resource(url))

    def get_course_by_canvas_id(self, canvas_id):
        """
        Alias method for get_course().
        """
        return self.get_course(canvas_id)

    def get_course_by_sis_id(self, sis_id):
        """
        Return course resource for given sis id.
        """
        return self.get_course(self._sis_id(sis_id, sis_field="course"))

    def get_courses_for_regid(self, regid):
        """
        Return a list of courses for the passed regid.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.index
        """
        url = "/api/v1/courses.json?as_user_id=%s" % (self._sis_id(regid,
                                                      sis_field="user"))

        courses = []
        for datum in self._get_resource(url):
            course = self.get_course(datum["id"])
            courses.append(course)

        return courses

    def _course_from_json(self, data):
        course = Course()
        course.course_id = data["id"]
        course.sis_course_id = data["sis_course_id"]
        course.name = data["name"]

        course_url = data["calendar"]["ics"]
        course_url = re.sub(r"(.*?[a-z]/).*", r"\1", course_url)
        course.course_url = "%scourses/%s" % (course_url, data["id"])

        return course
