from django.test import TestCase
from django.conf import settings
from restclients.sws.college import get_all_colleges
from restclients.exceptions import DataFailureException

class SWSTestCollege(TestCase):

    def test_all_colleges(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            colleges = get_all_colleges()
            self.assertEquals(len(colleges), 20)
