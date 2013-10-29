from django.test import TestCase
from django.conf import settings
from restclients.canvas.admins import Admins
from restclients.exceptions import DataFailureException

class CanvasTestAdmins(TestCase):
    def test_admins(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):

            canvas = Admins()

            admins = canvas.get_admins_by_sis_id('uwcourse:seattle:nursing:nurs')

            self.assertEquals(len(admins), 11, "Failed to follow Link header")

            admin = admins[10]

            self.assertEquals(admin.role, 'AccountAdmin', "Has proper role")
            self.assertEquals(admin.user.user_id, 1111, "Has proper id")

    def test_create_admin(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Admins()

            admin = canvas.create_admin_by_sis_id('uwcourse:seattle:nursing:nurs', 1111, 'AccountAdmin')

            self.assertEquals(admin.user.user_id, 1111, "Has proper id")
            self.assertEquals(admin.role, 'AccountAdmin', "Has proper role")

    def test_delete_admin(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):

            canvas = Admins()

            status = canvas.delete_admin_by_sis_id('uwcourse:seattle:nursing:nurs', 1111, 'AccountAdmin')
            self.assertEquals(status, True, "Return OK")
