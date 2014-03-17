from django.test import TestCase
from django.conf import settings
from restclients.models.sws import College 
from restclients.exceptions import DataFailureException
from restclients.sws.department import get_departments_by_college

class SWSTestDepartment(TestCase):

    def test_departments_for_college(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            college = College(label="MED")
            depts = get_departments_by_college(college)

            self.assertEquals(len(depts), 30)

            # Valid department labels, no files for them                            
            self.assertRaises(DataFailureException,                             
                              get_departments_by_college,
                              College(label="NURS"))
