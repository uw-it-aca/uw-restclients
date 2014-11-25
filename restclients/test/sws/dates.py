from django.test import TestCase
from restclients.sws import parse_sws_date
from datetime import datetime


class SWSTestDates(TestCase):
    def test_date_formats(self):
        target_date = datetime.strptime("11/04/2014", "%m/%d/%Y")
        self.assertEqual(target_date, parse_sws_date("20141104"))
        self.assertEqual(target_date, parse_sws_date("2014-11-04"))
        self.assertEqual(target_date, parse_sws_date("11/04/2014"))

        try:
            parse_sws_date("11.04.2014")
            self.fail("Didn't raise ValueError")
        except ValueError as ex:
            self.assertIn("Unknown SWS date format", ex.args)