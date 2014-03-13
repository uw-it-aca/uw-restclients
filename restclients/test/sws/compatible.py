from django.test import TestCase
from django.conf import settings
from datetime import datetime, timedelta
from restclients.sws import SWS
from restclients.exceptions import DataFailureException

class SWSTest(TestCase):
    def test_mock_data_fake_grading_window(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            sws = SWS()
            term = sws.get_current_term()
            self.assertEquals(term.year, 2013)
            self.assertEquals(term.quarter, 'spring')
                
            term = sws.get_term_by_year_and_quarter(2013, 'spring')
            self.assertEquals(term.year, 2013)
            self.assertEquals(term.quarter, 'spring')

            prev_term = sws.get_previous_term()
            self.assertEquals(prev_term.year, 2013)
            self.assertEquals(prev_term.quarter, 'winter')

            next_term = sws.get_next_term()
            self.assertEquals(next_term.year, 2013)
            self.assertEquals(next_term.quarter, 'summer')

            term_before = sws.get_term_before(next_term)
            self.assertEquals(term_before.year, 2013)
            self.assertEquals(term_before.quarter, 'spring')

            term_after = sws.get_term_after(prev_term)
            self.assertEquals(term_after.year, 2013)
            self.assertEquals(term_after.quarter, 'spring')

