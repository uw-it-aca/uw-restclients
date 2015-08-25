import datetime
from django.test import TestCase
from django.conf import settings
from restclients.grad.committee import get_committee_by_regid


class CommitteeTest(TestCase):

    def test_get_committee_by_regid(self):
         with self.settings(
             RESTCLIENTS_GRAD_DAO_CLASS=\
                 'restclients.dao_implementation.grad.File',
             RESTCLIENTS_PWS_DAO_CLASS=\
                 'restclients.dao_implementation.iasystem.File'):
            requests = get_committee_by_regid(
                "9136CCB8F66711D5BE060004AC494FFE")

            self.assertEqual(len(requests), 3)

            committee = requests[0]
            self.assertIsNotNone(committee.json_data())
            self.assertEqual(committee.committee_type,
                             "Advisor")
            self.assertEqual(committee.status, "active")
            self.assertEqual(committee.dept, "Anthropology")
            self.assertEqual(committee.degree_title, None)
            self.assertEqual(committee.degree_type,
                             "MASTER OF PUBLIC HEALTH (EPIDEMIOLOGY)")
            self.assertEqual(committee.major_full_name, "ANTH")
            self.assertEqual(committee.start_date,
                             datetime.datetime(2012, 12, 7, 8, 26, 14))
            self.assertEqual(len(committee.members), 1)

            committee = requests[1]
            self.assertEqual(committee.committee_type,
                             "Master's Committee")
            members = committee.members
            self.assertEqual(len(members), 3)
            self.assertEqual(members[0].first_name, "Nina L.")
            self.assertEqual(members[0].last_name, "Patrick")
            self.assertEqual(members[0].member_type, "chair")
            self.assertEqual(members[0].reading_type, "chair")
            self.assertEqual(members[0].dept, "Epidemiology - Public Health")
            self.assertEqual(members[0].email, "nnn@u.washington.edu")
            self.assertEqual(members[0].status, "active")
            json_data = members[0].json_data()
            self.assertEqual(json_data["member_type"],
                             "Chair")
            self.assertEqual(json_data["reading_type"],
                             "Reading Committee Chair")

            committee = requests[2]
            self.assertEqual(committee.committee_type,
                             "Doctoral Supervisory Committee")
            members = committee.members
            self.assertEqual(len(members), 4)


    def test_empty_system(self):
         with self.settings(
             RESTCLIENTS_GRAD_DAO_CLASS=\
                 'restclients.dao_implementation.grad.File',
             RESTCLIENTS_PWS_DAO_CLASS=\
                 'restclients.dao_implementation.iasystem.File'):
             self.assertIsNone(get_committee_by_regid(
                     "00000000000000000000000000000001"))
