from django.test import TestCase
from django.conf import settings
from restclients.hrpws.appointee import get_appointee_by_netid,\
    get_appointee_by_eid, get_appointee_by_regid
from restclients.exceptions import DataFailureException


class AppointeeTest(TestCase):

    def test_get_appointee(self):
        with self.settings(
            RESTCLIENTS_UWNETID_DAO_CLASS =
                'restclients.dao_implementation.hrpws.File'):
            self.eval(get_appointee_by_netid("javerage"))
            self.eval(get_appointee_by_eid("123456789"))
            self.eval(get_appointee_by_regid(
                    "9136CCB8F66711D5BE060004AC494FFE"))


    def eval(self, ap):
        self.assertTrue(ap.is_active_emp_status())
        self.assertEqual(ap.regid,
                         "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(ap.eid,
                         "123456789")
        self.assertEqual(ap.status, "A")
        self.assertEqual(ap.status_desc, "ACTIVE")
        self.assertEqual(ap.home_dept_budget_number, "100001")
        self.assertEqual(ap.home_dept_budget_name, "UWIT GOF")
        self.assertEqual(ap.home_dept_org_code, "2100101000")
        self.assertEqual(ap.home_dept_org_name, "OVP - UW-IT")
        self.assertEqual(ap.campus_code, "1")
        self.assertEqual(ap.campus_code_desc, "On Campus")

    def test_invalid_user(self):
        with self.settings(
                RESTCLIENTS_HRPWS_DAO_CLASS =
                'restclients.dao_implementation.hrpws.File'):

            self.assertRaises(DataFailureException,
                              get_appointee_by_regid,
                              "0000000000000000000000000000000")

            self.assertRaises(DataFailureException,
                              get_appointee_by_eid,
                              "000000000")
