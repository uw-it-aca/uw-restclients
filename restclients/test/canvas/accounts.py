from django.test import TestCase
from django.conf import settings
from restclients.canvas.accounts import Accounts as Canvas
from restclients.exceptions import DataFailureException

class CanvasTestAccounts(TestCase):

    def test_account(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            account = canvas.get_account_by_sis_id('uwcourse:seattle:cse:cse')
            self.assertEquals(account.account_id, 696969)
            self.assertEquals(account.name, "Computer Science & Engineering", "Has proper name")
            self.assertEquals(account.sis_account_id, 'uwcourse:seattle:cse:cse')
            self.assertEquals(account.parent_account_id, 987654)

    def test_sub_account(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            accounts = canvas.get_sub_accounts_by_sis_id('uwcourse:seattle:cse')

            account = accounts[1]

            self.assertEquals(len(accounts), 3, "Too few accounts")
            self.assertEquals(account.name, "Comp Sci & Engr Accelerated Masters Prg", "Has proper name")
            self.assertEquals(account.sis_account_id, 'uwcourse:seattle:cse:csem')
            self.assertEquals(account.parent_account_id, 54321)

    def test_all_sub_accounts(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            accounts = canvas.get_all_sub_accounts_by_sis_id('uwcourse:seattle:cse')

            account = accounts[1]

            self.assertEquals(len(accounts), 3, "Too few accounts")
            self.assertEquals(account.name, "Comp Sci & Engr Accelerated Masters Prg", "Has proper name")
            self.assertEquals(account.sis_account_id, 'uwcourse:seattle:cse:csem')
            self.assertEquals(account.parent_account_id, 54321)
