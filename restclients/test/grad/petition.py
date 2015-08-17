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

            self.assertEqual(len(requests), 2)
            petition = requests[0]
            self.assertIsNotNone(petition.json_data())
            self.assertEqual(petition.description,
                             "Master's degree - Extend six year limit")
            self.assertEqual(petition.submit_date,
                             datetime.datetime(2013, 5, 11, 11, 25, 35))
            self.assertEqual(petition.decision_date,
                             datetime.datetime(2013, 6, 10, 16, 32, 28))
            self.assertEqual(petition.dept_recommend, "Approve")
            self.assertEqual(petition.gradschool_decision, "Approved")
            self.assertTrue(petition.is_dept_approve())
            self.assertFalse(petition.is_dept_deny())
            self.assertFalse(petition.is_dept_pending())
            self.assertFalse(petition.is_dept_withdraw())
            self.assertFalse(petition.is_gs_pending())
            self.assertIsNotNone(petition.json_data())
            petition = requests[1]
            self.assertEqual(petition.gradschool_decision, "Pending")
            self.assertIsNone(petition.decision_date)
            self.assertTrue(petition.is_gs_pending())
            self.assertIsNotNone(petition.json_data())

    def test_empty_system_key(self):
         with self.settings(
             RESTCLIENTS_GRAD_DAO_CLASS=\
                 'restclients.dao_implementation.grad.File',
             RESTCLIENTS_PWS_DAO_CLASS=\
                 'restclients.dao_implementation.iasystem.File'):
             self.assertIsNone(get_petition_by_regid(
                     "00000000000000000000000000000001"))
