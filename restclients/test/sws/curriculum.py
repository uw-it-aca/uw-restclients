from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.models.sws import Department, Term
from restclients.exceptions import DataFailureException

class SWSTestCurriculum(TestCase):

    def test_curricula_for_department(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()

            department = Department(label="EDUC")
            curricula = sws.get_curricula_for_department(department)

            self.assertEquals(len(curricula), 7)

            # Valid department labels, no files for them                            
            self.assertRaises(DataFailureException,                             
                              sws.get_curricula_for_department,
                              Department(label="BIOL"))

            self.assertRaises(DataFailureException,
                              sws.get_curricula_for_department,
                              Department(label="CSE"))

    def test_curricula_for_term(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()

            term = Term(quarter='winter', year=2013)
            curricula = sws.get_curricula_for_term(term)

            self.assertEquals(len(curricula), 423)
            # Valid terms, no files for them
            self.assertRaises(DataFailureException,
                              sws.get_curricula_for_term,
                              Term(quarter='spring', year=2012))

            self.assertRaises(DataFailureException,
                              sws.get_curricula_for_term,
                              Term(quarter='autumn', year=2012))
