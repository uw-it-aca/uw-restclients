from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.exceptions import DataFailureException

class SWSTestTerm(TestCase):

    #Expected values will have to change when the json files are updated
    def test_previous_quarter(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            term = sws.get_previous_term()

            expected_quarter = "summer"
            expected_year = 2012

            self.assertEquals(term.year, expected_year,
                              "Return %s for the previous year" %
                              expected_year)

            self.assertEquals(term.quarter, expected_quarter,
                              "Return %s for the previous quarter" %
                              expected_quarter)

            self.assertEquals(term.first_day_quarter.year, 2012)
            self.assertEquals(term.first_day_quarter.month, 6)
            self.assertEquals(term.first_day_quarter.day, 18)

            self.assertEquals(term.last_day_instruction.year, 2012)
            self.assertEquals(term.last_day_instruction.month, 8)
            self.assertEquals(term.last_day_instruction.day, 17)

            self.assertEquals(term.aterm_last_date.year, 2012)
            self.assertEquals(term.aterm_last_date.month, 7)
            self.assertEquals(term.aterm_last_date.day, 18)

            self.assertEquals(term.bterm_first_date.year, 2012)
            self.assertEquals(term.bterm_first_date.month, 7)
            self.assertEquals(term.bterm_first_date.day, 19)

            self.assertEquals(term.last_final_exam_date.year, 2012)
            self.assertEquals(term.last_final_exam_date.month, 8)
            self.assertEquals(term.last_final_exam_date.day, 17)

            self.assertEquals(term.grade_submission_deadline.date().year, 2012)
            self.assertEquals(term.grade_submission_deadline.date().month, 8)
            self.assertEquals(term.grade_submission_deadline.date().day, 21)
            self.assertEquals(term.grade_submission_deadline.time().hour, 17)
            self.assertEquals(term.grade_submission_deadline.time().minute, 0)

    def test_current_quarter(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            term = sws.get_current_term()

            expected_quarter = "summer"
            expected_year = 2012

            self.assertEquals(term.year, expected_year,
                              "Return %s for the current year" %
                              expected_year)

            self.assertEquals(term.quarter, expected_quarter,
                              "Return %s for the current quarter" %
                              expected_quarter)

            self.assertEquals(term.first_day_quarter.year, 2012)
            self.assertEquals(term.first_day_quarter.month, 6)
            self.assertEquals(term.first_day_quarter.day, 18)

            self.assertEquals(term.last_day_instruction.year, 2012)
            self.assertEquals(term.last_day_instruction.month, 8)
            self.assertEquals(term.last_day_instruction.day, 17)

            self.assertEquals(term.aterm_last_date.year, 2012)
            self.assertEquals(term.aterm_last_date.month, 7)
            self.assertEquals(term.aterm_last_date.day, 18)

            self.assertEquals(term.bterm_first_date.year, 2012)
            self.assertEquals(term.bterm_first_date.month, 7)
            self.assertEquals(term.bterm_first_date.day, 19)

            self.assertEquals(term.last_final_exam_date.year, 2012)
            self.assertEquals(term.last_final_exam_date.month, 8)
            self.assertEquals(term.last_final_exam_date.day, 17)

            self.assertEquals(term.grade_submission_deadline.date().year, 2012)
            self.assertEquals(term.grade_submission_deadline.date().month, 8)
            self.assertEquals(term.grade_submission_deadline.date().day, 21)
            self.assertEquals(term.grade_submission_deadline.time().hour, 17)
            self.assertEquals(term.grade_submission_deadline.time().minute, 0)

    #Expected values will have to change when the json files are updated
    def test_next_quarter(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            term = sws.get_next_term()

            expected_quarter = "summer"
            expected_year = 2012

            print term.year
            self.assertEquals(term.year, expected_year,
                              "Return %s for the next year" %
                              expected_year)

            self.assertEquals(term.quarter, expected_quarter,
                              "Return %s for the next quarter" %
                              expected_quarter)

            self.assertEquals(term.first_day_quarter.year, 2012)
            self.assertEquals(term.first_day_quarter.month, 6)
            self.assertEquals(term.first_day_quarter.day, 18)

            self.assertEquals(term.last_day_instruction.year, 2012)
            self.assertEquals(term.last_day_instruction.month, 8)
            self.assertEquals(term.last_day_instruction.day, 17)

            self.assertEquals(term.aterm_last_date.year, 2012)
            self.assertEquals(term.aterm_last_date.month, 7)
            self.assertEquals(term.aterm_last_date.day, 18)

            self.assertEquals(term.bterm_first_date.year, 2012)
            self.assertEquals(term.bterm_first_date.month, 7)
            self.assertEquals(term.bterm_first_date.day, 19)

            self.assertEquals(term.last_final_exam_date.year, 2012)
            self.assertEquals(term.last_final_exam_date.month, 8)
            self.assertEquals(term.last_final_exam_date.day, 17)

            self.assertEquals(term.grade_submission_deadline.date().year, 2012)
            self.assertEquals(term.grade_submission_deadline.date().month, 8)
            self.assertEquals(term.grade_submission_deadline.date().day, 21)
            self.assertEquals(term.grade_submission_deadline.time().hour, 17)
            self.assertEquals(term.grade_submission_deadline.time().minute, 0)



    def test_specific_quarters(self):
        #testing bad data - get_term_by_year_and_quarter
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            self.assertRaises(DataFailureException,
                              sws.get_term_by_year_and_quarter,
                              -2012, 'summer')

            self.assertRaises(DataFailureException,
                              sws.get_term_by_year_and_quarter,
                              0, 'summer')

            self.assertRaises(DataFailureException,
                              sws.get_term_by_year_and_quarter,
                              1901, 'summer')

            self.assertRaises(DataFailureException,
                              sws.get_term_by_year_and_quarter,
                              2012, 'fall')

            self.assertRaises(DataFailureException,
                              sws.get_term_by_year_and_quarter,
                              2012, '')

            self.assertRaises(DataFailureException,
                              sws.get_term_by_year_and_quarter,
                              2012, ' ')

