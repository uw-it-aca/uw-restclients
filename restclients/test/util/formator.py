from django.test import TestCase
from datetime import date, datetime, timedelta
from restclients.util.formator import standard_date_str
from restclients.util.formator import standard_datetime_str
from restclients.util.formator import truncate_time_str


class formatorTest(TestCase):

    def test_standard_date_str(self):
        
        self.assertEquals(standard_date_str(date(2014, 7, 4)),
                          "July 4, 2014")
        
        self.assertEquals(standard_date_str(date(2014, 6, 12)),
                          "June 12, 2014")
                                            

    def test_standard_datetime_str(self):
        self.assertEquals(standard_datetime_str(datetime(2014, 7, 4, 3, 3)),
                          "July 4, 2014 at 3:03 a.m.")
        
        self.assertEquals(standard_datetime_str(datetime(2014, 6, 12, 17, 55)),
                          "June 12, 2014 at 5:55 p.m.")
                                            

    def test_truncate_time_str(self):
        self.assertEquals(truncate_time_str(datetime(2014, 5, 2, 17, 55), 7),
                          "May 2, 2014")
        self.assertEquals(truncate_time_str(datetime(2014, 5, 2, 17, 55)),
                          "May 2, 2014 at 5:55 p.m.")
