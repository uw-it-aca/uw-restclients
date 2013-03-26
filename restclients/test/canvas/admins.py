from django.test import TestCase
from django.conf import settings
from restclients.canvas import Canvas
from restclients.exceptions import DataFailureException

class CanvasTestAdmins(TestCase):

    def test_admins(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):

            canvas = Canvas()

            admins = canvas.get_admins_by_sis_id('uwcourse:seattle:nursing:nurs')

            self.assertEquals(len(admins), 11, "Failed to follow Link header")

            admin = admins[10]

            self.assertEquals(admin.get('role'), 'AccountAdmin', "Has proper role")
            self.assertEquals(admin.get('user').get('id'), 1111, "Has proper id")

