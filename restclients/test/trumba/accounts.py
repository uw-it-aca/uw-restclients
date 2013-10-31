from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.trumba.account import Account
from restclients.trumba.exceptions import AccountNameEmpty, AccountNotExist, AccountUsedByDiffUser, CalendarNotExist, CalendarOwnByDiffAccount, InvalidEmail, InvalidPermissionLevel, FailedToClosePublisher, NoAllowedPermission, ErrorCreatingEditor, NoDataReturned, UnknownError

class TrumbaTestAccounts(TestCase):

    def test_add_editor_error_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertRaises(AccountNameEmpty, 
                              Account.add_editor,'','')
            
            self.assertRaises(InvalidEmail,
                              Account.add_editor,'010','')

            self.assertRaises(AccountUsedByDiffUser,
                              Account.add_editor,'011','test10')


    def test_add_editor_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertTrue(Account.add_editor('008','test8'))

            self.assertTrue(Account.add_editor('010','test10'))



