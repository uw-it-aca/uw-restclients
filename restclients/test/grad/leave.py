import datetime
from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.grad.leave import get_leave_by_regid
from restclients.test import fdao_grad_override, fdao_pws_override


@fdao_grad_override
@fdao_pws_override
class LeaveTest(TestCase):

    def test_get_leave_by_regid(self):
        requests = get_leave_by_regid(
            "9136CCB8F66711D5BE060004AC494FFE")

        self.assertEqual(len(requests), 5)
        leave = requests[0]
        self.assertIsNotNone(leave.json_data())
        self.assertEqual(leave.reason,
                         "Dissertation/Thesis research/writing")
        self.assertEqual(leave.submit_date,
                         datetime.datetime(2012, 9, 10, 9, 40, 03))
        self.assertEqual(leave.status, "paid")
        self.assertTrue(leave.is_status_paid())
        self.assertFalse(leave.is_status_approved())
        self.assertFalse(leave.is_status_denied())
        self.assertFalse(leave.is_status_requested())
        self.assertFalse(leave.is_status_withdrawn())
        self.assertEqual(len(leave.terms), 1)
        self.assertEqual(leave.terms[0].quarter, "autumn")
        self.assertEqual(leave.terms[0].year, 2012)

    def test_error(self):
        self.assertRaises(DataFailureException,
                          get_leave_by_regid,
                          "00000000000000000000000000000001")
