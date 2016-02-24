from datetime import datetime
from django.test import TestCase
from django.conf import settings
from restclients.hfs.idcard import get_hfs_accounts
from restclients.exceptions import DataFailureException
from decimal import  *


ADD_FUND_URL =\
    "https://www.hfs.washington.edu/olco/Secure/AccountSummary.aspx"


class HfsTest(TestCase):

    def test_get_hfs_accounts(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            hfs_acc = get_hfs_accounts("javerage")
            self.assertEquals(hfs_acc.student_husky_card.last_updated,
                              datetime(2014, 6, 2, 15, 17, 16))
            self.assertEquals(hfs_acc.student_husky_card.balance,
                              Decimal('1.23'))
            self.assertEquals(
                hfs_acc.student_husky_card.add_funds_url,
                ADD_FUND_URL)

            self.assertEquals(hfs_acc.employee_husky_card.last_updated,
                              datetime(2014, 5, 19, 14, 16, 26))
            self.assertEquals(hfs_acc.employee_husky_card.balance,
                              Decimal('0.56'))
            self.assertEquals(hfs_acc.employee_husky_card.add_funds_url,
                              ADD_FUND_URL)

            self.assertEquals(hfs_acc.resident_dining.last_updated,
                              datetime(2014, 6, 1, 13, 15, 36))
            self.assertEquals(hfs_acc.resident_dining.balance, Decimal('7.89'))
            self.assertEquals(hfs_acc.resident_dining.add_funds_url,
                              ADD_FUND_URL)


    def test_get_hfs_empty_account(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            hfs_acc = get_hfs_accounts("eight")
            self.assertIsNotNone(hfs_acc.student_husky_card)
            self.assertIsNone(hfs_acc.employee_husky_card)
            self.assertIsNotNone(hfs_acc.resident_dining)


    def test_get_hfs_partially_empty_account(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            hfs_acc = get_hfs_accounts("jnew")
            self.assertIsNotNone(hfs_acc.student_husky_card)
            self.assertIsNone(hfs_acc.student_husky_card.last_updated)
            self.assertEquals(hfs_acc.student_husky_card.balance,
                              Decimal('0.0'))

            self.assertIsNone(hfs_acc.employee_husky_card)

            self.assertEquals(hfs_acc.resident_dining.balance,
                              Decimal('777.89'))
            self.assertEquals(hfs_acc.resident_dining.last_updated,
                               datetime(2014, 5, 17, 13, 15, 36))
            self.assertEquals(hfs_acc.resident_dining.add_funds_url,
                              ADD_FUND_URL)


    def test_invalid_user(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS =
            'restclients.dao_implementation.hfs.File'):

            #Testing error message in a 200 response
            self.assertRaises(DataFailureException,
                              get_hfs_accounts, "invalidnetid")
            self.assertRaises(DataFailureException,
                              get_hfs_accounts, "invalidnetid123")

            try:
                get_hfs_accounts("jerror")
            except DataFailureException as ex:
                self.assertEquals(ex.status, 500)
                self.assertEquals(ex.msg,
                                  "An error has occurred.")
            try:
                get_hfs_accounts("none")
            except DataFailureException as ex:
                self.assertEquals(ex.status, 404)
                self.assertEquals(ex.msg,
                                  "UWNetID none not found in IDCard Database.")

            MSG = "%s%s%s" % (
                "Input for this method must be either a valid UWNetID ",
                "or two nine-digit Student and ",
                "Faculty/Staff/Employee ID numbers, comma-separated.")
            try:
                get_hfs_accounts("invalidnetid")
            except DataFailureException as ex:
                self.assertEquals(ex.status, 400)
                self.assertEquals(
                    ex.msg, MSG)

    def test_float_parsing(self):
        with self.settings(
            RESTCLIENTS_HFS_DAO_CLASS=
            'restclients.dao_implementation.hfs.File'):
            hfs_acc = get_hfs_accounts("jbothell")
            self.assertEquals(hfs_acc.student_husky_card.balance,
                              Decimal('5.1'))
