from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.exceptions import DataFailureException

class SWSTestTerm(TestCase):
    def test_current_quarter(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            term = sws.get_current_term()

            expected_quarter = "summer"
            expected_year = 2012
            expected_first_day_quarter = "2012-06-18"
            expected_last_day_instruction = "2012-08-17"
            expected_aterm_last_date = "2012-07-18"
            expected_bterm_first_date = "2012-07-19"
            expected_last_final_exam_date = "2012-08-17"
            
            self.assertEquals(term.year, expected_year, "Return %s for the current year" % expected_last_final_exam_date)
            self.assertEquals(term.quarter, expected_quarter, "Return %s for the current quarter" % expected_quarter)
            self.assertEquals(term.first_day_quarter, expected_first_day_quarter, "Return %s for the current first day of the quarter" % expected_first_day_quarter)
            self.assertEquals(term.last_day_instruction, expected_last_day_instruction, "Return %s for the current last day of instruction" % expected_last_day_instruction)
            self.assertEquals(term.aterm_last_date, expected_aterm_last_date, "Return %s for the current aterm last date" % expected_aterm_last_date)
            self.assertEquals(term.bterm_first_date, expected_bterm_first_date, "Return %s for the current bterm first date" % expected_bterm_first_date)
            self.assertEquals(term.last_final_exam_date, expected_last_final_exam_date, "Return %s for the current last final exam date" % expected_last_final_exam_date)            
            
    def test_specific_quarters(self):
        #bad data - get_term_by_year_and_quarter
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            self.assertRaises(DataFailureException, sws.get_term_by_year_and_quarter, -2012, 'summer')
            self.assertRaises(DataFailureException, sws.get_term_by_year_and_quarter, 0, 'summer')
            self.assertRaises(DataFailureException, sws.get_term_by_year_and_quarter, 1901, 'summer')
            self.assertRaises(DataFailureException, sws.get_term_by_year_and_quarter, 2012, 'fall')
            self.assertRaises(DataFailureException, sws.get_term_by_year_and_quarter, 2012, '')
            self.assertRaises(DataFailureException, sws.get_term_by_year_and_quarter, 2012, ' ')