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

            self.assertEquals(term.last_final_exam_date.year, 2013)
            self.assertEquals(term.last_final_exam_date.month, 3)
            self.assertEquals(term.last_final_exam_date.day, 22)

            self.assertEquals(term.grade_submission_deadline.date().year, 2013)
            self.assertEquals(term.grade_submission_deadline.date().month, 3)
            self.assertEquals(term.grade_submission_deadline.date().day, 26)
            self.assertEquals(term.grade_submission_deadline.time().hour, 17)
            self.assertEquals(term.grade_submission_deadline.time().minute, 0)

    #Expected values will have to change when the json files are updated
    def test_next_quarter(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            term = sws.get_next_term()

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


    def test_quarter_after(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()

            starting = sws.get_next_term()
            self.assertEquals(starting.year, 2013)
            self.assertEquals(starting.quarter, 'summer')

            next1 = sws.get_term_after(starting)
            self.assertEquals(next1.year, 2013)
            self.assertEquals(next1.quarter, 'autumn')

            next2 = sws.get_term_after(next1)
            self.assertEquals(next2.year, 2014)
            self.assertEquals(next2.quarter, 'winter')

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

            # Equality tests
            self.assertEquals(sws.get_term_by_year_and_quarter(2012, 'autumn'),
                              sws.get_term_by_year_and_quarter(2012, 'autumn'))

            self.assertNotEquals(sws.get_term_by_year_and_quarter(2012, 'autumn'),
                                 sws.get_term_by_year_and_quarter(2013, 'winter'))
