from restclients.canvas import Canvas
from restclients.models.canvas import CanvasRole, CanvasAccount
from urllib import quote


class Roles(Canvas):
    def get_roles_in_account(self, account_id, params={}):
        """
        List the roles available to an account, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index
        """
        url = "/api/v1/accounts/%s/roles%s" % (account_id, self._params(params))
        roles = []
        for datum in self._get_resource(url):
            roles.append(self._role_from_json(datum))
        return roles

    def get_roles_by_account_sis_id(self, account_sis_id, params={}):
        """
        List the roles available to an account, for the passed account SIS ID.
        """
        return self.get_roles_in_account(self._sis_id(account_sis_id,
                                                      sis_field="account"),
                                         params)

    def get_role(self, account_id, role_id):
        """
        Get information about a single role, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show
        """
        url = "/api/v1/accounts/%s/roles/%s" % (account_id, role_id)
        return self._role_from_json(self._get_resource(url))

    def get_role_by_account_sis_id(self, account_sis_id, role_id):
        """
        Get information about a single role, for the passed account SIS ID.
        """
        return self.get_role(self._sis_id(account_sis_id, sis_field="account"),
                             role_id)

    def _role_from_json(self, data):
        role = CanvasRole() 
        role.role = data["role"]
        role.role_id = data["id"]
        role.base_role_type = data["base_role_type"]
        role.workflow_state = data["workflow_state"]
        role.permissions = data.get("permissions", {})
        if "account" in data:
            role.account = CanvasAccount(data["account"])
        return role
