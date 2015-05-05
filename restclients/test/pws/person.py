from django.test import TestCase
from django.conf import settings
from restclients.pws import PWS
from restclients.exceptions import InvalidRegID, InvalidNetID, InvalidEmployeeID
from restclients.exceptions import DataFailureException

class PWSTestPersonData(TestCase):

    def test_by_regid(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Valid data, shouldn't throw exceptions
            self._test_regid('javerage', '9136CCB8F66711D5BE060004AC494FFE')

    def test_by_netid(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Valid data, shouldn't throw exceptions
            self._test_netid('javerage', '9136CCB8F66711D5BE060004AC494FFE')

    def test_by_employeeid(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            pws = PWS()
            person = pws.get_person_by_employee_id('123456789')
            self.assertEquals(person.uwnetid, 'javerage', "Correct netid")
            self.assertEquals(person.uwregid, '9136CCB8F66711D5BE060004AC494FFE', "Correct regid")

    def test_names(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            person = pws.get_person_by_netid('javerage')
            self.assertEquals(person.surname, 'STUDENT')
            self.assertEquals(person.first_name, 'JAMES AVERAGE')
            self.assertEquals(person.full_name, 'JAMES AVERAGE STUDENT')
            self.assertEquals(person.display_name, 'James Student')

    def test_bad_netids(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Invalid data, should throw exceptions
            pws = PWS()
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, " ")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "one two")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "</html>")
            self.assertRaises(InvalidNetID, pws.get_person_by_netid, "aaaaaaaaa")
            self.assertRaises(DataFailureException, pws.get_person_by_netid, "hello")

    def test_bad_regids(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            #Invalid data, should throw exceptions
            pws = PWS()
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, "")
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, " ")
            self.assertRaises(InvalidRegID, pws.get_person_by_regid, "AAA")

            self.assertRaises(InvalidRegID,
                              pws.get_person_by_regid,
                              "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

            self.assertRaises(InvalidRegID,
                              pws.get_person_by_regid,
                              "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG")

            self.assertRaises(DataFailureException,
                              pws.get_person_by_regid,
                              "9136CCB8F66711D5BE060004AC494FFF")

    def test_bad_employee_ids(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            self.assertRaises(InvalidEmployeeID, pws.get_person_by_employee_id, "")
            self.assertRaises(InvalidEmployeeID, pws.get_person_by_employee_id, " ")
            self.assertRaises(InvalidEmployeeID, pws.get_person_by_employee_id, "A")
            self.assertRaises(InvalidEmployeeID, pws.get_person_by_employee_id, "12345678N")
            self.assertRaises(InvalidEmployeeID, pws.get_person_by_employee_id, "1")
            self.assertRaises(InvalidEmployeeID, pws.get_person_by_employee_id, "1234567890")

    def test_compare_persons(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()

            person1 = pws.get_person_by_regid("7718EB38AE3411D689DA0004AC494FFE")
            person2 = pws.get_person_by_regid("7718EB38AE3411D689DA0004AC494FFE")
            person3 = pws.get_person_by_regid("9136CCB8F66711D5BE060004AC494FFE")

            self.assertEquals(person1 == person2, True, "persons are equal")
            self.assertEquals(person1 == person3, False, "persons are inequal")

    def test_affiliation_data(self):
         with self.settings(
                 RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
             pws = PWS()

             person1 = pws.get_person_by_netid("javerage")
             self.assertEquals(person1.is_student, True)
             self.assertEquals(person1.is_alum, True)
             self.assertEquals(person1.is_staff, True)
             self.assertEquals(person1.is_faculty, None)
             self.assertEquals(person1.is_employee, True)

             self.assertEquals(person1.mailstop, None, "MailStop")
             self.assertEquals(person1.home_department, "C&C TEST BUDGET",
                               "HomeDepartment")

    def _test_regid(self, netid, regid):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            pws = PWS()
            person = pws.get_person_by_regid(regid)

            self.assertEquals(person.uwnetid, netid, netid + "'s netid")
            self.assertEquals(person.uwregid, regid, netid + "'s regid")

    def _test_netid(self, netid, regid):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            pws = PWS()
            person = pws.get_person_by_netid(netid)

            self.assertEquals(person.uwnetid, netid, netid + "'s netid")
            self.assertEquals(person.uwregid, regid, netid + "'s regid")
