"""
This is the interface for interacting with Instructure's Canvas web services.
"""

from restclients.dao import Canvas_DAO
from restclients.models import CanvasEnrollment, CanvasCourse
from restclients.exceptions import DataFailureException
from urllib import quote
import json
import re


DEFAULT_PAGINATION = 0


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

    def sis_course_id(self, sis_id):
        return self._sis_id(sis_id, sis_field='course')

    def sis_section_id(self, sis_id):
        return self._sis_id(sis_id, sis_field='section')

    def sis_user_id(self, sis_id):
        return self._sis_id(sis_id, sis_field='user')

    def get_course_section(self, course_id, section_id):
        return self._get_resource("/api/v1/courses/%s/sections/%s"
                                  % (course_id, section_id))

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

    def get_sub_accounts_by_canvas_id(self, canvas_id, params={}):
        return self._get_sub_accounts(canvas_id, params)

    def get_sub_accounts_by_sis_id(self, sis_id, params={}):
        return self._get_sub_accounts(self._sis_id(sis_id), params)

    def get_all_sub_accounts_by_canvas_id(self, canvas_id):
        #uncomment when instructure fixes pagination in recursion
        #params = self._pagination({'recursive': 'true'})
        #return self._get_sub_accounts(canvas_id, params)
        subs = self.get_sub_accounts_by_canvas_id(canvas_id)
        return self._recurse_sub_accounts(subs, [])

    def get_all_sub_accounts_by_sis_id(self, sis_id):
        #uncomment when instructure fixes pagination in recursion
        #params = self._pagination({'recursive': 'true'})
        #return self._get_sub_accounts(self._sis_id(sis_id), params)
        subs = self.get_sub_accounts_by_sis_id(sis_id)
        return self._recurse_sub_accounts(subs, [])

    def _get_sub_accounts(self, id, params):
        """
        return list of sub accounts within the given account
        """
        params = self._pagination(params)
        return self._get_resource("/api/v1/accounts/%s/sub_accounts%s"
                                  % (id, self._params(params)))

    def _recurse_sub_accounts(self, sub_accounts, account_list):
        account_list.extend(sub_accounts)
        for account in sub_accounts:
            subs = self.get_sub_accounts_by_canvas_id(account['id'])
            self._recurse_sub_accounts(subs, account_list)

        return account_list

    def get_courses_in_account_by_canvas_id(self, canvas_id, params={}):
        return self._get_courses_in_account(canvas_id, params)

    def get_courses_in_account_by_sis_id(self, sis_id, params={}):
        return self._get_courses_in_account(self._sis_id(sis_id), params)

    def get_published_courses_in_account_by_canvas_id(self, canvas_id):
        return self._get_courses_in_account(canvas_id, {'published': True})

    def get_published_courses_in_account_by_sis_id(self, sis_id):
        return self._get_courses_in_account(self._sis_id(sis_id),
                                            {'published': True})

    def _get_courses_in_account(self, id, params):
        """
        return list of admins in given account
        """
        params = self._pagination(params)
        url = "/api/v1/accounts/%s/courses%s" % (id, self._params(params))

        return self._get_resource(url)

    def get_admins_by_canvas_id(self, canvas_id):
        return self._get_admins(canvas_id)

    def get_admins_by_sis_id(self, sis_id):
        return self._get_admins(self._sis_id(sis_id))

    def _get_admins(self, id):
        """
        return list of admins in given account
        """
        params = self._pagination({})
        return self._get_resource("/api/v1/accounts/%s/admins%s"
                                  % (id, self._params(params)))

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
            params['per_page'] = self._per_page

        return params

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
