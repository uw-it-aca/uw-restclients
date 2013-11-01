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


    def test_delete_editor_error_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertRaises(AccountNotExist, 
                              Account.delete_editor,'')
            
            self.assertRaises(AccountNotExist,
                              Account.delete_editor,'test')


    def test_delete_editor_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertTrue(Account.delete_editor('test10'))

    def test_set_sea_permissions_error_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertRaises(AccountNotExist,
                              Account.set_sea_permissions, 1, '', 'EDIT')

            self.assertRaises(NoAllowedPermission,
                              Account.set_sea_permissions, 1, 'test10', 'PUBLISH')

    def test_set_sea_permissions_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertTrue(Account.set_sea_permissions(1, 'test10', 'SHOWON'))

            self.assertTrue(Account.set_sea_permissions(1, 'test10', 'EDIT'))

