from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS

class SWSTestTerm(TestCase):
    def test_current_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()

            term = sws.get_current_term()
            self.assertEquals(term.year, 2012, "Return 2012 for the current year")
            self.assertEquals(term.quarter, "summer", "Return summer for the current quarter")
