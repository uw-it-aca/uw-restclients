from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
import restclients.trumba.account as Account
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
                          3006, 'test if CalendarNotExist is thrown')

        self.assertRaises(CalendarOwnByDiffAccount,
                          Account._check_err,
                          3007, 'test if CalendarOwnByDiffAccount is thrown')

        self.assertRaises(AccountNotExist,
                          Account._check_err,
                          3008, 'test if AccountNotExist is thrown')

        self.assertRaises(AccountUsedByDiffUser,
                          Account._check_err,
                          3009, 'test if AccountUsedByDiffUser is thrown')

        self.assertRaises(AccountUsedByDiffUser,
                          Account._check_err,
                          3013, 'test if AccountUsedByDiffUser is thrown')

        self.assertRaises(InvalidPermissionLevel,
                          Account._check_err,
                          3010, 'test if InvalidPermissionLevel is thrown')

        self.assertRaises(FailedToClosePublisher,
                          Account._check_err,
                          3011, 'test if FailedToClosePublisher is thrown')

        self.assertRaises(InvalidEmail,
                          Account._check_err,
                          3014, 'test if InvalidEmail is thrown')

        self.assertRaises(NoAllowedPermission,
                          Account._check_err,
                          3015, 'test if NoAllowedPermission is thrown')

        self.assertRaises(AccountNameEmpty,
                          Account._check_err,
                          3016, 'test if AccountNameEmpty is thrown')

        self.assertRaises(ErrorCreatingEditor,
                          Account._check_err,
                          3017, 'test if ErrorCreatingEditor is thrown')

        self.assertRaises(ErrorCreatingEditor,
                          Account._check_err,
                          3018, 'test if ErrorCreatingEditor is thrown')

        self.assertRaises(UnexpectedError,
                          Account._check_err,
                          3020, 'test if UnexpectedError is thrown')
