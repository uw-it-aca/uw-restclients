import datetime
from django.test import TestCase
from django.conf import settings
from restclients.grad.petition import get_petition_by_regid


class PetitionTest(TestCase):

    def test_get_petition_by_regid(self):
         with self.settings(
             RESTCLIENTS_GRAD_DAO_CLASS=\
                 'restclients.dao_implementation.grad.File',
             RESTCLIENTS_PWS_DAO_CLASS=\
                 'restclients.dao_implementation.iasystem.File'):
            requests = get_petition_by_regid(
                "9136CCB8F66711D5BE060004AC494FFE")

            self.assertEqual(len(requests), 1)
            petition = requests[0]
            self.assertEqual(petition.description,
                             "Master's degree - Extend six year limit")
            self.assertEqual(petition.submit_date,
                             datetime.datetime(2005, 7, 11, 11, 25, 35))
            self.assertEqual(petition.dept_recommend, "Approve")
            self.assertEqual(petition.gradschool_decision, "Approved")
