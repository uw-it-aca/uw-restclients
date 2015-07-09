import datetime
from django.test import TestCase
from django.conf import settings
from restclients.grad.leave import get_leave_by_regid


class LeaveTest(TestCase):

    def test_get_leave_by_regid(self):
         with self.settings(
             RESTCLIENTS_GRAD_DAO_CLASS=\
                 'restclients.dao_implementation.grad.File',
             RESTCLIENTS_PWS_DAO_CLASS=\
                 'restclients.dao_implementation.iasystem.File'):
            requests = get_leave_by_regid(
                "9136CCB8F66711D5BE060004AC494FFE")

            self.assertEqual(len(requests), 5)
            leave = requests[0]
            self.assertEqual(leave.reason,
                             "Dissertation/Thesis research/writing")
            self.assertEqual(leave.submit_date,
                             datetime.datetime(2012, 9, 10, 9, 40, 03))
            self.assertEqual(leave.status, "paid")
            self.assertEqual(len(leave.terms), 1)
            self.assertEqual(leave.terms[0].quarter, "autumn")
            self.assertEqual(leave.terms[0].year, 2012)
