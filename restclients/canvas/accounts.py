from restclients.canvas import Canvas
from restclients.models.canvas import Account


class Accounts(Canvas):
    def get_account(self, account_id):
        """
        Return account resource for given canvas account id.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show
        """
        url = "/api/v1/accounts/%s" % account_id
        return self._account_from_json(self._get_resource(url))

    def get_account_by_sis_id(self, sis_id):
        """
        Return account resource for given sis id.
        """
        return self.get_account(self._sis_id(sis_id))

    def get_sub_accounts(self, account_id, params):
        """
        Return list of subaccounts within the account with the passed canvas id.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.sub_accounts
        """
        params = self._pagination(params)
        url = "/api/v1/accounts/%s/sub_accounts%s" % (account_id,
                                                      self._params(params))

        accounts = []
        for datum in self._get_resource(url):
            accounts.append(self._account_from_json(datum))

        return accounts

    def get_sub_accounts_by_sis_id(self, sis_id):
        """
        Return list of subaccounts within the account with the passed sis id.
        """
        return self.get_sub_accounts(self._sis_id(sis_id), params={})

    def get_all_sub_accounts(self, account_id):
        """
        Return a recursive list of subaccounts within the account with
        the passed canvas id.
        """
        return self.get_sub_accounts(account_id,
                                     params={"recursive": "true"})

    def get_all_sub_accounts_by_sis_id(self, sis_id):
        """
        Return a recursive list of subaccounts within the account with
        the passed sis id.
        """
        return self.get_sub_accounts(self._sis_id(sis_id),
                                     params={"recursive": "true"})

    def update_account(self, account):
        """
        Update the passed account. Returns the updated account.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update
        """
        url = "/api/v1/accounts/%s" % account.account_id
        body = {"account": {"name": account.name}}

        data = self._put_resource(url, body)
        return self._account_from_json(data)

    def _account_from_json(self, data):
        account = Account()
        account.account_id = data["id"]
        account.sis_account_id = data["sis_account_id"] if "sis_account_id" in data else None
        account.name = data["name"]
        account.parent_account_id = data["parent_account_id"]
        account.root_account_id = data["root_account_id"]
        return account
