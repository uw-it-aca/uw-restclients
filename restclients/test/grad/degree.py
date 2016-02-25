import datetime
from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.grad.degree import get_degree_by_regid


class DegreeTest(TestCase):

    def test_get_request_by_regid(self):
         with self.settings(
             RESTCLIENTS_GRAD_DAO_CLASS=\
                 'restclients.dao_implementation.grad.File',
             RESTCLIENTS_SWS_DAO_CLASS=\
                 'restclients.dao_implementation.sws.File'):
            requests = get_degree_by_regid(
                "9136CCB8F66711D5BE060004AC494FFE")

            self.assertEqual(len(requests), 6)
            degree = requests[0]
            self.assertIsNotNone(degree.json_data())
            self.assertEqual(degree.req_type, "Masters Request")
            self.assertEqual(degree.submit_date,
                             datetime.datetime(2015, 3, 11, 20, 53, 32))
            self.assertEqual(
                degree.degree_title,
                "MASTER OF LANDSCAPE ARCHITECTURE/MASTER OF ARCHITECTURE")
            self.assertEqual(degree.major_full_name,
                             "Landscape Arch/Architecture (Concurrent)")
            self.assertEqual(degree.status,
                             "Awaiting Dept Action (Final Exam)")
            self.assertTrue(degree.is_status_await())
            self.assertFalse(degree.is_status_graduated())
            self.assertFalse(degree.is_status_candidacy())
            self.assertFalse(degree.is_status_recommended())
            self.assertIsNone(degree.exam_place)
            self.assertIsNone(degree.exam_date)
            self.assertEqual(degree.target_award_year, 2015)
            self.assertEqual(degree.target_award_quarter, "winter")
            degree = requests[5]
            self.assertEqual(degree.status,
                             "Did Not Graduate")
            self.assertTrue(degree.is_status_not_graduate())

    def test_error(self):
         with self.settings(
             RESTCLIENTS_SWS_DAO_CLASS=\
                 'restclients.dao_implementation.sws.File'):
             self.assertRaises(DataFailureException,
                               get_degree_by_regid,
                               "00000000000000000000000000000001")
