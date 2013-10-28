from django.conf import settings
from restclients.canvas import Canvas
from restclients.dao import Canvas_DAO
from restclients.models.canvas import User
from restclients.exceptions import DataFailureException
import json


class Users(Canvas):
    def get_user(self, user_id):
        """
        Returns user profile data.

        https://canvas.instructure.com/doc/api/users.html#method.profile.settings
        """
        url = "/api/v1/users/%s/profile" % user_id
        return self._user_from_json(self._get_resource(url))

    def get_user_by_sis_id(self, sis_user_id):
        """
        Returns user profile data for the passed user sis id.
        """
        return self.get_user(self._sis_id(sis_user_id, sis_field="user"))

    def create_user(self, user,
                    account_id=settings.RESTCLIENTS_CANVAS_ACCOUNT_ID):
        """
        Create and return a new user and pseudonym for an account.

        https://canvas.instructure.com/doc/api/users.html#method.users.create
        """
        url = "/api/v1/accounts/%s/users" % account_id
        body = json.dumps(user.post_data())

        dao = Canvas_DAO()
        response = dao.postURL(url, {"Content-Type": "application/json"}, body)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return self._user_from_json(json.loads(response.data))

    def _user_from_json(self, data):
        user  = User()
        user.user_id = data["id"]
        user.name = data["name"]
        user.short_name = data["short_name"] if "short_name" in data else None
        user.sortable_name = data["sortable_name"] if "sortable_name" in data else None
        user.login_id = data["login_id"] if "login_id" in data else None
        user.sis_user_id = data["sis_user_id"] if "sis_user_id" in data else None
        user.email = data["email"] if "email" in data else None
        user.time_zone = data["time_zone"] if "time_zone" in data else None
        user.locale = data["locale"] if "locale" in data else None
        return user
