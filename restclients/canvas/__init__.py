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


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


class Canvas(object):
    """
    The Canvas object has methods for getting information
    about accounts, courses, enrollments and users within
    Canvas
    """

    def __init__(self, per_page=DEFAULT_PAGINATION):
        """
        Prepares for paginated responses
        """
        self._per_page = per_page
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

    def valid_canvas_id(self, id):
        return self._re_canvas_id.match(id) is not None

    def sis_account_id(self, sis_id):
        return self._sis_id(sis_id, sis_field='account')

    def sis_course_id(self, sis_id):
        return self._sis_id(sis_id, sis_field='course')

    def sis_section_id(self, sis_id):
        return self._sis_id(sis_id, sis_field='section')

    def sis_user_id(self, sis_id):
        return self._sis_id(sis_id, sis_field='user')

    def get_course_section(self, course_id, section_id):
        return self._get_resource("/api/v1/courses/%s/sections/%s"
                                  % (course_id, section_id))

    def get_sections_by_canvas_id(self, canvas_id, params={}):
        return self._get_sections(canvas_id, params)

    def get_sections_by_sis_id(self, sis_id, params={}):
        return self._get_sections(self._sis_id(sis_id, sis_field='course'),
                                  params)

    def get_sections_with_students_by_canvas_id(self, canvas_id):
        return self._get_sections(canvas_id, {'include': 'students'})

    def get_sections_with_students_by_sis_id(self, sis_id):
        return self._get_sections(self._sis_id(sis_id, sis_field='course'),
                                  {'include': 'students'})

    def _get_sections(self, id, params):
        params = self._pagination(params)
        return self._get_resource("/api/v1/courses/%s/sections%s"
                                  % (id, self._params(params)))

    def get_admins_by_canvas_id(self, canvas_id):
        return self.get_admins(canvas_id)

    def get_admins_by_sis_id(self, sis_id):
        return self.get_admins(self._sis_id(sis_id))

    def get_admins(self, id):
        """
        return list of admins in given account
        """
        params = self._pagination({})
        return self._get_resource("/api/v1/accounts/%s/admins%s"
                                  % (id, self._params(params)))

    def delete_admin_by_canvas_id(self, canvas_id, user_id, role):
        return self.delete_admin(canvas_id, user_id, role)

    def delete_admin_by_sis_id(self, sis_id, user_id, role):
        return self.delete_admin(self._sis_id(sis_id), user_id, role)

    def add_admin(self, account_id, user_id, role):
        """
        add given user with assigned role to given account
        """
        url = "/api/v1/accounts/%s/admins" % (account_id)
        dao = Canvas_DAO()
        post_response = dao.postURL(url, {"Content-Type": "application/json"},
                                    json.dumps({'user_id': unquote(user_id),
                                                'role': role,
                                                'send_confirmation': '0'}))

        if not (post_response.status == 200 or post_response.status == 204):
            raise DataFailureException(url, post_response.status,
                                       post_response.data)

        return json.loads(post_response.data)

    def delete_admin(self, account_id, user_id, role):
        """
        delete given user with assigned role in given account_id
        """
        url = "/api/v1/accounts/%s/admins/%s?role=%s" \
            % (account_id, user_id, quote(role))
        dao = Canvas_DAO()
        delete_response = dao.deleteURL(url, {})

        if not (delete_response.status == 200 or delete_response.status == 204):
            raise DataFailureException(url, delete_response.status,
                                       delete_response.data)

        return delete_response.status

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
        return representation of the requested resource,
        chasing pagination links to coalesce resources
        """
        response = Canvas_DAO().getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        if isinstance(data, list):
            next_page = self._next_page(response)
            if next_page:
                data.extend(self._get_resource(next_page))

        return data

    def create_course(self, subaccount_id, course_name):
        """
        Create a canvas course with the given subaccount id and course name
        """
        url = "/api/v1/accounts/%s/courses" % subaccount_id
        dao = Canvas_DAO()
        post_response = dao.postURL(url, {"Content-Type": "application/json"},
                                    json.dumps({"course": {"name": course_name}}))

        if not (post_response.status == 200 or post_response.status == 204):
            raise DataFailureException(url, post_response.status,
                                       post_response.data)

        return json.loads(post_response.data)

    def create_course_section(self, course_id, sis_section_id, section_name):
        """
        Create a canvas course section with the given section name and id
        """
        url = "/api/v1/courses/%s/sections" % course_id
        dao = Canvas_DAO()
        post_response = dao.postURL(url, {"Content-Type": "application/json"},
                                    json.dumps({"course_section": {"name": section_name,
                                                                   "sis_section_id": sis_section_id}}))

        if not (post_response.status == 200 or post_response.status == 204):
            raise DataFailureException(url, post_response.status,
                                       post_response.data)

        return json.loads(post_response.data)

    def get_user(self, user_regid):
        """
        Fetches a user profile
        """
        url = "/api/v1/users/sis_user_id:%s/profile" % user_regid
        dao = Canvas_DAO()
        get_response = dao.getURL(url, {"Content-Type": "application/json"})

        if not (get_response.status == 200 or get_response.status == 204):
            raise DataFailureException(url, get_response.status,
                                       get_response.data)

        return json.loads(get_response.data)

    def add_user(self, **kwargs):
        """
        Creates a new user
        """
        url = "/api/v1/accounts/%s/users" % kwargs['account_id']
        dao = Canvas_DAO()
        params = {"pseudonym": {"unique_id": kwargs["login_id"],
                                "send_confirmation": "0"}}

        if "sis_id" in kwargs and kwargs["sis_id"]:
            params["pseudonym"]["sis_user_id"] = kwargs["sis_id"]

        for user_key in ['name', 'short_name', 'sortable_name', 'locale', 'birthdate']:
            if user_key in kwargs and kwargs[user_key]:
                if "user" not in params:
                    params["user"] = {}

                params["user"][user_key] = kwargs[user_key]

        post_response = dao.postURL(url, {"Content-Type": "application/json"},
                                    json.dumps(params))

        if not (post_response.status == 200 or post_response.status == 204):
            raise DataFailureException(url, post_response.status,
                                       post_response.data)

        return json.loads(post_response.data)

    def enroll_user(self, course_id, user_id):
        """
        Enroll a user into a course
        """
        url = "/api/v1/courses/%s/enrollments" % course_id
        dao = Canvas_DAO()
        post_response = dao.postURL(url, {"Content-Type": "application/json"},
                                    json.dumps({"enrollment": {"user_id": user_id,
                                                               "type": "TeacherEnrollment"},
                                                "enrollment_state": "active"}))

        if not (post_response.status == 200 or post_response.status == 204):
            raise DataFailureException(url, post_response.status,
                                       post_response.data)

        return post_response.status

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
