from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.trumba.account import Account
from restclients.trumba.exceptions import AccountNameEmpty, AccountNotExist, AccountUsedByDiffUser, CalendarNotExist, CalendarOwnByDiffAccount, InvalidEmail, InvalidPermissionLevel, FailedToClosePublisher, NoAllowedPermission, ErrorCreatingEditor, NoDataReturned, UnknownError, UnexpectedError

class TrumbaTestAccounts(TestCase):

    def test_make_add_editor_url(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertEqual(Account._make_add_editor_url('Margaret Murray', 'murray4'),
                             "/service/accounts.asmx/CreateEditor?Name=Margaret%20Murray&Email=murray4@washington.edu&Password=")


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

    def test_is_permission_set(self):
        self.assertTrue(Account._is_permission_set(1003))
        self.assertFalse(Account._is_permission_set(-1003))

    def test_is_editor_added(self):
        self.assertTrue(Account._is_editor_added(1001))
        self.assertTrue(Account._is_editor_added(3012))
        self.assertFalse(Account._is_editor_added(-1001))

    def test_is_editor_deleted(self):
        self.assertTrue(Account._is_editor_deleted(1002))
        self.assertFalse(Account._is_editor_deleted(-1002))

    def test_check_err(self):
        self.assertRaises(CalendarNotExist,
                          Account._check_err,
                          3006)

        self.assertRaises(CalendarOwnByDiffAccount,
                          Account._check_err,
                          3007)

        self.assertRaises(AccountNotExist,
                          Account._check_err,
                          3008)

        self.assertRaises(AccountUsedByDiffUser,
                          Account._check_err,
                          3009)

        self.assertRaises(AccountUsedByDiffUser,
                          Account._check_err,
                          3013)

        self.assertRaises(InvalidPermissionLevel,
                          Account._check_err,
                          3010)

        self.assertRaises(FailedToClosePublisher,
                          Account._check_err,
                          3011)

        self.assertRaises(InvalidEmail,
                          Account._check_err,
                          3014)

        self.assertRaises(NoAllowedPermission,
                          Account._check_err,
                          3015)

        self.assertRaises(AccountNameEmpty,
                          Account._check_err,
                          3016)

        self.assertRaises(ErrorCreatingEditor,
                          Account._check_err,
                          3017)

        self.assertRaises(ErrorCreatingEditor,
                          Account._check_err,
                          3018)

        self.assertRaises(UnexpectedError,
                          Account._check_err,
                          3020)
