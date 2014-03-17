from django.test import TestCase
from django.conf import settings
from datetime import datetime, timedelta
from restclients.exceptions import DataFailureException
from restclients.sws.term import get_term_by_year_and_quarter, get_term_before, get_term_after
from restclients.sws.term import get_current_term, get_next_term, get_previous_term


class SWSTestTerm(TestCase):

    def test_mock_data_fake_grading_window(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # This rounds down to 0 days, so check by seconds :(
            hour1_delta = timedelta(hours=-1)
            hour48_delta = timedelta(hours=-48)
            now = datetime.now()

            term = get_current_term()
            self.assertEquals(term.is_grading_period_open(), True, "Grading period is open")
            self.assertEquals(term.is_grading_period_past(), False, "Grading period is not past")

            deadline = term.grade_submission_deadline
            self.assertEquals(deadline + hour1_delta > now, True, "Deadline is in the future")
            self.assertEquals(deadline + hour48_delta < now, True, "But not too far in the future")

            open_diff_all = now - term.grading_period_open

            # Timezone configuration can mess this up, so using seconds
            self.assertEquals(open_diff_all.seconds > 0, True, "Open date is in the past")
            self.assertEquals(open_diff_all.days < 2, True, "But not too far in the past")

            open_diff_summer_a = now - term.aterm_grading_period_open
            self.assertEquals(open_diff_summer_a.seconds > 0, True, "Open date is in the past")
            self.assertEquals(open_diff_summer_a.days < 2, True, "But not too far in the past")

            # Also test for Spring 2013, as that's the "current" quarter
            term = get_term_by_year_and_quarter(2013, 'spring')

            self.assertEquals(term.is_grading_period_open(), True, "Grading period is open")
            self.assertEquals(term.is_grading_period_past(), False, "Grading period is not past")

            deadline = term.grade_submission_deadline
            self.assertEquals(deadline + hour1_delta > now, True, "Deadline is in the future")
            self.assertEquals(deadline + hour48_delta < now, True, "But not too far in the future")

            open_diff_all = now - term.grading_period_open

            # Timezone configuration can mess this up, so using seconds
            self.assertEquals(open_diff_all.seconds > 0, True, "Open date is in the past")
            self.assertEquals(open_diff_all.days < 2, True, "But not too far in the past")

            open_diff_summer_a = now - term.aterm_grading_period_open
            self.assertEquals(open_diff_summer_a.seconds > 0, True, "Open date is in the past")
            self.assertEquals(open_diff_summer_a.days < 2, True, "But not too far in the past")


    def test_current_quarter(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = get_current_term()

            expected_quarter = "spring"
            expected_year = 2013

            self.assertEquals(term.year, expected_year,
                              "Return %s for the current year" %
                              expected_year)

            self.assertEquals(term.quarter, expected_quarter,
                              "Return %s for the current quarter" %
                              expected_quarter)


    #Expected values will have to change when the json files are updated
    def test_previous_quarter(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = get_previous_term()

            expected_quarter = "winter"
            expected_year = 2013

            self.assertEquals(term.year, expected_year,
                              "Return %s for the previous year" %
                              expected_year)

            self.assertEquals(term.quarter, expected_quarter,
                              "Return %s for the previous quarter" %
                              expected_quarter)

            self.assertEquals(term.first_day_quarter.year, 2013)
            self.assertEquals(term.first_day_quarter.month, 1)
            self.assertEquals(term.first_day_quarter.day, 7)

            self.assertEquals(term.last_day_instruction.year, 2013)
            self.assertEquals(term.last_day_instruction.month, 3)
            self.assertEquals(term.last_day_instruction.day, 15)

            self.assertEquals(term.aterm_last_date, None)
            self.assertEquals(term.bterm_first_date, None)
            self.assertEquals(term.aterm_grading_period_open, None)

            self.assertEquals(term.last_final_exam_date.year, 2013)
            self.assertEquals(term.last_final_exam_date.month, 3)
            self.assertEquals(term.last_final_exam_date.day, 22)

            self.assertEquals(term.grade_submission_deadline.date().year, 2013)
            self.assertEquals(term.grade_submission_deadline.date().month, 3)
            self.assertEquals(term.grade_submission_deadline.date().day, 26)
            self.assertEquals(term.grade_submission_deadline.time().hour, 17)
            self.assertEquals(term.grade_submission_deadline.time().minute, 0)

            self.assertEquals(len(term.time_schedule_construction), 3)

            for tsc in term.time_schedule_construction:
                if tsc.campus == 'seattle':
                    self.assertEquals(tsc.is_on, False)

            self.assertEquals(term.is_grading_period_open(), False, "Grading period is not open")
            self.assertEquals(term.is_grading_period_past(), True, "Grading period is past")

    #Expected values will have to change when the json files are updated
    def test_next_quarter(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = get_next_term()

            expected_quarter = "summer"
            expected_year = 2013

            self.assertEquals(term.year, expected_year,
                              "Return %s for the next year" %
                              expected_year)

            self.assertEquals(term.quarter, expected_quarter,
                              "Return %s for the next quarter" %
                              expected_quarter)

            self.assertEquals(term.last_day_add.year, 2013)
            self.assertEquals(term.last_day_add.month, 7)
            self.assertEquals(term.last_day_add.day, 14)

            self.assertEquals(term.last_day_drop.year, 2013)
            self.assertEquals(term.last_day_drop.month, 8)
            self.assertEquals(term.last_day_drop.day, 11)

            self.assertEquals(term.first_day_quarter.year, 2013)
            self.assertEquals(term.first_day_quarter.month, 6)
            self.assertEquals(term.first_day_quarter.day, 24)

            self.assertEquals(term.last_day_instruction.year, 2013)
            self.assertEquals(term.last_day_instruction.month, 8)
            self.assertEquals(term.last_day_instruction.day, 23)

            self.assertEquals(term.aterm_last_date.year, 2013)
            self.assertEquals(term.aterm_last_date.month, 7)
            self.assertEquals(term.aterm_last_date.day, 24)

            self.assertEquals(term.bterm_first_date.year, 2013)
            self.assertEquals(term.bterm_first_date.month, 7)
            self.assertEquals(term.bterm_first_date.day, 25)

            self.assertEquals(term.aterm_last_day_add.year, 2013)
            self.assertEquals(term.aterm_last_day_add.month, 7)
            self.assertEquals(term.aterm_last_day_add.day, 14)

            self.assertEquals(term.bterm_last_day_add.year, 2013)
            self.assertEquals(term.bterm_last_day_add.month, 7)
            self.assertEquals(term.bterm_last_day_add.day, 31)

            self.assertEquals(term.last_final_exam_date.year, 2013)
            self.assertEquals(term.last_final_exam_date.month, 8)
            self.assertEquals(term.last_final_exam_date.day, 23)

            self.assertEquals(term.grade_submission_deadline.date().year, 2013)
            self.assertEquals(term.grade_submission_deadline.date().month, 8)
            self.assertEquals(term.grade_submission_deadline.date().day, 27)
            self.assertEquals(term.grade_submission_deadline.time().hour, 17)
            self.assertEquals(term.grade_submission_deadline.time().minute, 0)

            self.assertEquals(term.aterm_grading_period_open.date().year, 2013)
            self.assertEquals(term.aterm_grading_period_open.date().month, 7)
            self.assertEquals(term.aterm_grading_period_open.date().day, 18)
            self.assertEquals(term.aterm_grading_period_open.time().hour, 8)
            self.assertEquals(term.aterm_grading_period_open.time().minute, 0)

            self.assertEquals(len(term.time_schedule_construction), 3)

            for tsc in term.time_schedule_construction:
                if tsc.campus == 'bothell':
                    self.assertEquals(tsc.is_on, True)

            self.assertEquals(term.is_grading_period_open(), False, "Grading period is not open")
            self.assertEquals(term.is_grading_period_past(), True, "Grading period is past")

    def test_quarter_before(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            starting = get_next_term()
            self.assertEquals(starting.year, 2013)
            self.assertEquals(starting.quarter, 'summer')

            next1 = get_term_before(starting)
            self.assertEquals(next1.year, 2013)
            self.assertEquals(next1.quarter, 'spring')

            next2 = get_term_before(next1)
            self.assertEquals(next2.year, 2013)
            self.assertEquals(next2.quarter, 'winter')

            next3 = get_term_before(next2)
            self.assertEquals(next3.year, 2012)
            self.assertEquals(next3.quarter, 'autumn')

    def test_quarter_after(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            starting = get_next_term()
            self.assertEquals(starting.year, 2013)
            self.assertEquals(starting.quarter, 'summer')

            next1 = get_term_after(starting)
            self.assertEquals(next1.year, 2013)
            self.assertEquals(next1.quarter, 'autumn')

            next2 = get_term_after(next1)
            self.assertEquals(next2.year, 2014)
            self.assertEquals(next2.quarter, 'winter')

    def test_specific_quarters(self):
        #testing bad data - get_by_year_and_quarter
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            self.assertRaises(DataFailureException,
                              get_term_by_year_and_quarter,
                              -2012, 'summer')

            self.assertRaises(DataFailureException,
                              get_term_by_year_and_quarter,
                              0, 'summer')

            self.assertRaises(DataFailureException,
                              get_term_by_year_and_quarter,
                              1901, 'summer')

            self.assertRaises(DataFailureException,
                              get_term_by_year_and_quarter,
                              2012, 'fall')

            self.assertRaises(DataFailureException,
                              get_term_by_year_and_quarter,
                              2012, '')

            self.assertRaises(DataFailureException,
                              get_term_by_year_and_quarter,
                              2012, ' ')

            # Equality tests
            self.assertEquals(get_term_by_year_and_quarter(2012, 'autumn'),
                              get_term_by_year_and_quarter(2012, 'autumn'))

            self.assertNotEquals(get_term_by_year_and_quarter(2012, 'autumn'),
                                 get_term_by_year_and_quarter(2013, 'winter'))

    def test_week_of_term(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            now = datetime.now()
            term = get_current_term()


            term.first_day_quarter = now.date()

            # First day of class
            self.assertEquals(term.get_week_of_term(), 1, "Term starting now in first week")
            self.assertEquals(term.get_week_of_term_for_date(now), 1, "Term starting now in first week, by date")

            # Middle of the term
            start_date = now + timedelta(days=-6)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), 1, "6 days in")
            self.assertEquals(term.get_week_of_term_for_date(now), 1, "6 days in")

            start_date = now + timedelta(days=-7)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), 2, "7 days in")
            self.assertEquals(term.get_week_of_term_for_date(now), 2, "7 days in")

            start_date = now + timedelta(days=-8)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), 2, "8 days in")
            self.assertEquals(term.get_week_of_term_for_date(now), 2, "8 days in")

            start_date = now + timedelta(days=-13)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), 2, "13 days in")
            self.assertEquals(term.get_week_of_term_for_date(now), 2, "13 days in")

            start_date = now + timedelta(days=-14)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), 3, "14 days in")
            self.assertEquals(term.get_week_of_term_for_date(now), 3, "14 days in")

            # Before the term
            start_date = now + timedelta(days=1)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), -1, "-1 days")
            self.assertEquals(term.get_week_of_term_for_date(now), -1, "-1 days")

            start_date = now + timedelta(days=7)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), -1, "-7 days")
            self.assertEquals(term.get_week_of_term_for_date(now), -1, "-7 days")

            start_date = now + timedelta(days=8)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), -2, "-8 days")
            self.assertEquals(term.get_week_of_term_for_date(now), -2, "-8 days")

            start_date = now + timedelta(days=9)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), -2, "-9 days")
            self.assertEquals(term.get_week_of_term_for_date(now), -2, "-9 days")

            start_date = now + timedelta(days=14)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), -2, "-14 days")
            self.assertEquals(term.get_week_of_term_for_date(now), -2, "-14 days")

            start_date = now + timedelta(days=15)
            term.first_day_quarter = start_date.date()
            self.assertEquals(term.get_week_of_term(), -3, "-15 days")
            self.assertEquals(term.get_week_of_term_for_date(now), -3, "-15 days")

