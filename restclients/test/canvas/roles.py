from django.test import TestCase
from django.conf import settings
from restclients.canvas import Canvas
from restclients.exceptions import DataFailureException

class CanvasTestRoles(TestCase):

    def test_roles(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            roles = canvas.get_roles_by_canvas_id(12345)

            self.assertEquals(len(roles), 15, "Failed to follow Link header")

            role = roles[10]

            self.assertEquals(role.get('role'), "Course Access")
            self.assertEquals(role.get('permissions').get('read_course_list').get('enabled'), True)

    def test_role(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            role = canvas.get_role_by_canvas_id(12345, 'Course Access')

            self.assertEquals(role.get('role'), "Course Access")
            self.assertEquals(role.get('permissions').get('read_course_list').get('enabled'), True)
