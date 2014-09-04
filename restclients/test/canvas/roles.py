from django.test import TestCase
from django.conf import settings
from restclients.canvas.roles import Roles
from restclients.exceptions import DataFailureException


class CanvasTestRoles(TestCase):

    def test_roles(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Roles()

            roles = canvas.get_roles_in_account(12345)

            self.assertEquals(len(roles), 15, "Failed to follow Link header")

            role = roles[10]

            self.assertEquals(role.role, "Course Access")
            self.assertEquals(role.permissions.get('read_course_list').get('enabled'), True)

    def test_role(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Roles()

            role = canvas.get_role(12345, 'Course Access')

            self.assertEquals(role.role, "Course Access")
            self.assertEquals(role.permissions.get('read_course_list').get('enabled'), True)
