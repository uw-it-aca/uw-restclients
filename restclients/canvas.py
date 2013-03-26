"""
This is the interface for interacting with Instructure's Canvas web services.
"""

from restclients.dao import Canvas_DAO
from restclients.models import CanvasEnrollment, CanvasCourse
from restclients.exceptions import DataFailureException
from urllib import quote
import json
import re


class Canvas(object):
    """
    The Canvas object has methods for getting information
    about accounts, courses, enrollments and users within
    Canvas
    """
    def __init__(self):
        """
        Prepares for paginated responses
        """
        self._re_next_link = re.compile(r"""<http[s]?://[^/]+([^>]*)>;\s*
                                            rel=([\"\']?)next\2 # next doc
                                         """,
                                        re.I | re.X)

    def get_courses_for_regid(self, regid):
        data = self._get_resource("/api/v1/courses.json?as_user_id=%s"
                                  % self._sis_id(regid, sis_field='user'))
        courses = []

        for section in data:
            course_id = section["id"]
            course_info = self.get_course_info_by_canvas_id(course_id)

            if course_info["sis_course_id"] is not None:
                course_url = section["calendar"]["ics"]
                course_url = re.sub(r"(.*?[a-z]/).*", r"\1", course_url)
                course_url = "%scourses/%s" % (course_url, course_id)

                course = CanvasCourse()
                course.course_url = course_url
                course.course_name = course_info["name"]
                course.sis_id = course_info["sis_course_id"]

                courses.append(course)

        return courses

    def get_enrollments_for_regid(self, regid):
        data = self._get_resource("/api/v1/users/%s/enrollments"
                                  % self._sis_id(regid, sis_field='user'))
        enrollments = []

        for section in data:
            course_id = section["course_id"]
            course_info = self.get_course_info_by_canvas_id(course_id)

            if course_info["sis_course_id"] is not None:
                user_url = section["html_url"]
                course_url = re.sub("/users/.*", "", user_url)
                enrollment = CanvasEnrollment()
                enrollment.course_url = course_url
                enrollment.course_name = course_info["name"]
                enrollment.sis_id = course_info["sis_course_id"]

                enrollments.append(enrollment)
        return enrollments

    def get_course_info_by_canvas_id(self, canvas_id):
        return self._get_course(canvas_id)

    def get_course_info_by_sis_id(self, sis_id):
        return self._get_course(self._sis_id(sis_id, sis_field='course'))

    def _get_course(self, id):
        return self._get_resource("/api/v1/courses/%s" % id)

    def get_account_by_canvas_id(self, canvas_id):
        return self._get_account(canvas_id)

    def get_account_by_sis_id(self, sis_id):
        return self._get_account(self._sis_id(sis_id))

    def _get_account(self, id):
        """
        return account resource for given account id
        """
        return self._get_resource("/api/v1/accounts/%s" % id)

    def update_account_by_canvas_id(self, canvas_id, resource):
        return self._update_account(canvas_id, resource)

    def update_account_by_sis_id(self, sis_id, resource):
        return self._update_account(self._sis_id(sis_id), resource)

    def _update_account(self, id, resource):
        """
        update given account with given account resource
        """
        url = "/api/v1/accounts/%s" % id

        dao = Canvas_DAO()
        put_response = dao.putURL(url, {"Content-Type": "application/json"},
                                  json.dumps(resource))

        if not (put_response.status == 200 or put_response.status == 204):
            raise DataFailureException(url, put_response.status,
                                       put_response.data)

        return put_response.status

    def get_sub_accounts_by_canvas_id(self, canvas_id):
        return self._get_sub_accounts(canvas_id)

    def get_sub_accounts_by_sis_id(self, sis_id):
        return self._get_sub_accounts(self._sis_id(sis_id))

    def _get_sub_accounts(self, id):
        """
        return list of sub accounts within the given account
        """
        return self._get_resource("/api/v1/accounts/%s/sub_accounts" % id)

    def get_admins_by_canvas_id(self, canvas_id):
        return self._get_admins(canvas_id)

    def get_admins_by_sis_id(self, sis_id):
        return self._get_admins(self._sis_id(sis_id))

    def _get_admins(self, id):
        """
        return list of admins in given account
        """
        return self._get_resource("/api/v1/accounts/%s/admins" % id)

    def delete_admin_by_canvas_id(self, canvas_id, user_id, role):
        return self._delete_admin(canvas_id, user_id, role)

    def delete_admin_by_sis_id(self, sis_id, user_id, role):
        return self._delete_admin(self._sis_id(sis_id), user_id, role)

    def _delete_admin(self, account_id, user_id, role):
        """
        delete given user with assigned role in given account_id
        """
        url = "/api/v1/accounts/%s/admins/%s?role=%s" \
            % (account_id, user_id, quote(role))
        dao = Canvas_DAO()
        delete_response = dao.deleteURL(url, {})

        if delete_response.status != 204:
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

    def _next_page(self, response):
        """
        return url path to next page of paginated data
        """
        link = self._re_next_link.match(response.getheader('link', ''))
        return link.group(1).replace(':', '%3A') if link else None

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
