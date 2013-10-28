from restclients.canvas import Canvas
from restclients.dao import Canvas_DAO
from restclients.models.canvas import Course, Term
from restclients.exceptions import DataFailureException
import json
import re


class Courses(Canvas):
    def get_course(self, course_id, params={}):
        """
        Return course resource for given canvas course id.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.show
        """
        if "include" in params and params["include"] is not None:
            includes = params["include"].split(",")
            if "term" not in includes:
                params["include"] = ",".join(includes.append("term"))

        else:
            params["include"] = "term"

        url = "/api/v1/courses/%s%s" % (course_id, self._params(params))
        return self._course_from_json(self._get_resource(url))

    def get_course_by_sis_id(self, sis_course_id, params={}):
        """
        Return course resource for given sis id.
        """
        return self.get_course(self._sis_id(sis_course_id, sis_field="course"),
                               params)

    def get_courses_in_account(self, account_id, params={}):
        """
        Returns a list of courses for the passed account ID.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.courses_api
        """
        if "published" in params:
            params["published"] = "true" if params["published"] else ""

        params = self._pagination(params)
        url = "/api/v1/accounts/%s/courses%s" % (account_id,
                                                 self._params(params))
        courses = []
        for data in self._get_resource(url):
            courses.append(self._course_from_json(data))
        return courses

    def get_courses_in_account_by_sis_id(self, sis_account_id, params={}):
        """
        Return a list of courses for the passed account SIS ID.
        """
        return self.get_courses_in_account(self._sis_id(sis_account_id,
                                                        sis_field="account"),
                                           params)

    def get_published_courses_in_account(self, account_id, params={}):
        """
        Return a list of published courses for the passed account ID.
        """
        params["published"] = True
        return self.get_courses_in_account(account_id, params)

    def get_published_courses_in_account_by_sis_id(self, sis_account_id, params={}):
        """
        Return a list of published courses for the passed account SIS ID.
        """

        return self.get_published_courses_in_account(
            self._sis_id(sis_account_id, sis_field="account"), params)

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

    def create_course(self, account_id, course_name):
        """
        Create a canvas course with the given subaccount id and course name.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.create
        """
        url = "/api/v1/accounts/%s/courses" % account_id
        body = json.dumps({"course": {"name": course_name}})

        dao = Canvas_DAO()
        response = dao.postURL(url, {"Content-Type": "application/json"}, body)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return self._course_from_json(json.loads(response.data))

    def _course_from_json(self, data):
        course = Course()
        course.course_id = data["id"]
        course.sis_course_id = data["sis_course_id"] if "sis_course_id" in data else None
        course.account_id = data["account_id"]
        course.name = data["name"]

        course_url = data["calendar"]["ics"]
        course_url = re.sub(r"(.*?[a-z]/).*", r"\1", course_url)
        course.course_url = "%scourses/%s" % (course_url, data["id"])

        if "term" in data:
            course.term = Term(term_id=data["term"]["id"],
                               sis_term_id=data["term"]["sis_term_id"],
                               name=data["term"]["name"])

        return course
