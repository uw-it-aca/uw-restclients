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
        self.assertEqual(ap.netid,
                         "javerage")
        self.assertEqual(ap.regid,
                         "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(ap.employee_id,
                         "123456789")
        self.assertEqual(ap.status, "A")
        self.assertEqual(ap.status_desc, "ACTIVE")
        self.assertEqual(ap.home_dept_budget_number, "100001")
        self.assertEqual(ap.home_dept_budget_name, "UWIT GOF")
        self.assertEqual(ap.home_dept_org_code, "2100101000")
        self.assertEqual(ap.home_dept_org_name, "OVP - UW-IT")
        self.assertEqual(ap.campus_code, "1")
        self.assertEqual(ap.campus_code_desc, "On Campus")

        appointments = ap.appointments
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0].app_number, 1)
        self.assertEqual(appointments[0].app_state, "Current")
        self.assertTrue(appointments[0].is_current_app_state())
        self.assertEqual(appointments[0].dept_budget_name,
                         "ACAD. & COLLAB. APP'S")
        self.assertEqual(appointments[0].dept_budget_number,
                         "100001")
        self.assertEqual(appointments[0].job_class_code,
                         "0875")
        self.assertEqual(appointments[0].job_class_title,
                         "STUDENT ASSISTANT")
        self.assertEqual(appointments[0].org_code,
                         "2101002000")
        self.assertEqual(appointments[0].org_name,
                         "ACAD. & COLLAB. APPL.")
        self.assertEqual(appointments[0].paid_app_code, "P")
        self.assertEqual(appointments[0].status, "A")
        self.assertEqual(appointments[0].status_desc, "ACTIVE")


    def test_invalid_user(self):
        with self.settings(
                RESTCLIENTS_HRPWS_DAO_CLASS =
                'restclients.dao_implementation.hrpws.File'):

            self.assertRaises(DataFailureException,
                              get_appointee_by_regid,
                              "00000000000000000000000000000001")

            self.assertRaises(DataFailureException,
                              get_appointee_by_eid,
                              "100000000")
