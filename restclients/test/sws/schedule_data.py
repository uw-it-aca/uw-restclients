from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.sws.term import get_current_term, get_next_term, get_previous_term
from restclients.sws.term import get_term_by_year_and_quarter
from restclients.sws.registration import get_schedule_by_regid_and_term

class SWSTestScheduleData(TestCase):
    def test_sws_schedule_data(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            #Valid data, shouldn't throw exceptions
            term = get_previous_term()
            get_schedule_by_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = get_current_term()
            get_schedule_by_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = get_next_term()
            get_schedule_by_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = get_term_by_year_and_quarter(2012, 'summer')
            get_schedule_by_regid_and_term('9136CCB8F66711D5BE060004AC494FFE', term)
            term = get_current_term()

            #Bad data, should throw exceptions
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFF",
                              term)

            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFX",
                              term)

            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "javerage",
                              term)

            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "",
                              term)

            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              " ",
                              term)

            term.year = None
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.year = 1929
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.year = 2399
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.year = 0
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.year = -2012
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.quarter = "spring"
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.quarter = "fall"
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.quarter = ""
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.quarter = " "
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)

            term.quarter = "Spring"
            self.assertRaises(DataFailureException,
                              get_schedule_by_regid_and_term,
                              "9136CCB8F66711D5BE060004AC494FFE",
                              term)
