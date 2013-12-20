"""
This is the interface for interacting with Instructure's Canvas web services.
"""

from restclients.dao import Canvas_DAO
from restclients.models.canvas import Course
from restclients.exceptions import DataFailureException
from urllib import quote, unquote
import warnings
import json
import re


DEFAULT_PAGINATION = 0
MASQUERADING_USER = None


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


class Canvas(object):
    """
    The Canvas object has methods for getting information
    about accounts, courses, enrollments and users within
    Canvas
    """

    def __init__(self, per_page=DEFAULT_PAGINATION, as_user=MASQUERADING_USER):
        """
        Prepares for paginated responses
        """
        self._per_page = per_page
        self._as_user = as_user
        self._re_canvas_id = re.compile(r'^\d+$')

    def get_courses_for_regid(self, regid):
        deprecation("Use restclients.canvas.courses.get_courses_for_regid")
        from restclients.canvas.courses import Courses
        return Courses().get_courses_for_regid(regid)

    def get_enrollments_for_regid(self, regid):
        deprecation("Use restclients.canvas.enrollments.get_enrollments_for_regid")
        from restclients.canvas.enrollments import Enrollments
        return Enrollments().get_enrollments_for_regid(regid)

    def get_term_by_sis_id(self, sis_term_id):
        """
        Return a term resource for the passed SIS ID.
        """
        # There is not an actual term resource in the Canvas API, so we have
        # to fake it
        from restclients.canvas.courses import Courses
        sis_course_id = "-".join([sis_term_id, "TRAIN-102-A"])
        course = Courses().get_course_by_sis_id(sis_course_id)
        return course.term

    def valid_canvas_id(self, canvas_id):
        return self._re_canvas_id.match(str(canvas_id)) is not None

    def sis_account_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="account")

    def sis_course_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="course")

    def sis_section_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="section")

    def sis_user_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="user")

    def get_roles_by_canvas_id(self, canvas_id):
        return self._get_roles(canvas_id)

    def get_roles_by_sis_id(self, sis_id):
        return self._get_roles(self._sis_id(sis_id))

    def _get_roles(self, id):
        """
        return list of users and associated roles in given account
        """
        return self._get_resource("/api/v1/accounts/%s/roles" % id)

    def get_role_by_canvas_id(self, canvas_id, role):
        return self._get_role(canvas_id, role)

    def get_role_by_sis_id(self, sis_id, role):
        return self._get_role(self._sis_id(sis_id), role)

    def _get_role(self, id, role):
        """
        return list of roles defined in given account id
        """
        return self._get_resource("/api/v1/accounts/%s/roles/%s"
                                  % (id, quote(role)))

    def _sis_id(self, id, sis_field='account'):
        """
        generate sis_id object reference
        """
        return quote('sis_%s_id:%s' % (sis_field, id))

    def _params(self, params):
        if params and len(params):
            p = []
            for key, val in params.iteritems():
                if isinstance(val, list):
                    p.extend([key + '=' + str(v) for v in val])
                else:
                    p.append(key + '=' + str(val))

            return "?%s" % ('&'.join(p))

        return ""

    def _pagination(self, params):
        if self._per_page != DEFAULT_PAGINATION:
            params["per_page"] = self._per_page

        return params

    def _next_page(self, response):
        """
        return url path to next page of paginated data
        """
        for link in response.getheader("link", "").split(","):
            try:
                (url, rel) = link.split(";")
                if "next" in rel:
                    return url.lstrip("<").rstrip(">")
            except:
                return

    def _get_resource(self, url):
        """
        Canvas GET method. Return representation of the requested resource,
        chasing pagination links to coalesce resources.
        """
        if(self._as_user is not None):
            url = url + "?as_user_id=" + self.sis_user_id(self._as_user)
        
        response = Canvas_DAO().getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)
        print url

        if isinstance(data, list):
            next_page = self._next_page(response)
            if next_page:
                data.extend(self._get_resource(next_page))

        return data

    def _put_resource(self, url, body):
        """
        Canvas PUT method.
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        response = Canvas_DAO().putURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _post_resource(self, url, body):
        """
        Canvas POST method.
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        response = Canvas_DAO().postURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def sis_import(self, root_account, csv_data):
        """
        Submits raw CSV SIS data
        """
        url = "/api/v1/accounts/%s/sis_imports.json?import_type=instructure_csv" % root_account
        dao = Canvas_DAO()
        post_response = dao.postURL(url, {"Content-Type": "text/csv"},
                                    csv_data)
        if not (post_response.status == 200 or post_response.status == 204):
            raise DataFailureException(url, post_response.status,
                                       post_response.data)
        return json.loads(post_response.data)

    def get_import_status(self, root_account, import_id):
        """
        Submits raw CSV SIS data
        """
        url = "/api/v1/accounts/%s/sis_imports/%s" % (root_account, import_id)
        dao = Canvas_DAO()
        get_response = dao.getURL(url, {"Content-Type": "application/json"})
        if not (get_response.status == 200 or get_response.status == 204):
            raise DataFailureException(url, get_response.status,
                                       get_response.data)

        return json.loads(get_response.data)
