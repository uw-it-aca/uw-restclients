from django.test import TestCase
from restclients.canvas.users import Users
from restclients.models.canvas import CanvasUser


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
            self.assertEquals(user.avatar_url, "https://en.gravatar.com/avatar/d8cb8c8cd40ddf0cd05241443a591868?s=80&r=g", "Has correct avatar url")

    def test_create_user(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Users()

            new_user = CanvasUser(name="J AVG USR",
                login_id="testid99",
                sis_user_id="DEB35E0A465242CF9C5CDBC108050EC0",
                email="testid99@foo.com",
                locale="en")

            account_id = 88888
            user = canvas.create_user(new_user, account_id)

            self.assertEquals(user.name, "J AVG USR", "Has correct name")
            self.assertEquals(user.short_name, None, "Has correct short name")
            self.assertEquals(user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
                              "Has correct sis id")
            self.assertEquals(user.email, "testid99@foo.com", "Has correct email")

    def test_get_logins(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Users()

            user_id = 188885
            sis_user_id = "DEB35E0A465242CF9C5CDBC108050EC0"
            logins = canvas.get_user_logins(user_id)

            self.assertEquals(len(logins), 2, "Has correct login count")

            login = logins[0]
            self.assertEquals(login.user_id, user_id, "Has correct user id")
            self.assertEquals(login.login_id, 100, "Has correct login_id")
            self.assertEquals(login.sis_user_id, sis_user_id, "Has correct sis id")
            self.assertEquals(login.unique_id, "testid99", "Has correct unique id")


            logins = canvas.get_user_logins_by_sis_id(sis_user_id)

            self.assertEquals(len(logins), 2, "Has correct login count")

            login = logins[0]
            self.assertEquals(login.user_id, user_id, "Has correct user id")
            self.assertEquals(login.login_id, 100, "Has correct login_id")
            self.assertEquals(login.sis_user_id, sis_user_id, "Has correct sis id")
            self.assertEquals(login.unique_id, "testid99", "Has correct unique id")

    def test_update_login(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Users()

            user_id = 188885
            logins = canvas.get_user_logins(user_id)

            login = logins[0]
            login.unique_id = "testid99new"
            login.sis_user_id = ""

            new_login = canvas.update_user_login(login, account_id=12345)
            self.assertEquals(new_login.unique_id, login.unique_id, "Has correct unique id")
            self.assertEquals(new_login.sis_user_id, login.sis_user_id, "Has correct sis id")
