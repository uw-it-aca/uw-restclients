import datetime
from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.grad.petition import get_petition_by_regid
from restclients.test import fdao_grad_override, fdao_pws_override


@fdao_grad_override
@fdao_pws_override
class PetitionTest(TestCase):

    def test_get_petition_by_regid(self):
        requests = get_petition_by_regid(
            "9136CCB8F66711D5BE060004AC494FFE")

        self.assertEqual(len(requests), 4)
        petition = requests[0]
        self.assertIsNotNone(petition.json_data())
        self.assertEqual(petition.description,
                         "Master's degree - Extend six year limit")
        self.assertEqual(petition.submit_date,
                         datetime.datetime(2013, 5, 11, 11, 25, 35))
        self.assertEqual(petition.decision_date,
                         datetime.datetime(2013, 6, 10, 16, 32, 28))
        self.assertEqual(petition.dept_recommend, "approve")
        self.assertEqual(petition.gradschool_decision, "approved")
        self.assertTrue(petition.is_dept_approve())
        self.assertFalse(petition.is_dept_deny())
        self.assertFalse(petition.is_dept_pending())
        self.assertFalse(petition.is_dept_withdraw())
        self.assertFalse(petition.is_gs_pending())
        json_data = petition.json_data()
        self.assertIsNotNone(json_data)
        self.assertEqual(json_data['submit_date'],
                         "2013-05-11T11:25:35")
        self.assertEqual(json_data['decision_date'],
                         "2013-06-10T16:32:28")
        self.assertEqual(json_data['dept_recommend'],
                         "Approve")
        self.assertEqual(json_data['gradschool_decision'],
                         "Approved")

        petition = requests[1]
        self.assertEqual(petition.gradschool_decision, "pending")
        self.assertIsNone(petition.decision_date)
        self.assertTrue(petition.is_gs_pending())
        json_data = petition.json_data()
        self.assertIsNotNone(json_data)
        self.assertEqual(json_data['dept_recommend'],
                         "Approve")
        self.assertEqual(json_data['gradschool_decision'],
                         "Pending")


        petition = requests[2]
        self.assertEqual(petition.dept_recommend, "withdraw")
        self.assertEqual(petition.gradschool_decision, "withdraw")
        self.assertIsNone(petition.decision_date)
        self.assertTrue(petition.is_dept_withdraw())
        json_data = petition.json_data()
        self.assertIsNotNone(json_data)
        self.assertEqual(json_data['dept_recommend'],
                         "Withdraw")
        self.assertEqual(json_data['gradschool_decision'],
                         "Withdraw")


        petition = requests[3]
        self.assertEqual(petition.gradschool_decision, "withdrawn")
        self.assertIsNone(petition.decision_date)
        self.assertTrue(petition.is_dept_approve())
        json_data = petition.json_data()
        self.assertIsNotNone(json_data)
        self.assertEqual(json_data['dept_recommend'],
                         "Approve")
        self.assertEqual(json_data['gradschool_decision'],
                         "Withdrawn")

    def test_error(self):
        self.assertRaises(DataFailureException,
                          get_petition_by_regid,
                          "00000000000000000000000000000001")
