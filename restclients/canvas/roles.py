from restclients.canvas import Canvas
from restclients.models.canvas import CanvasRole, CanvasAccount
from urllib import quote


class Roles(Canvas):
    def get_roles_in_account(self, account_id):
        """
        List the roles available to an account, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index
        """
        url = "/api/v1/accounts/%s/roles" % account_id

        roles = []
        for datum in self._get_resource(url):
            roles.append(self._role_from_json(datum))
        return roles

    def get_roles_by_account_sis_id(self, account_sis_id):
        """
        List the roles available to an account, for the passed account SIS ID.
        """
        return self.get_roles_in_account(self._sis_id(account_sis_id,
                                                      sis_field="account"))

    def get_role(self, account_id, role):
        """
        Get information about a single role, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show
        """
        url = "/api/v1/accounts/%s/roles/%s" % (account_id, quote(role))
        return self._role_from_json(self._get_resource(url))

    def get_role_by_account_sis_id(self, account_sis_id, role):
        """
        Get information about a single role, for the passed account SIS ID.
        """
        return self.get_role(self._sis_id(account_sis_id, sis_field="account"),
                             role)

    def _role_from_json(self, data):
        role = CanvasRole()
        role.role = data["role"]
        role.base_role_type = data["base_role_type"]
        role.workflow_state = data["workflow_state"]
        role.permissions = data.get("permissions", {})
        role.account = CanvasAccount(data["account"])
        return role
