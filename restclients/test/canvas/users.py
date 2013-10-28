from django.test import TestCase
from restclients.canvas.users import Users
from restclients.models.canvas import User


class CanvasTestUsers(TestCase):
    def test_get_user(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Users()

            user = canvas.get_user(188885)

            self.assertEquals(user.user_id, 188885, "Has correct user id")
            self.assertEquals(user.name, "J AVG USR", "Has correct name")
            self.assertEquals(user.short_name, None, "Has correct short name")
            self.assertEquals(user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
                              "Has correct sis id")
            self.assertEquals(user.email, "testid99@foo.com", "Has correct email")

            user = canvas.get_user_by_sis_id("DEB35E0A465242CF9C5CDBC108050EC0")

            self.assertEquals(user.user_id, 188885, "Has correct user id")
            self.assertEquals(user.name, "J AVG USR", "Has correct name")
            self.assertEquals(user.short_name, None, "Has correct short name")
            self.assertEquals(user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
                              "Has correct sis id")
            self.assertEquals(user.email, "testid99@foo.com", "Has correct email")

    def test_create_user(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Users()

            new_user = User(name="J AVG USR", login_id="testid99",
                            sis_user_id="DEB35E0A465242CF9C5CDBC108050EC0",
                            email="testid99@foo.com", locale="en")

            account_id = 88888
            user = canvas.create_user(new_user, account_id)

            self.assertEquals(user.name, "J AVG USR", "Has correct name")
            self.assertEquals(user.short_name, None, "Has correct short name")
            self.assertEquals(user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
                              "Has correct sis id")
            self.assertEquals(user.email, "testid99@foo.com", "Has correct email")
