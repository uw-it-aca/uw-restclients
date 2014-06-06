from datetime import datetime
from django.test import TestCase
from django.conf import settings
from restclients.hfs.idcard import get_hfs_accounts
from restclients.exceptions import DataFailureException

class HfsTest(TestCase):

    def test_get_hfs_accounts(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            hfs_acc = get_hfs_accounts("javerage")
            self.assertEquals(hfs_acc.student_husky_card.last_updated,
                              datetime(2014, 6, 2, 15, 17, 16))
            self.assertEquals(hfs_acc.student_husky_card.balance, 1.23)
            self.assertEquals(hfs_acc.student_husky_card.add_funds_url, 
                              "https://www.hfs.washington.edu/olco")

            self.assertEquals(hfs_acc.employee_husky_card.last_updated,
                              datetime(2014, 5, 19, 14, 16, 26))
            self.assertEquals(hfs_acc.employee_husky_card.balance, 0.56)
            self.assertEquals(hfs_acc.employee_husky_card.add_funds_url, 
                              "https://www.hfs.washington.edu/olco")

            self.assertEquals(hfs_acc.resident_dining.last_updated,
                              datetime(2014, 6, 1, 13, 15, 36))
            self.assertEquals(hfs_acc.resident_dining.balance, 7.89)
            self.assertEquals(hfs_acc.resident_dining.add_funds_url, 
                              "https://www.hfs.washington.edu/olco")


    def test_get_hfs_empty_account(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            hfs_acc = get_hfs_accounts("none")
            self.assertIsNone(hfs_acc.student_husky_card)
            self.assertIsNone(hfs_acc.employee_husky_card)
            self.assertIsNone(hfs_acc.resident_dining)


    def test_get_hfs_partially_empty_account(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            hfs_acc = get_hfs_accounts("jnewstudent")
            self.assertEquals(hfs_acc.student_husky_card.balance, 0.00)
            self.assertEquals(hfs_acc.student_husky_card.last_updated,
                              datetime(2014, 1, 15, 15, 17, 16))
            self.assertEquals(hfs_acc.student_husky_card.add_funds_url, 
                              "https://www.hfs.washington.edu/olco")

            self.assertIsNone(hfs_acc.employee_husky_card)

            self.assertEquals(hfs_acc.resident_dining.balance, 777.89)
            self.assertEquals(hfs_acc.resident_dining.last_updated,
                              datetime(2014, 5, 17, 13, 15, 36))
            self.assertEquals(hfs_acc.resident_dining.add_funds_url, 
                              "https://www.hfs.washington.edu/olco")



    def test_invalid_user(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            #Testing error message in a 200 response
            self.assertRaises(DataFailureException, get_hfs_accounts, "invalidnetid")
            #Testing non-200 response
            self.assertRaises(DataFailureException, get_hfs_accounts, "invalidnetid123")

            try:
                get_hfs_accounts("invalidnetid")
            except DataFailureException as ex:
                self.assertEquals(ex.msg, "An error has occurred.")

