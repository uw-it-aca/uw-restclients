from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.sws import SWS
from restclients.sws.term import Terms as TermSws

class SWSTestScheduleData(TestCase):
    def test_sws_schedule_data(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            sws = SWS()
            
            #Valid data, shouldn't throw exceptions
            term = TermSws.get_previous()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = TermSws.get_current()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = TermSws.get_next()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = TermSws.get_by_year_and_quarter(2012, 'summer')
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = TermSws.get_current()

            #Bad data, should throw exceptions
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFF", 
                              term)

            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFX", 
                              term)

            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "javerage", 
                              term)

            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "", 
                              term)

            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              " ", 
                              term)

            term.year = None
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.year = 1929
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.year = 2399
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.year = 0
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.year = -2012
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)
            
            term.quarter = "spring"
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.quarter = "fall"
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.quarter = ""
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.quarter = " "
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

            term.quarter = "Spring"
            self.assertRaises(DataFailureException, 
                              sws.schedule_for_regid_and_term, 
                              "9136CCB8F66711D5BE060004AC494FFE", 
                              term)

