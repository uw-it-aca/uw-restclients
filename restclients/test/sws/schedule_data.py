from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.exceptions import DataFailureException

class SWSTestScheduleData(TestCase):
    def test_sws_schedule_data(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            
            #Valid data, shouldn't throw exceptions
            term = sws.get_previous_term()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = sws.get_current_term()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = sws.get_next_term()
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = sws.get_term_by_year_and_quarter(2012, 'summer')
            sws.schedule_for_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = sws.get_current_term()
            sws.schedule_for_regid_and_term('00000000000000000000000000000001', term)
            sws.schedule_for_regid_and_term('00000000000000000000000000000003', term)
            sws.schedule_for_regid_and_term('00000000000000000000000000000004', term)
            sws.schedule_for_regid_and_term('AABBCCDDEEFFAABBCCDDEEFFAABBCCDA', term)
            sws.schedule_for_regid_and_term('AABBCCDDEEFFAABBCCDDEEFFAABBCCDB', term)
            sws.schedule_for_regid_and_term('AABBCCDDEEFFAABBCCDDEEFFAABBCCDC', term)
            sws.schedule_for_regid_and_term('AABBCCDDEEFFAABBCCDDEEFFAABBCCDD', term)
            sws.schedule_for_regid_and_term('AABBCCDDEEFFAABBCCDDEEFFAABBCCDE', term)
            sws.schedule_for_regid_and_term('12345678901234567890123456789012', term)
          
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

