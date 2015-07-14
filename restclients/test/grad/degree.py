import datetime
from django.test import TestCase
from django.conf import settings
from restclients.grad.degree import get_degree_by_regid


class DegreeTest(TestCase):

    def test_get_request_by_regid(self):
         with self.settings(
             RESTCLIENTS_GRAD_DAO_CLASS=\
                 'restclients.dao_implementation.grad.File',
             RESTCLIENTS_PWS_DAO_CLASS=\
                 'restclients.dao_implementation.iasystem.File'):
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
            self.assertIsNone(degree.exam_place)
            self.assertIsNone(degree.exam_date)
            self.assertEqual(degree.target_award_year, 2015)
            self.assertEqual(degree.target_award_quarter, "winter")
