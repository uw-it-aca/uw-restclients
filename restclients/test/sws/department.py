from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.models.sws import College 
from restclients.exceptions import DataFailureException

class SWSTestDepartment(TestCase):

    def test_departments_for_college(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()

            college = College(label="MED")
            depts = sws.get_departments_for_college(college)

            self.assertEquals(len(depts), 30)

            # Valid department labels, no files for them                            
            self.assertRaises(DataFailureException,                             
                              sws.get_departments_for_college,
                              College(label="NURS"))
