from django.test import TestCase
from django.conf import settings
from restclients.models.sws import Department, Term
from restclients.exceptions import DataFailureException
from restclients.sws.curriculum import get_curricula_by_department, get_curricula_by_term

class SWSTestCurriculum(TestCase):

    def test_curricula_for_department(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            department = Department(label="EDUC")
            curricula = get_curricula_by_department(department)

            self.assertEquals(len(curricula), 7)

            # Valid department labels, no files for them                            
            self.assertRaises(DataFailureException,                             
                              get_curricula_by_department,
                              Department(label="BIOL"))

            self.assertRaises(DataFailureException,
                              get_curricula_by_department,
                              Department(label="CSE"))

            # Test future_terms
            # Valid value but no file
            self.assertRaises(DataFailureException,
                              get_curricula_by_department,
                              department,
                              future_terms=1)

            # Valid future_terms value
            curricula = get_curricula_by_department(department,
                                                         future_terms=0)
            self.assertEquals(len(curricula), 7)

            # Invalid future_terms values
            self.assertRaises(ValueError,
                              get_curricula_by_department,
                              department,
                              future_terms=3)

            self.assertRaises(ValueError,
                              get_curricula_by_department,
                              department,
                              future_terms=-1)

            self.assertRaises(ValueError,
                              get_curricula_by_department,
                              department,
                              future_terms='x')

    def test_curricula_for_term(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = Term(quarter='winter', year=2013)
            curricula = get_curricula_by_term(term)

            self.assertEquals(len(curricula), 423)
            # Valid terms, no files for them
            self.assertRaises(DataFailureException,
                              get_curricula_by_term,
                              Term(quarter='spring', year=2012))

            self.assertRaises(DataFailureException,
                              get_curricula_by_term,
                              Term(quarter='autumn', year=2012))
